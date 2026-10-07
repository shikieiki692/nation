# -*- coding: utf-8 -*-
"""量化：题面区**末尾**出现「答案册标题行」（后随 <40 字）的卡（入池/弃卡分列）。"""
import os, re, sys, glob, csv
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'C:\Obsidion\妙妙屋'
verd = {}
for r in csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')):
    verd[os.path.basename(r['path'])] = r['verdict']

ANS_HEAD = re.compile(r'(?m)^#{1,4}[ \t]*([^\n]{0,60}?答案[^\n]{0,30})\s*$')
pool_hit, other_hit = [], []
for p in glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True):
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案')
    if i < 0 or j < 0:
        continue
    qz = t[i:j]
    for m in ANS_HEAD.finditer(qz):
        body = m.group(1).strip()
        if body in ('参考答案', '答案'):
            continue
        tail = len(qz) - m.end()
        if tail < 40:
            bn = os.path.basename(p)
            (pool_hit if verd.get(bn) == '入池' else other_hit).append((bn, tail, body[:30]))
            break
print('题面**末尾**带答案册标题：入池 %d 张 / 其他 %d 张' % (len(pool_hit), len(other_hit)))
print('  —— 入池的：')
for bn, tail, body in pool_hit[:20]:
    print('     %-46s tail=%d | %s' % (bn[:44], tail, body))
