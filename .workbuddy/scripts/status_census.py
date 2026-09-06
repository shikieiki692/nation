#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
status 字段普查（只统计真正的题目文件）

背景：grep -rh '^status:' 会把文档正文里的示例（如 SOP 第 333 行
`status: deprecated`）也算进去，且不过滤非题目文件（README type: 系统）。
本脚本严格按 type 白名单过滤，只数 04-题库 + 05-真题库 下的活题。

用法：
    python status_census.py            # 打印分布
    python status_census.py --list 已入库   # 列出某个 status 的文件
"""
import sys
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[2]
SCAN_DIRS = ["04-题库", "05-真题库"]
# 注意：05-真题库 用 `type: 真题`（63 个），04-题库 用 `type: 题目`。
# 两者相加 = 4,182，与题库架构总览的口径一致。
# `type: 例题` 不被构建 gather 识别（见长期记忆），故不列入。
QB_TYPES = {"题目", "真题"}

EXCLUDE_FILE_NAMES = {
    "README.md", "题库架构总览.md", "新题入库SOP.md",
    "题库格式速查.md", "题库审计清单.md", "index.md", "索引.md",
}


def read_frontmatter(path: Path):
    """返回 (fields_dict, fm_end_line_idx)；无 frontmatter 返回 (None, -1)"""
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            lines = f.read().split("\n")
    except Exception:
        return None, -1
    if not lines or lines[0].strip() != "---":
        return None, -1
    fields = {}
    for i in range(1, len(lines)):
        s = lines[i]
        if s.strip() == "---":
            return fields, i
        # 只取顶层 key: value，不做完整 YAML 解析（够用且快）
        if s and not s[:1].isspace() and ":" in s:
            k, _, v = s.partition(":")
            fields[k.strip()] = v.strip()
    return None, -1


def main():
    want_list = None
    if "--list" in sys.argv:
        want_list = sys.argv[sys.argv.index("--list") + 1]

    counter = Counter()
    by_status = defaultdict(list)
    type_counter = Counter()
    total = 0

    for d in SCAN_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            if p.name in EXCLUDE_FILE_NAMES:
                continue
            fm, _ = read_frontmatter(p)
            if fm is None:
                continue
            t = fm.get("type", "").strip()
            type_counter[t] += 1
            if t not in QB_TYPES:
                continue
            total += 1
            st = fm.get("status", "").strip() or "(缺失)"
            counter[st] += 1
            by_status[st].append(p)

    if want_list:
        for p in sorted(by_status.get(want_list, [])):
            print(p.relative_to(ROOT).as_posix())
        print(f"\n[{want_list}] 共 {len(by_status.get(want_list, []))} 条")
        return 0

    print(f"题目类文件总数（type in {QB_TYPES}）: {total}\n")
    print("=== status 分布 ===")
    for st, n in counter.most_common():
        pct = n / total * 100 if total else 0
        print(f"  {st:<12} {n:>5}  ({pct:.2f}%)")
    print("\n=== type 分布（被过滤掉的非题目文件参考）===")
    for t, n in type_counter.most_common():
        if t not in QB_TYPES:
            print(f"  {t or '(无type)':<14} {n:>5}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
