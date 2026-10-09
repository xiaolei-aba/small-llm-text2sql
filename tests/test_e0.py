import hashlib
import sqlite3
import tempfile
import unittest
from pathlib import Path
from src.data.prompt import messages
from src.inference.postprocess import extract_sql
from src.evaluation.safe_sql import execute
from src.evaluation.official import result_equal


class E0Tests(unittest.TestCase):
    def test_prompt_and_cleanup(self):
        m=messages('QUESTION','SCHEMA')
        self.assertEqual(len(m),2)
        self.assertEqual([x['role'] for x in m],['system','user'])
        self.assertIn('QUESTION',m[1]['content'])
        self.assertEqual(extract_sql('```sql\nSELECT 1;\n```'),'SELECT 1;')
        self.assertEqual(extract_sql("SELECT 'A  B';"),"SELECT 'A  B';")

    def test_readonly_and_limits(self):
        with tempfile.TemporaryDirectory() as folder:
            db=Path(folder)/'test.sqlite'
            c=sqlite3.connect(db)
            c.executescript('CREATE TABLE t(x INTEGER); INSERT INTO t VALUES(1),(2);')
            c.close()
            before=hashlib.sha256(db.read_bytes()).hexdigest()
            self.assertEqual(execute('SELECT sum(x) FROM t',db)['rows'],[(3,)])
            for sql in ['DELETE FROM t','DROP TABLE t',"ATTACH DATABASE ':memory:' AS other",'PRAGMA writable_schema=ON',"SELECT load_extension('x')",'SELECT 1; SELECT 2']:
                self.assertFalse(execute(sql,db)['ok'],sql)
            self.assertFalse(execute('SELECT x FROM t',db,max_rows=1)['ok'])
            self.assertFalse(execute('-- no query',db)['ok'])
            self.assertFalse(execute('WITH RECURSIVE t(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM t) SELECT sum(x) FROM t',db,timeout=.01)['ok'])
            self.assertEqual(before,hashlib.sha256(db.read_bytes()).hexdigest())

    def test_official_result_semantics(self):
        self.assertTrue(result_equal([(1,),(2,)],[(2,),(1,)],'select x from t'))
        self.assertFalse(result_equal([(1,),(2,)],[(2,),(1,)],'select x from t order by x'))
        self.assertFalse(result_equal([(1,),(1,)],[(1,),(2,)],'select x from t'))
        self.assertFalse(result_equal([('A',)],[('a',)],'select x from t'))
        self.assertTrue(result_equal([(1,'a')],[('a',1)],'select x,y from t'))


if __name__=='__main__':
    unittest.main()
