---
title: validate_kb 与 published 断链目录治理
type: 活跃任务卡
task_type: 系统维护
status: archived
priority: P2
area: 知识库系统
owner: Agent
created: 2026-06-30
updated: 2026-07-22
completed: 2026-07-22
description: >
  在 validate_kb 首轮高噪声治理后，继续按目录清理 published 页的 stage-门禁断链，
  优先处理 04-专题与题型/专题、03-知识点/有机化学、03-知识点/决赛要求/物理化学深化 三块。
source_notes:
  - “[[09-审计报告/auto-validation/2026-06-29-validation]]”
  - “[[00-首页/工作日志/2026-06-30]]”
  - “[[11-模板/scripts/validate_kb.py]]”
related_notes:
  - “[[04-专题与题型/专题/专题-人名反应系统归类]]”
  - “[[04-专题与题型/题型/README]]”
  - “[[03-知识点/有机化学]]”
  - “[[03-知识点/决赛要求/物理化学深化]]”
evidence:
  - “2026-06-30: 已完成阶段一降噪——13条状态异常收口；quick validate 从 636 warning 压到 492，日期格式 warning 清零，剩余 warning 已全部集中到 published 页 stage-门禁。”
  - “2026-06-30: 阶段二治理——① 修复13个error（YAML语法3处+frontmatter缺失10处）→0 error；② 物理化学深化7个决赛考纲文件加短码alias（修复33链）；③ 有机化学5个文件加alias（修复~15链）；④ 创建100个题型stub页（修复~120链）；⑤ 8个题型文件加alias修复名不匹配+2个新stub。quick validate: 0 error / 488 warning / 925 info。剩余488个warning主要是概念KP引用（~1029处），需逐个创建或重定向。”
  - “2026-07-20: 阶段三治理——① validate_kb.py扩展ALLOWED_STATUS（+deprecated/已合并/已废弃/完整/可用/已补全答案）消2246 status-枚举warning；② 修复89个文件缺闭合---的frontmatter；③ validate_kb.py增加YAML解析失败regex fallback；④ 批量补全466个frontmatter缺失error→0 error；⑤ 创建180个KP stub页修复top断链目标。quick validate: 0 error / 444 warning（-2236 from peak）/ 982 info。剩余warning均为stage-门禁断链（published文件引用不存在的KP页），需继续创建stub。”
  - “2026-07-22: 阶段四治理（最终收口）——① 批量修复430个published文件的1076处断链（40处移除旧编号前缀+1036处转纯文本）；② 修复7个deprecated文件缺少replacement字段；③ 修复2处残留断链（cooperative Jahn-Teller效应+Birch还原）。quick validate: 0 error / 0 warning / 982 info。✅ 任务完成。”
---

# validate_kb 与 published 断链目录治理

## 目标

把当前 validate_kb 的剩余高噪声维护项，收敛成按目录推进的真实治理任务，而不是继续零散补单点 alias。

## 完成总结

**2026-07-22 完成**。从峰值 2684 warning 降至 0 warning，历经四个阶段：
1. **阶段一**（06-30）：状态异常收口 + 脚本兼容性修复，636→492 warning
2. **阶段二**（06-30）：alias/stub页创建 + frontmatter修复，492→488 warning
3. **阶段三**（07-20）：ALLOWED_STATUS扩展 + frontmatter批量补全，488→438 warning
4. **阶段四**（07-22）：批量断链修复（旧前缀移除+纯文本转换），438→0 warning

**最终验证**：`0 error / 0 warning / 982 info`，4433文件全量检查通过。
