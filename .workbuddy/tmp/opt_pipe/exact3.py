# -*- coding: utf-8 -*-
"""精确路径：核实 UChO-02-02-21给出XY / GChO-63-07 / XeC-19-02。"""
import os, re, sys, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'EX', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
rows = list(csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')))


def nws(s):
    return len(re.sub(r'\s+', '', s))


def exact(key):
    """精确匹配：basename == key 或 basename 去掉 .md 后 startswith key（key 含足够长唯一串）。"""
    for r in rows:
        bn = os.path.basename(r['path'])[:-3]
        if bn.startswith(key):
            return os.path.join(ROOT, r['path']), r
    return None, None


for key in ['题-UChO-02-02-21给出XY', '题-GChO-63-07', '题-XeC-19-02']:
    p, r = exact(key)
    print('#' * 100)
    print('%s | %s' % (r['reason'], os.path.basename(p)))
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
    c = BO.X.extract(p)
    q0 = BO.conv_imgs(BO.clean_q(c['question']))
    a = BO.html_table_to_md(BO.clean_a(BO.conv_imgs(c['answer']), q0))
    q = BO.html_table_to_md(q0)
    print('  原文 题面区 %d / 答案区 %d' % (len(t[i:j]), len(t[j:k])))
    print('  清洗 q=%d a=%d | a图=%d' % (nws(q), nws(a), len(re.findall(r'!\[\[', a))))
    print('  --- 题面区原文 ---'); print(re.sub(r'\n{2,}', '\n', t[i:j]).strip()[:800])
    print('  --- 答案区原文 ---'); print(re.sub(r'\n{2,}', '\n', t[j:k]).strip()[:800])
