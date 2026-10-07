# -*- coding: utf-8 -*-
"""核 310 张「答案疑丢」：删块首 60 字是否出现在题面（回显）？还是真丢？"""
import os, re, sys, glob, csv, difflib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'ANSC', '--all-years']
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


KEYS = ['题-HYS-02-06-表面张力', '题-CM-17-05', '题-HZ-02-01', '题-QBY-02-05-本题记丙酮']
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
    qn, an = norm(q), norm(a)
    ra = norm(BO.conv_imgs(rawa))
    print('=' * 100)
    print(os.path.basename(p)[:58], '| 答案区原文 %d → 清洗后 %d' % (len(ra), len(an)))
    for b in sorted(dels(ra, an), key=len, reverse=True)[:3]:
        head = b[:60]
        print('  删块(%d) 首60=%r' % (len(b), head))
        print('       首60在题面? %s   在答案清洗后? %s' % (head in qn, b in an))
