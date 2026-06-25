---
title: 题库 Dataview 组卷查询验证
type: 活跃任务卡
status: completed
completed: 2026-06-12
priority: P1
area: 题库系统
owner: Agent
created: 2026-06-03
updated: 2026-06-12
source_notes: "[[00-首页/工作日志/2026-06-03]]"
related_notes: "[[模板-专题练习卷]]"
evidence: "[[00-首页/工作日志/2026-06-03]]"
---

# 题库 Dataview 组卷查询验证

在真实题库中测试 `[[模板-专题练习卷]]` 的筛题效果。

## 验证结论

- `[[模板-专题练习卷]]` 中原查询模板存在 3 个会影响真实组卷的点，已修正：
  - `4.1` 使用了 `type` 作为“题型”展示列，实际应为 `question_type`
  - `4.1` 的 `OR/AND` 未加括号，原写法会把难度条件只绑定到最后一个知识点
  - `4.2` 把三段不同查询写在同一个 Dataview 代码块里，真实使用时应拆成 3 个独立查询块
- 为兼容题库中 `knowledge_points` 同时存在 wikilink / 纯文本项的情况，模板查询统一改为 `contains(string(knowledge_points), "...")`
- `[[04-题库/教材习题/ABOC/索引]]` 的“按知识点检索”原为 `FLATTEN` 后直接列表，无法作为真正的“按知识点组卷”入口；现已补为 `GROUP BY knowledge_points`

## 已落地修正

- [[11-模板/模板-专题练习卷]]
- [[04-题库/教材习题/ABOC/索引]]
- [[02-数据库/数据库-真题]]

## 后续建议

- `[[02-数据库/数据库-真题]]` 已将 DataviewJS 交互组卷面板前置为页首主入口，并保留“基础 / 综合 / 挑战”静态查询块作为备用模板区。

## 运行态补充结论

- 后续实机验收中发现：`[[02-数据库/数据库-真题]]` 本身可正常打开，但执行 `markdown:toggle-preview` 时，Obsidian 抛出 `TypeError: this.currentMode.getEphemeralState is not a function`
- 继续排查后确认：临时禁用 `dust-calendar v1.4.0` 后，预览切换错误消失，页面可正常进入 `preview`
- 因此本轮“预览态切换失败”问题的直接触发源是 `dust-calendar` 插件，而不是题库页 Dataview 查询本身
- 在此基础上，`[[02-数据库/数据库-真题]]` 已进一步收口：删除低价值的“按模块统计 / 按题型统计 / 按难度分布”三块，仅保留仍有直接使用价值的入口
