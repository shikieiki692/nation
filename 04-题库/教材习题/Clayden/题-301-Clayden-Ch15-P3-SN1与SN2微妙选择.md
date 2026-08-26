---
title: 题-301-Clayden-Ch15-P3-SN1与SN2微妙选择
type: 题目
fidelity: 原书逐字
submodule: 亲核取代反应
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["3.2"]
knowledge_points: ["[[SN1反应]]", "[[SN2反应]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch15-P3]
source: Clayden Organic Chemistry 2nd Ed. Chapter 15 Problem 3
cross_references: ["[[题-299-Clayden-Ch15-P1-SN1与SN2机理判断]]", "[[题-308-Clayden-Ch15-P10-四个反应SN1与SN2判断]]"]
module: 有机化学
status: 已填充
---
# 题-301: SN1与SN2微妙选择

## 题目

For each of the following reactions, decide whether an SN1 or SN2 mechanism is operating and explain your choice:

1. A dichloride with two secondary chlorides, one adjacent to an oxygen atom, reacting with MeOH → product with one Cl replaced by OMe
2. A primary chloride site reacts selectively over a secondary chloride in the presence of a nucleophile

**原文题目**：

对于下列反应，判断各是按SN1还是SN2机理进行，并解释理由：

1. 一个含有两个仲氯原子的二氯化物，其中一个氯原子位于氧原子邻位，与甲醇反应后，只有一个Cl被OMe取代
2. 一个伯氯位点在有亲核试剂存在时优先于仲氯发生反应

## 参考答案

**Answer (English)**:

1. **SN1 mechanism**. The secondary chloride adjacent to the oxygen is preferentially ionized because the lone pairs on oxygen can stabilize the resulting carbocation through resonance (forming an oxonium ion). This makes ionization much faster at this position. The second Cl (not adjacent to O) is slow to ionize and remains unchanged.

2. **SN2 mechanism**. The primary chloride is much less sterically hindered than the secondary chloride, so it reacts preferentially via SN2 with the nucleophile. In SN2, steric effects dominate — primary substrates react much faster than secondary ones.

**中文解析**：

1. **SN1机理**：氧原子邻位的仲氯原子之所以优先反应，是因为当这个C-Cl键异裂形成碳阳离子时，氧原子的孤对电子可以通过共振稳定碳阳离子（形成氧鎓离子结构）。这种邻位氧原子对碳阳离子的稳定作用使得该位置的电离速率大大加快。而另一个仲氯原子不在氧的邻位，缺乏这种稳定作用，因此不发生反应。这是一个典型的选择性SN1反应。

2. **SN2机理**：伯碳底物在SN2反应中比仲碳底物快得多，因为空间位阻是SN2反应速率的决定性因素。亲核试剂需要从离去基团的背面进攻碳原子，伯碳的空间位阻最小，仲碳则有更大的位阻。因此，在两个氯原子中，伯氯优先发生SN2取代。

**判断SN1 vs SN2的关键依据**：

| 判断因素 | SN1倾向 | SN2倾向 |
|---------|---------|---------|
| 底物结构 | 稳定碳阳离子（叔碳、烯丙基、苄基） | 空间位阻小（甲基、伯碳） |
| 溶剂/亲核试剂 | 弱亲核试剂、极性质子溶剂 | 强亲核试剂、极性非质子溶剂 |
| 电子效应 | 邻位给电子基团稳定碳阳离子 | 邻位吸电子基团活化SN2过渡态 |

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| SN1反应 | 邻位氧原子对碳阳离子的稳定作用 | 直接 |
| SN2反应 | 伯碳vs仲碳的空间位阻差异 | 直接 |
| [[亲核取代]] | SN1与SN2的竞争和判断 | 间接 |

## 解题思路

1. **读题定位**：两个反应分别考察SN1和SN2的判断依据——电子效应（碳阳离子稳定化）vs空间效应
2. **🔑 关键转换**：反应1：氧原子孤对电子共振稳定碳阳离子 → SN1选择性；反应2：伯碳空间位阻小于仲碳 → SN2选择性
3. **验证**：反应1中如果底物是伯碳，即使有邻位氧也可能走SN2；反应2中如果用弱亲核试剂/质子溶剂，两个Cl可能都不反应

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 反应1认为是SN2 | 没有识别出邻位氧的碳阳离子稳定化作用 | 氧的孤对电子可共振稳定碳阳离子，这是SN1的典型特征 | 如果将氧换成硫原子，效果是否相同？ |
| 反应2认为是SN1 | 没有注意到两个Cl的结构差异 | 伯碳vs仲碳的空间位阻差异是SN2选择性的基础 | 什么条件下仲碳的SN2会比伯碳快？ |
| 混淆电子效应和空间效应的适用场景 | 没有建立系统的判断框架 | 碳阳离子稳定化→SN1；空间位阻→SN2 | 什么时候两种效应会同时起作用？ |