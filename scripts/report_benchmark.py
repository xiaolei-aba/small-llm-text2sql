"""Combine E5 repeat-zero quality with all-three-repeat timing; never mix splits."""
import csv
import hashlib
import json
import statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def main():
    config=json.loads((ROOT/'configs/e5.json').read_text())
    manifest_path=ROOT/'data/manifests/e5_benchmark.json'
    manifest_hash=hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    records=[]
    for condition in config['conditions']:
        name=condition['name'];source=ROOT/'results/predictions'/f'{name}.jsonl'
        profile=json.loads(source.with_suffix('.profile.json').read_text())
        quality=json.loads((ROOT/'results'/f'{name}_summary.json').read_text())
        assert profile['predictions_sha256']==quality['predictions_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
        times=sorted(b['seconds']*1000 for b in profile['batches'] for _ in range(b['requests']))
        per_repeat=[]
        for repeat in range(config['repetitions']):
            group=[b for b in profile['batches'] if b['repeat']==repeat]
            per_repeat.append(sum(b['tokens'] for b in group)/sum(b['seconds'] for b in group))
        row={**quality,'experiment_id':'E5','run_id':name,'status':'completed','model':profile['model']['repo_id'],
             'model_revision':profile['model']['revision'],'method':'zero_shot_precision_batch',
             'dataset':'Spider 1.0','dataset_revision':'zip_sha256:00636695dabed6b5f4b8328a16b13e069a2f16591d5efcce57660669c85b121b',
             'split':'dev_benchmark_32','split_manifest_sha256':manifest_hash,'train_samples':0,'seed':42,
             'quantization':'none','compute_dtype':condition['dtype'],'max_new_tokens':256,
             'schema_version':'spider_schema_v2','prompt_version':'sqlite_zero_shot_v1',
             'peak_vram_gb':profile['peak_allocated_bytes']/1e9,'peak_reserved_vram_gb':profile['peak_reserved_bytes']/1e9,
             'latency':statistics.mean(times),'latency_p50_ms':statistics.median(times),
             'latency_p95_ms':times[min(len(times)-1,int(.95*len(times)))],
             'throughput':profile['throughput'],'requests_per_second':profile['requests_per_second'],
             'generated_tokens':profile['generated_tokens'],'benchmark_requests':profile['benchmark_requests'],
             'inference_backend':'transformers_sdpa','concurrency':1,'inference_batch_size':condition['batch_size'],
             'eval_protocol':'single_db_ex_official_result_eq_keep_distinct',
             'evaluator_commit':'e97acc546ecbee8fa27fa8dbf025ef61493a876c','git_commit':profile['git_commit'],
             'environment_file':'docs/environment_e1.txt','config_file':'configs/e5.json',
             'predictions_file':str(source.relative_to(ROOT)),
             'notes':'32 length-stratified requests; quality=repeat0; speed=all3 repeats; batch latency is completion time; no vLLM/quantization',
             'per_repeat_throughput':per_repeat,'repeat_output_changes':profile['repeat_output_changes'],
             'load_seconds':profile['load_seconds']}
        if condition.get('adapter'):
            training=json.loads((ROOT/'results'/f"{Path(condition['adapter']).name}_training.json").read_text())
            assert training['adapter_sha256']==profile['adapter_sha256']
            row.update(method='lora_merged' if condition['merge'] else 'lora_unmerged',train_samples=training['train_samples'],
                       lora_rank=training['config']['rank'],lora_alpha=training['config']['alpha'],
                       adapter_sha256=profile['adapter_sha256'])
            row['notes']+='; same completed E1 adapter, inference only; load_seconds includes merge if enabled'
        row['environment_file']='docs/environment_e5.json'
        records.append(row)
    target=ROOT/'results/metrics.csv'
    with target.open(newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames;existing=list(reader)
    if 'inference_batch_size' not in fields:fields.append('inference_batch_size')
    ids={r['run_id'] for r in existing}
    with target.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(existing)
        writer.writerows(r for r in records if r['run_id'] not in ids)
    by_name={r['run_id']:r for r in records}
    pairs=[]
    for baseline,candidate in [('e5_bf16_b1','e5_bf16_b2'),('e5_bf16_b1','e5_fp16_b1'),
                               ('e5_fp16_b1','e5_fp16_b2'),('e5_lora_unmerged_b1','e5_lora_merged_b1')]:
        def read_rows(path):
            return {r['sample_id']:r for r in [json.loads(l) for l in path.read_text(encoding='utf-8').splitlines()]}
        a=read_rows(ROOT/'results/predictions'/f'{baseline}.jsonl')
        b=read_rows(ROOT/'results/predictions'/f'{candidate}.jsonl')
        ae=read_rows(ROOT/'results'/f'{baseline}_evaluation.jsonl')
        be=read_rows(ROOT/'results'/f'{candidate}_evaluation.jsonl')
        assert set(a)==set(b)==set(ae)==set(be) and len(a)==config['samples']
        pairs.append({'baseline':baseline,'candidate':candidate,
            'throughput_ratio':by_name[candidate]['throughput']/by_name[baseline]['throughput'],
            'first_repeat_raw_output_changes':sum(a[i]['raw_output']!=b[i]['raw_output'] for i in a),
            'first_repeat_improved':sum(not ae[i]['execution_correct'] and be[i]['execution_correct'] for i in a),
            'first_repeat_regressed':sum(ae[i]['execution_correct'] and not be[i]['execution_correct'] for i in a)})
    (ROOT/'results/e5_summary.json').write_text(json.dumps({'conditions':records,'paired_conditions':pairs,
        'manifest_sha256':manifest_hash},indent=2)+'\n')
    lines=['# E5 原生推理实测','','基座模型同一revision，固定32请求，质量只取第1轮，速度取3轮共96次请求。以下EX不能和1034全量dev直接比较；非vLLM、非量化。',
       '', '|条件|32条EX|可执行率|平均完成延迟ms|输出token/s|峰值allocated GB|三轮token/s|','|---|---:|---:|---:|---:|---:|---|']
    for r in records:
        rounds=', '.join(f'{v:.2f}' for v in r['per_repeat_throughput'])
        lines.append(f"|{r['run_id']}|{r['execution_accuracy']:.2%}|{r['valid_sql_rate']:.2%}|{r['latency']:.2f}|{r['throughput']:.2f}|{r['peak_vram_gb']:.3f}|{rounds}|")
    lines+=['','批量完成延迟不除以batch size；吞吐分母为各batch墙钟时间之和。数值精度/批量形状可能改变greedy输出，不能只比较速度忽略质量。单机固定条件顺序、样本较少、频率/温度/后台负载会影响结果；不推广为普适倍数。']
    for r in records:lines.append(f"- {r['run_id']}：重复间输出变化 {r['repeat_output_changes']}；模型加载 {r['load_seconds']:.2f}s。")
    lines+=['','## 配对变化（只针对这32条输入）','',
            '|对照→候选|输出token/s比值|首轮原始输出改变|改对|改错|','|---|---:|---:|---:|---:|']
    for p in pairs:
        lines.append(f"|{p['baseline']}→{p['candidate']}|{p['throughput_ratio']:.3f}x|{p['first_repeat_raw_output_changes']}|{p['first_repeat_improved']}|{p['first_repeat_regressed']}|")
    lines+=['','比值对应各自实际生成输出，若输出长度/内容改变就不能解释为严格固定生成token轨迹的内核加速。合并可能引入BF16舍入；32条质量相同也不能证明全量质量无损。']
    (ROOT/'docs/e5_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['run_id','execution_accuracy','latency','throughput','peak_vram_gb']} for r in records],indent=2))


if __name__=='__main__':main()
