# -*- coding: utf-8 -*-
r"""追加 T1 修复记录（日志/memory）。"""
import io, os
os.chdir(r'C:\Obsidion\妙妙屋')

LOG = '00-首页/工作日志/2026-10-14.md'
addl = '''
### T1 · chemy 域 D1/D2 修复（Å 误包 ＋ Δ 噪声）

- **规模**：D1 3卡/5处 ＋ D2 35卡/47处 ＝ 52 处；定性 **AUTO 28**（D1 5 ＋ D2 23）／**REVIEW 24**（多为合法 `\\Delta H/S/N_1`、`\\Delta\\phi/\\xi`、`\\xrightarrow[\\Delta]`）。
- ✅ **已修 AUTO 27 处 / 20 文件**（工具按**卡级安全策略**：卡内含任一 REVIEW 则整卡跳过，不半改）。典型：`\\mathrm { \\Delta NaCl }`→`\\mathrm{NaCl}`；`\\mathrm{\\mathring A}`→`\\text{Å}`；孤立 `\\mathrm { \\Delta }` 整体删。上下文抽验＝**Δ 确为 OCR 噪声**。
- 🔴 **过程事故（已纠正）**：工具第 82 行 `r'\\\\mathrm{%s}'`（raw string）产出**双反斜杠** ⇒ 已修工具本体（→ `r'\\mathrm{%s}'` ＋ `rstrip`→`strip`）。
  · 我为清理它写的 `\\\\mathrm` 正则**误伤合法的 `\\\\\\mathrm`（3 反斜杠＝ `\\\\` 数组换行 ＋ `\\mathrm`）**，把 3→2 ⇒ **`git checkout HEAD -- 04-题库` 全量还原后用修好的工具重跑**。
  · 🔴 **判据**：数「连续反斜杠段长」——1＝正常／2＝缺陷／**3＝合法**；正则须 `(?<!\\\\)\\\\\\\\(?!\\\\)`（恰好 2），**不可用 `\\\\\\\\`**。
- **复验**：2 反斜杠 **33→33（未污染）**、3 反斜杠 **112→112（合法形态完好）**；`validate_kb` **0E/0W**；FM strict **20/20**；**20 卡 ∩ 九卷计划 = 0 ⇒ 无需重出卷**。
- **遗留**：REVIEW 24（需逐条人工判）＋ AUTO 1（混合卡内）。🆕 **新发现**：HEAD 存量 **33 处 `\\\\mathrm`（2 反斜杠）**，疑同类缺陷，须先判是否在 `\\begin{array}` 内。
- 报告＝`09-审计报告/2026-10-14-T1-chemy-D1D2修复.md`。
'''
d = io.open(LOG, encoding='utf-8', newline='').read()
io.open(LOG, 'w', encoding='utf-8', newline='').write(d.rstrip('\n') + '\n\n' + addl)
print('worklog ok')

MEM = '.workbuddy/memory/2026-10-14.md'
addm = '''
### 🔴🔴 T1 chemy D1/D2 修复 ＋ 双反斜杠事故（2026-10-14 续五）

- **已修** AUTO 27 处/20 卡（D1 Å 5 ＋ D2 Δ 22）；REVIEW 24 保留（多为合法符号）。卡级安全策略＝**含 REVIEW 的卡整卡跳过**。**20 卡 ∩ 九卷计划 = 0 ⇒ 无卷受影响**。
- 🔴🔴 **`\\mathrm`（双反斜杠）＝LaTeX 缺陷**（`\\` 是换行符）；`fix_mathring_delta.py` 曾用 raw `r'\\\\mathrm{%s}'` 产出它 ⇒ **已修工具本体**。
- 🔴🔴 **`\\\mathrm`（3 反斜杠）＝合法**（`\\` 数组换行 ＋ `\mathrm`）——**切勿当缺陷清掉**！判据＝**数连续反斜杠长度**（1 正常／2 缺陷／3 合法）；正则须 `(?<!\\\\)\\\\\\\\(?!\\\\)`（**恰好 2**）；用 `\\\\\\\\` 会吃掉 3 里的 2 ⇒ 曾误伤、已 `git checkout HEAD -- 04-题库` 还原重做。
- 📌 **事故处置范式**：发现批量改写引入新缺陷时，**先 `git checkout HEAD -- <目录>` 全量还原（若该目录 HEAD 本就干净）**，再修工具、重跑、**用「基线计数」复验**（本次：2 反斜杠 33→33、3 反斜杠 112→112）。
- 🆕 **待评估**：HEAD 存量 **33 处 `\\mathrm`（2 反斜杠）** —— 判其是否位于 `\\begin{array}` 内（在内则 `\\` 合法）。
'''
d3 = io.open(MEM, encoding='utf-8', newline='').read()
io.open(MEM, 'w', encoding='utf-8', newline='').write(d3.rstrip('\n') + '\n' + addm)
print('memory ok')
