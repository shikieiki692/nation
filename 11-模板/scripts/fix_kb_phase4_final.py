#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_kb_phase4_final.py — 收尾修复（写盘版）

修复项：
  1. 4 个模块习题集文件去 BOM
  2. ZOC-027 / 教学改编题(暂缓) 补六字段
  3. 无机化学例题与习题 的 例题 文件（type=例题）缺 fidelity/subject_module/pack 时补齐
说明：Atkins/Weller 等 type=题组 文件不套用题目六字段（schema 不同，审计已排除）。
"""

from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8")

V = Path(__file__).resolve().parents[2]
BACKUP = V / "09-审计报告" / "备份" / "题库修复-2026-08-31"
MANIFEST = BACKUP / "manifest.jsonl"
TODAY = datetime.date.today().isoformat()

CH_MAP = {
    "Ch01": "元素与分析", "Ch02": "化学原理", "Ch03": "化学原理", "Ch04": "化学原理",
    "Ch05": "结构化学", "Ch06": "结构化学", "Ch07": "结构化学", "Ch08": "化学原理",
    "Ch09": "化学原理", "Ch10": "化学原理", "Ch11": "结构化学", "Ch12": "元素与分析",
    "Ch13": "元素与分析", "Ch14": "元素与分析", "Ch15": "元素与分析", "Ch16": "元素与分析",
    "Ch17": "元素与分析", "Ch18": "元素与分析", "Ch19": "元素与分析", "Ch20": "元素与分析",
    "Ch21": "元素与分析", "Ch22": "元素与分析",
}

SPECIAL = {
    "04-题库/有机化学/周环反应/题-ZOC-027-光照条件下[2+2]环加成的立体化学.md": {
        "fidelity": "原书改写", "exam_stage": "初赛", "subject_module": "有机化学", "pack": "模块习题集",
    },
    "04-题库/教学改编题/无机和结构化学/题-改编-分子结构基础-挑战附加题（暂缓）.md": {
        "fidelity": "自编", "exam_stage": "初赛", "subject_module": "结构化学", "pack": "章节练习",
    },
}

BOM_FILES = [
    "04-题库/模块习题集-元素与分析.md", "04-题库/模块习题集-化学原理.md",
    "04-题库/模块习题集-有机化学.md", "04-题库/模块习题集-结构化学.md",
]


def patch_fm(text: str, fields: dict, fix_diff: bool) -> tuple[str, list[str]]:
    if not text.startswith("---"):
        return text, []
    end = text.find("\n---", 3)
    if end < 0:
        return text, []
    block, body = text[3:end], text[end:]
    out: list[str] = []
    notes: list[str] = []
    have = set()
    for line in block.split("\n"):
        m = re.match(r"^(\w[\w_-]*):\s*(.*)$", line)
        if m:
            k, v = m.group(1), m.group(2).strip()
            have.add(k)
            if fix_diff and k == "difficulty" and re.fullmatch(r"\d+-\d+", v):
                lo = int(v.split("-")[0])
                out.append(f"difficulty: {max(lo, 4)}")
                notes.append(f"difficulty {v}→{max(lo,4)}")
                continue
        out.append(line)
    added = False
    for k, v in fields.items():
        if k not in have:
            out.append(f"{k}: {v}")
            notes.append(f"+{k}={v}")
            added = True
    if added:
        # 字段有新增才顺带更新 updated
        for i, line in enumerate(out):
            if re.match(r"^updated:", line):
                out[i] = f"updated: {TODAY}"
                break
        else:
            out.append(f"updated: {TODAY}")
    return "---" + "\n".join(out) + body, notes


def main() -> None:
    touched: list[tuple[Path, str, bytes, str]] = []

    # 1) BOM
    for rel in BOM_FILES:
        f = V / rel
        if not f.exists():
            continue
        raw = f.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            touched.append((f, rel, raw, raw[3:].decode("utf-8")))
            print(f"  [BOM] {rel}")

    # 2) SPECIAL
    for rel, fields in SPECIAL.items():
        f = V / rel
        if not f.exists():
            print(f"  ⚠ 不存在: {rel}")
            continue
        raw = f.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        new, notes = patch_fm(text, fields, fix_diff=False)
        if new != text:
            touched.append((f, rel, raw, new))
            print(f"  {f.name}: {'; '.join(notes)}")

    # 3) 无机化学例题与习题 例题 文件
    n_ex = 0
    for f in (V / "04-题库/教材习题/无机化学例题与习题").rglob("*.md"):
        rel = f.relative_to(V).as_posix()
        if "/例题/" not in rel:
            continue
        raw = f.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        import yaml
        e = text.find("\n---", 3)
        try:
            fm = yaml.safe_load(text[3:e])
        except Exception:
            fm = {}
        if not isinstance(fm, dict) or str(fm.get("type", "")).strip() != "例题":
            continue
        missing = [k for k in ("fidelity", "subject_module", "pack") if fm.get(k) in (None, "", [])]
        if not missing:
            continue
        m = re.search(r"Ch(\d{2})", rel)
        subj = CH_MAP.get(m.group(1) if m else "", "元素与分析")
        new, notes = patch_fm(text, {"fidelity": "原书逐字", "subject_module": subj, "pack": "章节练习"}, fix_diff=False)
        if new != text:
            touched.append((f, rel, raw, new))
            n_ex += 1
            print(f"  例题 {f.name}: {'; '.join(notes)}")
    print(f"  例题补齐: {n_ex} 个")

    print(f"\n📊 待写入 {len(touched)} 文件")
    for f, rel, raw, new in touched:
        dst = BACKUP / rel
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(raw)
        f.write_bytes(new.encode("utf-8"))
        with open(MANIFEST, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"file": rel, "actions": [{"action": "收尾修复（写盘）"}]}, ensure_ascii=False) + "\n")
    print(f"💾 已写入 {len(touched)} 文件，备份在 {BACKUP}")


if __name__ == "__main__":
    main()
