# -*- coding: utf-8 -*-
"""生成习题书"成书题 ↔ 题库源文件"双向溯源映射（只读源库，不重建成书）。
复用 build_module_book 的 gather/merge/classify 逻辑，输出 JSON：
  [{module, chapter, num, title, source, fid, exam, path}]
题库源文件被修改后，可据此清单核对成书是否需重建。"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, '11-模板/scripts')
import build_module_book as B

VAULT = Path(__file__).resolve().parents[2]  # scripts → 11-模板 → 仓库根

MODULES = [
    ("化学原理", "习题书-教师版/第一篇-化学原理", B.CHEM_MAP, None),
    ("有机化学", "习题书-教师版/第三篇-有机化学", B.ORGANIC_MAP, B.ORGANIC_EXCLUDE),
    ("元素与分析", "习题书-教师版/第四篇-元素与分析", B.YSFX_MAP, None),
    ("结构化学", "习题书-教师版/第二篇-结构化学", B.STRUCTURE_MAP, None),
]

rows = []
for module, out_rel, cmap, exclude in MODULES:
    pool = [q for q in B.gather_questions(module)
            if q.get("submodule") not in (set(exclude or []))]
    _gap = [q for q in pool if B.is_gap_item(q)]
    pool = [q for q in pool if not B.is_gap_item(q)]
    if B.MERGE_DA:
        pool = B.merge_da_items(pool)
    groups = {}
    for item in pool:
        res = B.classify_by_keywords(item, cmap, module)
        if res is None:
            continue
        groups.setdefault(res, []).append(item)
    groups = dict(sorted(groups.items(), key=lambda x: x[0][0]))
    for key in groups:
        groups[key].sort(key=lambda x: x["difficulty"])
    for (num, name), items in groups.items():
        qn = 0
        for item in items:
            qn += 1
            title = B.short_title(item) or ""
            exam = B.exam_label(item) or ""
            rows.append({
                "module": module,
                "chapter_num": num,
                "chapter_name": name,
                "book_num": f"{num}.{qn}",
                "title": title,
                "source": item.get("source", "") or "",
                "fid": item.get("fidelity", "") or "",
                "exam": exam,
                "src_path": item.get("path", ""),
            })

out = VAULT / "04-课件/习题集/溯源映射.json"
out.write_text(json.dumps({
    "generated": B.TODAY,
    "total": len(rows),
    "note": "成书题 ↔ 题库源文件映射；题库源文件修改后据此核对成书是否需重建。",
    "rows": rows,
}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"溯源映射已生成: {out}（{len(rows)} 题）")

# 统计按篇
from collections import Counter
c = Counter(r["module"] for r in rows)
print("按篇:", dict(c))
