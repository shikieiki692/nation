# -*- coding: utf-8 -*-
r"""追加：双反斜杠修复 + 新缺陷类（日志/memory）。用 chr(92) 防转义。"""
import io, os
os.chdir(r'C:\Obsidion\妙妙屋')
B = chr(92)

LOG = '00-首页/工作日志/2026-10-14.md'
addl = ("\n### 双反斜杠 `" + B + B + "mathrm` 修复 ＋ 新缺陷类\n\n"
        "- **存量定位**：`" + B + B + "mathrm`（双反斜杠）内容文件仅 **Cannizzaro 卡 29 处**（真缺陷）＋ `元文件/题库组卷隔离清单.md` 4 处（代码块示例，非缺陷）；"
        "其余 1,018 处在 `.workbuddy/` `09-AI工作区/` **笔记里**（是记录该模式的示例）。\n"
        "- ✅ **已修 1 文件/29 处**（`$" + B + B + "mathrm{D_2O}$` → `$" + B + "mathrm{D_2O}$`）；断言：2 反斜杠归零／3 不减／失败不写盘；该卡 `" + B + "begin{array}` 数 = 0 ⇒ 无一例外真缺陷。\n"
        "- 🆕 **新缺陷类**：`$$` 内**孤立 `" + B + B + "`**（不在数组/环境内）⇒ **texmath 放弃、整块原样打印 TeX**。最小复现：`$$ a=b" + B + B + "qquad c=d $$` ❌ vs `$$ a=b" + B + "qquad c=d $$` ✅ vs `array` 内 ✅。"
        "该卡 `$$…" + B + B + "qquad…$$` 已**拆成两个 `$$` 块** ⇒ 复验 docx 可见文本 `mathrm` **0 处**、oMath 22（拆前 20）。\n"
        "- **闸门**：FM strict True；`validate_kb` **0E/0W**；该卡**未被任何卷引用** ⇒ 无需重出卷。\n"
        "- 🆕 **全库扫描**（屏蔽所有环境）：**28 文件 / 41 个 `$$` 块 / 3 行内** 含残存 `" + B + B + "`；典型＝`" + B + "xrightarrow{1.;Et_2O" + B + B + "2.;H_3O^+}`。"
        "⚠️ **未修**（跨多线＋改法需逐例判＋`render_gate` 抓不到）⇒ 建议另立专项。\n"
        "- 报告＝`09-审计报告/2026-10-14-双反斜杠修复与新缺陷类.md`。\n")
d = io.open(LOG, encoding='utf-8', newline='').read()
io.open(LOG, 'w', encoding='utf-8', newline='').write(d.rstrip('\n') + '\n' + addl)
print('worklog ok')

MEM = '.workbuddy/memory/2026-10-14.md'
addm = ("\n### 🔴🔴 新缺陷类：`$$` 内孤立 `" + B + B + "` ⇒ texmath 放弃（2026-10-14 续六）\n\n"
        "- 🔴🔴 **判据**：`" + B + B + "`（换行）**只能出现在 `" + B + "begin{...}` 环境内**；在数组/环境外出现 ⇒ **texmath 放弃，整块原样打印 TeX**。"
        "实测：`$$ a=b" + B + B + "qquad c=d $$` ❌（unexpected control sequence）｜`" + B + "qquad` 单反斜杠 ✅｜`array` 内 `" + B + B + "` ✅。\n"
        "- 🔴 **`render_gate` 抓不到它**（texmath 原样输出多不报错）⇒ 长期盲区；**判据＝pandoc 转 docx 后查可见文本有无残留命令名**（如 `mathrm`）。\n"
        "- **规模**：屏蔽所有环境后全库仍 **28 文件 / 41 个 `$$` 块 / 3 行内**；典型 `" + B + "xrightarrow{1.;Et2O" + B + B + "2.;H3O^+}`。\n"
        "- ✅ **已修**：Cannizzaro 卡 29 处 `" + B + B + "mathrm` ＋ 1 处 `$$…" + B + B + "qquad…$$`（拆成两个 `$$` 块）；未入卷，无需重出。\n"
        "- 📌 **`" + B + B + "mathrm` 存量**：内容文件仅 Cannizzaro 卡 29（真缺陷）＋ 隔离清单 4（代码块示例）；其余在笔记里。\n")
d3 = io.open(MEM, encoding='utf-8', newline='').read()
io.open(MEM, 'w', encoding='utf-8', newline='').write(d3.rstrip('\n') + '\n' + addm)
print('memory ok')
