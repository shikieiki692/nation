#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
校验题目文件的 `pack` 是否符合准入规则（B4，2026-09-02 从 4,182 题实测归纳）。

两级严重度 —— 这是本脚本的核心设计，别合并成一级：

【ERROR】硬规则，实测 100% 成立，违反必改：
    省预赛                → 预赛专项      （306/306）
    决赛 且 属真题        → 综合模拟卷    （214/214）

【WARN】难度默认值，实测 97.78%（4,089/4,182），仅作新题建议，违反不报错：
    其余情况：difficulty ≤ 3 → 章节练习；≥ 4 → 模块习题集

为什么难度规则只是 WARN：93 条例外散布在 43 个不同目录（最大聚集仅 10 条），
不是「整本书被编者统一归类」这种可解释的模式，而是真实噪声。
当成硬规则会逼人去改几百个没错的题。

「属真题」判定：文件在 05-真题库，或相对路径以 `真题/` 开头，或文件名以 `真题-` 开头。

用法：
    python check_pack_rule.py              # 报告（ERROR 与 WARN 分开列）
    python check_pack_rule.py --fix        # 只修 ERROR（规则唯一确定，不猜）
    python check_pack_rule.py --strict     # WARN 也算失败（接 CI 时用）
    python check_pack_rule.py --stats      # 只看分布统计
退出码：有 ERROR 返回 1；无 ERROR 时返回 0（除非 --strict 且有 WARN）。
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
Q_DIRS = ("04-题库", "05-真题库")
Q_TYPES = ("题目", "真题")

PACK_EXAM = "预赛专项"
PACK_MOCK = "综合模拟卷"
PACK_FREE = ("章节练习", "模块习题集")

FIELD = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:")


def read_lines(p: Path) -> list[str]:
    with open(p, "r", encoding="utf-8", newline="") as f:
        return f.read().split("\n")


def write_lines(p: Path, lines: list[str]) -> None:
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))


def fm_range(lines: list[str]):
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i
    return None


def clean(v: str) -> str:
    return v.strip().strip('"').strip("'")


def find_key(lines: list[str], fm_end: int, field: str):
    pat = re.compile(rf"^{re.escape(field)}\s*:")
    for i in range(1, fm_end):
        if pat.match(lines[i]):
            return i
    return None


def parse_fm(lines: list[str], fm_end: int) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in lines[1:fm_end]:
        m = FIELD.match(line)
        if m:
            out[m.group(1)] = line.split(":", 1)[1].strip().rstrip("\r")
    return out


def is_zhenti(d: str, rel: str) -> bool:
    """是否属真题：05-真题库整仓，或 04-题库 下真题/ 目录，或文件名 真题- 开头。"""
    if d == "05-真题库":
        return True
    return rel.startswith("真题/") or Path(rel).name.startswith("真题-")


def expected_pack(stage: str, zhenti: bool) -> tuple[str, ...]:
    """【硬规则】返回该条件下合法的 pack 集合。实测 100% 成立。"""
    if stage == "省预赛":
        return (PACK_EXAM,)
    if stage == "决赛" and zhenti:
        return (PACK_MOCK,)
    return PACK_FREE


def diff_num(v: str):
    m = re.search(r"\d+", str(v or ""))
    return int(m.group()) if m else None


def suggest_pack(stage: str, zhenti: bool, difficulty: str) -> str | None:
    """【软规则】硬规则没覆盖时，按难度给默认建议。实测吻合 97.78%，仅作建议。"""
    if expected_pack(stage, zhenti) != PACK_FREE:
        return None  # 硬规则已定，无需建议
    d = diff_num(difficulty)
    if d is None:
        return None
    return "章节练习" if d <= 3 else "模块习题集"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true", help="只修 ERROR（规则唯一确定）；WARN 不自动改")
    ap.add_argument("--strict", action="store_true", help="WARN 也算失败（接 CI 时用）")
    ap.add_argument("--stats", action="store_true", help="只看分布统计")
    args = ap.parse_args()

    n = 0
    bad: list[tuple[str, str, str, tuple[str, ...], str]] = []   # ERROR
    warn: list[tuple[str, str, str, str]] = []                   # WARN
    dist: Counter = Counter()
    stage_pack: Counter = Counter()

    for d in Q_DIRS:
        for p in sorted((VAULT / d).rglob("*.md")):
            try:
                lines = read_lines(p)
            except (OSError, UnicodeDecodeError):
                continue
            fm_end = fm_range(lines)
            if fm_end is None:
                continue
            fm = parse_fm(lines, fm_end)
            # type 白名单：题库目录下混着索引/系统/答案等非题目文件
            if clean(fm.get("type", "")) not in Q_TYPES:
                continue
            n += 1
            rel = p.relative_to(VAULT / d).as_posix()
            stage = clean(fm.get("exam_stage", ""))
            pack = clean(fm.get("pack", ""))
            dist[pack] += 1
            stage_pack[(stage, pack)] += 1

            exp = expected_pack(stage, is_zhenti(d, rel))
            if pack not in exp:
                bad.append((p.relative_to(VAULT).as_posix(), pack, stage, exp, d))
            else:
                sug = suggest_pack(stage, is_zhenti(d, rel), clean(fm.get("difficulty", "")))
                if sug and pack != sug:
                    warn.append((p.relative_to(VAULT).as_posix(), pack, sug,
                                 f"{stage or '(空)'} d={diff_num(clean(fm.get('difficulty','')))}"))

    if args.stats:
        print(f"题目 {n} 条\n=== pack 分布 ===")
        for k, v in dist.most_common():
            print(f"  {v:>6}  {k}")
        print("\n=== exam_stage × pack ===")
        for (s, k), v in sorted(stage_pack.items(), key=lambda x: -x[1]):
            ok = "✓" if k in expected_pack(s, True) or k in expected_pack(s, False) else "✗"
            print(f"  {ok} {v:>6}  {s or '(空)':<8} {k}")
        return

    print(f"受检题目：{n}")
    print(f"  ERROR（硬规则违反）：{len(bad)}")
    print(f"  WARN （偏离难度默认值，97.78% 吻合，不强制）：{len(warn)}")

    if bad:
        print(f"\n❌ ERROR 明细（前 20）：")
        for rel, pack, stage, exp, _ in bad[:20]:
            print(f"  {rel}")
            print(f"      exam_stage={stage or '(空)'}  pack={pack or '(空)'}  应为 {'/'.join(exp)}")
        if len(bad) > 20:
            print(f"  ...另有 {len(bad) - 20} 条")

    if warn:
        show = 8 if not args.strict else 20
        print(f"\n⚠️  WARN 明细（前 {show}，多为编者有意为之，不必改）：")
        for rel, pack, sug, ctx in warn[:show]:
            print(f"  {rel}")
            print(f"      {ctx}  pack={pack}  难度默认建议={sug}")
        if len(warn) > show:
            print(f"  ...另有 {len(warn) - show} 条")

    if not bad:
        print("\n✅ 无硬规则违反")

    if not args.fix:
        if bad:
            print("\n只报告模式，加 --fix 只修 ERROR。")
        sys.exit(1 if bad else (1 if (args.strict and warn) else 0))

    if not bad:
        print("\n没有需要修正的 ERROR。")
        sys.exit(0)

    fixed = 0
    for rel, pack, stage, exp, _ in bad:
        # 只修规则唯一确定的；二选一的情况不猜，留给人工
        if len(exp) != 1:
            continue
        p = VAULT / rel
        lines = read_lines(p)
        fm_end = fm_range(lines)
        if fm_end is None:
            continue
        idx = find_key(lines, fm_end, "pack")
        if idx is None:
            continue
        term = "\r" if lines[idx].endswith("\r") else ""
        lines[idx] = f"pack: {exp[0]}" + term
        write_lines(p, lines)
        fixed += 1
    print(f"\n已修正 {fixed}/{len(bad)} 条 ERROR（WARN 一律不自动改）。")
    sys.exit(1 if fixed < len(bad) else 0)


if __name__ == "__main__":
    main()
