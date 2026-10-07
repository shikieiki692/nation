# -*- coding: utf-8 -*-
"""线1 v6：全库搜索 24 个源名（+「答案/解析」）是否存在于任何位置（含 06-外部资料导入 / 备份）。"""
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

# 先建全库文件名索引（md/pdf），跳过 .git
import collections
byname = collections.defaultdict(list)
SKIP = {'.git', '.workbuddy'}
for dp, dns, fns in os.walk(ROOT):
    if any(s in dp.replace('\\', '/').split('/') for s in SKIP):
        continue
    for f in fns:
        if f.endswith(('.md', '.pdf')):
            byname[f].append(dp.replace(ROOT, '').replace('\\', '/')[:70])

print('全库 md/pdf 文件 %d 个' % sum(len(v) for v in byname.values()))
print()
for sf, cards in sorted(srcs.items(), key=lambda x: -len(x[1])):
    stem = os.path.basename(sf)
    stem = stem[:-3] if stem.endswith('.md') else stem
    key = re.sub(r'\d{6,}$', '', stem)[:16]
    # 找文件名含 key 且含 答案/解析 的
    hits = []
    for f, ds in byname.items():
        if key and key in f and re.search(r'答案|解析', f):
            hits += ['%s/%s' % (d, f) for d in ds]
    print('%-44s (%2d张) → %s' % (key[:44], len(cards), (hits[:3] if hits else '❌ 全库无「%s…答案」' % key[:12])))
