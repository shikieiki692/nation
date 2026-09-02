# -*- coding: utf-8 -*-
"""缺 question_type 的题按目录分布 + 真题 year/题型覆盖（只读）。"""
import sys
import re
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\Obsidion\妙妙屋")
SCAN_DIRS = [ROOT / "04-题库", ROOT / "05-真题库"]


def fm_text(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return None


def field_value(fm, key):
    lines = fm.split("\n")
    for idx, ln in enumerate(lines):
        m = re.match(r"^([A-Za-z_][\w\-]*)\s*:", ln)
        if m and m.group(1) == key:
            val = ln.split(":", 1)[1].strip()
            if val not in ("", "[]", "{}", "null", "~"):
                return val
            j = idx + 1
            while j < len(lines) and re.match(r"^\s*-\s+\S", lines[j]):
                return lines[j].strip().lstrip("- ").strip()
            return None
    return None


missing_by_dir = Counter()
missing_total = 0
zhen_missing_year = 0
zhen_total = 0
zhen_missing_qt = 0
kong_question_type = Counter()  # 题型值为空字符串/占位的统计

for d in SCAN_DIRS:
    if not d.exists():
        continue
    for p in d.rglob("*.md"):
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        fm = fm_text(t)
        if fm is None:
            continue
        m = re.search(r"^type:\s*(.+?)\s*$", fm, re.M)
        if not m or m.group(1).strip() not in ("题目", "真题"):
            continue
        typ = m.group(1).strip()
        rel = p.relative_to(ROOT)
        # 目录取前两级
        parts = rel.parts[:-1]
        bucket = "/".join(parts[:2]) if len(parts) >= 2 else (parts[0] if parts else "(根)")
        qt = field_value(fm, "question_type")
        if qt is None:
            missing_by_dir[bucket] += 1
            missing_total += 1
            if typ == "真题":
                zhen_missing_qt += 1
        elif qt.strip() in ("", "[]", "待标", "综合题"):
            kong_question_type[qt.strip() or "(空)"] += 1
        if typ == "真题":
            zhen_total += 1
            y = field_value(fm, "year")
            if y is None:
                zhen_missing_year += 1

print("=== 缺 question_type 的题按目录（前两级）分布 ===")
for k, c in missing_by_dir.most_common():
    print(f"  {k}: {c}")
print(f"  合计缺: {missing_total}")
print(f"\n=== 真题（{zhen_total} 条）===")
print(f"  缺 year: {zhen_missing_year}")
print(f"  缺 question_type: {zhen_missing_qt}")
print("\n=== question_type 占位/特殊值 ===")
for k, c in kong_question_type.most_common():
    print(f"  {k}: {c}")
