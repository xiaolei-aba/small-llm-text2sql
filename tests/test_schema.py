"""Small metadata-only tests; these are not Text-to-SQL model experiments."""

import hashlib
import sqlite3
import tempfile
import unittest
from pathlib import Path

from src.data.schema import format_schema


class SchemaTests(unittest.TestCase):
    def test_annotated_sqlite_sequence_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'sequence.sqlite'
            conn = sqlite3.connect(path)
            conn.execute('CREATE TABLE example (id INTEGER PRIMARY KEY AUTOINCREMENT)')
            conn.close()
            metadata = {'x': {'table_names_original':['example','sqlite_sequence'],
                        'column_names_original':[[-1,'*'],[0,'id'],[1,'name'],[1,'seq']],
                        'primary_keys':[1], 'foreign_keys':[]}}
            text = format_schema('x',metadata,path)
            self.assertIn('Table sqlite_sequence:',text)
            self.assertIn('- seq UNDECLARED',text)

    def test_composite_key_determinism_and_no_row_values(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "test.sqlite"
            conn = sqlite3.connect(path)
            conn.executescript('CREATE TABLE "parent table" (a INTEGER, b TEXT, PRIMARY KEY(a,b));'
                               'CREATE TABLE child (pid INTEGER REFERENCES "parent table"(a));'
                               'INSERT INTO "parent table" VALUES (1, "SECRET_ROW_VALUE");')
            conn.close()
            metadata = {"test": {"table_names_original": ["parent table", "child"],
                                 "column_names_original": [[-1, "*"], [0, "a"], [0, "b"], [1, "pid"]],
                                 "primary_keys": [1, 2], "foreign_keys": [[3, 1]]}}
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            text = format_schema("test", metadata, path)
            self.assertEqual(text, format_schema("test", metadata, path))
            self.assertIn("Primary key: (a, b)", text)
            self.assertIn("child.pid -> parent table.a", text)
            self.assertNotIn("SECRET_ROW_VALUE", text)
            self.assertEqual(before, hashlib.sha256(path.read_bytes()).hexdigest())

    def test_missing_file_is_not_created(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "missing.sqlite"
            with self.assertRaises(FileNotFoundError):
                format_schema("test", {"test": {}}, path)
            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
