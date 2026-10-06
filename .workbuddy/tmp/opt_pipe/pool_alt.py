# -*- coding: utf-8 -*-
"""对比「年份硬闸」开/关两种情形下的可用池规模。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_org as O          # noqa: E402

_orig = O.in_2526

print('=== 现状：in_2526 硬闸 ===')
p1 = O.build_pool()
for m in ('元素与分析', '结构化学', '化学原理'):
    print('  %-8s %d' % (m, len(p1[m])))

print('=== 放宽：取消 in_2526（保留其余全部闸） ===')
O.in_2526 = lambda norm, sf: True
p2 = O.build_pool()
for m in ('元素与分析', '结构化学', '化学原理'):
    print('  %-8s %d' % (m, len(p2[m])))
