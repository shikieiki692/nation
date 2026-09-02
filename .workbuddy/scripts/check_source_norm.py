#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证「同来源限流」的来源归一化规则。

问题：source 字段有 1,228 个去重值，其中 1,083 个只出现一次；而同一本书被
拆成多种写法（「赵鑫光《…笔记》」+「…第2章」+「…第3章」… 共 7 个来源、
416 题）。不归一化，同来源限流会形同虚设——同一本书的题会以 7 种名字各出 3 题。

本脚本用与 dataviewjs 里 srcKey() 等价的规则跑一遍全库，看归一化后
TOP 来源的规模是否合理。
"""
import re
import sys
import yaml
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"C:\Obsidion\妙妙屋") / "11-模板/scripts"))
import validate_kb as V  # noqa: E402

ROOT = Path(r"C:\Obsidion\妙妙屋")

RULES = [
    (re.compile(r"[（(]忠实转录[)）]"), ""),
    (re.compile(r"[·•]\s*第\s*\d+\s*[讲章][\s\S]*$"), ""),
    (re.compile(r"第\s*[\d一二三四五六七八九十]+\s*[章节讲篇][\s\S]*$"), ""),
    # 分册/卷号：「上海中学竞赛课程·化学·第2分册」→「上海中学竞赛课程」
    (re.compile(r"[·•]\s*第\s*[\d一二三四五六七八九十]+\s*[分册卷][\s\S]*$"), ""),
    # 末尾的「-1」「-2」分卷号：「第34届…(决赛)试题-1」→「第34届…(决赛)试题」
    (re.compile(r"-\s*\d{1,2}\s*$"), ""),
    (re.compile(r"[\s·•、,，\-—]+$"), ""),
]


def src_key(s: str) -> str:
    k = str(s or "").strip()
    for pat, rep in RULES:
        k = pat.sub(rep, k)
    return k.strip() or "(未知来源)"


def main() -> None:
    files = []
    for d in ("04-题库", "05-真题库"):
        files.extend(sorted((ROOT / d).rglob("*.md")))
    files = [p for p in files if p.name not in V.EXCLUDE_FILE_NAMES]

    raw, norm = Counter(), Counter()
    n = 0
    for p in files:
        with open(p, "r", encoding="utf-8", newline="") as f:
            t = f.read()
        lines = t.split("\n")
        if not lines or lines[0].strip() != "---":
            continue
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is None:
            continue
        try:
            fm = yaml.safe_load("\n".join(lines[1:end])) or {}
        except Exception:
            continue
        if not isinstance(fm, dict):
            continue
        if str(fm.get("type", "")).strip() not in ("题目", "真题"):
            continue
        n += 1
        s = str(fm.get("source", "")).strip()
        raw[s] += 1
        norm[src_key(s)] += 1

    print(f"题目 {n}")
    print(f"  source 原始去重 {len(raw)}  →  归一化后 {len(norm)}")
    print(f"  只出现 1 次：原始 {sum(1 for v in raw.values() if v == 1)}"
          f"  →  归一化 {sum(1 for v in norm.values() if v == 1)}")
    print(f"  最大来源规模：原始 {max(raw.values())}  →  归一化 {max(norm.values())}")
    print("\n归一化后 TOP 20：")
    for k, v in norm.most_common(20):
        print(f"  {v:5d}  {k[:56]}")

    # 抽几个典型的对照，确认没切错
    print("\n归一化对照（前 12 个原始值）：")
    for k, v in raw.most_common(12):
        print(f"  {v:4d}  {k[:52]:54s} → {src_key(k)[:38]}")


if __name__ == "__main__":
    main()
