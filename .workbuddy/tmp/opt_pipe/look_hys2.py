# -*- coding: utf-8 -*-
"""看化英社「决赛夏季模拟试题2」的试题源与答案源（第 3 题附近）。"""
import re, sys, os
sys.stdout.reconfigure(encoding='utf-8')

D = r'C:\Obsidion\妙妙屋\2026机构初赛模拟题\07-化英社'
Q = os.path.join(D, '第40届化英社化学奥林匹克决赛夏季模拟试题2.md')
A = os.path.join(D, '第40届化英社化学奥林匹克决赛夏季模拟试题2参考答案.md')

for lbl, p in (('试题', Q), ('答案', A)):
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    print('=' * 100)
    print('%s  %d 字' % (lbl, len(t)))
    print('  --- 标题行 ---')
    for m in re.finditer(r'(?m)^#{1,6} .*$', t):
        print('    @%6d %s' % (m.start(), m.group(0)[:70]))
