#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
B4 · status 收敛：补齐缺失的 status，给唯一缺理由的 deprecated 补 deprecation_reason。

扫描出来的三类缺口（2026-09-02 实测，4,182 题）：
  1. 30 条无 status    —— 27 条 Weller Ch21（题干完整但「原书未提供解答」，文件里写明了）
                         + 3 条例题（解析是内容的一部分）
                       统一补 `已填充`：内容已录入，且不谎称「答案已补全」
  2. 1 条 deprecated 缺废弃理由（题-061-ABOC，无取代文件是有意为之）→ 补 deprecation_reason
  3. 5 条 `待填充`     —— 经查是**部分填充**（第37届决赛大题，从第 4 小问开始，前 3 问缺），
                        状态正确，**本脚本不动**，只交给 题库.base 视图追踪

为什么不给 30 条判「已补全答案」：`已填充` 有 96.3% 带答案区、`已补全答案` 只有 77.1%，
两者与答案区**反向相关**，说明 status 无法从正文推导。取占 80.5% 的默认值 `已填充` 最稳妥。

用法：
    python fix_status.py            # dry-run（默认）
    python fix_status.py --write    # 落盘
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

ABOC_REASON = ("自编冒充原书转录且目标分子缺失无法作答，2026-08-30 质量剔除；"
               "无取代文件，故 superseded_by 留空")


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
    """插入新行时按邻居风格补行尾（本库混合行尾）。"""
    if idx < len(lines):
        return "\r" if lines[idx].endswith("\r") else ""
    return "\r" if lines and lines[-1].endswith("\r") else ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="落盘（默认 dry-run）")
    args = ap.parse_args()

    plan_status: list[tuple[Path, str]] = []   # (文件, 插入值)
    plan_reason: list[tuple[Path, str]] = []
    skipped: list[tuple[str, str]] = []

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
            if clean(fm.get("type", "")) not in Q_TYPES:
                continue
            st = clean(fm.get("status", ""))
            rel = p.relative_to(VAULT).as_posix()

            if not st:
                plan_status.append((p, "已填充"))
            elif st == "deprecated":
                # 理由字段名有两种：deprecation_reason（规范）/ superseded_note（遗留）
                if not clean(fm.get("deprecation_reason", "")) and not clean(fm.get("superseded_note", "")):
                    plan_reason.append((p, ABOC_REASON))
                elif clean(fm.get("superseded_note", "")):
                    skipped.append((rel, "理由写在 superseded_note，由 fix_zombie_fields.py 统一"))
                else:
                    skipped.append((rel, "已有 deprecation_reason"))
            elif st == "待填充":
                skipped.append((rel, "确认是部分填充，状态正确，不动"))

    print(f"计划补 status：{len(plan_status)} 条")
    print(f"计划补 deprecation_reason：{len(plan_reason)} 条")
    print(f"跳过：{len(skipped)} 条")
    print("─" * 66)

    n_status = n_reason = n_err = 0

    for p, val in plan_status:
        rel = p.relative_to(VAULT).as_posix()
        try:
            lines = read_lines(p)
            fm_end = fm_range(lines)
            if fm_end is None:
                raise RuntimeError("frontmatter 消失")
            if find_key(lines, fm_end, "status") is not None:
                print(f"  -- 已有 status，跳过：{rel}")
                continue
            lines.insert(fm_end, f"status: {val}" + term_at(lines, fm_end))
            if args.write:
                write_lines(p, lines)
            n_status += 1
            print(f"  ✓ {rel}\n      + status: {val}")
        except Exception as e:
            n_err += 1
            print(f"  !! {rel}: {type(e).__name__}: {e}")

    for p, reason in plan_reason:
        rel = p.relative_to(VAULT).as_posix()
        try:
            lines = read_lines(p)
            fm_end = fm_range(lines)
            if fm_end is None:
                raise RuntimeError("frontmatter 消失")
            anchor = find_key(lines, fm_end, "status")
            if anchor is None:
                raise RuntimeError("找不到 status 行")
            ins = anchor + 1
            lines.insert(ins, f'deprecation_reason: "{reason}"' + term_at(lines, ins))
            if args.write:
                write_lines(p, lines)
            n_reason += 1
            print(f"  ✓ {rel}\n      + deprecation_reason: {reason[:40]}...")
        except Exception as e:
            n_err += 1
            print(f"  !! {rel}: {type(e).__name__}: {e}")

    print("─" * 66)
    print(f"补 status {n_status} ｜ 补 reason {n_reason} ｜ 异常 {n_err}")
    if skipped:
        print("\n跳过明细：")
        for rel, why in skipped[:12]:
            print(f"  -- {rel}\n      {why}")
        if len(skipped) > 12:
            print(f"  ...另有 {len(skipped) - 12} 条")
    print("已落盘。" if args.write else "这是 DRY-RUN，加 --write 才落盘。")


if __name__ == "__main__":
    main()
