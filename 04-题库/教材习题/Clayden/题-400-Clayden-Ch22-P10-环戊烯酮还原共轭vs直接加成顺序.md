---
title: 题-400-Clayden-Ch22-P10-环戊烯酮还原共轭vs直接加成顺序
type: 题目
submodule: 共轭加成
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 竞赛拔高
syllabus_codes: ["21"]
knowledge_points: ["[[共轭加成]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch22-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 22 Problem 10
cross_references: ["[[题-321-Clayden-Ch19-P2-两个烯烃溴化机理和产物]]", "[[题-320-Clayden-Ch19-P1-HCl对三个烯烃加成方向]]", "[[题-629-Clayden-Ch38-P2-另一种卡宾方法→天然抗生素]]", "[[题-628-Clayden-Ch38-P1-碱引发两个简单卡宾反应]]"]
module: 有机化学
status: 已填充
---
# 题-400: 环戊烯酮还原——共轭vs直接加成顺序

## 题目

When we discussed reduction of cyclopentenone to cyclopentanol, we suggested that conjugate addition of borohydride must occur before direct addition of borohydride: in other words, the scheme below must be followed. What is the alternative scheme? Why is the scheme shown definitely correct?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/3faae2557ac9088b4acbe12b0b6d7166c12472d84be8f6682afbe6d0e1d78f0b.jpg]]

**原文题目**：Explain why conjugate addition of NaBH₄ to cyclopentenone must occur before direct addition. What is the alternative order and why is it wrong?

## 参考答案

**Answer (English)**: The alternative scheme would be to reduce the ketone first and the alkene second. This order must be wrong though, because simple alkenes are nucleophilic and are not reduced by NaBH₄. NaBH₄ is a nucleophilic reducing agent and attacks alkenes only if they are conjugated with an electron-withdrawing group. The conjugate addition must always occur first so as to keep the carbonyl group intact for the second step.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/d399b08f582392b7e74cfc6855e688ff6383e3b8b7ba33461b8514cd4fcadb9d.jpg]]

**中文解析**：

关键步骤：
1. **替代方案（错误）**：先还原C=O（直接加成）→再还原C=C（共轭加成）→这个顺序是错误的
2. **为什么错误**：简单烯烃（未共轭的C=C）是亲核性的，不会被NaBH₄还原。NaBH₄是亲核性还原剂，只有当C=C与吸电子基团（如C=O）共轭时才能进攻
3. **正确顺序的必要性**：必须先进行共轭加成（还原C=C），此时C=O必须保持完整以活化C=C。然后C=O再被直接加成还原

> **核心概念**：NaBH₄的还原是亲核性的——它进攻缺电子的碳。孤立的烯烃是富电子的，不会被亲核试剂进攻。只有当烯烃与C=O共轭时，β-碳才缺电子，才能被NaBH₄进攻。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[共轭加成]] | NaBH₄对共轭烯酮的共轭加成 | 直接 |
| [[Michael加成]] | 亲核性还原剂对α,β-不饱和羰基的选择性 | 直接 |
| [[化学选择性]] | 共轭加成和直接加成的顺序选择 | 间接 |

## 解题思路

1. **读题定位**：题目问为什么共轭加成必须先于直接加成——底物是环戊烯酮（α,β-不饱和酮），还原剂是NaBH₄
2. **🔑 关键转换**：NaBH₄是亲核性还原剂→只能进攻缺电子的碳→孤立C=C是富电子的→只有共轭C=C（β-碳缺电子）才能被进攻
3. **验证**：检查共轭加成是否保留了C=O（为第二步做准备），直接加成是否还原了C=O

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为NaBH₄可以还原孤立烯烃 | 对NaBH₄的亲核性理解不深 | NaBH₄是亲核性还原剂，不进攻富电子的孤立烯烃 | 为什么H₂/Pt可以还原孤立烯烃而NaBH₄不行？ |
| 忽略C=O对C=C的活化作用 | 对共轭体系的电子效应理解不深 | C=O的吸电子效应使β-碳缺电子，才能被亲核试剂进攻 | 没有C=O时，C=C能被亲核试剂进攻吗？ |
| 认为两种加成顺序都可行 | 对化学选择性理解不深 | 共轭加成必须先于直接加成，因为直接加成会消耗C=O | 如果先直接加成会发生什么？ |