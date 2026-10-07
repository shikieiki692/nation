# -*- coding: utf-8 -*-
"""核 2 张「答案真丢」卡的题面是否含被删小问。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'AL2', '--all-years']
import build_org as BO


def norm(s):
    s = re.sub(r'!\[\[[^\]]*\]\]', '', s)
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)
    s = re.sub(r'\s+', '', s)
    return s


for k in ['题-HZ-07-06-金属原子之间的无限键', '题-UChO-02-04-自由基聚合是一种很重要']:
    fs = glob.glob('04-题库/2026机构初赛模拟题/**/%s*.md' % k, recursive=True)
    if not fs:
        print('未找到', k); continue
    p = fs[0]
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); kk = t.find('## 知识点映射')
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c['question'])))
    print('=' * 100)
    print(os.path.basename(p)[:58])
    print(' 题面区 %d / 答案区 %d' % (len(t[i:j]), len(t[j:kk])))
    qn = norm(q)
    for probe in ['6-2-3', '6-2-1'] if 'HZ-07-06' in k else ['4-2-4', '4-2']:
        print('  题面含 %s ? %s' % (probe, probe in qn))
    print(' --- 题面区（前 900）---')
    print(re.sub(r'\n{2,}', '\n', t[i:j])[:900])
    print(' --- 答案区（前 700）---')
    print(re.sub(r'\n{2,}', '\n', t[j:kk])[:700])
