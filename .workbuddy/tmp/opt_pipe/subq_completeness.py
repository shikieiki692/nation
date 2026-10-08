# -*- coding: utf-8 -*-
"""subq_completeness.py —— 检查每张卡的「题面/答案」小问号分布，
快速识别「题面被截断（小问号只在答案区）」或「答案缺小问」的卡。"""
import os
import re
import sys
import glob

Q = r"04-题库/2026机构初赛模拟题"
LAB = re.compile(r"(?m)^[ \t>]*\**\s*(\d{1,2})\s*-\s*(\d{1,2})(?:\s*-\s*(\d{1,2}))?")


def labels(txt):
    out = []
    for m in LAB.finditer(txt):
        a, b, c = m.group(1), m.group(2), m.group(3)
        out.append(f"{a}-{b}" + (f"-{c}" if c else ""))
    return out


def top(labs):
    return sorted({l.split("-")[1] for l in labs}, key=lambda x: int(x))


def analyze(path):
    t = open(path, encoding="utf-8-sig").read()
    qi = t.find("## 题目")
    ai = t.find("## 参考答案")
    if qi < 0 or ai < 0:
        return None
    q = t[qi:ai]
    a = t[ai:]
    ql, al = labels(q), labels(a)
    return ql, al, q, a


cards = []
for f in glob.glob(os.path.join(Q, "**", "题-*.md"), recursive=True):
    cards.append(f)

if len(sys.argv) > 1:
    names = set(sys.argv[1:])
    cards = [c for c in cards if os.path.basename(c) in names]

for f in sorted(cards):
    r = analyze(f)
    if r is None:
        continue
    ql, al, q, a = r
    qt, at = top(ql), top(al)
    missing = [x for x in at if x not in qt]
    if missing:
        b = os.path.basename(f)
        print(f"⚠️  {b[:56]}")
        print(f"      题面小问={qt}  答案小问={at}  答案有而题面无={missing}")
