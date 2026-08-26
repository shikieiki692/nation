---
title: 题-280-Clayden-Ch8-P9-半胱氨酸和精氨酸pKa及不同pH结构
type: 题目
fidelity: 原书逐字
submodule: 酸碱质子理论
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: []
knowledge_points: ["[[pKa]]", "[[有机酸碱性]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch8-P9]
source: Clayden Organic Chemistry 2nd Ed. Chapter 8 Problem 9
cross_references: ["[[题-274-Clayden-Ch8-P3-羟基酸在不同pH下的存在形式]]", "[[题-281-Clayden-Ch8-P10-两个戊二醇合成失败原因]]"]
module: 有机化学
status: 已填充
---
# 题-280: 半胱氨酸和精氨酸pKa及不同pH结构

## 题目

Draw the structures of cysteine and arginine at pH 1, 7, 10, and 14. Given pKa values: Cys (1.8, 8.3, 10.8), Arg (2.2, 9.0, 13.2).

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/416312e8ef601d47f6d2c035003c8011c66c5f8574ddef7d203126e70d91921b.jpg]]

**原文题目**：画出半胱氨酸和精氨酸在pH 1、7、10和14时的结构。已知pKa值：半胱氨酸（1.8、8.3、10.8），精氨酸（2.2、9.0、13.2）。

## 参考答案

**Answer (English)**: 
- Cysteine pKa: 1.8 (CO2H), 8.3 (NH3⁺), 10.8 (SH)
  - pH 1: CO2H protonated, NH3⁺ protonated, SH protonated (net charge +1)
  - pH 7: CO2⁻ deprotonated, NH3⁺ protonated, SH protonated (net charge 0, zwitterion)
  - pH 10: CO2⁻, NH3⁺ → NH2 deprotonated, SH protonated (net charge -1)
  - pH 14: CO2⁻, NH2, S⁻ all deprotonated (net charge -2)
- Arginine pKa: 2.2 (CO2H), 9.0 (NH3⁺), 13.2 (guanidinium)
  - pH 1: All protonated (net charge +2)
  - pH 7: CO2⁻, NH3⁺ protonated, guanidinium protonated (net charge +1)
  - pH 10: CO2⁻, NH2 deprotonated, guanidinium protonated (net charge 0, zwitterion)
  - pH 14: CO2⁻, NH2, guanidine all deprotonated (net charge -1)

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/8431b9b3bb9911d21b822ffea72fe51fd8c04dfe5442cc162b4e97695f401a46.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/454f8d4cb9b717bb1817d5c70a0720c7252ad3210bdb14959d0ad24b3d43f54b.jpg]]

**中文解析**：
1. **半胱氨酸**（pKa = 1.8, 8.3, 10.8）：pH 1时全部质子化（净电荷+1）；pH 7时羧基去质子化（两性离子，净电荷0）；pH 10时氨基去质子化（净电荷-1）；pH 14时巯基也去质子化（净电荷-2）。
2. **精氨酸**（pKa = 2.2, 9.0, 13.2）：pH 1时全部质子化（净电荷+2）；pH 7时仅羧基去质子化（净电荷+1）；pH 10时氨基去质子化（两性离子，净电荷0）；pH 14时胍基也去质子化（净电荷-1）。
3. **关键**：比较pH与各pKa，pH > pKa的基团去质子化。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[pKa]] | 根据pKa判断不同pH下的质子化状态 | 直接 |
| [[有机酸碱性]] | 氨基酸中各基团酸碱性的比较 | 直接 |
| [[氨基酸化学]] | 氨基酸的等电点和两性离子 | 间接 |

## 解题思路

1. **读题定位**：列出各基团的pKa，比较pH与pKa判断质子化状态。
2. **🔑 关键转换**：pH < pKa → 质子化；pH > pKa → 去质子化。逐个基团判断。
3. **验证**：检查净电荷是否正确，两性离子在等电点附近（pH ≈ pI）。

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 混淆pKa与等电点 | pKa是基团的酸性常数，pI是净电荷为零的pH | pI = (pKa1 + pKa2)/2（简单氨基酸） | 半胱氨酸的pI是多少？ |
| pH 7时SH去质子化 | SH的pKa = 10.8，pH 7时仍质子化 | SH在pH 7时仍为SH | 巯基的pKa是多少？ |
| 精氨酸胍基在pH 7去质子化 | 胍基pKa = 13.2，pH 7时仍质子化 | 胍基在pH 7时仍带正电 | 胍基为什么pKa这么高？ |