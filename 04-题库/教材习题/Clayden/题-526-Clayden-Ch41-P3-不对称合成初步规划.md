---
title: 题-526-Clayden-Ch41-P3-不对称合成初步规划
type: 题目
fidelity: 原书逐字
submodule: 不对称合成
exam_stage: 决赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[不对称合成]]", "[[手性中心]]"]
tags: [化竞, Clayden, 有机化学, 不对称合成]
updated: 2026-07-25
aliases: [Clayden-Ch41-P3]
source: Clayden Organic Chemistry 2nd Ed. Chapter 41 Problem 3
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]", "[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
---
# 题-526: 不对称合成初步规划

## 题目

How would you make enantiomerically enriched samples of these compounds (either enantiomer)?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/00efd358cf9e5f0e94c17eac9ea08967b476efd510b610043e52b1606017cdbb.jpg]]

**原文题目**：How would you make enantiomerically enriched samples of these compounds (either enantiomer)?

## 参考答案

**Answer (English)**: There are many possible answers here. What we had in mind was some sort of asymmetric Diels-Alder reaction for the first, an asymmetric aldol for the second or else opening an epoxide made by Sharpless epoxidation, asymmetric dihydroxylation for the third, and perhaps asymmetric dihydroxylation of a Z-alkene for the fourth. Of course you might have used resolution or asymmetric hydrogenation, or the chiral pool, or any other strategy from chapter 41.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/ff7c8a762b6d756bbc2cc275487bbcb317bdf20abd221b8dcfc5a1619aa8f209.jpg]]

**中文解析**：

**整体策略分析**：
本题考查不对称合成的初步规划能力——面对四个不同的手性目标分子，能够识别其结构特征并匹配合适的不对称合成方法。这要求学生掌握第四十一章中介绍的各类不对称合成策略：不对称催化还原、Sharpless不对称环氧化、不对称双羟化、手性助剂法、拆分法、手性池策略等。

**四个目标分子的策略分析**：

1. **第一个化合物——含手性中心的环状结构**：
   - 结构特征：环己烯骨架上的手性中心，具有两个取代基
   - 推荐策略：**不对称Diels-Alder反应**——这是构建含手性中心六元环的最直接方法
   - 也可以考虑：Sharpless不对称环氧化 + 环氧化物开环，或手性助剂法
   - 为什么选DA反应：DA反应天然构建六元环，使用手性二烯体或亲二烯体可控制产物的绝对构型

2. **第二个化合物——含1,3-二羟基结构的链状分子**：
   - 结构特征：具有1,3-二醇关系（β-羟基酮/醇的还原产物）
   - 推荐策略：**不对称Aldol反应**——直接构建1,3-二羟基关系
   - 也可考虑：Sharpless不对称环氧化后选择性开环
   - 为什么选Aldol：Aldol反应是构建β-羟基羰基化合物的经典方法，Evans手性助剂法或脯氨酸催化Aldol可获得高ee值

3. **第三个化合物——含氨基和羟基的手性中心**：
   - 结构特征：具有1,2-官能团化（OH和NH₂在相邻碳上）
   - 推荐策略：**Sharpless不对称环氧化**，随后亲核试剂（如叠氮化物）开环
   - 也可考虑：不对称双羟化，或拆分法
   - 为什么选Sharpless：1,2-官能团化是环氧化-开环策略的经典应用

4. **第四个化合物——含手性中心的二醇**：
   - 结构特征：相邻碳上的两个羟基（1,2-二醇）
   - 推荐策略：**不对称双羟化（Sharpless AD）**——直接从Z-烯烃出发，一步构建邻二醇
   - 为什么选AD：邻二醇是不对称双羟化反应的直接产物

**关键教学要点**：
- 本题答案是开放性的，多种策略都可行——这体现了不对称合成规划的灵活性
- 核心能力是"结构特征→合成方法"的匹配：识别目标分子中的关键结构特征，然后选择最可靠的方法构建它
- 其他可行策略包括：拆分法、不对称氢化、手性池策略等——任何第四十一章介绍的方法都可以尝试

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[不对称合成]] | 根据目标结构特征选择不对称合成方法 | 直接 |
| [[手性中心]] | 识别目标分子中需要构建的手性中心 | 直接 |
| [[合成设计]] | 逆合成分析中匹配目标特征与合成方法 | 直接 |
| 不对称Diels-Alder | 构建含手性中心六元环的策略 | 间接 |
| [[Sharpless不对称环氧化]] | 构建1,2-官能团化手性中心 | 间接 |
| [[不对称双羟化]] | 构建邻二醇手性中心 | 间接 |

## 解题思路

1. **读题定位**：题目要求为四个手性目标分子设计不对称合成路线（任何对映体均可）。关键词：对映体富集、合成设计、开放性答案
2. **🔑 关键转换**：逐一分析每个目标的结构特征——(a) 环状结构→Diels-Alder；(b) 1,3-二醇→Aldol；(c) 1,2-官能团化→Sharpless环氧化+开环；(d) 邻二醇→不对称双羟化
3. **验证**：检查每个策略是否能从简单原料出发，经过合理步骤得到目标分子，且立体化学可控

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 对每个目标都选同一种方法 | 没有分析不同结构特征对应不同方法 | 不同结构特征需要不同策略：环→DA，邻二醇→AD，β-羟基→Aldol | 为什么邻二醇优先选AD而不是环氧化+水解？ |
| 只列出一种方法就停止 | 不对称合成规划的思维局限 | 本题是开放性的，应列出多种可能策略并说明选择理由 | 如果AD反应在某个底物上ee值不高，还有什么替代方案？ |
| 混淆Sharpless环氧化和双羟化 | 对两类反应的底物/产物不熟 | 环氧化→环氧化物（三元环醚），双羟化→邻二醇（两个OH） | Sharpless环氧化的底物要求是什么（烯丙醇）？ |
| 忽略手性池和拆分策略 | 只关注催化不对称方法 | 不对称合成策略不限于催化方法，拆分和手性池也是重要选择 | 什么情况下拆分比不对称催化更实用？ |