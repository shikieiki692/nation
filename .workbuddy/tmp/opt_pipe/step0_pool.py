# -*- coding: utf-8 -*-
"""Step 0 复现：组卷真实池规模（只读，不落盘）"""
import os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ['ALL_YEARS'] = '1'
sys.argv = [sys.argv[0], '--vol', 'X', '--all-years']
import build_org

pool = build_org.build_pool()
print('type(pool) =', type(pool))
total = 0
if isinstance(pool, dict):
    for k, v in pool.items():
        n = len(v) if hasattr(v, '__len__') else 0
        print('   ', k, n)
        total += n
else:
    total = len(pool)
print('POOL_TOTAL =', total)
