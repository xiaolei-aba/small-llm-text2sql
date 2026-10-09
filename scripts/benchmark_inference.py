"""E5 native Transformers precision/batch comparison, after core E0-E3 only.

32 length-stratified dev requests, three repeats, identical generation settings.
Quality uses repeat zero; all repeats measure speed. This is not a full-dev score.
"""
import gc
import hashlib
import importlib.metadata
import json
import random
import statistics
import subprocess
import sys
import time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.data.schema import load_schema_index,format_schema
from src.data.prompt import messages
from src.inference.postprocess import extract_sql


def gpu_snapshot():
    try:
        return subprocess.check_output(['nvidia-smi',
            '--query-gpu=name,memory.used,memory.total,temperature.gpu,power.draw,clocks.sm',
            '--format=csv'],text=True,timeout=10).strip()
    except (OSError,subprocess.SubprocessError) as exc:
        return 'Snapshot unavailable: '+repr(exc)


def run_condition(condition,records,dev,schemas,lock,config,output):
    import torch
    from transformers import AutoModelForCausalLM,AutoTokenizer
    dtype=getattr(torch,condition['dtype']);batch_size=condition['batch_size']
    torch.manual_seed(config['seed'])
    hardware_before=gpu_snapshot()
    begin=time.perf_counter()
    tok=AutoTokenizer.from_pretrained(ROOT/lock['local_dir'],local_files_only=True,padding_side='left')
    tok.pad_token_id=tok.eos_token_id
    model=AutoModelForCausalLM.from_pretrained(ROOT/lock['local_dir'],local_files_only=True,
                 dtype=dtype,device_map={'':'cuda:0'},attn_implementation='sdpa').eval()
    adapter_hash=None
    if condition.get('adapter'):
        from peft import PeftModel
        adapter=ROOT/condition['adapter']
        training=json.loads((ROOT/'results'/f'{adapter.name}_training.json').read_text())
        adapter_hash=hashlib.sha256((adapter/'adapter_model.safetensors').read_bytes()).hexdigest()
        if training['status']!='completed' or training['adapter_sha256']!=adapter_hash:
            raise RuntimeError('Benchmark adapter integrity mismatch')
        model=PeftModel.from_pretrained(model,adapter).eval()
        if condition['merge']:model=model.merge_and_unload(safe_merge=True).eval()
    torch.cuda.synchronize();load=time.perf_counter()-begin
    kwargs=dict(do_sample=config['do_sample'],num_beams=config['num_beams'],
                max_new_tokens=config['max_new_tokens'],repetition_penalty=config['repetition_penalty'],
                pad_token_id=tok.eos_token_id)
    with torch.inference_mode():
        warm=tok.apply_chat_template(messages('Count rows in table t.','Table t: x INTEGER'),
                                      tokenize=True,add_generation_prompt=True,return_tensors='pt').to('cuda')
        model.generate(warm,attention_mask=torch.ones_like(warm),do_sample=False,max_new_tokens=8,pad_token_id=tok.eos_token_id)
    del warm
    torch.cuda.synchronize();torch.cuda.reset_peak_memory_stats()
    identity=[config,condition,records,lock]
    if adapter_hash:identity.append(adapter_hash)
    fingerprint=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    batches=[];first=[];outputs={};changed=0
    trace_path=ROOT/'results/profiles'/f"{condition['name']}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}.jsonl"
    trace_path.parent.mkdir(parents=True,exist_ok=True)
    with trace_path.open('x',encoding='utf-8') as trace,torch.inference_mode():
        for repeat in range(config['repetitions']):
            for offset in range(0,len(records),batch_size):
                group=records[offset:offset+batch_size]
                torch.cuda.synchronize();start=time.perf_counter()
                texts=[tok.apply_chat_template(messages(dev[r['index']]['question'],schemas[r['db_id']]),
                         tokenize=False,add_generation_prompt=True) for r in group]
                inputs=tok(texts,add_special_tokens=False,padding=True,return_tensors='pt').to('cuda')
                n=inputs['input_ids'].shape[1]
                if n>config['max_input_tokens']:raise RuntimeError('No silent truncation')
                generated=model.generate(**inputs,**kwargs)[:,n:]
                torch.cuda.synchronize()
                row_outputs=[]
                eos=model.generation_config.eos_token_id
                stops=set(eos if isinstance(eos,list) else [eos])
                for tokens in generated.tolist():
                    end=next((i+1 for i,t in enumerate(tokens) if t in stops),len(tokens))
                    tokens=tokens[:end]
                    row_outputs.append((tok.decode(tokens,skip_special_tokens=True),len(tokens),bool(tokens and tokens[-1] in stops)))
                elapsed=time.perf_counter()-start
                batch_id=f'{repeat}:{offset//batch_size}'
                batches.append({'repeat':repeat,'batch_id':batch_id,'seconds':elapsed,'requests':len(group),
                                'tokens':sum(n for raw,n,ended in row_outputs)})
                for record,(raw,count,ended) in zip(group,row_outputs):
                    ex=dev[record['index']]
                    row={**record,'question':ex['question'],'gold_sql':ex['query'],
                         'raw_output':raw,'generated_sql':extract_sql(raw),'generated_tokens':count,
                         'generation_time':elapsed,'batch_id':batch_id,'generation_status':'ok',
                         'truncated':count==config['max_new_tokens'] and not ended,'ended_on_eos':ended,'config_hash':fingerprint,
                         'peak_allocated_bytes':torch.cuda.max_memory_allocated(),
                         'peak_reserved_bytes':torch.cuda.max_memory_reserved()}
                    if repeat==0:first.append(row);outputs[row['sample_id']]=raw
                    elif outputs[row['sample_id']]!=raw:changed+=1
                    trace.write(json.dumps({'repeat':repeat,**row},ensure_ascii=False)+'\n')
                trace.flush()
            print(condition['name'],'repeat',repeat+1,'/',config['repetitions'],flush=True)
    latencies=[b['seconds']*1000 for b in batches for _ in range(b['requests'])]
    profile={'completed':True,'condition':condition,'config':{**config,'dtype':condition['dtype']},'config_file':'configs/e5.json',
       'model':lock,'adapter':condition.get('adapter'),'adapter_sha256':adapter_hash,
       'config_hash':fingerprint,'load_seconds':load,
       'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
       'effective_generation_config':{**model.generation_config.to_dict(),**kwargs},
       'peak_allocated_bytes':torch.cuda.max_memory_allocated(),'peak_reserved_bytes':torch.cuda.max_memory_reserved(),
       'benchmark_requests':sum(b['requests'] for b in batches),'generated_tokens':sum(b['tokens'] for b in batches),
       'generation_seconds':sum(b['seconds'] for b in batches),'latency_ms':statistics.mean(latencies),
       'throughput':sum(b['tokens'] for b in batches)/sum(b['seconds'] for b in batches),
       'requests_per_second':sum(b['requests'] for b in batches)/sum(b['seconds'] for b in batches),
       'repeat_output_changes':changed,'batches':batches,'trace':str(trace_path.relative_to(ROOT)),
       'hardware_before':hardware_before,'hardware_after':gpu_snapshot(),
       'timing_note':'Every member latency equals batch completion time; throughput divides by unique batch wall times, not summed member latencies'}
    with output.open('x',encoding='utf-8') as f:
        for row in first:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    profile['predictions_sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix('.profile.json').write_text(json.dumps(profile,indent=2)+'\n')
    del model
    return profile


def main():
    if Path(sys.prefix).name!='text2sql':raise RuntimeError('Use text2sql')
    if not (ROOT/'results/e3_dev_summary.json').exists():raise RuntimeError('Complete E0-E3 before E5')
    import torch
    packages={name:importlib.metadata.version(name) for name in ['torch','transformers','peft','accelerate','numpy']}
    try:packages['bitsandbytes']=importlib.metadata.version('bitsandbytes')
    except importlib.metadata.PackageNotFoundError:pass
    (ROOT/'docs/environment_e5.json').write_text(json.dumps({'python':sys.version,'packages':packages,
        'cuda':torch.version.cuda,'gpu':torch.cuda.get_device_name(0),
        'capability':torch.cuda.get_device_capability(0)},indent=2)+'\n')
    lock=json.loads((ROOT/'configs/model_lock.json').read_text())
    config=json.loads((ROOT/'configs/e5.json').read_text())
    all_records=json.loads((ROOT/'data/manifests/e0_dev.json').read_text())['records']
    ordered=sorted(all_records,key=lambda r:(r['prompt_tokens'],r['index']))
    records=[ordered[round(i*(len(ordered)-1)/(config['samples']-1))] for i in range(config['samples'])]
    random.Random(config['seed']).shuffle(records)
    (ROOT/'data/manifests/e5_benchmark.json').write_text(json.dumps({'selection':'32 evenly spaced input length order statistics, then seed42 shuffle; no gold-based selection','records':records},indent=2)+'\n')
    data=ROOT/'data/raw/spider/spider_data';dev=json.loads((data/'dev.json').read_text())
    index=load_schema_index(data/'tables.json')
    schemas={db:format_schema(db,index,data/'database'/db/(db+'.sqlite')) for db in {r['db_id'] for r in records}}
    conditions=list(config['conditions']);random.Random(config['seed']).shuffle(conditions)
    for condition in conditions:
        output=ROOT/'results/predictions'/f"{condition['name']}.jsonl"
        if output.exists():
            profile=json.loads(output.with_suffix('.profile.json').read_text())
            identity=[config,condition,records,lock]
            if condition.get('adapter'):
                identity.append(hashlib.sha256((ROOT/condition['adapter']/'adapter_model.safetensors').read_bytes()).hexdigest())
            expected=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
            if not profile['completed'] or profile['config_hash']!=expected or profile['predictions_sha256']!=hashlib.sha256(output.read_bytes()).hexdigest():
                raise RuntimeError('Existing incomplete/corrupt benchmark; inspect before rerun')
            print('Preserved completed condition',condition['name']);continue
        gc.collect();torch.cuda.empty_cache()
        run_condition(condition,records,dev,schemas,lock,config,output)
    print('All benchmark generation completed; score repeat-zero outputs separately')


if __name__=='__main__':main()
