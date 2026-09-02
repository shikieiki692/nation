#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检验 pack 能否从「所在目录 / exam_stage / source」推导出来。
能推导 → 新题入库可自动赋 pack，不必人工标；不能推导 → 只能写准入规则让人遵守。
只读不写。
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
Q_DIRS = ("04-题库", "05-真题库")
FIELD = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:")


def clean(v: str) -> str:
    return v.strip().strip('"').strip("'")


def main() -> None:
    pack_dir: dict[str, Counter] = defaultdict(Counter)
    pack_stage: dict[str, Counter] = defaultdict(Counter)
    pack_src: dict[str, Counter] = defaultdict(Counter)
    n = 0

    for d in Q_DIRS:
        for p in sorted((VAULT / d).rglob("*.md")):
            try:
                with open(p, "r", encoding="utf-8", newline="") as f:
                    lines = f.read().split("\n")
            except (OSError, UnicodeDecodeError):
                continue
            if not lines or lines[0].strip() != "---":
                continue
            end = None
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    end = i
                    break
            if end is None:
                continue
            fm: dict[str, str] = {}
            for line in lines[1:end]:
                m = FIELD.match(line)
                if m:
                    fm[m.group(1)] = line.split(":", 1)[1].strip().rstrip("\r")
            if clean(fm.get("type", "")) not in ("题目", "真题"):
                continue
            n += 1
            pk = clean(fm.get("pack", "")) or "(空)"
            rel = p.relative_to(VAULT / d).as_posix()
            top = rel.split("/")[0]
            second = "/".join(rel.split("/")[:2])
            pack_dir[pk][second] += 1
            pack_stage[pk][clean(fm.get("exam_stage", "")) or "(空)"] += 1
            pack_src[pk][clean(fm.get("source", ""))[:18]] += 1

    print(f"题目 {n} 条\n")

    def show(title: str, data: dict[str, Counter], limit: int = 6, indent: str = "     ") -> None:
        print(f"=== {title} ===")
        for pk in sorted(data, key=lambda x: -sum(data[x].values())):
            tot = sum(data[pk].values())
            print(f"  {pk}  (共 {tot})")
            for k, v in data[pk].most_common(limit):
                print(f"{indent}{v:>6} {k}")
        print()

    show("pack × 所在目录（二级）", pack_dir)
    show("pack × exam_stage", pack_stage)
    show("pack × source（前 6）", pack_src)


if __name__ == "__main__":
    main()
