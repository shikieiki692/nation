# -*- coding: utf-8 -*-
"""抽样「被判更早」的卡，打印全部与时间相关的 FM，判断年份判据是否失真。"""
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


def fm(t):
    d = {}
    for k in ('title', 'source', 'source_norm', 'source_file', 'source_category',
              'source_grade', 'source_tier', 'created', 'updated', 'exam_stage', 'subject_module'):
        m = re.search(r'^' + k + r':[ \t]*(.*?)[ \t]*$', t, re.M)
        d[k] = m.group(1).strip().strip('"') if m else ''
    return d


cards = []
for rel in O.SRCS:
    cards += sorted(glob.glob(os.path.join(BASE, rel, '**', '题-*.md'), recursive=True))

early = [p for p in cards if not O.in_2526(re.search(r'^source_norm:[ \t]*(.*)$', open(p, encoding='utf-8-sig').read(), re.M).group(1).strip().strip('"'),
                                            re.search(r'^source_file:[ \t]*(.*)$', open(p, encoding='utf-8-sig').read(), re.M).group(1).strip().strip('"'))]

print('被判「更早」共', len(early))
byinst = collections.defaultdict(list)
for p in early:
    byinst[os.path.relpath(p, BASE).split(os.sep)[0]].append(p)

for inst in ('chemy', '质心GChO', '汇智', 'XeChem', '化英社', '清北营', '方圆', '伽马'):
    print('\n===== %s（更早 %d 张）抽样 3 =====' % (inst, len(byinst.get(inst, []))))
    for p in byinst.get(inst, [])[:3]:
        t = open(p, encoding='utf-8-sig').read()
        d = fm(t)
        print('  file      :', os.path.basename(p))
        print('   source_norm:', d['source_norm'])
        print('   source     :', d['source'])
        print('   source_file:', d['source_file'])
        print('   created/updated:', d['created'], '/', d['updated'])

# 附：全库「更早」卡里 source_file 含 2026 的比例
n26 = sum(1 for p in early if '2026' in os.path.basename(
    re.search(r'^source_file:[ \t]*(.*)$', open(p, encoding='utf-8-sig').read(), re.M).group(1).strip().strip('"')))
print('\n「更早」卡的 source_file 文件名含 2026 的：%d / %d' % (n26, len(early)))
