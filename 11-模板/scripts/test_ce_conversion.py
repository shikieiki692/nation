# -*- coding: utf-8 -*-
r"""_preprocess_ce_in_math（mhchem→LaTeX）的单测。

背景（2026-09-11 修）：
`_parse_species` 曾用 `_([^{])` 归一裸下标，遇到 `C_\beta` 会把 `\` 单独塞进花括号，
输出 `C_{\}beta` —— 无效 LaTeX，pandoc 转不成 OMML，Word 里显示源码。
本测试把「下划线/插入符后跟完整 LaTeX 命令」固化为回归用例。

运行:
    python -X utf8 11-模板/scripts/test_ce_conversion.py
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "build-all-handout-docx.py"


def _load():
    spec = importlib.util.spec_from_file_location("build_all_handout_docx", TARGET)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["build_all_handout_docx"] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    m = _load()
    conv = m._preprocess_ce_in_math

    cases = [
        # (输入, 期望输出)
        # —— 回归：希腊字母命令不得被切碎 ——
        (r"$\ce{C_\beta}$", r"$C_{\beta}$"),
        (r"$\ce{H-C_\beta-C_\alpha-X}$", r"$H-C_{\beta}-C_{\alpha}-X$"),
        (r"$\ce{B^- + H-C_\beta-C_\alpha-X <=> C_\beta^- - C_\alpha-X + BH}$",
         r"$B^{-} + H-C_{\beta}-C_{\alpha}-X \rightleftharpoons C_{\beta}^{-} - C_{\alpha}-X + BH$"),
        # —— 基础：数字下标、电荷、箭头 ——
        (r"$\ce{H2O}$", r"$H_{2}O$"),
        (r"$\ce{2H2 + O2 -> 2H2O}$", r"$2H_{2} + O_{2} \rightarrow 2H_{2}O$"),
        (r"$\ce{Fe^{3+} + 3F- <=> FeF3}$", r"$Fe^{3+} + 3F^{-} \rightleftharpoons FeF_{3}$"),
        # —— 箭头上方标注：LaTeX 命令不加 \text{}，中文要加 ——
        (r"$\ce{RO-OR ->[\Delta] 2 RO.}$", r"$RO-OR \xrightarrow{\Delta} 2 RO.$"),
        (r"$\ce{A ->[加热] B}$", r"$A \xrightarrow{\text{加热}} B$"),
        # —— 箭头标注不得二次包裹 \text{}（源里已是 \text{…}） ——
        (r"$\ce{A ->[\text{Ti(OiPr)4}] B}$", r"$A \xrightarrow{\text{Ti(OiPr)4}} B$"),
        # —— 箭头标注里的化学式应补下标/电荷 ——
        (r"$\ce{A ->[H3O+] B}$", r"$A \xrightarrow{H_{3}O^{+}} B$"),
        (r"$\ce{A ->[AlCl3] B}$", r"$A \xrightarrow{AlCl_{3}} B$"),
    ]

    failed = 0
    for src, want in cases:
        got = conv(src)
        ok = got == want
        if not ok:
            failed += 1
        print(f"[{'PASS' if ok else 'FAIL'}] {src}")
        if not ok:
            print(f"       期望: {want}")
            print(f"       实际: {got}")

    # 全局不变量：转换结果里不得出现 `{\}` 这种畸形片段
    bad = re.compile(r"\{\\\}")
    for src, _ in cases:
        if bad.search(conv(src)):
            print(f"[FAIL] 输出含畸形片段 {{\\}}: {src}")
            failed += 1

    print("-" * 60)
    print(f"用例 {len(cases)}，失败 {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
