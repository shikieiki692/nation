# -*- coding: utf-8 -*-
"""make_reject_report.py —— 由「不可组卷题目清单.csv」生成汇总报告 md。"""
import collections, csv, io, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
CSV = R + r"\09-审计报告\2026-10-07-不可组卷题目清单.csv"
OUT = R + r"\09-审计报告\2026-10-07-不可组卷题目清单.md"

rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
A = [r for r in rows if r["klass"] == "A"]
B = [r for r in rows if r["klass"] == "B"]
inn = [r for r in rows if r["verdict"] == "入池"]

# 修法建议（按原因）
FIX = {
    "无答案/占位": "**源确缺答案** ⇒ 不可修（除另找答案）；如源有答案而卡无 ⇒ 需回源补录",
    "越界（含他题内容）": "源卡答案串入下一题 ⇒ **换卡**即可（组卷层已过滤，源卡不动）",
    "题面泄露": "源卡**题面区混入答案**（题面长达 3000+ 字）⇒ 需按题界重切卡（成本高，建议换卡）",
    "答案公式未转录": "源答案的公式被 OCR 成了纯文字（公式全丢）⇒ 可**回源裁图**（同 GChO 方案）或重录",
    "题面/答案过短": "多为「答案＝题面回显」剥空 ⇒ 不可修，换卡",
    "假结构式": "`array` 结构式被压成 ASCII 骨架 ⇒ 需回源裁图",
    "题名泄露": "题名即讲稿口播 ⇒ 改题名或换卡",
    "手写稿口语/涂鸦": "手写稿 OCR 残留 ⇒ 裁图替换（同 GChO 方案）",
}

md = []
md.append("# 机构模拟题「不可组卷」清单与诊断（2026-10-07）\n")
md.append("> 范围：`04-题库/2026机构初赛模拟题`（13 机构，全量 %d 卡）。\n"
          "> 判据＝复刻组卷器 `build_org.py` 的**完整弃卡链**（同 `MYMEMO` 记载的 7 道闸）；"
          "本清单可直接用于「哪些题不能进卷、为什么」。\n" % len(rows))
md.append("> 逐卡明细：`09-审计报告/2026-10-07-不可组卷题目清单.csv`（%d 行）。\n" % len(rows))

md.append("\n---\n\n## 一、总览\n")
md.append("| 项 | 数量 | 占比 |")
md.append("|:--|--:|--:|")
md.append("| 全量卡 | %d | 100%% |" % len(rows))
md.append("| **可组卷（入池）** | **%d** | %.1f%% |" % (len(inn), 100.0 * len(inn) / len(rows)))
md.append("| 弃卡合计 | %d | %.1f%% |" % (len(A) + len(B), 100.0 * (len(A) + len(B)) / len(rows)))
md.append("| ├ A 类：**内容不可用** | **%d** | %.1f%% |" % (len(A), 100.0 * len(A) / len(rows)))
md.append("| └ B 类：口径外（模块/难度/年份等） | %d | %.1f%% |" % (len(B), 100.0 * len(B) / len(rows)))

md.append("\n## 二、A 类：内容不可用（%d 张）—— 按原因 × 机构\n" % len(A))
ca = collections.Counter(r["reason"] for r in A)
d = collections.defaultdict(collections.Counter)
for r in A:
    d[r["reason"]][r["inst"]] += 1
md.append("| 原因 | 张数 | 主要机构 | 可修性 |")
md.append("|:--|--:|:--|:--|")
for reason, n in ca.most_common():
    top = "、".join("%s %d" % (k, v) for k, v in d[reason].most_common(4))
    md.append("| %s | %d | %s | %s |" % (reason, n, top, FIX.get(reason, "—")))

md.append("\n## 三、B 类：口径外（%d 张）—— 属正常过滤\n" % len(B))
cb = collections.Counter(r["reason"] for r in B)
md.append("| 原因 | 张数 | 说明 |")
md.append("|:--|--:|:--|")
NOTE_B = {
    "非目标模块": "本卷只取「元素与分析／结构化学／化学原理」（有机另线）",
    "有机章节": "题源/标题判为有机章节",
    "题面含竞赛真题特征": "与历年国初真题高度重合 ⇒ 不入选模拟卷",
    "讲稿批次": "授课脚本（题面混讲解），非题目",
    "RISK 命中": "命中高风险特征词",
}
for reason, n in cb.most_common():
    md.append("| %s | %d | %s |" % (reason, n, NOTE_B.get(reason, "—")))

md.append("\n## 四、本轮修正：组卷器一处**误杀**（已修）\n")
md.append("`PLACEHOLDER` 占位闸原判据＝「答案含 `源卷答案`/`已随卡`/`答案出处` 等串 ⇒ 弃卡」，")
md.append("但它**不区分「注记行」与「实质解答」** ⇒ 把「出处注记 ＋ 长解答」的卡一并弃掉。")
md.append("实测 **11 张**被误弃（如 `题-HYS-03-05` 答案 **4904 字**、`题-HYS-40-05` **4013 字**）。\n")
md.append("**修正**：先剔除注记行（行首 `📎`/`⛔`/`📄`、含 `答案出处：`/`源 PDF`/`未逐字校对`/`文字层自动提取`），")
md.append("再看剩余实质是否 <25 字 ⇒ 才判无答案。\n")
md.append("**效果**：无答案 105 → **94**；入池 1512 → **1516**。\n")
md.append("修正后**新增入池 4 张**（另有 7 张转入「答案公式未转录」闸后仍弃）：\n")
md.append("| 卡 | 实质答案长 | 备注 |")
md.append("|:--|--:|:--|")
md.append("| `题-HYS-03-05-卡诺循环…` | 4078 | 答案完整 ✅ |")
md.append("| `题-HYS-40-05-卡诺循环…` | 3378 | 答案完整 ✅ |")
md.append("| `题-XeC-08-02-是一种典型的低价硅物种…` | 170 | ⚠️ 题面 `$`<10 未触发公式闸；答案的结构式似为图而图中缺 ⇒ **建议复核** |")
md.append("| `题-2ChO-05-05-本题的化学式要求用M表示…` | 179 | ⚠️ 答案零散（文字层提取残片）⇒ **建议复核** |")

md.append("\n## 五、优先处置建议\n")
md.append("1. **越界 66 张**：组卷层已自动过滤，**无需动源卡**；若要把它们救回池，走「换卡」。")
md.append("2. **答案公式未转录 52 张**：源答案的公式全丢 ⇒ 可用**回源裁图**法（本轮 GChO 方案可复用）批量救回。")
md.append("3. **题面泄露 52 张**：多为 chemy／化英社（题面区 3000+ 字）；建议**换卡**而非重切。")
md.append("4. **无答案/占位 94 张**：核实是否全部「源确缺答案」；其中若非源自缺 ⇒ 回源补录。")
md.append("5. 假结构式 1／题名泄露 1／手写稿涂鸦 1：单点修复。")

io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")
print("已生成 %s（%d 行）" % (OUT, len(md)))
