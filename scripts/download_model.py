"""Resume official Hugging Face snapshot download at the locked revision."""
import os
os.environ.setdefault('HF_HUB_DISABLE_XET', '1')
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from huggingface_hub import snapshot_download

ROOT = Path(__file__).resolve().parents[1]
if Path(sys.prefix).name != 'text2sql':
    raise RuntimeError('Use text2sql')
lock = json.loads((ROOT/'configs/model_lock.json').read_text())
snapshot_download(repo_id=lock['repo_id'], revision=lock['revision'],
                  local_dir=str(ROOT/lock['local_dir']), max_workers=2,
                  allow_patterns=['*.json','*.txt','*.safetensors','LICENSE','README.md'])
(ROOT/'docs/model_download.json').write_text(json.dumps({**lock,
    'completed_at_utc':datetime.now(timezone.utc).isoformat()},indent=2)+'\n',encoding='utf-8')
print('Snapshot download completed', flush=True)
