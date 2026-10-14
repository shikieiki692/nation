# -*- coding: utf-8 -*-
r"""判定：备份文件里 mathrm 前的反斜杠个数分布。"""
import os, io, glob, re
os.chdir(r'C:\Obsidion\妙妙屋')
bak = sorted(glob.glob('.workbuddy/tmp/opt_pipe/_bak/dblback_*'))[-1]
print('备份:', bak)
tot1 = tot2 = 0
samples = []
for f in sorted(os.listdir(bak)):
    if not f.endswith('.md'):
        continue
    t = io.open(os.path.join(bak, f), encoding='utf-8-sig', errors='replace').read()
    for m in re.finditer(r'(\\+)mathrm', t):
        n = len(m.group(1))
        if n == 1:
            tot1 += 1
        elif n == 2:
            tot2 += 1
            if len(samples) < 6:
                s = max(0, m.start() - 45)
                samples.append((f[:34], t[s:m.end() + 30].replace('\n', '⏎')))
        elif n >= 3:
            print('  ⚠️ %d 个反斜杠 in %s' % (n, f[:40]))
print()
print('1 个反斜杠（正常）: %d' % tot1)
print('2 个反斜杠（bug） : %d' % tot2)
print()
print('=== 2 反斜杠样例 ===')
for f, s in samples:
    print('◆ %s' % f)
    print('   …%s…' % s)
