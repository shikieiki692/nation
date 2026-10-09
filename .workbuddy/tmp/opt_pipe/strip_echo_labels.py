# -*- coding: utf-8 -*-
"""strip_echo_labels.py —— 卷 md「答案区回显行」清理（dry/--apply）。

判据：在「#### 答案」区内，若某行以标签 L（`N-k`/`N-k-j`，允许 `**` 包裹）开头，
      且其下一条非空行也以同一标签开头 ⇒ 该行是「回显行」⇒ 删除。
（源：《一式/长沙/化英社/chemy》等机构「参考答案稿」把题干逐问抄进答案区，
  `volpost --ans` 会把它们转成裸标签或原样保留，交付件里表现为标签重复。）
"""
import re
import shutil
import sys

V = sys.argv[1] if len(sys.argv) > 1 else "XV"
APPLY = "--apply" in sys.argv
p = f"04-题库/初赛模拟卷{V}（非有机·答案版）.md"

LAB = re.compile(r"^[ \t]*(?:\*\*)?(\d{1,2}(?:-\d{1,2}){1,3})(?:\*\*)?[ \t]*(?=$|[^\d])")


def strip(t):
    i = t.find("#### 答案")
    if i < 0:
        return t, []
    head, seg = t[:i], t[i:]
    lines = seg.split("\n")
    out, removed = [], []
    for n, l in enumerate(lines):
        m = LAB.match(l)
        if m:
            nxt = ""
            for x in lines[n + 1:]:
                if x.strip():
                    nxt = x
                    break
            m2 = LAB.match(nxt)
            bare = re.fullmatch(r"[ \t]*\*\*\d{1,2}-\d{1,2}(?:-\d{1,2})?\*\*[ \t]*", l)
            # ① 同标签重复（L 开头 + 下一非空行也是 L）
            same = bool(m2) and m2.group(1) == m.group(1)
            # ② 裸标签（无正文）后紧跟另一个标签行 ⇒ 孤立回显标签
            orphan = bool(bare) and bool(m2)
            if same or orphan:
                removed.append((m.group(1), ("同标签" if same else "孤立"), l.strip()[:58]))
                continue
        out.append(l)
    return head + "\n".join(out), removed


t = open(p, encoding="utf-8-sig").read()
t2, removed = strip(t)
print("卷 %s：删回显行 %d 处" % (V, len(removed)))
for lab, why, s in removed:
    print("   [%s/%s] %r" % (lab, why, s))
print("字数 %d → %d" % (len(t), len(t2)))
if APPLY and removed:
    shutil.copy2(p, p + ".bak-echo")
    open(p, "w", encoding="utf-8", newline="\n").write(t2)
    print("已写盘")
elif not APPLY:
    print("(dry)")
