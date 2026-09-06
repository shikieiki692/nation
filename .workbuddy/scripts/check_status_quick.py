# -*- coding: utf-8 -*-
"""题库状态快查：type/status/question_type/year/concepts 覆盖统计。
口径：04-题库 + 05-真题库，题目类白名单 {题目, 真题}。"""
import re
from pathlib import Path
from collections import Counter

root = Path(r"C:\Obsidion\妙妙屋")
QB_TYPES = {"题目", "真题"}

def fm_lines(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return []
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return []

def fm_get(fm, key):
    pat = re.compile(r"^" + key + r":\s*(.*)$")
    for i, ln in enumerate(fm):
        m = pat.match(ln)
        if m:
            v = m.group(1).strip().strip("'\"")
            if v:
                return v
            for nxt in fm[i + 1:]:
                s = nxt.strip()
                if s.startswith("- "):
                    return "(list)"
                if s:
                    break
            return None
    return None

type_c = Counter()
st_c = Counter()          # 题目类 status
type_nonq = Counter()     # 非题目类文件 type 分布
qb_total = 0
qt_have = 0
qt_c = Counter()
year_have = 0
concepts_have = 0
no_type = 0
no_fm = 0
total_md = 0

for d in ("04-题库", "05-真题库"):
    for p in (root / d).rglob("*.md"):
        total_md += 1
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = fm_lines(text)
        t = fm_get(fm, "type")
        if t is None:
            if fm:
                no_type += 1
            else:
                no_fm += 1
            continue
        if t in QB_TYPES:
            qb_total += 1
            s = fm_get(fm, "status")
            st_c[s or "(无status)"] += 1
            qt = fm_get(fm, "question_type")
            if qt:
                qt_have += 1
                qt_c[qt] += 1
            if fm_get(fm, "year"):
                year_have += 1
            if fm_get(fm, "concepts"):
                concepts_have += 1
        else:
            type_nonq[t] += 1

pct = qt_have / qb_total * 100 if qb_total else 0
print(f"扫描 md 总数: {total_md}")
print(f"题目类总数 (题目+真题): {qb_total}")
print(f"非题目类文件数: {total_md - qb_total - no_type - no_fm}, 无type: {no_type}, 无frontmatter: {no_fm}")
print("\n== 题目类 status 分布 ==")
for k, v in st_c.most_common():
    print(f"  {k}: {v}")
print(f"\nquestion_type 有值: {qt_have} ({pct:.1f}%)  缺失: {qb_total - qt_have}")
print("question_type 值分布 top15:")
for k, v in qt_c.most_common(15):
    print(f"  {k}: {v}")
print(f"\nyear 有值: {year_have} ({year_have / qb_total * 100:.1f}%)")
print(f"concepts 有值: {concepts_have} ({concepts_have / qb_total * 100:.1f}%)")
print("\n非题目类 type 分布:")
for k, v in type_nonq.most_common():
    print(f"  {k}: {v}")
