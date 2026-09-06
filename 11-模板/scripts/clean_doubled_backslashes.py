"""修复源文件中数学模式内整体翻倍的反斜杠（OCR 转写残留）。

FULL_FILES 是整段数学都翻倍的文件（含 C 系列结构化学综合题），可整体减半；
TARGETED_FILES 是“单反斜杠数组 + 个别命令翻倍”的混合文件，只修 `\\` 后接字母的情况。
文本与 Markdown 表格不受影响。

用法:
    python -X utf8 11-模板/scripts/clean_doubled_backslashes.py
"""

from __future__ import annotations

import re
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = VAULT_ROOT / "04-题库"

FULL_FILES = [
    "教材习题/结构化学基础/题-289-结构化学基础-综合-习题C.4.md",
    "教材习题/结构化学基础/题-293-结构化学基础-综合-习题C.8.md",
    "教材习题/结构化学基础/题-295-结构化学基础-综合-习题C.10.md",
    "教材习题/结构化学基础/题-296-结构化学基础-综合-习题C.11.md",
    "教材习题/结构化学基础/题-297-结构化学基础-综合-习题C.12.md",
    "教材习题/结构化学基础/题-298-结构化学基础-综合-习题C.13.md",
    "教材习题/结构化学基础/题-300-结构化学基础-综合-习题C.15.md",
    "教材习题/结构化学基础/题-301-结构化学基础-综合-习题C.16.md",
    "教材习题/结构化学基础/题-302-结构化学基础-综合-习题C.17.md",
    "教材习题/结构化学基础/题-303-结构化学基础-综合-习题C.18.md",
    "教材习题/结构化学基础/题-304-结构化学基础-综合-习题C.19.md",
    "教材习题/结构化学基础/题-305-结构化学基础-综合-习题C.20.md",
    "教材习题/结构化学基础/题-306-结构化学基础-综合-习题C.21.md",
    "教材习题/结构化学基础/题-307-结构化学基础-综合-习题C.22.md",
    "教材习题/结构化学基础/题-308-结构化学基础-综合-习题C.23.md",
    "教材习题/中级无机化学/题-003-中级无机化学-群论-习题1.13.md",
]

TARGETED_FILES = [
    "教材习题/汇智竞赛题目/题-汇智-分子结构-32.md",
    "化学原理/Ch08-酸碱平衡/08-07.md",
    "教材习题/上海中学竞赛课程/答案/第四讲-碱金属碱土金属-答案.md",
    "教材习题/上海中学竞赛课程/题-031-上海中学-碱金属碱土金属-习题4.md",
    "教材习题/无机化学例题与习题/Ch04-化学平衡/例题/例4.3-例43273K时水的饱和蒸气.md",
    "教材习题/无机化学例题与习题/Ch10-氧化还原反应/例题/例10.10-电势-pH图.md",
    "教材习题/结构化学基础/题-099-结构化学基础-对称性-习题4.17.md",
    "教材习题/赵鑫光/题-赵鑫光-分子-习60.md",
    "教材习题/赵鑫光/题-赵鑫光-分子-例12.md",
]

MATH_SPLIT = re.compile(
    r"(\$\$.*?\$\$|\$[^$\n]*\$|\\\(.*?\\\)|\\\[.*?\\\])",
    re.S,
)
TARGET_RE = re.compile(r"\\\\(?=[A-Za-z])")


def fix_math(text: str, targeted: bool) -> str:
    parts = MATH_SPLIT.split(text)
    for i in range(1, len(parts), 2):
        if targeted:
            parts[i] = TARGET_RE.sub(lambda m: "\\", parts[i])
        else:
            parts[i] = parts[i].replace("\\\\", "\\")
    return "".join(parts)


def main() -> int:
    changed = 0
    for rel in FULL_FILES + TARGETED_FILES:
        path = SRC_ROOT / rel
        if not path.exists():
            print(f"missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        new_text = fix_math(text, targeted=rel in TARGETED_FILES)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="")
            changed += 1
    print(f"files_changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
