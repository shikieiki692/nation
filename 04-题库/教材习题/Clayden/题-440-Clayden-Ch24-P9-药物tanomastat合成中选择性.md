---
title: 题-440-Clayden-Ch24-P9-药物tanomastat合成中选择性
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
aliases: [Clayden-Ch24-P9]
source: Clayden Organic Chemistry 2nd Ed. Chapter 24 Problem 9
cross_references: ["[[题-608-Clayden-Ch36-P1-原子编号追踪重排]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-609-Clayden-Ch36-P2-Beckmann重排立体化学和机理]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-440: 药物tanomastat合成中选择性

## 题目

**【中文】**解释药物tanomastat合成中展示的区域选择性。

**【原文】**
Explain the regioselectivity displayed in this synthesis of the drug tanomastat.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/139ca9d8ebf004213c696843725a5f602db04e39df62a126846ca9636ffe94fa.jpg]]

## 参考答案

**Answer (English)**:

The first reaction is a Friedel-Crafts acylation. There are two rings and two carbonyl groups. One ring is chlorinated: chlorine has a deactivating effect on electrophilic aromatic substitution, so the non-chlorinated ring reacts. The two carbonyls differ in that the top one is (a) less hindered and (b) not conjugated, both of which contribute to its greater reactivity. There is also the question of regioselectivity in the way that the acylation occurs at the para position of the non-chlorinated ring. Aryl substituents are ortho,para directing, and steric factors favour the para over the ortho positions.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/ec7dfae6241ba68c378b031c01dad5bdee52ee8c26bce0bcb72586b7ed8597dc.jpg]]

In the second step, thiophenol gives the conjugate addition, rather than the direct addition product to either carbonyl group. Sulfur nucleophiles are soft, and this is typical behaviour for thiols.

**中文解析**：

**第一步：Friedel-Crafts酰基化**

需要解释三个层次的选择性：

1. **化学选择性（环的选择）**：两个芳环中，一个含Cl（失活基），另一个不含。Cl通过诱导效应降低环上电子密度→对亲电取代有失活作用。因此，未氯化的环更容易被亲电进攻。

2. **化学选择性（羰基的选择）**：两个酰氯羰基中：
   - 上方羰基：位阻较小 + 未与苯环共轭→活性更高
   - 下方羰基：位阻较大 + 与苯环共轭→活性较低
   - 因此上方羰基被选择性地活化为亲电体

3. **区域选择性（进攻位点）**：酰化发生在非氯化环的对位。芳基取代基是邻/对位定位基，位阻效应 favor 对位。

**第二步：硫酚的共轭加成**
- PhSH是软亲核试剂（S原子极化率大）
- 软亲核试剂优先进攻软亲电位点→共轭加成到C=C双键
- 而不是进攻硬亲电位点（C=O）→直接加成
- 这是硫醇的典型行为

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[区域选择性]] | 三个层次的选择性分析 | 直接 |
| Friedel-Crafts反应 | 酰基化的化学和区域选择性 | 直接 |
| [[逆合成分析]] | 复杂药物合成中的选择性控制策略 | 间接 |
| [[软硬酸碱理论]] | 软亲核试剂（硫醇）的共轭加成偏好 | 间接 |

## 解题思路

1. 读题定位：药物合成中的选择性问题——FC酰化 + 硫酚共轭加成
2. 关键转换：
   - 三个选择性层次：哪个环被进攻→哪个羰基是亲电体→环上哪个位点
   - 硫酚的软亲核性→共轭加成（非直接加成）
3. 验证：产物结构中酰基在非氯化环的对位，PhS在共轭加成位置

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 忽略Cl对环的失活效应 | 认为Cl是弱活化基 | Cl是弱失活基（诱导吸电子>共轭给电子） | 卤素的诱导和共轭效应哪个更强？ |
| 不分析两个羰基的反应性差异 | 认为两个酰氯等价 | 位阻和共轭状态不同→反应性不同 | 共轭如何影响酰氯的反应性？ |
| 认为硫酚进行直接加成 | 不理解软硬酸碱理论 | S是软亲核试剂→优先进攻软亲电位点（C=C共轭体系）| 为什么软亲核试剂倾向于共轭加成？ |