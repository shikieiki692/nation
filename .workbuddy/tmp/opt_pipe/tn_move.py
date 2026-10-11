# -*- coding: utf-8 -*-
"""吞图「真吞图」搬移（答案区 → 题面区）。dry-run 先行，--apply 写盘。

真吞图 6 张：QBY-02-04 / QBY-03-09 / CM-63-03 / CM-103-05 / CM-138-09 / HYS-03-04
断言：锚点在题面区唯一 / 图行在答案区唯一 / 图在锚点之后 / 题面图+ / 答案图- / 总图守恒 / 无 CRLF
"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")
IMG = re.compile(r"!\[\[|!\[\]\(|<img\b")

JOBS = [
    dict(inst="清北营", name="题-QBY-02-04-下图为实验室制备12二溴乙烷.md",
         anchor="下图为实验室制备1,2-二溴乙烷的装置图",
         img="images/31985c54cc08e65c59ba23756cb460785825d88f3a376b729430040b2099ef6f.jpg",
         note="题面「下图为…装置图」；搬答案区装置图(A~E)"),
    dict(inst="清北营", name="题-QBY-03-09-Ineleganolide最.md",
         anchor="研究者提出了一种更简洁高效的合成路线，如下图所示",
         img="images/accfec1b0406feec3723c8e5015f73b17f76c5afcfaa0c149a5dc1b8b2b0e528.jpg",
         note="题面「合成路线如下图所示」；搬答案区(+)-ineleganolide 全合成路线图"),
    dict(inst="chemy", name="题-CM-63-03-二氧化钛除金红石外还有多种晶.md",
         anchor="下图为锐钛矿的晶胞示意图",
         img="images/50a973e15d3a96b05e7ebb28c2ea4ecc91fcae3fe8968b040133d6feaa03f14a.jpg",
         note="题面「下图为锐钛矿的晶胞示意图」；搬答案区锐钛矿晶胞图【在池】"),
    dict(inst="chemy", name="题-CM-103-05-生物正交反应是在活细胞内进行.md",
         anchor="下图所示的 Ru 催化剂及其衍生物便是一种高效催化剂",
         img="images/dd1f6db675e19b4b803f1e17b2672227779d1aad115c6931e61318fedef29086.jpg",
         note="题面「下图所示的 Ru 催化剂」；搬答案区 Ru 催化循环图(含 ? 断点)"),
    dict(inst="chemy", name="题-CM-138-09-观察下图所示合成路线并回答后.md",
         anchor="观察下图所示合成路线并回答后面的问题",
         img="images/735ae652580b458f02cd42a37852d314e69a982da3214d9251d7debbe9897957.jpg",
         dels=[r"\begin{array}{l} \text {X}"],
         note="题面「观察下图所示合成路线」；搬答案区合成路线图 + 删题面破碎 math 垃圾"),
    dict(inst="化英社", name="题-HYS-03-04-甲烷单加氧酶MMO可在常温常.md",
         anchor="利用HL配体（结构如下图所示）",
         img="images/da13efecbea6b204c1b129ec74e21d3f917ce1ea2fe6977d01e1ef6d64df2f56.jpg",
         note="题面「HL配体（结构如下图所示）」；搬答案区 HL 配体结构图"),
]


def counts(t):
    ls = t.replace("\r\n", "\n").split("\n")
    qi = next(k for k, l in enumerate(ls) if l.startswith("## 题目"))
    ai = next(k for k, l in enumerate(ls) if l.startswith("## 参考答案"))
    return len(IMG.findall("\n".join(ls[qi:ai]))), len(IMG.findall("\n".join(ls[ai:])))


def idx(t):
    ls = t.replace("\r\n", "\n").split("\n")
    return (next(k for k, l in enumerate(ls) if l.startswith("## 题目")),
            next(k for k, l in enumerate(ls) if l.startswith("## 参考答案")), ls)


def do_move(t, anchor_sub, img_sub):
    """按行索引搬移：答案区图行 → 题面区锚点行后（各留一空行）。"""
    qi, ai, ls = idx(t)
    al = [i for i in range(qi, ai) if anchor_sub in ls[i]]
    assert len(al) == 1, "锚点在题面区命中 %d（%s）" % (len(al), anchor_sub[:36])
    il = [i for i in range(ai, len(ls)) if img_sub in ls[i]]
    assert len(il) == 1, "图行在答案区命中 %d（%s）" % (len(il), img_sub[:36])
    a, b = al[0], il[0]
    assert b > a, "图须在锚点之后"
    imgline = ls[b]
    del ls[b]                                   # 抽走答案区图行
    if 0 < b < len(ls) and ls[b] == "" and ls[b - 1] == "":
        del ls[b]                               # 折叠因抽走产生的双空行
    ls[a + 1:a + 1] = ["", imgline]             # 锚点后插「空行 + 图行」
    if a + 3 < len(ls) and ls[a + 2] == "" and ls[a + 3] == "":
        del ls[a + 3]                           # 折叠锚点后双空行
    return "\n".join(ls)


def do_del(t, sub):
    """删除含指定子串的整行（用于题面破碎 math 垃圾），并折叠双空行。"""
    ls = t.split("\n")
    il = [i for i, l in enumerate(ls) if sub in l]
    assert len(il) == 1, "删除行命中 %d（%s）" % (len(il), sub[:30])
    i = il[0]
    del ls[i]
    if 0 < i < len(ls) and ls[i] == "" and ls[i - 1] == "":
        del ls[i]
    return "\n".join(ls)


def main():
    apply = "--apply" in sys.argv
    for j in JOBS:
        p = os.path.join(BASE, j["inst"], j["name"])
        t0 = open(p, encoding="utf-8-sig", newline="").read()
        assert "\r" not in t0, "CRLF 存在：" + j["name"]
        q0, a0 = counts(t0)
        t = do_move(t0, j["anchor"], j["img"])
        for sub in j.get("dels", []):
            t = do_del(t, sub)
        q1, a1 = counts(t)
        assert q1 == q0 + 1, "题面图应 +1：%d→%d" % (q0, q1)
        assert a1 == a0 - 1, "答案图应 -1：%d→%d" % (a0, a1)
        assert q1 + a1 == q0 + a0, "总图数不守恒"
        assert "\r" not in t
        print("=" * 76)
        print("▸ %s / %s" % (j["inst"], j["name"][:50]))
        print("   %s" % j["note"])
        print("   题面图 %d→%d ｜ 答案图 %d→%d ｜ 守恒 %d ✓%s"
              % (q0, q1, a0, a1, q0 + a0, "  ＋删 %d 行" % len(j.get("dels", [])) if j.get("dels") else ""))
        if apply:
            open(p, "w", encoding="utf-8", newline="").write(t)
            print("   【已写盘】")
        else:
            print("   （dry-run）")


if __name__ == "__main__":
    main()
