---
title: "题-610-Clayden-Ch36-P3-硼参与重排加关环重排加立体化学"
type: 题目
fidelity: 原书逐字
submodule: 重排反应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
question_type: [作图]
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[重排反应]]"]
tags: [化竞, Clayden, 有机化学, 重排反应, 硼氢化, 立体化学]
updated: 2026-07-25
aliases: [Clayden-Ch36-P3]
source: Clayden Organic Chemistry 2nd Ed. Chapter 36 Problem 3
cross_references: ["[[题-514-Clayden-Ch40-P1-烯醇醚溴化WittigPd化学入门]]", "[[题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择]]", "[[题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性]]", "[[题-515-Clayden-Ch40-P2-Heck反应机理步骤理解]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
source_grade: B
---
# 题-610: 硼参与重排 + 关环重排 + 立体化学

## 题目

**【中文】**画出这些反应（见图）的机理和中间体的结构。解释其立体化学，特别是涉及硼的反应。为什么选择 9-BBN 作为硼氢化试剂？

**【原文】**Draw mechanisms for the reactions and structures for the intermediates. Explain the stereochemistry, especially of the reactions involving boron. Why was 9-BBN chosen as the hydroborating agent?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/fc4a418a3a59951a295609e625eca69217d2484a75b6d2245919ff2a08e6455f.jpg]]

**原文题目**：画出反应的机理和中间体结构。解释立体化学，特别是涉及硼的反应。为什么选择9-BBN作为硼氢化试剂？

## 参考答案

**Answer (English)**: The structure of 9-BBN and the mechanism of the oxidation are described on p. 446 of the textbook.

The starting material is symmetrical so it doesn't matter which face of which alkene you attack. The only important things are that boron binds to the more nucleophilic end of the alkene and that R₂BH and H are added cis. Alkaline H₂O₂ makes the hydroperoxide anion (HOO⁻) which attacks boron.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/27eb4513d1eab0d8da2060f6b19ac876bed3bfab384866677d1af627384c986a.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/95a8507c9531f22ae716bffbf0193806d47053252bc716609e91bb3d0a624173.jpg]]

The mesylate cyclizes in aqueous base. The more nucleophilic end of the remaining alkene displaces the mesylate with inversion to make the cis ring junction much preferred by the 5,5 fused system. Water adds to the tertiary cation to give the next intermediate.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/2ce67fa013c9c5be8363d3d518e3dc44cf5c7bf7b4cc66eddb30dc3426d687b0.jpg]]

Elimination of the alcohol (E1 of course as it is tertiary) gives the alkene and a repeat of the hydroboration from the outside (convex face) of the folded molecule gives the final alcohol with five new stereogenic centres.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/c67f71ffff4cd95e75de992051775ff80436d6bff8fce5f7f0ea34b3abb055a4.jpg]]

9-BBN was chosen because it is very large and reinforces the natural electronic preference of boron to bind to the less substituted end of the alkene with an extra steric effect. It also has bridgehead atoms bound to boron and they make poor migrating groups, forcing the migration of the third B substituent.

**中文解析**：

本题涉及**四个连续反应步骤**，每步都涉及立体化学控制：

1. **9-BBN硼氢化**：底物对称，从任一烯烃面进攻均可。硼连接到烯烃更亲核的一端，R₂BH和H顺式加成。9-BBN体积大，增强区域选择性（硼连接到取代较少的碳），且桥头碳原子不易迁移，迫使第三个B取代基迁移
2. **碱性H₂O₂氧化**：HOO⁻进攻硼→1,2-迁移→C-B键变为C-OH键，构型保持
3. **甲磺酸酯环化**：碱性水溶液中，剩余烯烃的亲核端以构型翻转（inversion）方式取代甲磺酸酯，形成顺式稠合的5,5双环体系（5元环稠合更倾向于顺式）
4. **E1消除 + 第二次硼氢化**：叔醇E1消除得烯烃，分子折叠后从凸面进行第二次硼氢化，得到含5个新立体中心的最终产物

> **为什么选9-BBN？**
> - 体积大 → 增强区域选择性（硼优先连接位阻小的碳）
> - 桥头碳原子与硼相连 → 不是好的迁移基团 → 迫使第三个取代基迁移
> - 最终产物用于合成iridoid萜类化合物（Matthews & Whitesell, J. Org. Chem., 1975, 40, 3313）

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[重排反应]] | 硼氧化过程中的1,2-迁移 | 直接 |
| [[1,2-迁移与重排]] | 硼→碳的1,2-烷基迁移 | 直接 |
| [[立体化学]] | 顺式加成、构型翻转、面选择性 | 直接 |
| [[硼氢化氧化]] | 9-BBN硼氢化 + 碱性H₂O₂氧化 | 直接 |
| [[环张力]] | 5,5双环体系顺式稠合的偏好 | 间接 |

## 解题思路

1. **读题定位**：四个连续反应步骤，重点是机理、中间体结构、立体化学和9-BBN的选择原因
2. **🔑 关键转换**：对称双烯 → 硼氢化（顺式加成）→ 氧化（C-B→C-OH）→ 甲磺酸酯环化（反式取代）→ E1消除 → 第二次硼氢化（凸面进攻）→ 五立体中心产物
3. **验证**：检查每个步骤的立体化学是否自洽；最终产物的5个立体中心是否与机理一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 硼氢化写成反式加成 | 混淆硼氢化和卤化 | 硼氢化是顺式加成（syn addition） | 硼氢化和溴化的立体化学有何不同？ |
| 忘记氧化步骤的构型保持 | 不理解1,2-迁移的立体化学 | 碱性H₂O₂氧化中，C-B键变为C-OH键，构型完全保持 | 氧化过程中哪一步发生构型保持？ |
| 环化时忘记构型翻转 | 混淆SN1和SN2 | 甲磺酸酯环化是SN2过程，发生构型翻转 | 为什么5,5双环体系更倾向于顺式稠合？ |
| 不理解9-BBN的优势 | 只知道"体积大" | 9-BBN的桥头碳不易迁移 + 体积大增强区域选择性 = 双重优势 | 如果用BH₃代替9-BBN，选择性会如何变化？ |