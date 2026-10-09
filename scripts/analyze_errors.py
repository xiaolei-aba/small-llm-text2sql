"""Overlapping, explicitly heuristic diagnostics on real E0/E1/E3 predictions."""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def signature(sql,schema):
    literals=re.findall(r"'([^']*)'|\b(\d+(?:\.\d+)?)\b",sql)
    clean=re.sub(r"'[^']*'",' ',sql.lower())
    words=set(re.findall(r'\b\w+\b',clean))
    tables=set(t.lower() for t in schema['table_names_original'])
    columns=set(c.lower() for t,c in schema['column_names_original'] if t>=0)
    return {'tables':words&tables,'columns':words&columns,
        'aggregates':set(re.findall(r'\b(count|sum|avg|min|max)\s*\(',clean)),
        'group':bool(re.search(r'\bgroup\s+by\b',clean)),
        'where':bool(re.search(r'\bwhere\b',clean)),'literals':set(literals),
        'joins':len(re.findall(r'\bjoin\b',clean)),'selects':len(re.findall(r'\bselect\b',clean))}


def categories(row,evaluation,schema):
    if evaluation['execution_correct']:return []
    tags=[];error=(evaluation.get('execution_error') or '').lower()
    if row.get('truncated'):tags.append('Truncation')
    if 'interrupted' in error or 'timeout' in error:tags.append('Execution Timeout')
    if 'no such function' in error:tags.append('SQL Dialect / Function Error')
    if 'misuse of aggregate' in error:tags.append('Aggregation / GROUP BY Error')
    if any(x in error for x in ['syntax error','incomplete input','empty sql','did not produce']):tags.append('SQL Syntax Error')
    if any(x in error for x in ['no such table','no such column','ambiguous column']):tags+=['Invalid Schema Reference','Schema Linking Error']
    g,p=signature(row['gold_sql'],schema),signature(row['generated_sql'],schema)
    if g['tables']!=p['tables']:tags+=['Table Selection Error','Schema Linking Error']
    if g['columns']!=p['columns']:tags+=['Column Selection Error','Schema Linking Error']
    if g['joins']!=p['joins']:tags.append('JOIN Error')
    if g['aggregates']!=p['aggregates'] or g['group']!=p['group']:tags.append('Aggregation / GROUP BY Error')
    if (g['where'] or p['where']) and (g['where']!=p['where'] or g['literals']!=p['literals']):tags.append('WHERE Condition Error')
    if max(g['selects'],p['selects'])>1 and g['selects']!=p['selects']:tags.append('Nested Query Error')
    return sorted(set(tags)) or ['Other']


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--runs',nargs='+',default=['e0_dev','e1_dev'])
    ap.add_argument('--output',default='e2_error_analysis');args=ap.parse_args()
    schema={s['db_id']:s for s in json.loads((ROOT/'data/raw/spider/spider_data/tables.json').read_text())}
    reports={};all_rows={};all_scores={}
    md=['# 真实预测错误分析','',
        '分类为多标签启发式，分布之和可超过错误总数；只在 EX 错误样本上标记。词法表/列集合差异、JOIN/SELECT 数、聚合符、WHERE 字面量不构成确定因果；等价改写、别名、嵌套作用域可能误标。需人工读案例核验。','']
    for run in args.runs:
        path=ROOT/'results/predictions'/f'{run}.jsonl'
        rows=[json.loads(l) for l in path.read_text(encoding='utf-8').splitlines()]
        scores={s['sample_id']:s for s in [json.loads(l) for l in (ROOT/'results'/f'{run}_evaluation.jsonl').read_text().splitlines()]}
        assert len(rows)==1034 and len(scores)==1034
        assert all(s['predictions_sha256']==hashlib.sha256(path.read_bytes()).hexdigest() for s in scores.values())
        counts=Counter();cases=[]
        for row in rows:
            tags=categories(row,scores[row['sample_id']],schema[row['db_id']]);counts.update(tags)
            if tags:cases.append({k:row[k] for k in ['sample_id','db_id','difficulty','question','gold_sql','generated_sql']}|
                                 {'tags':tags,'execution_error':scores[row['sample_id']]['execution_error']})
        summary=json.loads((ROOT/'results'/f'{run}_summary.json').read_text())
        reports[run]={'summary':summary,'error_count':len(cases),'category_counts':dict(counts),'cases':cases}
        all_rows[run]={r['sample_id']:r for r in rows};all_scores[run]=scores
        md += [f'## {run}',f"EX={summary['execution_accuracy']:.4%}；可执行率={summary['valid_sql_rate']:.4%}；错误 {len(cases)}/1034。",'',
               '|难度|数量|EX|','|---|---:|---:|']
        for level in ['easy','medium','hard','extra_hard']:
            md.append(f"|{level}|{summary[level+'_samples']}|{summary[level+'_accuracy']:.2%}|")
        md+=['','|诊断标签|次数|','|---|---:|']+[f'|{k}|{v}|' for k,v in counts.most_common()]
        shown=set()
        for tag,count in counts.most_common():
            case=next((c for c in cases if tag in c['tags'] and c['sample_id'] not in shown),None)
            if not case:continue
            shown.add(case['sample_id']);md += ['',f"### {tag}：{case['sample_id']} / {case['db_id']}",
              case['question'],'','Gold（仅离线）：','```sql',case['gold_sql'],'```','预测：','```sql',case['generated_sql'],'```',
              f"诊断：{', '.join(case['tags'])}；SQLite：{case['execution_error']}"]
    comparisons={}
    if len(args.runs)>=2:
        import numpy as np
        baseline=args.runs[0]
        for run in args.runs[1:]:
            a=all_scores[baseline];b=all_scores[run]
            dbs=sorted(set(r['db_id'] for r in all_rows[run].values()))
            stats=[]
            for db in dbs:
                ids=[i for i,r in all_rows[run].items() if r['db_id']==db]
                stats.append([sum(int(b[i]['execution_correct'])-int(a[i]['execution_correct']) for i in ids),len(ids)])
            stats=np.array(stats);rng=np.random.default_rng(42)
            resampled=stats[rng.integers(0,len(dbs),size=(10000,len(dbs)))].sum(axis=1)
            ci=np.quantile(resampled[:,0]/resampled[:,1],[.025,.975]).tolist()
            c={'baseline':baseline,'candidate':run,'improved':sum(not a[i]['execution_correct'] and b[i]['execution_correct'] for i in a),
               'regressed':sum(a[i]['execution_correct'] and not b[i]['execution_correct'] for i in a),
               'delta_ex':reports[run]['summary']['execution_accuracy']-reports[baseline]['summary']['execution_accuracy'],
               'db_cluster_bootstrap_95_ci':ci,'bootstrap_replicates':10000,'seed':42,
               'limitation':'20 DB clusters; conditional on these trained models, not multi-training-seed uncertainty'}
            comparisons[run]=c;md += ['',f'## 配对变化 {baseline} → {run}',json.dumps(c,ensure_ascii=False,indent=2)]
    (ROOT/'results'/f'{args.output}.json').write_text(json.dumps({'runs':reports,'comparisons':comparisons},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'docs'/f'{args.output}.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps({run:{'errors':v['error_count'],'tags':v['category_counts']} for run,v in reports.items()},indent=2))


if __name__=='__main__':main()
