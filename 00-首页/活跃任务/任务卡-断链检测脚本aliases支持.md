---
title: 断链检测脚本 aliases 支持
type: 活跃任务卡
status: completed
priority: P2
area: 脚本维护
owner: Agent
created: 2026-06-03
updated: 2026-06-07
completed: 2026-06-07
source_notes: [[09-审计报告/2026-06-07-断链检测]]
related_notes: [[状态摘要]], [[00-首页/工作日志/2026-06-07]]
evidence: [[00-首页/工作日志/2026-06-07]] §断链审计脚本升级（命名差异分层）
---

# 断链检测脚本 aliases 支持

**当前状态：已完成，并已超出原任务范围。**

已落地能力：
- 读取多行 frontmatter `aliases`
- 同时用 `title` / `aliases` / basename 匹配候选目标
- 支持旧命名前缀、日期、班型、`L1/L2` 等语义噪声剥离

> 该任务原本只是“让断链脚本读 aliases”；截至 2026-06-07，脚本已升级为更可靠的分层断链审计，不再保留在 `active` 队列。
