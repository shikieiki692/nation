# -*- coding: utf-8 -*-
"""看疑似「题干在标题行」的卡：标题区全文 + 清洗后题面，判断是否真丢。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'LH', '--all-years']
import build_org as BO

KEYS = ['题-XeC-14-01-112写出A与B', '题-CM-60-22-将金属镧', '题-XeC-14-06-61将101mg',
        '题-GM-03-05', '题-CM-60-17', '题-HYS-03-01']


def nws(s):
    return len(re.sub(r'\s+', '', s))


def find(k):
    fs = glob.glob('04-题库/2026机构初赛模拟题/**/%s*.md' % k, recursive=True)
    return fs[0] if fs else None


for k in KEYS:
    p = find(k)
    if not p:
        print('!! 未找到', k); continue
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案')
    qz = t[i:j]
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c['question'])))
    print('=' * 100)
    print('%s' % os.path.basename(p)[:58])
    print('  原文题面区 %d 字 → 清洗后 %d 字' % (nws(qz), nws(q)))
    print('  --- 原文题面区（前 6 行）---')
    for l in [x for x in qz.split('\n') if x.strip()][:6]:
        print('    %r' % l[:120])
    print('  --- 清洗后题面（前 260 字）---')
    print('    ' + re.sub(r'\n{2,}', ' | ', q)[:260])
