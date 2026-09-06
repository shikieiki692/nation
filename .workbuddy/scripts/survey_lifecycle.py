#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
B4 生命周期治理摸底：只统计 04-题库 / 05-真题库 里 type ∈ {题目, 真题} 的文件。

产出四件事：
  1. 字段覆盖率表 —— 找「僵尸字段」（只在极少数文件上出现，既不能筛选也不该强求）
  2. pack 分布 + pack 与 subject_module / exam_stage 的交叉（定准入规则的依据）
  3. status 分布 + status 与 fidelity 的交叉（定收敛规则的依据）
  4. 讲义类文件的 problems 字段覆盖（讲义 ↔ 题库映射的现状）

只读不写。
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
Q_DIRS = ("04-题库", "05-真题库")
Q_TYPES = ("题目", "真题")

FIELD = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:")


def read_lines(p: Path) -> list[str]:
    with open(p, "r", encoding="utf-8", newline="") as f:
        return f.read().split("\n")


def fm_rows(lines: list[str]) -> tuple[dict[str, str], int]:
    """返回 {字段: 原始值}。frontmatter 结束行下标由调用方另算。"""
    if not lines or lines[0].strip() != "---":
        return {}, 0
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, 0
    out: dict[str, str] = {}
    for line in lines[1:end]:
        m = FIELD.match(line)
        if m:
            out[m.group(1)] = line.split(":", 1)[1].strip().rstrip("\r")
    return out, end


def clean(v: str) -> str:
    return v.strip().strip('"').strip("'")


def main() -> None:
    total = 0
    field_cnt: Counter[str] = Counter()
    pack_cnt: Counter[str] = Counter()
    status_cnt: Counter[str] = Counter()
    cross_pack_mod: dict[str, Counter] = defaultdict(Counter)
    cross_status_fid: dict[str, Counter] = defaultdict(Counter)
    no_pack, no_status = [], []

    for d in Q_DIRS:
        for p in sorted((VAULT / d).rglob("*.md")):
            try:
                lines = read_lines(p)
            except (OSError, UnicodeDecodeError):
                continue
            fm, end = fm_rows(lines)
            if not fm or clean(fm.get("type", "")) not in Q_TYPES:
                continue
            total += 1
            for k in fm:
                field_cnt[k] += 1
            rel = p.relative_to(VAULT).as_posix()

            pk = clean(fm.get("pack", ""))
            st = clean(fm.get("status", ""))
            if pk:
                pack_cnt[pk] += 1
            else:
                no_pack.append(rel)
            if st:
                status_cnt[st] += 1
            else:
                no_status.append(rel)

            cross_pack_mod[pk or "(空)"][clean(fm.get("subject_module", "")) or "(空)"] += 1
            cross_status_fid[st or "(空)"][clean(fm.get("fidelity", "")) or "(空)"] += 1

    print(f"题目文件总数：{total}\n")

    print("=== 一、字段覆盖率（僵尸字段排查）===")
    print(f"{'字段':<22}{'有值':>7}{'占比':>8}")
    for k, n in field_cnt.most_common():
        pct = n / total * 100
        flag = ""
        if pct < 1:
            flag = "  ← 僵尸(<1%)"
        elif pct < 10:
            flag = "  ← 稀疏(<10%)"
        elif pct < 50:
            flag = "  ← 半覆盖"
        print(f"{k:<22}{n:>7}{pct:>7.1f}%{flag}")

    print(f"\n无 pack：{len(no_pack)} ｜ 无 status：{len(no_status)}")
    for r in (no_pack + no_status)[:5]:
        print(f"    {r}")

    print("\n=== 二、pack 分布 ===")
    for k, n in pack_cnt.most_common():
        print(f"  {n:>6}  {k}")

    print("\n=== 二b、pack × subject_module 交叉（准入规则依据）===")
    mods = sorted({m for c in cross_pack_mod.values() for m in c})
    print(f"{'pack':<14}" + "".join(f"{m[:6]:>9}" for m in mods))
    for pk in sorted(cross_pack_mod, key=lambda x: -sum(cross_pack_mod[x].values())):
        row = "".join(f"{cross_pack_mod[pk].get(m, 0):>9}" for m in mods)
        print(f"{pk:<14}{row}")

    print("\n=== 三、status 分布 ===")
    for k, n in status_cnt.most_common():
        print(f"  {n:>6}  {k}")

    print("\n=== 三b、status × fidelity 交叉 ===")
    fids = sorted({f for c in cross_status_fid.values() for f in c})
    print(f"{'status':<14}" + "".join(f"{f[:6]:>9}" for f in fids))
    for st in sorted(cross_status_fid, key=lambda x: -sum(cross_status_fid[x].values())):
        row = "".join(f"{cross_status_fid[st].get(f, 0):>9}" for f in fids)
        print(f"{st:<14}{row}")

    # ── 讲义 ↔ 题库映射现状 ──
    print("\n=== 四、讲义类文件的 problems 字段覆盖 ===")
    lect_types = ("讲义", "学生讲义", "课件", "备课大纲")
    by_type: dict[str, list[tuple[str, bool, bool]]] = defaultdict(list)
    for p in VAULT.rglob("*.md"):
        parts = p.relative_to(VAULT).parts
        if parts[0] in (".git", "09-审计报告", "06-外部资料导入", "媒体仓库"):
            continue
        try:
            lines = read_lines(p)
        except (OSError, UnicodeDecodeError):
            continue
        fm, _ = fm_rows(lines)
        if not fm:
            continue
        t = clean(fm.get("type", ""))
        if t in lect_types:
            by_type[t].append((
                p.relative_to(VAULT).as_posix(),
                "problems" in fm,
                "question_ids" in fm or "题库" in fm,
            ))
    for t in lect_types:
        rows = by_type.get(t, [])
        if not rows:
            continue
        has = sum(1 for _, a, _ in rows if a)
        print(f"  {t:<10} 共 {len(rows):>4} 个 ｜ 有 problems 字段 {has:>4} ({has/len(rows)*100:.1f}%)")
        for r, a, _ in rows[:3]:
            print(f"      {'✓' if a else '✗'} {r}")


if __name__ == "__main__":
    main()
