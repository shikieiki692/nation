# -*- coding: utf-8 -*-
"""对每张卷：列「题号/标题」与「来源行」，并标出「非有机卷里出现有机套」等矛盾。"""
import io, os, re, glob

os.chdir(r'C:\Obsidion\妙妙屋')
VOL = sorted(glob.glob('04-题库/初赛模拟卷*（非有机·答案版）.md'))
H = re.compile(r'^###\s*第\s*(\d+)\s*题')
S = re.compile(r'^>\s*来源[:：]\s*(.+)$')

for p in VOL:
    name = os.path.basename(p).replace('初赛模拟卷', '').replace('（非有机·答案版）.md', '')
    t = io.open(p, encoding='utf-8-sig').read()
    L = t.split('\n')
    print('===== 卷 %s =====' % name)
    cur = None
    for i, l in enumerate(L):
        m = H.match(l)
        if m:
            cur = (m.group(1), l.strip()[4:80])
        ms = S.match(l)
        if ms and cur:
            src = ms.group(1).strip()
            flag = ''
            if '有机' in src and '有机' not in cur[1]:
                flag = '   ⚠️ 非有机题←有机套'
            if '无机' in src and '无机' not in cur[1] and '结构' not in cur[1]:
                flag = '   ⚠️'
            print('  第%-2s题 %-28s | %s%s' % (cur[0], cur[1][:28], src[:62], flag))
            cur = None
    print()
