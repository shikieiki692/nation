# -*- coding: utf-8 -*-
"""把「用反引号包公式」的行内代码转成数学模式 `$...$`。

背景：部分讲义把公式写成 `` `E^\\theta = 0.34 V` ``（行内代码），pandoc 会渲染成等宽字体的
LaTeX 源码，学生看到的是 `\\theta`、`\\frac` 这类字面量。

保守规则：只转**含 LaTeX 宏或 ^{}/_{} 上下标**的反引号片段；单独符号（如 `` `Cu²⁺` ``）不动，
避免把「代码/符号」意图误转成数学模式。

用法:
    python -X utf8 11-模板/scripts/handout_code_span_to_math.py [文件名子串] [--apply]
默认 dry-run。
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



# 参考/样板类文档：其反引号是「规范示例」（如讲 `\theta` 写法），不是待转的公式
EXCLUDE = {"讲义升级模式-原子结构样板"}

CODE = re.compile(r"`([^`\n]+)`")
MACRO = re.compile(r"\\(frac|mathrm|mathbf|text|Delta|delta|sqrt|times|cdot|approx|"
                   r"theta|alpha|beta|gamma|rho|left|right|mathrm|mathrm|quad|pi|ln|log)")
SCRIPTED = re.compile(r"\^\{|^_\{|_\{")


def conv(line: str) -> tuple[str, int]:
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        s = m.group(1)
        if "$" in s:
            return m.group(0)
        if not (MACRO.search(s) or SCRIPTED.search(s)):
            return m.group(0)
        n += 1
        return "$" + s + "$"

    return CODE.sub(repl, line), n


def process(path: Path, apply: bool) -> int:
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.read().splitlines(keepends=True)
    out: list[str] = []
    total = 0
    in_fence = False
    in_comment = False
    for L in lines:
        if L.strip().startswith("```"):
            in_fence = not in_fence
            out.append(L)
            continue
        if in_comment:
            out.append(L)
            if "-->" in L:
                in_comment = False
            continue
        if "<!--" in L:
            if "-->" not in L or L.index("-->") < L.index("<!--"):
                in_comment = True
            out.append(L)
            continue
        if in_fence:
            out.append(L)
            continue
        new, n = conv(L)
        if n:
            total += n
            print("L→ %s" % new.rstrip()[:120])
        out.append(new)
    if total and apply:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("".join(out))
    return total


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    key = args[0] if args else None
    files = [p for p in sorted(iter_sources())
             if p.name != "README.md" and p.stem not in EXCLUDE
             and (key is None or key in p.name)]
    total = 0
    for p in files:
        c = process(p, apply)
        if c:
            print("---- %s：%d 处" % (p.name, c))
        total += c
    print("\n合计 %d 处；模式：%s" % (total, "APPLY" if apply else "DRY-RUN"))


if __name__ == "__main__":
    main()
