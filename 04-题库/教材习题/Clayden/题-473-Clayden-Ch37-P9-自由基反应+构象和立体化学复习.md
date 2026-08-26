---
title: 题-473-Clayden-Ch37-P9-自由基反应+构象和立体化学复习
type: 题目
fidelity: 原书逐字
submodule: 自由基反应
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[自由基]]"]
tags: [化竞, Clayden, 有机化学, 自由基反应]
updated: 2026-07-25
aliases: [Clayden-Ch37-P9]
source: Clayden Organic Chemistry 2nd Ed. Chapter 37 Problem 9
cross_references: ["[[题-466-Clayden-Ch37-P2-重氮盐亲核取代vs自由基对比]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-465-Clayden-Ch37-P1-重要自由基反应复习]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-473: Corey Epibatidine合成中的自由基+构象/立体化学

## 题目

The last few stages of Corey's epibatidine synthesis are shown here. Give mechanisms for the first two reactions and suggest a reagent for the last step.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/a5a5fa1e03d819c70baf85072c8525ab194b6b2a7f78ff1ab13810b20d36b80e.jpg]]

**原文题目**：The last few stages of Corey's epibatidine synthesis are shown here. Give mechanisms for the first two reactions and suggest a reagent for the last step.

## 参考答案

**Answer (English)**: The first step involves deprotonation of the rather acidic amide (the CF₃ group helps) and the displacement of the only possible bromide—the one on the opposite face of the six-membered ring as the S_N2 reaction must take place with inversion.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/9bc00c6b8c9c103e417cd56ef2c95a9a6d49677bb342a602ec237b306acacd2b.jpg]]

The second step is a standard dehalogenation by Bu₃SnH. AIBN generates Bu₃Sn· by hydrogen abstraction from the reagent and this removes the bromine. Make sure you complete the chain and do not use H· at any point.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/12e898c7f2cb4bb734c78fd341ff0661ed8807d540e8e49d89e423f6c5c267a7.jpg]]

Finally we need to hydrolyse the amide. This normally requires strong acid or alkali but the CF₃ group makes this amide significantly more electrophilic than most and milder conditions can be used. Corey actually used NaOMe in methanol at 13 °C for two hours and got a yield of 96%. Any reasonable conditions you may have chosen would be fine too.

**中文解析**：

关键步骤：

**第一步：分子内SN2环化**
1. CF₃基团使酰胺N-H酸性增强 → 碱去质子化 → 酰胺氮负离子
2. 氮负离子对六元环上反面的C-Br进行SN2进攻（必须在反面，因为SN2要求背面进攻/构型翻转）
3. 形成新的C-N键，构建epibatidine的双环骨架

**第二步：Bu₃SnH自由基脱溴**
1. AIBN引发：热分解产生自由基 → 从Bu₃SnH夺氢 → 产生Bu₃Sn·
2. Bu₃Sn·从底物夺取Br → 产生碳自由基
3. 碳自由基从另一分子Bu₃SnH夺氢 → 得到产物 + 再生Bu₃Sn·（链传递）
4. ⚠️ 注意：不能画H·直接参与，必须通过Bu₃Sn·/Bu₃SnH循环

**第三步：酰胺水解**
- CF₃的强吸电子效应使酰胺羰基更缺电子，更容易被亲核进攻
- 温和条件即可水解：NaOMe/MeOH, 13°C, 2h → 96%收率
- 产物是游离胺（epibatidine的去甲基类似物）

> **注意**：这个例子展示了自由基反应在天然产物全合成中的应用，以及CF₃基团如何活化通常惰性的酰胺键。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[自由基]] | Bu₃SnH脱溴的自由基链机理 | 直接 |
| [[构象分析]] | SN2环化要求反面进攻（构象控制） | 直接 |
| [[立体化学]] | SN2的构型翻转和产物立体化学 | 直接 |
| [[酰胺水解]] | CF₃活化酰胺的温和水解 | 间接 |

## 解题思路

1. **读题定位**：三步反应分别涉及SN2环化、自由基脱溴和酰胺水解——需要综合有机化学多个章节的知识
2. **关键转换**：碱去质子化酰胺 → SN2环化（反面进攻） → Bu₃SnH脱溴（自由基链） → 酰胺水解（CF₃活化）
3. **验证**：检查SN2是否在反面发生，自由基链是否完整（不能有H·），水解条件是否合理

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| SN2环化画在同面 | 忽略了SN2的立体化学要求 | SN2必须背面进攻，产物构型翻转 | SN2的立体化学要求是什么？ |
| 自由基脱溴中画H· | 没有理解Bu₃SnH的作用 | H必须通过Bu₃Sn·/Bu₃SnH循环传递，不能有游离H· | 为什么不能有H·？ |
| 用强酸/强碱水解酰胺 | 没有考虑CF₃的活化作用 | CF₃使酰胺更容易水解，温和条件（NaOMe/MeOH）即可 | CF₃如何活化酰胺？ |
| 忘记解释为什么选择反面Br | 没有考虑构象因素 | 六元环上只有一个Br在反面，SN2只能进攻它 | 如果两个Br都在同面会怎样？ |