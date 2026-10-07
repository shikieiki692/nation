# -*- coding: utf-8 -*-
"""xiii_full.py —— 全量导出指定卡的题面+答案（不截断），供逐字核验。"""
import os
import re
import sys

ROOT = r"C:\Obsidion\妙妙屋"
IMG = re.compile(r"!\[\[([^\]\|]+)(?:\|[^\]]*)?\]\]|!\[[^\]]*\]\(([^)]+)\)")


def sect(txt, *names):
    ends = r"(?=^##[ \t]*(?:参考答案|答案|知识点映射)[ \t]*$|\Z)"
    if names[0] == "题目":
        ends = r"(?=^##[ \t]*(?:参考答案|答案)[ \t]*$|\Z)"
    for nm in names:
        m = re.search(r"^##[ \t]*" + nm + r"[ \t]*\n(.*?)" + ends, txt, re.S | re.M)
        if m:
            return m.group(1)
    return ""


out = []
for cp in sys.argv[1:]:
    p = cp if os.path.isabs(cp) else os.path.join(ROOT, cp)
    if not os.path.isfile(p):
        out.append("[MISS] " + cp)
        continue
    txt = open(p, encoding="utf-8-sig").read()
    fm = txt.split("---", 2)[1] if txt.startswith("---") else ""
    sf = re.search(r'^source_file:[ \t]*(.*)$', fm, re.M)
    q = sect(txt, "题目").strip()
    a = sect(txt, "参考答案", "答案").strip()
    out.append("#" * 100)
    out.append("### 卡: %s" % os.path.basename(p))
    out.append("### source_file: %s" % (sf.group(1).strip() if sf else ""))
    out.append("### 题面 %d 字 / 答案 %d 字" % (len(q), len(a)))
    out.append("---- 题面全文 ----")
    out.append(q)
    out.append("---- 答案全文 ----")
    out.append(a)
    out.append("")

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xiii_full.txt'),
     'w', encoding='utf-8', newline='\n').write("\n".join(out))
print("已写 xiii_full.txt：%d 卡" % (len(sys.argv) - 1))
