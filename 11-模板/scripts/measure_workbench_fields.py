# -*- coding: utf-8 -*-
"""测 04-题库/组卷工作台.md §零 所需的字段底数（组卷池口径）。
组卷池 = type in {题目, 真题} 且 status != deprecated。
输出：逐字段覆盖 + 三档题量（扣已用）+ source 去重值。

🔴 2026-10-13 修复：原 KEY 正则只认「key: value」同行标量 ⇒ 块列表/跨行数组
（knowledge_points: 换行 - "[[X]]"）一律读空 ⇒ KP 覆盖被严重低估（同 qb_census.py
2026-10-12 已修缺陷同源）。现统一走权威解析器 11-模板/scripts/fm_parse.py。
"""
import io
import os
import re
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(_R, "11-模板", "scripts"))
import fm_parse  # noqa: E402

os.chdir(_R)

SCALAR = re.compile(r"(?m)^([A-Za-z_][A-Za-z0-9_]*)[ \t]*:[ \t]*(.*)$")


def scalar(fm, key):
    m = SCALAR.search(fm)
    # 逐键精确匹配
    m = re.search(r"(?m)^%s[ \t]*:[ \t]*(.*)$" % re.escape(key), fm)
    if not m:
        return ""
    v = m.group(1).strip().strip("'").strip('"').strip()
    return v


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
        if "_归档" in dp or "_archive" in dp:
            continue
        for f in fn:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            t = io.open(p, encoding="utf-8-sig", errors="replace").read()
            fm, _body = fm_parse.split_fm(t)
            if not fm:
                continue
            if scalar(fm, "status") == "deprecated":
                continue
            if scalar(fm, "type") not in ("题目", "真题"):
                continue
            tot += 1
            for fld in FIELDS:
                # 🔴 判非空 = 键存在 且 取值（兼容内联数组/块列表/标量三种形态）非空
                if fm_parse.has_key(fm, fld) and fm_parse.get_list_field(fm, fld):
                    cnt[fld] += 1
            srcvals[scalar(fm, "source")] += 1
            lv = scalar(fm, "teaching_level") or "(缺)"
            level_all[lv] += 1
            if not fm_parse.get_list_field(fm, "used_in"):
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
print("  习题书档（拓展）    ：全池 %d / 扣已用 %d" % (
    level_all["拓展"], level_unused["拓展"]))
print("  测试题档（竞赛）    ：全池 %d / 扣已用 %d" % (
    level_all["竞赛"], level_unused["竞赛"]))
