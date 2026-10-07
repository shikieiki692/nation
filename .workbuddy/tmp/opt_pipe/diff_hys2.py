# -*- coding: utf-8 -*-
"""对比化英社 决赛夏季试题2 两份文件在第3题区段的差异。"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

D = r'C:\Obsidion\妙妙屋\2026机构初赛模拟题\07-化英社'
F = [('试题2.md', '第40届化英社化学奥林匹克决赛夏季模拟试题2.md'),
     ('试题2参考答案.md', '第40届化英社化学奥林匹克决赛夏季模拟试题2参考答案.md')]

for lbl, fn in F:
    p = os.path.join(D, fn)
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 第3题')
    j = t.find('## 第 5 题', i)
    seg = t[i:j] if i >= 0 and j > i else t[i:i + 2000]
    print('=' * 100)
    print('%s  第3题段 %d 字' % (lbl, len(seg)))
    print(seg[:1500])
