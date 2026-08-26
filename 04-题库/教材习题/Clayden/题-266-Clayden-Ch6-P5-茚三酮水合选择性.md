---
title: 题-266-Clayden-Ch6-P5-茚三酮水合选择性
type: 题目
fidelity: 原书逐字
submodule: 羰基亲核加成
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[羰基亲核加成]]", "[[水合物]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch6-P5]
source: Clayden Organic Chemistry 2nd Ed. Chapter 6 Problem 5
cross_references: ["[[题-263-Clayden-Ch6-P2-环丙酮水合vs半缩醛稳定性]]", "[[题-267-Clayden-Ch6-P6-羟基酮IR异常→环状半缩醛]]", "[[题-268-Clayden-Ch6-P8-NaBH4还原氯醛水合物机理]]"]
module: 有机化学
status: 已填充
---
# 题-266: 茚三酮（Ninhydrin）水合选择性

## 题目

The triketone shown here is called 'ninhydrin' and is used for the detection of amino acids. It exists in aqueous solution as a hydrate. Which ketone is hydrated and why?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/358c183c9e6597ff4912a3f0ac36c5027e17439f0d54a60b36d0af19007b8b43.jpg]]

**原文题目**：如图所示的三酮叫"茚三酮"，用于检测氨基酸。它在水溶液中以水合物形式存在。哪个酮被水合了？为什么？

## 参考答案

**Answer (English)**: The two ketones next to the benzene ring are stabilized by conjugation with it but also destabilized by the central ketone — two electron-withdrawing groups next to each other is a bad thing. The central carbonyl group is not stabilized by conjugation and is destabilized by two other ketones so it forms the hydrate. Did you remember that hydrate formation is thermodynamically controlled?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/c3080680046891eb63b2ac2273e88de681b81d296a2748ee4dde723d6f054d59.jpg]]

**中文解析**：

茚三酮有三个羰基，需要判断哪一个被水合：

**两侧的酮（与苯环共轭）**：
- 与苯环共轭→电子离域→C=O被稳定化
- 但同时受到中间羰基的吸电子效应影响（两个吸电子基相邻不好）
- 总体上仍被苯环稳定，不容易水合

**中间的酮（不与苯环共轭）**：
- 不与苯环共轭→没有共轭稳定化
- 两侧各有一个吸电子酮基→被双重去稳定化
- 水合后变为sp³碳，消除两个相邻吸电子基的影响
- 水合是热力学控制的——中间酮水合后体系能量最低

**结论**：中间的C=O被水合，因为它最不稳定（无共轭+双重吸电子去稳定化），水合后释放最多的去稳定化能量。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[羰基亲核加成]] | 水合反应作为亲核加成 | 直接 |
| [[水合物]] | 水合物稳定性的判断依据 | 直接 |
| [[共轭效应]] | 苯环共轭对酮稳定性的影响 | 直接 |
| [[平衡常数]] | 热力学控制的平衡方向 | 间接 |

## 解题思路

1. **读题定位**：三酮化合物，哪个羰基被水合？→需要比较三个羰基的相对稳定性
2. **🔑 关键转换**：水合是热力学控制的——最不稳定的羰基最容易水合。中间酮：无苯环共轭+两个相邻吸电子基=最不稳定→水合
3. **验证**：水合后中间碳从sp²变sp³，两个相邻C=O变为C-OH，消除了相邻吸电子基的不良影响

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为三个羰基等价 | 没有仔细看分子对称性 | 两侧酮与苯环共轭，中间酮不共轭——化学环境不同 | 如何判断分子中的共轭体系？ |
| 忽略"热力学控制"提示 | 没有理解水合是平衡反应 | 水合物形成是可逆的，最终产物由热力学稳定性决定 | 动力学控制和热力学控制有什么区别？ |
| 认为吸电子基促进水合 | 混淆了水合和水解 | 吸电子基使羰基碳更正→更容易被亲核进攻→但关键是看水合物的稳定性 | 为什么CCl₃CHO几乎完全水合？ |