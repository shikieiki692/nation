# -*- coding: utf-8 -*-
"""用 difflib opcodes 打印「被删文本块」，直接目视判断是否真丢。"""
import os, re, sys, glob, difflib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'DD', '--all-years']
import build_org as BO


def norm(s):
    s = re.sub(r'!\[\[[^\]]*\]\]', '', s)
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)
    s = re.sub(r'</?[a-zA-Z][^>]*>', '', s)
    s = re.sub(r'\s+', '', s)
    return s


def deleted_blocks(old, new, minsz=25):
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ('delete', 'replace') and (i2 - i1) >= minsz:
            out.append(old[i1:i2])
    return out


KEYS = ['题-GM-23-02', '题-YJ-11-04', '题-GChO-65-08', '题-HYS-09-03']
for k in KEYS:
    fs = glob.glob('04-题库/2026机构初赛模拟题/**/%s*.md' % k, recursive=True)
    if not fs:
        print('未找到', k); continue
    p = fs[0]
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); kk = t.find('## 知识点映射')
    rawq, rawa = t[i + len('## 题目'):j], t[j + len('## 参考答案'):kk]
    c = BO.X.extract(p)
    q0 = BO.conv_imgs(BO.clean_q(c['question']))
    a0 = BO.clean_a(BO.conv_imgs(c['answer']), q0)
    q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
    print('=' * 100)
    print(os.path.basename(p)[:60])
    for tag, old, new in (('题面', norm(BO.conv_imgs(rawq)), norm(q)),
                          ('答案', norm(BO.conv_imgs(rawa)), norm(a))):
        blks = deleted_blocks(old, new)
        tot = sum(len(b) for b in blks)
        print('  [%s] 删块 %d 个 / 共 %d 字' % (tag, len(blks), tot))
        for b in sorted(blks, key=len, reverse=True)[:4]:
            print('      -(%3d) %r' % (len(b), b[:120]))
