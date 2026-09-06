#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_kb_phase3_zhen.py — 05-真题库 63 题补齐六字段

规则：
  - fidelity: 原书改写（抽查确认题面重排、含讲评定位教师注，非逐字转录）
  - exam_stage: source 含「省级初赛」→ 省预赛；含具体届次初赛 → 初赛
  - pack: 省预赛 → 预赛专项；初赛 → 模块习题集（SOP 规则 R2）
  - subject_module: 文件名前缀映射
  - knowledge_points: 块列表纯文本 → 行内 wikilink；13 个不可解析名用 MINI_KP 映射
  - difficulty 为空的补 3
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8")
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_kb as VKB

V = VKB.VAULT_ROOT
SRC = V / "05-真题库"
BACKUP = V / "09-审计报告" / "备份" / "题库修复-2026-08-31"
MANIFEST = BACKUP / "manifest.jsonl"
TODAY = datetime.date.today().isoformat()

SUBJECT_BY_PREFIX = [
    ("有机", "有机化学"), ("自由基", "有机化学"),
    ("结构", "结构化学"), ("晶体结构", "结构化学"),
    ("分析", "元素与分析"),
    ("物化", "化学原理"), ("化学动力学", "化学原理"), ("热力学", "化学原理"),
    ("电化学", "化学原理"), ("相平衡", "化学原理"), ("平衡", "化学原理"),
    ("无机", "元素与分析"), ("元素", "元素与分析"), ("配合物", "元素与分析"),
    ("氧化还原", "元素与分析"), ("酸碱理论", "元素与分析"),
]

MINI_KP = {
    "滴定计算": "容量分析计算", "矿物化学": "元素化学", "合金组成计算": "化学式推断",
    "莫尔法": "沉淀滴定", "EDTA": "EDTA滴定", "Fe₃O₄": "铁",
    "三棱柱空隙": "密堆积", "键长计算": "键长", "自由基环化": "环化反应",
    "简单六方堆积": "六方密堆积", "晶胞参数": "晶格常数", "自由基链式反应": "自由基",
    "异构体": "配合物异构", "pH计算": "pH",
    "力致变构": None,   # 无落点 → 删除该条目
}


def subject_of(name: str, kps: list[str]) -> str:
    for pref, mod in SUBJECT_BY_PREFIX:
        if f"-{pref}-" in name or name.startswith(f"真题-{pref}-"):
            return mod
    for k in kps:
        if k in ("立体化学", "SN1反应", "SN2反应", "Aldol缩合", "烯烃", "炔烃"):
            return "有机化学"
        if k in ("晶胞", "晶体结构", "Bragg方程", "钙钛矿"):
            return "结构化学"
        if k in ("滴定", "酸碱滴定", "氧化还原滴定", "误差"):
            return "元素与分析"
    return "元素与分析"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    stems = {f.stem for f in (V / "03-知识点").rglob("*.md")}
    touched = 0
    for f in sorted(SRC.glob("*.md")):
        raw = f.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        if not text.startswith("---"):
            print(f"  ⚠ 跳过（无 frontmatter）: {f.name}")
            continue
        end = text.find("\n---", 3)
        if end < 0:
            continue
        block = text[3:end]
        body = text[end:]
        fm = yaml.safe_load(block)
        if not isinstance(fm, dict) or str(fm.get("type", "")).strip() != "真题":
            continue

        kps = fm.get("knowledge_points") or []
        if isinstance(kps, str):
            kps = [kps]
        kps = [str(k).strip().strip('"').strip("[].") if not str(k).strip().startswith("[[")
               else str(k).strip().strip('"[]').replace("[[", "").replace("]]", "")
               for k in kps if str(k).strip()]
        kps = [k for k in kps if k]
        subject = subject_of(f.name, kps)

        src = str(fm.get("source", ""))
        stage = "省预赛" if "省级初赛" in src else "初赛"
        pack = "预赛专项" if stage == "省预赛" else "模块习题集"

        # KP 名称落点
        new_kps: list[str] = []
        notes: list[str] = []
        for k in kps:
            if k in stems:
                new_kps.append(k)
            elif k in MINI_KP:
                tgt = MINI_KP[k]
                if tgt:
                    new_kps.append(tgt)
                    notes.append(f"KP {k}→{tgt}")
                else:
                    notes.append(f"KP {k} 删除（无落点）")
            else:
                new_kps.append(k)
                notes.append(f"⚠ KP {k} 仍不可解析")
        # 去重保序
        seen = set()
        new_kps = [x for x in new_kps if not (x in seen or seen.add(x))]

        add = {
            "fidelity": "原书改写",
            "exam_stage": stage,
            "subject_module": subject,
            "pack": pack,
        }
        diff_line = None if fm.get("difficulty") is not None else "difficulty: 3"

        # —— 行级编辑 ——
        lines = block.split("\n")
        out: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if re.match(r"^knowledge_points:\s*$", line):
                j = i + 1
                while j < len(lines) and re.match(r"^\s*-\s+", lines[j]):
                    j += 1
                out.append("knowledge_points: [" + ", ".join(f'"[[{k}]]"' for k in new_kps) + "]")
                i = j
                continue
            m = re.match(r"^difficulty:\s*(.*)$", line)
            if m and diff_line:
                out.append(diff_line)
                notes.append("difficulty None→3")
                i += 1
                continue
            if re.match(r"^updated:", line):
                out.append(f"updated: {TODAY}")
                i += 1
                continue
            out.append(line)
            i += 1
        # 追加缺失字段（放块尾，YAML 合法）
        for k, v in add.items():
            if not re.search(rf"^{k}:", "\n".join(out), re.M):
                out.append(f"{k}: {v}")
                notes.append(f"+{k}={v}")
            else:
                notes.append(f"{k} 已存在，保留")
        new_block = "\n".join(out)
        new_text = "---" + new_block + body
        if new_text == text:
            continue

        touched += 1
        print(f"  {f.name}: {'; '.join(notes[:5])}")
        if not args.dry:
            rel = f.relative_to(V).as_posix()
            dst = BACKUP / rel
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(raw)
            f.write_bytes(new_text.encode("utf-8"))
            with open(MANIFEST, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"file": rel, "actions": [{"action": "真题库补六字段", "detail": notes}]},
                                    ensure_ascii=False) + "\n")

    print(f"\n📊 {'预览' if args.dry else '已更新'} {touched} 个文件")


if __name__ == "__main__":
    main()
