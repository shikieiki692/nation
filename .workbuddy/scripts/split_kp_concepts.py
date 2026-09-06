#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把题目的 knowledge_points 拆成两级：
  - 能解析到真实文件的  → 留在 knowledge_points（继续作为可校验 wikilink）
  - 解析不到的          → 剥离 [[]] 后移入 concepts（纯文本标签，不校验断链）

设计原则：
  * 链接解析一律复用 validate_kb.find_wikilink_target，禁止自写正则重写
  * 只改动「确实有拆不出的项」的文件，无变化的文件一个字节都不碰
  * 读写一律 newline=""，防止 CRLF 整文件重写
  * 先 dry-run 出统计与样例，人工确认后再 --write

用法：
  python split_kp_concepts.py                 # dry-run，出统计 + 样例
  python split_kp_concepts.py --write         # 实写
  python split_kp_concepts.py --limit 300     # dry-run 只看前 N 个文件（调格式用）
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
sys.path.insert(0, str(VAULT / "11-模板" / "scripts"))
import validate_kb as V  # noqa: E402

TARGET_DIRS = ["04-题库", "05-真题库"]
QB_TYPES = V.QB_TYPES

# 与 validate_kb.check_frontmatter 完全一致的抽取方式
WIKILINK_RE = re.compile(r"(?<!\!)\[\[([^\]|#]+)")
IMAGE_SUFFIX = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

FM_BOUNDARY = re.compile(r"^---\s*$")


# ── frontmatter 文本级定位 ────────────────────────────────────────
def split_fm(text: str):
    """返回 (fm_start_idx, fm_end_idx, lines)；无 frontmatter 返回 (None, None, None)。"""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None, lines
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return 0, i, lines
    return None, None, lines


def locate_field(lines: list[str], fm_end: int, field: str):
    """
    定位字段在 frontmatter 内的行区间。
    返回 (key_idx, val_start, val_end, style)  style ∈ {"inline", "block"}
    val 区间为 [val_start, val_end)
    """
    pat = re.compile(rf"^{re.escape(field)}\s*:")
    for idx in range(1, fm_end):
        if pat.match(lines[idx]):
            rest = lines[idx].split(":", 1)[1].strip()
            if rest:
                return idx, idx, idx + 1, "inline"
            j = idx + 1
            while j < fm_end and re.match(r"^\s*(-|\s)", lines[j]) and lines[j].strip():
                j += 1
            return idx, idx + 1, j, "block"
    return None, None, None, None


# ── 单项分类 ──────────────────────────────────────────────────────
def label_of(item: str) -> str:
    """取出单项的语义标签：[[X|alias]] → X；纯文本 → 原样。"""
    m = WIKILINK_RE.search(item)
    if m:
        return m.group(1).strip()
    return item.strip()


def strip_wikilink(item: str) -> str:
    """把 [[X]] / [[X|alias]] 降级为纯文本 X。"""
    s = item.strip()
    m = re.match(r"^\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]$", s)
    if m:
        return m.group(1).strip()
    return s


def classify(item: str):
    """返回 (归类, 解析到的路径或 None)；归类 ∈ {keep, concept, skip}"""
    if not isinstance(item, str):
        return "skip", None
    lab = label_of(item)
    if not lab:
        return "skip", None
    if Path(lab).suffix.lower() in IMAGE_SUFFIX:
        return "skip", None
    if V.is_placeholder_target(lab):
        return "skip", None
    hit = V.find_wikilink_target(lab, VAULT)
    if hit is None:
        return "concept", None
    return "keep", hit


# ── 渲染 ──────────────────────────────────────────────────────────
def yq(s: str) -> str:
    """YAML 标量安全引号：含 [ ] : # { } & * ! | > % @ ` " 或引号时加双引号。"""
    if s == "":
        return '""'
    if re.search(r'[\[\]:#{}&*!|>%@`",\n]', s) or s != s.strip():
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def render_block(field: str, items: list[str]) -> list[str]:
    out = [f"{field}:"]
    out.extend("  - " + yq(i) for i in items)
    return out


# ── 主流程 ────────────────────────────────────────────────────────
def read_text_raw(path: Path) -> str:
    """读取且完全禁用换行转换（newline="" 必须走 open()，Path.read_text 不接受该参数）。"""
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_text_raw(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def process_file(path: Path, write: bool, stats: Counter, samples: list, backlog: list):
    text = read_text_raw(path)
    fs, fe, lines = split_fm(text)
    if fs is None:
        stats["无frontmatter跳过"] += 1
        return

    ki, vs, ve, style = locate_field(lines, fe, "knowledge_points")
    if ki is None:
        stats["无knowledge_points字段"] += 1
        return
    stats[f"格式-{style}"] += 1

    # 解析原值
    fm_text = "\n".join(lines[fs + 1:fe])
    try:
        import yaml
        fm = yaml.safe_load(fm_text) or {}
    except Exception:
        stats["YAML解析失败跳过"] += 1
        return
    if not isinstance(fm, dict):
        stats["YAML解析失败跳过"] += 1
        return

    raw = fm.get("knowledge_points")
    if raw is None:
        stats["knowledge_points为空"] += 1
        return
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, list):
        stats["knowledge_points类型异常"] += 1
        return

    keep, concepts, skipped = [], [], []
    for it in raw:
        kind, hit = classify(it)
        if kind == "keep":
            keep.append(it)
        elif kind == "concept":
            concepts.append(strip_wikilink(it))
        else:
            skipped.append(it)
            keep.append(it)

    stats["总项数"] += len(raw)
    stats["保留项"] += len(keep)
    stats["降级为concepts项"] += len(concepts)

    if not concepts:
        stats["无需改动的文件"] += 1
        return

    # 约定：knowledge_points 不允许为空。
    # 见 fix_kb_phase2_apply.py:215「列表被清空：knowledge_points 不允许为空 → 保留原样」
    # 与 audit_question_bank.py:344 将空列表判为 P1。
    # 因此当全部项都解析不出时，不拆分、保留原样 —— 这类题需要人工指派一个真实 KP，
    # 脚本不凭空造，也不该用空列表把缺口掩盖成另一种告警。
    if not keep:
        stats["全降级跳过（需人工指派KP）"] += 1
        backlog.append((path.relative_to(VAULT).as_posix(), list(raw), concepts))
        return

    stats["待改动文件"] += 1
    rel = path.relative_to(VAULT).as_posix()
    if len(samples) < 12:
        samples.append((rel, style, list(keep), list(concepts)))

    if not write:
        return

    # 原地替换 knowledge_points 区间，并在其后插入 concepts
    new_field_lines = render_block("knowledge_points", keep)
    if concepts:
        new_field_lines += render_block("concepts", concepts)
    lines[vs:ve] = new_field_lines

    write_text_raw(path, "\n".join(lines))
    stats["已写入"] += 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="实写（默认 dry-run）")
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 个文件（调试用）")
    args = ap.parse_args()

    files: list[Path] = []
    for d in TARGET_DIRS:
        files.extend(sorted((VAULT / d).rglob("*.md")))
    files = [p for p in files if p.name not in V.EXCLUDE_FILE_NAMES]
    if args.limit:
        files = files[: args.limit]

    stats: Counter = Counter()
    samples: list = []
    backlog: list = []
    print(f"扫描 {len(files)} 个文件（{', '.join(TARGET_DIRS)}）…")

    for p in files:
        try:
            process_file(p, args.write, stats, samples, backlog)
        except Exception as e:
            stats["异常跳过"] += 1
            if stats["异常跳过"] <= 5:
                print(f"  !! {p.relative_to(VAULT).as_posix()}: {type(e).__name__}: {e}")

    print("\n═══ 统计 ═══")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k:28s} {v}")

    if samples:
        print("\n═══ 样例（前 12 个待改动文件）═══")
        for rel, style, keep, cp in samples:
            print(f"\n[{style}] {rel}")
            print(f"   knowledge_points 保留 {len(keep)}: {keep[:4]}")
            print(f"   concepts 降级 {len(cp)}: {cp[:6]}")

    if backlog:
        print("\n═══ 全降级文件（知识点一个都解析不出，需人工指派 KP）═══")
        for rel, raw_items, cp in backlog[:20]:
            print(f"  {rel}")
            print(f"      原 knowledge_points: {raw_items}")
        print(f"  …共 {len(backlog)} 个文件（保持原样，未拆分）")

    print("\n" + ("已实写。" if args.write else "这是 DRY-RUN，加 --write 才会落盘。"))


if __name__ == "__main__":
    main()
