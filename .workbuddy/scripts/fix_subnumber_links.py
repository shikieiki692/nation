#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复「多写一级子编号」导致的断链。

现象：md 里写 [[…/题-039-1-1-雄黄变铁与砒黄变铜]]，
      实际文件在【同一个目录】下，名字是 题-039-1-雄黄变铁与砒黄变铜.md。
      即：文件被删掉了一级子编号，但引用没跟着改。

安全规则（必须全部满足才改）：
  1. 目标名形如 题-<届>-<题号>-<子号>-<描述>
  2. 去掉「子号」那一级后，得到的名字【完全相等】于某个真实存在的 md
  3. 且该文件与引用所指路径【同目录】（说明就是它，不是同名的另一题）
  反例（会被规则挡下）：
      题-030-6-2-315K下N2O4NO2分压计算 -> 题-030-6-315K… 不存在，不改
      题-030-6-1-295K下N2O4NO2分压计算 -> 题-030-6-295K… 存在，可改
"""
import json
import os
import re

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.join(VAULT, ".workbuddy", "tmp")
SKIP = {".git", "node_modules", ".obsidian", "__pycache__"}

RE_SUB = re.compile(r"^(题-\d+-\d+)-(\d+)-(.+)$")


def main():
    with open(os.path.join(TMP, "broken_links.json"), encoding="utf-8") as f:
        bl = json.load(f)

    # 全库 md: stem -> [相对路径]
    stems = {}
    for root, dirs, fs in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for fn in fs:
            if fn.endswith(".md"):
                stem = fn[:-3]
                stems.setdefault(stem, []).append(
                    os.path.relpath(os.path.join(root, fn), VAULT))

    # 候选：目标名 + 引用它的文件
    targets = {}
    for src, t in bl["trulymissing"]:
        targets.setdefault(t, set()).add(src)

    plan = []
    for t, srcs in targets.items():
        stem = t.split("/")[-1]
        m = RE_SUB.match(stem)
        if not m:
            continue
        cand = f"{m.group(1)}-{m.group(3)}"
        if cand not in stems:
            continue
        # 同目录校验：引用路径里的目录部分必须与候选文件所在目录一致
        tdir = os.path.dirname(t).replace("/", os.sep)
        ok_paths = [p for p in stems[cand]
                    if os.path.dirname(p) == tdir or tdir == ""]
        if not ok_paths:
            continue
        plan.append((t, cand, sorted(srcs)))

    print(f"可安全改写 {len(plan)} 个目标，涉及 {sum(len(s) for _,_,s in plan)} 个源文件\n")

    done = skipped = 0
    for t, cand, srcs in sorted(plan, key=lambda x: -len(x[2])):
        print(f"  {t[:60]}")
        print(f"     -> [[{cand}]]")
        for src in srcs:
            p = os.path.join(VAULT, src.replace("/", os.sep))
            if not os.path.isfile(p):
                print(f"     [跳过] 源文件不存在 {src}")
                skipped += 1
                continue
            with open(p, encoding="utf-8", newline="") as f:
                text = f.read()
            a = f"[[{t}]]"
            b = f"[[{t}|"
            n = text.count(a) + text.count(b)
            if n == 0:
                print(f"     [跳过] 未找到链接文本 {src}")
                skipped += 1
                continue
            new = text.replace(a, f"[[{cand}]]").replace(b, f"[[{cand}|")
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(new)
            done += 1
            print(f"     已改 {n} 处  {os.path.basename(src)[:46]}")

    print(f"\n改写 {done} 个文件 / 跳过 {skipped} 个")


if __name__ == "__main__":
    main()
