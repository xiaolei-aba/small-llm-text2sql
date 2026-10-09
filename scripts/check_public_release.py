"""Check the candidate publication set without printing matched sensitive values."""
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = {
    'credential': r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|hf_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16}|xox[baprs]-[A-Za-z0-9-]{15,})',
    'private_key': r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
    'credential_assignment': r'''(?i)["']?(?:api[_-]?key|access[_-]?token|password|passwd|client[_-]?secret)["']?\s*[:=]\s*["'][^"'\r\n]{6,}["']''',
    'local_path': r'(?i)(?<![a-z0-9])[a-z]:[\\/]+|/(?:home|Users)/[^/\s]+',
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    'url_credentials': r'https?://[^\s/"<>]+:[^\s/"<>]+@',
    'signed_url': r'(?i)(?:[?&](?:token|access_token|sig|Signature)|X-Amz-Signature)=',
}
PUBLIC_IDENTITY = '335571521+xiaolei-aba@users.noreply.github.com'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8').strip()


def main():
    files = sorted(set(filter(None, git('ls-files', '-c', '-o', '--exclude-standard', '-z').split('\0'))))
    findings = []
    for name in files:
        path = ROOT/name
        if path.stat().st_size >= 10*1024**2:
            findings.append({'path': name, 'rule': 'large_file'})
        data = path.read_bytes()
        if b'\0' in data:
            findings.append({'path': name, 'rule': 'binary_requires_review'})
        text = data.decode('utf-8')
        for kind, pattern in RULES.items():
            for match in re.finditer(pattern, text):
                if kind == 'email' and match.group() == PUBLIC_IDENTITY:
                    continue  # exact noreply address verified by the repository owner
                findings.append({'path': name, 'rule': kind, 'line': text.count('\n', 0, match.start())+1})
    excluded = ['models/model.safetensors', 'adapters/test/adapter_model.safetensors',
                'checkpoints/test/latest.pt', 'data/raw/spider/spider_data/dev.json',
                'data/raw/example.sqlite', 'data/processed/sft_train.jsonl',
                'cache/downloads/test.zip', 'logs/train.log', 'envs/text2sql/python.exe',
                '.vscode/settings.json', '.env', 'tmp/example.part',
                'third_party/spider/evaluation.py', 'results/predictions/example.jsonl']
    assert set(git('check-ignore', '--', *excluded).splitlines()) == set(excluded)
    tracked = git('ls-files', '-z').split('\0')
    assert not any(p.startswith(('models/', 'adapters/', 'checkpoints/', 'cache/')) for p in tracked)
    assert not any(p.startswith('third_party/') and p != 'third_party/README.md' for p in tracked)
    with (ROOT/'results/metrics.csv').open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 10 and len({r['run_id'] for r in rows}) == 10
    for row in rows:
        summary = json.loads((ROOT/'results'/f"{row['run_id']}_summary.json").read_text())
        assert int(row['eval_samples']) == summary['eval_samples']
        for key in ['execution_accuracy', 'valid_sql_rate']:
            assert float(row[key]) == summary[key]
    assert git('config', '--local', 'user.email') == PUBLIC_IDENTITY
    assert git('config', '--local', 'user.name') == 'xiaolei-aba'
    assert not git('remote')
    license_text = (ROOT/'LICENSE').read_text(encoding='utf-8')
    upstream_license = (ROOT/'LICENSES/Spider-Apache-2.0.txt').read_text(encoding='utf-8')
    assert license_text.split('APPENDIX:')[0] == upstream_license.split('APPENDIX:')[0]
    assert 'Copyright 2026 xiaolei-aba' in (ROOT/'NOTICE').read_text(encoding='utf-8')
    notices = (ROOT/'THIRD_PARTY_NOTICES.md').read_text(encoding='utf-8')
    assert 'CC BY-SA 4.0' in notices and 'LICENSE_SCOPE.md' in notices
    readme = (ROOT/'README.md').read_text(encoding='utf-8')
    for run in ['e0_dev','e1_dev','e3_dev','e4_dev']:
        summary = json.loads((ROOT/'results'/f'{run}_summary.json').read_text())
        assert summary['eval_samples'] == 1034
        assert f"{summary['execution_accuracy']:.2%}" in readme
    for caveat in ['单库','不稳定','32','未运行vLLM']:
        assert caveat in readme, caveat
    print(json.dumps({'candidate_files': len(files), 'sensitive_findings': findings,
                      'ignore_checks': len(excluded), 'metric_rows': len(rows)}, indent=2))
    if findings:
        raise SystemExit(1)
    print('Publication checks passed; Apache-2.0 code scope and upstream exceptions verified; no remote publication authorized.')


if __name__ == '__main__':
    main()
