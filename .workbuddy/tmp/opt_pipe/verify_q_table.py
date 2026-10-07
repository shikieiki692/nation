# -*- coding: utf-8 -*-
"""验证 html_table_to_md 是否真的丢内容（比对剥标签后的纯文本）。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'QT', '--all-years']
import build_org as BO

KEYS = ['题-QBY-07-07', '题-CM-60-17', '题-GChO-46-02', '题-UChO-01-07']


def plain(s):
    s = re.sub(r'<[^>]+>', '', s)          # 去 HTML 标签
    s = re.sub(r'\|', '', s)               # 去管道符
    s = re.sub(r'[-:]{3,}', '', s)         # 去分隔行
    return re.sub(r'\s+', '', s)


def find(k):
    fs = glob.glob('04-题库/2026机构初赛模拟题/**/%s-*.md' % k, recursive=True)
    return fs[0] if fs else None


for k in KEYS:
    p = find(k)
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    c = BO.X.extract(p)
    x = BO.clean_q(BO.conv_imgs(c['question']))
    y = BO.html_table_to_md(x)
    print('=' * 100)
    print('%s' % os.path.basename(p)[:60])
    print('  clean_q 版: %d 字（含标签）→ 纯文本 %d 字' % (len(x), len(plain(x))))
    print('  table_md 版: %d 字（含标签）→ 纯文本 %d 字' % (len(y), len(plain(y))))
    print('  纯文本差: %d' % (len(plain(x)) - len(plain(y))))
    # 找 table_md 后丢掉的行（按纯文本比对）
    xl = [l for l in x.split('\n') if plain(l)]
    yjoin = plain(y)
    lost = [l for l in xl if len(plain(l)) >= 10 and plain(l) not in yjoin]
    print('  --- 疑丢行（%d 条）---' % len(lost))
    for l in lost[:8]:
        print('    - %r' % l[:120])
