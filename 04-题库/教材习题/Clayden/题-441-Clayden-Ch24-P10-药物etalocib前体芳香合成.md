---
title: 题-441-Clayden-Ch24-P10-药物etalocib前体芳香合成
type: 题目
fidelity: 原书逐字
submodule: 区域选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
question_type: [合成]
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[区域选择性]]"]
tags: [化竞, Clayden, 有机化学, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch24-P10]
source: Clayden Organic Chemistry 2nd Ed. Chapter 24 Problem 10
cross_references: ["[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-609-Clayden-Ch36-P2-Beckmann重排立体化学和机理]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-608-Clayden-Ch36-P1-原子编号追踪重排]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-441: 药物etalocib前体芳香合成

## 题目

**【中文】**该化合物是药物etalocib的合成前体。建议一种合成路线。提示：考虑使用亲核芳香取代。

**【原文】**
This compound is needed as a synthetic precursor to the drug etalocib. Suggest a synthesis. Hint: consider using nucleophilic aromatic substitution.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/be943425542323581bdee9446b83aab5ebcfba062331fd2ad6f3cd42cf2e1844.jpg]]

## 参考答案

**Answer (English)**:

There are lots of ortho relationships in this compound. Somehow we have to join the two aromatic rings together to make an ether. This can only really be done by nucleophilic aromatic substitution, so we need to look for an electron-withdrawing group to help us. The nitrile is in the right place, provided we have a leaving group (such as fluoride) ortho to it. So our last step can be as shown:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/19461c02b91807f33234ed44b9fbcc31b6309fc87a73f61c7e5b8d009c65ba96.jpg]]

To make the left hand ring we have to consider what methods are available to introduce the three substituents. It's always easier to add C-substituents than O-substituents, so we might consider how to alkylate the phenol below. The solution used was to use ortholithiation, making the dianion with two equivalents of BuLi and making use of the fact that two O substituents guide the BuLi in to deprotonate the position between them.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/6937d59aa9a0f0436a73a413bdaee86a84ee41264a14cc6ff43ce98c2aa3322e.jpg]]

**中文解析**：

该合成涉及两个关键策略：亲核芳香取代连接两环 + 邻位锂化引入取代基。

**逆合成分析——最后一步：两个芳环的连接**
- 醚键的形成需要C-O键断裂→亲核芳香取代（SNAr）
- SNAr需要强吸电子基活化邻位的离去基团
- CN是吸电子基，F是好的离去基（C-F键弱于C-Cl键在SNAr中的断裂）
- 最后一步：酚氧负离子进攻含CN和F的芳环→取代F→形成醚键

**左环的合成——邻位锂化**
- 三个取代基（OH, OMe, 烷基）需要被引入
- C-取代基比O-取代基更容易引入
- 关键洞察：两个含O取代基（OH和OMe）可以通过配位导向BuLi到它们之间的位点
- 用2当量BuLi→先形成O上的锂化物，再在两个O之间去质子化→芳基锂
- 芳基锂与亲电体（如CO₂或烷基卤）反应→引入C-取代基

**为什么不用Friedel-Crafts烷基化？**
- FC烷基化有重排问题（一级碳正离子→更稳定的碳正离子）
- FC酰基化+还原可以避免重排，但位阻和区域选择性可能有问题
- 邻位锂化可以精确控制取代位置

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[区域选择性]] | SNAr的位点选择；邻位锂化的位点选择 | 直接 |
| [[合成设计]] | 多步芳香化合物的逆合成分析 | 直接 |
| [[芳香亲电取代]] | 比较FC和邻位锂化的优劣 | 间接 |
| [[亲核芳香取代]] | CN活化邻位F的SNAr | 直接 |

## 解题思路

1. 读题定位：合成一个含两个芳环的醚类化合物，作为药物前体
2. 关键转换：
   - 逆合成：C(aryl)-O-C(aryl)键→SNAr（需要吸电子基+离去基）
   - 左环：邻位锂化（两个O导向）→精确引入取代基
   - 右环：含CN和F的芳环作为SNAr底物
3. 验证：SNAr产物中F被酚氧负离子取代；左环通过邻位锂化获得正确的取代模式

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 尝试用Williamson醚合成连接两环 | 两个底物都是芳基，SN2不可行 | 芳基C-O键不能通过SN2形成；需要SNAr或过渡金属催化 | Williamson醚合成的限制是什么？ |
| 不理解CN在SNAr中的作用 | 认为CN只是取代基 | CN是强吸电子基，通过诱导和共轭效应活化邻位的F离去 | 为什么CN在邻位比在间位更有效？ |
| 不理解2当量BuLi的必要性 | 认为是确保完全反应 | 先与OH去质子化（形成O-Li），再在两个O之间的位点去质子化（形成芳基Li） | 邻位锂化的配位导向机理是什么？ |
| 选择FC而非邻位锂化引入C取代基 | 不理解邻位锂化的精确性 | FC烷基化有重排和位移问题；邻位锂化可以精确控制位点 | 邻位锂化适用于什么类型的取代基引入？ |