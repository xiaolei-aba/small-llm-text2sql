"""Deterministic schema text from Spider metadata and read-only SQLite metadata.

No question, gold SQL, or row values are accepted by this interface.
Spider PK/FK annotations are authoritative; declared SQLite types are displayed.
"""

import json
import sqlite3
from pathlib import Path

SCHEMA_VERSION = "spider_schema_v2"


def load_schema_index(tables_path):
    rows = json.loads(Path(tables_path).read_text(encoding="utf-8"))
    index = {row["db_id"]: row for row in rows}
    if len(index) != len(rows):
        raise ValueError("Duplicate db_id in tables.json")
    return index


def quote_identifier(value):
    return '"' + value.replace('"', '""') + '"'


def read_sqlite_schema(db_path):
    path = Path(db_path).resolve(strict=True)
    conn = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    try:
        conn.execute("PRAGMA query_only=ON")
        names = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "ORDER BY name"
        )]
        return {name: [dict(cid=r[0], name=r[1], type=r[2], pk=r[5])
                       for r in conn.execute(f"PRAGMA table_info({quote_identifier(name)})")]
                for name in names}
    finally:
        conn.close()


def format_schema(db_id, schema_index, db_path):
    db = schema_index[db_id]
    actual = read_sqlite_schema(db_path)
    lookup = {name.casefold(): cols for name, cols in actual.items()}
    tables = db["table_names_original"]
    columns = db["column_names_original"]
    pks = set(db["primary_keys"])
    lines = ["Database schema:"]
    for table_id, table in enumerate(tables):
        if table.casefold() not in lookup:
            raise ValueError(f"{db_id}: table {table!r} absent in SQLite")
        col_lookup = {col["name"].casefold(): col for col in lookup[table.casefold()]}
        lines.extend(["", f"Table {table}:"])
        pk_names = []
        for column_id, (owner, name) in enumerate(columns):
            if owner != table_id:
                continue
            if name.casefold() not in col_lookup:
                raise ValueError(f"{db_id}: column {table}.{name} absent in SQLite")
            declared_type = col_lookup[name.casefold()]["type"] or "UNDECLARED"
            lines.append(f"- {name} {declared_type}")
            if column_id in pks:
                pk_names.append(name)
        if pk_names:
            lines.append("Primary key: (" + ", ".join(pk_names) + ")")
    lines.extend(["", "Foreign keys:"])
    for source, target in db["foreign_keys"]:
        source_table, source_col = columns[source]
        target_table, target_col = columns[target]
        if source_table < 0 or target_table < 0:
            raise ValueError("Invalid wildcard in foreign key")
        lines.append(f"{tables[source_table]}.{source_col} -> {tables[target_table]}.{target_col}")
    if not db["foreign_keys"]:
        lines.append("(none annotated)")
    return "\n".join(lines)
