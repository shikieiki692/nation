# -*- coding: utf-8 -*-
r"""补记：隔离索引提交第二次误删事故 ＋ `--only` 为唯一正解。"""
import io

MEM = '.workbuddy/memory/2026-10-14.md'
ADD = '''
### 🔴🔴 隔离索引提交**第二次**误删他人文件（2026-10-14 午后）—— `--only` 是唯一正解

- **实伤**：一笔隔离索引提交（`read-tree h0` → `add` → `commit`）又带出 **3 项 `delete mode`**：
  `.workbuddy/memory/ARCHIVE-2026-10-02-遗留判据.md`、`.workbuddy/memory/MEMORY.md`、
  `09-审计报告/2026-10-14-chemy-P3旧卡归属错位评估.md`（114 行整文件）—— 全是**并行会话**的文件。
- **恢复**：三文件**工作区版本完好** ⇒ `git add` + **`git commit --only -m … -- <paths>`** 补回（`36e000d4b`），已推送。
- 🔴🔴 **结论（定版判据）**：
  1. **隔离索引 + 普通 `commit` 不可靠** —— 即使 `read-tree` 后只 `add` 自己的路径，`commit` 仍可能把「索引 vs 工作区不一致」的条目写成 delete。
  2. **正解＝`git commit --only -m <msg> -- <paths>`**：只提交指定路径，**完全绕开索引其余差异**（本次实测有效）。
  3. **每笔提交后必 `git show --stat HEAD` 看有无 `delete mode`** —— 若出现非自己删的文件，立即 `git add` 工作区版本 + 单独 fixup 补回，⛔ 绝不 revert 他人提交。
- ⚠️ **推送前必查 `git diff --cached --name-only`**（主索引残留暂存项）—— 本次推送前发现 6 项残留并补齐（`2d7ee5ddb`）。
'''
d = io.open(MEM, encoding='utf-8', newline='').read()
io.open(MEM, 'w', encoding='utf-8', newline='').write(d.rstrip('\n') + '\n' + ADD)
print('memory ok')

SOP = '11-模板/规范/机构模拟题组卷管线SOP.md'
s = io.open(SOP, encoding='utf-8', newline='').read()
old = '⇒ **必用 `git commit --only -m … <paths>`**，或提交后**必扫 `git show --stat HEAD` 有无 `delete mode` / 陌生路径**。'
new = ('⇒ **必用 `git commit --only -m … <paths>`**（隔离索引 + 普通 commit **实测仍会误删**，2026-10-14 两次），'
       '并**每笔提交后必扫 `git show --stat HEAD` 有无 `delete mode` / 陌生路径**；发现即 `git add` 工作区版本 + 单独 fixup 补回。')
if old in s:
    s = s.replace(old, new, 1)
    io.open(SOP, 'w', encoding='utf-8', newline='').write(s)
    print('SOP ok')
else:
    print('SOP 锚点未匹配（跳过）')
