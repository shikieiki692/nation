---
title: 题-469-Clayden-Ch37-P5-烷基溴自由基关环到烯烃
type: 题目
fidelity: 原书逐字
submodule: 自由基反应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[自由基]]"]
tags: [化竞, Clayden, 有机化学, 自由基反应]
updated: 2026-07-25
aliases: [Clayden-Ch37-P5]
source: Clayden Organic Chemistry 2nd Ed. Chapter 37 Problem 5
cross_references: ["[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-465-Clayden-Ch37-P1-重要自由基反应复习]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-466-Clayden-Ch37-P2-重氮盐亲核取代vs自由基对比]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
---
# 题-469: 烷基溴的Bu₃SnH自由基关环

## 题目

Propose a mechanism for this reaction accounting for the selectivity. Include a conformational drawing of the product.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/1ec07377ad3aca92d028c74e80305644541528956510f763489c799049fe1c64.jpg]]

**原文题目**：Propose a mechanism for this reaction accounting for the selectivity. Include a conformational drawing of the product.

## 参考答案

**Answer (English)**: This time AIBN abstracts the hydrogen from Bu₃SnH and the tin radicals carry the chain along. First they remove the bromine atom from the starting material to make a vinyl radical that cyclizes onto the unsaturated ketone to give a radical stabilized by conjugation with the carbonyl group. The chain is completed by abstraction of hydrogen from another molecule of Bu₃SnH, the tin radical formed then allowing the cycle to restart.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/9e22d3622921681adabcfef225e1108b2bd8c157c29846061cf6e380378000ff.jpg]]

The stereochemistry of the product comes from the requirement of a 1,3-bridge to be diaxial as this is the only way the bridge can reach across the ring. At the moment of cyclization, the vinyl radical side chain must be in an axial position.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/75963cc8da3deb5a7f5d4644b62e70d6310aea2357c27ace1edb99144ff0f375.jpg]]

**中文解析**：

关键步骤：
1. **引发**：AIBN热分解产生异丁腈自由基，从Bu₃SnH夺取氢原子，生成Bu₃Sn·自由基
2. **夺溴**：Bu₃Sn·从底物的乙烯基溴上夺取溴原子，产生乙烯基自由基（vinyl radical）
3. **关环**：乙烯基自由基对分子内的α,β-不饱和酮进行5-exo-trig关环，加成到烯烃上产生一个被羰基共轭稳定的碳自由基
4. **链传递**：该自由基从另一分子Bu₃SnH夺取氢原子，得到产物并再生Bu₃Sn·
5. **立体化学**：产物中1,3-桥必须是双直立键（diaxial），因为只有这种构象才能让桥跨越环的两侧。关环时乙烯基侧链必须处于直立位置

> **注意**：Bu₃SnH是自由基反应中常用的氢原子供体和卤素清除剂，通过Sn-H键的低键解离能实现链传递。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[自由基]] | Bu₃Sn·自由基的产生和链传递 | 直接 |
| [[自由基机理]] | 完整的自由基关环链反应机理 | 直接 |
| [[关环反应]] | 5-exo-trig关环的选择性和立体化学 | 直接 |
| [[构象分析]] | 1,3-桥必须双直立的构象要求 | 间接 |

## 解题思路

1. **读题定位**：题目要求画机理、解释选择性、画构象图——涉及Bu₃SnH介导的自由基关环和产物构象
2. **🔑 关键转换**：AIBN引发 → Bu₃Sn·夺溴 → 乙烯基自由基 → 5-exo关环到不饱和酮 → 夺氢完成链 → 产物构象为双直立桥
3. **验证**：检查关环是否为5-exo-trig（而非6-endo），产物构象是否为diaxial桥，自由基是否被羰基共轭稳定

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 画H·直接从Bu₃SnH转移 | 混淆自由基和离子机理 | 必须通过Bu₃Sn·自由基中间体，不能画H·直接转移 | 为什么不能有游离的H·？ |
| 忘记画构象图 | 只画了平面机理 | 题目要求构象图，1,3-桥必须是双直立键 | 为什么双直立是唯一可能？ |
| 关环位置画错 | 没有考虑自由基稳定性 | 自由基应加成到烯烃的β位，使产生的自由基与羰基共轭 | 为什么与羰基共轭的自由基更稳定？ |
| 混淆5-exo和6-endo | 没有数关环的原子数 | 从自由基碳到烯烃碳：5-exo是形成五元环（更常见） | Baldwin规则如何预测关环？ |