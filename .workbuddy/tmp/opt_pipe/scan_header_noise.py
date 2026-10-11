# -*- coding: utf-8 -*-
"""scan_header_noise.py —— 扫「机构名/页眉残留独占一行」（P2-11，**只读筛查**）。

背景：卷 XVI 实测 2 处缺陷同源 —— GChO 卷的**页眉**被 OCR 截断成「CHO」，作为**独占一行**
混进源卡答案区（CM-17-05 / CM-12-05）；第一轮综合套卷线汇智系 20+ 卡同病。
判据：**独占一行、内容恰为机构名或其截断形**（如 `CHO`/`GChO`/`chemy`/`汇智`…）⇒ 页眉/页脚残留。
⚠️ `CHO` 也可能是**醛基化学式**（合法内容）⇒ 只筛候选，**定性必须看上下文/回源**。
   本脚本按「卡的机构 = 该字样机构」加权：GChO 卡里的裸 `CHO/GChO` 行 ⇒ 高度可疑。
"""
import glob
import json
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


def scan_img_adjacent(p):
    """★ 规则 B（2026-10-11 新增）：**图邻散字** —— 独占一行的短 token（≤8 字符、无中文/无 $/无 |）
    且其 ±2 行内存在图片引用 ⇒ 高度疑似「图内标注被 OCR 抽成正文散字」（卷 XVI 的 CHO 即此类）。

    为什么单列此规则：源页的结构图里常有 CHO/TMS/OTIPS/CN/Ph 等**图示标注**，OCR 会把它当正文行。
    这类 token 多数情况下是**合法简写**，故本规则**只产候选**，定性一律回源目检。
    """
    t = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
    lines = t.split("\n")
    img_idx = [i for i, l in enumerate(lines) if "![[" in l or "![](" in l]
    hits = []
    for i, l in enumerate(lines):
        tok = l.strip()
        if not tok or len(tok) > 8:
            continue
        if any(ch in tok for ch in "$|#>*`[]（）()。，；："):
            continue
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]{0,7}", tok):
            continue
        near = [j for j in img_idx if abs(j - i) <= 2]
        if not near:
            continue
        hits.append((i + 1, tok, near[0] + 1))
    return hits


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    if "--img-adj" in sys.argv:
        # 范围：默认 = 各卷计划锁内的卡（已交付件才需要真缺陷判定）；--all 才全库
        if "--all" in sys.argv:
            cards = sorted(glob.glob(os.path.join(BASE, "*", "题-*.md")))
            scope = "全库 %d 张" % len(cards)
        else:
            cards, seen = [], set()
            for f in sorted(glob.glob(os.path.join(R, ".workbuddy/tmp/opt_pipe", "vol_plan_*.json"))):
                try:
                    d = json.load(open(f, encoding="utf-8"))
                except Exception:
                    continue
                for _m, lst in d:
                    for c in lst:
                        p = os.path.join(R, c["path"].replace("/", os.sep))
                        if p not in seen and os.path.exists(p):
                            seen.add(p)
                            cards.append(p)
            scope = "各卷计划锁内 %d 张（已交付）" % len(cards)
        print("扫描范围：%s\n" % scope)
        tot = 0
        for p in cards:
            hits = scan_img_adjacent(p)
            if hits:
                tot += len(hits)
                print("▸ [%s] %s" % (os.path.basename(os.path.dirname(p)), os.path.basename(p)[:44]))
                for ln, tok, imln in hits:
                    print("    L%-5d 「%-8s」 邻图行 L%d" % (ln, tok, imln))
        print("\n合计候选 %d 处 ｜ ⚠️ 只筛候选：多数 token 是合法简写，定性必须回源目检。" % tot)
        return 0

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
