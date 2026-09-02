---
title: 题-437-Clayden-Ch24-P6-Friedel-Crafts和Wolff-Kishner序列中A和B
type: 题目
fidelity: 原书逐字
submodule: 区域选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[区域选择性]]"]
tags: [化竞, Clayden, 有机化学, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch24-P6]
source: Clayden Organic Chemistry 2nd Ed. Chapter 24 Problem 6
cross_references: ["[[题-608-Clayden-Ch36-P1-原子编号追踪重排]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-609-Clayden-Ch36-P2-Beckmann重排立体化学和机理]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-437: Friedel-Crafts/Wolff-Kishner序列中A和B

## 题目

Identify A and B and account for the selectivity displayed in this sequence of reactions.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/28afa9b08f22dc76ea2ec691ae1edeabbbc8b14fc42240d31bd0cc0545e5316d.jpg]]

**原文题目**：鉴定A和B，并解释该反应序列中展示的选择性。

## 参考答案

**Answer (English)**:

The Friedel-Crafts acylation in the first step is controlled by the bromo substituent, which is an ortho,para director: here we get para selectivity as usual for steric reasons. The product A is a ketoacid.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/7734284ba3cef5e79f621f3fa01e5325330479a0159a56cd170ed4182630806a.jpg]]

The next step is the Wolff-Kishner reduction. The product is the acid B (or its potassium salt). Now adding acid forms a ring in another Friedel-Crafts acylation. The electrophile must be the acylium ion: usually Friedel-Crafts acylations need more than just strong acid, but this one is fast because it is intramolecular. The only positions the electrophile can reach are ortho to the carbon chain, so it must react there even though that means it has to attack meta to the Br group. It's still ortho to the alkyl chain, which is ortho,para directing.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/903e5ea21c280dcbc90190e70980d4ea9235439643382a2e181d0284cd048353.jpg]]

**中文解析**：

**第一步：Friedel-Crafts酰基化 → 产物A**
- Br是邻/对位定位基（通过孤对电子的共轭效应）
- 酰基优先进攻对位（位阻原因，邻位有Br的位阻）
- A = 对位酰基化的溴苯衍生物（酮酸）

**第二步：Wolff-Kishner还原 → 产物B**
- 将C=O还原为CH₂（碱性条件下肼还原）
- B = 还原后的羧酸（或其钾盐）

**第三步：分子内Friedel-Crafts酰基化 → 环化产物**
- 酸处理下，B中的COOH形成酰基正离子（acylium ion）
- 这是分子内反应，所以反应速度很快（即使通常FC酰化需要Lewis酸催化）
- **区域选择性**：酰基正离子只能到达碳链的邻位（空间可达性限制）
- 虽然该位点处于Br的间位，但它处于烷基链的邻位（烷基是邻/对位定位基）
- 结果：形成六元环酮（萘酮衍生物）

**核心概念**：分子内反应的选择性往往由空间可达性（哪个位点能被分子内的亲电体够到）而非取代基的电子效应决定。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[区域选择性]] | Friedel-Crafts酰化中对位选择性；分子内环化的位点选择 | 直接 |
| Friedel-Crafts反应 | Friedel-Crafts酰基化的机理和区域选择性 | 直接 |
| Wolff-Kishner还原 | C=O还原为CH₂的条件和适用范围 | 间接 |
| [[分子内反应]] | 分子内FC酰化的优势和选择性控制 | 间接 |

## 解题思路

1. **读题定位**：三步序列——FC酰化→Wolff-Kishner→分子内FC环化，要求鉴定中间体A和B并解释选择性
2. **🔑 关键转换**：
   - 步骤1：Br邻/对位定位→对位酰化（位阻优先）→A
   - 步骤2：Wolff-Kishner还原C=O→CH₂→B
   - 步骤3：分子内FC环化→酰基正离子够到碳链邻位→六元环产物
3. **验证**：A的结构符合对位选择性；B的结构是还原产物；最终产物的环化位点在碳链邻位

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为Br的定位效应在环化步骤也控制选择性 | 环化步骤中空间可达性比电子效应更重要 | 酰基正离子只能到达碳链的邻位，Br的间位定位效应被空间因素覆盖 | 什么时候空间效应可以override电子效应？ |
| 将A画成邻位酰化产物 | 忽略了Br的位阻 | Br的位阻使得对位选择性占主导 | 什么条件下邻位选择性会更好？ |
| 不理解Wolff-Kishner还原 | 混淆Wolff-Kishner和Clemmensen还原 | Wolff-Kishner：碱性条件（KOH/N₂H₄）；Clemmensen：酸性条件（Zn(Hg)/HCl） | 两个还原反应各适用于什么底物？ |
| 不理解分子内FC为何不需要Lewis酸 | 认为FC酰化总是需要AlCl₃ | 分子内反应熵有利，活化能更低，强酸即可产生酰基正离子 | 分子内FC酰化的适用条件是什么？ |