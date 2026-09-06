# -*- coding: utf-8 -*-
"""修复二分册题库 source_file 错指第1讲台账的问题（批45 教训第四犯）。"""
import os, re, sys

BASE = r"c:\Obsidion\妙妙屋\04-题库\教材习题\高中化学竞赛教程第二分册"
LEDGERS = {
    "L1": "习题-二分册-第1讲-化学反应速率与化学平衡",
    "L2": "习题-二分册-第2讲-电解质溶液和电离平衡",
    "L3": "习题-二分册-第3讲-难溶电解质的沉淀溶解平衡",
    "L4": "习题-二分册-第4讲-原电池及常见化学电源",
    "L5": "习题-二分册-第5讲-电解的原理及应用",
    "L6": "习题-二分册-第6讲-配位化学基础",
}

changed = {k: 0 for k in LEDGERS}
skipped = []
for fn in sorted(os.listdir(BASE)):
    if not (fn.startswith("题-") and fn.endswith(".md")):
        continue
    m = re.match(r"题-\d+-二分册-L([1-6])", fn)
    if not m:
        skipped.append(fn)
        continue
    lec = "L" + m.group(1)
    target = 'source_file: "[[07-资料提炼/习题提炼/%s]]"' % LEDGERS[lec]
    p = os.path.join(BASE, fn)
    with open(p, encoding="utf-8", newline="") as f:
        t = f.read()
    lines = t.split("\n")
    n_fm = 0
    hit = False
    for i, ln in enumerate(lines):
        if ln.strip() == "---":
            n_fm += 1
            if n_fm == 2:
                break
        if ln.startswith("source_file:"):
            if ln == target:
                hit = True
                break
            lines[i] = target
            hit = True
            changed[lec] += 1
            break
    if not hit:
        skipped.append(fn)
        continue
    nt = "\n".join(lines)
    assert len(nt.split("\n")) == len(lines), fn
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(nt)

print("replaced per lecture:", changed)
print("skipped(no source_file/no L-tag):", skipped)
