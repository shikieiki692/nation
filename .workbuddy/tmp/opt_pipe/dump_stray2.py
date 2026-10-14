# -*- coding: utf-8 -*-
r"""Dump 真中目标的孤立 `\\` 上下文（只读，干净版）。"""
import os, io, re
os.chdir(r'C:\Obsidion\妙妙屋')
BLOCK = re.compile(r'\$\$(.+?)\$\$', re.S)
INLINE = re.compile(r'(?<!\$)\$([^$\n]+?)\$(?!\$)')

def stray_positions(seg):
    out = []; i = 0; n = len(seg); stack = []
    m_env = re.compile(r'\\begin\{([a-zA-Z*]+)\}')
    m_end = re.compile(r'\\end\{([a-zA-Z*]+)\}')
    m_sub = re.compile(r'\\substack\s*\{')
    while i < n:
        if seg.startswith('\\\\', i):
            if not stack: out.append(i)
            i += 2; continue
        m = m_env.match(seg, i)
        if m: stack.append('env'); i = m.end(); continue
        m = m_end.match(seg, i)
        if m:
            if stack: stack.pop()
            i = m.end(); continue
        m = m_sub.match(seg, i)
        if m: stack.append('sub'); i = m.end(); continue
        if seg[i] == '}':
            if stack and stack[-1] == 'sub': stack.pop()
            i += 1; continue
        i += 1
    return out

FILES = [
 '04-题库/元文件/有机化学阶段测试卷-答案.md',
 '04-题库/有机化学/有机合成与金属有机/题-有机-合成-Grignard试剂与不同羰基化合物反应路线设计.md',
 '04-题库/2026机构初赛模拟题/汇智/题-HZ-09-05-Cu可以与许多配体形成配合物.md',
 '04-题库/2026机构初赛模拟题/清北营/题-QBY-02-08-将羧基快捷高产率地转化为氰基.md',
 '04-题库/2026机构初赛模拟题/清北营/题-QBY-11-09-91自1977年Kagan等.md',
 '04-题库/2026机构初赛模拟题/质心GChO/题-GChO-58-08-基于对吡啶性质的兴趣和吡啶在.md',
 '04-题库/2026机构初赛模拟题/质心GChO/题-GChO-83-09-氮杂环丙烷具有丰富的反应性9.md',
 '04-题库/2026机构初赛模拟题/质心UChO/题-UChO-02-08-氮杂环卡宾NHC是重要的有机.md',
 '04-课件/学生讲义/3-物理化学/酸碱理论-超级充实版（自学完整）.md',
 '04-课件/学生讲义/_综合/真题模拟拆解-超级充实版（自学完整）.md',
]
for p in FILES:
    if not os.path.isfile(p):
        print('MISS %s' % p[:60]); continue
    t = io.open(p, encoding='utf-8-sig').read()
    print('◆ %s' % p[:70])
    for m in BLOCK.finditer(t):
        for pos in stray_positions(m.group(1)):
            print('   [块] …%s…' % m.group(1)[max(0, pos - 70):pos + 40].replace('\n', '⏎'))
    for m in INLINE.finditer(t):
        for pos in stray_positions(m.group(1)):
            print('   [行内] …%s…' % m.group(1)[max(0, pos - 55):pos + 35])
