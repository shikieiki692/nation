# -*- coding: utf-8 -*-
"""各机构卡片 source_file 的「根目录」分布 —— 看哪些机构的卡来自 vault 根原件目录、哪些来自 chemy试题 等。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
BASE = '04-题库/2026机构初赛模拟题/'

print('=== vault 根 2026机构初赛模拟题/ 子目录 ===')
root = '2026机构初赛模拟题'
print(sorted(os.listdir(root)) if os.path.isdir(root) else '(缺)')
print()

agg = collections.defaultdict(collections.Counter)
for d in sorted(os.listdir(BASE)):
    dp = os.path.join(BASE, d)
    if not os.path.isdir(dp):
        continue
    for p in glob.glob(dp + '/题-*.md'):
        t = io.open(p, encoding='utf-8-sig', errors='replace').read()
        m = re.search(r'^source_file:[ \t]*"?(.+?)"?[ \t]*$', t, re.M)
        f = m.group(1) if m else '(无)'
        parts = f.split('/')
        head = '/'.join(parts[:2]) if len(parts) >= 2 else f
        agg[d][head] += 1

for d in sorted(agg):
    tot = sum(agg[d].values())
    print('◆ %-12s 共 %4d 卡' % (d, tot))
    for k, v in agg[d].most_common(4):
        print('     %4d  %s' % (v, k))
