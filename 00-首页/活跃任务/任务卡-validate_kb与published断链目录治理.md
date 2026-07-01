---
title: validate_kb 与 published 断链目录治理
type: 活跃任务卡
task_type: 系统维护
status: active
priority: P2
area: 知识库系统
owner: Agent
created: 2026-06-30
updated: 2026-06-30
description: >
  在 validate_kb 首轮高噪声治理后，继续按目录清理 published 页的 stage-门禁断链，
  优先处理 04-专题与题型/专题、03-知识点/有机化学、03-知识点/决赛要求/物理化学深化 三块。
source_notes:
  - "[[09-审计报告/auto-validation/2026-06-29-validation]]"
  - "[[00-首页/工作日志/2026-06-30]]"
  - "[[11-模板/scripts/validate_kb.py]]"
related_notes:
  - "[[04-专题与题型/专题/专题-人名反应系统归类]]"
  - "[[04-专题与题型/题型/README]]"
  - "[[03-知识点/有机化学]]"
  - "[[03-知识点/决赛要求/物理化学深化]]"
evidence:
  - "2026-06-30: 已完成阶段一降噪——13条状态异常收口；quick validate 从 636 warning 压到 492，日期格式 warning 清零，剩余 warning 已全部集中到 published 页 stage-门禁。"
  - "2026-06-30: 阶段二治理——① 修复13个error（YAML语法3处+frontmatter缺失10处）→0 error；② 物理化学深化7个决赛考纲文件加短码alias（修复33链）；③ 有机化学5个文件加alias（修复~15链）；④ 创建100个题型stub页（修复~120链）；⑤ 8个题型文件加alias修复名不匹配+2个新stub。quick validate: 0 error / 488 warning / 925 info。剩余488个warning主要是概念KP引用（~1029处），需逐个创建或重定向。"
---

# validate_kb 与 published 断链目录治理

## 目标

把当前 validate_kb 的剩余高噪声维护项，收敛成按目录推进的真实治理任务，而不是继续零散补单点 alias。

## 当前判断

- 阶段一已经把“脚本不会认 / 旧路径兼容 / frontmatter 误报”这一层清掉了大半。
- 剩下的主要是高频被引用但确实还缺稳定承接页的概念、题型和目录入口。
- 继续推进时，要优先选择“一改能同时消多页 warning”的目标。

## 建议顺序

1. `04-专题与题型/专题`
2. `03-知识点/有机化学`
3. `03-知识点/决赛要求/物理化学深化`

## 完成标准

- 最新 quick validate 继续下降
- 不再出现新的 `status` / `updated` 规则噪声
- 新增桥接页、alias 和目录页都能被入口文档正确引用
