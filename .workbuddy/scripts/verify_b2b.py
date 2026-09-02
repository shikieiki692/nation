#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
B2b 写入校验：与写入前的 zip 快照逐行比对。

注意两点（B2a 踩过的坑）：
  1. git 有 `*.md text eol=lf` 归一化，所以不能拿 git diff 看行尾，必须与快照逐字节比。
  2. Path.read_text() 不接受 newline=，默认会把 CRLF 折叠成 LF，恰好抹掉要检测的
     行尾差异 —— 必须用 open(..., newline="")。
"""
import sys
import zipfile
from pathlib import Path
from collections import Counter
import difflib

ROOT = Path(r"C:\Obsidion\妙妙屋")
SNAP = sorted((ROOT / ".workbuddy/backups").glob("pre_b2b_*.zip"))[-1]

TARGET_DIRS = ["04-题库", "05-真题库"]
VOCAB = {"选择", "填空", "简答", "计算", "推断", "作图", "机理", "方程式书写", "推导", "例题", "综合"}


def read_raw(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def main() -> None:
    zf = zipfile.ZipFile(SNAP)
    names = [n for n in zf.namelist() if n.endswith(".md")]
    print(f"快照 {SNAP.name}：{len(names)} 个 md\n")

    stats = Counter()
    bad = []

    for name in names:
        try:
            old = zf.read(name).decode("utf-8")
        except Exception as e:
            stats["快照读取失败"] += 1
            bad.append((name, f"读取失败 {e}"))
            continue
        cur_p = ROOT / name
        if not cur_p.exists():
            stats["文件消失"] += 1
            bad.append((name, "文件消失"))
            continue
        new = read_raw(cur_p)
        if old == new:
            stats["未改动"] += 1
            continue
        stats["已改动"] += 1

        ol, nl = old.split("\n"), new.split("\n")
        sm = difflib.SequenceMatcher(None, ol, nl, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            if tag == "replace" and (i2 - i1) == (j2 - j1) == 1:
                o, n = ol[i1], nl[j1]
                if not o.startswith("question_type:"):
                    bad.append((name, f"非 question_type 行被改: {o[:60]!r} -> {n[:60]!r}"))
                    stats["非法替换"] += 1
                else:
                    stats["归一化替换"] += 1
                continue
            if tag == "insert":
                for j in range(j1, j2):
                    line = nl[j]
                    if not line.startswith("question_type:"):
                        bad.append((name, f"插入了非 question_type 行: {line[:60]!r}"))
                        stats["非法插入"] += 1
                        continue
                    stats["插入question_type"] += 1
                    # 行尾必须与邻居一致
                    neighbour = nl[j + 1] if j + 1 < len(nl) else (nl[j - 1] if j else "")
                    want_cr = neighbour.endswith("\r")
                    if line.endswith("\r") != want_cr:
                        bad.append((name, f"行尾风格与邻居不一致: {line[:60]!r}"))
                        stats["行尾不一致"] += 1
                continue
            bad.append((name, f"出现删除/多行替换 opcode={tag} {i1}:{i2}->{j1}:{j2}"))
            stats["删除或块替换"] += 1

    print("═══ diff 校验 ═══")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k:24s} {v}")

    print(f"\n═══ 异常 {len(bad)} 条 ═══")
    for name, msg in bad[:25]:
        print(f"  {name}\n      {msg}")

    # 落盘后的取值分布
    print("\n═══ question_type 取值分布（全库题目文件）═══")
    import yaml
    import re
    sys.path.insert(0, str(ROOT / "11-模板/scripts"))
    import validate_kb as V  # noqa: E402

    files = []
    for d in TARGET_DIRS:
        files.extend(sorted((ROOT / d).rglob("*.md")))
    files = [p for p in files if p.name not in V.EXCLUDE_FILE_NAMES]

    vals = Counter()
    n_missing = 0
    n_q = 0
    for p in files:
        t = read_raw(p)
        lines = t.split("\n")
        if not lines or lines[0].strip() != "---":
            continue
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is None:
            continue
        # 注意：不能用 `---\n` 字面量匹配，本库有 CRLF 文件，会整批漏掉
        try:
            fm = yaml.safe_load("\n".join(lines[1:end])) or {}
        except Exception:
            continue
        if not isinstance(fm, dict) or str(fm.get("type", "")).strip() != "题目":
            continue
        n_q += 1
        v = fm.get("question_type")
        if v is None or (isinstance(v, list) and not v):
            n_missing += 1
            continue
        items = v if isinstance(v, list) else [v]
        for x in items:
            vals[str(x).strip()] += 1

    print(f"  题目文件 {n_q}，仍缺 question_type {n_missing}（{n_missing / n_q:.1%}）")
    print(f"  已有标注 {n_q - n_missing}（{(n_q - n_missing) / n_q:.1%}）")
    for k, v in vals.most_common():
        flag = "" if k in VOCAB else "   <== 不在词表"
        print(f"    {k:12s} {v}{flag}")


if __name__ == "__main__":
    main()
