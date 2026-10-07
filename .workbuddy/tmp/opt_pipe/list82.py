# -*- coding: utf-8 -*-
"""列 A 类 82 张「无答案/占位」的机构与 source_norm 分布。"""
import csv, os, re, sys, collections
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'C:\Obsidion\妙妙屋'
rows = [r for r in csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig'))
        if r['reason'] == '无答案/占位']
print('无答案 %d 张，按机构：' % len(rows))
for k, v in collections.Counter(r['inst'] for r in rows).most_common():
    print('  %-10s %d' % (k, v))


def field(t, k):
    m = re.search(r'^' + k + r':[ \t]*(.*)$', t, re.M)
    return (m.group(1).strip().strip('"') if m else '')


c = collections.Counter()
sf = {}
for r in rows:
    p = os.path.join(ROOT, r['path'])
    t = open(p, encoding='utf-8-sig', errors='replace').read()
    n = field(t, 'source_norm') or '?'
    c[n] += 1
    sf.setdefault(n, field(t, 'source_file'))
print()
print('按 source_norm（%d 个源）：' % len(c))
for k, v in c.most_common():
    print('  %-30s %2d  | file=%s' % (k[:30], v, sf[k][:56]))
