---
title: 题-596-Clayden-Ch33-P1-开链化合物立体化学控制入门
type: 题目
fidelity: 原书逐字
submodule: 非对映选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 2
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[非对映选择性]]"]
tags: [化竞, Clayden, 有机化学, 非对映选择性]
updated: 2026-07-25
aliases: [Clayden-Ch33-P1]
source: Clayden Organic Chemistry 2nd Ed. Chapter 33 Problem 1
cross_references: ["[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
source_grade: B
---
# 题-596: 开链化合物立体化学控制入门

## 题目

How would you make each diastereoisomer of this product from the same alkene?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/85fe38d944b93101e525a14cf1801c2f89393b958371382d9e43c669692bd16a.jpg]]

## 参考答案

**Answer (English)**: The compounds are acetals and can be made from the corresponding diols with no change in stereochemistry. The question really is: how do you make cis and trans diols from the alkene?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/f5e144f247083c021bc318bde6572944d75211d2244d2af4d18f15f7fdba3d79.jpg]]

The cis diol is best made by dihydroxylation with OsO₄ as the reagent and a co-oxidant to regenerate it. The trans diol comes from the epoxide by nucleophilic attack with water.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/21b4ad3d557aabc56e3afaa6c4cbbf490f51f54dc5c44f27761e40b95dc7282d.jpg]]

**中文解析**：

关键步骤：
1. **分析产物结构**：目标产物是缩醛，可以由相应的二醇制备而不改变立体化学。问题的核心是：如何从同一个烯烃分别制备顺式和反式二醇？
2. **顺式二醇**：用OsO₄进行双羟基化反应，OsO₄从双键的同侧加成两个OH，得到顺式二醇。需要共氧化剂（如NMO）来再生OsO₄
3. **反式二醇**：先用mCPBA进行环氧化，然后水作为亲核试剂开环（S_N2反式进攻），得到反式二醇

> **核心概念**：从同一烯烃制备不同立体化学的产物是有机合成的基本策略。OsO₄双羟基化给出顺式产物（顺式加成），而环氧化+水开环给出反式产物（两次反式开环的净结果）。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[非对映选择性]] | 从同一底物制备不同非对映异构体 | 直接 |
| [[立体化学]] | 顺式vs反式加成的立体化学结果 | 直接 |
| [[手性中心]] | 双羟基化和环氧化开环建立手性中心 | 间接 |

## 解题思路

1. **读题定位**：从同一烯烃制备两种非对映异构体——识别产物为缩醛，关键在二醇的立体化学
2. **关键转换**：缩醛←二醇（立体化学不变）→顺式二醇用OsO₄，反式二醇用mCPBA/H₂O
3. **验证**：检查OsO₄给出顺式二醇（同侧加成），环氧化+水开环给出反式二醇（两次反式开环）

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 混淆OsO₄和mCPBA的立体化学结果 | 死记硬背 | OsO₄是顺式加成（同侧），mCPBA+H₂O是反式开环 | 为什么OsO₄是顺式加成？ |
| 忘记缩醛化不影响立体化学 | 深化水解条件 | 缩醛化只涉及C-O键形成，不影响手性中心 | 缩醛保护的条件是什么？ |
| 认为环氧化水开环是顺式 | 未理解S_N2反式开环 | S_N2开环必须反式，两次反式的结果是反式二醇 | 环氧化物的酸催化开环也是反式吗？ |