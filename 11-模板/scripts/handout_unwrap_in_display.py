# -*- coding: utf-8 -*-
"""还原「展示公式块内被误加行内 $ 包裹」的行。

背景：`handout_wrap_bare_latex.py` 早期版本未识别跨行 `$$...$$` 展示块，
把块内公式行包成了 `$$` + `$公式$` + `$$`，会破坏 pandoc 渲染。本脚本把这类行还原。

判定：处于跨行 `$$` 展示块内（含 blockquote 前缀 `> ` 的形式），
且行内容以单个 `$` 开头结尾（非 `$$`）→ 去掉首尾 `$`。

用法:
    python -X utf8 11-模板/scripts/handout_unwrap_in_display.py [文件名子串] [--apply]
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



# 前缀：空白 + 若干层引用符 `> `
PREFIX = re.compile(r"^([\s>]*)")


def is_display_fence(s: str) -> bool:
    return s == "$$" or s == "> $$" or s == ">$$"


def process(path: Path, apply: bool) -> int:
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.read().splitlines(keepends=True)
    # 先按「成对」收集展示块，避免孤立的 $$ 行让状态机错乱
    bodies = [L.rstrip("\r\n") for L in lines]
    fence_idx = [i for i, b in enumerate(bodies) if is_display_fence(b.strip())]
    blocks = [(fence_idx[k], fence_idx[k + 1])
              for k in range(0, len(fence_idx) - 1, 2)]
    if len(fence_idx) % 2:
        print("  [warn] %s 有奇数个 $$ 分隔行（%d），末尾孤立行不视作块起始"
              % (path.name, len(fence_idx)))

    out: list[str] = []
    n = 0
    in_fence = False
    for i, L in enumerate(lines):
        if L.strip().startswith("```"):
            in_fence = not in_fence
            out.append(L)
            continue
        if in_fence:
            out.append(L)
            continue
        body = L.rstrip("\r\n")
        eol = L[len(body):]
        if any(s < i < e for s, e in blocks):
            m = PREFIX.match(body)
            prefix = m.group(1)
            core = body[len(prefix):].strip()
            if (core.startswith("$") and core.endswith("$")
                    and not core.startswith("$$") and len(core) > 2):
                out.append(prefix + core[1:-1] + eol)
                n += 1
                print("L→ %s" % (prefix + core[1:-1])[:110])
                continue
        out.append(L)
    if n and apply:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("".join(out))
    return n


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    key = args[0] if args else None
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
