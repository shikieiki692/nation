# -*- coding: utf-8 -*-
r"""卷内文本级缺陷扫描（只读）：① 行内重复句 ② 相邻重复行 ③ 数字粘连。"""
import os, io, re
os.chdir(r'C:\Obsidion\妙妙屋')

VOLS = ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']
SKIP = re.compile(r'^\s*(\||!\[|#{1,6}\s|>|\*\s|-\s|\d+\.\s|```|\$\$|\s*$)')

def norm(s):
    return re.sub(r'[\s$\\{}\[\]()（）]', '', s)

tot = 0
for V in VOLS:
    for tag in ['学生版', '答案版']:
        p = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        if not os.path.isfile(p):
            continue
        lines = io.open(p, encoding='utf-8-sig').read().split('\n')
        hits = []
        prev = ''
        for i, ln in enumerate(lines):
            s = ln.rstrip()
            if not s.strip() or SKIP.match(s):
                prev = ''; continue
            n = norm(s)
            # ① 行内相邻重复子串（>=12 字）
            for m in re.finditer(r'(.{12,}?)\1', n):
                hits.append(('行内重复', i + 1, (m.group(1)[:40])))
                break
            # ② 与上一非空行相同 / 互为前缀（长度>=15）
            pn = norm(prev) if prev else ''
            if pn and len(pn) >= 15 and (n == pn or n.startswith(pn) or pn.startswith(n)):
                hits.append(('相邻重复', i + 1, (n[:50])))
            prev = s
        if hits:
            tot += len(hits)
            print('=== %s %s ===' % (V, tag))
            for k, L, s in hits[:8]:
                print('   [%s] L%-4d %s' % (k, L, s))
print()
print('合计命中 %d 处' % tot)
