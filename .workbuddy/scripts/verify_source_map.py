# -*- coding: utf-8 -*-
"""逐章交叉验证：溯源映射.json 的 (module, chapter) 题数 == 成书章节文件 question_count"""
import io, json, os, re

R = r'C:\Obsidion\妙妙屋'
BK = os.path.join(R, '04-课件', '习题集', '四·成书层（习题书）', '习题书-教师版')
PIAN = {'化学原理': '第一篇-化学原理', '结构化学': '第二篇-结构化学',
        '有机化学': '第三篇-有机化学', '元素与分析': '第四篇-元素与分析'}

d = json.load(io.open(os.path.join(R, '04-课件', '习题集', '溯源映射.json'), encoding='utf-8'))
print('generated =', d['generated'], '| total =', d['total'], '| rows =', len(d['rows']))

from collections import Counter
cnt = Counter((r['module'], r['chapter_num'], r['chapter_name']) for r in d['rows'])
print('分组数 =', len(cnt))

bad = 0
for module, pian in PIAN.items():
    p = os.path.join(BK, pian)
    files = [f for f in os.listdir(p) if f.endswith('.md') and f not in ('目录.md',)]
    book = {}
    for f in files:
        t = io.open(os.path.join(p, f), encoding='utf-8').read(3000)
        m = re.search(r'(?m)^question_count:\s*(\d+)', t)
        book[f] = int(m.group(1)) if m else None
    # 映射侧
    mp = {}
    for (mod, num, name), n in cnt.items():
        if mod == module:
            mp['%s-%s.md' % (num, name)] = n
    print('\n### %s  成书 %d 个文件 / 映射 %d 章' % (module, len(book), len(mp)))
    for f in sorted(book):
        b = book[f]
        m2 = mp.get(f)
        # 目录.md 是篇汇总，不参与
        if f == '目录.md':
            continue
        flag = 'OK ' if b == m2 else '❌ '
        if b != m2:
            bad += 1
        if b != m2 or f not in mp:
            print('   %s 成书=%-5s 映射=%-5s %s' % (flag, b, m2, f))
    extra = set(mp) - set(book)
    if extra:
        print('   ⚠️ 映射多出:', sorted(extra))
print('\n不一致条目数 =', bad)
print('全部一致' if bad == 0 else '存在不一致')

# 抽样一条
print('\n样例行:')
for r in d['rows'][:2] + d['rows'][-2:]:
    print('  ', r['module'], r['chapter_num'], r['chapter_name'], r['book_num'], '|', r['title'][:30], '|', r['src_path'][:60])
