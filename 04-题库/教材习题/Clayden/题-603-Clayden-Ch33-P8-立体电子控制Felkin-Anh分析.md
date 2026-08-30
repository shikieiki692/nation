---
title: 题-603-Clayden-Ch33-P8-立体电子控制Felkin-Anh分析
type: 题目
fidelity: 原书逐字
submodule: 非对映选择性
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 竞赛拔高
syllabus_codes: ["21"]
knowledge_points: ["[[Felkin-Anh模型]]"]
tags: [化竞, Clayden, 有机化学, 非对映选择性]
updated: 2026-07-25
aliases: [Clayden-Ch33-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 33 Problem 8
cross_references: ["[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性]]", "[[题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-603: 立体电子控制Felkin-Anh分析

## 题目

**【中文】**解释该反应（见图）的立体选择性。用碱处理该产物会生成环氧化物的哪种异构体？

**【原文】**Explain the stereoselectivity of this reaction. What isomer of the epoxide would be produced by treatment of the product with base?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/f6563d05265a4c14ada6afdcb116fb4f31616601efb5db0403b5f369d27fd840.jpg]]

## 参考答案

**Answer (English)**: In this case the chloro substituent dominates because it has an electronic interaction with the carbonyl group. The two alkyl chains come out opposite one another so it is easy to draw the product in a reasonable fashion by imagining yourself observing the Newman projection from the top right.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/cb712c9013c8921576eabd748f055df3aeac2bd8c74a7307f1e4baeba86eda24.jpg]]

To draw the stereochemistry of the epoxide formation it is sensible to put the reacting groups in the plane of the paper and arranged so that the oxyanion can do an $S_\mathrm{N}2$ displacement.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/22d28d06a35fd52e021e46333b2f423ac9b500b8fc3efd6aef6896510202237f.jpg]]

**中文解析**：

关键步骤：
1. **立体电子效应优先**：在这个案例中，氯取代基支配了反应的立体化学——因为Cl与羰基之间存在立体电子相互作用（σ\*_C-Cl与π\*_C=O的相互作用），使得Cl倾向于占据垂直于C=O的位置（而非基于大小）
2. **Felkin-Anh修正**：当存在杂原子取代基时，立体电子效应可以使杂原子（而非最大基团）占据垂直于C=O的位置。两个烷基链彼此处于反式
3. **环氧化物形成**：将反应基团放在纸面上，氧负离子进行$S_\mathrm{N}2$分子内取代，得到特定构型的环氧化物

> **核心概念**：当手性中心上存在杂原子（特别是电负性基团如Cl、OR）时，Felkin-Anh模型需要修正——立体电子效应可以使杂原子优先占据垂直位置。这是因为杂原子的σ\*轨道与羰基π\*轨道的超共轭稳定化作用。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[Felkin-Anh模型]] | 立体电子效应修正的Felkin-Anh分析 | 直接 |
| [[立体电子效应]] | σ\*_C-Cl与π\*_C=O的超共轭 | 直接 |
| [[非对映选择性]] | 杂原子控制vs空间控制的竞争 | 间接 |

## 解题思路

1. **读题定位**：解释反应的立体化学+碱处理环氧化物——识别底物为含α-Cl的醛的亲核加成
2. **关键转换**：Cl的立体电子效应→Cl垂直于C=O（而非基于大小）→亲核试剂进攻→特定构型产物→碱处理$S_\mathrm{N}2$关环→环氧化物
3. **验证**：检查Cl是否在垂直位置，产物构型是否与立体电子效应一致，环氧化物是否由$S_\mathrm{N}2$关环得到

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 用标准Felkin-Anh（最大基团垂直） | 忽略立体电子效应 | 当有杂原子时，立体电子效应优先于空间效应 | 什么情况下立体电子效应优先？ |
| 画错Cl的位置 | 未理解σ\*-π\*相互作用 | Cl的σ\*轨道与C=O的π\*轨道超共轭，使Cl垂直于C=O | 为什么Cl而不是更大的烷基垂直？ |
| 环氧化物$S_\mathrm{N}2$画反 | 未考虑反式开环 | 氧负离子从Cl的反面进攻，得到反式环氧化物 | $S_\mathrm{N}2$环化时离去基团和亲核基团的立体关系？ |