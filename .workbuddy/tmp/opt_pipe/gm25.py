# -*- coding: utf-8 -*-
"""看 伽马 gamma晶体结构习题.md 的 第4题 是否干净（有无内嵌解答） + 4 张 GM-25 卡的源。"""
import os, re, sys, csv
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Obsidion\妙妙屋'
p = os.path.join(ROOT, r'2026机构初赛模拟题\06-伽马\gamma晶体结构习题.md')
t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
i = t.find('## 第4题'); j = t.find('## 第5题')
print('第4题段 %d 字：' % (j - i))
print(re.sub(r'\n{2,}', '\n', t[i:j])[:1600])
print()
print('--- 4 张 GM-25 卡的 source 字段 ---')
rows = list(csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')))
for r in rows:
    bn = os.path.basename(r['path'])
    if r['reason'] == '题面泄露' and bn.startswith('题-GM-25'):
        cp = os.path.join(ROOT, r['path'])
        ct = open(cp, encoding='utf-8-sig', errors='replace').read()
        b = ct.split('---', 2)[1]
        m = re.search(r'^source:[ \t]*(.*)$', b, re.M)
        print('   %-44s | %s' % (bn[:42], m.group(1).strip() if m else ''))
