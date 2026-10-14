# -*- coding: utf-8 -*-
r"""拉出 8 处存疑的完整上下文块（只读）。"""
import io, os, re
os.chdir(r'C:\Obsidion\妙妙屋')
BASE = '04-题库/2026机构初赛模拟题/chemy/'
TARGETS = [
 ('题-CM-56-02-近日美国普林斯顿大学的研究人.md', 2400),
 ('题-CM-55-05-1961年Vaska报导了一.md', 900),
 ('题-CM-48-05-向含有少量酚酞指示剂的水溶液.md', 900),
 ('题-CM-73-09-簇合物在主族元素发展中起着比.md', 700),
]
for fn, win in TARGETS:
    p = BASE + fn
    t = io.open(p, encoding='utf-8-sig').read()
    print('=' * 100)
    print('◆ %s' % fn)
    for i, m in enumerate(re.finditer(r'Delta', t), 1):
        s = max(0, m.start() - win // 2)
        e = min(len(t), m.end() + win // 2)
        print('--- Δ#%d ---' % i)
        print(t[s:e])
