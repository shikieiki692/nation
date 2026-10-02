# -*- coding: utf-8 -*-
"""把讲义正文里的「半截 math」改成 Unicode 上下标（复杂式改整段 math）。

半截 math = 基体字符在 `$` 外、math 内只剩上下标，如 `H$_2$O`、`Na$^+$`、`2s$^2$`。
Word 导出时基体和上下标是两个 run，极易错位；且违反库铁律「简单就 Unicode，复杂就整段 math」。

关键判定：`$` 的前一个字符必须是「基体」（数字/字母/汉字/右括号）。
`$_{57}\\mathrm{La}$` 这种 `$` 前是空格的是**合法完整 math，绝不能改**。

用法:
    python -X utf8 11-模板/scripts/handout_fix_half_math.py [--apply]
默认 dry-run。
"""

from __future__ import annotations

import re
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



TRIG = re.compile(r"[0-9A-Za-z一-鿿）\)]")

SAMPLES: list[tuple[str, str, str]] = []

SUB = {"0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅",
       "6": "₆", "7": "₇", "8": "₈", "9": "₉", "+": "₊", "-": "₋",
       "=": "₌", "(": "₍", ")": "₎", "a": "ₐ", "e": "ₑ", "h": "ₕ",
       "k": "ₖ", "l": "ₗ", "m": "ₘ", "n": "ₙ", "o": "ₒ", "p": "ₚ",
       "s": "ₛ", "t": "ₜ", "x": "ₓ"}
SUP = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵",
       "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "+": "⁺", "-": "⁻",
       "=": "⁼", "(": "⁽", ")": "⁾", "n": "ⁿ", "i": "ⁱ"}


def to_uni(script: str) -> str | None:
    """`_3^-` → `₃⁻`；无法完整转写时返回 None。"""
    out = ""
    pos = 0
    while pos < len(script):
        op = script[pos]
        pos += 1
        if op not in "_^":
            return None
        if pos < len(script) and script[pos] == "{":
            end = script.find("}", pos)
            if end < 0:
                return None
            body = script[pos + 1:end]
            pos = end + 1
        else:
            body = script[pos]
            pos += 1
        table = SUB if op == "_" else SUP
        if any(c not in table for c in body):
            return None
        out += "".join(table[c] for c in body)
    return out or None


def fix_line(line: str) -> tuple[str, int, list[tuple[str, str]]]:
    n = 0
    samples: list[tuple[str, str]] = []
    if "$$" in line:
        return line, 0, samples
    j = 0
    while j < len(line):
        if line[j] != "$":
            j += 1
            continue
        k = line.find("$", j + 1)
        if k < 0:
            break
        inner = line[j + 1:k]
        if j > 0 and TRIG.match(line[j - 1]) and inner[:1] in ("_", "^"):
            base = line[j - 1]
            uni = to_uni(inner)
            if uni is not None:
                repl = base + uni
            elif base.isalpha():
                repl = "$\\mathrm{%s%s}$" % (base, inner)
            else:
                repl = "$%s%s$" % (base, inner)
            frag = line[j - 1:k + 1]
            line = line[:j - 1] + repl + line[k + 1:]
            samples.append((frag, repl))
            j = j - 1 + len(repl)
            n += 1
            continue
        j = k + 1
    return line, n, samples


def body_start(lines: list[str]) -> int:
    """返回 frontmatter 之后的行号（无 frontmatter 则为 0）。"""
    if not lines or not lines[0].strip() == "---":
        return 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i + 1
    return 0


def process(path: Path, apply: bool) -> tuple[int, int]:
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    lines = text.splitlines(keepends=True)
    start = body_start(lines)

    out: list[str] = []
    n_fix = 0
    in_fence = False
    for idx, L in enumerate(lines):
        if idx >= start:
            if L.strip().startswith("```"):
                in_fence = not in_fence
                out.append(L)
                continue
            if not in_fence:
                new, n, samples = fix_line(L)
                n_fix += n
                for a, b in samples:
                    SAMPLES.append((path.name, a, b))
                out.append(new)
                continue
        out.append(L)

    if n_fix and apply:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("".join(out))
    return n_fix, len(lines)


def main() -> None:
    apply = "--apply" in sys.argv
    total = 0
    hit_files = 0
    for p in sorted(iter_sources()):
        if p.name == "README.md":
            continue
        n, _ = process(p, apply)
        if n:
            hit_files += 1
            total += n
            print("%-52s %4d 处" % (p.name, n))
    print("\n合计 %d 处 / %d 份；模式：%s"
          % (total, hit_files, "APPLY 已写盘" if apply else "DRY-RUN 未写盘"))
    if "--sample" in sys.argv:
        seen: set[str] = set()
        print("\n--- 替换样例（去重，最多 40 条）---")
        for name, a, b in SAMPLES:
            key = a + "|" + b
            if key in seen:
                continue
            seen.add(key)
            print("  %-30s → %s" % (a, b))
            if len(seen) >= 40:
                break


if __name__ == "__main__":
    main()
