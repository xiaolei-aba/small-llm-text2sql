"""Preflight all dev references through the same restricted SQL executor."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.evaluation.safe_sql import execute
if Path(sys.prefix).name!='text2sql':
    raise RuntimeError('Use text2sql')
data=ROOT/'data/raw/spider/spider_data'
rows=json.loads((data/'dev.json').read_text())
failures=[]
for i,row in enumerate(rows):
    result=execute(row['query'],data/'database'/row['db_id']/(row['db_id']+'.sqlite'))
    if not result['ok']:
        failures.append({'sample_id':f'dev:{i}','db_id':row['db_id'],'error':result['error']})
report={'samples':len(rows),'failures':failures,'scope':'gold execution only; no model or accuracy'}
(ROOT/'docs/gold_execution_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(bool(failures))
