# -*- coding: utf-8 -*-
r"""预览 fmt_formula_ext 的改动样本（只读）。"""
import os, re, sys, glob, collections
HERE = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe"
sys.path.insert(0, HERE)
import volpost
R = r"C:\Obsidion\妙妙屋"
ROOTS = ["04-题库/教材习题", "04-题库/真题", "04-题库/化学原理", "04-题库/有机化学"]
WANT = ("fspace", "fbase", "fbase2", "fempty")
RULES = [(nm, rx, rep) for nm, rx, rep in volpost.RULES if nm in WANT]

files = []
for root in ROOTS:
    files += glob.glob(os.path.join(R, root, "**", "题-*.md"), recursive=True)
shown = 0
seen = collections.Counter()
for fp in sorted(set(files)):
    t = open(fp, encoding="utf-8-sig").read()
    for name, rx, rep in RULES:
        for m in rx.finditer(t):
            if seen[name] >= 3:
                continue
            new = rep(m) if callable(rep) else m.expand(rep)
            if new == m.group(0):
                continue
            seen[name] += 1
            s = max(0, m.start() - 32)
            print('[%-7s] …%s…  ⇒  …%s…' % (name,
                  t[s:m.start()] + m.group(0)[:60], new[:60]))
            shown += 1
    if shown >= 30:
        break
print()
print('各规则抽样：', dict(seen))
