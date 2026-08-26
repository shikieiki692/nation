---
title: 题-576-Clayden-Ch31-P7-二维立体化学复习
type: 题目
fidelity: 原书逐字
submodule: 立体电子效应
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[立体化学]]"]
tags: [化竞, Clayden, 有机化学, 构象分析]
updated: 2026-07-25
aliases: [Clayden-Ch31-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 31 Problem 7
cross_references: ["[[题-551-Clayden-Ch29-P2-烷基吡啶LHMDS侧链延伸]]", "[[题-550-Clayden-Ch29-P1-杂环上亲电亲核取代产物预测]]"]
module: 有机化学
status: 已填充
---
# 题-576: 二维立体化学复习（太平洋海绵油）

## 题目

A revision problem in spectroscopy. A Pacific sponge contains 2.8% dry weight of a sweet-smelling oil with the following spectroscopic details. What is its structure and stereochemistry?

Mass spectrum gives formula: C₉H₁₆O. IR 1680 and 1635 cm⁻¹.

$\delta_{H}$ 0.90 (6H, d, J 7), 1.00 (3H, t, J 7), 1.77 (1H, m), 2.09 (2H, t, J 7), 2.49 (2H, q, J 7), 5.99 (1H, d, J 16), and 6.71 (1H, dt, J 16, 7).

$\delta_{C}$ 8.15 (q), 22.5 (two qs), 28.3 (d), 33.1 (t), 42.0 (t), 131.8 (d), 144.9 (d), and 191.6 (s).

**原文题目**：Determine the structure and stereochemistry of the sweet-smelling oil from a Pacific sponge.

## 参考答案

**Answer (English)**: The IR suggests a conjugated carbonyl compound, confirmed by the carbonyl and two alkene signals in the carbon NMR with the additional information that the carbonyl group is an aldehyde or ketone (δC about 200). The proton NMR shows it is a ketone (no CHO proton), that the alkene has two protons (5.99 and 6.71), and that they are trans (J = 16 Hz). We also see an ethyl group (2H q and 3H t) attached to something with no Hs (could it be the carbonyl group?). This suggests an ethyl ketone unit which leaves only C₄H₈. We know we have Me₂CH- from the 6H d and that leaves only CH₂. We have a structure.

The distinctive features of ¹³C NMR spectra of C=O compounds are described on p. 408 of the textbook.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/37c864d54ba08bc87967d32342ffd875ca4ea27527a5bf3f750e522d2107d04b.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/3f3fa11e2b116a7ae02542a60cff200dfe2697b9d6c29e5cf8d166f882b7cbde.jpg]]

**中文解析**：

关键步骤：
1. **分子式分析**：C₉H₁₆O，不饱和度=2（一个C=O + 一个C=C）
2. **IR分析**：1680 cm⁻¹（共轭C=O）和1635 cm⁻¹（共轭C=C）→ α,β-不饱和酮
3. **¹³C NMR分析**：191.6 (s)为酮羰基（醛应在~200且有d信号）；131.8和144.9为烯烃碳
4. **¹H NMR分析**：
   - 5.99(d, J=16)和6.71(dt, J=16, 7) → **反式烯烃**（J=16 Hz）
   - 0.90(6H, d) → Me₂CH- 异丙基
   - 1.00(3H, t) + 2.49(2H, q) → 乙基连接在无氢原子上（羰基碳）
5. **结构组装**：异丙基-CH₂-CH=CH-CO-Et

> **注意**：J=16 Hz是反式烯烃的标志性偶合常数（顺式通常J=6-12 Hz）。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[立体化学]] | 反式烯烃的J值判断（J=16 Hz） | 直接 |
| [[NMR谱学]] | ¹H和¹³C NMR的综合解析，官能团归属 | 直接 |
| [[构象分析]] | 分子整体构象对NMR信号的影响 | 间接 |

## 解题思路

1. **读题定位**：光谱综合解析——质谱给分子式，IR给官能团类型，NMR给详细结构
2. **🔑 关键转换**：C₉H₁₆O（不饱和度2）→IR确认共轭烯酮→NMR区分醛/酮→J=16 Hz确认反式→组装片段
3. **验证**：检查碳数（C₉）、氢数（H₁₆）、不饱和度（2）、所有NMR信号归属

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将共轭酮误判为醛 | 没有仔细看¹³C NMR | 醛碳应为~200 ppm (d)，酮碳为~190 ppm (s) | 醛和酮的¹³C NMR有何区别？ |
| 忽略J=16 Hz的立体化学意义 | 只关注化学位移 | J=16 Hz明确指示反式烯烃 | 反式和顺式烯烃的J值范围分别是？ |
| 乙基归属错误 | 没有考虑连接位置 | 2H(q)+3H(t)连接在无氢的羰基碳上 | 如何从偶合模式推断连接关系？ |