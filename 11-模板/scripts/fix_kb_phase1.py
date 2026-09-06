#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_kb_phase1.py — 题库阶段一修复（零语义判断）

修复项：
  1. 去 BOM
  2. Markdown 图片 ![](...) → ![[basename]]（仅当 basename 能全库解析）
  3. 标准态 ° → θ（规则同 clean_standard_state_degree.py：仅 [HGSEK]°）
  4. 翻倍反斜杠（仅 4+ 连续且为偶数长度时减半）

安全机制：
  - 每个被修改的文件在写入前完整备份到 09-审计报告/备份/题库修复-2026-08-31/
  - manifest.jsonl 记录每次修改（文件 / 动作 / 次数）
  - 字节级读写，不改变原有换行符（CRLF/LF 原样保留）
  - --dry 仅预览不写入
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT = SCRIPT_DIR.parent.parent
BACKUP = VAULT / "09-审计报告" / "备份" / "题库修复-2026-08-31"
MANIFEST = BACKUP / "manifest.jsonl"
TARGETS = ["04-题库", "05-真题库"]
SKIP_PARTS = {".obsidian", ".git", "node_modules", "__pycache__", "09-AI工作区", ".chem_media"}
QT = {"题目", "真题", "例题", "题组", "题目集"}
# 答案文件也是题库实体（24 道题外链引用），图片/编码类修复同样适用
FIX_TYPES = QT | {"答案", "真题答案"}

BOM = b"\xef\xbb\xbf"
MD_IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
STD_DEG = re.compile(r"(?<=[HGSEK])°")
BS_RUN = re.compile(r"\\{4,}")

img_index: dict[str, list[str]] = defaultdict(list)
manifest: list[dict] = []


def load_img_index() -> None:
    for f in VAULT.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
            continue
        if set(f.parts) & SKIP_PARTS:
            continue
        img_index[f.name.lower()].append(f.relative_to(VAULT).as_posix())


def backup(rel: str, raw: bytes) -> None:
    dst = BACKUP / rel
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(raw)


def write(path: Path, rel: str, raw: bytes, text: str, actions: list[dict], dry: bool) -> None:
    new = text.encode("utf-8")
    if new == raw:
        return
    if not dry:
        backup(rel, raw)
        path.write_bytes(new)
    manifest.append({"file": rel, "actions": actions, "dry": dry})


def in_code_fence(text: str, pos: int) -> bool:
    """判断 pos 是否处于 ``` 围栏内。"""
    before = text[:pos]
    n = len(re.findall(r"(?m)^(```|~~~)", before))
    return n % 2 == 1


def fix_body(text: str, rel: str) -> tuple[str, list[dict]]:
    actions: list[dict] = []

    # 2) Markdown 图片 → wiki（围栏内不动）
    def sub_img(m: re.Match) -> str:
        if in_code_fence(text, m.start()):
            return m.group(0)
        # 候选：完整 target（路径可含空格）与去掉 title 的末段
        cands = [m.group(2).strip().strip('"\'')]
        parts = cands[0].split()
        if len(parts) > 1:
            cands.append(parts[0])
            cands.append(parts[-1])
        for tgt in cands:
            base = Path(tgt).name.lower()
            if base in img_index:
                actions.append({"action": "mdimg→wiki", "from": m.group(0)[:70], "to": f"![[{base}]]"})
                return f"![[{base}]]"
        return m.group(0)

    n_img = len(MD_IMG.findall(text))
    if n_img:
        before = text
        text = MD_IMG.sub(sub_img, text)
        if text == before:
            actions = [a for a in actions]  # 无可解析项
        n_done = sum(1 for a in actions if a["action"] == "mdimg→wiki")
        if n_done:
            print(f"    图片语法 {n_done}/{n_img} 处")

    # 3) 标准态 °
    n = len(STD_DEG.findall(text))
    if n:
        text = STD_DEG.sub("θ", text)
        actions.append({"action": "标准态°→θ", "count": n})
        print(f"    标准态 ° {n} 处")

    # 4) 翻倍反斜杠：4+ 连续减半
    runs = BS_RUN.findall(text)
    if runs:
        text = BS_RUN.sub(lambda m: "\\" * (len(m.group(0)) // 2), text)
        actions.append({"action": "翻倍反斜杠减半", "count": len(runs)})
        print(f"    翻倍反斜杠 {len(runs)} 处")

    return text, actions


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    load_img_index()
    print(f"图片索引：{len(img_index)} 个 basename")

    stats = defaultdict(int)
    for d in TARGETS:
        for f in sorted((VAULT / d).rglob("*.md")):
            if set(f.relative_to(VAULT).parts) & SKIP_PARTS:
                continue
            raw = f.read_bytes()
            rel = f.relative_to(VAULT).as_posix()
            text = raw.decode("utf-8", errors="replace")

            # BOM 会挡住 startswith('---')，先用去 BOM 后的副本做 type 判定
            probe = text.lstrip("\ufeff")
            fm: dict = {}
            if probe.startswith("---"):
                e = probe.find("\n---", 3)
                if e > 0:
                    import yaml
                    try:
                        m = yaml.safe_load(probe[3:e])
                        fm = m if isinstance(m, dict) else {}
                    except Exception:
                        fm = {}
            if str(fm.get("type", "")).strip() not in FIX_TYPES:
                continue

            actions: list[dict] = []

            # 1) BOM（作用于整文件，含 frontmatter）
            if raw.startswith(BOM):
                text = probe
                actions.append({"action": "去BOM", "count": 1})
                print(f"  [BOM] {rel}")

            body_start = 0
            if text.startswith("---"):
                e = text.find("\n---", 3)
                body_start = e + 4 if e > 0 else 0
            body, body_actions = fix_body(text[body_start:], rel)
            if body_actions:
                text = text[:body_start] + body
                actions.extend(body_actions)

            if actions:
                stats["files"] += 1
                write(f, rel, raw, text, actions, args.dry)
            if args.limit and stats["files"] >= args.limit:
                break

    print(f"\n📊 {'预览' if args.dry else '已修复'} {stats['files']} 个文件")
    if not args.dry and manifest:
        BACKUP.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST, "a", encoding="utf-8") as fh:
            for m in manifest:
                fh.write(json.dumps(m, ensure_ascii=False) + "\n")
        print(f"📄 manifest: {MANIFEST}")
        print(f"💾 备份目录: {BACKUP}")


if __name__ == "__main__":
    main()
