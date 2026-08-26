---
title: 题-319-Clayden-Ch17-P10-差向异构溴化物消除结果对比
type: 题目
fidelity: 原书逐字
submodule: 消除反应
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 竞赛拔高
syllabus_codes: ["3.2"]
knowledge_points: ["[[E1反应]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch17-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 17 Problem 10
cross_references: ["[[题-307-Clayden-Ch15-P9-两个反应的立体化学]]", "[[题-317-Clayden-Ch17-P8-环己基溴E2困难和构象变化]]", "[[题-294-Clayden-Ch14-P4-四个化合物立体化学讨论]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-319: 差向异构溴化物消除结果对比

## 题目

Account for the constrasting results of these two reactions.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/7d31a198b9b3e193e85d4930052cbb5f90f0ae446f82808722bd8a1e6277f8fe.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/337b259db4c02caebc38d821a43f22e1d39c602bb980057d90678136c56f7da3.jpg]]

**原文题目**：

解释这两个反应的对比结果。

## 参考答案

**Answer (English)**:

The two compounds differ only in their configuration, and as they both have a tert-butyl group they have no choice about their conformation. The bromide must be the leaving group, and when you draw the molecules you find that it must also be axial. In the first case there is a proton antiperiplanar to it that can lead to a conjugated alkene. In the second case, the bond antiperiplanar to the bromine is a C–C bond, but that's OK on this occasion because decarboxylation can take place by the mechanism shown. There is an antiperiplanar C–H bond on the other side of course, but the decarboxylation must be faster than simple E2 elimination.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/2126801c4cfb2c5d030c3ef9867933fd074e56cde44f5960beec4cebc167face.jpg]]

**中文解析**：

这是一个关于立体电子效应对反应途径控制的经典例子。

**非对映体A：正常E2消除**

```
    H (反式共平面)
     \
      C---C---Br
     /     \
    CO₂R    H
```

- β-氢与Br处于反式共平面位置
- E2的立体化学要求完全满足
- 碱夺取β-氢，形成共轭烯烃
- 产物稳定（共轭体系）

**非对映体B：脱羧反应**

```
    CO₂R (反式共平面)
     \
      C---C---Br
     /     \
    H       H
```

- 没有β-氢与Br反式共平面
- 但C-C(CO₂R)键与Br反式共平面
- 这个C-C键断裂（脱羧），而不是C-H键断裂
- 脱羧比E2更快，因为立体电子效应更有利

**为什么脱羧比E2更快？**

| 因素 | E2（非对映体A） | 脱羧（非对映体B） |
|------|----------------|------------------|
| 反式共平面键 | C-H | C-C(CO₂R) |
| 断键类型 | C-H断裂 | C-C断裂 |
| 产物 | 共轭烯烃 | 羧酸根+烯烃 |
| 速率 | 正常 | 更快 |

**立体电子效应的关键**：

- E2和脱羧都要求反式共平面几何
- 非对映体A中，C-H是反式共平面 → E2
- 非对映体B中，C-C是反式共平面 → 脱羧
- **构象决定反应途径**

**更深层的解释**：

脱羧反应之所以更快，是因为：
1. CO₂是一个很好的离去基团（稳定产物）
2. C-C键断裂的立体电子效应在反式共平面时最有利
3. 没有竞争的E2途径（无反式共平面H）

**结论**：
- 同一分子的不同非对映体可以走完全不同的反应途径
- 立体化学（构象）决定反应途径
- 反式共平面要求是E2和脱羧的共同特征

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| E1反应 | 无E1竞争（都是E2/脱羧） | 直接 |
| E2反应 | E2的反式共平面要求 | 直接 |
| [[立体化学]] | 非对映体构象对反应途径的影响 | 间接 |

## 解题思路

1. **读题定位**：两个非对映体消除结果不同，需要分析构象差异
2. **🔑 关键转换**：非对映体A有反式共平面H→E2；非对映体B有反式共平面C-C→脱羧
3. **验证**：检查两种情况的立体电子效应是否都有利

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为两个非对映体应该给出相同产物 | 没有考虑构象差异 | 不同构象导致不同反应途径 | 什么条件下非对映体会给出相同产物？ |
| 认为脱羧不如E2快 | 没有理解立体电子效应 | 在非对映体B中，脱羧的立体电子效应更有利 | 为什么反式共平面的C-C断裂比C-H断裂更快？ |
| 混淆E1和E2 | 没有识别出两种情况都是E2类反应 | 都是E2类反应（协同过程），不是E1 | 如何区分E1和E2？ |