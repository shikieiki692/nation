# -*- coding: utf-8 -*-
r"""v2：屏蔽所有 \begin{X}...\end{X} 环境后再找残存 `\\`（只读）。"""
import os, io, re
os.chdir(r'C:\Obsidion\妙妙屋')

BLOCK = re.compile(r'\$\$(.+?)\$\$', re.S)
INLINE = re.compile(r'(?<!\$)\$([^$\n]+?)\$(?!\$)')
ENV = re.compile(r'\\begin\{[a-zA-Z*]+\}.*?\\end\{[a-zA-Z*]+\}', re.S)
SUB = re.compile(r'\\substack\{.*?\}', re.S)

def strip_env(seg):
    s = ENV.sub(lambda m: ' ' * len(m.group(0)), seg)
    s = SUB.sub(lambda m: ' ' * len(m.group(0)), s)
    return s

def stray(seg):
    return len(re.findall(r'\\\\', strip_env(seg)))

hits = []
for root in ['04-题库', '04-课件', '03-知识点', '05-真题库']:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f)
            try:
                t = io.open(p, encoding='utf-8-sig').read()
            except Exception:
                continue
            nb = sum(1 for m in BLOCK.finditer(t) if stray(m.group(1)))
            ni = sum(1 for m in INLINE.finditer(t) if stray(m.group(1)))
            if nb or ni:
                hits.append((p, nb, ni))
print('命中 %d 文件（已屏蔽所有环境）' % len(hits))
tb = sum(h[1] for h in hits); ti = sum(h[2] for h in hits)
for p, nb, ni in sorted(hits, key=lambda x: -(x[1] + x[2]))[:25]:
    print('  块%-2d 行内%-2d %s' % (nb, ni, p[:76]))
print()
print('合计：$$ 块 %d ｜ 行内 $ %d' % (tb, ti))
