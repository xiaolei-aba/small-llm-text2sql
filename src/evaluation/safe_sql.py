"""Read-only SQLite with authorizer, deadline, and bounded result collection."""
import sqlite3
import time
from pathlib import Path


def execute(sql, db_path, timeout=5.0, max_rows=100000, max_bytes=32_000_000):
    start = time.perf_counter()
    conn = None
    try:
        if not sql.strip():
            raise ValueError('Empty SQL')
        path = Path(db_path).resolve(strict=True)
        conn = sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
        conn.text_factory = lambda value: value.decode(errors='ignore')
        conn.execute('PRAGMA query_only=ON')
        conn.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 1_000_000)
        conn.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 100_000)
        allowed = {sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_FUNCTION,sqlite3.SQLITE_RECURSIVE}
        def authorize(action, arg1, arg2, database, trigger):
            if action not in allowed:
                return sqlite3.SQLITE_DENY
            if action == sqlite3.SQLITE_FUNCTION and (arg2 or '').lower() in ('load_extension','readfile','writefile'):
                return sqlite3.SQLITE_DENY
            if action == sqlite3.SQLITE_READ and database not in ('main',None):
                return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK
        conn.set_authorizer(authorize)
        conn.set_progress_handler(lambda: int(time.perf_counter()-start > timeout),1000)
        cursor = conn.execute(sql)
        if cursor.description is None:
            raise ValueError('SQL did not produce a query result')
        rows=[]
        size=0
        for row in cursor:
            size += len(repr(row).encode('utf-8'))
            if len(rows)>=max_rows or size>max_bytes:
                raise RuntimeError('Result resource limit exceeded')
            if time.perf_counter()-start>timeout:
                raise TimeoutError('SQL execution timeout')
            rows.append(row)
        return {'ok':True,'rows':rows,'error':None,'seconds':time.perf_counter()-start}
    except Exception as exc:
        return {'ok':False,'rows':None,'error':f'{type(exc).__name__}: {exc}','seconds':time.perf_counter()-start}
    finally:
        if conn is not None:
            conn.close()
