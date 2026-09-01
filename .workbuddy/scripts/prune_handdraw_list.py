#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按 handdraw_verify.json 的结论，从 00-首页/活跃任务/图片剩余待手绘清单.md 里
精确摘除 STALE（源 md 已无该引用）与 GONE（源 md 文件 itself 已不存在）两类条目。

条目块结构（内容/原文两行可能缺失）：
    - **文件**: [[X.md]]
      - **内容**: ...
      - **原文**: `...`
    <空行>

安全设计：
  - 只按「起始行索引」整块删除，不做字符串替换，绝不误伤相邻条目
  - newline="" 原样读写，避免 LF/CRLF 换行符抖动造成整文件 diff
  - 先写 .bak，再写目标文件
"""
import json
import os
import re
import shutil

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.join(VAULT, ".workbuddy", "tmp")
LIST = os.path.join(VAULT, "00-首页", "活跃任务", "图片剩余待手绘清单.md")

RE_ENTRY = re.compile(r"^[ \t]*- \*\*文件\*\*: \[\[([^\]]+)\]\][ \t]*$")
RE_CONTENT = re.compile(r"^[ \t]*- \*\*内容\*\*: (.+?)[ \t]*$")
RE_IMG = re.compile(r"\[\[([^\]\|#\^]+?)\]\]")
RE_HASH = re.compile(r"[0-9a-f]{32,64}\.[a-z]{3,4}", re.I)


def key_of(src, content, raw):
    """条目的唯一标识：源文件名 + 图片 basename"""
    bn = ""
    for t in (raw, content):
        m = RE_IMG.findall(t or "")
        if m:
            bn = m[0].replace("\\", "/").split("/")[-1].strip()
            break
    if not bn:
        for t in (content, raw):
            m = RE_HASH.search(t or "")
            if m:
                bn = m.group(0)
                break
    return (src, bn)


def main():
    with open(os.path.join(TMP, "handdraw_verify.json"), encoding="utf-8") as f:
        v = json.load(f)

    drop_keys = set()
    for cat in ("STALE", "GONE"):
        for r in v[cat]:
            drop_keys.add((r["source"], r["basename"] or ""))
    print(f"待摘除条目: STALE {len(v['STALE'])} + GONE {len(v['GONE'])} = {len(drop_keys)}")

    with open(LIST, encoding="utf-8", newline="") as f:
        raw_text = f.read()
    lines = raw_text.split("\n")

    # 切块：每个 "- **文件**" 起，到下一个 "- **文件**" 或文件尾
    starts = [i for i, ln in enumerate(lines) if RE_ENTRY.match(ln)]
    blocks = []
    for n, s in enumerate(starts):
        e = starts[n + 1] if n + 1 < len(starts) else len(lines)
        src = RE_ENTRY.match(lines[s]).group(1)
        content = raw = ""
        for i in range(s + 1, e):
            m = RE_CONTENT.match(lines[i])
            if m:
                content = m.group(1)
            m2 = re.match(r"^[ \t]*- \*\*原文\*\*: `(.+?)`[ \t]*$", lines[i])
            if m2:
                raw = m2.group(1)
        blocks.append((s, e, src, content, raw))

    keep = []
    dropped = []
    for s, e, src, content, raw in blocks:
        k = key_of(src, content, raw)
        if k in drop_keys or (src, "") in drop_keys:
            dropped.append((s, e, src, k[1]))
        else:
            keep.append((s, e))

    print(f"实际匹配到并摘除: {len(dropped)} 块")
    for s, e, src, bn in dropped:
        print(f"  L{s+1}-{e}  {src[:44]}  {bn[:20]}")

    out_lines = []
    for s, e in keep:
        # 块尾的连续空行原样带上
        out_lines.extend(lines[s:e])

    # 收尾：去掉文件末尾多余空行，保证以单个换行结束
    while out_lines and out_lines[-1].strip() == "":
        out_lines.pop()

    shutil.copyfile(LIST, LIST + ".bak")
    with open(LIST, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(out_lines) + "\n")

    after = open(LIST, encoding="utf-8", newline="").read().split("\n")
    n_after = sum(1 for ln in after if RE_ENTRY.match(ln))
    print(f"\n条目数 {len(starts)} -> {n_after}")
    print(f"备份: {os.path.basename(LIST)}.bak")


if __name__ == "__main__":
    main()
