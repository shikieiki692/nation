---
title: 题-488-Clayden-Ch27-P12-Wittig产物立体化学NMR确认
type: 题目
fidelity: 原书逐字
submodule: 硅硅磷化学
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[Wittig反应]]"]
tags: [化竞, Clayden, 有机化学, NMR]
updated: 2026-07-25
aliases: [Clayden-Ch27-P12]
source: Clayden Organic Chemistry 2nd Ed. Chapter 27 Problem 12
cross_references: ["[[题-424-Clayden-Ch23-P1-溴代醛选择性转化为两个产物]]", "[[题-425-Clayden-Ch23-P2-内酯选择性开环]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-488: Wittig产物立体化学NMR确认

## 题目

The following reaction between a phosphonium salt, base, and an aldehyde gives a hydrocarbon C₆H₁₂ with the 200 MHz ¹H NMR spectrum shown. Give a structure for the product and comment on its stereochemistry.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/4df28f9760ea3a60dfca2f7b4e57e5247c2e58804591c7969c8a12886236a86b.jpg]]

**原文题目**：The following reaction between a phosphonium salt, base, and an aldehyde gives a hydrocarbon C₆H₁₂ with the 200 MHz ¹H NMR spectrum shown. Give a structure for the product and comment on its stereochemistry.

## 参考答案

**Answer (English)**: We'll approach this as a spectroscopic problem, rather than predicting the outcome and then making the data fit. First analyse the data, measuring chemical shifts, integrals and J values.

| δH (ppm) | 积分 | 裂分 | J (Hz) | 归属 |
|---|---|---|---|---|
| 0.97 | 6H | d | 7 | CHMe₂ |
| 1.60 | 3H | d | 5 | MeCH= |
| 2.70 | 1H | double septuplet | 7, 4 | Me₂CH-CH= |
| 5.15 | 1H | dd | 10, 4 | =CH- |
| 5.35 | 1H | dq | ~5 | =CHMe |

From this alone we can see an alkene with two vicinal Hs, a methyl group, and an isopropyl group. That adds up to C₆H₁₂ so we have found everything. The isopropyl group contains a 7 Hz coupling between the two methyl groups and the H at 2.70 ppm which is coupled to one of the alkene protons with J = 4 Hz. The remaining coupling of the alkene proton at 5.15 ppm (10 Hz) must be to the other alkene proton and that fits with a cis double bond.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/cfd0b33bb19a90da69e1668091d4570e0569f0b83bdde0b43851708f3e0d5dc2.jpg]]

The compound is cis (Z) 4-methylpent-2-ene. This is a Wittig reaction with an unstabilized ylid, so you should expect to find a cis double bond.

**中文解析**：

关键步骤：
1. **NMR数据分析**：
   - δ 0.97 (6H, d, J=7 Hz)：异丙基两个甲基，被CH耦合
   - δ 1.60 (3H, d, J=5 Hz)：与烯烃相连的甲基
   - δ 2.70 (1H, double septuplet, J=7, 4 Hz)：异丙基CH，被两个甲基(7Hz)和烯烃H(4Hz)耦合
   - δ 5.15 (1H, dd, J=10, 4 Hz)：烯烃H，被另一个烯烃H(10Hz)和CH(4Hz)耦合
   - δ 5.35 (1H, dq, J~5 Hz)：烯烃H，被甲基(5Hz)耦合；dq中d和q的J恰好相等→重叠为6线(1:3:4:4:3:1)
2. **结构确定**：C₆H₁₂ = 异丙基 + 甲基 + 双键 = (Z)-4-甲基戊-2-烯
3. **立体化学确认**：J=10 Hz（烯烃vicinal coupling）→ cis（Z）构型
4. **Wittig验证**：非稳定化叶立德→Z-烯烃，与NMR数据一致

> **核心要点**：J=10 Hz的耦合常数是判断cis烯烃的关键证据；dq裂分中d和q的J值巧合导致特殊的1:3:4:4:3:1峰形。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| Wittig反应 | 非稳定化叶立德→Z-烯烃的验证 | 直接 |
| [[NMR谱学]] | 耦合常数判断烯烃构型，复杂裂分模式解析 | 直接 |
| [[烯烃立体选择性]] | Z/E选择性的光谱确认 | 直接 |

## 解题思路

1. **读题定位**：光谱解析题→从NMR数据推断结构和立体化学
2. **关键转换**：分析所有δ、积分、J值→组装片段（异丙基+甲基+双键）→J=10 Hz→Z构型
3. **验证**：所有NMR数据是否与(Z)-4-甲基戊-2-烯吻合

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将dq误判为其他裂分 | 不熟悉巧合J值 | d和q的J恰好相等→内线重叠→6线(1:3:4:4:3:1) | 为什么dq会出现这种特殊峰形？ |
| J=10 Hz判断为trans | J值范围记错 | Jcis≈6-12 Hz，Jtrans≈15-18 Hz；10 Hz是cis | 如何区分J=10和J=15？ |
| 忘记验证分子式 | 直接猜结构 | C₆H₁₂的不饱和度=1，所有片段加起来必须等于C₆H₁₂ | 不饱和度如何计算？ |