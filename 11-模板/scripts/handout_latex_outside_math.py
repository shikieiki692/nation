# -*- coding: utf-8 -*-
"""定位讲义里「数学模式外的 LaTeX 宏」（漏写 $ 包裹），只读诊断。

与导出脚本 precheck 的差别：本脚本用**原文件行号**（precheck 行号基于预处理后文本，对不上）。

用法:
    python -X utf8 11-模板/scripts/handout_latex_outside_math.py <文件名子串> [--all]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
SRC = VAULT / "04-课件" / "学生讲义"

def iter_sources():
    """递归采集讲义源（按模块分子目录后），排除 _归档 与 _ 开头的辅助目录。"""
    for p in sorted(SRC.rglob("*.md")):
        rel = p.relative_to(SRC)
        if "_归档" in rel.parts or rel.parts[0].startswith("_"):
            continue
        yield p



MACRO = re.compile(r"\\(frac|mathrm|mathbf|Delta|delta|sqrt|times|cdot|approx|quad|"
                   r"left|right|theta|alpha|beta|gamma|rho|sigma|omega|infty|neq|"
                   r"geq|leq|vec|bar|hat|text|dfrac|tfrac|binom|sum|int|log|ln)")


def math_ranges(line: str) -> list[tuple[int, int]]:
    """返回行内 $...$ 与 $$...$$ 的区间。"""
    spans: list[tuple[int, int]] = []
    i = 0
    n = len(line)
    while i < n:
        if line[i] == "$":
            if line.startswith("$$", i):
                k = line.find("$$", i + 2)
                if k < 0:
                    break
                spans.append((i, k + 2))
                i = k + 2
                continue
            k = line.find("$", i + 1)
            if k < 0:
                break
            spans.append((i, k + 1))
            i = k + 1
            continue
        i += 1
    return spans


def outside_hits(line: str) -> list[tuple[int, str]]:
    spans = math_ranges(line)
    out = []
    for m in MACRO.finditer(line):
        if any(s <= m.start() < e for s, e in spans):
            continue
        out.append((m.start(), m.group(0)))
    return out


def scan(path: Path) -> int:
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.read().splitlines()
    n = 0
    in_display = False
    in_fence = False
    for idx, L in enumerate(lines, 1):
        if L.strip().startswith("```"):
            in_fence = not in_fence
            continue
        # 跨行展示公式块 $$ ... $$ ：块内全部跳过，否则 aligned 环境内容会被误报
        if in_display:
            if L.strip() == "$$":
                in_display = False
            continue
        if L.strip() == "$$":
            in_display = True
            continue
        if in_fence:
            continue
        if "$$" in L and L.strip().startswith("$$"):
            continue  # 单行展示公式
        hits = outside_hits(L)
        if hits:
            n += 1
            macros = sorted({h[1] for h in hits})
            print("L%-5d %s" % (idx, " ".join(macros)))
            print("       %s" % L.strip()[:150])
    return n


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] != "--all":
        key = sys.argv[1]
        files = [p for p in sorted(iter_sources()) if key in p.name]
    else:
        files = sorted(iter_sources())
    total = 0
    for p in files:
        if p.name == "README.md":
            continue
        c = scan(p)
        if c:
            print("---- %s：%d 行" % (p.name, c))
        total += c
    print("\n合计 %d 行" % total)


if __name__ == "__main__":
    main()
