#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""try_placeholder_fix.py —— 试算「剔除占位注记行后」的无答案判据，量化误杀面。"""
import csv, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, R + r"\.workbuddy\tmp\opt_pipe")
_orig = list(sys.argv)
sys.argv = ["x", "--vol", "TRY", "--all-years"]
import build_org as BO
X = BO.X

rows = [r for r in csv.DictReader(open(R + "/09-审计报告/2026-10-07-不可组卷题目清单.csv", encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]

NOTE = re.compile(r"^\s*(?:[>]+\s*)*(?:📎|⛔)|答案出处[：:]|[（(]源 ?PDF|未逐字校对|文字层自动提取|文字化需人工转录")
keep, drop = [], []
for r in rows:
    p = R + "/" + r["path"]
    t = open(p, encoding="utf-8", errors="replace").read()
    try:
        c = X.extract(p)
    except Exception:
        continue
    rawq, rawa = c["question"], c["answer"]
    body = []
    for ln in rawa.split("\n"):
        s = ln.strip()
        if not s:
            continue
        if NOTE.search(s):                 # 剔除注记行
            continue
        body.append(s)
    real = re.sub(r"\s+", "", "".join(body))
    has_img = ("![" in rawa)
    if len(real) < 25 and not has_img:
        keep.append(r["path"])             # 仍判无答案（真缺）
    else:
        drop.append((r["path"], len(real), len(rawa), has_img))

print("原判「无答案/占位」 %d 张" % len(rows))
print("  修正后仍判无答案（真缺）: %d 张" % len(keep))
print("  ★ 修正后应入池（原误杀）: %d 张" % len(drop))
print()
for p, real, raw, img in drop[:20]:
    print("   %-52s 实质%5d / 原%5d 图=%s" % (p.split("/")[-1][:52], real, raw, img))
