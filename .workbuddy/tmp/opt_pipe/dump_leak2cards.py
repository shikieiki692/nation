# -*- coding: utf-8 -*-
"""看 2 张「题面泄露」卡的清洗后题面全文（判断泄露是否只由评分行造成）。"""
import os, re, sys, csv, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'L2', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
KEYS = ['题-HYS-02-03-理想溶液', '题-HZ-37-09-91关于晶格能']
for k in KEYS:
    p = glob.glob('04-题库/2026机构初赛模拟题/**/%s*.md' % k, recursive=True)[0]
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c['question'])))
    print('=' * 100)
    print(os.path.basename(p)[:60], '| q=%d 字' % len(re.sub(r'\s+', '', q)))
    lines = [l for l in q.split('\n') if l.strip()]
    for l in lines[:22]:
        mark = '  <<< 泄露行' if BO.LEAK.search(l) else ''
        print('   %s%s' % (l[:118], mark))
    print('   ...（共 %d 非空行）' % len(lines))
