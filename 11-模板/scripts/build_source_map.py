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

# 注：此处第三列原为 out_rel（重组前的 `习题书-教师版/…` 路径），自始**未被使用**，
# 且 2026-09-19 目录重组后已成过期路径 → 2026-09-21 移除，避免误导。
MODULES = [
    ("化学原理", B.CHEM_MAP, None),
    ("有机化学", B.ORGANIC_MAP, B.ORGANIC_EXCLUDE),
    ("元素与分析", B.YSFX_MAP, None),
    ("结构化学", B.STRUCTURE_MAP, None),
]

# 章内排序**必须与 build_module_book 一致**，否则 rows 里的 book_num 与成书实际编号不对应。
# （2026-09-07 起成书章内分层：基础巩固 d≤3 在前、竞赛提升 d4~d5 在后；层内 fidelity 优先、难度次之。）
FID_RANK = {"原书逐字": 0, "原书改写": 1, "自编": 2}

rows = []
n_catchall = 0
for module, cmap, exclude in MODULES:
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
            # 与 build_module_book 一致：未命中章节映射的题归入末章「99-综合题」
            # （2026-09-17 用户拍板）。⚠️ 旧版此处是 `continue`——会**静默丢题**，
            # 以致映射题数少于成书（实测 4,182 vs 4,279，差 97 题）。
            res = B.CATCHALL_CHAPTER
            n_catchall += 1
        groups.setdefault(res, []).append(item)
    groups = dict(sorted(groups.items(), key=lambda x: x[0][0]))
    for key in groups:
        groups[key].sort(key=lambda x: (0 if x["difficulty"] <= 3 else 1,
                                        FID_RANK.get(x.get("fidelity", ""), 9), x["difficulty"]))
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
print(f"溯源映射已生成: {out}（{len(rows)} 题；其中未命中章节映射、归入「99-综合题」{n_catchall} 题）")

# 统计按篇
from collections import Counter
c = Counter(r["module"] for r in rows)
print("按篇:", dict(c))
