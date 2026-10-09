"""Read-only inventory of an official Spider extraction; no model inference."""

import argparse
import hashlib
import json
import random
import sys
import sqlite3
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data.schema import SCHEMA_VERSION, format_schema, load_schema_index, read_sqlite_schema, quote_identifier


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    if Path(sys.prefix).name != "text2sql":
        raise RuntimeError("Use the text2sql environment")
    root = args.root.resolve(strict=True)
    schema_index = load_schema_index(root / "tables.json")
    report = {"audited_at_utc": datetime.now(timezone.utc).isoformat(),
              "dataset": "Spider 1.0", "root": str(root), "schema_version": SCHEMA_VERSION,
              "schema_count": len(schema_index), "splits": {}, "files": [], "errors": []}
    split_rows = {}
    for split, filename in [("train", "train_spider.json"), ("dev", "dev.json")]:
        rows = json.loads((root / filename).read_text(encoding="utf-8"))
        for i, row in enumerate(rows):
            for key in ("question", "query", "db_id"):
                if not isinstance(row.get(key), str) or not row[key].strip():
                    raise ValueError(f"{split}/{i}: missing {key}")
        split_rows[split] = rows
        report["splits"][split] = {"file": filename, "samples": len(rows),
                                     "db_ids": sorted({r["db_id"] for r in rows})}
    report["other_top_level_json"] = {}
    for path in sorted(root.glob("*.json")):
        if path.name not in ("tables.json", "train_spider.json", "dev.json"):
            contents = json.loads(path.read_text(encoding="utf-8"))
            report["other_top_level_json"][path.name] = {
                "record_count": len(contents), "used_in_e0": False}
    train_dbs = set(report["splits"]["train"]["db_ids"])
    dev_dbs = set(report["splits"]["dev"]["db_ids"])
    report["train_dev_db_overlap"] = sorted(train_dbs & dev_dbs)
    db_files = sorted((root / "database").rglob("*.sqlite"))
    report["sqlite_file_count"] = len(db_files)
    report["database_directory_count"] = len([p for p in (root / "database").iterdir() if p.is_dir()])
    for path in sorted(root.rglob("*")):
        if path.is_file():
            report["files"].append({"path": path.relative_to(root).as_posix(),
                                     "bytes": path.stat().st_size, "sha256": sha256(path)})
    report['database_checks'] = []
    report['annotation_differences'] = []
    formatted = {}
    for db_id in sorted(set(schema_index) | train_dbs | dev_dbs):
        try:
            db_path = root / "database" / db_id / f"{db_id}.sqlite"
            conn = sqlite3.connect(db_path.resolve(strict=True).as_uri()+'?mode=ro', uri=True)
            try:
                conn.execute('PRAGMA query_only=ON')
                integrity = [r[0] for r in conn.execute('PRAGMA integrity_check')]
                report['database_checks'].append({'db_id':db_id,'integrity_check':integrity})
                if integrity != ['ok']:
                    raise ValueError(f'Integrity check failed: {integrity}')
                db = schema_index[db_id]
                actual = read_sqlite_schema(db_path)
                tables = db['table_names_original']
                columns = db['column_names_original']
                for ti, table in enumerate(tables):
                    real = next(n for n in actual if n.casefold()==table.casefold())
                    annotated_pk = [columns[i][1].casefold() for i in db['primary_keys'] if columns[i][0]==ti]
                    sqlite_pk = [c['name'].casefold() for c in sorted(actual[real],key=lambda c:c['pk']) if c['pk']]
                    annotated_fk = sorted((columns[a][1].casefold(),tables[columns[b][0]].casefold(),columns[b][1].casefold()) for a,b in db['foreign_keys'] if columns[a][0]==ti)
                    sqlite_fk = sorted((r[3].casefold(),r[2].casefold(),(r[4] or '').casefold()) for r in conn.execute(f'PRAGMA foreign_key_list({quote_identifier(real)})'))
                    annotated_cols = {c.casefold() for owner,c in columns if owner==ti}
                    actual_cols = {c['name'].casefold() for c in actual[real]}
                    if annotated_cols != actual_cols:
                        raise ValueError(f'{table}: column set differs: {annotated_cols ^ actual_cols}')
                    if annotated_pk != sqlite_pk or annotated_fk != sqlite_fk:
                        report['annotation_differences'].append({'db_id':db_id,'table':table,'spider_pk':annotated_pk,'sqlite_pk':sqlite_pk,'spider_fk':annotated_fk,'sqlite_fk':sqlite_fk})
            finally:
                conn.close()
            formatted[db_id] = format_schema(db_id, schema_index, db_path)
            if formatted[db_id] != format_schema(db_id, schema_index, db_path):
                raise ValueError("Non-deterministic schema text")
        except Exception as exc:
            report["errors"].append({"db_id": db_id, "error": str(exc)})
    report["checked_database_count"] = len(formatted)
    # Deterministic random sample of database IDs, independent of gold SQL.
    chosen = random.Random(42).sample(sorted(train_dbs | dev_dbs), 3)
    report["schema_preview_db_ids"] = chosen
    preview = [f"# Schema previews\n\nSeed=42; formatter={SCHEMA_VERSION}.\n"]
    for db_id in chosen:
        preview.append(f"## {db_id}\n\n```text\n{formatted.get(db_id, 'SCHEMA VALIDATION FAILED: see errors in audit JSON')}\n```\n")
    example = split_rows["dev"][0]
    report["example"] = {"sample_id": "dev:0", "db_id": example["db_id"],
                         "question": example["question"], "gold_sql": example["query"],
                         "schema": formatted.get(example["db_id"])}
    report['files_unchanged_after_checks'] = all(sha256(root / item['path']) == item['sha256'] for item in report['files'])
    if not report['files_unchanged_after_checks']:
        report['errors'].append({'error':'Raw file hash changed during audit'})
    download = json.loads((ROOT/'data/manifests/spider_download.json').read_text(encoding='utf-8'))
    archive = ROOT/'cache/downloads/spider_data.zip'
    report['archive_sha256'] = sha256(archive)
    report['archive_matches_download_manifest'] = report['archive_sha256']==download['archive_sha256']
    report['archive_file_mismatches'] = []
    skipped = {r['path'] for r in download['skipped_members']}
    matched = 0
    with zipfile.ZipFile(archive) as bundle:
        for info in bundle.infolist():
            if info.is_dir() or info.filename in skipped:
                continue
            path = root.parent / info.filename
            with bundle.open(info) as stream:
                expected = hashlib.file_digest(stream,'sha256').hexdigest()
            if not path.is_file() or sha256(path)!=expected:
                report['archive_file_mismatches'].append(info.filename)
            else:
                matched += 1
    report['archive_files_matched'] = matched
    if not report['archive_matches_download_manifest'] or report['archive_file_mismatches']:
        report['errors'].append({'error':'Archive/extracted content verification failed'})
    report['scope'] = 'All 166 tables.json databases: integrity/schema; test databases: archive byte verification only; no gold SQL execution'
    report['exit_code'] = int(bool(report['errors'] or report['train_dev_db_overlap']))
    out = ROOT / "data" / "manifests" / "spider_audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "docs" / "schema_previews.md").write_text("\n".join(preview), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ('files','database_checks','annotation_differences')}, ensure_ascii=False, indent=2))
    if report["errors"] or report["train_dev_db_overlap"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
