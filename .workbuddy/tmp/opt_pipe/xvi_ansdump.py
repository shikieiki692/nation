# -*- coding: utf-8 -*-
"""打印卷 md 全部题的答案区正文（剥图片引用、表格边框），供解析撰写。"""
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8")
V = sys.argv[1] if len(sys.argv) > 1 else "XVI"
t = io.open(r"04-题库/初赛模拟卷%s（非有机·答案版）.md" % V, encoding="utf-8-sig").read()
parts = re.split(r"(?m)^### ", t)
for seg in parts[1:]:
    lines = seg.split("\n")
    ai = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("#### 答案"):
            ai = i
            break
    if ai is None:
        continue
    body = "\n".join(lines[ai + 1:])
    body = re.sub(r"!\[\[[^\]]*\]\]", "[图]", body)
    body = re.sub(r"^\|[\s:\-|]*\|$", "", body, flags=re.M)
    body = re.sub(r"(?m)^\|", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    print("\n" + "#" * 72)
    print("## " + lines[0])
    print("#" * 72)
    print(body)
