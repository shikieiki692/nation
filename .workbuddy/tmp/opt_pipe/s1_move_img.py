# -*- coding: utf-8 -*-
"""S1 真缺陷修复·图引用搬移（答案区 → 题面区）。

用法：python s1_move_img.py [--apply]
判据/断言：
  · 目标图行在**答案区**唯一出现；题面锚点行唯一出现；图行紧邻一个空行；
  · 搬移后：题面图 +1、答案图 -1、**总图数不变**；CRLF 仍为 0。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")
IMG = re.compile(r"!\[\[|!\[\]\(|<img\b")

# (机构, 文件名, 题面锚点子串, 待搬图引用（唯一子串）, 备注)
MOVES = [
    ("chemy", "题-CM-65-06-6-1化学式为的化合物中含有.md",
     "6-2 富瓦烯(简记为Fv， 结构如右图)",
     "images/0cba57abff056853c4ccc25955b39b650d1b3240d61234f1366a8f19b3f21d7c.jpg",
     "题面「富瓦烯…结构如右图」；答案区 L72 图＝富瓦烯结构"),
]


def counts(t):
    ls = t.replace("\r\n", "\n").split("\n")
    qi = next(k for k, l in enumerate(ls) if l.startswith("## 题目"))
    ai = next(k for k, l in enumerate(ls) if l.startswith("## 参考答案"))
    q = "\n".join(ls[qi:ai]); a = "\n".join(ls[ai:])
    return len(IMG.findall(q)), len(IMG.findall(a))


def move(path, anchor_sub, img_sub, apply=False):
    t0 = open(path, encoding="utf-8-sig", newline="").read()
    assert "\r" not in t0, "CRLF 存在"
    q0, a0 = counts(t0)

    # 定位图行
    ls0 = t0.split("\n")
    il = [i for i, l in enumerate(ls0) if img_sub in l and l.strip().startswith(("!", "<img"))]
    al = [i for i, l in enumerate(ls0) if anchor_sub in l]
    assert len(il) == 1, "图行命中 %d" % len(il)
    assert len(al) == 1, "锚点命中 %d" % len(al)
    img_line = ls0[il[0]]
    anchor_line = ls0[al[0]]
    assert il[0] > al[0], "图须在题面锚点之后（答案区）"

    # ① 从答案区移除： "…\n\nIMG\n\n…" → "…\n\n…"（先做，避免二次匹配）
    pat_rm = "\n\n" + img_line + "\n"
    assert t0.count(pat_rm) == 1, "移除模式命中 %d" % t0.count(pat_rm)
    t1 = t0.replace(pat_rm, "\n")
    assert t1.count(img_sub) == 0, "移除后仍有残留"

    # ② 插入到题面锚点后： anchor\n\n → anchor\n\nIMG\n\n
    pat_in = anchor_line + "\n\n"
    assert t1.count(pat_in) == 1, "插入模式命中 %d" % t1.count(pat_in)
    t2 = t1.replace(pat_in, anchor_line + "\n\n" + img_line + "\n\n", 1)

    q1, a1 = counts(t2)
    assert (q1, a1) == (q0 + 1, a0 - 1), "图数不守恒：题面 %d→%d 答案 %d→%d" % (q0, q1, a0, a1)
    assert q1 + a1 == q0 + a0, "总图数变化"
    assert "\r" not in t2

    if apply:
        open(path, "w", encoding="utf-8", newline="").write(t2)
    return q0, a0, q1, a1, img_line


def main():
    apply = "--apply" in sys.argv
    for inst, name, anchor, imgsub, note in MOVES:
        p = os.path.join(BASE, inst, name)
        if not os.path.exists(p):
            print("!! 缺文件:", p); continue
        print("=" * 74)
        print("▸ %s" % name[:50])
        print("   备注: %s" % note)
        q0, a0, q1, a1, img = move(p, anchor, imgsub, apply=apply)
        print("   图数：题面 %d→%d ｜ 答案 %d→%d ✓" % (q0, q1, a0, a1))
        print("   待搬图行: %s" % img[:78])
        print("   %s" % ("【已写盘】" if apply else "（dry-run，未写盘）"))


if __name__ == "__main__":
    main()
