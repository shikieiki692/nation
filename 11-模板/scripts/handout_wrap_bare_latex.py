# -*- coding: utf-8 -*-
"""给「整行是公式却漏写 $ 包裹」的行补上 `$...$`。

保守判定（三条全满足才动）：
1. 整行没有任何 `$`
2. 含 LaTeX 宏
3. 去掉 `\\text{...}` 后不含裸中文（中文进 math 会渲染异常）
4. 不是表格行、不是标题、不是引用块内的中文说明

用法:
    python -X utf8 11-模板/scripts/handout_wrap_bare_latex.py <文件名子串> [--apply]
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



MACRO = re.compile(r"\\(frac|mathrm|mathbf|Delta|delta|sqrt|times|cdot|approx|quad|"
                   r"left|right|theta|alpha|beta|gamma|rho|sigma|omega|infty|neq|"
                   r"geq|leq|vec|bar|hat|text|dfrac|tfrac|binom|sum|int|log|ln|pi|sin|cos)")
CJK = re.compile(r"[一-鿿]")
# 这些命令内部允许出现中文（\mathrm{区域}、\ce{丁二烯}、\text{库仑力}、\boxed{}）
CMD_CN = re.compile(r"\\(text|mathrm|mathbf|ce|boxed)\{[^}]*\}")


def bare_cjk(line: str) -> bool:
    return bool(CJK.search(CMD_CN.sub("", line)))


def wrappable(line: str) -> bool:
    s = line.strip()
    if not s or "$" in s:
        return False
    # 列表项/表格/标题/引用：`- ` 只有不含宏时才算列表项，负号开头的公式行（- \sum ...）要放行
    if s.startswith(("|", "#", ">", "*", "!", "```")):
        return False
    if s.startswith("- ") and not MACRO.search(s):
        return False
    if not MACRO.search(s):
        return False
    # 多行对齐环境残片（含 & 对齐符 / \\ 换行 / \begin{...}），需人工重组为 aligned 块，自动包会出错
    if "&" in s or "\\\\" in s or "\\begin{" in s or "\\end{" in s:
        return False
    return not bare_cjk(s)


def process(path: Path, apply: bool) -> int:
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.read().splitlines(keepends=True)
    out: list[str] = []
    n = 0
    in_fence = False
    in_comment = False
    for L in lines:
        # 代码围栏
        if L.strip().startswith("```"):
            in_fence = not in_fence
            out.append(L)
            continue
        # HTML 注释区
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
        body = L.rstrip("\r\n")
        eol = L[len(body):]
        if wrappable(body):
            out.append("$" + body + "$" + eol)
            n += 1
            print("L→ $%s$" % body[:110])
        else:
            out.append(L)
    if n and apply:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("".join(out))
    return n


def main() -> None:
    key = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None
    apply = "--apply" in sys.argv
    files = [p for p in sorted(iter_sources())
             if p.name != "README.md" and (key is None or key in p.name)]
    total = 0
    for p in files:
        c = process(p, apply)
        if c:
            print("---- %s：%d 行" % (p.name, c))
        total += c
    print("\n合计 %d 行；模式：%s" % (total, "APPLY" if apply else "DRY-RUN"))


if __name__ == "__main__":
    main()
