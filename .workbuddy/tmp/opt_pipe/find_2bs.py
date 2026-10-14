# -*- coding: utf-8 -*-
r"""找「恰好 2 个反斜杠 + mathrm」的位置（只读），按目录统计并给上下文。"""
import os, io, re
from collections import Counter
os.chdir(r'C:\Obsidion\妙妙屋')

PAT = re.compile(r'(?<!\\)\\\\(?!\\)mathrm')     # 恰好 2 个反斜杠
RUN = re.compile(r'(\\+)mathrm')
SKIPDIR = {'.git', 'node_modules', '_bak', 'blobs'}

c = Counter(); det = []
n_run2 = 0
for dp, dn, fn in os.walk('.'):
    dn[:] = [d for d in dn if d not in SKIPDIR]
    for f in fn:
        if not f.endswith('.md'):
            continue
        p = os.path.join(dp, f)
        try:
            t = io.open(p, encoding='utf-8-sig').read()
        except Exception:
            continue
        for m in RUN.finditer(t):
            if len(m.group(1)) == 2:
                n_run2 += 1
                top = '/'.join(p.replace('\\', '/').split('/')[:2])
                c[top] += 1
                if len(det) < 12:
                    s = max(0, m.start() - 70)
                    det.append((p, t[s:m.end() + 45].replace('\n', '⏎')))
print('恰好 2 反斜杠 + mathrm 的处数：%d' % n_run2)
print()
for k, v in c.most_common(15):
    print('  %-38s %d' % (k, v))
print()
print('=== 上下文 ===')
for p, seg in det:
    print('◆ %s' % p[:64])
    print('   …%s…' % seg)
