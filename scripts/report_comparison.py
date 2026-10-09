"""Render completed full-dev measurements; no inferred or placeholder scores."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_run(run):
    summary = json.loads((ROOT / 'results' / f'{run}_summary.json').read_text())
    source = ROOT / 'results/predictions' / f'{run}.jsonl'
    profile = json.loads(source.with_suffix('.profile.json').read_text())
    rows = [json.loads(line) for line in source.read_text(encoding='utf-8').splitlines()]
    assert summary['eval_samples'] == len(rows) == len({r['sample_id'] for r in rows}) == 1034
    assert hashlib.sha256(source.read_bytes()).hexdigest() == summary['predictions_sha256']
    training = None
    if profile.get('adapter'):
        name = Path(profile['adapter']).name
        training = json.loads((ROOT / 'results' / f'{name}_training.json').read_text())
        assert training['status'] == 'completed'
        assert training['adapter_sha256'] == profile['adapter_sha256']
    return summary, profile, training, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', required=True)
    parser.add_argument('--candidate', required=True)
    parser.add_argument('--output', required=True, help='Markdown stem inside docs')
    parser.add_argument('--analysis', help='Optional completed paired-analysis JSON stem inside results')
    args = parser.parse_args()
    runs = {name: load_run(name) for name in [args.baseline, args.candidate]}
    names = list(runs)
    a, b = [runs[name][0] for name in names]
    assert {r['sample_id'] for r in runs[names[0]][3]} == {r['sample_id'] for r in runs[names[1]][3]}
    lines = [f'# {args.baseline} → {args.candidate} 实测对照', '',
             '同一固定 1034 条 Spider dev、完整 schema、零样本任务 Prompt、greedy 生成（repetition_penalty=1.1）及只读单库 EX。只评预算结束的 adapter，未按 dev 挑 checkpoint。', '',
             f'|指标|{names[0]}|{names[1]}|变化|', '|---|---:|---:|---:|']
    for key in ['execution_accuracy', 'valid_sql_rate', 'easy_accuracy', 'medium_accuracy',
                'hard_accuracy', 'extra_hard_accuracy']:
        lines.append(f'|{key}|{a[key]:.2%}|{b[key]:.2%}|{100*(b[key]-a[key]):+.2f} 百分点|')
    pooled = [(s['hard_accuracy'] * s['hard_samples'] + s['extra_hard_accuracy'] * s['extra_hard_samples']) /
              (s['hard_samples'] + s['extra_hard_samples']) for s in [a, b]]
    lines.append(f'|hard+extra-hard 合并（340条）|{pooled[0]:.2%}|{pooled[1]:.2%}|{100*(pooled[1]-pooled[0]):+.2f} 百分点|')
    for key in ['generation_failures', 'truncated_outputs', 'latency', 'latency_p95_ms',
                'throughput', 'peak_vram_gb', 'peak_reserved_vram_gb']:
        lines.append(f'|{key}|{a[key]:.3f}|{b[key]:.3f}|{b[key]-a[key]:+.3f}|')
    lines += ['', 'Latency 单位 ms/request；throughput 为输出 token/s，计时不含模型加载和 SQL 评分。显存单位十进制 GB；reserved 包含缓存。模型输出长度可能不同，因此全量生成速度差异不能完全归因于加载后端。', '']
    if args.analysis:
        analysis = json.loads((ROOT / 'results' / f'{args.analysis}.json').read_text(encoding='utf-8'))
        paired = analysis['comparisons'][args.candidate]
        assert paired['baseline'] == args.baseline
        lower, upper = paired['db_cluster_bootstrap_95_ci']
        lines += ['## 配对结果', '',
                  f"改对 {paired['improved']} 条、改错 {paired['regressed']} 条。20个数据库聚类bootstrap的总体EX差值95%区间为 [{100*lower:+.2f}, {100*upper:+.2f}] 个百分点（10000次，seed42）。",
                  f'完整错误诊断与案例：docs/{args.analysis}.md；这是多标签启发式，不是确定因果。', '']
    for name, (summary, profile, train, rows) in runs.items():
        lines += [f'## {name} 证据',
                  f"- 预测 SHA256：`{summary['predictions_sha256']}`。",
                  f"- 原始输出：`results/predictions/{name}.jsonl`；逐条评分：`results/{name}_evaluation.jsonl`；汇总：`results/{name}_summary.json`。",
                  f"- 输出 token：{sum(r['generated_tokens'] for r in rows)}；生成代码 commit：`{profile.get('git_commit', '未记录')}`。"]
        if train:
            lines += [f"- 训练 {train['train_examples_seen']} 条曝光 / {train['train_samples']} 唯一样本 / {train['optimizer_steps']} 步；序列 token {train['train_tokens_seen']}，监督 token {train['supervised_tokens']}。",
                      f"- 训练循环 {train['train_seconds']:.3f} 秒；allocated {train['peak_allocated_bytes']/1e9:.3f} GB；reserved {train['peak_reserved_bytes']/1e9:.3f} GB。",
                      f"- adapter SHA256：`{train['adapter_sha256']}`；训练配置与恢复历史：`results/{Path(profile['adapter']).name}_training.json`。"]
            if train.get('resume_history'):
                lines += ['- 训练曾恢复：计时排除停机与丢弃步骤。额外成本与恢复证据见训练报告，不把保留轨迹时间当作全部项目耗时。']
        lines.append('')
    lines += ['## 解释范围', '',
              '这是单个训练 seed、固定模型与 20 个 dev 数据库上的比较。单库 EX 可能因空结果或当前数据巧合判相等，不是 Test Suite Accuracy 或 Exact Match。官方难度是结构标签，不保证对具体模型单调。dev 参与优化方向选择后，后续结论为探索性；数据库聚类 bootstrap 也不能消除方法选择偏差或衡量训练 seed 方差。', '',
              '错误类别、配对改进/退化及数据库聚类区间由 scripts/analyze_errors.py 的对应报告补充；不要把训练 loss 或自动词法诊断当作准确率或确定因果。']
    target = ROOT / 'docs' / f'{args.output}.md'
    target.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(target)


if __name__ == '__main__':
    main()
