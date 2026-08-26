---
title: 题-417-Clayden-Ch13-P4-NMR谱归属和论证
type: 题目
fidelity: 原书逐字
submodule: NMR谱学
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch13-P4]
source: Clayden Organic Chemistry 2nd Ed. Chapter 13 Problem 4
cross_references: ["[[题-537-Clayden-Ch18-P2-Bullatenone结构A预测NMR并纠正]]", "[[题-536-Clayden-Ch18-P1-C6H5FO的13C NMR C-F偶合结构确定]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]", "[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]"]
module: 有机化学
status: 已填充
---
# 题-417: NMR谱归属和论证

## 题目

Assign the NMR spectra of this compound and justify your assignments. 'Assign' means 'say which signal belongs to which atom'.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/2936590643a26250a3254368d6adf08ff081da1092365bfa1ed415ae105ee77d.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/b5db8fa3671e11e80c84141184fce8d65c89442393ee4b7cc02b8a04449baeda.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/d05ab6d30be1553c73e121c918f709b6da75aeff77af9e7c7259859eb8ccced8.jpg]]

## 参考答案

**Answer (English)**: There is no coupling in this proton NMR spectrum which makes it much easier. Measure the chemical shifts and estimate the number of protons in each signal from the integration: δ_H (ppm) 1.4 (6H), 1.8 (3H), 2.9 (2H) and 5.6 (1H). The peak at 7.5 is CHCl₃ impurity in the CDCl₃ solvent. This is enough to assign the spectrum.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/08b56d55a79402139e182b8d9d93924521380958be3a2180c8a8a70ac046b81a.jpg]]

The carbon spectrum: three peaks in the 0–50 ppm region (methyl on alkene, CH₂ group, and the pair of methyls on same carbon). The 1:1:1 triplet at 77 ppm is the solvent CDCl₃. The signal in the 50–100 ppm region is the carbon next to oxygen in the Me₂C group. The two signals in the 100–150 ppm region are the two carbons of the alkene, and the very small peak at 150 ppm is the carbonyl group.

**中文解析**：

关键要点：
1. **¹H NMR归属**：无偶合使分析简化，关键是测量化学位移和从积分估算H数目：
   - δ 1.4 (6H)：两个等价甲基
   - δ 1.8 (3H)：烯上的甲基
   - δ 2.9 (2H)：CH₂基团
   - δ 5.6 (1H)：烯H
   - δ 7.5：CDCl₃中的CHCl₃杂质峰（忽略）
2. **¹³C NMR归属**：
   - 0–50 ppm：三个脂肪碳（烯甲基、CH₂、偕二甲基）
   - 77 ppm：CDCl₃溶剂三重峰
   - 50–100 ppm：与O相连的碳
   - 100–150 ppm：两个烯碳
   - 150 ppm：羰基碳（峰很小）

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | ¹H和¹³C NMR综合归属方法 | 直接 |
| [[化学位移]] | 不同区域对应不同碳/氢类型 | 直接 |
| [[1H NMR]] | 积分比确定各类H的相对数目 | 直接 |
| [[13C NMR]] | ¹³C化学位移区域划分和归属 | 直接 |

## 解题思路

1. **读题定位**：题目要求对真实NMR谱进行归属——需测量化学位移、读取积分、分析多重性
2. **🔑 关键转换**：¹H NMR中无偶合简化分析→积分确定H数目→¹³C NMR按化学位移区域逐一归属→交叉验证两种谱的一致性
3. **验证**：检查¹H和¹³C NMR的结构信息是否一致，确认杂质峰已排除

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将CHCl₃杂质峰当作样品信号 | 不熟悉CDCl₃溶剂中CHCl₃在δ 7.5 | 7.5 ppm的尖峰是溶剂杂质，应排除 | CDCl₃溶剂峰出现在什么位置？ |
| 忽略积分信息 | 只看化学位移不看积分 | 积分比反映各类H的相对数目，是归属的关键 | 如何从积分比确定分子式？ |
| 混淆¹H和¹³C化学位移范围 | 没有区分两种谱的尺度 | ¹H通常0–12 ppm，¹³C通常0–220 ppm | ¹³C NMR中77 ppm的三重峰是什么？ |