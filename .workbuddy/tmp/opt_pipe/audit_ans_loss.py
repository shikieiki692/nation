# -*- coding: utf-8 -*-
"""决定性判据：答案区被删块在题面里的 8-gram 包含度 < 0.3 ⇒ 真丢（否则＝回显）。"""
import os, re, sys, glob, csv, difflib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'ANSL', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'


def norm(s):
    s = re.sub(r'!\[\[[^\]]*\]\]', '', s)
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)
    s = re.sub(r'</?[a-zA-Z][^>]*>', '', s)
    s = re.sub(r'\s+', '', s)
    return s


def dels(old, new, minsz=25):
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    return [old[i1:i2] for tag, i1, i2, j1, j2 in sm.get_opcodes()
            if tag in ('delete', 'replace') and (i2 - i1) >= minsz]


def cont(b, ref, n=8):
    if len(b) < n:
        return 1.0 if b in ref else 0.0
    gs = [b[i:i + n] for i in range(0, len(b) - n + 1, 2)]
    return sum(1 for g in gs if g in ref) / len(gs)


def main():
    pool = set()
    with open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['verdict'] == '入池':
                pool.add(os.path.basename(r['path']))
    cards = [p for p in glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
             if os.path.basename(p) in pool]
    out = []
    for p in cards:
        t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
        i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
        if i < 0 or j < 0 or k < 0:
            continue
        rawa = t[j + len('## 参考答案'):k]
        c = BO.X.extract(p)
        q0 = BO.conv_imgs(BO.clean_q(c['question']))
        a0 = BO.clean_a(BO.conv_imgs(c['answer']), q0)
        q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
        qn, an = norm(q), norm(a)
        ra = norm(BO.conv_imgs(rawa))
        bad = []
        for b in dels(ra, an):
            if cont(b, qn) < 0.3:
                bad.append(b)
        if bad:
            out.append((p, bad))
    print('入池 %d 张；答案「真丢」卡 %d 张' % (len(cards), len(out)))
    for p, bad in sorted(out, key=lambda x: -sum(len(b) for b in x[1]))[:30]:
        print('  %s | %d 块 共 %d 字' % (os.path.basename(p)[:48], len(bad), sum(len(b) for b in bad)))
        for b in sorted(bad, key=len, reverse=True)[:2]:
            print('       -(%3d) %r' % (len(b), b[:110]))


main()
