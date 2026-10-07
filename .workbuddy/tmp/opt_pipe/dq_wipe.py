# -*- coding: utf-8 -*-
"""逐张 dump 题面缩水卡的 原文 vs 清洗后，定位差异来源。"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'DQ', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
KEYS = ['题-XeC-12-06', '题-QBY-07-07', '题-CM-60-17', '题-UChO-02-02',
        '题-GChO-46-02', '题-UChO-01-04', '题-UChO-01-07', '题-UChO-15-UChO-08']


def nws(s):
    return re.sub(r'\s+', '', s)


def find(k):
    for base in ['chemy', '化英社', 'XeChem', '汇智', '伽马', '球球', '质心', '北京夏令营', 'ICHO']:
        pass
    import glob
    fs = glob.glob('04-题库/2026机构初赛模拟题/**/%s-*.md' % k, recursive=True)
    return fs[0] if fs else None


for k in KEYS:
    p = find(k)
    if not p:
        print('!! 未找到', k); continue
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案')
    qraw = t[i + len('## 题目'):j]
    c = BO.X.extract(p)
    # 逐步追踪
    steps = []
    x = c['question']
    steps.append(('raw', x)); x = BO.conv_imgs(x); steps.append(('conv_imgs', x))
    x = BO.clean_q(x)
    steps.append(('clean_q', x))
    q = BO.html_table_to_md(x)
    steps.append(('table_md', q))
    print('=' * 100)
    print('%s | 原文 %d 字 → 清洗后 %d 字' % (os.path.basename(p)[:56], len(nws(qraw)), len(nws(q))))
    WIPE = '题面片段被删'
    for tag, v in steps:
        print('  %-12s %5d 字' % (tag, len(nws(v))))
    # 找 clean_q 里被删的段落
    before = BO.conv_imgs(c['question'])
    after = BO.clean_q(before)
    print('  --- clean_q 前后 diff（仅显示被删行）---')
    import difflib
    bl = before.split('\n'); al = set(after.split('\n'))
    for l in bl:
        if l.strip() and l not in al and len(nws(l)) >= 8:
            print('    - %r' % l[:110])
