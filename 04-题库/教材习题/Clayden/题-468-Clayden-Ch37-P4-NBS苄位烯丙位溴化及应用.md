---
title: 题-468-Clayden-Ch37-P4-NBS苄位烯丙位溴化及应用
type: 题目
fidelity: 原书逐字
submodule: 自由基反应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[自由基取代]]"]
tags: [化竞, Clayden, 有机化学, 自由基反应]
updated: 2026-07-25
aliases: [Clayden-Ch37-P4]
source: Clayden Organic Chemistry 2nd Ed. Chapter 37 Problem 4
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-465-Clayden-Ch37-P1-重要自由基反应复习]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-466-Clayden-Ch37-P2-重氮盐亲核取代vs自由基对比]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
---
# 题-468: NBS苄位/烯丙位溴化及后续环化

## 题目

Treatment of this aromatic heterocycle with NBS (N-bromosuccinimide) and AIBN gives mainly one product but this is difficult to purify from minor impurities containing one or three bromine atoms. Further treatment with 10% aqueous NaOH gives one easily separable product in modest yield (50%). What are the mechanisms for the reactions?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/e7d7698a46752459e6b10b213c4975dbf1202d07ea573142e4c2fbe076e7aacf.jpg]]

**原文题目**：Treatment of this aromatic heterocycle with NBS (N-bromosuccinimide) and AIBN gives mainly one product but this is difficult to purify from minor impurities containing one or three bromine atoms. Further treatment with 10% aqueous NaOH gives one easily separable product in modest yield (50%). What are the mechanisms for the reactions?

## 参考答案

**Answer (English)**: Two preliminary reactions need to take place: NBS is a source of a low concentration of bromine molecules and AIBN initiates the radical chain by forming a nitrile-stabilized tertiary radical.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/723b09648b43a77da316883ea1d3b645246ff492e1591f2eb0a6ba794b9badb9.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/278dc79dd2833b128f45b553ccf5050f064c18365e5a6fc4b4634dc0d4ec872d.jpg]]

The new radical abstracts hydrogen atoms from the benzylic positions to make stable delocalized radicals. These react with bromine to give the benzylic bromide and release a bromine atom.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/0b37a8f2009e40535f308e7a4649a3d56c5d9387c4dedbdd5a063db22b0382c9.jpg]]

All subsequent hydrogen abstractions are carried out by bromine atoms, either of the kind we have just seen or to remove a hydrogen atom from the other methyl group. This reaction provides the HBr that generates more bromine from NBS.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/34ef506a5d09c7d43f8d00dc83bf81338317c2d0fc1614a70459fea724f44a12.jpg]]

Finally the dibromide reacts with NaOH to give the new heterocycle. Both S_N2 displacements are very easy at a benzylic centre and the second is intramolecular.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/59fac28ea87506252af3240e6a1a161df130e6f511d6c59f35fd9ca8f0682557.jpg]]

**中文解析**：

关键步骤：
1. **NBS的双重角色**：NBS本身不直接溴化，而是提供低浓度Br₂。AIBN引发产生自由基，NBS与HBr反应再生Br₂（维持低浓度）
2. **AIBN引发**：AIBN热分解产生氰基稳定的叔自由基，该自由基从NBS夺取Br·，开始链反应
3. **苄位溴化**：Br·从苄位甲基夺取氢原子，产生苄基自由基（被芳环离域稳定）→ 苄基自由基与Br₂反应 → 苄基溴 + Br·（链传递）
4. **多溴化问题**：Br·也可以从另一个甲基夺氢，产生二溴代物（副产物含1个或3个Br）
5. **NaOH环化**：二溴代物在NaOH条件下发生两次S_N2取代——第一次是分子间取代（OH⁻进攻苄位Br），第二次是分子内环化（O⁻进攻另一个苄位Br），形成新的杂环

> **注意**：苄位的S_N2反应特别容易发生，因为过渡态中芳环可以稳定发展的正电荷。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[自由基取代]] | NBS溴化的自由基链反应机理 | 直接 |
| [[自由基]] | 苄基自由基的形成和稳定性 | 直接 |
| [[键解离能]] | 苄位C-H键解离能低，易被夺取 | 间接 |
| NBS溴化 | NBS作为Br₂的缓释源 | 间接 |

## 解题思路

1. **读题定位**：题目涉及两步反应——NBS/AIBN溴化和NaOH环化。需要分别写出两个机理
2. **🔑 关键转换**：NBS提供Br₂ → AIBN引发自由基链 → Br·夺取苄位H → 苄基溴（+副产物多溴代物）→ NaOH水解环化
3. **验证**：检查溴化是否发生在苄位（而非芳环上），环化产物是否为含氧杂环，副产物是否含1或3个Br

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为NBS直接提供Br⁺ | 混淆自由基和离子机理 | NBS通过自由基链提供低浓度Br₂，不是离子溴化 | NBS和Br₂在机理上有什么区别？ |
| 在芳环上画溴化 | 忘记自由基溴化的选择性 | 自由基溴化发生在苄位/烯丙位（C-H键弱），不在芳环上 | 为什么苄位C-H比芳环C-H更容易被夺取？ |
| 忽略多溴化副产物 | 没有考虑反应的多次发生 | 第一个Br取代后，另一个甲基也可能被溴化，产生二溴代物 | 如何控制只发生单溴化？ |
| 环化机理写成E2消除 | 混淆取代和消除 | NaOH条件下是S_N2取代（OH⁻进攻苄位Br），不是消除 | 为什么苄位S_N2特别容易？ |