# -*- coding: utf-8 -*-
"""fix_xv_cards3.py —— 把「小问号紧贴汉字」拆开（如 `4-3-1给出`→`4-3-1 给出`），
使组卷期重编号（renumber2）能识别；不影响已带空格的标签与 H1 文件名。
用法: python -X utf8 fix_xv_cards3.py [--apply]
"""
import re
import shutil
import sys

APPLY = "--apply" in sys.argv
cards = [l.strip() for l in open(".workbuddy/tmp/opt_pipe/xv_cards.txt", encoding="utf-8") if l.strip()]

PAT = re.compile(r"(^|[。；;：:、\s])(\d{1,2}-\d{1,2}(?:-\d{1,2})?)(?=[\u4e00-\u9fa5])")


def fix_line(line):
    if line.startswith("# ") or line.startswith("title:") or line.startswith("aliases:"):
        return line
    return PAT.sub(lambda m: m.group(1) + m.group(2) + " ", line)


total = 0
for p in cards:
    t = open(p, encoding="utf-8-sig").read()
    lines = t.split("\n")
    new = [fix_line(l) for l in lines]
    if new == lines:
        continue
    n = sum(1 for a, b in zip(lines, new) if a != b)
    total += n
    print("  %-52s %d 行" % (p.split("/")[-1][:50], n))
    for a, b in zip(lines, new):
        if a != b:
            print("      %r → %r" % (a[:46], b[:46]))
    if APPLY:
        shutil.copy2(p, p + ".bak-xv3")
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(new))

print("共 %d 行待改；%s" % (total, "已写盘" if APPLY else "(dry)"))
