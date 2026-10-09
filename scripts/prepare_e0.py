"""Freeze evaluation manifests and tokenizer input inspection without inference."""
import collections
import json
import random
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.evaluation.official import hardness
from src.data.schema import load_schema_index,format_schema
from src.data.prompt import messages,PROMPT_VERSION
from transformers import AutoTokenizer

if Path(sys.prefix).name!='text2sql':
    raise RuntimeError('Use text2sql')
lock=json.loads((ROOT/'configs/model_lock.json').read_text())
data=ROOT/'data/raw/spider/spider_data'
dev=json.loads((data/'dev.json').read_text())
tok=AutoTokenizer.from_pretrained(ROOT/lock['local_dir'],local_files_only=True)
schema_index=load_schema_index(data/'tables.json')
schemas={db:format_schema(db,schema_index,data/'database'/db/(db+'.sqlite')) for db in sorted({r['db_id'] for r in dev})}
records=[]
for i,row in enumerate(dev):
    prompt=messages(row['question'],schemas[row['db_id']])
    ids=tok.apply_chat_template(prompt,add_generation_prompt=True,tokenize=True)
    records.append({'sample_id':f'dev:{i}','index':i,'db_id':row['db_id'],'difficulty':hardness(row['sql']),'prompt_tokens':len(ids)})
# Fixed random candidates, select each hardness and major structures; not accuracy selection.
candidates=list(range(len(dev))); random.Random(42).shuffle(candidates)
selected=[]
criteria=[('difficulty_'+d,lambda i,d=d: records[i]['difficulty']==d) for d in ['easy','medium','hard','extra']]
criteria += [('where',lambda i:bool(dev[i]['sql']['where'])),('order',lambda i:bool(dev[i]['sql']['orderBy'])),('group',lambda i:bool(dev[i]['sql']['groupBy'])),('multi_table',lambda i:len(dev[i]['sql']['from']['table_units'])>=3),('nested',lambda i:'select' in dev[i]['query'].lower()[6:]),('simple',lambda i:records[i]['difficulty']=='easy')]
for reason,condition in criteria:
    idx=next(i for i in candidates if i not in selected and condition(i))
    selected.append(idx)
smoke={'seed':42,'selection':'one per fixed structural/difficulty criterion from shuffled dev IDs; no prediction-based selection','sample_ids':[f'dev:{i}' for i in selected],'records':[records[i] for i in selected]}
(ROOT/'data/manifests/e0_smoke.json').write_text(json.dumps(smoke,indent=2)+'\n')
(ROOT/'data/manifests/e0_dev.json').write_text(json.dumps({'records':records,'difficulty_counts':dict(collections.Counter(r['difficulty'] for r in records))},indent=2)+'\n')
example=dev[selected[0]]
text=tok.apply_chat_template(messages(example['question'],schemas[example['db_id']]),tokenize=False,add_generation_prompt=True)
(ROOT/'docs/tokenizer_example.md').write_text('# Real input inspection\n\nQuestion: '+example['question']+'\n\ndb_id: '+example['db_id']+'\n\nPrompt tokens: '+str(records[selected[0]]['prompt_tokens'])+'\n\n```text\n'+text+'\n```\n',encoding='utf-8')
print('Difficulty counts',collections.Counter(r['difficulty'] for r in records))
print('Max dev prompt tokens',max(r['prompt_tokens'] for r in records))
print('Smoke IDs',smoke['sample_ids'])
