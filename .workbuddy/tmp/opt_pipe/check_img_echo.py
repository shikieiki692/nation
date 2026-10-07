# -*- coding: utf-8 -*-
"""查 HYS-02-07 题面/答案的图引用，判断是否为同图回显。"""
import os, re, sys, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'IM', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
rows = list(csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')))
p = [r for r in rows if os.path.basename(r['path']).startswith('题-HYS-02-07-万物')][0]
p = os.path.join(ROOT, p['path'])
c = BO.X.extract(p)
q0 = BO.conv_imgs(BO.clean_q(c['question']))
a = BO.flatten_layout_tables(BO.conv_imgs(c['answer']))
print('题面图:', re.findall(r'!\[\[([^\]]+)\]\]', q0))
print('答案图:', re.findall(r'!\[\[([^\]]+)\]\]', a))
print()
print('--- 题面中纯图段（长度 ≥12）---')
def nz(s):
    return re.sub(r'[#\s{}]', '', s)
for seg in re.split(r'\n{2,}', q0):
    n = nz(seg)
    if len(n) >= 12 and '![[' in n:
        print('   %r' % n[:90])
