# -*- coding: utf-8 -*-
"""Step0-b：学生版 vs 答案版 的卷级分区标题对照（只读）。"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
QD = os.path.join(ROOT, "04-题库")
VOLS = ["X", "XI", "XIp", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "O1"]
H = re.compile(r"^##\s+(第[一二三四五六]部分.*)$")

def heads(path):
    if not os.path.exists(path):
        return None
    lines = open(path, "rb").read().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
    return [(i, m.group(1).strip()) for i, ln in enumerate(lines, 1) for m in [H.match(ln)] if m]

print("%-5s | %-38s | %-38s" % ("卷", "学生版", "答案版"))
print("-" * 92)
for v in VOLS:
    kind = "有机" if v == "O1" else "非有机"
    s = heads(os.path.join(QD, f"初赛模拟卷{v}（{kind}·学生版）.md"))
    a = heads(os.path.join(QD, f"初赛模拟卷{v}（{kind}·答案版）.md"))
    fs = " / ".join(t.split("（")[0] for _, t in s) if s else "(无)"
    fa = " / ".join(t.split("（")[0] for _, t in a) if a else "(无)"
    flag = "" if fs == fa else "  ⚠师/生不一致"
    print("%-5s | %-38s | %-38s%s" % (v, fs, fa, flag))
