# -*- coding: utf-8 -*-
"""把讲义里学生可见的教师向 blockquote 元信息移入 HTML 注释。

背景：v1.2 规定教师侧信息（对应专题/对应备课大纲/前置要求/深度边界/考纲覆盖/
使用建议/本讲定位/适用）只能出现在 frontmatter 或 HTML 注释，禁止进入学生可见正文。

关键约束：
1. 同一 blockquote run 内常混装学生可见导语（如「本讲的核心目标：…」），
   必须**逐行挑选**搬移，禁止整块包注释。
2. 扫描必须跳过已有 HTML 注释区，否则会把已合规文件重复包注释。
3. EXT 字段（前置知识/核心概念/对应专题页/对应考纲）只在与 CORE 同 run 时才搬，
   防止长篇学生向解释被误搬。
4. 落点：邻近（≤15 行）有含「教师向」字样的注释块则合并插入闭合行前，否则就地新建。

用法:
    python -X utf8 11-模板/scripts/handout_teacher_meta_to_comment.py [--dry-run] [--apply]
默认 dry-run。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "04-课件" / "学生讲义"

def iter_sources():
    """递归采集讲义源（按模块分子目录后），排除 _归档 与 _ 开头的辅助目录。"""
    for p in sorted(SRC.rglob("*.md")):
        rel = p.relative_to(SRC)
        if "_归档" in rel.parts or rel.parts[0].startswith("_"):
            continue
        yield p



CORE = ["对应专题", "对应备课大纲", "前置要求", "深度边界", "考纲覆盖",
        "使用建议", "建议使用方式", "本讲定位", "适用"]
EXT = ["前置知识", "核心概念", "对应专题页", "对应考纲"]

LEAK_CORE = re.compile(r"^>\s*\*\*(" + "|".join(CORE) + r")\*\*")
LEAK_EXT = re.compile(r"^>\s*\*\*(" + "|".join(EXT) + r")\*\*")
EMPTY_QUOTE = re.compile(r"^>\s*$")
TEACHER_MARK = "教师向"

OPEN_TAG = "<!-- ============ 教师向信息区+规划区（学生不可见，Word/PDF 导出自动忽略） ============"
CLOSE_TAG = "============================================================================= -->"


def detect_eol(lines: list[str]) -> str:
    for l in lines:
        if l.endswith("\r\n"):
            return "\r\n"
        if l.endswith("\n"):
            return "\n"
    return "\n"


def mask_fences(lines: list[str]) -> list[str]:
    """把 ``` 围栏内与裸 mermaid 流程图行置空。

    mermaid 箭头 `A --> B` 含 `-->`，不屏蔽会被误判成注释闭合标签。
    """
    out: list[str] = []
    in_fence = False
    for L in lines:
        if L.strip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        if (L.lstrip().startswith(">") and "-->" in L
                and "--" in L.replace("-->", "")):
            out.append("")
            continue
        out.append("" if in_fence else L)
    return out


def find_comment_blocks(lines: list[str]) -> list[tuple[int, int, str]]:
    """返回 [(start, end, text)]，含单行与多行注释块。基于屏蔽后的行判定。"""
    masked = mask_fences(lines)
    blocks: list[tuple[int, int, str]] = []
    i = 0
    n = len(masked)
    while i < n:
        L = masked[i]
        if "<!--" in L:
            if "-->" in L and L.index("-->") > L.index("<!--"):
                blocks.append((i, i, L))
                i += 1
                continue
            start = i
            j = i + 1
            while j < n and "-->" not in lines[j]:
                j += 1
            if j < n:
                blocks.append((start, j, "".join(lines[start:j + 1])))
                i = j + 1
            else:
                # 未闭合注释，视为到文件尾
                blocks.append((start, n - 1, "".join(lines[start:n])))
                i = n
        else:
            i += 1
    return blocks


def in_blocks(idx: int, blocks) -> bool:
    for s, e, _ in blocks:
        if s <= idx <= e:
            return True
    return False


def run_bounds(lines: list[str], i: int) -> tuple[int, int]:
    s = i
    while s - 1 >= 0 and lines[s - 1].lstrip().startswith(">"):
        s -= 1
    e = i
    while e + 1 < len(lines) and lines[e + 1].lstrip().startswith(">"):
        e += 1
    return s, e


def build_block(move: list[str], eol: str) -> list[str]:
    out = [OPEN_TAG + eol]
    out.extend(move)
    out.append(CLOSE_TAG + eol)
    return out


def process(path: Path, apply: bool) -> dict:
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    lines = text.splitlines(keepends=True)
    eol = detect_eol(lines)
    masked = mask_fences(lines)
    blocks = find_comment_blocks(lines)
    diff_before = "".join(masked).count("<!--") - "".join(masked).count("-->")

    drop: set[int] = set()
    inserts: dict[int, list[str]] = {}
    stats = {"move": 0, "keep": 0, "merged": 0, "created": 0, "files_hit": 0}

    i = 0
    n = len(lines)
    while i < n:
        if in_blocks(i, blocks):
            i += 1
            continue
        stripped = masked[i].rstrip("\r\n")
        if not LEAK_CORE.match(stripped):
            i += 1
            continue
        s, e = run_bounds(lines, i)
        run = lines[s:e + 1]
        has_core = any(LEAK_CORE.match(x.rstrip("\r\n")) for x in run)
        move, keep = [], []
        for off, x in enumerate(run):
            t = x.rstrip("\r\n")
            if LEAK_CORE.match(t) or (has_core and LEAK_EXT.match(t)):
                move.append(x)
                drop.add(s + off)
            else:
                keep.append(x)
        # 清理 keep 首尾的空引用行
        while keep and EMPTY_QUOTE.match(keep[0].rstrip("\r\n")):
            keep.pop(0)
        while keep and EMPTY_QUOTE.match(keep[-1].rstrip("\r\n")):
            keep.pop()

        # 找合并目标：距 run 最近且含「教师向」的注释块
        target_end = None
        best = 10 ** 9
        for bs, be, btext in blocks:
            if TEACHER_MARK not in btext:
                continue
            dist = min(abs(bs - s), abs(be - s))
            if dist <= 15 and dist < best:
                best = dist
                target_end = be

        if move:
            if target_end is not None:
                inserts.setdefault(target_end, []).extend(move)
                stats["merged"] += 1
            else:
                inserts.setdefault(s, []).extend(build_block(move, eol))
                stats["created"] += 1
            stats["move"] += len(move)
        stats["keep"] += len(keep)
        i = e + 1

    if stats["move"] == 0:
        return stats

    out: list[str] = []
    for idx, L in enumerate(lines):
        if idx in inserts:
            out.extend(inserts[idx])
        if idx not in drop:
            out.append(L)
    new_text = "".join(out)

    # 闭合自检：本次只应成对新增注释，前后「未配对开标签数」必须不变
    m2 = "".join(mask_fences(new_text.splitlines(keepends=True)))
    diff_after = m2.count("<!--") - m2.count("-->")
    if diff_after != diff_before:
        print("  [ABORT] 注释配平变化 %d→%d，跳过: %s" % (diff_before, diff_after, path.name))
        return stats

    stats["files_hit"] = 1
    if apply:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_text)
    return stats


def main() -> None:
    apply = "--apply" in sys.argv
    files = sorted(p for p in iter_sources() if p.name != "README.md")
    tot = {"move": 0, "keep": 0, "merged": 0, "created": 0, "files_hit": 0}
    for p in files:
        st = process(p, apply)
        if st["move"]:
            print("%-52s 移 %2d 行 | 留 %2d 行 | 合并 %d 新建 %d"
                  % (p.name, st["move"], st["keep"], st["merged"], st["created"]))
        for k in tot:
            tot[k] += st[k]
    print("\n合计：触及 %d 份，移入注释 %d 行，保留可见 %d 行，合并块 %d / 新建块 %d"
          % (tot["files_hit"], tot["move"], tot["keep"], tot["merged"], tot["created"]))
    print("模式：%s" % ("APPLY 已写盘" if apply else "DRY-RUN 未写盘"))


if __name__ == "__main__":
    main()
