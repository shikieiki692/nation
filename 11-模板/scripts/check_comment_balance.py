# -*- coding: utf-8 -*-
"""检查讲义 md 的 HTML 注释配对（<!-- 与 --> 计数）。

不配对会让该篇在 Obsidian 里整体空白（P0），每次改动 HTML 注释前后都必须跑。

用法:
    python -X utf8 11-模板/scripts/check_comment_balance.py
"""

from __future__ import annotations

import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "04-课件" / "学生讲义"

def iter_sources():
    """递归采集讲义源（按模块分子目录后），排除 _归档 与 _ 开头的辅助目录。"""
    for p in sorted(SRC.rglob("*.md")):
        rel = p.relative_to(SRC)
        if "_归档" in rel.parts or rel.parts[0].startswith("_"):
            continue
        yield p




def mask_fences(lines: list[str]) -> list[str]:
    """把 ``` 代码围栏内的行置空。

    Mermaid 流程图箭头 `A --> B` 含 `-->`，直接计数会误报注释不闭合。
    """
    out: list[str] = []
    in_fence = False
    for L in lines:
        if L.strip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        # 裸 mermaid：写在 blockquote 内的流程图，行如 `> A[x] -- "x" --> B(y)`
        if (L.lstrip().startswith(">") and "-->" in L
                and "--" in L.replace("-->", "")):
            out.append("")
            continue
        out.append("" if in_fence else L)
    return out


def main() -> None:
    bad = 0
    total = 0
    for p in sorted(iter_sources()):
        with open(p, encoding="utf-8", newline="") as f:
            t = f.read()
        masked = "".join(mask_fences(t.splitlines(keepends=True)))
        o, c = masked.count("<!--"), masked.count("-->")
        total += 1
        if o != c:
            bad += 1
            print("不闭合 %-52s <!-- %d / --> %d" % (p.name, o, c))
    print("受检 %d 份，不闭合 %d 份（已剥离代码围栏/mermaid 箭头）" % (total, bad))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
