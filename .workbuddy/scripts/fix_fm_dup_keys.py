#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全库 frontmatter 重复键修复（fix_kp_dup.py 的推广版）。

背景：104 条真题 knowledge_points 重复键已修；推广扫描又发现 115 文件（03-知识点
~110 + Atkins 习题母文件 3 + 归档任务卡 2）。这些文件是「真实头部 + 后续批量追加
模板段」结构，后值常是模板空壳 —— **机械保留最后一次会丢真实数据**，须按语义选值。

规则（只处理 frontmatter 顶格键；嵌套结构不碰）：
  · 各次出现值全同        → 保留第一处，删其余
  · 有空值也有非空值      → 保留非空值中最后一个，删其余（模板壳让位给真实数据）
  · 全非空且不同：
      - 日期字段（updated/last_updated/created/date）→ 取字典序最大（最新）
      - 数值字段（image_count 等 _count）            → 取数值最大
      - 其他（清单/内容类）                          → 取最长（信息量最大）
      - 仍存疑 → 跳过并列入人工清单（不写盘）
  · 选中值写回该键第一次出现的位置；严格保留各非删除行原行尾；读写 newline=""
安全：dry-run 默认；--write 前自动 zip 快照；修复后请跑 validate_kb --changed 与 --full。
"""
from __future__ import annotations

import argparse
import re
import zipfile
from datetime import datetime
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
SCAN_DIRS = ("03-知识点", "04-题库", "05-真题库", "00-首页", "11-模板")

KEY_PAT = re.compile(r"^([A-Za-z_][\w\-]*)\s*:(?P<v>.*)$")
DATE_FIELDS = {"updated", "last_updated", "created", "date"}
NUM_FIELDS = {"image_count"}


def fm_end_idx(lines: list[str]) -> int | None:
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i
    return None


def choose_value(field: str, vals: list[str]) -> str | None:
    """从多次出现的值中选出应保留的那个；无法判定返回 None。"""
    if len(set(vals)) == 1:
        return vals[0]
    nonempty = [v for v in vals if v.strip()]
    if not nonempty:
        return vals[0]
    if len(nonempty) == 1:
        return nonempty[0]
    if field in DATE_FIELDS:
        return max(nonempty)
    if field in NUM_FIELDS or field.endswith("_count"):
        return max(nonempty, key=lambda v: float(v) if re.fullmatch(r"\d+(\.\d+)?", v.strip()) else -1)
    return max(nonempty, key=len)  # 内容/清单类：取信息量最大的


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="实写（默认 dry-run）")
    args = ap.parse_args()

    plan: list[tuple[Path, list[int], dict[int, str]]] = []  # (path, 删除行, {行: 替换值})
    manual: list[tuple[Path, str]] = []
    n_scanned = 0
    for d in SCAN_DIRS:
        for p in (VAULT / d).rglob("*.md"):
            try:
                with open(p, "r", encoding="utf-8", newline="") as f:
                    text = f.read()
            except OSError:
                continue
            lines = text.split("\n")
            fe = fm_end_idx(lines)
            if fe is None:
                continue
            n_scanned += 1
            keys: dict[str, list[int]] = {}
            for i in range(1, fe):
                m = KEY_PAT.match(lines[i])
                if m and (not lines[i] or lines[i][0] not in " \t-"):
                    keys.setdefault(m.group(1), []).append(i)
            drops: list[int] = []
            repl: dict[int, str] = {}
            for field, idxs in keys.items():
                if len(idxs) < 2:
                    continue
                vals = [KEY_PAT.match(lines[i]).group("v") for i in idxs]
                keep_v = choose_value(field, vals)
                if keep_v is None:
                    manual.append((p, field))
                    continue
                first = idxs[0]
                # 行尾保持第一处的风格
                if KEY_PAT.match(lines[first]).group("v") != keep_v:
                    eol = "\r" if lines[first].endswith("\r") else ""
                    repl[first] = f"{field}:{keep_v}".rstrip("\r") + eol
                drops.extend(idxs[1:])
            if drops or repl:
                plan.append((p, drops, repl))

    cat_same = sum(1 for _, d, r in plan if not r)
    cat_fix = sum(1 for _, d, r in plan if r)
    print(f"扫描 {n_scanned} 文件 ｜ 需处理 {len(plan)}（同值/空壳 {cat_same}，含改值 {cat_fix}）"
          f" ｜ 人工过目 {len(manual)}")
    for p, field in manual:
        print(f"  !! 人工：{p.relative_to(VAULT).as_posix()}  「{field}」")

    if args.write and plan:
        snap = VAULT / ".workbuddy" / "backups" / \
            f"fix_fm_dup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        snap.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(snap, "w", zipfile.ZIP_DEFLATED) as z:
            for p, _, _ in plan:
                z.write(p, p.relative_to(VAULT).as_posix())
        print(f"快照 → {snap.relative_to(VAULT).as_posix()}（{len(plan)} 文件）")

    n_ok = 0
    for p, drops, repl in plan:
        rel = p.relative_to(VAULT).as_posix()
        if not args.write:
            print(f"  {rel}: 删 {len(drops)} 行" + (f"，改值 {len(repl)} 行" if repl else ""))
            continue
        lines = open(p, "r", encoding="utf-8", newline="").read().split("\n")
        for i, v in repl.items():
            lines[i] = v
        for i in sorted(drops, reverse=True):
            del lines[i]
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write("\n".join(lines))
        n_ok += 1

    print(f"{'已实写' if args.write else 'DRY-RUN'}：{n_ok or len(plan)} / {len(plan)}")
    if args.write and plan:
        print("下一步：validate_kb --changed（文件清单见 git status）→ --full 回归。")


if __name__ == "__main__":
    main()
