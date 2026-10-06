# -*- coding: utf-8 -*-
"""精确还原 3 张被误填的方圆卡（答案区取 49d4821ce^ 版）。"""
import subprocess, sys, os

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
OLD = '49d4821ce^'
B = '04-题库/2026机构初赛模拟题/方圆/'
F = ['题-FY-01-05-51X是某天然矿物的主要成分.md',
     '题-FY-01-06-611在一个萃取过程中体系的.md',
     '题-FY-01-08-81Carreira课题组在.md']


def rng(t):
    i = t.find('## 参考答案'); k = t.find('## 知识点映射')
    return (i, k) if i > 0 and k > i else (None, None)


for n in F:
    p = B + n
    old = subprocess.run(['git', 'show', OLD + ':' + p], capture_output=True, text=True,
                         encoding='utf-8', errors='replace').stdout
    oi, ok = rng(old)
    assert oi is not None, n
    raw = open(p, 'rb').read()
    bom = raw[:3] == b'\xef\xbb\xbf'
    t = raw.decode('utf-8-sig').replace('\r\n', '\n')
    ci, ck = rng(t)
    new = t[:ci] + old[oi:ok].rstrip('\n') + '\n' + t[ck:]
    if APPLY:
        open(p, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + new.encode('utf-8'))
    print('✓ %s  (%d → %d 字)' % (n[:34], len(t), len(new)))
print('[%s]' % ('APPLY' if APPLY else 'DRY-RUN'))
