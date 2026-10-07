# -*- coding: utf-8 -*-
"""逐步骤追踪 UChO-02-02 的题面清洗 与 HYS-02-07 的答案清洗（图片去向）。"""
import os, re, sys, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'TR9', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
rows = list(csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')))


def nws(s):
    return len(re.sub(r'\s+', '', s))


def get(bn_key):
    for r in rows:
        if bn_key in os.path.basename(r['path']):
            return os.path.join(ROOT, r['path'])
    return None


# ---- UChO-02-02 题面链路 ----
p = get('UChO-02-02')
print('#' * 100)
print('UChO-02-02 题面链路:', os.path.basename(p))
c = BO.X.extract(p)
x = c['question']
print('  extract.question     %5d 字' % nws(x))
for name in ['strip_src_heading', 'flatten_layout_tables', 'drop_empty_headings',
             'flatten_subq_headings', 'strip_artifacts', 'fix_orphan_tables', 'fix_tex']:
    before = nws(x)
    x = getattr(BO, name)(x)
    print('  %-22s %5d → %5d' % (name, before, nws(x)))
print('  --- 清洗后全文 ---'); print(x[:500])

# ---- HYS-02-07 答案链路 ----
p2 = get('HYS-02-07-万物')
print()
print('#' * 100)
print('HYS-02-07 答案链路:', os.path.basename(p2))
c2 = BO.X.extract(p2)
q0 = BO.conv_imgs(BO.clean_q(c2['question']))
a = BO.conv_imgs(c2['answer'])
print('  conv_imgs(answer)   %5d 字 / 图 %d' % (nws(a), len(re.findall(r'!\[\[', a))))
for name in ['strip_src_heading', 'flatten_layout_tables']:
    before = (nws(a), len(re.findall(r'!\[\[', a)))
    a = getattr(BO, name)(a)
    print('  %-22s %5d→%5d 字 / 图 %d→%d' % (name, before[0], nws(a), before[1], len(re.findall(r'!\[\[', a))))
before = (nws(a), len(re.findall(r'!\[\[', a)))
a = BO.strip_q_echo(q0, a)
print('  %-22s %5d→%5d 字 / 图 %d→%d' % ('strip_q_echo', before[0], nws(a), before[1], len(re.findall(r'!\[\[', a))))
print('  --- strip_q_echo 前全文 ---')
b = BO.strip_src_heading(BO.conv_imgs(c2['answer'])); b = BO.flatten_layout_tables(b)
print(repr(b[:600]))
