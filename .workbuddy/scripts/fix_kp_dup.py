#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复 frontmatter 重复键：`knowledge_points:` 连写两次（一次空值 + 一次 block list）。

背景（2026-09-02 勘察发现）：04-题库/真题/ 下 104 条题目文件 frontmatter 形如
    knowledge_points:
    knowledge_points:
      - "[[氧化还原反应方程式配平]]"
PyYAML 后值覆盖所以 validate_kb 不报错，但 js-yaml（Obsidian Dataview 的解析器）
对重复键行为不定 —— 三 .base / 工作台视图里这批真题可能整条消失（Gate ①② 风险）。

规则：
  · type 白名单 {题目, 真题}
  · frontmatter 内 `knowledge_points:` 出现 ≥2 次 → 保留最后一次出现，删除之前的
  · 被删行必须无行内值（空键），否则该文件跳过并报警（防止丢数据）
  · 删行不动其他行，严格保留原行尾（本库混合行尾）
"""
from __future__ import annotations

import argparse
import re
import zipfile
from datetime import datetime
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
Q_DIRS = ("04-题库", "05-真题库")
KEY_PAT = re.compile(r"^knowledge_points\s*:(?P<v>.*)$")


def read_raw(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def fm_range(lines: list[str]) -> int | None:
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i
    return None


def fm_scalar(fl: list[str], field: str) -> str:
    pat = re.compile(rf"^{re.escape(field)}\s*:\s*(.*)$")
    val = ""
    for ln in fl:
        m = pat.match(ln)
        if m:
            val = m.group(1).strip()
    return val


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="实写（默认 dry-run）")
    args = ap.parse_args()

    targets: list[tuple[Path, list[int], list[int]]] = []  # (path, 删除行下标, 同键行下标)
    n_q = 0
    for d in Q_DIRS:
        for p in (VAULT / d).rglob("*.md"):
            try:
                text = read_raw(p)
            except OSError:
                continue
            lines = text.split("\n")
            fm_end = fm_range(lines)
            if fm_end is None:
                continue
            fl = lines[1:fm_end]
            if fm_scalar(fl, "type") not in ("题目", "真题"):
                continue
            n_q += 1
            hits = [i for i, ln in enumerate(fl) if KEY_PAT.match(ln)]
            if len(hits) < 2:
                continue
            # 保留最后一个；之前的必须都是空键
            keep = hits[-1]
            drop = []
            for i in hits[:-1]:
                if KEY_PAT.match(lines[1 + i]).group("v").strip():
                    print(f"!! 跳过（被删行有内容，需人工看）：{p.relative_to(VAULT).as_posix()}")
                    drop = []
                    break
                drop.append(1 + i)  # lines 里的真实下标
            if drop:
                targets.append((p, drop, hits))

    print(f"题目/真题 {n_q} ｜ 含重复 knowledge_points 键：{len(targets)}")
    n_fix = 0
    if args.write and targets:
        snap = VAULT / ".workbuddy" / "backups" / \
            f"fix_kp_dup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        snap.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(snap, "w", zipfile.ZIP_DEFLATED) as z:
            for p, _, _ in targets:
                z.write(p, p.relative_to(VAULT).as_posix())
        print(f"快照 → {snap.relative_to(VAULT).as_posix()}（{len(targets)} 文件）")

    for p, drop, hits in targets:
        rel = p.relative_to(VAULT).as_posix()
        if not args.write:
            print(f"  将删 {len(drop)} 行（保留最后一个键，行 {1 + hits[-1] + 1}）：{rel}")
            n_fix += 1
            continue
        lines = read_raw(p).split("\n")
        for i in sorted(drop, reverse=True):
            del lines[i]
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write("\n".join(lines))
        n_fix += 1
        print(f"  ✓ 已修：{rel}")

    print(f"{'已实写' if args.write else 'DRY-RUN'}：{n_fix} / {len(targets)}")
    if args.write and n_fix:
        print("下一步：python .workbuddy/scripts/validate_kb.py --changed <文件列表> 后再 --full 回归。")


if __name__ == "__main__":
    main()
