#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复「提炼-Clayden-第NN章」系列笔记里的哈希抄写错误。

诊断依据（三重，缺一不可）：
  1. 两个 64 位十六进制串的汉明距离只有 1~2。不同内容产生的哈希会有一半左右
     的位翻转，字符差异应在 30 位上下；距离 1~2 在随机情况下概率约 2e-67。
  2. 正确哈希对应的文件真实存在于原书 OCR 的 _images 目录里。
  3. 正确哈希出现在该书的 OCR 母本 md（Clayden中文版_XXX.md）中 —— 母本是权威记录，
     说明是衍生笔记转抄时写错，而非母本记错。

只做「错误哈希串 -> 正确哈希串」的整串替换，不做任何模糊改写。
每处替换后立刻校验新 basename 在全库可解析，否则回滚该文件并中止。
"""
import json
import os
import shutil

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.join(VAULT, ".workbuddy", "tmp")
SKIP = {".git", "node_modules", ".obsidian", "__pycache__"}


def build_md_index():
    idx = {}
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in files:
            if f.endswith(".md"):
                idx.setdefault(f, []).append(os.path.join(root, f))
    return idx


def main():
    with open(os.path.join(TMP, "img_basename_index.json"), encoding="utf-8") as f:
        imgidx = json.load(f)
    with open(os.path.join(TMP, "handdraw_verify.json"), encoding="utf-8") as f:
        v = json.load(f)

    # 去重：同一 (源文件, 错哈希) 只处理一次
    pairs = []
    seen = set()
    for r in v["ALIVE"]:
        if not r["near"]:
            continue
        dist, correct = r["near"][0]
        key = (r["source"], r["basename"])
        if key in seen:
            continue
        seen.add(key)
        pairs.append((r["source"], r["basename"], correct, dist))

    print("建立 md 索引...")
    mdidx = build_md_index()

    ok = fail = 0
    for src, wrong, correct, dist in pairs:
        paths = mdidx.get(src, [])
        if not paths:
            print(f"  [跳过] 找不到源文件 {src}")
            fail += 1
            continue
        wrong_stem = wrong.rsplit(".", 1)[0]
        correct_stem = correct.rsplit(".", 1)[0]
        if correct not in imgidx:
            print(f"  [中止] 正确文件在索引里查不到: {correct}")
            fail += 1
            continue

        for p in paths:
            with open(p, encoding="utf-8", newline="") as f:
                text = f.read()
            n = text.count(wrong_stem)
            if n == 0:
                continue
            new_text = text.replace(wrong_stem, correct_stem)
            # 校验：替换后每个新 basename 都可解析
            bad = [b for b in {correct} if b not in imgidx]
            if bad:
                print(f"  [中止] {os.path.relpath(p, VAULT)} 替换后仍不可解析")
                fail += 1
                continue
            shutil.copyfile(p, p + ".bak")
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(new_text)
            ok += 1
            print(f"  [修复] {os.path.relpath(p, VAULT)}")
            print(f"         {wrong_stem[:20]}… -> {correct_stem[:20]}…  (距{dist}, 替换 {n} 处)")

    print(f"\n修复 {ok} 个文件 / 失败 {fail} 个")


if __name__ == "__main__":
    main()
