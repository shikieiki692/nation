# -*- coding: utf-8 -*-
"""列出需要重导出的讲义 md（只读，不写盘任何讲义）。

判定：无对应 docx，或 max(docx.mtime) < md.mtime。
名称归一：剥日期前缀、剥（自学完整|课堂填空|Word清稿|完整版）等后缀、剥 " · xxx"。

同时标出「不在脚本默认筛选集（超级充实|基础版|复习|-新课）」的，这些必须显式 --path 指定。

用法:
    python -X utf8 11-模板/scripts/handout_stale_docx_report.py [输出清单文件]
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "04-课件" / "学生讲义"
# 2026-09-07 起产物统一落在这里（与 build-all-handout-docx.py 的 HANDOUT_OUT 保持一致）
DOC_DIR = VAULT_ROOT / "06-学生侧材料" / "讲义"

DEFAULT_MARKER = re.compile(r"超级充实|基础版|复习|-新课")

SKIP = {
    "分子轨道式相关真题小问总集",
    "原子结构-前置知识速查",
    "物化元素分析教材落实审计报告",
    "讲义升级模式-原子结构样板",
}


def core(name: str) -> str:
    n = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)
    n = re.sub(r"（(自学完整|课堂填空|Word清稿|学生版-无解析|完整版)）$", "", n)
    n = re.sub(r"\s*·\s*.*$", "", n)
    return n.strip()


def iter_sources():
    """递归采集讲义源（2026-09-07 起按学科模块分子目录），排除 _归档 与 _ 开头辅助目录。"""
    for p in sorted(SRC.rglob("*.md")):
        rel = p.relative_to(SRC)
        if "_归档" in rel.parts or rel.parts[0].startswith("_"):
            continue
        yield p


def main() -> None:
    docs: dict[str, float] = {}
    # ⚠️ 必须递归：2026-09-07 起产物按学科模块分子目录（化学原理/有机化学/…），
    # 用 glob("*.docx") 只能扫到顶层 → docs 恒为空 → 全部误报「无 docx」。
    for p in DOC_DIR.rglob("*.docx"):
        if p.name.startswith("~$"):
            continue
        c = core(p.stem)
        docs[c] = max(docs.get(c, 0.0), p.stat().st_mtime)

    stale: list[tuple[str, bool, str]] = []
    for p in iter_sources():
        if p.name == "README.md":
            continue
        c = core(p.stem)
        if c in SKIP:
            continue
        mt = p.stat().st_mtime
        if c in docs and docs[c] >= mt:
            continue
        need_path = not DEFAULT_MARKER.search(p.stem)
        reason = "无 docx" if c not in docs else "docx 较旧"
        stale.append((p.name, need_path, reason))

    print("需重导出 %d 份（其中 %d 份不在默认筛选集，需 --path 指定）"
          % (len(stale), sum(1 for _, np_, _ in stale if np_)))
    print()
    for name, need_path, reason in stale:
        print("%s%-46s %s" % ("[path] " if need_path else "[batch] ", name, reason))

    if len(sys.argv) > 1:
        out = Path(sys.argv[1])
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="") as f:
            f.write("\n".join(n for n, _, _ in stale) + "\n")
        print("\n清单已写入 %s" % out)


if __name__ == "__main__":
    main()
