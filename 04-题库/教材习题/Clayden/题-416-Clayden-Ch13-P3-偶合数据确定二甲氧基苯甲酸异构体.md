---
title: 题-416-Clayden-Ch13-P3-偶合数据确定二甲氧基苯甲酸异构体
type: 题目
submodule: NMR谱学
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch13-P3]
source: Clayden Organic Chemistry 2nd Ed. Chapter 13 Problem 3
cross_references: ["[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]", "[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]", "[[题-536-Clayden-Ch18-P1-C6H5FO的13C NMR C-F偶合结构确定]]", "[[题-537-Clayden-Ch18-P2-Bullatenone结构A预测NMR并纠正]]"]
module: 有机化学
status: 已填充
---
# 题-416: 偶合数据确定二甲氧基苯甲酸异构体

## 题目

One isomer of dimethoxybenzoic acid has the ¹H NMR spectrum δ_H (ppm) 3.85 (6H, s), 6.63 (1H, t, J 2 Hz), and 7.17 (2H, d, J 2 Hz). One isomer of coumalic acid has the ¹H NMR spectrum δ_H (ppm) 6.41 (1H, d, J 10 Hz), 7.82 (1H, dd, J 2, 10 Hz), and 8.51 (1H, d, J 2 Hz). In each case, which isomer is it? The bonds sticking into the centre of the ring can be to any carbon atom.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/e42a07aaabf6daa9e36c00addcc2672a9082a270613d091fea4156547597a792.jpg]]

## 参考答案

**Answer (English)**: The coupling constants in the first spectrum are all too small to be between hydrogens on neighbouring carbon atoms, and there must be symmetry in the molecule. There is only one structure that answers these criteria: 3,5-dimethoxybenzoic acid.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/f545617289e469e44ab7ba701dc0c7a5468a4f9489df5d2eee8e1035ca038fd6.jpg]]

The second compound has one coupling of 10 Hz (ortho coupling between protons on neighbouring carbons), and the other coupling of 2 Hz is too small to be anything but meta coupling. The first structure is correct, and you might have worked this out from the very large chemical shift — almost in the aldehyde region — of the isolated proton with only a 2 Hz coupling. This proton is on an alkene carbon bonded to oxygen in the first structure, but on a simple alkene carbon in the second.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/84f86d3dc7333d0154b9bfb17a17ce0624d4b846eda7c1feafe19b7872a80726.jpg]]

**中文解析**：

关键要点：
1. **偶合常数判断连接关系**：J = 2 Hz太小，不可能是邻位偶合（正常邻位J = 7–10 Hz），必然是间位偶合（meta coupling）
2. **对称性判断**：第一个谱中6H单峰说明两个OMe等价，2H双峰和1H三峰说明芳香环有对称性——只有3,5-二甲氧基苯甲酸符合
3. **化学位移辅助判断**：第二个化合物中8.51 ppm的H位移极大（接近醛区），说明该H连接在与O相连的烯碳上

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | 通过偶合模式推断取代基位置 | 直接 |
| [[偶合常数]] | 邻位（7–10 Hz）vs 间位（2 Hz）偶合区分 | 直接 |
| [[化学位移]] | 化学位移辅助判断H的化学环境 | 直接 |
| [[芳香族化合物]] | 芳香环取代模式与NMR的关系 | 间接 |

## 解题思路

1. **读题定位**：题目给出两个化合物的¹H NMR数据，要求推断具体异构体——核心是利用偶合常数和对称性
2. **🔑 关键转换**：J值大小判断连接关系（邻位/间位）→对称性缩小候选结构→化学位移验证
3. **验证**：将推断结构的预期NMR与实际数据对比，检查所有信号是否一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将2 Hz偶合误判为邻位偶合 | 不熟悉偶合常数范围 | 邻位偶合J = 7–10 Hz，间位J ≈ 2 Hz | 苯环上邻位、间位、对位偶合常数分别是多少？ |
| 忽略对称性约束 | 没有分析等价H的数目 | 6H单峰说明两个OMe等价，限定了取代模式 | 3,5-二取代苯有几种等价H？ |
| 不利用化学位移验证 | 只看偶合不看位移 | 8.51 ppm的H在与O相连的烯碳上，位移应很大 | 连氧烯碳上的H为什么位移特别大？ |