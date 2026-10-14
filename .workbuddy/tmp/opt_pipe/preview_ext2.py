# -*- coding: utf-8 -*-
r"""预览 fmt_ext2 的全部 55 处改动（只读）。"""
import os, re, sys, glob
HERE = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe"
sys.path.insert(0, HERE)
import volpost
R = r"C:\Obsidion\妙妙屋"
ROOTS = ["04-题库/真题", "04-题库/化学原理", "04-题库/有机化学"]
FSPACE = re.compile(r'(?<!\d[-.])([A-Za-z0-9])[ \t]+(\$[_^]\{)')
FBASE = next((rx, rep) for nm, rx, rep in volpost.RULES if nm == 'fbase')
RULES = [('fspace_g', FSPACE, r'\1\2'), ('fbase', FBASE[0], FBASE[1])]

files = []
for root in ROOTS:
    files += glob.glob(os.path.join(R, root, "**", "题-*.md"), recursive=True)
n = 0
for fp in sorted(set(files)):
    t = open(fp, encoding="utf-8-sig").read()
    outs = []
    for name, rx, rep in RULES:
        for m in rx.finditer(t):
            new = rep(m) if callable(rep) else m.expand(rep)
            if new == m.group(0):
                continue
            a = max(0, m.start() - 30)
            outs.append('  [%-8s] …%s… ⇒ …%s…' % (name,
                        t[a:m.start()] + m.group(0)[:34],
                        t[a:m.start()] + new[:34]))
    if outs:
        print('◆ %s' % os.path.basename(fp)[:52])
        for o in outs[:5]:
            print(o)
        n += len(outs)
print('\n合计 %d 处' % n)
