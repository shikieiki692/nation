---
title: 题-531-Clayden-Ch41-P8-从手性池化合物识别目标结构特征
type: 题目
fidelity: 原书逐字
submodule: 不对称合成
exam_stage: 决赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[手性池合成]]", "[[不对称合成]]"]
tags: [化竞, Clayden, 有机化学, 不对称合成, 手性池]
updated: 2026-07-25
aliases: [Clayden-Ch41-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 41 Problem 8
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]", "[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-531: 从手性池化合物识别目标结构特征

## 题目

This compound is a precursor to a Novartis drug used for the control of inflammation. How might it be made from a chiral pool starting material?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/ab478f6b014e164694ced42dbe8ff7ece75f7e4614959db430ca478b91550dbe.jpg]]

**原文题目**：This compound is a precursor to a Novartis drug used for the control of inflammation. How might it be made from a chiral pool starting material?

## 参考答案

**Answer (English)**: The hydrocarbon skeleton of the target is that of the amino acid phenylalanine. The configuration is (S), the same as the natural amino acid, so we can use the standard amino acid to hydroxy acid conversion via diazotization, which goes with retention of configuration. The aromatic ring needs hydrogenating too.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/7d8bb5924a53451cf6bd45a74eb61eab59ba6eea5585fd2a6c5cea94f12091fa.jpg]]

**中文解析**：

**整体策略分析**：
本题考查的是"手性池"（chiral pool）策略的核心能力——从目标分子的碳骨架和手性特征出发，识别出可以利用的天然手性原料。手性池策略是不对称合成的三大策略之一（另两个是手性助剂法和不对称催化法），其优势在于天然手性化合物来源丰富、价格低廉、光学纯度高。

**目标分子分析**：
1. **碳骨架特征**：目标分子的碳骨架与氨基酸**苯丙氨酸（phenylalanine）**完全一致——苯基丙氨酸骨架
2. **手性特征**：目标分子的构型为**(S)**，与天然氨基酸的构型相同
3. **官能团差异**：目标分子是羟基酸（-CH(OH)CO2H），而苯丙氨酸是氨基酸（-CH(NH2)CO2H）

**合成策略——氨基酸到羟基酸的转化**：
1. **起始原料**：L-苯丙氨酸（天然手性池化合物，(S)-构型）
2. **关键反应——重氮化水解**：
   - 将L-苯丙氨酸与NaNO2/HCl反应
   - 氨基（-NH2）被重氮化为重氮盐（-N2+）
   - 重氮盐被水分子取代，生成羟基（-OH）
   - **关键点：该反应以保持构型的方式进行（retention of configuration）**
   - 因此(S)-氨基→(S)-羟基，手性信息完整保留
3. **芳环氢化**：
   - 使用催化氢化（Pd/C + H2）将苯环还原为环己烷环
   - 得到目标分子：(S)-2-羟基-4-环己基丁酸

**为什么选手性池策略**：
- L-苯丙氨酸是天然存在的氨基酸，光学纯度100%，价格低廉
- 重氮化水解反应保持构型，不需要额外的不对称控制步骤
- 整个路线简洁高效，只需两步转化

**重氮化水解保持构型的机理**：
- α-氨基酸的重氮化经历α-内酯（α-lactone）中间体
- 亲核试剂（H2O）从离去基团（N2）的同一面进攻→构型保持
- 这与SN2反应的构型翻转不同

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[手性池合成]] | 从天然手性化合物出发合成目标分子 | 直接 |
| [[不对称合成]] | 手性池策略作为不对称合成的三大策略之一 | 直接 |
| [[天然产物合成]] | 利用天然手性池化合物简化合成 | 间接 |
| [[重氮化反应]] | 氨基酸到羟基酸的转化（构型保持） | 间接 |
| [[催化氢化]] | 苯环到环己烷的还原 | 间接 |

## 解题思路

1. **读题定位**：题目要求从手性池原料设计合成路线。关键词：手性池、Novartis药物前体、消炎药
2. **🔑 关键转换**：识别目标碳骨架=苯丙氨酸骨架→L-苯丙氨酸是手性池原料→重氮化水解将-NH2转化为-OH（构型保持）→氢化还原苯环
3. **验证**：(a) L-苯丙氨酸的(S)构型→(S)-羟基酸（构型保持）；(b) 碳骨架完整保留；(c) 只需两步转化，效率高

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 无法识别碳骨架=苯丙氨酸 | 对手性池化合物的结构不熟 | 天然氨基酸是最重要的手性池来源之一，需要熟悉常见氨基酸的碳骨架 | 常见的手性池化合物有哪些？ |
| 用SN2机理理解重氮化水解 | 混淆反应机理 | 重氮化水解经历α-内酯中间体，亲核试剂从同一面进攻，构型保持（非SN2翻转） | 为什么重氮化水解是构型保持而非翻转？ |
| 忽略需要还原苯环 | 没有仔细对比目标和原料的结构差异 | L-苯丙氨酸有苯环，目标分子有环己烷环，需要催化氢化 | 苯环氢化的条件是什么？ |
| 误认为需要复杂的不对称合成方法 | 没有识别出手性池策略的优势 | 有天然手性池原料时，手性池策略通常是最简单的选择 | 什么情况下手性池策略不如不对称催化？ |