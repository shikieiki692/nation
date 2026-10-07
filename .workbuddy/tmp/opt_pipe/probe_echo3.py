# -*- coding: utf-8 -*-
"""用 CSV 精确路径核实 5 张卡的 a 图与 echo 判据。"""
import os, re, sys, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'EC2', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
rows = list(csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')))
want = ('题面/答案过短', '仅题干回显', '假结构式', '无答案/占位')
for r in rows:
    if r['reason'] not in want:
        continue
    bn = os.path.basename(r['path'])
    if not any(k in bn for k in ['HYS-02-01', 'HYS-02-07', 'XeC-19-02', 'GChO-63-07', 'UChO-02-02', 'FY-无机专题一-01-11']):
        continue
    p = os.path.join(ROOT, r['path'])
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    c = BO.X.extract(p)
    q0 = BO.conv_imgs(BO.clean_q(c['question']))
    a0 = BO.clean_a(BO.conv_imgs(c['answer']), q0)
    q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
    _an = re.sub(r'\s+', '', a); _qn = re.sub(r'\s+', '', q)
    r_ = BO.contain_ratio(_an, _qn)
    print('=' * 100)
    print('%-12s | %s' % (r['reason'], bn[:58]))
    print('  清洗后 q=%d字 a=%d字 | a图=%d | ratio=%.3f 非回显=%d' % (
        len(_qn), len(_an), len(re.findall(r'!\[\[', a)), r_, len(_an) * (1 - r_)))
    print('  a 前置 300:', re.sub(r'\n{2,}', '\n', a)[:300])
