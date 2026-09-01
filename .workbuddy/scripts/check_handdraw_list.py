#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核对 00-首页/活跃任务/图片剩余待手绘清单.md 中「缺图 86 修复扫尾」条目，
按 Obsidian 的 basename 解析规则判断哪些其实已经不缺了。

Obsidian 规则：![[a/b/xx.jpg]] 只要全库任意位置存在名为 xx.jpg 的文件即可解析，
不看路径。所以「路径写错 / 哈希写错一位」但同名文件仍在书自带 _images 里的，属假缺图。
"""
import json
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.join(VAULT, ".workbuddy", "tmp")
LIST = os.path.join(VAULT, "00-首页", "活跃任务", "图片剩余待手绘清单.md")

RE_ENTRY = re.compile(r"^[ \t]*- \*\*文件\*\*: \[\[([^\]]+)\]\]\s*$")
RE_CONTENT = re.compile(r"^[ \t]*- \*\*内容\*\*: (.+?)\s*$")
RE_RAW = re.compile(r"^[ \t]*- \*\*原文\*\*: `(.+?)`\s*$")
RE_IMG = re.compile(r"\[\[([^\]\|#\^]+?)\]\]")


def main():
    with open(os.path.join(TMP, "img_basename_index.json"), encoding="utf-8") as f:
        index = json.load(f)

    with open(LIST, encoding="utf-8") as f:
        lines = f.read().split("\n")

    entries = []          # (文件行号, 源文件, 内容行号, 内容文本, 原文行号, 原文文本)
    cur = None
    for i, ln in enumerate(lines):
        m = RE_ENTRY.match(ln)
        if m:
            cur = {"file_line": i, "src": m.group(1), "content_line": None,
                   "content": "", "raw_line": None, "raw": ""}
            entries.append(cur)
            continue
        if cur is None:
            continue
        m = RE_CONTENT.match(ln)
        if m:
            cur["content_line"] = i
            cur["content"] = m.group(1)
            continue
        m = RE_RAW.match(ln)
        if m:
            cur["raw_line"] = i
            cur["raw"] = m.group(1)
            # 一条原文出现后，这条 entry 结束
            cur = None

    targets = [e for e in entries if "缺图 86 修复扫尾" in (e["content"] or "")]
    print(f"清单总条目 {len(entries)} 条；其中标「缺图 86 修复扫尾」{len(targets)} 条")

    resolved, still_missing = [], []
    for e in targets:
        imgs = RE_IMG.findall(e["raw"] or "")
        if not imgs:
            imgs = RE_IMG.findall(e["content"] or "")
        if not imgs:
            still_missing.append((e, None, "条目里没找到图片引用"))
            continue
        bn = imgs[0].replace("\\", "/").split("/")[-1].strip()
        where = index.get(bn)
        if where:
            resolved.append((e, bn, where))
        else:
            still_missing.append((e, bn, "全库同名文件不存在"))

    print(f"\n==== 已可解析（假缺图）{len(resolved)} 条 ====")
    for e, bn, where in resolved:
        print(f"  L{e['content_line']+1}: {bn}")
        print(f"        源文件: {e['src']}")
        print(f"        实际在: {where[0]}")
        if len(where) > 1:
            print(f"        （另有 {len(where)-1} 处同名副本）")

    print(f"\n==== 确实仍缺 {len(still_missing)} 条 ====")
    for e, bn, why in still_missing[:15]:
        print(f"  L{e['content_line']+1}: {bn or '(无引用)'}  —— {why}")
    if len(still_missing) > 15:
        print(f"  ... 其余 {len(still_missing)-15} 条略")

    out = {
        "resolved": [{"source": e["src"], "basename": bn,
                      "actual_path": where[0], "all_paths": where,
                      "content_line": e["content_line"], "raw_line": e["raw_line"],
                      "file_line": e["file_line"]}
                     for e, bn, where in resolved],
        "still_missing": [{"source": e["src"], "basename": bn, "why": why,
                           "content_line": e["content_line"], "raw_line": e["raw_line"],
                           "file_line": e["file_line"]}
                          for e, bn, why in still_missing],
    }
    with open(os.path.join(TMP, "handdraw_check.json"), "w", encoding="utf-8", newline="") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"\n明细已写入 .workbuddy/tmp/handdraw_check.json")


if __name__ == "__main__":
    main()
