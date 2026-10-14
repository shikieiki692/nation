# -*- coding: utf-8 -*-
r"""追加：提交路径收集口径的教训（日志/memory）。"""
import io, os
os.chdir(r'C:\Obsidion\妙妙屋')

LOG = '00-首页/工作日志/2026-10-14.md'
addl = ("\n### ⚠️ 操作失误与改进：提交路径不得用「全目录 status」\n\n"
        "- **失误**：提交 T1 余项时，我用 `git status --short 04-题库` 收集路径 ⇒ **误纳并行会话的新未跟踪文件** "
        "`chemy/_图片形态治理清单-2026-10-14.json`（本笔从 19 文件涨到 20、+30173 行）。\n"
        "- **处置**：该笔**未推送** ⇒ `git rm --cached <该文件>` ＋ `git commit --amend --no-edit` 摘除；"
        "该文件**恢复为未跟踪**（并行会话原状）；复核本笔恰好 19 文件。\n"
        "- 🔴 **改进判据**：**提交路径必须来自「本次实际改动的文件清单」**（如 `fix_*.py` 里显式列出的 12 卡 ＋ 文档 ＋ 工具），"
        "**不得**用「目录级 status」——目录里可能混着并行会话的未跟踪/未提交文件。\n"
        "- 教训同 `do_commit_t1.py` 的 `st.strip()` 坑：**路径收集是最易出错的一环**，每笔必核「文件数 ＋ 文件名单」。\n")
d = io.open(LOG, encoding='utf-8', newline='').read()
io.open(LOG, 'w', encoding='utf-8', newline='').write(d.rstrip('\n') + '\n' + addl)
print('worklog ok')

MEM = '.workbuddy/memory/2026-10-14.md'
addm = ("\n### 🔴 提交路径收集口径（2026-10-14 续十，血泪）\n\n"
        "- 🔴🔴 **提交路径不得用「目录级 `git status`」**：会**吃进并行会话的未跟踪/未提交文件**（本轮误纳 `chemy/_图片形态治理清单-2026-10-14.json`，本笔 +30173 行）。"
        "**正解＝用「本次实际改动的文件清单」**（脚本里显式列出）。\n"
        "- 🔴 **未推送的误纳可 `git rm --cached <f>` ＋ `git commit --amend --no-edit` 摘除**（文件恢复未跟踪＝并行会话原状）；已推送则只能新提交。\n"
        "- 🔴 **每笔提交后必核「文件数 ＋ 文件名单」**（`git show --stat --name-only HEAD`），别只看 insertions。\n")
d3 = io.open(MEM, encoding='utf-8', newline='').read()
io.open(MEM, 'w', encoding='utf-8', newline='').write(d3.rstrip('\n') + '\n' + addm)
print('memory ok')
