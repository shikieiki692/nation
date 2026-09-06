---
title: 题-434-Clayden-Ch24-P3-芳香亲电取代和自由基取代区域选择性
type: 题目
fidelity: 原书逐字
submodule: 区域选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
question_type: [简答]
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[区域选择性]]"]
tags: [化竞, Clayden, 有机化学, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch24-P3]
source: Clayden Organic Chemistry 2nd Ed. Chapter 24 Problem 3
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-608-Clayden-Ch36-P1-原子编号追踪重排]]", "[[题-609-Clayden-Ch36-P2-Beckmann重排立体化学和机理]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
source_grade: B
---
# 题-434: 芳香亲电取代和自由基取代区域选择性

## 题目

Explain the different regioselectivity in these two brominations of 1,2-dimethylbenzene.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/2ba25f6e0b4f05ddb1cd6535ebd892a5a470151a5f7d1cb7b9a313f65f01dad4.jpg]]

**原文题目**：解释1,2-二甲基苯（邻二甲苯）的两种溴化反应为何具有不同的区域选择性。

## 参考答案

**Answer (English)**:

**Electrophilic aromatic substitution (AlCl₃/Br₂)**: AlCl₃ activates Br₂ to form the electrophile 'Br⁺', which attacks the aromatic ring. Methyl groups are ortho,para directors, so any of the four unsubstituted positions could be attacked, but steric hindrance directs the first bromine to go to one of the positions that does not lead to a 1,2,3-trisubstituted ring.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/94a0c7941fdc1eeb2d64d989d422dcb16c561cb44e34057dbe13dac95b243f2e.jpg]]

Now we have three ortho, para directors, and bromine (with its lone pairs) is the strongest, so the next bromine will go ortho to the bromine in the less sterically hindered of the two possibilities.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/ecd84bb61deb47ac3a850e4cc0cc7d0139f89f27a4ecc31d284bab6cc9685dd8.jpg]]

**Radical substitution (Br₂/hv)**: In the presence of light, Br-Br bond undergoes homolysis, and Br· radicals are formed. One of these can abstract a hydrogen atom, breaking the weakest C-H bond. The methyl groups' C-H bonds are weaker than those of the phenyl ring because the benzyl radical that forms is delocalized into the aromatic ring. The benzyl radical attacks another molecule of bromine, and the cycle continues.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/725b36c3db2e8de6f90653d6308279ed86d9f838e0afa03f7efaebe318f1ca96.jpg]]

**中文解析**：

同一起始物（邻二甲苯）在不同条件下溴化，区域选择性完全不同：

**反应条件一：AlCl₃/Br₂（亲电芳香取代）**
1. AlCl₃活化Br₂产生亲电体Br⁺
2. 甲基是邻/对位定位基，四个未取代位置理论上都可被进攻
3. **位阻效应**决定选择性：Br⁺优先进攻不产生1,2,3-三取代环的位置
4. 第二个Br进入时，Br（有孤对电子）是最强的邻/对位定位基，进攻位阻较小的邻位

**反应条件二：Br₂/hv（自由基取代）**
1. 光照下Br-Br键均裂产生Br·自由基
2. Br·抽取H原子时，优先断裂最弱的C-H键
3. **苄基C-H键**（BDE约85 kcal/mol）远弱于苯环C-H键（BDE约110 kcal/mol）
4. 因为苄基自由基通过共轭离域到苯环而稳定化
5. 产物：苄基溴化物（侧链取代），而非环上溴化物

**核心区别**：亲电取代发生在环上（电子密度最高的位置）；自由基取代发生在侧链（形成最稳定自由基的位置）

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[区域选择性]] | 两种取代反应的不同区域选择性来源 | 直接 |
| [[芳香亲电取代]] | 甲基的邻/对位定位效应与位阻 | 直接 |
| [[自由基取代]] | 苄基自由基稳定性与侧链取代选择性 | 直接 |
| [[键解离能]] | 苄基C-H键较弱导致自由基选择性 | 间接 |

## 解题思路

1. **读题定位**：两个反应底物相同（邻二甲苯），条件不同——AlCl₃/Br₂（亲电）vs Br₂/hv（自由基）
2. **🔑 关键转换**：亲电取代→看电子效应（甲基活化邻/对位）+位阻效应；自由基取代→看C-H键强度（苄基最弱）
3. **验证**：亲电取代产物为环上溴化物（1,4-二溴-1,2-二甲基苯）；自由基取代产物为苄基溴化物

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为两种条件给出相同产物 | 没有区分亲电取代和自由基取代的机理差异 | 机理不同→选择性不同：亲电看电子密度，自由基看键强度 | 如何从反应条件判断是亲电还是自由基机理？ |
| 忽略位阻效应 | 只考虑了电子效应 | 邻二甲苯中位阻使得某些位置被"保护"，Br⁺难以接近 | 为什么第一个Br不进入两个甲基之间的位置？ |
| 混淆苄基自由基和苯基自由基 | 没理解离域对自由基稳定性的影响 | 苄基自由基的单电子可以离域到苯环→非常稳定；苯基自由基的单电子垂直于π体系→不稳定 | 苄基自由基和烯丙基自由基哪个更稳定？ |
| 认为Br₂/hv只发生在环上 | 自由基取代的区域选择性取决于C-H键强度 | 侧链苄基C-H键远弱于芳环C-H键 | 什么条件下Br₂/hv会在环上发生取代？ |