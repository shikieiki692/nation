# -*- coding: utf-8 -*-
"""线1 v4：打印每个源的同级目录里**全部**答案/解析文件，人工可比对。"""
import csv, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'C:\Obsidion\妙妙屋'
rows = [r for r in csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig'))
        if r['reason'] == '无答案/占位']


def field(t, k):
    m = re.search(r'^' + k + r':[ \t]*(.*)$', t, re.M)
    return (m.group(1).strip().strip('"') if m else '')


srcs = {}
for r in rows:
    p = os.path.join(ROOT, r['path'])
    t = open(p, encoding='utf-8-sig', errors='replace').read()
    srcs.setdefault(field(t, 'source_file'), []).append(1)

for sf, cards in sorted(srcs.items(), key=lambda x: -len(x[1]))[:8]:
    d = os.path.join(ROOT, os.path.dirname(sf))
    print('=' * 110)
    print('源: %s  (%d 张)' % (os.path.basename(sf), len(cards)))
    if not os.path.isdir(d):
        print('  （目录不存在）'); continue
    fs = [f for f in sorted(os.listdir(d)) if f.endswith('.md') and ('答案' in f or '解析' in f)]
    print('  同级答案/解析文件 %d 个：' % len(fs))
    for f in fs:
        print('    %s' % f[:100])
