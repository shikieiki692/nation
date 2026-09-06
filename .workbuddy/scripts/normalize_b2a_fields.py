#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B2a 题库 frontmatter 字段治理（确定性操作）

三件事，一次遍历完成：
  1. subject -> source_subject      键改名，值原样保留（消歧：subject 是来源教材科目，
                                     subject_module 是四大模块，两者分工并存）
  2. teaching_level 收敛到 4 档      基础 / 巩固 / 拓展 / 竞赛
                                     缺失值从 difficulty 推断；difficulty 也缺的不推断
  3. 补 year（仅 04-题库/真题）       路径「第{N}届」→ year = N + 1986（11 组配对 100% 验证）

设计原则（沿用 B1）：
  * 行级原地替换，不重新序列化 YAML —— diff 最小、行尾零污染
  * 读写一律 newline=""（必须走 open()，Path.read_text 不接受该参数）
  * 只改「确实需要改」的文件，无变化的文件一个字节都不碰
  * 先 dry-run 出统计与样例，人工确认后再 --write

为什么可以放心做：validate_kb.py 的 QB_ENUM 只约束
fidelity/difficulty/exam_stage/subject_module 四字段，对 teaching_level /
question_type / subject 完全无校验 —— 改名归并不会触发任何告警，但也意味着
规范只能落在 SOP 里，校验器保护不了。

用法：
  python normalize_b2a_fields.py                     # dry-run
  python normalize_b2a_fields.py --write             # 实写
  python normalize_b2a_fields.py --changed-list F    # 把待改动文件清单写到 F
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
sys.path.insert(0, str(VAULT / "11-模板" / "scripts"))
import validate_kb as V  # noqa: E402

TARGET_DIRS = ["04-题库", "05-真题库"]
ZHENTI_DIR = "04-题库/真题"

# ── teaching_level 收敛映射 ─────────────────────────────────────
# 长尾值的落点依据（2026-09-02 实测）：
#   拔高/提高/进阶/决赛/高级 100% 落在真题目录 → 语义就是竞赛层
#   强化/挑战 100% 或非真题为主，语义是拓展
LEVEL_MAP = {
    "基础": "基础",
    "巩固": "巩固",
    "拓展": "拓展",
    "竞赛拔高": "竞赛",
    "入门": "基础",
    "强化": "拓展",
    "挑战": "拓展",
    "拔高": "竞赛",
    "提高": "竞赛",
    "进阶": "竞赛",
    "决赛": "竞赛",
    "高级": "竞赛",
    "竞赛决赛": "竞赛",
    "竞赛深化": "竞赛",
}
LEVELS_4 = {"基础", "巩固", "拓展", "竞赛"}

# difficulty -> teaching_level（缺失值推断用，区间值取中位四舍五入）
DIFF_TO_LEVEL = {1: "基础", 2: "基础", 3: "巩固", 4: "拓展", 5: "竞赛"}

# 年份换算：第 N 届 → N + 1986（第27届=2013 … 第39届=2025，11 组配对全中）
JI_RE = re.compile(r"第(\d+)届")
YEAR_BASE = 1986
YEAR_RANGE = (1984, 2035)


# ── frontmatter 文本级定位（与 B1 的 split_kp_concepts.py 完全一致）────
def split_fm(text: str):
    """返回 (fm_start_idx, fm_end_idx, lines)；无 frontmatter 返回 (None, None, lines)。"""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None, lines
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return 0, i, lines
    return None, None, lines


def find_key_line(lines: list[str], fm_end: int, field: str):
    """
    定位 frontmatter 内某字段的行号。
    用 `^field:` 锚定 —— 关键：`^subject:` 不会匹配 `subject_module:`，
    因为 subject 后面紧跟的是 `_` 而不是 `:` 或空白。
    """
    pat = re.compile(rf"^{re.escape(field)}\s*:")
    for idx in range(1, fm_end):
        if pat.match(lines[idx]):
            return idx
    return None


def read_value(line: str):
    """取出 `key: value` 的 value，返回 (裸值, 引号符 or None)。"""
    _, _, rest = line.partition(":")
    v = rest.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1], v[0]
    return v, None


def replace_value(line: str, newval: str) -> str:
    """只替换 value 部分，保留 key 前的缩进、冒号后的空格、行尾空白。"""
    m = re.match(r"^(\s*[A-Za-z_][\w\-]*\s*:\s*)(.*?)(\s*)$", line)
    if not m:
        return line
    prefix, old, suffix = m.groups()
    q = old[0] if len(old) >= 2 and old[0] == old[-1] and old[0] in "\"'" else None
    new = f"{q}{newval}{q}" if q else newval
    return prefix + new + suffix


def line_term(line: str) -> str:
    """
    该行使用的行尾符（split("\\n") 之后，CRLF 行的 "\\r" 会留在行尾）。
    插入新行时必须沿用邻居的行尾风格，否则会在 CRLF 文件里插进裸 LF 行。
    """
    return "\r" if line.endswith("\r") else ""


def term_at(lines: list[str], idx: int) -> str:
    """取插入位置 idx 处的行尾风格（插在 lines[idx] 之前）。"""
    if idx < len(lines):
        return line_term(lines[idx])
    return line_term(lines[-1]) if lines else ""


def read_text_raw(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_text_raw(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def mid_round(x: float) -> int:
    """四舍五入（half-up，不用 Python 的 banker's rounding）。"""
    return int(math.floor(x + 0.5))


def infer_level_from_difficulty(fm: dict):
    """difficulty -> teaching_level；无法推断返回 None（绝不做双重推测）。"""
    d = fm.get("difficulty")
    if d is None or isinstance(d, (list, dict)):
        return None
    if isinstance(d, (int, float)):
        n = int(d)
        return DIFF_TO_LEVEL.get(n)
    m = re.match(r"^\s*(\d+)\s*[-~]\s*(\d+)\s*$", str(d))
    if m:
        return DIFF_TO_LEVEL.get(mid_round((int(m.group(1)) + int(m.group(2))) / 2))
    m = re.match(r"^\s*(\d+)\s*$", str(d))
    if m:
        return DIFF_TO_LEVEL.get(int(m.group(1)))
    return None


# ── 单文件处理 ───────────────────────────────────────────────────
def process_file(path: Path, write: bool, stats: Counter, samples: list, changed: list):
    rel = path.relative_to(VAULT).as_posix()
    text = read_text_raw(path)
    fs, fe, lines = split_fm(text)
    if fs is None:
        stats["无frontmatter跳过"] += 1
        return

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

    # feat == 收尾时统一写入，避免多次落盘
    dirty = False
    inserts: list[tuple[int, str]] = []   # (插入位置, 新行内容)
    notes: list[str] = []

    # ── 1. subject -> source_subject ──
    if "subject" in fm:
        if "source_subject" in fm:
            stats["subject改名跳过(已有source_subject)"] += 1
        else:
            i = find_key_line(lines, fe, "subject")
            if i is None:
                stats["subject改名失败(定位不到行)"] += 1
            else:
                lines[i] = re.sub(r"^(\s*)subject(\s*:)", r"\1source_subject\2", lines[i])
                dirty = True
                stats["subject改名"] += 1
                notes.append("subject→source_subject")

    # ── 2. teaching_level 收敛 ──
    if "teaching_level" in fm:
        cur = fm.get("teaching_level")
        if isinstance(cur, (list, dict)):
            stats["teaching_level类型异常跳过"] += 1
        else:
            s = str(cur).strip()
            if s in LEVELS_4:
                stats["teaching_level已在4档内"] += 1
            elif s in LEVEL_MAP:
                i = find_key_line(lines, fe, "teaching_level")
                if i is None:
                    stats["teaching_level归并失败(定位不到行)"] += 1
                else:
                    lines[i] = replace_value(lines[i], LEVEL_MAP[s])
                    dirty = True
                    stats[f"归并 {s}→{LEVEL_MAP[s]}"] += 1
                    notes.append(f"level {s}→{LEVEL_MAP[s]}")
            else:
                stats[f"teaching_level未知值跳过[{s}]"] += 1
    else:
        # 缺失 → 从 difficulty 推断，插到 difficulty 行之后（diff 里一眼看到依据）
        lv = infer_level_from_difficulty(fm)
        if lv is None:
            stats["teaching_level缺失且difficulty不可推断"] += 1
        else:
            i = find_key_line(lines, fe, "difficulty")
            if i is None:
                inserts.append((fe, f"teaching_level: {lv}{term_at(lines, fe)}"))
            else:
                inserts.append((i + 1, f"teaching_level: {lv}{term_at(lines, i + 1)}"))
            dirty = True
            stats[f"推断补全 teaching_level={lv}"] += 1
            notes.append(f"+level {lv}(from difficulty)")

    # ── 3. 补 year（仅 04-题库/真题 且 type=题目）──
    if rel.startswith(ZHENTI_DIR + "/") and fm.get("type") == "题目" and "year" not in fm:
        m = JI_RE.search(rel)
        if m:
            y = int(m.group(1)) + YEAR_BASE
            if YEAR_RANGE[0] <= y <= YEAR_RANGE[1]:
                inserts.append((fe, f"year: {y}{term_at(lines, fe)}"))
                dirty = True
                stats["补year(届数换算)"] += 1
                notes.append(f"+year {y}")
            else:
                stats["year超出合理范围跳过"] += 1
        else:
            stats["真题无届数无法补year"] += 1

    if not dirty:
        stats["无需改动的文件"] += 1
        return

    stats["待改动文件"] += 1
    changed.append(rel)
    if len(samples) < 15:
        samples.append((rel, notes))

    if not write:
        return

    # 插入操作从后往前做，避免前面的插入打乱后面的索引
    for idx, newline in sorted(inserts, key=lambda x: -x[0]):
        lines.insert(idx, newline)

    write_text_raw(path, "\n".join(lines))
    stats["已写入"] += 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="实写（默认 dry-run）")
    ap.add_argument("--changed-list", default="", help="把待改动文件清单写到该路径")
    args = ap.parse_args()

    files: list[Path] = []
    for d in TARGET_DIRS:
        files.extend(sorted((VAULT / d).rglob("*.md")))
    files = [p for p in files if p.name not in V.EXCLUDE_FILE_NAMES]

    stats: Counter = Counter()
    samples: list = []
    changed: list = []
    print(f"扫描 {len(files)} 个文件（{', '.join(TARGET_DIRS)}）…")

    for p in files:
        try:
            process_file(p, args.write, stats, samples, changed)
        except Exception as e:
            stats["异常跳过"] += 1
            if stats["异常跳过"] <= 5:
                print(f"  !! {p.relative_to(VAULT).as_posix()}: {type(e).__name__}: {e}")

    if args.changed_list:
        out = Path(args.changed_list)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(changed), encoding="utf-8", newline="")
        print(f"\n待改动清单已写入：{out}（{len(changed)} 条）")

    print("\n═══ 统计 ═══")
    for k, v in sorted(stats.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {k:44s} {v}")

    if samples:
        print("\n═══ 样例（前 15 个待改动文件）═══")
        for rel, notes in samples:
            print(f"  {rel}")
            print(f"      {', '.join(notes)}")

    print("\n" + ("已实写。" if args.write else "这是 DRY-RUN，加 --write 才会落盘。"))


if __name__ == "__main__":
    main()
