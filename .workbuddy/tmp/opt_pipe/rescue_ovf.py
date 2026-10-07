#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rescue_ovf.py —— 救「越界」卡：答案区尾部串入了**下一题的题干** ⇒ 在该处截断。"""
import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
_orig = list(sys.argv)
sys.argv = ["x", "--vol", "RO", "--all-years"]
import build_org as BO

LIM = int(_orig[_orig.index("--limit") + 1]) if "--limit" in _orig else 5
apply = "--apply" in _orig
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/ovf_backup")
os.makedirs(BK, exist_ok=True)

rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "越界（含他题内容）"]
print("越界卡 %d 张（处理 %d）\n" % (len(rows), LIM))
n = 0
for r in rows:
    if n >= LIM:
        break
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    i = t.find("## 题目"); j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    if not (0 <= i < j < k):
        continue
    own = BO.own_qno(t, p)
    if not own:
        print("  跳过（无题号）", os.path.basename(p)[:44]); continue
    araw = t[j:k]
    # 找答案区里第一个「第X题」(X>own) 的位置（跳过注记行）
    cut = None
    for ln_m in re.finditer(r"[^\n]*", araw):
        pass
    pos = 0
    for line in araw.split("\n"):
        s = line.strip()
        if s and not re.match(r'^(?:[>]+\s*)*(?:📎|⛔|📄)', s):
            m = re.search(r"第\s*(\d+)\s*题", line)
            if m and int(m.group(1)) > int(own):
                cut = pos + m.start()
                break
            m2 = re.match(r"^\s*(\d+)\s*[-－—]\s*\d+", line)
            if m2 and int(m2.group(1)) > int(own):
                cut = pos + m2.start()
                break
        pos += len(line) + 1
    if cut is None:
        print("  ⚠ 未定位越界点：", os.path.basename(p)[:44]); continue
    keep = araw[:cut].rstrip()
    drop = araw[cut:].strip()
    print("═" * 92)
    print("%s | own=%d | 答案 %d 字 → 留 %d 删 %d" % (os.path.basename(p)[:50], own, len(araw), len(keep), len(drop)))
    print("   截断处：…%s…" % re.sub(r"\s+", " ", araw[max(0, cut - 70):cut + 90]))
    if apply:
        newt = (t[:j] + keep + "\n\n> ⛔ 校勘（2026-10-07）：源卡答案区**尾部串入了下一题内容**（%d 字），"
                "已按题界截断；如需该题请查源卷。\n\n" % len(drop) + t[k:])
        bfp = os.path.join(BK, os.path.basename(p) + ".orig")
        if not os.path.exists(bfp):
            open(bfp, "w", encoding="utf-8", newline="\n").write(t)
        open(p, "w", encoding="utf-8", newline="\n").write(newt)
        print("   ✔ 已写入")
    n += 1
print("\n%s" % ("已写入" if apply else "（dry-run）"))
