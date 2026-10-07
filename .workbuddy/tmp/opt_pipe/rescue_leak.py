#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rescue_leak.py —— 救「题面泄露」卡：源卡题面区混入了答案 ⇒ 在第一个评分标注处截断，
截下的部分**搬入答案区**（题面只留题干）。

判据（2026-10-07）：题面中**第一处**答案特征（`（N 分）`/`(共N分)`/`解：`/`答：`）即答案起点；
先跳过 `### 第N题（XX分）` 标题行（其分值是题干自带，不算泄露）。
"""
import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
_orig = list(sys.argv)
sys.argv = ["x", "--vol", "R", "--all-years"]
import build_org as BO

LIM = int(_orig[_orig.index("--limit") + 1]) if "--limit" in _orig else 5
ONLY = _orig[_orig.index("--only") + 1] if "--only" in _orig else None
apply = "--apply" in _orig
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/leak_backup")
os.makedirs(BK, exist_ok=True)

# 答案起点特征（评分标注 / 解法提示）
ANS_START = re.compile(r"[（(]\s*(?:共\s*)?\d+(?:\.\d+)?\s*分[）)]|(?:解|答)\s*[:：]|【答案】|参考解答")

rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "题面泄露"]
if ONLY:
    rows = [r for r in rows if ONLY in r["path"]]
print("题面泄露卡 %d 张（处理前 %d）\n" % (len(rows), LIM))
n_done = 0
for r in rows:
    if n_done >= LIM:
        break
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    i = t.find("## 题目"); j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    if not (0 <= i < j < k):
        print("  跳过（结构异常）", os.path.basename(p)[:44]); continue
    qraw = t[i:j]
    # ★ 直接在**原始题面文本**上定位（等长替换标题行，偏移与 qraw 一致）
    qchk = re.sub(r"^#{2,4}[ \t]*第[ \t]*\d+[ \t]*题[^\n]*$",
                  lambda mm: " " * len(mm.group(0)), qraw, flags=re.M)
    m = ANS_START.search(qchk)
    if not m:
        print("  ⚠ 未找到答案起点：", os.path.basename(p)[:44]); continue
    cut = m.start()
    # 往前退到「句子/公式块边界」，避免把式子截半
    back = qraw.rfind("$$", 0, cut)
    dot = max(qraw.rfind("。", 0, cut), qraw.rfind("\n", 0, cut))
    cand = [x for x in (back + 2 if back >= 0 else None, dot + 1 if dot >= 0 else None) if x and x > 0]
    if cand and max(cand) > len(qraw) * 0.15:
        cut = max(cand)
    q_keep = qraw[:cut].rstrip()      # ★ qraw 已含 "## 题目"，勿重复添加
    q_move = qraw[cut:].strip()
    print("═" * 92)
    print("%s" % os.path.basename(p)[:58])
    print("   题面 %d 字 → 保留 %d ＋ 搬走 %d（起点：%s）" % (
        len(qraw), len(q_keep), len(q_move), re.sub(r"\s+", "", m.group(0))[:12]))
    print("   截断处原文：…%s…" % re.sub(r"\s+", " ", qraw[max(0, cut - 60):cut + 60]))
    if apply and q_move:
        newt = (t[:i] + q_keep + "\n\n## 参考答案\n\n"
                + q_move + "\n\n> ⛔ 校勘（2026-10-07）：源卡**题面区混入解答**（原题面 %d 字），"
                "已按「答案起点」截断，混入部分**移入本答案区**；截断判据＝首个评分标注/「解：」。\n\n"
                % len(qraw) + t[j + len("## 参考答案"):])
        bfp = os.path.join(BK, os.path.basename(p) + ".orig")
        if not os.path.exists(bfp):
            open(bfp, "w", encoding="utf-8", newline="\n").write(t)
        open(p, "w", encoding="utf-8", newline="\n").write(newt)
        print("   ✔ 已写入")
    n_done += 1
print("\n%s" % ("已写入" if apply else "（dry-run）"))
