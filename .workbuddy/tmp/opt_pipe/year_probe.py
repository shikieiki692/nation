# -*- coding: utf-8 -*-
"""按模块 × in_2526 交叉，并抽样「被判更早」的 source_norm，判断年份判据是否误伤。"""
import os
import re
import sys
import glob
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_org as O          # noqa: E402

BASE = O.BASE


def g(t, k):
    m = re.search(r'^' + k + r':\s*(.*)$', t, re.M)
    return m.group(1).strip() if m else ''


cards = []
for rel in O.SRCS:
    cards += sorted(glob.glob(os.path.join(BASE, rel, '**', '题-*.md'), recursive=True))

cross = collections.Counter()
early = collections.defaultdict(list)
for p in cards:
    t = open(p, encoding='utf-8-sig').read()
    mod = g(t, 'subject_module') or '(空)'
    norm = g(t, 'source_norm')
    ok = O.in_2526(norm, g(t, 'source_file'))
    cross[(mod, '2025~26' if ok else '更早')] += 1
    if not ok:
        early[mod].append(norm)

print('模块 × 年份判据')
for mod in ('元素与分析', '结构化学', '化学原理', '有机化学'):
    print('  %-8s 2025~26=%4d  更早=%4d' % (mod, cross[(mod, '2025~26')], cross[(mod, '更早')]))

print('\n★ 「更早」的 source_norm 抽样（元素与分析）')
c = collections.Counter(early['元素与分析'])
for k, v in c.most_common(25):
    print('  %3d  %s' % (v, k))

print('\n★ 「更早」的来源目录分布（全部）')
d = collections.Counter()
for p in cards:
    t = open(p, encoding='utf-8-sig').read()
    if not O.in_2526(g(t, 'source_norm'), g(t, 'source_file')):
        d[os.path.dirname(os.path.relpath(p, BASE)).split(os.sep)[0] + '/' + os.path.dirname(os.path.relpath(p, BASE)).split(os.sep)[-1]] += 1
for k, v in d.most_common(20):
    print('  %4d  %s' % (v, k))
