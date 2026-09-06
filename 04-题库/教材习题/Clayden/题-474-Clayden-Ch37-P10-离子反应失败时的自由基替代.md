---
title: 题-474-Clayden-Ch37-P10-离子反应失败时的自由基替代
type: 题目
fidelity: 原书逐字
submodule: 自由基反应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
question_type: [机理]
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[自由基]]"]
tags: [化竞, Clayden, 有机化学, 自由基反应]
updated: 2026-07-25
aliases: [Clayden-Ch37-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 37 Problem 10
cross_references: ["[[题-465-Clayden-Ch37-P1-重要自由基反应复习]]", "[[题-466-Clayden-Ch37-P2-重氮盐亲核取代vs自由基对比]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
used_in: ["[[有机化学阶段测试卷]]", "[[04-题库/有机化学阶段测试卷]]"]
source_category: 教材课后习题
---
# 题-474: 自由基替代离子反应——碘内酯化+自由基烯丙基化

## 题目

**【中文】**你将如何制备这一系列反应的起始原料？给出第一步反应的机理，并解释其区域选择性和立体选择性。你的答案应包括产物的构象图。最后一步的机理是什么？试图通过碘/锂交换再与烯丙基溴反应来完成最后一步的尝试失败了，为什么？为什么此处所示的替代方法能够成功？（反应式见图）

**【原文】**How would you make the starting material for this sequence of reactions? Give a mechanism for the first reaction that explains its regio- and stereoselectivity. Your answer should include a conformational drawing of the product. What is the mechanism of the last step? Attempts to carry out this last step by iodine/lithium exchange and reaction with allyl bromide failed. Why? Why is the alternative shown here successful?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/1af86c62a92cc68f2812da3fad653257554972bf289a775fad4349449be298de.jpg]]

**原文题目**：How would you make the starting material for this sequence of reactions? Give a mechanism for the first reaction that explains its regio- and stereoselectivity. Your answer should include a conformational drawing of the product. What is the mechanism of the last step? Attempts to carry out this last step by iodine/lithium exchange and reaction with allyl bromide failed. Why? Why is the alternative shown here successful?

## 参考答案

**Answer (English)**: The starting material is an obvious Diels-Alder product as it is a cyclohexene with a carbonyl group outside the ring on the opposite side. The first step is iodolactonization. Iodine attacks the alkene reversibly on both sides but, when it attacks opposite the carboxylate anion, the lactone ring snaps shut.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/9a422879094cf8ded6eff61dd75dbdcb870f2d1b27a40ad0f96db884e4dd2d08.jpg]]

The problem asks for a conformational drawing of the product and indeed that is necessary. The 1,3-lactone bridge must be diaxial as that is the only way for the carboxylate to reach across and therefore it must attack from an axial direction too.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/2e8ca69db5f4d5f2e9409757810375740272b407128abc40e689626af9aa5041.jpg]]

The last step is initiated by AIBN which removes the iodine atom from the compound to make a secondary radical. This attacks the allyl stannane and the intermediate loses Bu₃Sn· and that takes over the job of removing iodine atoms to keep the chain going. The radical intermediate has no stereochemistry at the planar radical carbon and attack occurs from the bottom face to avoid the blocking lactone bridge.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/638cf23b3361784449266d6f8792f0013c9c83627c9a31bfb81235140c701a87.jpg]]

Anionic reactions cannot be used for this allylation. If the iodine were metallated, the organometallic compound would immediately expel the lactone bridge as carboxylate ion is a good leaving group. The radical is stable because the C–O bond is strong and not easily cleaved in radical reactions.

![[278bf835e89f28110091fec17d3386ccc6d065838079decf57a03903c7a82383.jpg]]

**中文解析**：

关键步骤：

**起始原料合成**：Diels-Alder反应构建环己烯骨架（羰基在环外、与环反面）

**第一步：碘内酯化（Iodolactonization）**
1. I₂可逆地加成到烯烃两侧，但只有当I⁺从羧酸根反面进攻时，内酯环才能关环
2. 构象分析：1,3-内酯桥必须是双直立键（diaxial），因为只有这种构象才能让羧酸根跨越环的两侧
3. 因此I⁺必须从轴向进攻，羧酸根也从轴向关环

**第二步：自由基烯丙基化（关键步骤）**
1. AIBN引发 → 从底物夺取I → 产生仲碳自由基
2. 自由基进攻烯丙基三丁基锡（allyl stannane）→ 加成后失去Bu₃Sn· → 完成链循环
3. 立体化学：自由基碳是平面的，进攻从底面发生（避免内酯桥的空间阻碍）

**为什么离子反应失败？**
- 如果用I/Li交换产生有机锂试剂 → 有机锂会立即消除内酯桥（羧酸根是好的离去基团）
- 自由基中间体稳定，因为C-O键强，在自由基条件下不易断裂
- 这是自由基化学替代离子化学的经典案例

> **注意**：碘内酯化是构建含碘内酯的立体选择性方法，后续的自由基脱碘/烯丙基化利用了锡试剂的特殊反应性。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[自由基]] | Bu₃SnH/AIBN自由基烯丙基化机理 | 直接 |
| [[亲核取代]] | 离子反应（I/Li交换）为何失败 | 直接 |
| [[立体化学]] | 碘内酯化的立体选择性和产物构象 | 间接 |
| [[化学选择性]] | 自由基vs离子条件下的不同反应性 | 间接 |

## 解题思路

1. **读题定位**：三问——原料合成、第一步机理（含构象）、最后一步机理+为什么离子法失败
2. **关键转换**：Diels-Alder合成原料 → 碘内酯化（双直立产物）→ 自由基脱碘+烯丙基化 → 离子法失败原因（有机锂消除内酯）
3. **验证**：检查碘内酯化产物是否为双直立构象，自由基链是否完整，离子法失败原因是否合理

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 碘内酯化产物画成平伏键 | 没有理解1,3-桥必须双直立 | 1,3-内酯桥只能是双直立键（diaxial） | 为什么双直立是唯一可能？ |
| 忘记解释离子法失败 | 只回答了自由基机理 | I/Li交换产生的有机锂会消除内酯桥（羧酸根是好的离去基团） | 为什么自由基不失消除？ |
| 画自由基进攻从顶面 | 没有考虑空间阻碍 | 内酯桥在顶面，进攻必须从底面 | 空间阻碍如何控制立体化学？ |
| 混淆烯丙基化和简单夺氢 | 没有理解Bu₃SnH/allyl stannane的区别 | 这里用的是烯丙基锡（allyl stannane），不是Bu₃SnH | allyl stannane和Bu₃SnH的区别是什么？ |