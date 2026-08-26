---
title: 题-284-Clayden-Ch9-P2-有机金属反应产物预测
type: 题目
fidelity: 原书逐字
submodule: 有机金属试剂
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[Grignard试剂]]", "[[有机锂试剂]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch9-P2]
source: Clayden Organic Chemistry 2nd Ed. Chapter 9 Problem 2
cross_references: ["[[题-283-Clayden-Ch9-P1-有机金属加成羰基的机理]]", "[[题-285-Clayden-Ch9-P3-Fenarimol替代合成路线]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-284: 有机金属反应产物预测

## 题目

What products would be formed in these reactions?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/6327debe88903212744c21130ec101826f6bcd27128bbacb299e74095c551a1c.jpg]]

**原文题目**：预测下列反应的产物。

## 参考答案

**Answer (English)**: (a) EtMgBr acts as a base to deprotonate the terminal alkyne, forming the alkynyl Grignard reagent and ethane. (b) The Grignard reagent from cyclobutyl bromide adds to cyclobutanone to give a tertiary alcohol; cyclobutanone is more electrophilic due to ring strain. (c) ClCH₂CO₂H + RMgBr — bromine is replaced first (Br > Cl > F reactivity order for halogen-metal exchange), giving the carboxylic acid after work-up.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/3f5c8973945d463865f2ec00c79a7330e711bda71dc1dc03201a63c45b0954aa.jpg]]
![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/7cbddf841e4315315fed5a85ae5010d0258c47a7d4f3c9cce6297e34311c8cad.jpg]]
![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/b9469492a43f94673b1107b260d690cce719a1f843b37693664e75be156fc706.jpg]]

**中文解析**：

(a) **EtMgBr + 末端炔烃**：末端炔烃的 C-H 键具有酸性（pKa ≈ 25），EtMgBr 作为强碱（共轭酸乙烷 pKa ≈ 50）优先夺取炔氢（酸碱反应），而非进攻羰基。产物为炔基 Grignard 试剂 + 乙烷。

(b) **环丁基溴 → Grignard + 环丁酮**：Grignard 试剂对环丁酮进行亲核加成。由于四元环的环张力，环丁酮的羰基碳比普通酮更具亲电性，反应活性更高。产物为叔醇。

(c) **ClCH₂CO₂H + RMgBr**：分子中同时含 Br 和 Cl，但 Br 的卤素-金属交换活性高于 Cl（活性顺序：I > Br > Cl >> F），因此 RMgBr 优先取代 Br。产物为氯乙酸。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[Grignard试剂]] | Grignard 试剂的双重反应性（碱性 vs 亲核性） | 直接 |
| [[有机锂试剂]] | 有机锂与 Grignard 的反应性对比 | 直接 |
| [[C-C键形成]] | Grignard 加成构建 C-C 键 | 间接 |

## 解题思路

1. **读题定位**：三个子反应分别考察 Grignard 试剂的碱性（a）、亲核加成（b）、卤素选择性（c）——需要判断每种情况下优先发生的反应类型
2. **🔑 关键转换**：(a) pKa 判断：炔氢酸性 > 醇 → 酸碱反应优先；(b) 环张力增强羰基亲电性 → 正常加成；(c) 卤素活性 I > Br > Cl >> F → Br 优先反应
3. **验证**：(a) 产物应为炔基负离子而非加成产物；(b) 产物为含两个环丁基的叔醇；(c) 产物保留 Cl，仅 Br 被取代

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| (a) 误认为 EtMgBr 进攻炔烃三键 | 未考虑末端炔的酸性 | 末端炔 pKa ≈ 25，EtMgBr 优先作为碱夺取炔氢 | 如果底物是内部炔烃会怎样？ |
| (b) 忽略环丁酮的高反应活性 | 未理解环张力对羰基的影响 | 四元环使 C=O 键角偏离理想值，碳更缺电子，亲电性增强 | 环戊酮和环丁酮哪个更活泼？ |
| (c) 误认为 Cl 和 Br 同时被取代 | 不了解卤素-金属交换的选择性 | 卤素与碳的键能：C-Br < C-Cl < C-F，活性依次递减 | 为什么碘最容易被交换？ |