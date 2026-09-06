# -*- coding: utf-8 -*-
"""三模块结构评估用：目录 × teaching_level × difficulty 交叉分布（只读）。"""
import sys
import re
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\Obsidion\妙妙屋")
SCAN_DIRS = [ROOT / "04-题库", ROOT / "05-真题库"]

TL_ORDER = ["基础", "巩固", "拓展", "竞赛"]


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
            val = ln.split(":", 1)[1].strip().strip('"').strip("'")
            if val not in ("", "[]", "{}", "null", "~"):
                return val
            j = idx + 1
            while j < len(lines) and re.match(r"^\s*-\s+\S", lines[j]):
                return lines[j].strip().lstrip("- ").strip()
            return None
    return None


def first_int(s):
    if not s:
        return None
    m = re.search(r"\d+", str(s))
    return int(m.group()) if m else None


# 目录 × teaching_level
cross_tl = defaultdict(Counter)
cross_diff = defaultdict(Counter)
dir_total = Counter()
tl_total = Counter()
diff_tl = defaultdict(Counter)

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
        parts = rel.parts[:-1]
        bucket = "/".join(parts[:2]) if len(parts) >= 2 else (parts[0] if parts else "(根)")
        tl = field_value(fm, "teaching_level") or "(缺)"
        diff = field_value(fm, "difficulty")
        di = first_int(diff)
        dcell = str(di) if di is not None else "(缺)"
        cross_tl[bucket][tl] += 1
        cross_diff[bucket][dcell] += 1
        dir_total[bucket] += 1
        tl_total[tl] += 1
        diff_tl[tl][dcell] += 1

print("=== 目录（前两级）× teaching_level ===")
all_tl = TL_ORDER + ["(缺)"]
header = "目录".ljust(30) + "".join(x.rjust(6) for x in all_tl) + "合计".rjust(7)
print(header)
for bucket, cnt in sorted(cross_tl.items(), key=lambda kv: -kv[1]["__total__"] if "__total__" in kv[1] else -sum(kv[1].values())):
    row = bucket.ljust(30)
    for tl in all_tl:
        row += str(cnt.get(tl, 0)).rjust(6)
    row += str(sum(cnt.values())).rjust(7)
    print(row)
print("\n=== teaching_level 全库分布 ===")
for tl in all_tl:
    print(f"  {tl}: {tl_total.get(tl, 0)}")

print("\n=== teaching_level × difficulty(首整数) ===")
diffs = sorted({d for c in diff_tl.values() for d in c if d != "(缺)"}, key=lambda x: int(x))
header2 = "层级".ljust(10) + "".join(d.rjust(5) for d in diffs) + "(缺)".rjust(6)
print(header2)
for tl in all_tl:
    if tl_total.get(tl, 0) == 0:
        continue
    row = tl.ljust(10)
    for d in diffs:
        row += str(diff_tl[tl].get(d, 0)).rjust(5)
    row += str(diff_tl[tl].get("(缺)", 0)).rjust(6)
    print(row)

print("\n=== 各目录 difficulty 均值参考 ===")
for bucket, cnt in sorted(cross_diff.items(), key=lambda kv: -sum(kv[1].values()))[:15]:
    tot = sum(cnt.values())
    s = sum(int(d) * c for d, c in cnt.items() if d != "(缺)")
    valid = sum(c for d, c in cnt.items() if d != "(缺)")
    avg = s / valid if valid else 0
    top = ", ".join(f"{d}:{c}" for d, c in cnt.most_common(5))
    print(f"  {bucket} (n={tot}, 均值{avg:.1f}): {top}")
