---
title: 题-364-Clayden-Ch11-P8-Dapsone亚硫酸氢加合物（前药）机理
type: 题目
fidelity: 原书逐字
submodule: 缩醛与亚胺
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
question_type: [机理]
teaching_level: 竞赛
syllabus_codes: ["21"]
knowledge_points: ["[[羰基亲核加成]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch11-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 11 Problem 8
cross_references: ["[[题-328-Clayden-Ch20-P1-羰基化合物烯醇式绘制和稳定性]]", "[[题-263-Clayden-Ch6-P2-环丙酮水合vs半缩醛稳定性]]", "[[题-262-Clayden-Ch6-P1-硼氢化钠还原醛酮机理]]", "[[题-329-Clayden-Ch20-P2-两个酮烯醇含量差异解释]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
source_grade: B
---
# 题-364: Dapsone亚硫酸氢加合物（前药）机理

## 题目

**【中文】**在第 6 章中，我们介绍了抗麻风病药物氨苯砜（dapsone）如何通过形成"亚硫酸氢盐加合物"（bisulfite adduct）而变得可溶。现在你已经了解了第 11 章所述的反应，应当能够为该反应画出机理。该加合物被称为"前药"（prodrug），意思是它本身不是药物，而是在体内通过化学反应生成药物。这一过程可能如何发生？（反应式见图）

**【原文】**In chapter 6 we described how the anti-leprosy drug dapsone could be made soluble by the formation of a 'bisulfite adduct'. Now that you know about the reactions described in chapter 11, you should be able to draw a mechanism for this reaction. The adduct is described as a 'prodrug', meaning that it is not the drug but gives rise to the drug by chemistry within the body. How might this happen?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/428ea5a97d5d4306d96d6a543614d5226f7b592e8a49d3c0f916a485e601c92b.jpg]]

## 参考答案

**Answer (English)**:

**The trap**: The trap is to go straight to the product by displacing hydroxide ion from the formaldehyde bisulfite adduct. Hydroxide is a very bad leaving group and reactions like this never occur.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/c916d5b1e6869a4e85cd315122fe61dbbc5696d65921ac39ff12a928e93c9aea.jpg]]

**The correct mechanism**: To avoid this trap we must use carbonyl chemistry. First we must make formaldehyde from its adduct and add it to the amino group of dapsone.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/f5730c11b8a2edb5aee972716e71c9cb7c11f82f260fd3a147ec05931fa863e7.jpg]]

Now we can form an iminium salt and add the bisulfite back into this reactive electrophile to give the final product. This is loss of carbonyl oxygen in an unusual setting as the carbonyl was not there at the start and is present only in the intermediates.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/e72deca17cb88218aca0b5efd1999d6f439326d68e77dca98e84f3b33ae42ffa.jpg]]

**中文解析**：

本题是一个极具迷惑性的机理题——正确答案需要避开一个"陷阱"。同时涉及前药（prodrug）的概念。

**陷阱分析**：
- **错误做法**：直接用dapsone的NH₂进攻甲醛-亚硫酸氢加合物，同时取代OH⁻
- **为什么错**：OH⁻是极差的离去基团——这种直接取代反应永远不会发生
- 很多学生会犯这个错误，因为看起来"简洁"

**正确机理（三步）**：

**步骤1：甲醛从亚硫酸氢加合物中释放**
- 亚硫酸氢加合物在体内酸性环境下可逆分解，释放出游离的甲醛（CH₂O）
- 这就是"前药"的原理——加合物在体内释放活性分子

**步骤2：甲醛与dapsone的NH₂反应形成亚胺**
- 甲醛的C=O与dapsone的芳胺基（ArNH₂）反应
- 经典的亚胺形成：亲核加成 → 脱水 → C=N双键
- 生成亚胺离子（iminium ion）

**步骤3：亚硫酸氢根捕获亚胺离子**
- 亚硫酸氢根（HSO₃⁻）作为亲核试剂进攻亚胺离子的碳
- 形成C-S键，得到最终的前药产物
- 这就是"羰基氧的失去"——羰基氧在亚胺形成步骤中以水的形式失去

**前药原理**：
- 前药（prodrug）本身没有药理活性，在体内经过化学转化释放出活性药物
- Dapsone的亚硫酸氢加合物增加了水溶性（便于给药），在体内分解释放出dapsone

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[羰基亲核加成]] | 亚硫酸氢加合物的形成和分解机理 | 直接 |
| [[亚胺]] | 甲醛与胺形成亚胺离子是关键中间步骤 | 直接 |
| [[羧酸衍生物]] | OH⁻作为离去基团的局限性——理解离去基团能力 | 间接 |

## 解题思路

1. **读题定位**：题目涉及dapsone的亚硫酸氢加合物形成机理。提示这与第11章内容相关，且是"前药"
2. **🔑 关键转换**：识别陷阱——不能直接取代OH⁻。正确路径是先释放甲醛 → 形成亚胺离子 → 亚硫酸氢根捕获亚胺离子
3. **验证**：检查最终产物结构是否与题目一致；检查是否所有步骤都有合理的离去基团和亲核试剂

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 直接用NH₂取代OH⁻（最常见陷阱） | 没有考虑OH⁻的离去能力 | OH⁻是极差的离去基团（pKa of H₂O = 15.7），直接取代不会发生 | 哪些基团是好的离去基团？它们有什么共同特点？ |
| 忽略前药的体内转化 | 不理解"prodrug"的含义 | 前药在体外稳定，在体内经酶或酸碱催化分解释放活性分子 | 前药设计的目的是什么？有哪些类型？ |
| 机理中步骤顺序混乱 | 没有理清"释放甲醛 → 形成亚胺 → 捕获"的逻辑链 | 必须先释放游离甲醛，然后甲醛与胺反应形成亚胺离子，最后亚硫酸氢根捕获 | 为什么亚胺离子比醛酮更容易被亚硫酸氢根进攻？ |