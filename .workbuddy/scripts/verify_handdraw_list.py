#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
逐条回溯 00-首页/活跃任务/图片剩余待手绘清单.md 里「缺图 86 修复扫尾」84 条：
到「文件」字段指向的源 md 里，看那条图片引用到底还在不在。

结论三类：
  STALE  —— 源 md 里已经没有这个引用了（多半已修好），清单条目可删
  ALIVE  —— 源 md 里仍在，且图确实不存在 -> 真缺图，必须保留
  GONE   —— 源 md 文件本身都找不到了 -> 条目悬空，可删（但先列出来人工过目）

另附：对每条做「全库近似文件名」检索（Hamming 距离 <=2）。
64 位十六进制串之间随机碰撞距离 <=2 的概率约 2e-67，所以一旦命中，
几乎可以确定是同一个文件的哈希被写错了一两位 —— 这类给 RECOVER 建议。
"""
import collections
import json
import os
import re

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.join(VAULT, ".workbuddy", "tmp")
LIST = os.path.join(VAULT, "00-首页", "活跃任务", "图片剩余待手绘清单.md")

SKIP = {".git", "node_modules", ".obsidian", "__pycache__"}


def build_md_index():
    idx = collections.defaultdict(list)
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in files:
            if f.endswith(".md"):
                idx[f].append(os.path.join(root, f))
    return idx


def main():
    with open(os.path.join(TMP, "img_basename_index.json"), encoding="utf-8") as f:
        imgidx = json.load(f)
    with open(os.path.join(TMP, "handdraw_check.json"), encoding="utf-8") as f:
        chk = json.load(f)

    print("建立 md 文件索引...")
    mdidx = build_md_index()

    buckets = collections.defaultdict(list)
    for k in imgidx:
        buckets[len(k)].append(k)

    res = {"STALE": [], "ALIVE": [], "GONE": []}
    for e in chk["still_missing"]:
        bn, src = e["basename"], e["source"]
        if not bn:
            res["GONE"].append(dict(e, why="条目内没有图片引用"))
            continue

        # 近似文件名检索
        cands = buckets.get(len(bn), [])
        near = sorted(((sum(a != b for a, b in zip(c, bn)), c) for c in cands),
                      key=lambda x: x[0])
        near = [x for x in near if x[0] <= 2]

        paths = mdidx.get(src, [])
        if not paths:
            res["GONE"].append(dict(e, near=near, why="源 md 文件不存在"))
            continue

        text = ""
        for p in paths:
            try:
                text += open(p, encoding="utf-8", errors="ignore").read() + "\n"
            except OSError:
                pass

        alive = bn in text
        rec = dict(e, md_path=os.path.relpath(paths[0], VAULT),
                   n_md=len(paths), near=near)
        res["ALIVE" if alive else "STALE"].append(rec)

    print(f"\n==== 逐条回溯结果（共 {sum(len(v) for v in res.values())} 条）====")
    for k in ("ALIVE", "STALE", "GONE"):
        print(f"  {k:6} {len(res[k]):3} 条")

    print(f"\n---- ALIVE 真缺图（源 md 里引用仍在）{len(res['ALIVE'])} 条 ----")
    for r in res["ALIVE"]:
        tag = f"  ★有近似(距{r['near'][0][0]})" if r["near"] else ""
        print(f"  {r['basename'][:22]}…  {r['source'][:44]}{tag}")

    print(f"\n---- STALE 已失效（源 md 里没这个引用了）{len(res['STALE'])} 条 ----")
    for r in res["STALE"]:
        print(f"  {r['basename'][:22]}…  {r['source'][:44]}")

    print(f"\n---- GONE 源 md 都找不到了 {len(res['GONE'])} 条 ----")
    for r in res["GONE"]:
        print(f"  {r['basename'][:22] if r['basename'] else '(无)'}…  {r['source'][:44]}  {r['why']}")

    rec = [r for r in res["ALIVE"] if r["near"]]
    print(f"\n---- 可修复建议：ALIVE 且有近似文件名 {len(rec)} 条 ----")
    for r in rec:
        d, c = r["near"][0]
        print(f"  {r['basename'][:20]}… -> {c[:20]}…  (距 {d}, 位于 {os.path.dirname(imgidx[c][0])})")

    with open(os.path.join(TMP, "handdraw_verify.json"), "w", encoding="utf-8", newline="") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(f"\n明细已写入 .workbuddy/tmp/handdraw_verify.json")


if __name__ == "__main__":
    main()
