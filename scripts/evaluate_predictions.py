"""Single-db EX with fixed upstream comparison, isolated per-sample deadlines."""
import argparse
import csv
import hashlib
import json
import multiprocessing as mp
import statistics
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.evaluation.safe_sql import execute
from src.evaluation.official import result_equal


def worker(send,db,gold,pred):
    try:
        g=execute(gold,db)
        p=execute(pred,db)
        correct=bool(g['ok'] and p['ok'] and result_equal(g['rows'],p['rows'],gold))
        send.send({'gold_ok':g['ok'],'gold_error':g['error'],'execution_success':p['ok'],
                   'execution_error':p['error'],'execution_correct':correct})
    except Exception as exc:
        send.send({'evaluation_error':repr(exc)})
    finally:
        send.close()


def score(db,gold,pred):
    recv,send=mp.Pipe(duplex=False)
    process=mp.Process(target=worker,args=(send,db,gold,pred))
    process.start(); send.close()
    try:
        if not recv.poll(15):
            process.terminate(); process.join()
            return {'evaluation_error':'15s evaluator process deadline; gold/pred stage unknown'}
        result=recv.recv()
        process.join(2)
        if process.is_alive():
            process.terminate(); process.join()
        return result
    finally:
        recv.close()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--predictions',required=True)
    ap.add_argument('--manifest',required=True)
    ap.add_argument('--run-id',required=True)
    ap.add_argument('--experiment',default='E0')
    ap.add_argument('--record-metrics',action='store_true')
    args=ap.parse_args()
    if Path(sys.prefix).name!='text2sql':
        raise RuntimeError('Use text2sql')
    source=ROOT/args.predictions
    rows=[json.loads(l) for l in source.read_text(encoding='utf-8').splitlines()]
    ids=[r['sample_id'] for r in rows]
    manifest=json.loads((ROOT/args.manifest).read_text())
    expected=[r['sample_id'] for r in manifest['records']]
    if len(ids)!=len(set(ids)) or set(ids)!=set(expected):
        raise RuntimeError('Incomplete/duplicate predictions: refuse denominator change')
    dev=json.loads((ROOT/'data/raw/spider/spider_data/dev.json').read_text())
    expected_rows={r['sample_id']:r for r in manifest['records']}
    for row in rows:
        entry=expected_rows[row['sample_id']];official=dev[entry['index']]
        if row['db_id']!=official['db_id'] or row['gold_sql']!=official['query'] or row['difficulty']!=entry['difficulty']:
            raise RuntimeError('Prediction metadata no longer matches original dev and manifest')
    target=ROOT/'results'/f'{args.run_id}_evaluation.jsonl'
    done={}
    source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    if target.exists():
        done={r['sample_id']:r for r in [json.loads(l) for l in target.read_text(encoding='utf-8').splitlines()]}
        if any(r['predictions_sha256']!=source_hash for r in done.values()):
            raise RuntimeError('Prediction file changed since evaluation')
    with target.open('a',encoding='utf-8') as out:
        for row in rows:
            if row['sample_id'] in done:
                continue
            db=ROOT/'data/raw/spider/spider_data/database'/row['db_id']/(row['db_id']+'.sqlite')
            result=score(str(db),row['gold_sql'],row['generated_sql'])
            if result.get('evaluation_error') or not result.get('gold_ok'):
                raise RuntimeError(f"Evaluation blocked: {row['sample_id']}: {result}")
            result.update(sample_id=row['sample_id'],difficulty=row['difficulty'],predictions_sha256=source_hash)
            out.write(json.dumps(result)+'\n');out.flush();done[row['sample_id']]=result
            if len(done)%50==0:
                print('Scored',len(done),'/',len(rows),flush=True)
    values=list(done.values())
    summary={'run_id':args.run_id,'eval_samples':len(values),'predictions_sha256':source_hash,
             'execution_accuracy':sum(r['execution_correct'] for r in values)/len(values),
             'valid_sql_rate':sum(r['execution_success'] for r in values)/len(values),
             'generation_failures':sum(r['generation_status']!='ok' for r in rows),
             'truncated_outputs':sum(r.get('truncated',False) for r in rows)}
    for difficulty in ['easy','medium','hard','extra']:
        subset=[r for r in values if r['difficulty']==difficulty]
        key='extra_hard' if difficulty=='extra' else difficulty
        summary[key+'_samples']=len(subset)
        summary[key+'_accuracy']=sum(r['execution_correct'] for r in subset)/len(subset) if subset else None
    timings=sorted(r['generation_time']*1000 for r in rows)
    batch_times={r.get('batch_id',r['sample_id']):r['generation_time'] for r in rows}
    total_generation_seconds=sum(batch_times.values())
    summary.update(latency=statistics.mean(timings),latency_p50_ms=statistics.median(timings),
        latency_p95_ms=timings[min(len(timings)-1,int(.95*len(timings)))],
        throughput=sum(r['generated_tokens'] for r in rows)/total_generation_seconds,
        peak_vram_gb=max(r['peak_allocated_bytes'] for r in rows)/1e9,
        peak_reserved_vram_gb=max(r['peak_reserved_bytes'] for r in rows)/1e9)
    (ROOT/'results'/f'{args.run_id}_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    if args.record_metrics:
        path=ROOT/'results/metrics.csv'
        with path.open(newline='') as f:
            reader=csv.DictReader(f);fields=reader.fieldnames;existing=list(reader)
        if any(r['run_id']==args.run_id for r in existing):
            print('Metrics row already exists, not duplicated');return
        lock=json.loads((ROOT/'configs/model_lock.json').read_text())
        profile=json.loads(source.with_suffix('.profile.json').read_text())
        record={**summary,'experiment_id':args.experiment,'status':'completed','model':lock['repo_id'],
          'git_commit':profile.get('git_commit',''),
          'split_manifest_sha256':hashlib.sha256((ROOT/args.manifest).read_bytes()).hexdigest(),
          'dataset_revision':'zip_sha256:00636695dabed6b5f4b8328a16b13e069a2f16591d5efcce57660669c85b121b',
          'environment_file':'docs/environment_e0.txt','generated_tokens':sum(r['generated_tokens'] for r in rows),
          'benchmark_requests':len(rows),'requests_per_second':len(rows)/total_generation_seconds,
          'model_revision':lock['revision'],'method':'lora_sft' if profile.get('adapter') else 'zero_shot',
          'dataset':'Spider 1.0','split':'dev' if len(rows)==1034 else f'dev_subset_{len(rows)}',
          'train_samples':'' if profile.get('adapter') else 0,
          'seed':42,'quantization':'none','compute_dtype':profile['config']['dtype'],'max_new_tokens':256,
          'schema_version':'spider_schema_v2','prompt_version':'sqlite_zero_shot_v1',
          'inference_backend':'transformers','concurrency':1,
          'eval_protocol':'single_db_ex_official_result_eq_keep_distinct',
          'evaluator_commit':'e97acc546ecbee8fa27fa8dbf025ef61493a876c',
          'predictions_file':args.predictions,'config_file':profile.get('config_file','configs/e0.json'),
          'notes':'EX using original single DB; no TSA/EM; generated token/s excludes SQL evaluation'}
        if profile.get('adapter'):
            train=json.loads((ROOT/'results'/f"{Path(profile['adapter']).name}_training.json").read_text())
            if train['status']!='completed' or train['adapter_sha256']!=profile['adapter_sha256']:
                raise RuntimeError('Training artifact and inference adapter mismatch')
            cfg=train['config']
            if cfg.get('quantization','none')!=profile.get('quantization','none'):
                raise RuntimeError('Training/inference quantization policy mismatch')
            record.update(train_samples=train['train_samples'],train_examples_seen=train['train_examples_seen'],
                train_tokens_seen=train['train_tokens_seen'],train_time=train['train_seconds'],
                lora_rank=cfg['rank'],lora_alpha=cfg['alpha'],lora_dropout=cfg['dropout'],
                target_modules=';'.join(cfg['target_modules']),optimizer=cfg['optimizer'],
                max_seq_length=cfg['max_sequence_length'],micro_batch_size=cfg['micro_batch_size'],
                gradient_accumulation_steps=cfg['gradient_accumulation_steps'],optimizer_steps=train['optimizer_steps'],
                sampling_policy=cfg['sampling_policy'],config_file='results/'+Path(profile['adapter']).name+'_training.json',
                train_peak_vram_gb=train['peak_allocated_bytes']/1e9,
                train_peak_reserved_vram_gb=train['peak_reserved_bytes']/1e9,
                supervised_tokens_seen=train['supervised_tokens'],
                train_tokens_per_second=train['train_tokens_seen']/train['train_seconds'],
                adapter_sha256=profile['adapter_sha256'],environment_file='docs/environment_e1.txt')
            if cfg.get('quantization','none')!='none':
                record.update(method='qlora_sft',quantization=cfg['quantization'],environment_file='docs/environment_e4.txt')
            elif cfg.get('loss_difficulty_weights'):
                record['method']='complexity_weighted_lora_sft'
                record['notes']+='; global mean-one loss weights: '+json.dumps(cfg['loss_difficulty_weights'],sort_keys=True)
            record['notes']+='; train config and timings: results/'+Path(profile['adapter']).name+'_training.json'
        with path.open('a',newline='') as f:
            csv.DictWriter(f,fieldnames=fields,extrasaction='ignore').writerow(record)


if __name__=='__main__':
    mp.freeze_support()
    main()
