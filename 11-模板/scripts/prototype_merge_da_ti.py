"""题目合并原型：把一道大题的多个小题归一为一道题的预览。

只生成临时预览，不改正式库。用于评估“按大题合并”后的结构。

用法:
    python -X utf8 11-模板/scripts/prototype_merge_da_ti.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "04-题库/真题/第27届初赛/无机和结构化学"
OUT = VAULT_ROOT / ".tmp-merge-pilot/27届第3题-硫脲-合并预览.md"

_spec = importlib.util.spec_from_file_location(
    "build_module_book", VAULT_ROOT / "11-模板/scripts/build_module_book.py"
)
builder = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = builder
assert _spec.loader is not None
_spec.loader.exec_module(builder)
builder.STRICT = True

FILES = [
    ("3-1", "题-027-3-1-硫脲结构式.md"),
    ("3-2", "题-027-3-2-硫脲合成方程式.md"),
    ("3-3", "题-027-3-3-异构体B结构式.md"),
    ("3-4", "题-027-3-4-硫脲溶解金离子方程式.md"),
    ("3-5", "题-027-3-5-配位原子判断.md"),
    ("3-6", "题-027-3-6-氧化偶联产物C.md"),
]


def strip_fm_and_h1(body: str) -> str:
    body = body.split("---", 2)[-1] if body.startswith("---") else body
    lines = body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith("# "):
        lines.pop(0)
    lines = [ln for ln in lines if not ln.startswith("## 题目")]
    return "\n".join(lines).strip()


def main() -> int:
    blocks = []
    for tag, fn in FILES:
        text = (SRC / fn).read_text(encoding="utf-8")
        q, a = text.split("## 参考答案", 1)
        q_body = builder.strip_teaching_blocks(strip_fm_and_h1(q))
        a_body = builder.strip_teaching_blocks(a.strip())
        blocks.append(
            f"### ({tag}) {fn.split('-', 2)[-1].replace('.md', '')}\n\n"
            f"{q_body}\n\n"
            f"<details>\n<summary>📖 查看答案</summary>\n\n{a_body}\n\n</details>\n"
        )
    doc = (
        "# 27 届初赛 · 第 3 题（硫脲）· 合并小节预览\n\n"
        "> 原型：把 6 个小问归一为一道大题。正式版会进一步去重共同题干；此处保留原小问正文以核对信息完整性。\n\n"
        "## 题目\n\n"
        + "\n".join(blocks)
        + "\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(f"merged_blocks={len(blocks)} -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
