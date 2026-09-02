---
title: 题-438-Clayden-Ch24-P7-邻位锂化区域选择性
type: 题目
fidelity: 原书逐字
submodule: 区域选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 竞赛
syllabus_codes: ["21"]
knowledge_points: ["[[区域选择性]]"]
tags: [化竞, Clayden, 有机化学, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch24-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 24 Problem 7
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-608-Clayden-Ch36-P1-原子编号追踪重排]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-609-Clayden-Ch36-P2-Beckmann重排立体化学和机理]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-438: 邻位锂化区域选择性

## 题目

**【中文】**下面的反应序列展示了合成一种强效抗癌化合物所需中间体的过程。解释反应的区域选择性。为什么第二步需要两当量的BuLi？

**【原文】**
The sequence of reactions below shows the preparation of a compound needed for the synthesis of a powerful anti-cancer compound. Explain the regioselectivity of the reactions. Why do you think two equivalents of BuLi are needed in the second step?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/68d294ad7fdb7d20677989acb3afcb4db6321b9b360adc7ef375205535b426e2.jpg]]

## 参考答案

**Answer (English)**:

Both reactions involve ortholithiation—deprotonation of the aromatic ring to form an intermediate aryllithium. The deprotonation occurs where the BuLi can be 'guided in' by coordinating oxygen atoms. The methoxymethyl acetal, with its two oxygen atoms, is very good at doing this, so we expect deprotonation at one of the two positions ortho to this group. The other acetal is also a complexing group, so the deprotonation happens in between the two oxygen atoms.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/18bbed80f46d9a7e384b8a1bc35bfbcd9617221122cfb9fe5605acba306dca98.jpg]]

In the second step, deprotonation can again take place next to the methoxymethyl group. Two equivalents of BuLi are needed because the most acidic proton is in fact one of the protons of the methyl group: a benzyl lithium forms first, and then a more reactive aryllithium. When the electrophile (DMF) is added, it reacts only with the last formed, more basic anion.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/ce3aadf323af042e95a3d48f2b7e4ee215329c4ee2691257dc3e23470b6002a5.jpg]]

Phenyllithiums are more basic than benzyllithiums, because in benzyllithiums the 'anion' is conjugated with the ring; in phenyllithiums the 'anion' is perpendicular to the π system (like the lone pair in pyridine).

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/09a5e1c90858684c9dec4c5b304daf49d2efab218d2345d89f59704159ed533d.jpg]]

**中文解析**：

**第一步：邻位锂化（ortholithiation）**
- BuLi通过与氧原子的配位作用被"引导"到邻位去质子化
- 甲氧基甲基缩醛（CH₂(OCH₃)₂）有两个氧原子，配位能力很强
- 另一个缩醛也是配位基团
- 结果：去质子化发生在两个配位基团之间的位置

**第二步：需要2当量BuLi的原因**
1. **第一个BuLi**：拔除甲基上最酸性的H（苄基H，pKa≈41）→形成苄基锂（benzyllithium）
2. **第二个BuLi**：拔除芳环上相邻的H →形成芳基锂（aryllithium）
3. 两个负离子的碱性不同：芳基锂 > 苄基锂（芳基锂的负电子垂直于π体系，无法共轭稳定化）
4. **化学选择性**：加入亲电体DMF时，只与最后形成的、更碱性的芳基锂反应

**关键概念**：
- 苄基负电子：与苯环共轭→稳定化→碱性较弱
- 芳基负电子：垂直于π体系（类似吡啶中N的孤对电子）→无法共轭稳定化→碱性更强

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[区域选择性]] | 氧原子配位引导的邻位锂化 | 直接 |
| [[邻位锂化]] | BuLi与配位基团协同的邻位去质子化 | 直接 |
| [[有机锂试剂]] | BuLi的碱性和配位导向作用 | 直接 |
| 双负离子 | 双负离子中两个负离子的碱性差异和化学选择性 | 间接 |

## 解题思路

1. **读题定位**：两步邻位锂化反应，第二步需要2当量BuLi，加入DMF后得到醛
2. **🔑 关键转换**：
   - 步骤1：识别配位导向的邻位锂化（两个O→去质子化在它们之间）
   - 步骤2：2当量BuLi→先拔苄基H（更酸）再拔芳环H（更碱）→DMF选择性进攻芳基锂
3. **验证**：产物是醛，说明DMF（HCONMe₂）作为亲电体在芳基锂位点引入了CHO基团

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为2当量BuLi是为了确保完全反应 | 没有理解双负离子的化学选择性 | 2当量是因为依次形成两种不同的负离子；DMF只与更碱性的芳基锂反应 | 如果只用1当量BuLi会得到什么？ |
| 混淆苄基锂和芳基锂的碱性 | 没有理解共轭效应对负离子稳定性的影响 | 苄基锂：负电子共轭离域→稳定→弱碱；芳基锂：负电子垂直于π→不稳定→强碱 | 吡啶中N的孤对电子为什么碱性比吡咯强？ |
| 不理解配位导向的机理 | 认为去质子化位置由电子效应决定 | BuLi通过与O原子的Li-O配位被"拉"到邻位空间位置 | 除了O，还有哪些原子可以配位导向？ |