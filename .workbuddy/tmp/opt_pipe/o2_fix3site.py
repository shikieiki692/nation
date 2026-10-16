# -*- coding: utf-8 -*-
r"""O2 卷 md（两版）＋ 3 张源卡：三处缺陷修补。

① **内容丢失（图代文）**：卡 CM-207-09 的 9-2-3 选项与 9-2-4 题干被 mineru **误判为图**
   （图 `66dd98d1` 目检＝**该段文字本身的扫描块**）⇒ 卡与卷 md 均只剩 `…研究人员更改的氨` ＋ 图 ＋ `PrI。将…`。
   修法＝用 **L0 逐字文字**替换该图引用行（L0：`基酸残基主要位于何位置？` / `a) … b) … c) …` /
   `9-2-4 NNMT-36 不止可以…分别投入 EtI 和 n-`）。
② **OCR 页眉残渣误置 H2**：`## 奥林匹克` ＋ `'026年7`（源自 L0 页眉残渣）⇒ 整行删除。
③ **评分文字误置 H2**：`## (3 分, 结构 1 分, 手性位点一个 1 分)` ⇒ 去 `## ` 标记（照卷 X `md_patches` 先例）。
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Obsidion\妙妙屋")

IMG = "![[66dd98d19ef36b959a2d4926d73386cb07782f8da80d16b1f2af62ab97397810.jpg]]"
IMG2 = "![](images/66dd98d19ef36b959a2d4926d73386cb07782f8da80d16b1f2af62ab97397810.jpg)"

RESTORE = [
    "基酸残基主要位于何位置？",
    "",
    "a) 与吡唑衍生物结合区域　b) 与 SAM 结合区域　c) 蛋白质外围区域",
    "",
    "**3-2-4** NNMT-36 不止可以催化甲基化，还可以催化乙基化和丙基化反应，分别投入 EtI 和 n-",
]
JUNK = {"## 奥林匹克", "'026年7"}
H2BAD = "## (3 分, 结构 1 分, 手性位点一个 1 分)"
H2OK = "(3 分, 结构 1 分, 手性位点一个 1 分)"

VOL = "04-题库/初赛模拟卷O2（有机·%s版）.md"
K = "04-题库/2026机构初赛模拟题/"


def rd(p):
    with io.open(p, encoding="utf-8-sig", newline="") as fh:
        raw = fh.read()
    crlf = raw.count("\r\n")
    eol = "\r\n" if crlf * 2 > raw.count("\n") else "\n"
    return raw, eol, raw.replace("\r\n", "\n").split("\n")


def wr(p, lines, eol, raw):
    out = eol.join(lines)
    if out == raw:
        print("   (无变更)")
        return
    with io.open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)
    print("   写盘 %d → %d 字节" % (len(raw.encode("utf-8")), len(out.encode("utf-8"))))


def do_restore(p, tag):
    raw, eol, L = rd(p)
    idx = [i for i, l in enumerate(L) if l.strip() in (IMG, IMG2)]
    assert len(idx) == 1, "%s 图引用行计数 %d" % (tag, len(idx))
    i = idx[0]
    nxt = next((x.strip() for x in L[i + 1:] if x.strip()), "")
    assert nxt.startswith("PrI。将 MeI、EtI、n-PrI"), "%s 后继行异常: %r" % (tag, nxt[:40])
    prv = next((x.strip() for x in reversed(L[:i]) if x.strip()), "")
    assert prv.endswith("研究人员更改的氨"), "%s 前行异常: %r" % (tag, prv[-20:])
    L[i:i + 1] = RESTORE
    print("① [%s] L%d 图→文字（%d 行）" % (tag, i + 1, len(RESTORE)))
    wr(p, L, eol, raw)


def do_junk(p, tag):
    raw, eol, L = rd(p)
    keep, gone = [], []
    for l in L:
        if l.rstrip() in JUNK:
            gone.append(l.rstrip())
            continue
        keep.append(l)
    assert len(gone) == 2, "%s 垃圾行计数 %d %s" % (tag, len(gone), gone)
    print("② [%s] 删页眉残渣 2 行" % tag)
    wr(p, keep, eol, raw)


def do_dehead(p, tag):
    raw, eol, L = rd(p)
    idx = [i for i, l in enumerate(L) if l.rstrip() == H2BAD]
    assert len(idx) == 1, "%s 误置 H2 计数 %d" % (tag, len(idx))
    L[idx[0]] = H2OK
    print("③ [%s] L%d 去误置 H2" % (tag, idx[0] + 1))
    wr(p, L, eol, raw)


for v, kind in ((("学生", "学生"), ("答案", "答案"))):
    p = VOL % kind
    print("\n===== %s =====" % p)
    do_restore(p, kind)
    do_junk(p, kind)
    if kind == "答案":
        do_dehead(p, kind)

for p, tag in (
    (K + "chemy/题-CM-207-09-在药物分子中吡唑环是一个十分常见.md", "卡CM-207-09"),
    (K + "chemy/题-CM-17-08-烷烃构象中的取代基排斥不仅取.md", "卡CM-17-08"),
    (K + "化英社/题-HYS-40-09-23Wittig重排是一类重.md", "卡HYS-40-09"),
):
    print("\n===== %s =====" % tag)
    if "207-09" in p:
        do_restore(p, tag)
    if "17-08" in p:
        do_junk(p, tag)
    if "40-09" in p:
        do_dehead(p, tag)

print("\n===== 终检 =====")
for p in (VOL % "学生", VOL % "答案",
          K + "chemy/题-CM-207-09-在药物分子中吡唑环是一个十分常见.md",
          K + "chemy/题-CM-17-08-烷烃构象中的取代基排斥不仅取.md",
          K + "化英社/题-HYS-40-09-23Wittig重排是一类重.md"):
    t = io.open(p, encoding="utf-8-sig").read()
    print("  %-46s 66dd98d1=%d 奥林匹克=%d 误置H2=%d"
          % (os.path.basename(p)[:44], t.count("66dd98d1"),
             t.count("奥林匹克"), t.count(H2BAD)))
