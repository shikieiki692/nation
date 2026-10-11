# -*- coding: utf-8 -*-
"""scan_header_noise.py —— 扫「机构名/页眉残留独占一行」（P2-11，**只读筛查**）。

背景：卷 XVI 实测 2 处缺陷同源 —— GChO 卷的**页眉**被 OCR 截断成「CHO」，作为**独占一行**
混进源卡答案区（CM-17-05 / CM-12-05）；第一轮综合套卷线汇智系 20+ 卡同病。
判据：**独占一行、内容恰为机构名或其截断形**（如 `CHO`/`GChO`/`chemy`/`汇智`…）⇒ 页眉/页脚残留。
⚠️ `CHO` 也可能是**醛基化学式**（合法内容）⇒ 只筛候选，**定性必须看上下文/回源**。
   本脚本按「卡的机构 = 该字样机构」加权：GChO 卡里的裸 `CHO/GChO` 行 ⇒ 高度可疑。
"""
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")
INSTS = ["化英社", "清北营", "chemy", "伽马", "壹尖培优", "汇智", "XeChem",
         "质心GChO", "质心UChO", "方圆", "一式", "北京夏令营", "2ChO"]
# 可能被截断的形态（页眉 OCR 常见：少首字符、大小写混合、仅保留后半）
TRUNC = {
    "GChO": ["CHO", "GChO", "ChO", "GCHO"],
    "chemy": ["chemy", "Chemy", "hemy", "he m y"],
    "XeChem": ["XeChem", "eChem", "XeChem", "xechem"],
    "质心UChO": ["UChO", "ChO"],
    "化英社": ["化英社", "英社"],
    "清北营": ["清北营", "北营"],
    "壹尖培优": ["壹尖培优", "尖培优"],
    "汇智": ["汇智", "智"],
}
BARE = re.compile(r"^\s*([A-Za-z\u4e00-\u9fff][A-Za-z\u4e00-\u9fff ]{0,8})\s*$")
# ★ 2026-10-11：判据放宽为「**任意**机构名/截断形」——本次根因正是**跨机构**页眉
#   （chemy 卡里混入 GChO 页眉「CHO」）；本机构命中=M，跨机构命中=X（更可疑）。
ALL_TOKENS = {}
for _i, _lst in TRUNC.items():
    for _t in _lst:
        ALL_TOKENS.setdefault(_t, set()).add(_i)
for _i in INSTS:
    ALL_TOKENS.setdefault(_i, set()).add(_i)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    cards = sorted(glob.glob(os.path.join(BASE, "*", "题-*.md")))
    total = 0
    per_card = []
    for p in cards:
        inst = os.path.basename(os.path.dirname(p))
        if only and only != inst:
            continue
        t = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
        i, j = t.find("## 题目"), t.find("## 参考答案")
        zones = [("题面", t[i:j] if j > i > 0 else t[i:]), ("答案", t[j:] if j > 0 else "")]
        hits = []
        for zname, z in zones:
            off = (i if zname == "题面" else j)
            for m in re.finditer(r"(?m)^[ \t]*(.{1,10}?)[ \t]*$", z):
                tok = m.group(1).strip()
                if not tok or "$" in tok or "|" in tok or tok.startswith(("#", ">", "!", "-", "*", "(", "（")):
                    continue
                if not BARE.fullmatch(tok):
                    continue
                if tok not in ALL_TOKENS:
                    continue
                owners = ALL_TOKENS[tok]
                rel = "M" if inst in owners else "X"      # M=本机构字样，X=跨机构字样（更可疑）
                ln = t[:off + m.start()].count("\n") + 1
                ls = t.split("\n")
                ctx = " / ".join(x.strip()[:36] for x in ls[max(0, ln - 3):ln + 2])
                hits.append((zname, ln, tok, rel, ctx))
        if hits:
            per_card.append((p, inst, hits))
            total += len(hits)
    print("扫描 %d 张机构卡 ｜ 候选 %d 处（%d 张卡）\n" % (len(cards), total, len(per_card)))
    for p, inst, hits in per_card:
        print("▸ [%s] %s" % (inst, os.path.basename(p)))
        for zname, ln, tok, rel, ctx in hits:
            print("    L%-5d [%s] %-6s 「%-8s」  上下文: %s" % (ln, rel, zname, tok, ctx))
    print("\n⚠️ 只筛候选：`CHO` 也可能是醛基化学式 —— 定性/修复前必须看上下文（必要时回源）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
