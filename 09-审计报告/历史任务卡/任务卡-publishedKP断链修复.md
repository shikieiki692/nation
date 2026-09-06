---
title: published KP 断链修复（18处）
type: 活跃任务卡
task_type: 知识库维护
status: completed
priority: P2
area: 知识库系统
owner: Agent
created: 2026-08-04
updated: 2026-08-10
completed: 2026-08-10
source_notes:
  - "[[09-审计报告/auto-validation/2026-08-04-validation]]"
related_notes:
  - "[[09-审计报告/历史任务卡/任务卡-validate_kb与published断链目录治理]]"
evidence:
  - "2026-08-04: validate --quick 全库 0 error；18 处 published KP 存在断链（无机和结构化学/天然冰结构·电解冶金·硼化学·磷化学·等瓣相似·钨 等 + 有机 Felkin-Anh/Grossman/Hammett 等）。"
  - "2026-08-04 全量分类实测：13 断链/10 文件；2 条改链（Grossman→提炼-ABOC-第11章-解题训练），11 条目标 KP 缺失保留欠账。"
  - "2026-08-10: 近义复核推翻'无近义'结论——6 目标靠 alias 清零（缺电子化合物/硼化学/原子簇化学/Cahn-Ingold-Prelog规则/Hammett方程/电化学，7处 alias），新建 2 KP（水的特殊性/间隙化合物）。validate --full 0 error，断链 1885→1870（-15）；原 9 条 published 断链全部清零，新 KP 无新断链。"
  - "2026-08-10 复查：A 组 7 处 alias 落盘全部核实；新 KP §九 题型项为裸文本（非 wikilink，与全库风格一致，不产生断链/红链）；修正间隙化合物 alias 概念污染（移除'间隙固溶体'，与正文 Hägg 规则区分原则一致）。"
  - "2026-08-10 门禁残余批量清零：真实范围 22 文件（报告 top-10 截断误导为 16）。本次修复 16 讲义改名残留（41 处）+ 超分子化学/亲核取代与消除反应 frontmatter 残留（2 处）+ 专题-化学平衡 改链 [[题型-化学平衡计算]] + 氮族元素 3 alias（氮氧化物/硝酸/亚硝酸）+ 题-38决理-4 加无空格 alias + validate 门禁段补目录 fallback（消除 [[04-题库]] 目录链接误报）。validate --full 复跑 0 error，published 门禁 22→1，仅剩晶体结构练习题组 mineru 图片缺失（图片 backlog）。"
---

# published KP 断链修复（18 处）

## 目标

修复 `03-知识点/` 下 18 个 `stage=published` KP 的断链引用（REDLINK），使 published 态文件无断链。

## 当前状态

- 2026-08-04 全量分类实测：**13 条断链 / 10 个 published KP**（天然冰1·电解冶金1·硼化学3·硼硫族1·磷化学1·等瓣相似1·钨1·Felkin-Anh1·Grossman2·Hammett1）
- **已修复 2 条**（Grossman规则 → ABOC 第11章 文件改名残留，改指 [[07-资料提炼/书籍提炼/提炼-ABOC-第11章-解题训练]]）
- **2026-08-10 已清零**：原 11 条欠账全部消解（多中心键 2 条此前已靠 alias 消解；本次 7 处 alias + 新建 2 KP 清除剩余 9 条 published 断链，另顺带清 1 条题库断链）。
- **2026-08-10 门禁残余清零**：此前"10 文件 15 处"实为 22 文件（报告截断，top-10 + …还有 12 处）。批量修复后 published 门禁仅剩 1 项（晶体结构练习题组 mineru 图片缺失，图片 backlog 排期）。

## 待办

- [x] 跑 `validate --full` 获取精确断链目标（2026-08-04）
- [x] 逐一判断：2 条改链（Grossman→ABOC第11章解题训练）；11 条目标 KP 缺失
- [x] 待决策（2026-08-10）：7 处 alias 补链 + 新建 2 KP（水的特殊性/间隙化合物）；其余目标靠 alias 解决（电解→电化学，CIP排序规则→Cahn-Ingold-Prelog规则 等）
- [x] 创建后重跑 validate 确认清零（2026-08-10：0 error，断链 -15，原目标清零）
- [x] 后续：published 门禁残余批量清零（2026-08-10：22 文件 wikilink 断链全部清除，仅剩 1 项图片 backlog 转 [[00-首页/活跃任务/断链内容建设backlog]] 排期）
