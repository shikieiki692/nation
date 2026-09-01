# -*- coding: utf-8 -*-
"""
修复「子编号多了一级」的断链（第二批，10 处）。

与第一批的区别：
  第一批要求「剥掉一级后完全相等」，且只认不带路径的链接文本，
  因此带完整路径的写法（[[04-题库/真题/…/题-039-1-1-X]]）全部被跳过。
  本脚本按「原链接是否带目录」分别处理，保持原写法结构不变：
      带目录 → 换成 同目录/新名字
      不带   → 换成 新名字

安全约束（继承自第一批，均不可放宽）：
  1. 目标名形如 ^(题-\d+-\d+)-(\d+)-(.+)$（逐级剥离，最多剥到底）
  2. 剥离后的名字必须在全库【精确】存在同名 md
  3. 若原链接带目录，候选文件必须就在那个目录下
  4. 只替换精确写法，不做任何模糊匹配

【重要】表格内的别名分隔符必须保留转义形式 \|
  本库大量 wikilink 写在 Markdown 表格里，写成了 [[目标\|别名]]。
  这不是笔误 —— Obsidian 官方明确要求表格内转义管道符（否则 | 被当成
  列分隔符拆列表格），Live Preview 插入时也会自动转义；Obsidian 解析时
  会先把 \| 还原成 | 再交给 wikilink 规则。校验器 normalize_wikilink_target
  的 rstrip("/\\\\") 与之口径一致。
  因此替换时只换目标名，绝不把 \| 改成 |（那会拆坏表格）。
  全库共 505 处此类写法，均属正确，不在本次改动范围内。
"""
import os, re, json, shutil, collections

VAULT = r"C:\Obsidion\妙妙屋"
DATA = os.path.join(VAULT, r".workbuddy\tmp\broken_links2.json")

d = json.load(open(DATA, encoding="utf-8"))
todo = d["B_subnum"]

# 按源文件聚合
by_src = collections.defaultdict(list)
for r in todo:
    by_src[r["src"]].append(r)

done, skipped = 0, []
for src, recs in by_src.items():
    path = os.path.join(VAULT, src)
    if not os.path.exists(path):
        skipped.append((src, "源文件不存在"))
        continue
    text = open(path, encoding="utf-8").read()
    orig = text
    changed = []

    for r in recs:
        tgt = r["target"]
        new_name = r["new_name"]
        real = r["real"][0]

        # 决定替换后的写法
        if "/" in tgt:
            tgt_dir = tgt.rpartition("/")[0]
            new_tgt_dir = os.path.dirname(real).replace("\\", "/")
            if tgt_dir != new_tgt_dir:
                skipped.append((src, f"目录不一致 {tgt_dir} vs {new_tgt_dir}"))
                continue
            new_full = f"{new_tgt_dir}/{new_name}"
        else:
            new_full = new_name

        n = 0
        # 四种写法都要覆盖：无别名 / 普通别名 | / 表格转义别名 \|
        forms = [(f"[[{tgt}]]", f"[[{new_full}]]"),
                 (f"[[{tgt}|", f"[[{new_full}|"),
                 (f"[[{tgt}\\|", f"[[{new_full}\\|")]
        for old, new in forms:
            c = text.count(old)
            if c:
                text = text.replace(old, new)
                n += c
        if n:
            changed.append(f"{tgt} → {new_full} ({n})")
        else:
            skipped.append((src, f"未找到链接文本 [[{tgt}]]"))

    if text != orig:
        shutil.copyfile(path, path + ".bak")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        done += 1
        print(f"[{src}]")
        for c in changed:
            print(f"    {c}")

print(f"\n改写 {done} 个文件 / 跳过 {len(skipped)}")
for s, why in skipped:
    print(f"  [跳过] {s} — {why}")
