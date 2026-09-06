#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
找出「knowledge_points 被写成空列表」的文件并还原到 git 已提交基线。

背景：split_kp_concepts.py 首版在「某题知识点全部解析不出」时写了
knowledge_points: []，违反本库既定约定（fix_kb_phase2_apply.py:215
「knowledge_points 不允许为空」、audit_question_bank.py:344 空列表判 P1）。
该逻辑已修正，本脚本用于清理首版写入的残留。

用法：
  python restore_empty_kp.py            # 只列出，不还原
  python restore_empty_kp.py --restore  # 执行 git checkout 还原
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
sys.path.insert(0, str(VAULT / "11-模板" / "scripts"))
import validate_kb as V  # noqa: E402

TARGET_DIRS = ["04-题库", "05-真题库"]


def main() -> None:
    restore = "--restore" in sys.argv

    # 注意：本机 subprocess 调用 git 取不到中文路径的改动列表（返回空），
    # 因此改为直接全量扫描目标目录，不依赖 git。
    changed: list[str] = []
    for d in TARGET_DIRS:
        for p in sorted((VAULT / d).rglob("*.md")):
            changed.append(p.relative_to(VAULT).as_posix())

    hits: list[str] = []
    for rel in changed:
        p = VAULT / rel
        if not p.exists():
            continue
        fm, _ = V.parse_frontmatter_from_file(p)
        kp = fm.get("knowledge_points")
        if isinstance(kp, list) and len(kp) == 0:
            hits.append(rel)

    print(f"git 中改动的 {TARGET_DIRS} md 文件：{len(changed)}")
    print(f"其中 knowledge_points 为空列表：{len(hits)}")
    for h in hits:
        print("  ", h)

    if not hits:
        return

    lst = VAULT / ".workbuddy" / "backups" / "kp_empty_list_files.txt"
    lst.parent.mkdir(parents=True, exist_ok=True)
    lst.write_text("\n".join(hits), encoding="utf-8")
    print(f"\n清单已写入 {lst.relative_to(VAULT).as_posix()}")

    if not restore:
        print("\n这是预览模式，加 --restore 才会执行 git checkout 还原。")
        return

    res = subprocess.run(
        ["git", "checkout", "--"] + hits,
        cwd=VAULT, capture_output=True, text=True, encoding="utf-8",
    )
    print("\ngit checkout 返回码:", res.returncode)
    if res.stdout.strip():
        print(res.stdout.strip()[:2000])
    if res.stderr.strip():
        print("[stderr]", res.stderr.strip()[:2000])


if __name__ == "__main__":
    main()
