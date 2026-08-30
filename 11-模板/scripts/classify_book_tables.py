"""把习题书成书里的 HTML <table> 整理成 Phase 3 分类台账。

用法:
    python -X utf8 11-模板/scripts/classify_book_tables.py
        [--root 04-课件/习题集/习题书-教师版]
        [--source-root 04-题库]
        [--report 09-审计报告/2026-08-30-习题书V2-表格分类台账.md]
        [--jsonl 09-审计报告/2026-08-30-习题书V2-表格分类台账.jsonl]

分类说明:
    pipe_candidate  无 colspan/rowspan/图片/<br> 且列数不多，优先转 Markdown pipe table
    span_split      含 colspan/rowspan，需拆表或改版式
    image_redesign  表格内嵌图片，需把图片移出单元格
    br_cleanup      含 <br>，需拆行或改成分点
    wide_split      列数 > 8，需拆表或纵向版式
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]


def iter_tables(text: str):
    """按行返回 (start_line, end_line, block) 的表格区间，起始行为 1 基。"""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if "<table" not in line.lower():
            i += 1
            continue
        start = i
        depth = 0
        block: list[str] = []
        j = i
        while j < len(lines):
            current = lines[j]
            block.append(current)
            depth += current.lower().count("<table")
            depth -= current.lower().count("</table>")
            j += 1
            if depth <= 0:
                break
        yield start + 1, j, "\n".join(block)
        i = j


def classify(block: str, max_cols: int) -> str:
    low = block.lower()
    if "colspan" in low or "rowspan" in low:
        return "span_split"
    if "![[" in block or "<img" in low:
        return "image_redesign"
    if "<br" in low:
        return "br_cleanup"
    if max_cols > 8:
        return "wide_split"
    return "pipe_candidate"


def table_stats(block: str) -> tuple[int, int, int, int, int, bool, bool, bool, bool]:
    rows = len(re.findall(r"<tr\b", block, flags=re.I))
    cells = len(re.findall(r"<t[dh]\b", block, flags=re.I))
    max_cols = 0
    for tr in re.findall(r"<tr\b.*?</tr>", block, flags=re.I | re.S):
        max_cols = max(max_cols, len(re.findall(r"<t[dh]\b", tr, flags=re.I)))
    colspan = len(re.findall(r"colspan\s*=", block, flags=re.I))
    rowspan = len(re.findall(r"rowspan\s*=", block, flags=re.I))
    has_image = "![[" in block or "<img" in block.lower()
    has_br = "<br" in block.lower()
    has_formula = "$" in block
    has_pipe = "|" in block
    return rows, max_cols, colspan, rowspan, cells, has_image, has_br, has_formula, has_pipe


def nearest_heading(lines: list[str], start_idx: int) -> str:
    for idx in range(start_idx - 1, max(-1, start_idx - 40), -1):
        m = re.match(r"^#{1,4}\s+(.*)$", lines[idx])
        if m:
            return m.group(1).strip()
    return ""


def clean_preview(block: str, width: int = 90) -> str:
    s = re.sub(r"<[^>]+>", " ", block)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:width] + ("…" if len(s) > width else "")


def build_source_table_map(source_root: Path) -> dict[str, list[dict]]:
    """源文件按归一化签名建立 <table> 位置索引。"""
    mapping: dict[str, list[dict]] = {}
    for md_path in sorted(source_root.rglob("*.md")):
        text = md_path.read_text(encoding="utf-8")
        rel = md_path.relative_to(source_root).as_posix()
        for line_no, raw_line in enumerate(text.splitlines(), 1):
            for block in re.findall(r"<table\b[^>]*>.*?</table>", raw_line, flags=re.I | re.S):
                sig = re.sub(r"\s+", "", block)
                mapping.setdefault(sig, []).append({"file": rel, "line": line_no})
    return mapping


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(VAULT_ROOT / "04-课件/习题集/习题书-教师版"))
    ap.add_argument("--source-root", default=str(VAULT_ROOT / "04-题库"))
    ap.add_argument(
        "--report",
        default=str(VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-表格分类台账.md"),
    )
    ap.add_argument(
        "--jsonl",
        default=str(VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-表格分类台账.jsonl"),
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    source_root = Path(args.source_root).resolve()
    source_map = build_source_table_map(source_root)
    chapters = sorted(p for p in root.rglob("*.md") if p.parent != root)
    records: list[dict] = []

    for md_path in chapters:
        text = md_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        rel = md_path.relative_to(root).as_posix()
        for start, end, block in iter_tables(text):
            sig = re.sub(r"\s+", "", block)
            source_candidates = source_map.get(sig, [])
            rows, max_cols, colspan, rowspan, cells, has_image, has_br, has_formula, has_pipe = (
                table_stats(block)
            )
            kind = classify(block, max_cols)
            records.append(
                {
                    "chapter": rel,
                    "line": start,
                    "end_line": end,
                    "source_candidates": source_candidates,
                    "source_status": (
                        "matched" if len(source_candidates) == 1
                        else "multi" if len(source_candidates) > 1
                        else "unmatched"
                    ),
                    "rows": rows,
                    "cols": max_cols,
                    "cells": cells,
                    "colspan": colspan,
                    "rowspan": rowspan,
                    "has_image": has_image,
                    "has_br": has_br,
                    "has_formula": has_formula,
                    "has_pipe": has_pipe,
                    "classification": kind,
                    "heading": nearest_heading(lines, start - 1),
                    "preview": clean_preview(block),
                }
            )

    from collections import Counter

    kinds = Counter(r["classification"] for r in records)
    per_chapter: Counter = Counter(r["chapter"].split("/")[-1] for r in records)
    L = [
        "---",
        "title: 2026-08-30-习题书V2-表格分类台账",
        "type: 分类台账",
        "task_type: 习题册表格标准化",
        "status: 待逐表处理",
        "created: 2026-08-30",
        "updated: 2026-08-30",
        "---",
        "",
        "# 习题书 V2 表格分类台账（Phase 3）",
        "",
        "> 生成命令：`python 11-模板/scripts/classify_book_tables.py`",
        f"> 扫描目录：`{root.relative_to(VAULT_ROOT)}`",
        "",
        "## 一、分类汇总",
        "",
        "| 分类 | 数量 | 处理方向 |",
        "|---|---:|---|",
    ]
    order = ["pipe_candidate", "span_split", "image_redesign", "br_cleanup", "wide_split"]
    for kind in order:
        L.append(f"| {kind} | {kinds.get(kind, 0)} | {doc_line(kind)} |")
    L.append(f"| **合计** | **{len(records)}** | |")
    L.append("")
    L.append("## 二、逐章分布")
    L.append("")
    L.append("| 章节 | 表格数 |")
    L.append("|---|---:|")
    for name, count in sorted(per_chapter.items(), key=lambda x: -x[1]):
        L.append(f"| {name} | {count} |")
    L.append("")
    L.append("## 三、逐表明细")
    L.append("")
    L.append(
        "| 章节 | 行号 | 行×列 | span | 图片 | <br> | 公式 | 分类 | 源文件定位 | 上文标题 | 预览 |"
    )
    L.append("|---|---:|---:|---|---|---|---|---|---|---|---|---|")
    for r in sorted(records, key=lambda x: (x["chapter"], x["line"])):
        if r["source_status"] == "matched":
            c = r["source_candidates"][0]
            source_loc = f"{c['file']}:{c['line']}"
        elif r["source_status"] == "multi":
            c = r["source_candidates"][0]
            source_loc = f"{c['file']}:{c['line']} 等 {len(r['source_candidates'])} 处"
        else:
            source_loc = "需人工定位"
        L.append(
            "| {chapter} | {line} | {rows}×{cols} | {span} | {img} | {br} | {formula} | "
            "{classification} | {source_loc} | {heading} | {preview} |".format(
                chapter=r["chapter"],
                line=r["line"],
                rows=r["rows"],
                cols=r["cols"],
                span=(r["colspan"], r["rowspan"]),
                img="是" if r["has_image"] else "否",
                br="是" if r["has_br"] else "否",
                formula="是" if r["has_formula"] else "否",
                classification=r["classification"],
                source_loc=source_loc,
                heading=r["heading"].replace("|", "\\|")[:30],
                preview=r["preview"].replace("|", "\\|"),
            )
        )
    L.append("")
    report_path = Path(args.report).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(L) + "\n", encoding="utf-8")

    jsonl_path = Path(args.jsonl).resolve()
    with jsonl_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    unmatched = sum(1 for r in records if r["source_status"] == "unmatched")
    multi = sum(1 for r in records if r["source_status"] == "multi")
    print(f"tables={len(records)} records -> {report_path.name} (unmatched={unmatched} multi={multi})")
    for kind in order:
        print(f"  {kind}: {kinds.get(kind, 0)}")
    return 0


def doc_line(kind: str) -> str:
    return {
        "pipe_candidate": "优先转为 Markdown pipe table",
        "span_split": "拆表或改版式",
        "image_redesign": "图片移出单元格",
        "br_cleanup": "拆行或改分点",
        "wide_split": "拆表或纵向版式",
    }[kind]


if __name__ == "__main__":
    raise SystemExit(main())
