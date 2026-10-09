"""Restore exact official scorer source files and licenses from tracked hashes."""
import hashlib
import json
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for record in json.loads((ROOT/'configs/evaluator_lock.json').read_text()):
    target=ROOT/record['path']
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==record['sha256']:
        continue
    if target.exists():
        raise RuntimeError(f'Refuse overwrite modified scorer: {target}')
    with urllib.request.urlopen(record['url'],timeout=30) as response:
        data=response.read()
    if hashlib.sha256(data).hexdigest()!=record['sha256']:
        raise RuntimeError('Upstream content checksum mismatch')
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
print('Pinned scorer files verified')
