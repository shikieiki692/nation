# -*- coding: utf-8 -*-
"""复测：HYS-02-06 的 clean_q / html_table_to_md 是否真丢内容（用文件版 strip_md）。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'DBG2', '--all-years']
import build_org as BO

N = 14


def strip_md(s):
    s = re.sub(r'!\[\[[^\]]*\]\]', '', s)
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'[#*`>_~\[\](){}|\s]', '', s)
    s = re.sub(r'-', '', s)
    return s


def ng(s):
    return {s[i:i + N] for i in range(len(s) - N + 1)} if len(s) >= N else set()


p = glob.glob('04-题库/2026机构初赛模拟题/**/题-HYS-02-06-表面张力*.md', recursive=True)[0]
print('file:', os.path.basename(p))
t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
i = t.find('## 题目'); j = t.find('## 参考答案')
rawq = t[i + len('## 题目'):j]
c = BO.X.extract(p)
q0 = BO.conv_imgs(BO.clean_q(c['question']))
q = BO.html_table_to_md(q0)
qr = strip_md(BO.conv_imgs(rawq))
qn = strip_md(q)
print('rawq file zone=%d  extract.q=%d' % (len(rawq), len(c['question'])))
print('strip(rawq)=%d  strip(q)=%d  clean_q=%d  table_md=%d' % (
    len(qr), len(qn), len(re.sub(r'\s+', '', q0)), len(re.sub(r'\s+', '', q))))
print('nonws(q0)=%d nonws(q)=%d' % (len(re.sub(r'\s+', '', q0)), len(re.sub(r'\s+', '', q))))
lost = ng(qr) - ng(qn)
print('lost grams=%d' % len(lost))
for x in sorted(lost)[:3]:
    idx = qr.find(x)
    print('  GRAM %r  raw[%d:]= %r' % (x, idx, qr[max(0, idx - 15):idx + 40]))
