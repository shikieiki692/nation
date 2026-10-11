# -*- coding: utf-8 -*-
"""S1 真缺陷修复·图引用搬移 v2（答案区 → 题面区；支持一卡多图 + 文本联动）。

用法：python s1_move2.py [--apply]
断言：图行唯一 / 锚点唯一 / 图在锚点之后 / 搬移后 题面图+1、答案图-1、总图数不变 / 无 CRLF。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")
IMG = re.compile(r"!\[\[|!\[\]\(|<img\b")

JOBS = [
    dict(inst="chemy", name="题-CM-65-06-6-1化学式为的化合物中含有.md",
         note="题面「富瓦烯…结构如右图」；搬答案区富瓦烯结构图",
         moves=[("6-2 富瓦烯(简记为Fv， 结构如右图)",
                 "images/0cba57abff056853c4ccc25955b39b650d1b3240d61234f1366a8f19b3f21d7c.jpg")]),
    dict(inst="chemy", name="题-CM-123-07-利用手性助剂可实现双键不对称.md",
         note="题面「机理如下图所示」；搬答案区 Halpern 1982 机理图",
         moves=[("不对称氢化的机理如下图所示",
                 "images/462ff0db69e90df02540ac70e45a1be78b1db88eb07ccb8f1bdc82cd41685182.jpg")]),
    dict(inst="XeChem", name="题-XeC-07-04-beginarraycmat.md",
         note="题面「如图 1 所示」＋答案引「由图 2 知」；搬两张滴定数据图",
         moves=[("4-1 为确定 CH+/B 的 $K_{s}$ ，进行了电化学测量，如图 1 所示",
                 "images/43490cb10ec1592c2d1d7808094bb4c532a96c8d7310c7e3976f58004ce5c151.jpg"),
                ("4-1 为确定 CH+/B 的 $K_{s}$ ，进行了电化学测量，如图 1 所示",
                 "images/b6d420c9c3026185aae4acb6ef0c262de49741502c37e29421e8ae729647d09d.jpg")]),
    dict(inst="chemy", name="题-CM-17-07-超分子自组装的选择性.md",
         note="题面「反应物 1、2、3 与 bipy」＋「PtLCl2」；搬表格(3 图)与 PtLCl2 图，并改指引句",
         moves=[("**7-1** 在丙酮-水混合体系中，将下图所示金属配合物反应物 1、2、3",
                 "<table><tr><td><img src=\"images/bd5937d78b0f60fd62c667146ce9fac3d4564d6944545ea150d18c24e2ebf4c8.jpg\"/>"),
                ("**7-2** 将下图所示配合物（可记为 $\\mathrm{PtLCl_2}$）",
                 "images/5cf575eba24a244eedf230a72ea3d5fab89dd8d792b8b91d455686a4c3771d2b.jpg")],
         text_edits=[("（反应物 1、2、3 与 bipy 的结构见下方参考答案中的表格）",
                      "（反应物 1、2、3 与 bipy 的结构如下图）")]),
]


def counts(t):
    ls = t.replace("\r\n", "\n").split("\n")
    qi = next(k for k, l in enumerate(ls) if l.startswith("## 题目"))
    ai = next(k for k, l in enumerate(ls) if l.startswith("## 参考答案"))
    return len(IMG.findall("\n".join(ls[qi:ai]))), len(IMG.findall("\n".join(ls[ai:])))


def do_move(t, anchor_sub, img_sub):
    ls = t.split("\n")
    il = [i for i, l in enumerate(ls) if img_sub in l]
    al = [i for i, l in enumerate(ls) if anchor_sub in l]
    assert len(il) == 1, "图行命中 %d（%s）" % (len(il), img_sub[:40])
    assert len(al) == 1, "锚点命中 %d（%s）" % (len(al), anchor_sub[:40])
    assert il[0] > al[0], "图须在锚点之后"
    line = ls[il[0]]
    anchor = ls[al[0]]
    pat_rm = "\n\n" + line + "\n"
    assert t.count(pat_rm) == 1, "移除模式命中 %d" % t.count(pat_rm)
    t = t.replace(pat_rm, "\n")
    assert t.count(img_sub) == 0, "移除后仍残留"
    pat_in = anchor + "\n\n"
    assert t.count(pat_in) == 1, "插入模式命中 %d" % t.count(pat_in)
    t = t.replace(pat_in, anchor + "\n\n" + line + "\n\n", 1)
    return t


def main():
    apply = "--apply" in sys.argv
    for j in JOBS:
        p = os.path.join(BASE, j["inst"], j["name"])
        t0 = open(p, encoding="utf-8-sig", newline="").read()
        assert "\r" not in t0, "CRLF 存在：" + j["name"]
        q0, a0 = counts(t0)
        t = t0
        for anchor, imgsub in j["moves"]:
            t = do_move(t, anchor, imgsub)
        for old, new in j.get("text_edits", []):
            assert t.count(old) == 1, "文本编辑命中 %d：%s" % (t.count(old), old[:30])
            t = t.replace(old, new)
        q1, a1 = counts(t)
        assert q1 > q0, "题面图未增加"
        assert a1 < a0, "答案图未减少"
        assert q1 + a1 == q0 + a0, "总图数不守恒：%d+%d != %d+%d" % (q0, a0, q1, a1)
        assert "\r" not in t
        print("=" * 74)
        print("▸ %s" % j["name"][:50])
        print("   备注: %s" % j["note"])
        print("   搬移 %d 行 ｜ 题面图 %d→%d ｜ 答案图 %d→%d ｜ 合计守恒 %d ✓"
              % (len(j["moves"]), q0, q1, a0, a1, q0 + a0))
        if apply:
            open(p, "w", encoding="utf-8", newline="").write(t)
            print("   【已写盘】")
        else:
            print("   （dry-run，未写盘）")


if __name__ == "__main__":
    main()
