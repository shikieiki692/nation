# -*- coding: utf-8 -*-
"""验证 strip_src_heading 新实现：受影响卡补回正文；正常卡不变。"""
import os, re, sys, glob, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'H1V', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'


def old_strip(s):
    lines = s.split('\n')
    i = 0
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    if i < len(lines) and re.match(r'^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题', lines[i].strip()):
        i += 1
        while i < len(lines) and lines[i].strip() == '':
            i += 1
        s = '\n'.join(lines[i:])
    return s


def nws(s):
    return len(re.sub(r'\s+', '', s))


cards = glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
changed, same = 0, 0
diffs = []
for p in cards:
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案')
    if i < 0 or j < 0:
        continue
    qz = t[i + len('## 题目'):j]
    a, b = old_strip(qz), BO.strip_src_heading(qz)
    if a == b:
        same += 1
    else:
        changed += 1
        diffs.append((nws(b) - nws(a), p, a, b))

print('题面：变化 %d 张 / 不变 %d 张' % (changed, same))
print()
for d, p, a, b in sorted(diffs, reverse=True)[:12]:
    print('  +%3d 字 | %s' % (d, os.path.basename(p)[:52]))
    newfirst = [l for l in b.split('\n') if l.strip()][:1]
    print('        新首行: %r' % (newfirst[0][:90] if newfirst else ''))

# 答案区同样检查（clean_a 也用 strip_src_heading）
cchanged = 0
for p in cards:
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    j = t.find('## 参考答案'); k = t.find('## 知识点映射')
    if j < 0 or k < 0:
        continue
    az = t[j + len('## 参考答案'):k]
    if old_strip(az) != BO.strip_src_heading(az):
        cchanged += 1
print()
print('答案区：变化 %d 张' % cchanged)
