"""生成器回归测试：严格过滤、表格保留、docx 数学宏兼容。

用法:
    python -X utf8 11-模板/scripts/test_exercise_book_generator.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    builder = load("build_module_book", "build_module_book.py")
    docx = load("build_all_handout_docx", "build-all-handout-docx.py")

    builder.STRICT = True
    q = """## 题目
题干正文保留，含图片 ![[abc.jpg]]

## 小问关联
不应进入成书

## 参考答案
解析正文保留，含图片 ![[def.jpg]]
"""
    q_part, a_part = q.split("## 参考答案")
    q_clean = builder.strip_teaching_blocks(q_part)
    a_clean = builder.strip_teaching_blocks("## 参考答案" + a_part)
    assert "小问关联" not in q_clean
    assert "abc.jpg" in q_clean
    assert "参考答案" in a_clean and "def.jpg" in a_clean

    table = "| A | B |\n|---|---|\n| 1 | 2 |\n"
    out_table = builder.strip_teaching_blocks("## 题目\n" + table)
    assert "| A | B |" in out_table and "| 1 | 2 |" in out_table

    math = (
        r"$A \xlongequal{点燃} B$，$C = 12\,\mathrm{\AA}$，"
        r"$\Biggl(\frac{1}{2}\Biggr)$，$E \xrightarrow{1.\\2.} F$"
    )
    out = docx._preprocess_markdown(math)
    assert "\\xrightarrow" in out and "\\xlongequal" not in out
    assert "\\text{Å}" in out
    assert "Biggl" not in out
    assert "1.; 2." in out

    print("ALL_TESTS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
