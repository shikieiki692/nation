---
title: 题-435-Clayden-Ch24-P4-精细定位效应的芳香硝化
type: 题目
fidelity: 原书逐字
submodule: 区域选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[区域选择性]]"]
tags: [化竞, Clayden, 有机化学, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch24-P4]
source: Clayden Organic Chemistry 2nd Ed. Chapter 24 Problem 4
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-608-Clayden-Ch36-P1-原子编号追踪重排]]", "[[题-609-Clayden-Ch36-P2-Beckmann重排立体化学和机理]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-435: 精细定位效应的芳香硝化

## 题目

**【中文】**下面的硝基化合物是合成止吐药所需的。有人提议通过硝化所示烃来制备。你认为这会成功吗？

**【原文】**
The nitro compound below was needed for the synthesis of an anti-emetic drug. It was proposed to make it by nitration of the hydrocarbon shown. How successful do you think this would be?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/12b83ce1e331b4f3e730ecb9fc9bb9b4a7b974f87073f1929ff6dadc151186dd.jpg]]

## 参考答案

**Answer (English)**: The standard conditions for nitration generate the electrophile NO₂⁺. To get the product shown, this species has to attack the ring at a specific position. The intermediate cation looks quite reasonable since the positive charge can be delocalized even into the other ring.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/3667e06f559e6eb2c6e65566ae6d07366d5822dc1317d8433395221690a2f710.jpg]]

What about the alternatives? A similar cation is formed if the electrophile attacks position '1', but the nitro group is in a more hindered position here. Position '2' gives a cation that does not benefit from the same degree of stabilization (it cannot be delocalized into the other ring). Position 4 is similar but more hindered. Overall we can reasonably expect the reaction to give the product we want.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/40eaea16bc04c6e08b35fbc18482b75465d2dabc46d87c1126c19a1ce4e49e21.jpg]]

**中文解析**：

该问题考察对芳香亲电取代中间体（σ-配合物/Wheland中间体）稳定性的精细分析：

1. **目标产物的形成路径**：NO₂⁺进攻特定位置，形成的σ-配合物中间体中正电荷可以离域到另一个环上——这是特别稳定的中间体
2. **位置1**：也能形成类似的离域中间体，但硝基最终处于更拥挤的位阻位置
3. **位置2**：形成的σ-配合物中正电荷无法离域到另一个环（共轭体系被阻断），稳定性较差
4. **位置4**：与位置2类似，但位阻更大

**结论**：反应可以合理地给出目标产物。目标位置形成的中间体最稳定（双环离域），且位阻适中，因此该位置是动力学和热力学的优先选择。

**关键概念**：在多环体系中，亲电取代的区域选择性不仅取决于取代基的定位效应，还取决于σ-配合物中间体能否利用整个共轭体系来稳定正电荷。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[区域选择性]] | 多个可能反应位点中的精细选择性分析 | 直接 |
| [[芳香亲电取代]] | σ-配合物中间体稳定性对区域选择性的控制 | 直接 |
| [[定位效应]] | 甲基作为活化基团的定位作用 | 间接 |
| [[Wheland中间体]] | 亲电取代的关键中间体及其稳定性 | 间接 |

## 解题思路

1. **读题定位**：硝化一个双环芳烃，问能否得到目标硝基化合物
2. **🔑 关键转换**：画出每个可能位点被NO₂⁺进攻后形成的σ-配合物→比较正电荷离域范围和位阻→判断哪个中间体最稳定
3. **验证**：目标位点的中间体正电荷可离域到两个环→最稳定；其他位点要么位阻大，要么离域不充分

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 只考虑取代基定位效应 | 忽略了多环体系中中间体离域的重要性 | 在稠环体系中，σ-配合物能否离域到另一环是关键因素 | 为什么位置2的中间体不如目标位置稳定？ |
| 认为位阻是唯一因素 | 没有分析电子效应 | 位阻和电子效应共同决定区域选择性 | 如果所有位点位阻相同，选择性由什么决定？ |
| 忽略σ-配合物的分析 | 直接用过渡态判断产物 | 应该画出各位置的σ-配合物中间体来分析稳定性 | σ-配合物和过渡态有什么关系？ |