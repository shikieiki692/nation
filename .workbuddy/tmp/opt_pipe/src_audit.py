# -*- coding: utf-8 -*-
"""提取初赛模拟卷里所有「> 来源：」行的机构/届次分布，并与 chemy 卡片库对账。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
VOL = sorted(glob.glob('04-题库/初赛模拟卷*（非有机·答案版）.md')) + \
      sorted(glob.glob('04-题库/初赛模拟卷*（非有机·学生版）.md'))
print('卷文件数:', len(VOL))

SRC = re.compile(r'^>\s*来源[:：]\s*(.+)$', re.M)
inst = collections.Counter()
edition = collections.Counter()
rows = []
for p in VOL:
    t = io.open(p, encoding='utf-8-sig').read()
    vol = os.path.basename(p).replace('初赛模拟卷', '').replace('（非有机·答案版）.md', '').replace('（非有机·学生版）.md', '')
    for m in SRC.finditer(t):
        s = m.group(1).strip()
        rows.append((vol, s))
        # 机构 = 第一个空格前的词
        head = s.split()[0] if s.split() else '?'
        inst[head] += 1
        e = re.search(r'第\s*(\d+)\s*届', s)
        edition[e.group(1) if e else '(无届次)'] += 1

print('\n=== 来源行总数:', len(rows), '===')
print('--- 按机构（首词）---')
for k, v in inst.most_common(30):
    print('   %-14s %d' % (k, v))
print('--- 按届次 ---')
for k, v in sorted(edition.items()):
    print('   %-8s %d' % (k, v))

print('\n=== 含「第40届」的来源行（去重）===')
seen = set()
for vol, s in rows:
    if '第40届' in s.replace(' ', '') and s not in seen:
        seen.add(s)
        print('   [卷%s] %s' % (vol, s))
print('   共 %d 条不同' % len(seen))
