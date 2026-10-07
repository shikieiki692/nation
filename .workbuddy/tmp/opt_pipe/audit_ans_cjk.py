# -*- coding: utf-8 -*-
"""最终判定：答案删块的「CJK 骨架」是否出现在题面 CJK 骨架里（对 LaTeX 差异免疫）。"""
import os, re, sys, glob, csv, difflib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'CJK', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
CJK = re.compile(r'[\u4e00-\u9fff]+')


def skel(s, minrun=6):
    """取连续中文段（≥6 字）的集合。"""
    return set(x for x in CJK.findall(s) if len(x) >= minrun)


def dels(old, new, minsz=25):
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    return [old[i1:i2] for tag, i1, i2, j1, j2 in sm.get_opcodes()
            if tag in ('delete', 'replace') and (i2 - i1) >= minsz]


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
        rawq, rawa = t[i:j], t[j + len('## 参考答案'):k]
        c = BO.X.extract(p)
        q0 = BO.conv_imgs(BO.clean_q(c['question']))
        a0 = BO.clean_a(BO.conv_imgs(c['answer']), q0)
        q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
        qsk = skel(q) | skel(rawq)
        bad = []
        for b in dels(rawa.replace('<', ' <').replace('>', '> '), a, 0):
            pass
        # 用与 pipeline 一致的输入做 diff
        rawa2 = re.sub(r'\s+', '', re.sub(r'!\[\[[^\]]*\]\]', '', re.sub(r'!\[[^\]]*\]\([^)]*\)', '', BO.conv_imgs(rawa))))
        an2 = re.sub(r'\s+', '', re.sub(r'!\[\[[^\]]*\]\]', '', re.sub(r'!\[[^\]]*\]\([^)]*\)', '', a)))
        for b in dels(rawa2, an2, 25):
            bs = skel(b)
            if not bs:
                continue
            covered = sum(1 for x in bs if any(x in y or y in x for y in qsk)) / len(bs)
            if covered < 0.5:
                bad.append((b, covered))
        if bad:
            out.append((p, bad))
    print('入池 %d；答案「骨架不在题面」卡 %d 张' % (len(cards), len(out)))
    for p, bad in sorted(out, key=lambda x: -sum(len(b) for b, _ in x[1]))[:25]:
        print('  %s | %d 块' % (os.path.basename(p)[:50], len(bad)))
        for b, cv in sorted(bad, key=lambda x: -len(x[0]))[:2]:
            print('       cov=%.2f (%3d) %r' % (cv, len(b), b[:100]))


main()
