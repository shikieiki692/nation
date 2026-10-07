# -*- coding: utf-8 -*-
"""扫「题面近空/极短」的卡（清洗后纯文本 < 40 字），这才是真问题形态。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'QQ', '--all-years']
import build_org as BO


def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'[|]', '', s)
    return re.sub(r'\s+', '', s)


cards = glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
short = []
for p in cards:
    try:
        c = BO.X.extract(p)
        q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c['question'])))
    except Exception:
        continue
    w = len(plain(q))
    imgs = len(re.findall(r'!\[\[|!\[[^\]]*\]\(', q))
    if w < 40:
        short.append((w, imgs, p))

print('题面纯文本 < 40 字 的卡：%d 张' % len(short))
for w, imgs, p in sorted(short):
    print('  题面 %3d 字 / 图 %2d | %s' % (w, imgs, os.path.basename(p)[:56]))
