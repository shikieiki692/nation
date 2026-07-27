---
title: 题-607-Clayden-Ch33-P12-HIV蛋白酶抑制剂合成试剂选择
type: 题目
submodule: 非对映选择性
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 竞赛拔高
syllabus_codes: ["21"]
knowledge_points: ["[[非对映选择性]]"]
tags: [化竞, Clayden, 有机化学, 非对映选择性]
updated: 2026-07-25
aliases: [Clayden-Ch33-P12]
source: Clayden Organic Chemistry 2nd Ed. Chapter 33 Problem 12
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择]]", "[[题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]"]
module: 有机化学
status: 已填充
---
# 题-607: HIV蛋白酶抑制剂合成试剂选择

## 题目

The following sequences show parts of the syntheses of two different HIV protease inhibitors. What reagents are required for steps 1–4? (For steps 1 and 3, consider carefully how the stereochemistry of the product might be controlled.)

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/ab521808b57eae618fa04f585b99ef1a6833de659a8c2c6d082d5d525b72bece.jpg]]

## 参考答案

**Answer (English)**: In step 1, we need to achieve diastereoselectivity during the addition of a nucleophile, CN⁻, to a carbonyl group adjacent to a stereogenic centre. The question is: do we need chelation control, or just Felkin-Anh control? Drawn out below is the conformation in which the aldehyde would react with cyanide if simple Felkin-Anh control were operating: check for yourself that the product is the correct one. No chelation is needed.

In fact, this step was carried out with KCN in the presence of a Lewis acid (Me₃Al) because the bulky benzyl groups prevent the nitrogen participating in chelation.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/38195a5d5c585f5771229b68a78fc56109f585eb04a4d61360ed2f9aff666092.jpg]]

In the second sequence, the nucleophile in step 3 must be a vinyl anion equivalent, maybe vinylmagnesium bromide. Comparison of the relative configuration of this product with the one above it immediately suggests that Felkin-Anh control is not operative here, since the opposite diastereoisomer is formed. Drawn below is the expected reactive conformation for a reaction involving chelation control: note that the acidic NH proton must be removed by any basic nucleophile. The outcome is correct: we need to achieve chelation control, so a magnesium counterion is a good choice (Mg²⁺ readily takes part in chelated transition states). The final C=C bond cleavage in step 4 can be achieved by ozonolysis.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/0e660f56a1f84d7fd6de7b0f93c9b91dec6c667e0200af6eda6adf6c0ae8de0e.jpg]]

**中文解析**：

关键步骤：
1. **序列1步骤1（Felkin-Anh控制）**：CN⁻进攻手性醛的羰基。需要判断是螯合控制还是Felkin-Anh控制。画出Felkin-Anh过渡态验证产物正确——不需要螯合。实际使用KCN+Lewis酸（Me₃Al），因为大体积苄基阻止了氮的螯合
2. **序列1步骤2**：腈水解为酸，苄基氢解。顺序很重要——先水解再氢解，因为氢解可能还原腈
3. **序列2步骤3（螯合控制）**：需要乙烯基负离子等价物（如乙烯基溴化镁）。产物与序列1的相对构型相反，说明不是Felkin-Anh控制而是螯合控制。Mg²⁺适合螯合过渡态
4. **序列2步骤4**：C=C双键的氧化断裂（臭氧化）

> **核心概念**：在药物合成中，选择合适的试剂来控制立体化学至关重要。Felkin-Anh控制（使用KCN/Me₃Al）和螯合控制（使用RMgX/Mg²⁺）可以给出不同的非对映异构体。判断需要哪种控制取决于目标产物的立体化学。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[非对映选择性]] | Felkin-Anh vs 螯合控制的选择 | 直接 |
| [[化学选择性]] | 试剂选择（KCN/Me₃Al vs RMgX） | 直接 |
| [[药物合成]] | HIV蛋白酶抑制剂的立体化学控制 | 直接 |

## 解题思路

1. **读题定位**：为两个HIV蛋白酶抑制剂合成序列选择试剂——识别关键步骤为亲核加成的立体化学控制
2. **关键转换**：序列1→Felkin-Anh控制→KCN/Me₃Al→腈→水解→氢解；序列2→螯合控制→RMgX/Mg²⁺→构型相反→臭氧化
3. **验证**：检查序列1产物是否符合Felkin-Anh预测，序列2产物是否与序列1相反（螯合控制）

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 两个序列用相同试剂 | 未注意产物构型相反 | 序列1用Felkin-Anh控制，序列2用螯合控制 | 如何判断需要哪种控制？ |
| 氢解和水解顺序颠倒 | 未考虑化学选择性 | 必须先水解腈再氢解苄基，否则腈会被还原 | 为什么氢解可能还原腈？ |
| 忘记NH质子的影响 | 未考虑碱性亲核试剂会去质子化 | 酸性NH质子会被任何碱性亲核试剂夺去 | 去质子化对螯合控制有什么影响？ |