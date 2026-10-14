# -*- coding: utf-8 -*-
"""地面真值：活跃任务/ 85 文件 —— 有无 FM / type 值"""
import io, os, re
os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'
noFm, hasFm = [], []
for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    t = io.open(os.path.join(D, f), encoding='utf-8-sig').read()
    m = re.match(r'^---\r?\n(.*?)\r?\n---(\r?\n|$)', t, re.S)
    if not m:
        noFm.append(f)
        continue
    s = m.group(1)
    mm = re.search(r'^type:[ \t]*(.*)$', s, re.M)
    hasFm.append((f, mm.group(1).strip() if mm else '(无type行)'))
print('=== 无 frontmatter 的文件（%d）===' % len(noFm))
for f in noFm:
    print('   ', f)
print()
print('=== 有 FM 的文件（%d）===' % len(hasFm))
from collections import Counter
print('   分布:', dict(Counter(v for _, v in hasFm)))
print()
print('   其中 type 非「活跃任务卡」的:')
for f, v in hasFm:
    if v != '活跃任务卡':
        print('      %-52s %s' % (f[:52], v))
