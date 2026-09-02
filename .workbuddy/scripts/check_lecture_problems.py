#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
讲义 ↔ 题库 双向映射校验（problems 字段）

依据 00-首页/讲义生产SOP与双向映射规范.md：
  §四  - 新讲义必填 problems，存量不强制回填（下次大修时补齐）
  §五  - problems 列出本讲全部引用题号；定稿时回填题目侧 used_in
  §五.补充口径 - 无「题-xxxx」题号的题目暂允许用全路径链接
  §六  - 通过标准：validate 0 error；warning 可带入定稿但须在定稿前清零

严重度设计（对应「新讲义强制 + 历史不动」）：
  ERROR  新讲义（created >= NEW_SINCE）problems 缺失 / 为空 / 指向不存在的题目
  WARN   历史讲义的 problems 不可解析 —— 已知欠账，不阻塞

为什么按 created 切而不是 stage：规范 §六 第 5 步是「定稿时回填 problems」，
若按 stage=published 强制，当前 84 份已定稿的历史讲义会一次性变红，与「历史不动」冲突。
按 created 切则当前新讲义为 0、脚本绿灯，规则只对未来生效。

接受四种写法（现状三种并存 + 规范允许的例外）：
  "[[04-题库/xxx/题-0123]]"          全路径 wikilink
  "[[题-0123]]" / "[[题-0123|1]]"     wikilink（可带别名）
  "题-0123"                          纯文本题号（04-课件/学生讲义 现用写法）
  "06-33"                            章节号（规范补充口径允许）

链接解析一律复用 validate_kb.find_wikilink_target（三级兜底：
路径 → basename → title/aliases），禁止自写正则重写解析。

已知欠账（2026-09-02 实测，不阻塞）：
  38/148 条目不可解析。其中 7 条是编号多一层（题-039-1-1-X vs 实际 题-039-1-X，
  降一级即可修）；31 条讲义写的是讲次内部自造编号（如「37届Q5-NO与H2S反应」），
  与题库文件名无关，需人工对应或等拆题规范落地。另有 1 条是没填的模板占位符「题-NNN」。

用法：
    python check_lecture_problems.py                  # 全量
    python check_lecture_problems.py --dir 04-课件     # 指定目录（可多次）
    python check_lecture_problems.py --since 2026-06-01  # 放宽新讲义口径
    python check_lecture_problems.py --list-unresolved  # 列出不可解析明细
    python check_lecture_problems.py --strict          # WARN 也算失败
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VAULT / "11-模板" / "scripts"))
import validate_kb as V  # noqa: E402  —— 复用其 find_wikilink_target

# 讲义类文件（课件/备课大纲不算，不强制引用题目）
LECTURE_TYPES = {"学生讲义", "讲义", "新授课讲义"}
SCAN_DIRS = ["04-课件", "高考化学/04-讲义", "06-学生侧材料"]
EXCLUDE_NAMES = {"README.md", "模板", "索引"}

# 规则生效日：此后创建的讲义强制 problems 合规。
NEW_SINCE = "2026-09-02"

WIKI = re.compile(r"\[\[([^\]|#]+)")


def read_lines(p: Path) -> list[str]:
    with open(p, "r", encoding="utf-8", newline="") as f:
        return f.read().split("\n")


def fm_range(lines: list[str]):
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i
    return None


def parse_fm(lines: list[str], fm_end: int) -> dict:
    """粗解析：够用即可（problems 是列表，需特殊处理续行 - ）"""
    out: dict = {}
    key = None
    for line in lines[1:fm_end]:
        s = line.rstrip("\r")
        if s[:1] in (" ", "\t"):
            if key and s.strip().startswith("- "):
                # `problems:` 后为空值时 out[key] 是 str，需先转列表
                if not isinstance(out.get(key), list):
                    out[key] = [out[key]] if out.get(key) else []
                out[key].append(s.strip()[2:].strip().strip('"').strip("'"))
            continue
        if ":" in s:
            k, _, v = s.partition(":")
            key = k.strip()
            v = v.strip()
            if v.startswith("["):
                out[key] = []
                inner = v[1:].rstrip("]").strip()
                if inner:
                    out[key].append(inner.strip('"').strip("'"))
            else:
                out[key] = v.strip('"').strip("'")
    return out


def normalize(entry: str) -> str:
    """四种写法 -> 可解析的目标串"""
    e = entry.strip().strip('"').strip("'")
    m = WIKI.search(e)
    if m:                       # wikilink（可能带别名/锚点）
        return m.group(1).strip()
    e = e.split("|")[0].strip().split("#")[0].strip()
    if e.lower().endswith(".md"):
        e = e[:-3]
    return e


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", action="append", help="只扫指定目录（可多次）")
    ap.add_argument("--since", default=NEW_SINCE,
                    help=f"新讲义口径：created >= 此日期则强制合规（默认 {NEW_SINCE}）")
    ap.add_argument("--strict", action="store_true", help="WARN 也算失败")
    ap.add_argument("--list-unresolved", action="store_true")
    args = ap.parse_args()

    dirs = args.dir or SCAN_DIRS
    since = args.since

    errors: list[tuple[str, str]] = []
    warns: list[tuple[str, str]] = []
    unresolved_detail: list[tuple[str, str]] = []
    n_new = n_old = 0
    n_with = n_without = 0
    n_entries = n_ok = n_bad = 0

    for d in dirs:
        base = VAULT / d
        if not base.exists():
            print(f"跳过不存在的目录: {d}")
            continue
        for p in sorted(base.rglob("*.md")):
            if p.name in EXCLUDE_NAMES or p.name.startswith("."):
                continue
            lines = read_lines(p)
            fm_end = fm_range(lines)
            if fm_end is None:
                continue
            fm = parse_fm(lines, fm_end)
            if fm.get("type", "").strip() not in LECTURE_TYPES:
                continue

            rel = p.relative_to(VAULT).as_posix()
            created = str(fm.get("created", "")).strip()
            is_new = bool(created) and created >= since
            if is_new:
                n_new += 1
            else:
                n_old += 1

            problems = fm.get("problems")
            if isinstance(problems, str):
                problems = [problems] if problems.strip() else []

            if not problems:
                n_without += 1
                if is_new:
                    errors.append((rel, f"新讲义（created={created}）缺 problems 或为空"))
                continue
            n_with += 1

            bad: list[str] = []
            for e in problems:
                if not str(e).strip():
                    continue
                n_entries += 1
                tgt = normalize(str(e))
                if not tgt:
                    continue
                if V.find_wikilink_target(tgt, V.VAULT_ROOT) is None:
                    bad.append(tgt)
                    n_bad += 1
                    unresolved_detail.append((rel, tgt))
                else:
                    n_ok += 1

            if bad:
                msg = (f"problems 指向不存在的题目 {len(bad)} 条: "
                       + ", ".join(bad[:3]) + ("…" if len(bad) > 3 else ""))
                if is_new:
                    errors.append((rel, msg))
                else:
                    warns.append((rel, msg))

    print(f"讲义类文件: {n_new + n_old}（type in {LECTURE_TYPES}）")
    print(f"  新讲义（created >= {since}）: {n_new}")
    print(f"  历史讲义                    : {n_old}")
    print(f"  有 problems: {n_with}    无/空: {n_without}")
    print(f"problems 条目: {n_entries}   可解析: {n_ok}   不可解析: {n_bad}")
    print("─" * 74)
    print(f"ERROR {len(errors)}   WARN {len(warns)}")

    if errors:
        print("\n=== ERROR（新讲义不合规，必须修）===")
        for rel, msg in errors[:25]:
            print(f"  ✗ {rel}\n      {msg}")
        if len(errors) > 25:
            print(f"  …另有 {len(errors) - 25} 条")

    if warns:
        print(f"\n=== WARN（历史讲义欠账，不阻塞）===")
        for rel, msg in warns[:25]:
            print(f"  ! {rel}\n      {msg}")
        if len(warns) > 25:
            print(f"  …另有 {len(warns) - 25} 条")

    if args.list_unresolved:
        print(f"\n=== 不可解析条目明细（{len(unresolved_detail)} 条）===")
        for rel, tgt in unresolved_detail:
            print(f"  {tgt}\n      <- {rel}")

    rc = 1 if errors or (args.strict and warns) else 0
    if rc:
        print("\n判定：不通过")
    else:
        tail = f"（{len(warns)} 条历史欠账未清，--strict 可使其失败）" if warns else ""
        print(f"\n判定：通过{tail}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
