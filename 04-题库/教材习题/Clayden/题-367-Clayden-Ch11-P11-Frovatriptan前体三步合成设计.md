---
title: 题-367-Clayden-Ch11-P11-Frovatriptan前体三步合成设计
type: 题目
fidelity: 原书逐字
submodule: 缩醛与亚胺
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 竞赛
syllabus_codes: ["21"]
knowledge_points: ["[[逆合成分析]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch11-P11]
source: Clayden Organic Chemistry 2nd Ed. Chapter 11 Problem 11
cross_references: ["[[题-328-Clayden-Ch20-P1-羰基化合物烯醇式绘制和稳定性]]", "[[题-329-Clayden-Ch20-P2-两个酮烯醇含量差异解释]]", "[[题-263-Clayden-Ch6-P2-环丙酮水合vs半缩醛稳定性]]", "[[题-262-Clayden-Ch6-P1-硼氢化钠还原醛酮机理]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
---
# 题-367: Frovatriptan前体三步合成设计

## 题目

**【中文】**三个化学步骤可将环己烷-1,4-二酮转化为一种用于合成抗偏头痛药物 frovatriptan（夫罗曲坦）的化合物。提出如何实现这一转化。（提示：涉及缩醛保护与还原胺化；反应式见图）

**【原文】**Three chemical steps convert cyclohexane-1,4-dione into a compound which is used for the synthesis of the anti-migraine drug frovatriptan. Suggest how this transformation is carried out.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/e3e84bd56a7d352d4dbc48f6658327a501e3a2dcfa9dacc11428d9f7aa1a7531.jpg]]

## 参考答案

**Answer (English)**: Both carbonyl groups have undergone substitution. One of them is converted to an acetal, so we must treat the ketone with a diol and an acid catalyst.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/a2f64f5545870f754720a03fe8a9bede37f88f664b224c43be734d13b45d6b24.jpg]]

The other ketone must be converted into an amine, so we can use reductive amination: we could first make the imine with methylamine, and reduce it; alternatively we can use NaCNBH₃ to reduce the imine as it forms.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/ece1f5d69fdcca8242144b1497d13c75331fb879a1f45fd0c5b459f121b5ad2b.jpg]]

**中文解析**：

本题是一个真实的药物合成设计问题——将1,4-环己二酮转化为Frovatriptan（抗偏头痛药物）的前体。需要三步完成。

**逆合成分析**：
- **起始原料**：1,4-环己二酮（两个酮羰基）
- **目标产物**：一个酮羰基被缩醛保护，另一个酮羰基被转化为甲氨基（-NHMe）
- **需要的转化**：一个C=O → 缩醛（保护），另一个C=O → C-N（还原胺化）

**三步合成路线**：

**Step 1：选择性缩醛保护**
- 试剂：乙二醇（HOCH₂CH₂OH）+ 酸催化剂（如p-TsOH）
- 条件：苯中回流，Dean-Stark分水器除水
- 产物：一个酮形成环状缩醛（1,3-二氧戊环），另一个酮保留
- **选择性**：1,4-位的两个酮在空间上远离，可以用当量的二醇控制只保护一个

**Step 2：还原胺化**
- 试剂：甲胺（MeNH₂）+ NaCNBH₃
- 条件：弱酸性（pH 6-7）
- 机理：
  1. MeNH₂与保留的酮羰基反应形成亚胺（C=NMe）
  2. NaCNBH₃选择性还原亚胺为胺（C-NHMe），不还原缩醛
- 产物：缩醛保护的酮 + 甲氨基

**Step 3：脱保护（可选/后续步骤）**
- 如果需要，可以用稀酸水解脱去缩醛保护基
- 但在Frovatriptan合成中，缩醛可能在后续步骤中保留

**关键设计思路**：
1. **保护基策略**：先保护一个酮，再对另一个酮进行化学转化
2. **还原胺化**：NaCNBH₃是关键试剂——选择性还原亚胺而不影响缩醛
3. **化学选择性**：缩醛对还原剂稳定，这是它作为保护基的核心优势

> **药物合成意义**：Frovatriptan是治疗急性偏头痛的triptan类药物。1,4-环己二酮是其合成的关键中间体，通过保护基策略和还原胺化实现官能团的差异化转化。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[逆合成分析]] | 从目标产物反推合成路线，识别需要的转化 | 直接 |
| [[亚胺]] | 还原胺化中亚胺中间体的形成和还原 | 直接 |
| [[保护基策略]] | 缩醛保护基在多步合成中的选择性应用 | 间接 |

## 解题思路

1. **读题定位**：比较起始原料（1,4-环己二酮）和目标产物的结构差异——一个C=O变为缩醛，另一个C=O变为C-NHMe
2. **🔑 关键转换**：需要保护基策略——先用缩醛保护一个酮（使其在后续反应中惰性），再用还原胺化转化另一个酮为胺
3. **验证**：检查三步反应的选择性——缩醛保护不影响另一个酮；NaCNBH₃还原亚胺不影响缩醛；最终产物结构与目标一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 试图一步同时转化两个酮 | 没有理解选择性转化需要保护基 | 两个酮化学环境相同，必须先保护一个，才能选择性转化另一个 | 如果不使用保护基，有什么方法可以实现选择性？ |
| 还原胺化时使用LiAlH₄ | 误认为需要强还原剂 | NaCNBH₃在酸性条件下选择性还原亚胺；LiAlH₄会同时还原缩醛 | 为什么NaCNBH₃比NaBH₄更适合还原胺化？ |
| 缩醛保护的条件选择错误 | 没有考虑热力学控制 | 缩醛形成是可逆反应——需要用Dean-Stark分水器除水，推动平衡向产物方向 | 为什么缩醛形成需要除水？勒夏特列原理如何应用？ |