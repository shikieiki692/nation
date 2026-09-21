# -*- coding: utf-8 -*-
"""测 04-题库/组卷工作台.md §零 所需的字段底数（组卷池口径）。
组卷池 = type in {题目, 真题} 且 status != deprecated。
输出：逐字段覆盖 + 三档题量（扣已用）+ source 去重值。
"""
import io
import os
import re
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

FM = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.S)
KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")

FIELDS = ["fidelity", "difficulty", "teaching_level", "source", "subject_module",
          "pack", "exam_stage", "year", "question_type", "used_in", "depends_on",
          "source_norm", "source_grade", "source_category", "knowledge_points",
          "submodule"]

cnt = Counter()
tot = 0
srcvals = Counter()
level_all = Counter()
level_unused = Counter()

for base in ("04-题库", "05-真题库"):
    for dp, dn, fn in os.walk(base):
        for f in fn:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            t = io.open(p, encoding="utf-8", errors="replace").read()
            m = FM.match(t)
            if not m:
                continue
            d = {}
            for l in m.group(1).split("\n"):
                k = KEY.match(l.rstrip("\r"))
                if k:
                    d[k.group(1)] = k.group(2).strip()
            if d.get("status") == "deprecated":
                continue
            if d.get("type") not in ("题目", "真题"):
                continue
            tot += 1
            for fld in FIELDS:
                v = d.get(fld)
                if v is None or v == "":
                    continue
                if fld == "used_in":
                    # 两种形态：单链 "[[..]]" / YAML 列表 ["[[..]]"] / "[[..]]"
                    if v in ("[]", "''", '""'):
                        continue
                cnt[fld] += 1
            srcvals[d.get("source", "")] += 1
            lv = d.get("teaching_level", "(缺)")
            level_all[lv] += 1
            u = d.get("used_in")
            if not (u and u not in ("[]", "''", '""')):
                level_unused[lv] += 1

print("=" * 74)
print("组卷池（type ∈ {题目,真题} 且非 deprecated）= %d" % tot)
print("=" * 74)
for fld in FIELDS:
    n = cnt[fld]
    pct = n * 100.0 / tot if tot else 0
    print("  %-18s %5d  %5.1f%%" % (fld, n, pct))

print()
print("source 去重值 = %d（全池 %d 条）" % (len(srcvals), tot))
print("source 只出现 1 次的去重值 = %d" % sum(1 for v in srcvals.values() if v == 1))

print()
print("-" * 74)
print("teaching_level 三档（全池 / 扣已用）")
print("-" * 74)
for lv in ("基础", "巩固", "拓展", "竞赛", "(缺)"):
    print("  %-6s 全池 %5d   扣已用 %5d" % (lv, level_all[lv], level_unused[lv]))
print("  习题集档（基础+巩固）：全池 %d / 扣已用 %d" % (
    level_all["基础"] + level_all["巩固"], level_unused["基础"] + level_unused["巩固"]))
print("  习题书档（拓展）    ：全池 %d / 扣已用 %d" % (level_all["拓展"], level_unused["拓展"]))
print("  测试题档（竞赛）    ：全池 %d / 扣已用 %d" % (level_all["竞赛"], level_unused["竞赛"]))
