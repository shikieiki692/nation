# -*- coding: utf-8 -*-
"""测「反向回显剥离」：从题面删掉**在答案区确实存在**的段落，能救几张？（只测，不改卡）"""
import csv, os, re, sys, difflib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'REV', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'


def nz(s):
    return re.sub(r'[#\s{}]', '', s)


def strip_a_echo(q, a):
    """从题面剔除「在答案区确实存在」的段落（删除后信息不丢）。"""
    asegs = [nz(p) for p in re.split(r'\n{2,}', a)]
    asegs = [s for s in asegs if len(s) >= 12]
    aset = set(asegs)
    keep, dropped = [], 0
    for p in re.split(r'\n{2,}', q):
        pn = nz(p)
        if len(pn) >= 12 and (pn in aset or any(pn in s for s in asegs)):
            dropped += len(pn)
            continue
        keep.append(p)
    return '\n\n'.join(keep), dropped


rows = [r for r in csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig'))
        if r['reason'] in ('题面泄露', '仅题干回显')]
for r in rows:
    p = os.path.join(ROOT, r['path'])
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
    c = BO.X.extract(p)
    q0 = BO.conv_imgs(BO.clean_q(c['question']))
    a0 = BO.clean_a(BO.conv_imgs(c['answer']), q0)
    q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
    q2, dropped = strip_a_echo(q, a)
    ow = BO.own_qno(t, p)
    def leak(x):
        xc = re.sub(r'^#{0,4}[^\S\n]*第[^\S\n]*%s[^\S\n]*[題题][^\n]*$' % BO.num_alt(ow), '', x, flags=re.M)
        return bool(BO.LEAK.search(xc))
    print('%-42s | 题面 %4d→%4d（删%d）| 泄露 %s→%s | q_len_before=%d after=%d' % (
        os.path.basename(p)[:40], len(nz(q)), len(nz(q2)), dropped,
        'Y' if leak(q) else 'N', 'Y' if leak(q2) else 'N', len(nz(q)), len(nz(q2))))
