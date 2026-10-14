# -*- coding: utf-8 -*-
r"""追加「重要更正」（报告/日志/memory）。"""
import io, os
os.chdir(r'C:\Obsidion\妙妙屋')
B = chr(92)

P = '09-审计报告/2026-10-14-双反斜杠修复与新缺陷类.md'
add = ("\n---\n\n## 六 ⚠️ 重要更正（2026-10-14 晚 · 自我纠错）\n\n"
       "本轮做完后我去核闸门实现，发现**前文两处结论是错的**，此处更正（原结论保留在上文以存真）：\n\n"
       "### 6.1 ❌「`" + B + "xrightarrow{…" + B + B + "…}` 是新缺陷类」——**错**\n\n"
       "管线 `build-all-handout-docx.py` **规则 4b6（L2129–2136）本就有针对性处理**：\n"
       "```python\n"
       "# 4b6) " + B + "xrightarrow{..." + B + B + "...} 的条件内换行改为分号（texmath 不支持 " + B + B + "）\n"
       "text = re.sub(r'(" + B + "xrightarrow(?:[" + B + "[" + B + "]""]*])?{)([^{}]*)(})', _fix_arrow_breaks, text)\n"
       "```\n"
       "⇒ 该形态**按设计**写成 `" + B + B + "`、由管线转成 `; `，**docx 从来不坏**。\n"
       "我据此扫描判出的 **10 处（`04-题库` 2 文件）＋ 5 处（成书层）全是虚警**。\n\n"
       "### 6.2 ❌「render_gate 抓不到它」——**错**\n\n"
       "用闸门**自身函数** `gate_docx()` 测**修复前**的 Cannizzaro 卡：\n\n"
       "| 指标 | 修复前 |\n|:--|--:|\n| `Could not convert TeX math` 失败数 | **21** |\n| 产物字面 `$` | **46** |\n| oMath | **0** |\n\n"
       "⇒ **闸门报得出来**，**没有盲区**、**无需补判据**。\n"
       "（我此前引用了 memory 里「texmath 原样输出、render_gate 多数不报错」——那是说 `" + B + "ce{}`/`" + B + "chemfig{}` 这类 chemmacros 宏，**被我过度外推**到了本轮情形。）\n\n"
       "### 6.3 ✅ 真正为真的部分（结论不变）\n\n"
       "该卡的 **29 处 `" + B + B + "mathrm` ＋ 1 处 `" + B + B + "qquad`** 是**真缺陷**：\n"
       "用**管线自身的 `_preprocess_markdown`** 处理修复前内容 → 残留 `" + B + B + "mathrm` **29**、`" + B + B + "qquad` **1**、**oMath = 0**（**整篇公式全废**）\n"
       "⇒ 修复**必要且正确**（修复后 oMath 22、可见文本 0 残留）。\n\n"
       "### 6.4 判据沉淀（修正版）\n\n"
       "1. 🔴 **判「texmath 是否放弃」必须走管线预处理**（`_preprocess_markdown`）**再渲染** —— 直跑 pandoc 会把**管线已自动处理**的情况误判为缺陷（本轮虚警 15 处的根因）。\n"
       "2. 🔴 管线**已知可自动处理**（勿再当缺陷）：`" + B + "xrightarrow/" + B + "xleftarrow` 参数内 `" + B + B + "`（4b6 →`; `）、`" + B + "atop`（4b9 →`" + B + "substack`）、`" + B + "AA`（4b3 →`" + B + "text{Å}`）、尺寸前缀 `" + B + "Big…`（4b4）、`" + B + "tag{}`（4b5）。\n"
       "3. 🔴 **扫 `" + B + B + "` 的排除清单**：`" + B + "begin{env}` 内、`" + B + "substack{}` 内、**`" + B + "xrightarrow{}` 参数内**、**FM 段**（`description` 不渲染）。\n"
       "4. 📌 **净收益**：本轮实得 ＝ **1 张卡 30 处真缺陷修复** ＋ **两轮判据修正**（假阳性 41→18→0）＋ 「闸门无盲区」的确认。\n")
d = io.open(P, encoding='utf-8', newline='').read()
io.open(P, 'w', encoding='utf-8', newline='').write(d.rstrip('\n') + '\n' + add)
print('report ok')

LOG = '00-首页/工作日志/2026-10-14.md'
addl = ("\n### ⚠️ 重要更正：新缺陷类大半是虚警；闸门无盲区\n\n"
        "- ❌ 更正①：**`" + B + "xrightarrow{…" + B + B + "…}` 不是缺陷** —— 管线 `build-all-handout-docx.py` **规则 4b6（L2129-2136）** 本就把它转成 `; `（texmath 不支持 `" + B + B + "`）⇒ docx 从不坏；我扫出的 10 处（`04-题库` 2 文件）＋5 处（成书层）**全是虚警**。\n"
        "- ❌ 更正②：**render_gate 没有盲区** —— 用闸门自身 `gate_docx()` 测修复前的卡 ⇒ **失败 21／字面$ 46／oMath 0**，**报得出来**；此前引 memory 的 `" + B + "ce{}` 盲区结论属**过度外推**。⇒ **无需补判据**。\n"
        "- ✅ 仍为真：该卡 **29 处 `" + B + B + "mathrm` ＋ 1 处 `" + B + B + "qquad`** 是**真缺陷**（管线自身预处理复现：oMath=0、公式全废）⇒ 修复必要；修复后 oMath 22、0 残留。\n"
        "- 🔴 **判据**：判 texmath 是否放弃**必须走 `_preprocess_markdown` 再渲染**（直跑 pandoc 会误判管线已处理的情况）；扫 `" + B + B + "` 的排除清单＝`" + B + "begin{}` 内／`" + B + "substack{}` 内／**`" + B + "xrightarrow{}` 参数内**／**FM 段**。\n")
d2 = io.open(LOG, encoding='utf-8', newline='').read()
io.open(LOG, 'w', encoding='utf-8', newline='').write(d2.rstrip('\n') + '\n' + addl)
print('worklog ok')

MEM = '.workbuddy/memory/2026-10-14.md'
addm = ("\n### 🔴🔴 更正：管线自带 `" + B + "xrightarrow` 换行处理；render_gate 无盲区（2026-10-14 续八）\n\n"
        "- 🔴🔴 **`" + B + "xrightarrow{…" + B + B + "…}` 不是缺陷**：`build-all-handout-docx.py` **规则 4b6（L2129-2136）** 专把参数内 `" + B + B + "` 转 `; `（texmath 不支持 `" + B + B + "`）⇒ **docx 从来不坏**。管线还自带：4b3 `" + B + "AA`→`" + B + "text{Å}`、4b4 尺寸前缀、4b5 `" + B + "tag{}`、4b9 `" + B + "atop`→`" + B + "substack`。**判缺陷前先查管线预处理**。\n"
        "- 🔴🔴 **判「texmath 是否放弃」必须走 `_preprocess_markdown` 再渲染**：直跑 pandoc 会把管线已自动处理的情况**误判为缺陷**（本轮 15 处虚警的根因）。\n"
        "- 🔴🔴 **render_gate 无盲区**：用其自身 `gate_docx()` 测修复前内容 ⇒ 失败 21／字面$ 46／oMath 0，**报得出来**。memory 里「texmath 原样输出、gate 不报错」是说 `" + B + "ce{}`/`" + B + "chemfig{}`（chemmacros）——**勿过度外推**。\n"
        "- 🔴 **扫 `" + B + B + "` 的排除清单**：`" + B + "begin{env}` 内｜`" + B + "substack{}` 内｜**`" + B + "xrightarrow{}` 参数内**｜**FM 段**。按此四排除，全库真残差 **0**。\n"
        "- ✅ 真缺陷（已修）：Cannizzaro 卡 **29 处 `" + B + B + "mathrm` ＋ 1 处 `" + B + B + "qquad`**（修复前 oMath=0＝整篇公式全废）。\n")
d3 = io.open(MEM, encoding='utf-8', newline='').read()
io.open(MEM, 'w', encoding='utf-8', newline='').write(d3.rstrip('\n') + '\n' + addm)
print('memory ok')
