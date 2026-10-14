# -*- coding: utf-8 -*-
r"""扫「OCR 把化学符号/角标讹变成 Δ」类：① \Delta_{X} 非合法热力学下标 ② \mathrm{\Delta}^{ 残缺电荷。"""
import os, io, re
os.chdir(r'C:\Obsidion\妙妙屋')
LEGIT = {'r', 'f', 'c', 'vap', 'sub', 'sol', 'trs', 'mix', 'at', 'ion', 'lat', 'hyd',
         'd', 't', 'h', 's', 'g', 'l', 'a', 'u', 'p', 'v', 'fus', 'ads', 'des'}
P1 = re.compile(r'\\Delta\s*_\{?\s*([A-Za-z]{1,4})')
P2 = re.compile(r'\\mathrm\s*\{\s*\\Delta\s*\}\s*\^')

hits1 = {}; hits2 = {}
for root in ['04-题库', '04-课件', '03-知识点', '05-真题库']:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f)
            try:
                t = io.open(p, encoding='utf-8-sig').read()
            except Exception:
                continue
            for m in P1.finditer(t):
                sub = m.group(1)
                if sub.lower() in LEGIT:
                    continue
                hits1.setdefault(p, []).append((sub, t[max(0, m.start() - 45):m.end() + 22].replace('\n', '⏎')))
            for m in P2.finditer(t):
                hits2.setdefault(p, []).append(t[max(0, m.start() - 45):m.end() + 22].replace('\n', '⏎'))

print('=== ① `\\Delta_{<非热力学下标>}`：%d 文件 / %d 处 ===' % (len(hits1), sum(len(v) for v in hits1.values())))
for p, v in list(hits1.items())[:14]:
    for sub, seg in v[:2]:
        print('  [%s] %s' % (sub, p[:56]))
        print('       …%s…' % seg)
print()
print('=== ② `\\mathrm{\\Delta}^{`（残缺电荷）：%d 文件 / %d 处 ===' % (len(hits2), sum(len(v) for v in hits2.values())))
for p, v in list(hits2.items())[:10]:
    print('  %s' % p[:62])
    for seg in v[:2]:
        print('       …%s…' % seg)
