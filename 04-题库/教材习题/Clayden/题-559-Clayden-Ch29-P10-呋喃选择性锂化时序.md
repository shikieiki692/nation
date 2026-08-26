---
title: 题-559-Clayden-Ch29-P10-呋喃选择性锂化时序
type: 题目
fidelity: 原书逐字
submodule: 杂环化合物
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[呋喃]]"]
tags: [化竞, Clayden, 有机化学, 杂环]
updated: 2026-07-25
aliases: [Clayden-Ch29-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 29 Problem 10
cross_references: ["[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-559: 呋喃选择性锂化时序

## 题目

Explain the order of events and the choice of bases in this sequence.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/489abdf5f090ac1fa3c250eda007abda5fed3aeace6190f7f80c172b613850b8.jpg]]

**原文题目**：Explain the order of events and the choice of bases in this sequence involving selective lithiation of a substituted furan.

## 参考答案

**Answer (English)**: The allylic group evidently goes into the 2-position so deprotonation of the starting material by LDA must occur there, directed by both the oxygen and bromine atoms. The second electrophile (MeI) takes the place of the Br atom, so BuLi must lead to bromine-lithium exchange rather than deprotonation. The alternative order of events would require selective lithiation adjacent to the methyl group—not something you would expect to work reliably.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/656e12e1c5b3695427a813738c314ee6df94242d984a1a86644a1ac394d951f5.jpg]]

> The product is related to a constituent of the perfume of roses and was made by N. D. Ly and M. Schlosser, Helv. Chim. Acta 1977, 60, 2085.

**中文解析**：

关键步骤：
1. **第一步：LDA去质子化**：LDA（二异丙基氨基锂）作为位阻碱，在呋喃的2位去质子化——该位点被氧原子和溴原子双重定向（邻位定向金属化，DoM）。生成的碳负离子被烯丙基溴捕获，引入烯丙基到2位
2. **第二步：BuLi卤-锂交换**：nBuLi与呋喃上的Br发生卤-锂交换（而非去质子化），生成2位锂化中间体。然后MeI作为亲电试剂捕获，甲基取代了Br的位置
3. **为什么不用另一种顺序**：如果先做卤-锂交换再引入烯丙基，就需要在甲基邻位选择性去质子化——这不太可靠

> **核心概念**：LDA做选择性去质子化（邻位定向），BuLi做卤-锂交换——两种碱各司其职。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[呋喃]] | 呋喃的邻位锂化和卤-锂交换 | 直接 |
| [[邻位锂化]] | LDA定向去质子化（DoM）和BuLi卤-锂交换的区别 | 直接 |
| [[有机锂试剂]] | LDA vs nBuLi的不同反应性（去质子化 vs 卤-锂交换） | 直接 |
| 选择性合成 | 反应顺序对区域选择性的影响 | 间接 |

## 解题思路

1. **读题定位**：两步锂化反应，试剂分别是LDA和BuLi，亲电试剂分别是烯丙基溴和MeI——需要解释顺序和碱的选择
2. **🔑 关键转换**：LDA→选择性去质子化（DoM，O和Br定向）→烯丙基化；BuLi→卤-锂交换→甲基化
3. **验证**：检查最终产物中烯丙基在2位、甲基在原Br位——符合两步锂化的区域选择性

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 混淆LDA和BuLi的功能 | 不清楚两种碱的反应模式差异 | LDA做去质子化，BuLi做卤-锂交换 | 为什么LDA不做卤-锂交换？ |
| 两步顺序颠倒 | 没考虑区域选择性的可靠性 | 必须先LDA去质子化（有定向基），再BuLi交换Br | 如果先交换Br会出什么问题？ |
| BuLi去质子化而非交换Br | BuLi与芳基卤主要发生卤-锂交换 | nBuLi与sp²碳上的Br发生卤-锂交换（p.188） | BuLi在什么条件下做去质子化？ |