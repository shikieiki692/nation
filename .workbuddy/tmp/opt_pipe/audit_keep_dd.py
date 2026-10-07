# -*- coding: utf-8 -*-
"""全库「内容保真筛」· 位置对齐版（difflib）。

对每张入池卡：比对 源卡原文 与 最终清洗 q/a 的**被删文本块**（≥25 字），
  - 题面删块 ⊆ 标题行（题号+题名+分值） ⇒ 合规
  - 答案删块 ⊆ 题面文本（回显）            ⇒ 合规
其余一律报出。
"""
import os, re, sys, glob, difflib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'ALLDD', '--all-years']
import build_org as BO


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


def main():
    import csv
    root = r'C:\Obsidion\妙妙屋'
    pool = set()
    with open(os.path.join(root, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['verdict'] == '入池':
                pool.add(os.path.basename(r['path']))
    cards = [p for p in glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
             if os.path.basename(p) in pool]
    print('待检入池卡 %d 张' % len(cards), flush=True)
    sq, sa = [], []
    n = 0
    for p in cards:
        t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
        i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
        if i < 0 or j < 0 or k < 0:
            continue
        rawq, rawa = t[i + len('## 题目'):j], t[j + len('## 参考答案'):k]
        m = re.search(r'(?m)^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题[^\n]*$', rawq)
        head = norm(m.group(0)) if m else ''
        try:
            c = BO.X.extract(p)
            q0 = BO.conv_imgs(BO.clean_q(c['question']))
            a0 = BO.clean_a(BO.conv_imgs(c['answer']), q0)
            q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
        except Exception:
            continue
        if len(re.sub(r'\s+', '', q)) < 60 or len(re.sub(r'\s+', '', a)) < 25:
            continue
        n += 1
        qr, ra = norm(BO.conv_imgs(rawq)), norm(BO.conv_imgs(rawa))
        qn, an = norm(q), norm(a)
        bq = [b for b in dels(qr, qn) if b not in head]
        if not bq and head:
            # 题面里删的块可能只是标题的一部分 —— 逐个字符核
            pass
        if bq:
            sq.append((p, bq))
        # 答案删块：能否在题面里**模糊**找到（strip_q_echo 是模糊匹配）⇒ 才算回显
        def frag_in(b, ref, n=12, th=0.6):
            if len(b) < n:
                return b in ref
            gs = [b[i:i + n] for i in range(0, len(b) - n + 1, n // 2)]
            return sum(1 for g in gs if g in ref) / len(gs) >= th
        ba = [b for b in dels(ra, an) if not frag_in(b, qn)]
        if ba:
            sa.append((p, ba))
    print('入池粗判 %d 张' % n)
    print('=== 题面疑丢 %d 张 ===' % len(sq))
    for p, blks in sorted(sq, key=lambda x: -sum(len(b) for b in x[1]))[:25]:
        print('  %s | %d 块' % (os.path.basename(p)[:50], len(blks)))
        for b in sorted(blks, key=len, reverse=True)[:2]:
            print('       -(%3d) %r' % (len(b), b[:110]))
    print('=== 答案疑丢 %d 张 ===' % len(sa))
    for p, blks in sorted(sa, key=lambda x: -sum(len(b) for b in x[1]))[:25]:
        print('  %s | %d 块' % (os.path.basename(p)[:50], len(blks)))
        for b in sorted(blks, key=len, reverse=True)[:2]:
            print('       -(%3d) %r' % (len(b), b[:110]))


main()
