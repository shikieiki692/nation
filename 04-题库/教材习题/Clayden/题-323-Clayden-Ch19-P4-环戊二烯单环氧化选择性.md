---
title: 题-323-Clayden-Ch19-P4-环戊二烯单环氧化选择性
type: 题目
fidelity: 原书逐字
submodule: 烯烃的亲电加成
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
question_type: [简答]
teaching_level: 拓展
syllabus_codes: ["2.3"]
knowledge_points: ["[[环氧化合物]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch19-P4]
source: Clayden Organic Chemistry 2nd Ed. Chapter 19 Problem 4
cross_references: ["[[题-400-Clayden-Ch22-P10-环戊烯酮还原共轭vs直接加成顺序]]", "[[题-392-Clayden-Ch22-P2-共轭加成本质和不发生的情况]]", "[[题-336-Clayden-Ch7-P1-共轭判断和弯曲箭头表示]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
source_grade: B
---
# 题-323: 环戊二烯单环氧化选择性

## 题目

**【中文】**环戊二烯在低温、缓冲溶液条件下，与一当量 m-CPBA 反应。预测产物并解释选择性。

**【原文】**
Cyclopentadiene is treated with one equivalent of m-CPBA at low temperature, in buffered solution. Predict the product and explain the selectivity.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/ff024f867994b07cb762bd405c5891c688f233534d458434ee6389b398a84f80.jpg]]

## 参考答案

**Answer (English)**:

The product is **cyclopentadiene monoepoxide** (3,6-epoxycyclopent-1-ene or 2-oxabicyclo[2.1.0]pent-3-ene). The epoxidation occurs on one double bond, not both.

**Reason for selectivity**: In a conjugated diene, the HOMO has higher energy than that of an isolated alkene because of the extended π-conjugation. This makes cyclopentadiene's double bonds more electron-rich and thus more reactive toward the electrophilic peracid (m-CPBA) than a typical isolated alkene. However, with only one equivalent of m-CPBA, only one double bond reacts.

The first epoxidation removes one double bond from conjugation. The remaining double bond is now an **isolated** alkene, which is less electron-rich (lower HOMO) and therefore less reactive toward a second equivalent of m-CPBA. This is why low temperature and stoichiometric control allow clean **monoepoxidation**.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/6979d916a362583a0013b4325e4f5186f94083caeaa098cb40938748183f544e.jpg]]

HOMO of the diene

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/cca4d590fd3e2325d9eae20795c373f4e370059d3f628d0ecf5cfd9efcf99cec.jpg]]

**Buffer** is needed because the epoxide product is acid-sensitive: m-CPBA generates m-chlorobenzoic acid as a byproduct, and acid can catalyze ring-opening of the epoxide. The buffer neutralizes the acid.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/f8fdd23275ddaeb1186bcef3489765ad4e71178a77ff8807f0719f919d15ad9d.jpg]]

danger of decomposition by allyl cation formation

**中文解析**：

**产物**：环戊二烯单环氧化物（一个双键被环氧化，另一个保持不变）。

**选择性解释**：

1. **共轭二烯的HOMO能量更高**：环戊二烯的两个双键共轭，π电子离域使 HOMO 能量升高（相比孤立双键），因此更容易与亲电试剂 m-CPBA 反应。这使得共轭二烯比普通烯烃更活泼。

2. **单环氧化后活性骤降**：第一个双键环氧化后，剩余的双键变成**孤立烯烃**，不再共轭，HOMO 能量下降，对第二当量 m-CPBA 的反应活性显著降低。因此在低温+一当量条件下，反应停在单环氧化阶段。

3. **缓冲溶液的作用**：m-CPBA 反应后生成 m-氯苯甲酸（副产物），酸性条件会催化环氧化合物的开环。缓冲液中和生成的酸，保护环氧化物产物不被酸催化降解。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[环氧化合物]] | m-CPBA环氧化机理及环氧化产物的酸敏感性 | 直接 |
| [[亲电加成]] | 共轭二烯HOMO能量升高→对亲电试剂更活泼 | 直接 |
| [[烯烃稳定性]] | 共轭烯烃vs孤立烯烃的反应活性差异 | 间接 |

## 解题思路

1. **读题定位**：共轭二烯 + 1 eq m-CPBA + 低温 + 缓冲 → 问单环氧化的选择性
2. **🔑 关键转换**：共轭二烯HOMO高→优先反应→产物变为孤立烯→活性下降→停在单环氧化；缓冲液防止酸催化开环
3. **验证**：检查是否解释了为什么只反应一个双键（电子效应）和为什么需要缓冲（酸敏感性）

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为两个双键都会被环氧化 | 忽视了共轭→孤立后活性变化 | 第一个环氧化后剩余孤立双键活性显著降低 | 如何用更高当量m-CPBA实现双环氧化？ |
| 认为环氧化发生在"更稳定的双键"上 | 共轭二烯中两个双键是等价的 | 两个双键对称等价，任一均可反应 | 如果两个双键不对称，优先级如何判断？ |
| 忽略缓冲液的作用 | 不了解m-CPBA副产物是酸 | m-氯苯甲酸副产物会催化环氧化物开环 | 什么条件下环氧化物最容易被酸催化开环？ |