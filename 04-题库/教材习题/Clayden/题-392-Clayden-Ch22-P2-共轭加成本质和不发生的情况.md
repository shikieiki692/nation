---
title: 题-392-Clayden-Ch22-P2-共轭加成本质和不发生的情况
type: 题目
submodule: 共轭加成
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[共轭加成]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch22-P2]
source: Clayden Organic Chemistry 2nd Ed. Chapter 22 Problem 2
cross_references: ["[[题-321-Clayden-Ch19-P2-两个烯烃溴化机理和产物]]", "[[题-320-Clayden-Ch19-P1-HCl对三个烯烃加成方向]]", "[[题-628-Clayden-Ch38-P1-碱引发两个简单卡宾反应]]", "[[题-629-Clayden-Ch38-P2-另一种卡宾方法→天然抗生素]]"]
module: 有机化学
status: 已填充
---
# 题-392: 共轭加成本质和不发生的情况

## 题目

Which of the two routes suggested here would actually lead to the product?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/5642bc925c7b62117ce8ea3adc40645d2dd390166d24c8ea2fa3187114620e7c.jpg]]

**原文题目**：Which of the two routes would lead to the product? Determine the correct order of addition for HCl and EtMgBr to achieve conjugate addition of chloride and direct addition of ethyl group.

## 参考答案

**Answer (English)**: To get the product, the chloride must add in a conjugate fashion and ethyl Grignard in a direct fashion that removes the carbonyl group. Conjugate addition can happen only if the carbonyl group is intact so HCl must be added first.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/7e7f2fa0300d2d23da0dbdf9c2510cb2f06daab623faa67ab5bfe22bc2469e8c.jpg]]

In the other sequence, EtMgBr is likely to add to the carbonyl group direct and further addition of HCl may either substitute on the allylic alcohol or add the 'wrong way round' to the alkene.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/14346801e7bef4f5a623369c11b30fdc58bd5dc794b2135491c00b35039fa2c8.jpg]]

**中文解析**：

关键步骤：
1. **共轭加成的前提**：共轭加成（1,4-加成）要求羰基（C=O）必须保持完整。只有在羰基存在时，β-碳才因共轭而带有部分正电荷，才能被亲核试剂进攻
2. **路线1（正确）**：先加HCl → Cl⁻作为亲核试剂对烯酮进行共轭加成（1,4-加成）→ 再加EtMgBr → Grignard试剂作为硬亲核试剂对羰基进行直接加成（1,2-加成）→ 水解得叔醇
3. **路线2（错误）**：先加EtMgBr → Grignard试剂直接加成到羰基（1,2-加成）→ 羰基被消耗 → 无法进行共轭加成 → 后续加HCl会发生烯丙位取代或其他副反应

> **核心概念**：共轭加成需要羰基作为"活化基团"来使β-碳缺电子。一旦羰基被还原或加成，共轭加成就不可能了。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[共轭加成]] | 共轭加成对羰基完整性的依赖 | 直接 |
| [[Michael加成]] | 亲核试剂对α,β-不饱和羰基化合物的选择性加成 | 直接 |
| [[亲核加成]] | 1,2-直接加成和1,4-共轭加成的竞争 | 间接 |

## 解题思路

1. **读题定位**：题目问两条路线哪条能得到产物——产物需要Cl在β位（共轭加成产物），Et在羰基碳上（直接加成产物）
2. **🔑 关键转换**：共轭加成需要C=O完整 → 必须先加HCl（共轭加成）再加EtMgBr（直接加成）→ 顺序不能颠倒
3. **验证**：检查产物结构——Cl是否在β位？Et是否在原羰基碳上？水后处理是否正确？

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为EtMgBr可以共轭加成 | 没有区分软/硬亲核试剂 | Grignard试剂是硬亲核试剂，优先进行1,2-直接加成 | 如何让Grignard试剂进行共轭加成？ |
| 忽略C=O完整性对共轭加成的必要性 | 对共轭加成的活化机理理解不深 | 共轭加成依赖C=O的吸电子效应活化β-碳 | 为什么没有C=O就不能共轭加成？ |
| 先加EtMgBr再加HCl | 顺序颠倒导致副反应 | 先加HCl共轭加成，再加EtMgBr直接加成 | 如果先加EtMgBr会发生什么？ |