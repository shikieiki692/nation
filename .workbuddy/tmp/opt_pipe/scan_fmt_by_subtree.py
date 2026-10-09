# -*- coding: utf-8 -*-
"""按 04-题库 一级子树统计化学式排版残留，定位「本轮未覆盖」的范围。"""
import re, os, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
ROOT = os.path.join(R, "04-题库")
RX = {
    "dual": re.compile(r"[A-Za-z][0-9]*[ \t]*\$[_^]\{[^{}]*\}[_^]\{[^{}]*\}\$"),
    "single": re.compile(r"[A-Za-z][A-Za-z0-9]*[ \t]*\$[_^]\{[^{}]*\}\$"),
    "space$": re.compile(r"[A-Za-z0-9][ \t]+\$[_^]\{"),
    "empty": re.compile(r"[}\w\)\]][ \t]*\{\}[ \t]*[\^_]"),
}
agg = collections.defaultdict(collections.Counter)
for dp, dn, fn in os.walk(ROOT):
    if "images" in dp:
        continue
    for f in fn:
        if not f.endswith(".md"):
            continue
        rel = os.path.relpath(os.path.join(dp, f), ROOT)
        top = rel.split(os.sep)[0] if os.sep in rel else "(根级 md)"
        if top == "2026机构初赛模拟题":
            top = "2026机构初赛模拟题（本轮已覆盖）"
        try:
            t = open(os.path.join(dp, f), encoding="utf-8-sig").read()
        except Exception:
            continue
        for k, rx in RX.items():
            n = len(rx.findall(t))
            if n:
                agg[top][k] += n
print("%-34s %6s %6s %6s %6s" % ("子树", "dual", "single", "space$", "empty"))
for top, c in sorted(agg.items(), key=lambda x: -sum(x[1].values())):
    print("%-34s %6d %6d %6d %6d" % (top, c["dual"], c["single"], c["space$"], c["empty"]))
