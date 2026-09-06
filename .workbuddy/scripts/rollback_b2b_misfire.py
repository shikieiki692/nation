#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
回滚 B2b 误写：infer_question_type.py 漏了 type 白名单，把 question_type
写进了索引 / README / 真题整卷等非题目文件。

回滚基准 = git HEAD（B2a 提交 43b4b14d 之后工作区只有 B2b 的改动，
所以 HEAD 版本就是写入前的状态）。
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(r"C:\Obsidion\妙妙屋")

# verify 扫出 22 个「type 非题目 却有 question_type」的文件。
# 其中 05-真题库/真题-*.md 的 type 是「真题」，它们本来就是合法题目
# （B2a 统计题目总数 4,186 时已把 05-真题库 的 63 个算进去），不回滚。
TARGETS = [
    "04-题库/教学改编题/无机和结构化学/题-改编-14-配位化合物讲义替换题（2026-07-04）.md",
    "04-题库/教材习题/ABOC/索引.md",
    "04-题库/教材习题/无机化学例题与习题/索引.md",
    "04-题库/教材习题/物理化学Atkins/主题17-19-动力学与表面过程-习题.md",
    "04-题库/教材习题/结构化学基础/zhao_ch351-482_image_index.md",
    "04-题库/教材习题/结构化学基础/题库审计清单.md",
    "04-题库/有机化学/README.md",
    "04-题库/有机化学/索引.md",
    "04-题库/模块习题集-化学原理.md",
    "04-题库/物理化学/化学动力学/README.md",
    "04-题库/物理化学/化学平衡/README.md",
    "04-题库/物理化学/热力学与热化学/README.md",
    "04-题库/物理化学/电化学/README.md",
    "04-题库/真题/省预赛/2021-浙江预赛-答案.md",
    "04-题库/真题/省预赛/2021-浙江预赛.md",
    "04-题库/真题/省预赛/2022-浙江预赛.md",
    "04-题库/真题/省预赛/2023-浙江预赛.md",
    "04-题库/真题/第34届决赛/索引.md",
    "04-题库/经典例题/README.md",
]

QT_LINE = re.compile(r"^question_type\s*:")


def read_raw(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_raw(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def git_show(rel: str) -> str:
    out = subprocess.run(
        ["git", "show", f"HEAD:{rel}"],
        cwd=ROOT, capture_output=True,
    )
    if out.returncode != 0:
        raise RuntimeError(out.stderr.decode("utf-8", "replace")[:200])
    # git show 走管道会做换行转换，统一成 LF 后再进 split("\n") 比较
    return out.stdout.decode("utf-8").replace("\r\n", "\n")


def fm_range(lines: list[str]):
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i
    return None


def main() -> None:
    done = removed = restored = unchanged = 0
    for rel in TARGETS:
        p = ROOT / rel
        if not p.exists():
            print(f"  !! 不存在 {rel}")
            continue
        old_text = git_show(rel)
        old_lines = old_text.split("\n")
        old_end = fm_range(old_lines)
        if old_end is None:
            print(f"  !! HEAD 版本无 frontmatter {rel}")
            continue
        old_qt = [
            ln for ln in old_lines[1:old_end]
            if QT_LINE.match(ln)
        ]

        cur_text = read_raw(p)
        cur_lines = cur_text.split("\n")
        cur_end = fm_range(cur_lines)
        if cur_end is None:
            print(f"  !! 当前无 frontmatter {rel}")
            continue
        idxs = [i for i in range(1, cur_end) if QT_LINE.match(cur_lines[i])]

        if not idxs and not old_qt:
            unchanged += 1
            continue

        if not idxs:
            # 当前没有、HEAD 有 —— 不该发生，说明 HEAD 已被别的改动影响
            print(f"  ?? 当前无 question_type 但 HEAD 有：{rel}")
            unchanged += 1
            continue

        if old_qt:
            # 原本就有值 → 还原成原值（保持原行的行尾风格）
            target = idxs[0]
            cr = "\r" if cur_lines[target].endswith("\r") else ""
            cur_lines[target] = old_qt[0].rstrip("\r") + cr
            for j in reversed(idxs[1:]):
                del cur_lines[j]
            restored += 1
        else:
            # 原本没有 → 整行删掉
            for j in reversed(idxs):
                del cur_lines[j]
            removed += 1

        write_raw(p, "\n".join(cur_lines))
        done += 1

    print(f"\n回滚完成：处理 {done} 个（删除误加 {removed} / 还原原值 {restored} / 无需改 {unchanged}）")


if __name__ == "__main__":
    main()
