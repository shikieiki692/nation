#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
B4 · Task #10 僵尸字段治理（第一批：废弃字段收敛）

背景：全库存在两套并存的废弃机制，且命名不一致
  A. `status: deprecated`（5 条）+ deprecation_reason/superseded_by（wikilink）
  B. `deprecated: true` + deprecatedDate + sunsetDate + supersededBy（裸路径）（3 条）
     —— status 仍是「已补全答案」，而组卷工作台只挡 `status === "deprecated"`，
        所以这 3 条虽已标记废弃，仍会被抽进卷子。

用户决策：并入 status: deprecated（一套机制，工作台不用改即自动排除）。

本脚本做四件事（全部只动 frontmatter，行级原地替换，保持各文件原有行尾）：
  1. `superseded_note`  -> `deprecation_reason`（3 条，值加引号对齐 A 的写法）
  2. `supersededBy`     -> `superseded_by`，值从裸路径转 wikilink（3 条）
  3. B 的 3 条：`status: 已补全答案` -> `deprecated`
  4. B 的 3 条：删掉 deprecated / deprecatedDate / sunsetDate，
     并把日落信息并进 deprecation_reason（不丢信息，只是从可机读变文字）

前置校验（已跑过，见 check_deprecation_targets.py）：
  - 3 个父文件的小问 100% 已独立成题（12.35-12.45 / 19.57-19.63 / 19.64+19.68-19.77）
  - 7 个 superseded_by 目标全部可解析，新增的 3 个均命中同目录

用法：
    python fix_zombie_fields.py            # dry-run
    python fix_zombie_fields.py --write    # 落盘
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
Q_DIRS = ("04-题库", "05-真题库")
Q_TYPES = ("题目", "真题")

FIELD = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:")


# ---------- 行级读写工具（沿用 fix_status.py 已验证的实现） ----------

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


def parse_fm(lines: list[str], fm_end: int) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in lines[1:fm_end]:
        m = FIELD.match(line)
        if m:
            out[m.group(1)] = line.split(":", 1)[1].strip().rstrip("\r")
    return out


def find_key(lines: list[str], fm_end: int, field: str):
    pat = re.compile(rf"^{re.escape(field)}\s*:")
    for i in range(1, fm_end):
        if pat.match(lines[i]):
            return i
    return None


def term_at(lines: list[str], idx: int) -> str:
    """插入新行时按邻居风格补行尾（本库 CRLF/LF 混合）。"""
    if idx < len(lines):
        return "\r" if lines[idx].endswith("\r") else ""
    return "\r" if lines and lines[-1].endswith("\r") else ""


# ---------- 值变换 ----------

def to_wikilink(v: str) -> str:
    """`04-题库/a/b/题目名.md` -> `"[[题目名]]"`"""
    stem = Path(clean(v)).stem
    return f'"[[{stem}]]"'


def quote(v: str) -> str:
    return f'"{clean(v)}"'


def sunset_reason(dep_date: str, sun_date: str) -> str:
    return (f"拆题后父文件，全部小问已独立成题（取代文件见 superseded_by）；"
            f"{dep_date} 标记废弃，原定 {sun_date} 日落删除")


# ---------- 计划 ----------

def build_plan():
    """返回 {Path: list[op]}，op 为 ('rename', old, new, transform) / ('set', k, v) / ('del', k)"""
    plan: dict[Path, list] = {}

    for d in Q_DIRS:
        for p in sorted((VAULT / d).rglob("*.md")):
            lines = read_lines(p)
            fm_end = fm_range(lines)
            if fm_end is None:
                continue
            fm = parse_fm(lines, fm_end)
            if clean(fm.get("type", "")) not in Q_TYPES:
                continue

            ops: list = []

            # 1) superseded_note -> deprecation_reason
            if "superseded_note" in fm:
                if "deprecation_reason" in fm:
                    print(f"  !! 撞字段（两者都有），跳过改名：{p.name}")
                else:
                    ops.append(("rename", "superseded_note", "deprecation_reason", quote))

            # 2) supersededBy -> superseded_by（值转 wikilink）
            if "supersededBy" in fm:
                if "superseded_by" in fm:
                    print(f"  !! 撞字段（两者都有），跳过改名：{p.name}")
                else:
                    ops.append(("rename", "supersededBy", "superseded_by", to_wikilink))

            # 3+4) 日落机制 -> status: deprecated
            if clean(fm.get("deprecated", "")).lower() in ("true", "yes"):
                dep_date = clean(fm.get("deprecatedDate", "")) or "(无日期)"
                sun_date = clean(fm.get("sunsetDate", "")) or "(无日期)"
                ops.append(("set", "status", "deprecated"))
                for k in ("deprecated", "deprecatedDate", "sunsetDate"):
                    if k in fm:
                        ops.append(("del", k))
                if "deprecation_reason" not in fm and "superseded_note" not in fm:
                    ops.append(("set", "deprecation_reason",
                                f'"{sunset_reason(dep_date, sun_date)}"'))

            if ops:
                plan[p] = ops
    return plan


def apply_ops(lines: list[str], ops: list) -> list[str]:
    """注意：每次改动后 fm_end 可能变化，故每个 op 都重新定位。"""
    for op in ops:
        fm_end = fm_range(lines)
        if fm_end is None:
            raise RuntimeError("frontmatter 消失")
        if op[0] == "rename":
            _, old, new, transform = op
            i = find_key(lines, fm_end, old)
            if i is None:
                continue
            val = lines[i].split(":", 1)[1]
            lines[i] = f"{new}: {transform(val)}" + ("\r" if lines[i].endswith("\r") else "")
        elif op[0] == "set":
            _, key, val = op
            i = find_key(lines, fm_end, key)
            if i is None:
                anchor = find_key(lines, fm_end, "status")
                ins = (anchor + 1) if anchor is not None else fm_end
                lines.insert(ins, f"{key}: {val}" + term_at(lines, ins))
            else:
                lines[i] = f"{key}: {val}" + ("\r" if lines[i].endswith("\r") else "")
        elif op[0] == "del":
            _, key = op
            i = find_key(lines, fm_end, key)
            if i is not None:
                del lines[i]
    return lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="落盘（默认 dry-run）")
    args = ap.parse_args()

    print("扫描并生成计划…")
    plan = build_plan()
    print(f"待改文件：{len(plan)}\n" + "─" * 74)

    n_file = n_err = 0
    for p, ops in plan.items():
        rel = p.relative_to(VAULT).as_posix()
        try:
            lines = read_lines(p)
            new = apply_ops(list(lines), ops)
            if args.write:
                write_lines(p, new)
            n_file += 1
            print(f"✓ {rel}")
            # 打印 frontmatter 层面的增删
            old_fm = parse_fm(lines, fm_range(lines))
            new_fm = parse_fm(new, fm_range(new))
            for k in old_fm:
                if k not in new_fm:
                    print(f"    - {k}: {old_fm[k][:52]}")
            for k in new_fm:
                if k not in old_fm:
                    print(f"    + {k}: {new_fm[k][:52]}")
                elif new_fm[k] != old_fm[k]:
                    print(f"    ~ {k}: {old_fm[k][:34]}  ->  {new_fm[k][:34]}")
        except Exception as e:
            n_err += 1
            print(f"!! {rel}: {type(e).__name__}: {e}")

    print("─" * 74)
    print(f"改 {n_file} 个文件 ｜ 异常 {n_err}")
    print("已落盘。" if args.write else "这是 DRY-RUN，加 --write 才落盘。")


if __name__ == "__main__":
    sys.exit(main())
