# -*- coding: utf-8 -*-
"""查伽马/XeChem 的「试题 vs 答案」配对（能否回源重建）。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Obsidion\妙妙屋'

def heads(p, n=12):
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    print('   %s  (%d 字)' % (os.path.basename(p), len(t)))
    for m in list(re.finditer(r'(?m)^#{1,6} .*$', t))[:n]:
        print('      @%6d %s' % (m.start(), m.group(0)[:66]))
    return t

print('=== 伽马: gamma晶体结构习题.md ===')
heads(os.path.join(ROOT, r'2026机构初赛模拟题\06-伽马\gamma晶体结构习题.md'))
print('=== 伽马: 晶体题答案.md ===')
heads(os.path.join(ROOT, r'2026机构初赛模拟题\06-伽马\晶体题答案.md'))
print()
print('=== XeChem 目录里含「模拟三」的文件 ===')
for f in glob.glob(os.path.join(ROOT, '2026机构初赛模拟题/03-XeChem/*')):
    if '三' in os.path.basename(f) or '晶体' in os.path.basename(f):
        print('   ', os.path.basename(f)[:80])
print('=== 03-XeChem 全部 md ===')
for f in sorted(glob.glob(os.path.join(ROOT, '2026机构初赛模拟题/03-XeChem/*.md'))):
    print('   ', os.path.basename(f)[:80])
