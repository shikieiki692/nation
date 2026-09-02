#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LLM 语义补全试点 · 报告合成器：meta + verdicts → 审计报告 md（只读样本文件，不碰题目）"""
import json
import re
from pathlib import Path
from collections import Counter

SC = Path(__file__).parent
REPORT = Path(r"C:\Obsidion\妙妙屋\09-审计报告\question_type-LLM补全试点-抽样判定报告-2026-09-02.md")

meta = json.loads((SC / "_pilot_meta.json").read_text(encoding="utf-8"))
verd = json.loads((SC / "_pilot_verdicts.json").read_text(encoding="utf-8"))

# 解析题面摘录（每条第一行非 ===== 的前 100 字，剥掉图片链接）
sample_txt = (SC / "_pilot_sample.txt").read_text(encoding="utf-8")
stems = {}
cur = None
for line in sample_txt.splitlines():
    m = re.match(r"===== \[#(\d+)\]", line)
    if m:
        cur = int(m.group(1))
        continue
    if cur is not None and line.strip() and line.strip() != "---":
        t = re.sub(r"!\[\[[^\]]*\]\]", "［图］", line).strip()
        if t and t != "［图］" and cur not in stems:
            stems[cur] = t[:100]
        if len(stems) == len(meta["sample"]):
            break

rows = []
label_ct = Counter()
empty_reason = Counter()
for s in meta["sample"]:
    v = verd[str(s["id"])]
    types = v["types"]
    if types:
        label_ct["+".join(types)] += 1
    else:
        w = v["why"]
        if "题组关联" in w:
            empty_reason["题组关联文件（题干在父文件）"] += 1
        elif "混合" in w or "混杂" in w:
            empty_reason["多问混合不同质（按铁律留空）"] += 1
        else:
            empty_reason["题面缺失/无设问（数据质量问题）"] += 1
    short = s["rel"].rsplit("/", 1)[-1].removesuffix(".md")
    rows.append((s["id"], s["group"].replace("04-题库/", "").replace("05-真题库", "05-真题库"),
                 short, " / ".join(types) if types else "（留空）", v["why"]))

n = len(rows)
n_write = sum(1 for r in rows if r[3] != "（留空）")
n_empty = n - n_write

lines = []
A = lines.append
A("# question_type · LLM 语义补全试点抽样判定报告")
A("")
A("> 2026-09-02 · 抽样器 `.workbuddy/scripts/llm_type_pilot.py`（seed=42，口径与 infer_question_type.py 完全一致）")
A("> 样本 = 无信号档（question_type 缺失且规则 infer() 零命中）分层抽样 **%d 条 / 77 组**；判定由 LLM 逐条读题面完成，本报告供人工核验精度。" % n)
A("")
A("## 一、总结果")
A("")
A("| 项 | 数值 |")
A("|---|---|")
A("| 样本量 | %d |" % n)
A("| LLM 判定写入 | **%d（%.1f%%）** |" % (n_write, n_write * 100.0 / n))
A("| 判定留空 | %d（%.1f%%） |" % (n_empty, n_empty * 100.0 / n))
A("")
A("**写入标签分布**（多标签以 + 连接）：")
A("")
A("| 标签 | 条数 |")
A("|---|---|")
for k, v in label_ct.most_common():
    A("| %s | %d |" % (k, v))
A("")
A("**留空原因分布**：")
A("")
A("| 原因 | 条数 |")
A("|---|---|")
for k, v in empty_reason.most_common():
    A("| %s | %d |" % (k, v))
A("")
A("## 二、关键发现（放量前必须处理的规则外问题）")
A("")
A("1. **图片选项选择题是规则法盲区**（#17/#18/#45）：选项是 Newman 投影式/结构图图片，题面无文字选项行——规则法永远命不中，LLM 补全的核心增量之一。")
A("2. **题面缺失/无设问 4 条**（#9 ABOC 仅标题、#11 汇智仅背景无设问、#20 上海中学截断、#112 经典例题空 stem）——**数据质量问题，不属于补全范围**，建议单独出清单人工修源。")
A("3. **05-真题库存在题组关联文件**（#120/#121/#122：正文仅「完整题干请见 [[父题]]」）——题干在父文件，**LLM 补全必须先解析父文件或直接排除**，否则会据「见上方讲评定位」乱判。按题号前缀折叠的既有规则处理。")
A("4. **多问混合不同质是留空主因（%d 条）**——与 B2b 铁律一致（不同质留空），LLM 也遵守；这部分是「补不动」的硬余量。" % empty_reason.get("多问混合不同质（按铁律留空）", 0))
A("")
A("## 三、放量预估")
A("")
A("- 无信号档 1,325 条 × 写入率 %.1f%% ≈ **%d 条可写**（但样本中题面缺失/题组关联约占 5.6%%，实际略低）。" % (n_write * 100.0 / n, round(1325 * n_write / n)))
A("- 覆盖率预估：1,757 + ~1,000 ≈ 2,760/4,182 ≈ **66%**；若再对 T3 弱信号档（362 条）做同款判定，理论上限 ~75%（多问混合是硬余量）。")
A("- 放量流程建议：先排除题组关联文件与题面缺失文件 → 按 77 组分批判定 → qt_write_guard 行尾门禁落盘 → 抽样复检。")
A("")
A("## 四、全量判定明细（%d 条，供抽查）" % n)
A("")
A("| # | 组 | 文件 | 判定 | 理由 |")
A("|---|---|---|---|---|")
for rid, grp, short, lab, why in rows:
    A("| %d | %s | %s | **%s** | %s |" % (rid, grp, short, lab, why))
A("")
A("> 核验方式：任取若干条，在 Obsidian 打开原文件对照「判定+理由」；建议重点抽查简答/推断/填空三类边界档。")
A("")

REPORT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
print("写入率: %d/%d = %.1f%%" % (n_write, n, n_write * 100.0 / n))
print("标签分布:", dict(label_ct.most_common()))
print("留空分布:", dict(empty_reason.most_common()))
print("报告:", REPORT)
