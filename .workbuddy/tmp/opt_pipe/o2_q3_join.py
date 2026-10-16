# -*- coding: utf-8 -*-
r"""把 Q3 恢复出来的文字**并回完整段落**（L0 原段落为单行）。

现状（上一步恢复后）：
  `**3-2-3** …研究人员更改的氨` / `基酸残基主要位于何位置？` / `a) …` /
  `**3-2-4** …分别投入 EtI 和 n-` / `PrI。将 …`
目标：
  `**3-2-3** …研究人员更改的氨基酸残基主要位于何位置？` / `a) …` /
  `**3-2-4** …分别投入 EtI 和 n-PrI。将 …`
（＝与 L0 正文逐字一致）
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Obsidion\妙妙屋")

VOL = "04-题库/初赛模拟卷O2（有机·%s版）.md"
CARD = "04-题库/2026机构初赛模拟题/chemy/题-CM-207-09-在药物分子中吡唑环是一个十分常见.md"
TAIL1 = "基酸残基主要位于何位置？"
HEAD2 = "NNMT-36 不止可以催化甲基化"
TAIL2 = "PrI。将 MeI、EtI、n-PrI 的反应速率从小到大排序。"


def patch(p, tag):
    with io.open(p, encoding="utf-8-sig", newline="") as fh:
        raw = fh.read()
    crlf = raw.count("\r\n")
    eol = "\r\n" if crlf * 2 > raw.count("\n") else "\n"
    L = raw.replace("\r\n", "\n").split("\n")

    # ① 首段并尾
    a = [i for i, l in enumerate(L) if l.strip().endswith("研究人员更改的氨")]
    assert len(a) == 1, "%s 首段计数 %d" % (tag, len(a))
    i = a[0]
    b = next(j for j in range(i + 1, len(L)) if L[j].strip())
    assert L[b].strip() == TAIL1, "%s 首段后继异常: %r" % (tag, L[b].strip())
    L[i] = L[i].rstrip() + TAIL1
    del L[b]

    # ② 次段并尾
    c = [k for k, l in enumerate(L) if HEAD2 in l and l.lstrip().startswith("**")]
    assert len(c) == 1, "%s 次段计数 %d" % (tag, len(c))
    k = c[0]
    assert L[k].rstrip().endswith("和 n-"), "%s 次段尾异常: %r" % (tag, L[k][-14:])
    d = next(j for j in range(k + 1, len(L)) if L[j].strip())
    assert L[d].strip() == TAIL2, "%s 次段后继异常: %r" % (tag, L[d].strip())
    L[k] = L[k].rstrip() + TAIL2
    del L[d]

    with io.open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(eol.join(L))
    print("  [%s] 并段完成；%d → %d 字节" % (tag, len(raw.encode("utf-8")), len(eol.join(L).encode("utf-8"))))


for k in ("学生", "答案"):
    p = VOL % k
    print("===== %s =====" % p)
    patch(p, k)
print("===== 卡 CM-207-09 =====")
patch(CARD, "卡")

print("\n===== 复核（两版须逐字同）=====")
for k in ("学生", "答案"):
    L = io.open(VOL % k, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")
    i = [j for j, l in enumerate(L) if "研究人员更改的氨" in l][0]
    print("##### %s版" % k)
    for j in range(i, i + 6):
        if L[j].strip():
            print("   | %s" % L[j][:170])
