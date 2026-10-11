# -*- coding: utf-8 -*-
"""fix_header_noise.py —— 清理「图内标签被 OCR 抽成正文散字/页眉残留」的孤立 token 行。

已定性（2026-10-11 回源目检 chemy 模拟14答案 p14）：源页是**结构图**，图中含 CHO 等标注，
OCR 把图内文字抽成正文里的孤立 token 行（如「近似视作普通一级反应；\n\nCHO\n\n$$…」、
「…（1 分）\n\nCHO\n\nCp* 配体…」），**不是**页眉也不是正文用法 ⇒ 属噪音。
同类历史样本：CM-17-05 / CM-12-05 的裸「CHO」（已修）。

处理规则（保守，逐条断言）：
  R1 独占行且内容恰为 token ⇒ 整行连同其多余空行一起删（保留段落分隔）；
  R2 行首为「token + 空格 + 正文」⇒ 只剥掉行首 token（如「CHO 线性回归，有：…」）；
  R3 其余形态（token 嵌在公式/表格/图片语法里）⇒ **不动**，打印供人工判。

用法：python fix_header_noise.py [--dry]   # 默认 dry；--apply 才写盘
"""
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
TARGETS = [
    # (相对路径, token)
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-01-03-铝是地壳中含量第三高的元素在.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-01-06-氧化还原活性配体noninn.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-03-04-元素M因其元素符号而为人所知.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-04-07-71下图所示两个反应的产物不.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-04-09-炔丙醇在酸性条件下易于发生下.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-11-09-91胺的碱性与多种因素有关对.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-14-05-在高温下含有七并五环系的芳稠.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-14-06-硼和碳是周期表中唯二可形成大.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-16-07-氮杂环卡宾NHeterocy.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-16-10-2015年有课题组发现如下化.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-19-03-硅具有与碳类似但又有不同的成.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-19-06-61量子力学理论认为所有具有.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/chemy/题-CM-22-07-Phenytoin苯妥英是一.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/汇智/题-HZ-02-07-糠醛分子式为是一种常见的芳香.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/质心GChO/题-GChO-30-07-文艺复兴写出AF的结构简式不.md", "CHO"),
    ("04-题库/2026机构初赛模拟题/XeChem/题-XeC-19-09-PausonKhand反应简.md", "xechem"),
    ("04-题库/2026机构初赛模拟题/XeChem/题-XeC-20-09-上述整个过程便是生物素的生物.md", "xechem"),
]

DRY = "--dry" in sys.argv or "--apply" not in sys.argv


def fix(text, tok):
    """返回 (新文本, R1 删行数, R2 剥前缀数, R3 未处理清单)。"""
    lines = text.split("\n")
    out, r1, r2, r3 = [], 0, 0, []
    esc = re.escape(tok)
    for ln in lines:
        s = ln.strip()
        if s == tok:                                   # R1 独占行
            r1 += 1
            continue
        m = re.match(r"^([ \t]*)(%s)(\s+)(\S.*)$" % esc, ln)   # R2 行首 token + 空格 + 正文
        if m and not m.group(4).startswith(("|", "!", "#", ">", "-")):
            out.append(m.group(1) + m.group(4))
            r2 += 1
            print("        R2:", ln.strip()[:78])
            continue
        if re.search(r"\b%s\b" % esc, ln):              # R3 其他形态 → 人工判
            r3.append(ln.strip()[:70])
        out.append(ln)
    # 收敛连续空行（R1 删除后可能留下 3+ 连续空行）
    txt = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    return txt, r1, r2, r3


def main():
    total = [0, 0, 0]
    for rel, tok in TARGETS:
        p = os.path.join(R, rel)
        if not os.path.exists(p):
            print("!! 缺文件:", rel)
            continue
        t = open(p, encoding="utf-8-sig", newline="").read()
        t2, r1, r2, r3 = fix(t, tok)
        tag = "DRY " if DRY else "APPLY"
        print(f"[{tag}] {os.path.basename(rel)[:36]:<38} R1删行={r1} R2剥前缀={r2} R3待判={len(r3)}")
        for x in r3:
            print("        R3:", x)
        total[0] += r1
        total[1] += r2
        total[2] += len(r3)
        if not DRY:
            bakp = p + ".bak_noise"
            if not os.path.exists(bakp):
                shutil.copy2(p, bakp)
            open(p, "w", encoding="utf-8", newline="").write(t2)
    print(f"\n合计：R1 删行 {total[0]} ｜ R2 剥前缀 {total[1]} ｜ R3 待人工判 {total[2]}"
          + ("（DRY，未写盘）" if DRY else "（已写盘，原件备份 *.bak_noise）"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
