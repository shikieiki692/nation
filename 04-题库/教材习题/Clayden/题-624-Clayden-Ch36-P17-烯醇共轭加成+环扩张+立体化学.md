---
title: 题-624-Clayden-Ch36-P17-烯醇共轭加成+环扩张+立体化学
type: 题目
fidelity: 原书逐字
submodule: 重排反应
exam_stage: 复赛
subject: 有机化学
difficulty: 4
teaching_level: 竞赛拔高
syllabus_codes: ["21"]
knowledge_points: ["[[共轭加成]]", "[[重排反应]]"]
tags: [化竞, Clayden, 有机化学, 重排反应, 共轭加成, 烯胺]
updated: 2026-07-25
aliases: [Clayden-Ch36-P17]
source: Clayden Organic Chemistry 2nd Ed. Chapter 36 Problem 17
cross_references: ["[[题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择]]", "[[题-515-Clayden-Ch40-P2-Heck反应机理步骤理解]]", "[[题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性]]", "[[题-514-Clayden-Ch40-P1-烯醇醚溴化WittigPd化学入门]]"]
module: 有机化学
status: 已填充
---
# 题-624: 烯醇共轭加成+环扩张+立体化学

## 题目

Give mechanisms for these reactions, commenting on the fragmentation.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/448be5c1ecf4ab23c11ea9b3f813be285138989ef8465794dec739efeb1280b4.jpg]]

**原文题目**：Give mechanisms for these reactions, commenting on the fragmentation.

## 参考答案

**Answer (English)**: The first step is enamine formation and the second is conjugate addition. This appears to lead to a dead end as we cannot find a way to make the intermediate from the product.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/9e7080a0b62b0fa6747d293855b34670c985bd4a7432daadeb2d180cc171d168.jpg]]

The answer is to exchange the enamine of the ketone with the enamine of the aldehyde. Under the conditions, enamine formation is reversible and there are various ways you could draw details. Cyclization of this compound now gives the intermediate we are looking for.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/8ce5562ff784fe52ef18e8c2ea7f7f446ab94250966f8bc1f2c00bc02698178e.jpg]]

The last two diagrams show where the stereochemistry comes from. The final product has a chair six-membered ring. The 1,3-bridge on the bottom of this ring must be diaxial or it cannot reach round. The pyrrolidine is equatorial and the five-membered ring must be cis fused. No doubt the stereochemistry as well as the intermediates are under thermodynamic control.

Finally the fragmentation itself. Methylation of the nitrogen makes it into a leaving group and addition of hydroxide to the ketone provides the electronic push. Notice that the C–N⁺ bond, the C–C bond being fragmented, and a lone pair on the O⁻ group are all parallel. The stereochemistry is already there in the intermediate.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/3f53a8cf30677ea92bfb1d8660899688864e1e5941e7318929101929fd301812.jpg]]

**中文解析**：

**整体机理概述**：
本题涉及一个多步反应序列：烯胺形成→共轭加成→烯胺交换→分子内环化→N-甲基化→碎片化。每一步都有其独特的化学逻辑，最终通过碎片化构建目标产物并控制立体化学。

**步骤1：烯胺形成**：
酮与吡咯烷（pyrrolidine）在酸催化下形成烯胺（enamine）。烯胺是酮的烯醇等价体，具有亲核性。

**步骤2：共轭加成**：
烯胺对α,β-不饱和醛（丙烯醛）进行共轭加成（1,4-加成），将酮的α-碳连接到不饱和醛的β-碳上。

**步骤3：烯胺交换（关键步骤）**：
直接从步骤2的产物无法得到目标中间体。解决方案是：
- 烯胺的形成在反应条件下是**可逆的**
- 酮的烯胺可以与醛交换，形成醛的烯胺
- 这个交换过程是热力学驱动的

**步骤4：分子内环化**：
醛的烯胺进行分子内环化，形成目标中间体——一个含有吡咯烷环的双环体系。

**立体化学控制**：
- 最终产物具有椅式六元环构象
- 1,3-桥（含吡咯烷的五元环）必须是**双直立键（diaxial）**排列——否则无法跨越环
- 吡咯烷环是赤道位（equatorial）
- 五元环与六元环之间是**顺式稠合（cis fusion）**
- 立体化学和中间体都处于**热力学控制**下

**步骤5：N-甲基化**：
氮原子被甲基化（如用MeI），将原本是碱的吡咯烷变为季铵盐——这使其成为好的离去基团。

**步骤6：碎片化（最终步骤）**：
- OH⁻加到酮羰基上，形成烷氧基负离子
- O⁻的孤对电子作为推电子基团（push）
- C-N⁺键断裂，吡咯烷作为离去基团（pull）
- C-C键也断裂（碎片化）
- 注意：C-N⁺键、断裂的C-C键、O⁻孤对电子三者**平行（反式共面）**
- 立体化学已经在中间体中预设好了

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[共轭加成]] | 烯胺对α,β-不饱和醛的1,4-共轭加成 | 直接 |
| [[重排反应]] | 碎片化作为最终的C-C键断裂重排 | 直接 |
| [[立体化学]] | 1,3-桥的双直立键要求和顺式稠合 | 直接 |
| [[烯胺]] | 烯胺的可逆性和交换反应 | 间接 |
| [[邻基参与]] | 氮甲基化后的季铵盐作为离去基团 | 间接 |

## 解题思路

1. **读题定位**：题目要求给出完整机理并讨论碎片化。关键词：mechanisms, commenting on the fragmentation
2. **🔑 关键转换**：烯胺→共轭加成→烯胺交换（可逆性）→环化→N-甲基化→O⁻推动碎片化→C-N⁺键+C-C键断裂
3. **验证**：检查烯胺交换是否合理（可逆性）；检查立体化学——1,3-桥双直立键、吡咯烷赤道位、顺式稠合；检查碎片化中三个关键轨道是否平行

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为步骤2的产物直接环化 | 没有认识到需要烯胺交换 | 必须先进行烯胺交换（酮→醛烯胺），才能环化得到目标中间体 | 为什么烯胺形成是可逆的？ |
| 立体化学画错 | 没考虑构象要求 | 1,3-桥必须是双直立键，吡咯烷是赤道位，五元环顺式稠合 | 为什么1,3-桥必须是双直立键？ |
| 忘记N-甲基化 | 直接画碎片化 | 必须先甲基化氮使其成为好的离去基团（季铵盐），碎片化才能发生 | 为什么吡咯烷本身不是好的离去基团？ |
| 碎片化轨道不平行 | 没检查反式共面关系 | C-N⁺键、断裂C-C键、O⁻孤对电子必须平行（反式共面） | 如何验证三个轨道是否平行？ |