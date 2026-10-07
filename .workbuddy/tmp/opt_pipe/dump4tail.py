# -*- coding: utf-8 -*-
"""看 3+1 张题面尾带答案册标题的卡（题面区尾部 400 字）。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

KEYS = ['题-HYS-01-10-具有吗啡骨架', '题-HYS-02-10-101以下是两个', '题-HZ-38-08-的晶胞参数',
        '题-HZ-01-09-某无色有机底物S']
for k in KEYS:
    fs = [x for x in glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
          if os.path.basename(x).startswith(k)]
    if not fs:
        print('未找到', k); continue
    p = fs[0]
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案')
    qz = t[i:j]
    print('=' * 96)
    print(os.path.basename(p)[:58], '| 题面区 %d 字' % len(qz))
    print(' --- 尾部 320 ---')
    print(repr(qz[-320:]))
