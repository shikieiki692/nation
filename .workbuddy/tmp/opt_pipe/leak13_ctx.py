# -*- coding: utf-8 -*-
"""打印 13 张「题面泄露」卡的 LEAK 命中 token 与上下文（修复后闸门）。"""
import os, re, sys, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'LEAK13', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
rows = list(csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')))
for r in rows:
    if r['reason'] != '题面泄露':
        continue
    p = os.path.join(ROOT, r['path'])
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    c = BO.X.extract(p)
    q0 = BO.conv_imgs(BO.clean_q(c['question']))
    q = BO.html_table_to_md(q0)
    ow = BO.own_qno(t, p)
    qchk = re.sub(r'^#{0,4}[^\S\n]*第[^\S\n]*%s[^\S\n]*[题題][^\n]*$' % BO.num_alt(ow), '', q, flags=re.M)
    print('=' * 98)
    print('%-10s own=%-3s %s' % (r['inst'], ow, os.path.basename(p)[:52]))
    seen = set()
    for mm in BO.LEAK.finditer(qchk):
        g = mm.group(0)
        if g in seen:
            continue
        seen.add(g)
        ls = qchk.rfind('\n', 0, mm.start()) + 1
        le = qchk.find('\n', mm.start())
        line = qchk[ls:le if le > 0 else len(qchk)]
        print('   [%s] 行: %s' % (g, line[:120]))
        if len(seen) >= 2:
            break
