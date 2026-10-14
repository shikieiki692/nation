# -*- coding: utf-8 -*-
"""卷 XVI 的图引用：它们实际落在哪些目录？构建器（MEDIA=媒体仓库）能命中几张？"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
t = io.open('04-题库/初赛模拟卷XVI（非有机·答案版）.md', encoding='utf-8-sig').read()
refs = re.findall(r'!\[\[([^\]|]+?\.(?:jpg|jpeg|png))(?:\|[^\]]*)?\]\]', t, re.I)
refs += re.findall(r'!\[[^\]]*\]\(([^)]+?\.(?:jpg|jpeg|png))\)', t, re.I)
names = [os.path.basename(r) for r in refs]
print('卷 XVI 图引用 %d 个（唯一 %d）' % (len(names), len(set(names))))

# 全库索引
loc = collections.defaultdict(list)
for dp, dn, fn in os.walk('.'):
    dn[:] = [d for d in dn if d not in ('.git', '.workbuddy')]
    for f in fn:
        if f in set(names):
            loc[f].append(dp.replace('\\', '/'))

have = [n for n in set(names) if n in loc]
miss = [n for n in set(names) if n not in loc]
print('库内存在 %d ｜ 全库不存在 %d' % (len(have), len(miss)))

top = collections.Counter()
for n in have:
    top[loc[n][0].split('/')[1] if loc[n][0].count('/') >= 1 else loc[n][0]] += 1
print('落点（按二级目录）:')
for k, v in top.most_common(10):
    print('   %-46s %d' % (k, v))

inmedia = [n for n in have if any(p.startswith('./媒体仓库') or p.startswith('媒体仓库') for p in loc[n])]
print()
print('★ 在「媒体仓库/」的: %d / %d' % (len(inmedia), len(set(names))))
print('★ 不在媒体仓库的样例（前 6）:')
for n in [x for x in have if x not in inmedia][:6]:
    print('   %s' % n[:60])
    for p in loc[n][:2]:
        print('        %s' % p[:96])
