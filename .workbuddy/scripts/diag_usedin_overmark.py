# -*- coding: utf-8 -*-
"""诊断：结构化学阶段测试卷 used_in 多标——形态分布 + 并行冲突交集。"""
import os, re, collections
from datetime import datetime

VAULT = r"C:\Obsidion\妙妙屋"
WIKI_NAME = "结构化学阶段测试卷"
bn = lambda x: x.replace("\\", "/").split("/")[-1].removesuffix(".md")

files = []
for root in ("04-题库", "05-真题库"):
    for dp, dn, fn in os.walk(os.path.join(VAULT, root)):
        for f in fn:
            if f.endswith(".md"):
                p = os.path.join(dp, f)
                t = open(p, encoding="utf-8", newline="").read(4000)
                if re.search(r"^used_in:.*" + WIKI_NAME, t, re.M):
                    files.append(p)

t = open(os.path.join(VAULT, "04-题库", WIKI_NAME + ".md"), encoding="utf-8", newline="").read()
inlinks = {bn(l) for l in re.findall(r"\[\[([^\]\|#]+)", t)
           if "测试卷" not in l and "工作台" not in l}
targets = [p for p in files if bn(p) not in inlinks]
print("多标文件数:", len(targets))

shape = collections.Counter()
for p in targets:
    t = open(p, encoding="utf-8", newline="").read(4000)
    m = re.search(r"^used_in:[^\n]*$", t, re.M)
    line = m.group(0) if m else ""
    if re.match(r"^used_in:\s*\[", line):
        shape["inline_list"] += 1
    elif re.match(r'^used_in:\s*"?\[\[', line):
        shape["scalar"] += 1
    elif re.match(r"^used_in:\s*$", line):
        shape["block_list"] += 1
    else:
        shape["other:" + line[:50]] += 1
for k, v in shape.most_common():
    print(" ", k, v)

recent = [p for p in targets
          if datetime.fromtimestamp(os.path.getmtime(p)) >= datetime(2026, 9, 3)]
print("其中 09-03 被改过的（另一对话现场，需跳过）:", len(recent))
for p in recent[:8]:
    print("  ", p)
