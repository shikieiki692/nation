---
title: 题-475-Clayden-Ch37-P11-自由基关环的奇特立体化学
type: 题目
submodule: 自由基反应
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 竞赛拔高
syllabus_codes: ["21"]
knowledge_points: ["[[自由基]]"]
tags: [化竞, Clayden, 有机化学, 自由基反应]
updated: 2026-07-25
aliases: [Clayden-Ch37-P11]
source: Clayden Organic Chemistry 2nd Ed. Chapter 37 Problem 11
cross_references: ["[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-465-Clayden-Ch37-P1-重要自由基反应复习]]", "[[题-466-Clayden-Ch37-P2-重氮盐亲核取代vs自由基对比]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]"]
module: 有机化学
status: 已填充
---
# 题-475: 自由基关环的立体化学——非对映选择性

## 题目

Suggest a mechanism for this reaction explaining why a mixture of diastereoisomers of the starting material gives a single diastereoisomer of the product. Is there any other form of selectivity?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/c3c99eb7f7408fe40a48ac6980550a9452d01f24c8e1c4cc3a09eda8577d297.jpg]]

**原文题目**：Suggest a mechanism for this reaction explaining why a mixture of diastereoisomers of the starting material gives a single diastereoisomer of the product. Is there any other form of selectivity?

## 参考答案

**Answer (English)**: The abstraction of bromine, at first by AIBN and thereafter by Bu₃Sn· produces a radical that again does not eliminate but adds to an alkene. A five-membered ring is formed (this is usually the more favourable closure) by attack on the alkene on the opposite side from that occupied by the i-Pr group. The product is a mixture of diastereoisomers as no change occurs at the acetal centre.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/3512eed2cea6406843d80483ea62fcc225d2a01e1b262b42bb646666e52ee6be.jpg]]

Acid-catalysed oxidation first hydrolyses the acetal and then oxidizes either the hemiacetal or the aldehyde to the lactone. Now the molecule is one diastereoisomer as the ambiguous centre is planar. The other form of selectivity is the ring size (see the textbook, p. 1000).

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/712bf2a7f9db1771f1ecf7adfea1fdc983493cc9a55b154bd82fb37c0e00dfdc.jpg]]

**中文解析**：

关键步骤：

**第一步：自由基关环**
1. AIBN引发 → Bu₃Sn·从底物夺取Br → 产生碳自由基
2. 碳自由基对分子内烯烃进行5-exo关环（五元环通常比六元环更有利）
3. 立体选择性：自由基从i-Pr基团的反面进攻烯烃（空间位阻控制）
4. 关环后从Bu₃SnH夺氢，得到产物

**为什么非对映体混合物得到单一产物？**
- 起始原料是缩醛（acetal）的非对映体混合物
- 关环发生在缩醛中心的远处，不影响缩醛的立体化学
- 但关环产生了一个新的手性中心，且选择性由i-Pr基团的空间位阻控制
- 因此两种非对映体起始物都给出相同的关环产物（加上缩醛仍为混合物）

**第二步：酸催化氧化**
1. 酸水解缩醛 → 半缩醛/醛
2. 氧化（如PCC或Swern）→ 内酯
3. 此时"模糊"的手性中心变为平面（羰基碳），所以产物是单一非对映体

**其他选择性**：环大小选择性——5-exo关环（五元环）通常优于6-endo关环（六元环）

> **注意**：这个例子说明自由基关环的立体化学可以由底物上的取代基空间位阻控制，而不是由自由基中心的立体化学决定。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[自由基]] | Bu₃SnH介导的自由基关环 | 直接 |
| [[立体化学]] | 空间位阻控制的非对映选择性 | 直接 |
| [[关环反应]] | 5-exo vs 6-endo选择性 | 间接 |
| [[缩醛化学]] | 缩醛水解和氧化 | 间接 |

## 解题思路

1. **读题定位**：题目要求解释为什么非对映体混合物给出单一产物，以及是否存在其他选择性
2. **关键转换**：自由基关环（i-Pr反面进攻）→ 非对映体混合物因关环选择性统一 → 缩醛氧化后模糊中心变平面 → 单一产物
3. **验证**：检查关环是否为5-exo，立体化学是否由i-Pr控制，氧化后是否消除模糊中心

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为自由基中心本身有立体选择性 | 自由基碳是平面的，无立体化学 | 选择性来自邻近i-Pr基团的空间位阻，不是自由基本身 | 自由基碳的几何构型是什么？ |
| 忘记缩醛中心不受影响 | 没有追踪所有手性中心 | 关环不改变缩醛中心，但氧化使其变平面 | 缩醛水解后为什么会失去手性？ |
| 忽略环大小选择性 | 只关注了立体选择性 | 题目问"其他选择性"——环大小（5-exo vs 6-endo）也是选择性 | 为什么5-exo通常更有利？ |
| 混淆AIBN和Bu₃Sn·的角色 | 没有理解链传递 | AIBN只引发一次，之后Bu₃Sn·负责链传递中的夺溴 | AIBN在反应中消耗几次？ |