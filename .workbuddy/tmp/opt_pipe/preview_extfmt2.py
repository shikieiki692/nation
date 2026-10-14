# -*- coding: utf-8 -*-
r"""预览 v2：每个规则抽 3 例，印「替换前窗口 → 替换后窗口」。"""
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
seen = collections.Counter()
for fp in sorted(set(files)):
    t = open(fp, encoding="utf-8-sig").read()
    for name, rx, rep in RULES:
        if seen[name] >= 3:
            continue
        for m in rx.finditer(t):
            new = rep(m) if callable(rep) else m.expand(rep)
            if new == m.group(0):
                continue
            a, b = max(0, m.start() - 45), min(len(t), m.end() + 30)
            before = t[a:b].replace('\n', '⏎')
            t2 = t[:m.start()] + new + t[m.end():]
            after = t2[a:a + (m.end() - m.start()) + (len(new) - (m.end() - m.start())) + 75].replace('\n', '⏎')
            print('[%-7s] %s' % (name, os.path.basename(fp)[:34]))
            print('    前: …%s…' % before)
            print('    后: …%s…' % after[:len(before) + 20])
            seen[name] += 1
            break
    if all(seen[k] >= 3 for k in WANT):
        break
print()
print('抽样：', dict(seen))
