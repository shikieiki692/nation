# -*- coding: utf-8 -*-
"""dump 3 张「过短」+ 2 张「仅题干回显」卡的 题面/答案区原文。"""
import os, re, sys, glob, csv
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'C:\Obsidion\妙妙屋'
rows = list(csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')))
want = ('题面/答案过短', '仅题干回显')
for r in rows:
    if r['reason'] not in want:
        continue
    p = os.path.join(ROOT, r['path'])
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
    print('=' * 100)
    print('%-12s | %s' % (r['reason'], os.path.basename(p)[:60]))
    print('  题面区 %d 字 / 答案区 %d 字' % (len(t[i:j]), len(t[j:k])))
    print('  ---- 题面区 ----')
    print(re.sub(r'\n{2,}', '\n', t[i:j]).strip()[:700])
    print('  ---- 答案区 ----')
    print(re.sub(r'\n{2,}', '\n', t[j:k]).strip()[:900])
    print()
