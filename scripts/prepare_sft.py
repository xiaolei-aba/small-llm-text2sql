"""Prepare all 7000 train_spider records; dev is read only to check db separation."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.data.schema import load_schema_index,format_schema
from src.train.data import encode_example
from src.evaluation.official import hardness


def main():
    if Path(sys.prefix).name!='text2sql':
        raise RuntimeError('Use text2sql')
    from transformers import AutoTokenizer
    lock=json.loads((ROOT/'configs/model_lock.json').read_text())
    tok=AutoTokenizer.from_pretrained(ROOT/lock['local_dir'],local_files_only=True)
    data=ROOT/'data/raw/spider/spider_data'
    train=json.loads((data/'train_spider.json').read_text())
    dev=json.loads((data/'dev.json').read_text())
    assert not ({r['db_id'] for r in train}&{r['db_id'] for r in dev})
    index=load_schema_index(data/'tables.json')
    schemas={db:format_schema(db,index,data/'database'/db/(db+'.sqlite')) for db in sorted({r['db_id'] for r in train})}
    rows=[]
    for i,ex in enumerate(train):
        encoded=encode_example(tok,ex['question'],schemas[ex['db_id']],ex['query'],max_length=32768)
        rows.append(dict(sample_id=f'train:{i}',index=i,db_id=ex['db_id'],difficulty=hardness(ex['sql']),**encoded))
    output=ROOT/'data/processed/sft_train.jsonl'
    with output.open('w',encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row)+'\n')
    manifest={'source':'train_spider.json','source_sha256':hashlib.sha256((data/'train_spider.json').read_bytes()).hexdigest(),
      'processed_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'samples':len(rows),'excluded_samples':0,
      'max_sequence_tokens':max(len(r['input_ids']) for r in rows),
      'total_sequence_tokens':sum(len(r['input_ids']) for r in rows),'total_target_tokens':sum(r['target_tokens'] for r in rows),
      'difficulty_counts':dict(Counter(r['difficulty'] for r in rows)),
      'model_revision':lock['revision'],'schema_version':'spider_schema_v2','prompt_version':'sqlite_zero_shot_v1',
      'records':[{k:r[k] for k in ['sample_id','index','db_id','difficulty','prompt_tokens','target_tokens']} for r in rows]}
    (ROOT/'data/manifests/sft_train.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k!='records'},indent=2))


if __name__=='__main__': main()
