# -*- coding: utf-8 -*-
"""题面指纹去重验证：算全池卡的指纹，找出重复组，并对比「现有 fp」与「新 fp」。"""
import os, re, sys, glob, collections

sys.stdout.reconfigure(encoding='utf-8')
BASE = '04-题库/2026机构初赛模拟题'
SRCS = ['化英社', '清北营', 'chemy', '伽马', '壹尖培优', '汇智', 'XeChem',
        '质心GChO', '质心UChO', '方圆', '一式', '北京夏令营', '2ChO']


def qsec(t):
    i = t.find('## 题目'); j = t.find('## 参考答案')
    return t[i:j] if j > i > 0 else (t[i:] if i > 0 else '')


def cur_fp(q):
    q_fp = re.sub(r'^#{3,4}\s*第\s*\d+\s*题[^\n]*\n', '', q, count=1, flags=re.M)
    return re.sub(r'\s+', '', q_fp)[:120]


def norm_deep(q):
    s = q
    s = re.sub(r'!\[\[?[^\]]*\]?\]', '', s)
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)
    s = re.sub(r'<img[^>]*>', '', s)
    s = re.sub(r'(?m)^#{1,6}\s*第\s*[0-9一二三四五六七八九十]+\s*题[^\n]*$', '', s)
    s = re.sub(r'(?m)^#{1,6}.*$', '', s)
    # 去 LaTeX
    s = re.sub(r'\$[^$]*\$', '', s)
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    s = re.sub(r'[\\{}^_&]', '', s)
    # 去所有非中英文数字
    s = re.sub(r'[^\u4e00-\u9fffa-zA-Z0-9]', '', s)
    s = re.sub(r'[0-9]+', '', s)
    return s


cards = []
for r in SRCS:
    for p in glob.glob(os.path.join(BASE, r, '**', '题-*.md'), recursive=True):
        t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
        q = qsec(t)
        if len(re.sub(r'\s+', '', q)) < 60:
            continue
        cards.append((p, cur_fp(q), norm_deep(q)))

print('参与卡数：%d' % len(cards))
for name, getter in [('现有fp(120)', lambda c: c[1]), ('新fp(150)', lambda c: c[2][:150])]:
    g = collections.defaultdict(list)
    for p, c1, c2 in cards:
        k = getter((p, c1, c2))
        if k:
            g[k].append(p)
    dups = {k: v for k, v in g.items() if len(v) > 1}
    n = sum(len(v) for v in dups.values())
    print('\n=== %s ：重复组 %d，涉及 %d 卡 ===' % (name, len(dups), n))
    for k, v in list(dups.items())[:20]:
        print('  ×%d  %s' % (len(v), ' 、 '.join(os.path.basename(x).replace('题-', '')[:16] for x in v)))
