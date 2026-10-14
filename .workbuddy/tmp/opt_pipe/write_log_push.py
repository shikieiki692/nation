# -*- coding: utf-8 -*-
"""记录推送完成 ＋ 计划梳理。"""
import io

LOG = '00-首页/工作日志/2026-10-14.md'
ADD = '''
## 推送完成（owner：「先推送这个会话的内容吧，注意不要撞车」）

- **推送前侦察**：本地 ahead 64 笔（含并行会话提交）；工作区只有并行会话的 memory 等文件 ⇒ 未碰。
- 🔴 **推送前发现两处隐患并修复**：
  1. **主索引残留 6 项暂存**（早期脚本 `git add` 未清）：`fix_notes.py` / `vol_img_upscale.py` / `vol_meta_XVI.json` / XVI 核验报告 / XVI 答题卡 docx / `render_gate_allowlist.txt` ⇒ 已补齐提交（`2d7ee5ddb`）。
  2. 🔴🔴 **SOP.md 被误插 4 行 `git show --stat` 输出**（`Author:` / `Date:` / commit 消息 / **乱码文件名**）——某次脚本输出被写进了正文 ⇒ 按行号精确清理（保留正确的「提交脚本加固」段），断言污染文本消失；并**全库扫描确认无其它文件被同类污染**（仅另有一处是 2026-09-20 的历史文件，非本会话）。
- ✅ **推送成功**：`cf4be4dbe..2d7ee5ddb`；`git ls-remote` 核对远端＝本地＝`2d7ee5ddb`，**status 无 ahead/behind**（完全同步）。
- ⚠️ 遗留：工作区仍有并行会话的 memory/其它 docx 改动（**不碰**）。

## 计划梳理（待 owner 拍板）

见对话中的计划表；核心是 **T1 chemy 域 D1/D2 修复**（当前实况：D1 3 卡/5 处、D2 29 卡/41 处）。
'''
d = io.open(LOG, encoding='utf-8', newline='').read()
io.open(LOG, 'w', encoding='utf-8', newline='').write(d.rstrip('\n') + '\n\n' + ADD)
print('worklog ok')

MEM = '.workbuddy/memory/2026-10-14.md'
ADDM = '''
### 推送 ＋ 事故修复（2026-10-14 午后）

- 🔴🔴 **SOP.md 曾被误插 4 行 `git show --stat` 输出**（含 `Author:`/`Date:`/乱码文件名）——**脚本输出被写进正文**的典型事故；已按行号清理 + 全库扫描确认无他例。**教训：任何「把命令输出写进文件」的操作，必须用 `Write`/`Edit` 工具或显式变量，⛔ 不用 shell 重定向拼接**。
- 🔴 **主索引会残留暂存项**：隔离索引脚本的 `reset -q HEAD -- <paths>` 之后，早期 `git add` 的残留仍可能停在主索引 ⇒ **推送前必查 `git diff --cached --name-only`** 并补齐提交。
- ✅ 推送口径：`git fetch` → 查 ahead/工作区 → `git -c credential.helper=manager push origin master` → `git ls-remote` 核对（本次 `2d7ee5ddb` 完全同步）。
'''
d2 = io.open(MEM, encoding='utf-8', newline='').read()
io.open(MEM, 'w', encoding='utf-8', newline='').write(d2.rstrip('\n') + '\n' + ADDM)
print('memory ok')
