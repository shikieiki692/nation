#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_a_list.py —— A 类「内容不可用」108 张逐卡处置清单（含源文件指针）。"""
import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
OUT = os.path.join(R, "09-审计报告/2026-10-07-A类不可用题目处置清单.md")
rows = list(csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig")))
A = [r for r in rows if r["klass"] == "A"]

ACT = {
    "无答案/占位": "回源补答案（源卡答案区为空/仅注记）",
    "题面泄露": "换卡 或 回源重切（题面↔解答逐小问交错，不可机器手术）",
    "题面/答案过短": "回源补答案（答案区内容＝题面复制，清洗后为空）",
    "假结构式": "换卡（结构式被 OCR 成 ASCII 骨架，无法正则还原）",
}


def fm(p):
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    d = {}
    if t.startswith("---"):
        for l in t.split("---", 2)[1].split("\n"):
            m = re.match(r'^([a-z_]+):\s*"?(.*?)"?\s*$', l)
            if m:
                d[m.group(1)] = m.group(2)
    return d


order = ["无答案/占位", "题面泄露", "题面/答案过短", "假结构式"]
A.sort(key=lambda r: (order.index(r["reason"]) if r["reason"] in order else 9, r["inst"], r["path"]))
md = []
md.append("# A 类「内容不可用」题目处置清单（2026-10-07）\n")
md.append("> 范围：`04-题库/2026机构初赛模拟题`。来源＝`2026-10-07-不可组卷题目清单.csv` 中 `klass=A` 的 **%d** 张。\n"
          "> 这 %d 张**均已核实为源卡自身缺陷**，不是判据误杀（本会话已三修判据、共救回 133 张）。\n" % (len(A), len(A)))
md.append("\n## 处置原则\n")
md.append("- **回源补答案**：源卷/答案册里确有答案、只是没进卡 ⇒ 从 `source_file` 指向的源 MD/PDF 补录。\n")
md.append("- **换卡**：内容缺陷在源卡自身（切分错位、结构式乱码），重切成本 > 换卡 ⇒ 用同考点入池卡替代。\n")
md.append("- ⛔ 不建议对「题面↔解答交错」型做正则手术：13 张的混入形态各不相同（表格/文字行/评分行），易伤正文。\n")
md.append("\n### 证据：题面泄露 13 张的源侧**没有干净的题干/答案分区**\n")
md.append("13 张里 **7 张来自化英社同一份源**、**4 张来自伽马同一份源**，是**同一次缺陷**。查源后确认：\n")
md.append("- 化英社源 `…决赛夏季模拟试题2.md`（31 765 字）与 `…决赛夏季模拟试题2参考答案.md`（33 007 字）"
          "**结构几乎完全相同**（都从 `## …参考答案` 起、题号标题位置一一对应）⇒ 两份都是**整卷「题干＋解答」连续流**，"
          "并非「试题本＋答案本」。\n")
md.append("- 伽马源 `gamma晶体结构习题.pdf` 同为合订（第 N 题解答印在第 N+1 题所在页页首）。\n")
md.append("\n⇒ **重切无从下手**（题干与解答在源里逐小问交错，无分区锚点）⇒ 这 13 张以**换卡**为主。\n")

for k in order:
    sub = [r for r in A if r["reason"] == k]
    if not sub:
        continue
    md.append("\n## %s（%d 张）—— 建议：%s\n" % (k, len(sub), ACT.get(k, "—")))
    tb = ["| # | 机构 | 卡 | 源文件 | 备注 |", "|--:|:--|:--|:--|:--|"]
    for i, r in enumerate(sub, 1):
        p = os.path.join(R, r["path"])
        d = fm(p) if os.path.exists(p) else {}
        sf = d.get("source_file", "").replace("2026机构初赛模拟题/", "")
        tb.append("| %d | %s | `%s` | %s | %s |" % (i, r["inst"], os.path.basename(r["path"])[:46], sf[:52], r["verdict"]))
    md.append("\n".join(tb) + "\n")

md.append("\n## 附：本会话（2026-10-07）已救回的 133 张\n")
md.append("| 手段 | 张数 |\n|:--|--:|\n"
          "| 判据修正（占位闸／公式闸／越界引用闸／题面泄露标题闸／LEAK 锚定／手写词表） | 约 60 |\n"
          "| 回源补答案（GM-25 ×9＋GM-09 ×3） | 12 |\n"
          "| 题面泄露＝截断搬移（18）＋题头串入截断（9） | 27 |\n"
          "| 越界＝尾部截断（46）＋块删除（20） | 66 |\n")
md.append("\n⇒ 入池 **1518 → 1651**；A 类 **271 → 108**。\n")

open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")
print("已生成 %s（%d 行）" % (OUT, len(md)))
print("A 类 %d 张：%s" % (len(A), {k: sum(1 for r in A if r["reason"] == k) for k in order}))
