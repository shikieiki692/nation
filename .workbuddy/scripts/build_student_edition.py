# -*- coding: utf-8 -*-
"""
随堂层第一轮习题集 → 学生版（纯题卷无答案）

规则：
  - 进入跳过模式：`**参考答案**：` / `**答案：…**` 行，或 `#…参考答案(汇总)?` 节
  - 跳过终止：下一个 `### ` 题头 / `## ` 非答案节 / `---` 分隔线 / `**题目**：`
  - `## …参考答案(汇总)?` 节 → 跳到 EOF（卷尾答案区）
  - 汇编后复扫「答案」残留并打标（质量优先，人工复核）
  - 输出 staging：.workbuddy/tmp/student_build/（源文件不动）
"""
import io
import os
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

VAULT = Path(r"C:\Obsidion\妙妙屋")
QB_DIR = os.path.join(str(VAULT), "04-题库")
SRC_DIR = VAULT / "04-课件" / "习题集"
OUT = VAULT / ".workbuddy" / "tmp" / "student_build"

ENTER = re.compile(r"^\s*(?:\*\*参考答案\*\*|\*\*答案[:：]|#{1,3}\s*[^\n]*参考答案)")
ANS_SECTION = re.compile(r"^\s*#{1,3}\s*[^\n]*参考答案")
LEAVE = re.compile(r"^\s*(?:#{3} |## |---\s*$|\*\*题目\*\*：)")
# 来源行与尾部索引
YUANTI = re.compile(r"^\s*>\s*原题[：:]\s*\[\[([^\]|]+)")
INDEX_SEC = re.compile(r"^\s*#{1,3}\s*[^\n]*(?:来源索引|知识点索引|题目索引)")

_real_cache = {}


def is_real_exam(basename: str) -> bool:
    """判定题库题目是否为真题（路径含 /真题/）。"""
    if basename in _real_cache:
        return _real_cache[basename]
    hit = None
    for dp, _, ns in os.walk(QB_DIR):
        if basename + ".md" in ns:
            hit = os.path.join(dp, basename + ".md")
            break
    res = bool(hit) and ("真题" in Path(hit).parts)
    _real_cache[basename] = res
    return res


def _sec_level(ln: str):
    """返回 ATX 标题层级（# 个数）；非标题返回 None。"""
    m = re.match(r"^(#{1,6})\s", ln)
    return len(m.group(1)) if m else None


def strip_source_and_index(text: str):
    """非真题的 `> 原题：` 行删除；索引节（来源/知识点/题目索引）吞至下一个同级或更高级标题。

    ⚠️ 2026-09-18 修复：原实现命中索引节后 `sec=True` 吞到 EOF，但索引节并非总在卷尾
    （沉淀溶解平衡第537行、周期律第525行均在卷中），会把其后半卷全部吞掉
    （两卷分别丢失 20 / 22 题）。现改为：遇到层级 <= 索引节层级的标题即退出跳过。
    """
    lines = text.split("\n")
    out, drop, sec_lv = [], 0, None
    for ln in lines:
        if sec_lv is not None:
            lv = _sec_level(ln)
            if lv is not None and lv <= sec_lv:
                sec_lv = None                 # 回到正文层级 → 停止跳过
            else:
                drop += 1
                continue
        if INDEX_SEC.match(ln):
            sec_lv = _sec_level(ln) or 2      # 索引节通常为 ##（2 级）
            drop += 1
            continue
        m = YUANTI.match(ln)
        if m:
            stem = m.group(1).strip().rstrip("]").strip()
            if not is_real_exam(stem):
                drop += 1
                continue
        out.append(ln)
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out) + "\n", drop


def strip_answers(text: str):
    lines = text.replace("\r\n", "\n").split("\n")
    out, skip, sec_skip = [], False, False
    removed = 0
    for ln in lines:
        if sec_skip:
            continue                       # 卷尾答案节：直接吞到 EOF
        if skip:
            if ANS_SECTION.match(ln):
                sec_skip = True            # 节级答案区 → 吞到 EOF
                removed += 1
                continue
            if LEAVE.match(ln):
                skip = False               # 回到题面
            else:
                removed += 1
                continue
        if ENTER.match(ln):
            if ANS_SECTION.match(ln):
                sec_skip = True
            else:
                skip = True
            removed += 1
            continue
        out.append(ln)
    return "\n".join(out).strip() + "\n", removed


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(SRC_DIR.glob("第一轮*.md"))
    total_removed = 0
    print(f"{'文件':<38} {'删行':>4}  残留")
    for f in files:
        t = f.read_text(encoding="utf-8", newline="")
        body, _ = (t.split("\n---", 2)[2], None) if t.startswith("---") and t.count("\n---") >= 2 else (t, None)
        # FM 行级剥离（正文含 --- 分隔线时 split 法会出错；用首行/闭合行扫描）
        ls = t.replace("\r\n", "\n").split("\n")
        if ls and ls[0].strip() == "---":
            for i in range(1, len(ls)):
                if ls[i].strip() == "---":
                    body = "\n".join(ls[i + 1:])
                    break
        else:
            body = t
        new_body, removed = strip_answers(body)
        new_body, dropped = strip_source_and_index(new_body)
        removed += dropped
        # 复扫残留答案标记（题面区不应再有）
        residual = [
            (i + 1, ln[:50])
            for i, ln in enumerate(new_body.splitlines())
            if re.search(r"参考答案|\*\*答案[:：]|^答案[:：]", ln)
        ]
        header = t.replace("\r\n", "\n").split("\n")
        fm_txt = ""
        if header and header[0].strip() == "---":
            for i in range(1, len(header)):
                if header[i].strip() == "---":
                    fm_txt = "\n".join(header[: i + 1]) + "\n"
                    break
        (OUT / f.name).write_text(fm_txt + new_body, encoding="utf-8", newline="")
        total_removed += removed
        flag = f"⚠ {len(residual)} 处: {residual[0][1]}" if residual else "—"
        print(f"{f.name:<38} {removed:>4}  {flag}")
    print("-" * 60)
    print(f"共 {len(files)} 文件，删行 {total_removed}")


if __name__ == "__main__":
    main()
