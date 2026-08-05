---
title: published KP 断链修复（18处）
type: 活跃任务卡
task_type: 知识库维护
status: active
priority: P2
area: 知识库系统
owner: Agent
created: 2026-08-04
updated: 2026-08-04
source_notes:
  - "[[09-审计报告/auto-validation/2026-08-04-validation]]"
related_notes:
  - "[[00-首页/活跃任务/任务卡-validate_kb与published断链目录治理]]"
evidence:
  - "2026-08-04: validate --quick 全库 0 error；18 处 published KP 存在断链（无机和结构化学/天然冰结构·电解冶金·硼化学·磷化学·等瓣相似·钨 等 + 有机 Felkin-Anh/Grossman/Hammett 等）。"
  - "2026-08-04 全量分类实测：13 断链/10 文件；2 条改链（Grossman→提炼-ABOC-第11章-解题训练），11 条目标 KP 缺失保留欠账。"
---

# published KP 断链修复（18 处）

## 目标

修复 `03-知识点/` 下 18 个 `stage=published` KP 的断链引用（REDLINK），使 published 态文件无断链。

## 当前状态

- 2026-08-04 全量分类实测：**13 条断链 / 10 个 published KP**（天然冰1·电解冶金1·硼化学3·硼硫族1·磷化学1·等瓣相似1·钨1·Felkin-Anh1·Grossman2·Hammett1）
- **已修复 2 条**（Grossman规则 → ABOC 第11章 文件改名残留，改指 [[07-资料提炼/书籍提炼/提炼-ABOC-第11章-解题训练]]）
- **保留欠账 11 条**：目标 KP 全库不存在且无近义（水的特殊性/三中心两电子键/碳硼烷/多中心键/簇合物结构/Wade规则/间隙化合物/CIP排序规则/线性自由能关系/电解）——需创建 KP 或接受前向引用

## 待办

- [x] 跑 `validate --full` 获取精确断链目标（2026-08-04）
- [x] 逐一判断：2 条改链（Grossman→ABOC第11章解题训练）；11 条目标 KP 缺失
- [ ] 待决策：11 个缺失 KP 是否创建（水的特殊性/三中心两电子键/碳硼烷/多中心键/簇合物结构/Wade规则/间隙化合物/CIP排序规则/线性自由能关系/电解）
- [ ] 创建后重跑 validate 确认清零
