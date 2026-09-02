---
title: 题-383-Clayden-Ch21-P3-甲苯不同位点反应活性定量评估
type: 题目
fidelity: 原书逐字
submodule: 芳香亲电取代
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
question_type: [计算]
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[芳香亲电取代]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch21-P3]
source: Clayden Organic Chemistry 2nd Ed. Chapter 21 Problem 3
cross_references: ["[[题-525-Clayden-Ch41-P2-拆分法规划不对称合成入门]]", "[[题-336-Clayden-Ch7-P1-共轭判断和弯曲箭头表示]]", "[[题-524-Clayden-Ch41-P1-循环中间体创建新手性中心]]", "[[题-337-Clayden-Ch7-P2-复杂化合物中共轭体系范围]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-383: 甲苯不同位点反应活性定量评估

## 题目

How reactive are the different sites in toluene? Nitration of toluene produces the three possible products in the ratios shown. What would be the ratios if all the sites were equally reactive? What is the actual relative reactivity of the three sites? You could express this as x:y:1 or as a:b:c where a+b+c = 100. Comment on the ratio you deduce.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/503fbc386efff6503bd83ea994ef81fffa59e64e95ea06f785344b534054bfc7.jpg]]

**原文题目**：甲苯中不同位点的反应活性如何？甲苯硝化产生三个可能产物的比例如图所示。如果所有位点活性相同，比例会是多少？三个位点的实际相对反应活性是多少？请评论你推导出的比例。

## 参考答案

**Answer (English)**: As there are two ortho and two meta sites, the ratio if all were equally reactive would be 2:2:1 o:m:p. The observed reactivity is 30:2:37 or 15:1:18 or 43:3:54 depending on how you expressed it. The ortho and para positions are roughly equally reactive because the methyl group is electron-donating. The para is slightly more reactive than the ortho because of steric hindrance. The meta position is an order of magnitude less reactive because the intermediate is not stabilized by electron-donation (σ-conjugation) from the methyl group.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/efa90d7682c0c91506dc131b9f1395b17b81ade21de120016415b53c37347516.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/3d89c1386f54f887191172e3241f01b3318152e65132bec937e35dd5b53fe1e8.jpg]]

**中文解析**：

本题通过定量数据考察甲苯硝化中不同位点的反应活性差异。

关键要点：
1. **等活性比例**：甲苯有2个ortho位、2个meta位和1个para位，若活性相同，比例应为2:2:1（o:m:p）
2. **实际比例**：观测到的产物比例约为58% ortho、4% meta、38% para
3. **相对活性计算**：ortho和para位的相对活性相近（甲基是给电子基，通过σ共轭稳定邻对位的碳正离子中间体）
4. **para位略优于ortho位**：因为空间位阻使ortho位的反应稍慢
5. **meta位活性低一个数量级**：甲基无法通过σ共轭稳定meta位反应的碳正离子中间体

> **核心概念**：甲基通过σ共轭（hyperconjugation）给电子，稳定邻对位的Wheland中间体（σ-complex），但不能稳定meta位的中间体。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[芳香亲电取代]] | 甲苯硝化的定量产物分布 | 直接 |
| [[定位效应]] | 邻对位定位基对不同位点的活化作用 | 直接 |
| [[活化基]] | 甲基作为活化基对反应速率的影响 | 间接 |
| [[碳正离子]] | Wheland中间体的稳定性决定区域选择性 | 间接 |

## 解题思路

1. **读题定位**：题目给出甲苯硝化的实验比例，要求计算相对反应活性
2. **🔑 关键转换**：先计算等活性比例（2:2:1）→用实际比例除以等活性比例→得到各位置的相对活性→甲基通过σ共轭稳定邻对位中间体，不稳定meta位中间体
3. **验证**：检查计算结果是否与定位规则一致（邻对位活性高、间位活性低）

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 忘记ortho有2个位点 | 计数错误 | ortho位有2个等价位置，meta位也有2个 | 如果甲基被乙基取代，比例会如何变化？ |
| 将比例直接当作活性 | 未考虑位点数目的影响 | 相对活性 = (观测比例/实际位点数) / (观测比例/实际位点数) | 如何用Hammett方程定量描述取代基效应？ |
| 认为para比ortho活性高得多 | 混淆了空间位阻和电子效应 | 两者电子效应相近，para略高是因为空间位阻使ortho稍慢 | 什么取代基会使para选择性更高？ |