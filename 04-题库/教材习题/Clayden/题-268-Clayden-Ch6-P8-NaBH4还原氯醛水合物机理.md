---
title: 题-268-Clayden-Ch6-P8-NaBH4还原氯醛水合物机理
type: 题目
fidelity: 原书逐字
submodule: 羰基亲核加成
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
question_type: [机理]
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[羰基亲核加成]]", "[[硼氢化钠还原]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch6-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 6 Problem 8
cross_references: ["[[题-262-Clayden-Ch6-P1-硼氢化钠还原醛酮机理]]", "[[题-265-Clayden-Ch6-P4-NaBH4还原二羰基选择性]]", "[[题-269-Clayden-Ch6-P10-Grignard加成+NaBH4选择性还原]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
source_grade: B
---
# 题-268: NaBH₄还原氯醛水合物机理

## 题目

Trichloroethanol may be prepared by the direct reduction of chloral hydrate in water with sodium borohydride. Suggest a mechanism for this reaction. Take note that sodium borohydride does not displace hydroxide from carbon atoms!

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/aa6aa676300a73982ff563f893c757e1a599b881740da8a9b56319f2b705703a.jpg]]

**原文题目**：三氯乙醇可以通过NaBH₄在水中直接还原氯醛水合物制备。建议该反应的机理。注意：NaBH₄不会从碳原子上取代氢氧根！

## 参考答案

**Answer (English)**: If sodium borohydride doesn't displace hydroxide from carbon atoms, then what does it do? We know it attacks carbonyl groups to give alcohols and to get trichloroethanol we should have to reduce chloral. Hemiacetals are in equilibrium with their carbonyl equivalents, so...

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/5e564cd9f4e51fc129720daa3efbd22b6740b8bcb64171bc5f8e4fff4d32aac6.jpg]]

**中文解析**：

这道题的关键是识别一个"隐藏"的平衡：

**错误思路**：直接用NaBH₄取代氯醛水合物上的-OH → ✗（NaBH₄不做亲核取代）

**正确思路**：
1. **水合物⇌醛平衡**：氯醛水合物（CCl₃CH(OH)₂）与氯醛（CCl₃CHO）存在平衡
2. **NaBH₄还原醛**：平衡中少量的氯醛被NaBH₄还原为三氯乙醇
3. **平衡移动**：产物被移除→平衡向右移动→最终全部转化为三氯乙醇

这个机理的精髓：**不要只看起始物料的结构，要考虑它在溶液中的平衡状态**。水合物是"伪装"的醛！

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[羰基亲核加成]] | NaBH₄还原醛的核心步骤 | 直接 |
| [[硼氢化钠还原]] | NaBH₄只能还原羰基，不能做亲核取代 | 直接 |
| [[平衡常数]] | 水合物-醛平衡驱动反应 | 直接 |
| [[水合物]] | 水合物作为"隐藏"的羰基化合物 | 间接 |

## 解题思路

1. **读题定位**：NaBH₄还原氯醛水合物→产物是三氯乙醇。题目提示"NaBH₄不取代OH"→必须找到替代路径
2. **🔑 关键转换**：水合物⇌醛平衡！氯醛水合物（CCl₃CH(OH)₂）在溶液中与游离的CCl₃CHO存在平衡，NaBH₄还原的是平衡中的游离醛，产物移除后平衡右移
3. **验证**：检查最终产物——CCl₃CH₂OH（三氯乙醇），确实是CCl₃CHO被还原的产物

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 画NaBH₄直接取代OH | 没读题（题目明确说NaBH₄不取代OH） | NaBH₄是还原剂不是亲核取代试剂，只能进攻C=O | NaBH₄能做什么反应？不能做什么？ |
| 忽略水合物-醛平衡 | 没有意识到水合物是"伪装"的醛 | CCl₃CH(OH)₂ ⇌ CCl₃CHO + H₂O，NaBH₄还原游离醛 | 为什么氯醛容易形成水合物？（CCl₃吸电子效应） |
| 画出NaBH₄取代Cl的副反应 | 混淆了不同反应类型 | NaBH₄在温和条件下不取代Cl（需要更强的还原剂如LiAlH₄） | 如何选择性还原CCl₃CHO中的C=O而不脱Cl？ |