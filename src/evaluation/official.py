"""Load unchanged pure scoring functions from pinned, locally cached upstreams.

No upstream database executor is used: execution is always our read-only sandbox.
Single original SQLite DB, DISTINCT preserved, values predicted (never plugged).
"""
import ast
import hashlib
import json
import random
from collections import defaultdict
from itertools import product
from pathlib import Path
from typing import Tuple, List, Set

ROOT = Path(__file__).resolve().parents[2]
for _record in json.loads((ROOT/'configs/evaluator_lock.json').read_text()):
    if hashlib.sha256((ROOT/_record['path']).read_bytes()).hexdigest()!=_record['sha256']:
        raise RuntimeError('Official evaluator checksum mismatch')


def definitions(path, namespace, functions=None):
    tree = ast.parse(path.read_text(encoding='utf-8'))
    selected=[]
    for node in tree.body:
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
            if functions is None or node.name in functions:
                selected.append(node)
        elif isinstance(node,ast.Assign) and functions is None:
            # Spider module-level assignments are constant definitions.
            selected.append(node)
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(path),'exec'),namespace)
    return namespace


_hard = definitions(ROOT/'third_party/spider/evaluation.py',{})
_exec = definitions(ROOT/'third_party/test_suite/exec_eval.py',
                    dict(Tuple=Tuple,List=List,Set=Set,defaultdict=defaultdict,product=product,random=random),
                    {'permute_tuple','unorder_row','quick_rej','multiset_eq','get_constraint_permutation','result_eq'})


def hardness(sql_ast):
    return _hard['Evaluator']().eval_hardness(sql_ast)


def result_equal(gold_rows,pred_rows,gold_sql):
    random.seed(42)
    return _exec['result_eq'](gold_rows,pred_rows,order_matters='order by' in gold_sql.lower())
