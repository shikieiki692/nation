#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
对比 04-题库（type: 题目）与 05-真题库（type: 真题）的字段覆盖同构性

目的：判断能否安全地把 05-真题库 并进 02-数据库/题库.base。
若 05-真题库 缺 pack/difficulty/exam_stage 等分组字段，并进去只会多一堆空行。
"""
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
EXCLUDE = {"README.md", "题库架构总览.md", "新题入库SOP.md",
           "题库格式速查.md", "题库审计清单.md"}
KEY_FIELDS = ["pack", "difficulty", "exam_stage", "teaching_level",
              "question_type", "subject_module", "submodule",
              "knowledge_points", "source", "status", "used_in", "fidelity"]


def read_frontmatter(path: Path):
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            lines = f.read().split("\n")
    except Exception:
        return None
    if not lines or lines[0].strip() != "---":
        return None
    fields = {}
    for i in range(1, len(lines)):
        s = lines[i]
        if s.strip() == "---":
            return fields
        if s and not s[:1].isspace() and ":" in s:
            k, _, v = s.partition(":")
            fields[k.strip()] = v.strip().strip('"').strip("'")
    return None


def collect(tree: str, want_type: str):
    base = ROOT / tree
    out = []
    for p in base.rglob("*.md"):
        if p.name in EXCLUDE:
            continue
        fm = read_frontmatter(p)
        if fm is None:
            continue
        if fm.get("type", "").strip() != want_type:
            continue
        out.append(fm)
    return out


def main():
    a = collect("04-题库", "题目")
    b = collect("05-真题库", "真题")
    print(f"04-题库 type:题目  = {len(a)}")
    print(f"05-真题库 type:真题 = {len(b)}\n")
    print(f"{'字段':<18}{'04-题库':>12}{'05-真题库':>12}   判定")
    print("-" * 62)
    for k in KEY_FIELDS:
        ca = sum(1 for f in a if f.get(k, "").strip())
        cb = sum(1 for f in b if f.get(k, "").strip())
        pa = ca / len(a) * 100 if a else 0
        pb = cb / len(b) * 100 if b else 0
        if pb == 0 and pa > 50:
            verdict = "严重缺失，并入会大片空"
        elif abs(pa - pb) > 40:
            verdict = "覆盖差距大"
        else:
            verdict = "可用"
        print(f"{k:<18}{pa:>11.1f}%{pb:>11.1f}%   {verdict}")

    print("\n=== 05-真题库 特有/高频字段（04-题库少见）===")
    cnt_b, cnt_a = Counter(), Counter()
    for f in b:
        cnt_b.update(f.keys())
    for f in a:
        cnt_a.update(f.keys())
    for k, n in cnt_b.most_common():
        ra = cnt_a.get(k, 0) / len(a) * 100 if a else 0
        rb = n / len(b) * 100 if b else 0
        if rb > 30 and ra < 20:
            print(f"  {k:<20} 真题库 {rb:>5.1f}%  vs  题库 {ra:>5.1f}%")

    print("\n=== 05-真题库 的 status 取值 ===")
    for k, n in Counter(f.get("status", "").strip() or "(缺失)" for f in b).most_common():
        print(f"  {k:<14} {n}")


if __name__ == "__main__":
    main()
