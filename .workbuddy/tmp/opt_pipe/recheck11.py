# -*- coding: utf-8 -*-
"""复核 11 张：删块骨架是否在「清洗后的答案」里（是 ⇒ 只是格式转换，非丢失）。"""
import os, re, sys, glob, csv, difflib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'F11', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
CJK = re.compile(r'[\u4e00-\u9fff]+')
KEYS = ['题-CM-01-02', '题-XeC-40-02', '题-HYS-10-02', '题-HZ-08-01', '题-HYS-10-06',
        '题-XeC-15-01', '题-HYS-07-06', '题-HYS-01-05', '题-YS-07-08', '题-YS-08-05', '题-HYS-15-01']


def skel(s, minn=6):
    return set(x for x in CJK.findall(s) if len(x) >= minn)


def dels(old, new, minsz=25):
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    return [old[i1:i2] for tag, i1, i2, j1, j2 in sm.get_opcodes()
            if tag in ('delete', 'replace') and (i2 - i1) >= minsz]


for k in KEYS:
    fs = glob.glob('04-题库/2026机构初赛模拟题/**/%s-*.md' % k, recursive=True)
    fs = [x for x in fs if os.path.basename(x).startswith(k)]
    if not fs:
        print('未找到', k); continue
    p = fs[0]
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); kk = t.find('## 知识点映射')
    rawa = t[j + len('## 参考答案'):kk]
    c = BO.X.extract(p)
    q0 = BO.conv_imgs(BO.clean_q(c['question']))
    a0 = BO.clean_a(BO.conv_imgs(c['answer']), q0)
    q, a = BO.html_table_to_md(q0), BO.html_table_to_md(a0)
    stripim = lambda s: re.sub(r'\s+', '', re.sub(r'!\[\[[^\]]*\]\]', '', re.sub(r'!\[[^\]]*\]\([^)]*\)', '', BO.conv_imgs(s))))
    rawa2, an2 = stripim(rawa), stripim(a)
    qsk, ask = skel(q) | skel(t[i:j]), skel(a)
    print('=' * 96)
    print(os.path.basename(p)[:56])
    for b in sorted(dels(rawa2, an2), key=len, reverse=True)[:2]:
        bs = skel(b)
        cq = sum(1 for x in bs if any(x in y or y in x for y in qsk)) / max(1, len(bs)) if bs else 1
        ca = sum(1 for x in bs if any(x in y or y in x for y in ask)) / max(1, len(bs)) if bs else 1
        print('  块(%3d) 题面覆盖=%.2f 清洗后答案覆盖=%.2f → %s' % (
            len(b), cq, ca, '格式转换(非丢)' if ca >= 0.5 else '?? 真丢?'))
        print('      %r' % b[:90])
