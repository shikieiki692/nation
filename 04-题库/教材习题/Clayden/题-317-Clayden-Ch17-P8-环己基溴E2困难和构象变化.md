---
title: 题-317-Clayden-Ch17-P8-环己基溴E2困难和构象变化
type: 题目
fidelity: 原书逐字
submodule: 消除反应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["3.2"]
knowledge_points: ["[[E2反应]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch17-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 17 Problem 8
cross_references: ["[[题-299-Clayden-Ch15-P1-SN1与SN2机理判断]]", "[[题-310-Clayden-Ch17-P1-两个消除反应机理]]", "[[题-297-Clayden-Ch14-P7-RS构型标注]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-317: 环己基溴E2困难和构象变化

## 题目

Why is it difficult (though not impossible) for cyclohexyl bromide to undergo an E2 reaction? What conformational changes must occur during this reaction?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/9342eb1563d0ca085e95e3be3682f858d45f586605da14414ffb37a9fe1eea9d.jpg]]

**原文题目**：

为什么环己基溴进行E2反应困难（虽然不是不可能）？这个反应过程中必须发生什么构象变化？

## 参考答案

**Answer (English)**:

Cyclohexyl bromide prefers the chair conformation with the bromine equatorial. It cannot do an E2 reaction in this conformation as E2 requires the reacting C–H and C–Br bonds to be anti-periplanar. This can be achieved if the molecule first flips to put the C–Br bond in an unfavourable axial conformation.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/d79eb44eca13e599537327219ba451e278a32c064dcb4892ca595d49577bf416.jpg]]

**中文解析**：

这是一个关于环己烷构象与E2反应关系的经典问题。

**1. 环己基溴的优选构象**

```
平伏Br（稳定）：          轴向Br（不稳定）：
    H                           Br
     \                         /
      C---C---Br (平伏)       C---C---H (轴向)
     /     \                 /     \
    H       H               H       H
```

- 平伏Br：Br在环平面外，空间位阻小，能量低
- 轴向Br：Br在环平面上下，有1,3-二直立相互作用，能量高
- 能量差：~2 kcal/mol，平衡强烈偏向平伏构象

**2. 为什么平伏Br阻止E2**

E2要求H和Br处于**反式共平面**位置：

```
反式共平面：
    H
     \
      C---C---Br
     /     \
    (两个键在环的两侧，180°二面角)
```

当Br在平伏位置时：
- 所有相邻碳上的C-H键都与Br处于**邻位交叉**（gauche）关系
- **没有一个β-氢**与Br处于反式共平面
- E2的立体化学要求无法满足
- 因此E2无法发生

**3. E2所需的构象翻转**

要进行E2，环必须翻转：

```
翻转前（平伏Br）：          翻转后（轴向Br）：
    H                           H
     \                         /
      C---C---Br (平伏)       C---C---Br (轴向)
     /     \                 /     \
    H       H               H       H

                              +
    H (轴向)
     \
      C---C---Br (轴向)
     /     \
    H       H

    H和Br都在轴向，反式共平面！
```

- 翻转后，Br变为轴向
- 有一个β-氢也是轴向
- 两个轴向键处于反式共平面位置
- E2可以发生

**E2困难的原因总结**：

| 因素 | 影响 |
|------|------|
| 平伏Br更稳定 | 平衡偏向平伏构象 |
| 平伏Br无反式共平面H | E2无法进行 |
| 轴向Br能量高 | 翻转需要能量 |
| 翻转后E2才发生 | 反应速率慢 |

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| E2反应 | E2的反式共平面要求 | 直接 |
| [[构象分析]] | 环己烷的构象翻转 | 直接 |
| [[反式共平面]] | E2的立体化学要求 | 间接 |

## 解题思路

1. **读题定位**：环己基溴的E2反应困难，需要从构象角度分析
2. **🔑 关键转换**：平伏Br更稳定 → 但平伏Br无反式共平面H → 必须翻转到轴向Br → E2才能发生
3. **验证**：检查翻转后是否有轴向H与轴向Br处于反式共平面

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为环己基溴的E2很容易 | 没有考虑构象要求 | 平伏Br无法满足反式共平面 | 为什么环己基溴的E2比链状溴代烷慢？ |
| 混淆平伏和轴向的稳定性 | 忽略了1,3-二直立相互作用 | 平伏构象更稳定（空间位阻小） | 什么因素会稳定轴向构象？ |
| 没有理解反式共平面的几何要求 | 只考虑了电子效应 | 反式共平面是E2的必要条件 | 在环己烷中，两个轴向键的二面角是多少？ |