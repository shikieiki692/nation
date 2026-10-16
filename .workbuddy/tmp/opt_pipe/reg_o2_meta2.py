# -*- coding: utf-8 -*-
r"""登记 O2 第四轮的三处修补进 vol_meta_O2.json::md_patches。"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
O = r"C:/Obsidion/妙妙屋/.workbuddy/tmp/opt_pipe"

ADD = [
    {
        "script": "o2_fix3site.py",
        "why": "**三处缺陷修补（卷两版＋3 张源卡同改）**："
               "① **内容丢失（图代文）**——卡 CM-207-09 的 9-2-3 选项与 9-2-4 题干被 mineru **误判为图**"
               "（图 `66dd98d1` 目检＝**该段文字本身的扫描块**：`基酸残基主要位于何位置？` ＋ `a)…b)…c)…` ＋ "
               "`9-2-4 NNMT-36 不止可以…分别投入 EtI 和 n-`）⇒ 卡与卷 md 均只剩 `…研究人员更改的氨` ＋ 图 ＋ `PrI。将…`。"
               "修法＝用 **L0 逐字文字**替换该图引用行。"
               "② **OCR 页眉残渣误置 H2**：`## 奥林匹克` ＋ `'026年7`（源自 L0 页眉残渣）⇒ 整行删除（卷两版＋卡 CM-17-08）。"
               "③ **评分文字误置 H2**：`## (3 分, 结构 1 分, 手性位点一个 1 分)` ⇒ 去 `## ` 标记"
               "（照卷 X `md_patches` 先例；卷答案版＋卡 HYS-40-09）。",
        "apply": "python .workbuddy/tmp/opt_pipe/o2_fix3site.py",
        "added": "2026-10-16",
    },
    {
        "script": "o2_q3_join.py",
        "why": "把上项恢复出的 Q3 文字**并回完整段落**（L0 原段落为单行）："
               "`**3-2-3** …研究人员更改的氨` ＋ `基酸残基主要位于何位置？` → 整句；"
               "`**3-2-4** …分别投入 EtI 和 n-` ＋ `PrI。将 …` → 整句（卷两版＋卡 CM-207-09）。",
        "apply": "python .workbuddy/tmp/opt_pipe/o2_q3_join.py",
        "added": "2026-10-16",
    },
]


def main():
    p = os.path.join(O, "vol_meta_O2.json")
    d = json.load(io.open(p, encoding="utf-8"))
    mp = d.setdefault("md_patches", [])
    have = {x.get("script") for x in mp}
    add = [x for x in ADD if x["script"] not in have]
    mp.extend(add)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=1))
    print("vol_meta_O2.json md_patches: +%d → 共 %d 项" % (len(add), len(mp)))
    for x in mp:
        print("   -", x["script"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
