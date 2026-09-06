# -*- coding: utf-8 -*-
"""快速盘点题库当前状态（只读，不改任何文件）。

口径：04-题库 + 05-真题库，frontmatter type ∈ {题目, 真题} 才计入题目总数；
其余 type 只做分布展示。行尾无关紧要，全部按文本读。
"""
import sys
import re
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\Obsidion\妙妙屋")
SCAN_DIRS = [ROOT / "04-题库", ROOT / "05-真题库"]

FIELDS = [
    "question_type", "year", "concepts", "knowledge_points",
    "difficulty", "exam_stage", "used_in",
    "source_subject", "subject_module", "teaching_level",
]


def fm_text(text):
    """frontmatter 判定：split 后找第二个 ---，兼容 CRLF（\r 会被 strip 掉）。"""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return None


def field_value(fm, key):
    """返回字段首个值（标量或 YAML 列表首项），无值/缺失返回 None。"""
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


type_counter = Counter()
status_counter = Counter()
field_cov = {k: 0 for k in FIELDS}
total = 0
used_in_vals = Counter()
scanned = 0

for d in SCAN_DIRS:
    if not d.exists():
        continue
    for p in d.rglob("*.md"):
        scanned += 1
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        fm = fm_text(t)
        if fm is None:
            continue
        m = re.search(r"^type:\s*(.+?)\s*$", fm, re.M)
        if not m:
            continue
        typ = m.group(1).strip()
        type_counter[typ] += 1
        if typ not in ("题目", "真题"):
            continue
        total += 1
        st = field_value(fm, "status")
        status_counter[st or "(缺失)"] += 1
        for k in FIELDS:
            if field_value(fm, k) is not None:
                field_cov[k] += 1
        u = field_value(fm, "used_in")
        if u:
            for part in re.findall(r"\[\[([^\]|#]+)", u):
                used_in_vals[part.strip()] += 1

print("=== 文件扫描量 ===")
print(f"  扫描 md 文件: {scanned}")

print("\n=== type 分布（含非题目文件）===")
for k, c in type_counter.most_common():
    print(f"  {k}: {c}")

print(f"\n=== 题目+真题 总数: {total} ===")

print("\n=== status 分布 ===")
for k, c in status_counter.most_common():
    print(f"  {k}: {c}")
covered = sum(status_counter.values()) - status_counter.get("(缺失)", 0)
print(f"  (status 覆盖 {covered}/{total})")

print("\n=== 字段覆盖（题目+真题口径）===")
for k in FIELDS:
    pct = field_cov[k] / total * 100 if total else 0
    print(f"  {k}: {field_cov[k]} ({pct:.1f}%)")

print("\n=== used_in 指向 TOP10 ===")
for k, c in used_in_vals.most_common(10):
    print(f"  {k}: {c} 题")
print(f"  (used_in 非空题数: {sum(used_in_vals.values())})")
