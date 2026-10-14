# -*- coding: utf-8 -*-
r"""修复 2026-10-14 memory / SOP 中被 bash 反引号命令替换破坏的「提交脚本加固」段。
本脚本用 Write 生成、以文件方式执行 ⇒ 反引号不会被 shell 解释。
"""
import io, re

MEM = '.workbuddy/memory/2026-10-14.md'
SOP = '11-模板/规范/机构模拟题组卷管线SOP.md'

MEM_FIX = '''### 🔴🔴 提交脚本加固（stale tree 又咬了一次，2026-10-14 晚）

- **实伤**：隔离索引脚本走 `read-tree HEAD` → `add -f -- <我的路径>` → `commit`。本次 commit 却**多带了一个 `delete mode`**——删掉了**并行会话的** `09-审计报告/2026-10-14-chemy考段回填报告.md`（该文件在 HEAD 有、工作区被对方删除但未提交 ⇒ 我的提交**把删除也提交了**）。
- **防护**：已用**单独 fixup 提交补回**（`06dda55ec`）。**根治办法**：commit 时用 **`git commit --only -m … <paths>`**（只提交指定路径，不带索引中其它差异），或提交后**必查 `git show --stat HEAD` 有无非本会话文件**。
- **判据**：**每次 commit 后扫一眼 `--stat` 里有没有 `delete mode` / 陌生路径**；发现即单独 fixup 补回，⛔ 不 revert 他人提交。
- ⚠️ **写 memory/SOP 时勿用 bash 内联 python**（反引号会被命令替换 ⇒ 内容被吞）：一律 **Write 成 .py 再执行**。
'''

# ① memory：截断到「加固」段之前，再整段重写
d = io.open(MEM, encoding='utf-8', newline='').read()
i = d.find('### 🔴🔴 提交脚本加固')
if i >= 0:
    d = d[:i].rstrip('\n') + '\n\n' + MEM_FIX
    io.open(MEM, 'w', encoding='utf-8', newline='').write(d)
    print('memory 段已重写')

# ② SOP：删掉被破坏的那行，补正确版本
s = io.open(SOP, encoding='utf-8', newline='').read()
s = re.sub(r'\n> \*\*提交脚本加固（同日）\*\*：[^\n]*', '', s)
anchor = '>    已另立待办，**下一步逐卷核查**。'
SOP_FIX = anchor + '''
> **提交脚本加固（同日）**：隔离索引提交（read-tree → add → commit）**会把并行会话「已删未提交」的文件一并提交为 delete**（本次实伤：误删对方的 chemy 报告，已 fixup 补回）。⇒ **必用 `git commit --only -m … <paths>`**，或提交后**必扫 `git show --stat HEAD` 有无 `delete mode` / 陌生路径**。'''
if anchor in s:
    s = s.replace(anchor, SOP_FIX, 1)
    io.open(SOP, 'w', encoding='utf-8', newline='').write(s)
    print('SOP 段已重写')
