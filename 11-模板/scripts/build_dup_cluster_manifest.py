"""把重复图去重分析聚类成“污染簇”并输出可留存的清单。

用法:
    python -X utf8 11-模板/scripts/build_dup_cluster_manifest.py
"""

from __future__ import annotations

import re
from collections import OrderedDict
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-重复图去重分析.csv"
OUT = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-重复图簇清单.md"


def main() -> int:
    lines = SRC.read_text(encoding="utf-8").splitlines()
    header = lines[0].lstrip("\ufeff").split(",")
    i_h = header.index("图片哈希")
    i_f = header.index("全部源文件")
    i_c = header.index("出现文件数")
    groups: OrderedDict[str, dict] = OrderedDict()
    for line in lines[1:]:
        if not line.strip():
            continue
        cols = line.split(",")
        files = sorted(
            {re.sub(r":\d+$", "", s) for s in cols[i_f].split(" | ")},
        )
        key = " | ".join(files)
        g = groups.setdefault(
            key, {"files": files, "hashes": [], "max_files": int(cols[i_c])}
        )
        g["hashes"].append(cols[i_h])

    L = [
        "---",
        "title: 2026-08-30-习题书V2-重复图簇清单",
        "type: 审计报告",
        "task_type: 习题册图片去重",
        "status: 逐簇处理中",
        "created: 2026-08-30",
        "updated: 2026-08-30",
        "---",
        "",
        "# 习题书 V2 重复图簇清单",
        "",
        "> 每个“簇”= 同一 OCR 页的同一组图被复制到该页全部题目文件。处理方法是：逐张目检图片、读题干确定归属题，再从误挂文件删除、保留归属题。",
        "",
        "| 簇 | 涉及文件数 | 图数 | 届别 | 状态 |",
        "|---|---:|---:|---|---|",
    ]
    done = "题-027-2-8-甲烷燃烧体积比"
    for i, (key, g) in enumerate(sorted(groups.items(), key=lambda kv: -len(kv[1]["files"])), 1):
        first = g["files"][0]
        year = "27届" if "第27届" in first else "26届" if "第26届" in first else (
            "25届" if "第25届" in first else ""
        )
        status = "✅ 已清理" if any(done in f for f in g["files"]) else "待处理"
        # 短名称：取第一个文件的“题-027-2-8-…”主体
        name = first.replace("真题/", "").split("/")[-1].replace(".md", "")
        L.append(f"| {i} | {len(g['files'])} | {len(g['hashes'])} | {year} | {status} |")

    L.append("")
    L.append("## 处理原则")
    L.append("")
    L.append("1. 逐簇：先视觉确认图内容，再读各文件题干匹配归属。")
    L.append("2. 只保留与该题匹配的图，其余文件删除误挂的 `![[哈希.jpg]]`，媒体文件保留。")
    L.append("3. 每簇清理后重跑 `audit_exercise_book.py`，确认题数不倒退、无新缺失。")
    L.append("4. 全部簇清完后，全量重出 Word 并跑 `gate_exercise_books.py`。")
    L.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"clusters={len(groups)} -> {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
