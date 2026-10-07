# -*- coding: utf-8 -*-
"""实核 2 张双 0 覆盖卡：CM-01-02 / YS-07-08。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'Z2', '--all-years']
import build_org as BO

for k in ['题-CM-01-02-奎宁', '题-YS-07-08-81选出']:
    fs = [x for x in glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
          if os.path.basename(x).startswith(k)]
    if not fs:
        print('未找到', k); continue
    p = fs[0]
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); kk = t.find('## 知识点映射')
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c['question'])))
    a = BO.html_table_to_md(BO.clean_a(BO.conv_imgs(c['answer']), BO.conv_imgs(BO.clean_q(c['question']))))
    print('=' * 100)
    print(os.path.basename(p)[:58])
    print(' 题面区 %d / 答案区 %d；清洗 q=%d a=%d' % (
        len(t[i:j]), len(t[j:kk]), len(re.sub(r'\s+', '', q)), len(re.sub(r'\s+', '', a))))
    print(' --- 题面区（全）---')
    print(re.sub(r'\n{2,}', '\n', t[i:j])[:1000])
    print(' --- 答案区（前 700）---')
    print(re.sub(r'\n{2,}', '\n', t[j:kk])[:700])
