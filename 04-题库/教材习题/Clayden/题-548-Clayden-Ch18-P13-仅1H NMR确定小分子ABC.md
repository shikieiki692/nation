---
title: 题-548-Clayden-Ch18-P13-仅1H NMR确定小分子ABC
type: 题目
fidelity: 原书逐字
submodule: 波谱综合解析
exam_stage: 决赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch18-P13]
source: Clayden Organic Chemistry 2nd Ed. Chapter 18 Problem 13
cross_references: ["[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]", "[[题-415-Clayden-Ch13-P2-酐加MeMgBr产物用IR 13C 1H NMR区分]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]", "[[题-414-Clayden-Ch13-P1-五个化合物1H NMR信号和化学位移预测]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-548: 仅 ¹H NMR 确定小分子 A/B/C

## 题目

Identify the compounds produced in these reactions. Warning! Do not attempt to deduce the structures from the starting materials, but use the data. These molecules are so small that you can identify them from ¹H NMR alone.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/5f4d7774e681c2ce0e7a452b8641c9e3459c749be76a4b5a6a31942ba35c54e2.jpg]]

Data for A: C₄H₆; δH (ppm) 5.35 (2H, s) and 1.00 (4H, s)

Data for B: C₄H₆O; δH (ppm) 3.00 (2H, s), 0.90 (2H, d, J 3 Hz) and 0.80 (2H, d, J 3 Hz)

Data for C: C₄H₆O; δH (ppm) 3.02 (4H, t, J 5 Hz) and 1.00 (2H, quintet, J 5 Hz).

**Purpose of the problem**: Structure determination of reaction products by ¹H NMR alone.

## 参考答案

**Answer (English)**: The very small shifts of cyclopropane protons may have worried you but they often have shifts of less than 1 ppm. Compounds A and C are simple enough but B may have amazed you. It is unstable but can be isolated and the two three-membered rings sit at right angles to each other, so as in problem 12 the protons on each side of the cyclopropane ring are different.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/8cfb0dd65405060bb67595ca98090dc67225baf8256df1b66eb3df83589de0f3.jpg]]

**中文解析**：

关键解析步骤：

**化合物 A（C₄H₆）：**

1. **分子式**：C₄H₆，不饱和度 = 2
2. **¹H NMR**：
   - δ 5.35 (2H, s)：烯氢（=CH₂ 或 =CH-），单峰说明无邻位偶合
   - δ 1.00 (4H, s)：环丙烷氢（δ < 1 ppm 是环丙烷的典型特征）
3. **结论**：亚甲基环丙烷（methylenecyclopropane）— 环丙烷上连有 =CH₂

**化合物 B（C₄H₆O）：**

1. **分子式**：C₄H₆O，不饱和度 = 2（1 个 C=O + 1 个环）
2. **¹H NMR**：
   - δ 3.00 (2H, s)：CH₂ 接氧（环氧乙烷的 CH₂）
   - δ 0.90 (2H, d, J=3 Hz) + 0.80 (2H, d, J=3 Hz)：两组环丙烷氢，化学位移不同
3. **关键现象**：环丙烷上的 4 个氢分为两组 → 两个三元环相互垂直（spiro 结构），使环丙烷氢产生非对映异位性
4. **结论**：螺[2.2]戊烷-1-酮（spiro[2.2]pentan-1-one）— 不稳定的螺环酮

**化合物 C（C₄H₆O）：**

1. **分子式**：C₄H₆O，不饱和度 = 2
2. **¹H NMR**：
   - δ 3.02 (4H, t, J=5 Hz)：两个等价 CH₂ 接氧（环氧乙烷的 CH₂），t 峰说明与 CH₂ 偶合
   - δ 1.00 (2H, quintet, J=5 Hz)：CH₂，五重峰说明与两个 CH₂ 偶合（n+1 = 5 → 4 个邻位氢）
3. **结论**：环丁酮（cyclobutanone）的烯醇式或更准确地说是 1,2-环氧环丁烷类结构；实际上为环丁酮（cyclobutanone），其中 α-CH₂ 和 β-CH₂ 产生 t 和 quintet 偶合模式

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | 环丙烷质子的特征低场位移（< 1 ppm） | 直接 |
| [[波谱综合解析]] | 仅凭 ¹H NMR 偶合模式和化学位移确定小分子结构 | 直接 |
| 小环化合物 | 环丙烷、环丁烷、螺环化合物的 NMR 特征 | 直接 |
| [[立体化学]] | 螺环结构导致的非对映异位性 | 间接 |

## 解题思路

1. **读题定位**：三个小分子（C₄），不饱和度均为 2；题目明确提示"不要从起始物推断，只用数据"
2. **🔑 关键转换**：δ < 1 ppm 的信号 → 环丙烷氢（极特征！）；B 中两组不同的环丙烷氢 → 螺环使对称性降低；C 的 t + quintet 偶合模式 → 串联的 CH₂-CH₂-CH₂ 骨架
3. **验证**：A（亚甲基环丙烷）：2H 烯 + 4H 环丙烷 = C₄H₆；B（螺环酮）：两组不等价环丙烷氢 + 环氧 CH₂；C（环丁酮）：α-CH₂(t) + β-CH₂(quintet) 的偶合链完全吻合

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将 δ 1.00 以下的信号忽略或误判为杂质 | 不熟悉环丙烷的异常低场位移 | 环丙烷氢因环电流效应屏蔽，化学位移通常 < 1 ppm，是特征信号 | 环丙烷氢为什么比普通烷烃氢更屏蔽？ |
| 未识别 B 中的螺环非对映异位性 | 不理解空间效应对化学位移的影响 | 螺环使两个三元环相互垂直，环丙烷氢处于不同化学环境（面对 C=O 或背对 C=O） | 螺环化合物的对称性如何影响 NMR 信号数目？ |
| 将 C 的 quintet 误认为多重峰 | 未正确计算偶合氢数目 | quintet = n+1 = 5 → 有 4 个邻位氢，即 CH₂ 与两个 CH₂ 相连 | 如何从峰的分裂模式推断邻位氢的数目？ |