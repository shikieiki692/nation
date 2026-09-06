#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B2a 实写后的逐行校验。

为什么不用 git diff 验证行尾：.gitattributes 里有 `*.md text eol=lf`，
git 在 diff 时会做 CRLF 归一化，CRLF 污染在 git diff 里是隐形的。
所以必须与快照做逐字节/逐行比对。

检查项：
  1. 只允许三种 diff 操作：equal / replace(1:1) / insert
     —— 绝不允许 delete，绝不允许 1 行变多行
  2. replace 的旧行与新行必须行尾风格一致（都带 \\r 或都不带）
  3. insert 的新行只能是 teaching_level / year，且行尾风格与邻居一致
  4. 全库不复存在 `subject:` 键（source_subject 已就位），subject_module 数量不变
  5. teaching_level 全部落在 4 档内
"""
from __future__ import annotations

import difflib
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
CHANGED = VAULT / ".workbuddy/backups/b2a_changed_files.txt"
CRLF_BEFORE = VAULT / ".workbuddy/backups/b2a_crlf_before.json"
LEVELS_4 = {"基础", "巩固", "拓展", "竞赛"}

SUBJECT_KEY = re.compile(r"^subject[ \t]*:")
SOURCE_SUBJECT_KEY = re.compile(r"^source_subject[ \t]*:")
SUBJECT_MODULE_KEY = re.compile(r"^subject_module[ \t]*:")
TEACHING_KEY = re.compile(r"^teaching_level[ \t]*:")
YEAR_KEY = re.compile(r"^year[ \t]*:")
OK_INSERT = re.compile(r"^(teaching_level|year)[ \t]*:")


def find_snapshot() -> Path:
    zips = sorted((VAULT / ".workbuddy/backups").glob("b2a_before_*.zip"))
    if not zips:
        sys.exit("找不到 b2a_before_*.zip 快照")
    return zips[-1]


def read_raw(path: Path) -> str:
    """
    读取且禁用换行转换。
    注意：Path.read_text() 不接受 newline= 参数；而默认 newline=None 会做通用
    换行折叠（CRLF -> LF），恰好抹掉本脚本要检测的 CRLF 差异，必须走 open()。
    """
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def main() -> None:
    snap = find_snapshot()
    print(f"快照: {snap.name}")

    rels = [
        l.strip()
        for l in CHANGED.read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]
    before = json.loads(CRLF_BEFORE.read_text(encoding="utf-8"))
    print(f"待校验文件: {len(rels)}\n")

    problems: Counter = Counter()
    examples: list[str] = []
    n_crlf_before = n_crlf_after = 0

    def flag(kind: str, rel: str, detail: str) -> None:
        problems[kind] += 1
        if len(examples) < 25:
            examples.append(f"[{kind}] {rel}\n        {detail}")

    with zipfile.ZipFile(snap) as z:
        names = set(z.namelist())
        for rel in rels:
            if rel not in names:
                flag("快照缺失", rel, "")
                continue
            old = z.read(rel).decode("utf-8")
            new = read_raw(VAULT / rel)

            o_lines = old.split("\n")
            n_lines = new.split("\n")
            n_crlf_before += old.count("\r\n")
            n_crlf_after += new.count("\r\n")

            sm = difflib.SequenceMatcher(None, o_lines, n_lines, autojunk=False)
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "equal":
                    continue
                if tag == "delete":
                    flag("出现删除操作", rel, f"删除 {o_lines[i1:i2]!r}")
                    continue
                if tag == "replace":
                    if (i2 - i1) != (j2 - j1):
                        flag("replace 行数不等", rel,
                             f"{o_lines[i1:i2]!r} -> {n_lines[j1:j2]!r}")
                        continue
                    for o, n in zip(o_lines[i1:i2], n_lines[j1:j2]):
                        if o.endswith("\r") != n.endswith("\r"):
                            flag("replace 行尾风格改变", rel, f"{o!r} -> {n!r}")
                    continue
                if tag == "insert":
                    for n in n_lines[j1:j2]:
                        if not OK_INSERT.match(n):
                            flag("插入了预期外的行", rel, f"{n!r}")
                        # 行尾风格必须与后一行（若存在）或前一行一致
                        nb = n_lines[j2] if j2 < len(n_lines) else n_lines[j1 - 1]
                        if n.endswith("\r") != nb.endswith("\r"):
                            flag("插入行行尾与邻居不符", rel, f"{n!r} vs {nb!r}")
                    continue
                flag("未知 diff 操作", rel, tag)

    print("═══ 逐行 diff 检查 ═══")
    if problems:
        for k, v in problems.most_common():
            print(f"  ✗ {k:28s} {v}")
        print("\n  样例：")
        for e in examples:
            print("    " + e)
    else:
        print("  ✓ 全部通过：无删除、无行数不等、无行尾风格改变、插入行均合法")

    print(f"\n═══ 行尾字节统计（git diff 看不到这个）═══")
    print(f"  改动前 CRLF 总数: {n_crlf_before}")
    print(f"  改动后 CRLF 总数: {n_crlf_after}")
    print(f"  差值: {n_crlf_after - n_crlf_before:+d}（应等于插入行的数量，非负）")

    # ── 全局字段检查 ──────────────────────────────────────────
    print("\n═══ 全库字段检查 ═══")
    stat: Counter = Counter()
    bad_levels: Counter = Counter()
    for d in ("04-题库", "05-真题库"):
        for p in (VAULT / d).rglob("*.md"):
            txt = read_raw(p)
            lines = txt.split("\n")
            if not lines or lines[0].strip() != "---":
                stat["无frontmatter"] += 1
                continue
            fe = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
            if fe is None:
                stat["frontmatter未闭合"] += 1
                continue
            head = lines[1:fe]
            stat["文件总数"] += 1
            if any(SUBJECT_KEY.match(l) for l in head):
                stat["残留 subject 键"] += 1
            if any(SOURCE_SUBJECT_KEY.match(l) for l in head):
                stat["已有 source_subject"] += 1
            if any(SUBJECT_MODULE_KEY.match(l) for l in head):
                stat["subject_module(应保持不变)"] += 1
            for l in head:
                m = TEACHING_KEY.match(l)
                if m:
                    v = l.split(":", 1)[1].strip().strip("\"'")
                    stat[f"teaching_level={v}"] += 1
                    if v not in LEVELS_4:
                        bad_levels[v] += 1
                if YEAR_KEY.match(l):
                    stat["有 year"] += 1

    for k, v in sorted(stat.items(), key=lambda x: (-x[1], x[0])):
        mark = ""
        if k == "残留 subject 键" and v:
            mark = "  ✗"
        print(f"  {k:34s} {v}{mark}")
    if bad_levels:
        print("\n  ✗ 不在 4 档内的 teaching_level：")
        for k, v in bad_levels.most_common():
            print(f"      {k}: {v}")
    else:
        print("\n  ✓ teaching_level 全部落在 4 档内")


if __name__ == "__main__":
    main()
