# -*- coding: utf-8 -*-
"""「更早」桶的成分拆解：① 带旧届次(第32~38届) ② 完全无届次/年份字样(疑误判) ③ 其他。"""
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
JIE = re.compile(r'第\s*(\d+)\s*届')

cards = []
for rel in O.SRCS:
    cards += sorted(glob.glob(os.path.join(BASE, rel, '**', '题-*.md'), recursive=True))

buckets = collections.Counter()
by_inst = collections.defaultdict(collections.Counter)
for p in cards:
    t = open(p, encoding='utf-8-sig').read()
    m = re.search(r'^source_norm:[ \t]*(.*?)[ \t]*$', t, re.M)
    norm = m.group(1).strip().strip('"') if m else ''
    msf = re.search(r'^source_file:[ \t]*(.*?)[ \t]*$', t, re.M)
    sf = msf.group(1).strip().strip('"') if msf else ''
    inst = os.path.relpath(p, BASE).split(os.sep)[0]
    if O.in_2526(norm, sf):
        buckets['2025~26（判通过）'] += 1
        by_inst[inst]['2025~26'] += 1
    else:
        jie = [int(x) for x in JIE.findall(norm)]
        if jie:
            buckets['更早·带届次'] += 1
            by_inst[inst]['带旧届次'] += 1
        elif ('2025' in norm or '2026' in norm
              or '2025' in os.path.basename(sf) or '2026' in os.path.basename(sf)):
            buckets['更早·其他'] += 1
            by_inst[inst]['其他'] += 1
        else:
            buckets['更早·无任何年份字样'] += 1
            by_inst[inst]['无年份字样'] += 1

print('全库 4032 卡年份判据成分：')
for k, v in buckets.most_common():
    print('   %-18s %5d' % (k, v))

print('\n按机构 × 判据：')
for inst in sorted(by_inst):
    c = by_inst[inst]
    print('   %-10s 过2025~26=%4d  带旧届次=%4d  无年份字样=%4d  其他=%d'
          % (inst, c['2025~26'], c['带旧届次'], c['无年份字样'], c['其他']))
