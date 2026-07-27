---
title: 题-420-Clayden-Ch13-P7-400 MHz 1H NMR烯炔酮归属
type: 题目
submodule: NMR谱学
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch13-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 13 Problem 7
cross_references: ["[[题-537-Clayden-Ch18-P2-Bullatenone结构A预测NMR并纠正]]", "[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]", "[[题-536-Clayden-Ch18-P1-C6H5FO的13C NMR C-F偶合结构确定]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]"]
module: 有机化学
status: 已填充
---
# 题-420: 400 MHz ¹H NMR烯炔酮归属

## 题目

Assign the 400 MHz ¹H NMR spectrum of this enynone as far as possible, justifying both chemical shifts and coupling patterns.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/385e95b78e445986b879c0f80c950c15e9fff8f5eec0423633b7ee345a986134.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/dea981c6b4856d752e37289e337da5a4bc4a637d256e4627d5a175dd0291211d.jpg]]

## 参考答案

**Answer (English)**: First measure the spectrum and list the data:

| δ /ppm | integration | multiplicity | coupling, J / Hz | comments |
|--------|-------------|-------------|------------------|----------|
| 5.6 | 1H | m | ? | alkene region |
| 5.05 | 1H | d with fine splitting | 16.3 | alkene region |
| 4.97 | 1H | d with fine splitting | 10.4 | alkene region |
| 2.58 | 2H | t with fine splitting | 6.5 | next to C=O or C=C |
| 2.47 | 2H | t with fine splitting | 6.5 | next to C=O or C=C |
| 2.32 | 2H | q with fine splitting | 6.5 | next to C=O or C=C |
| 2.21 | 2H | t with fine splitting | 6.5 | next to C=O or C=C |
| 1.95 | 1H | broad s | - | alkyne? |
| 1.77 | 2H | q | 6.5 | not next to anything |

Three protons in the alkene region, five CH₂ groups and one solitary proton on the alkyne. In the alkene region, the multiplet is H² which couples to the CH₂ at C3 and the other two alkene Hs. On C1, H¹ᵃ has a large trans coupling (16 Hz) to H² while H¹ᵇ has a smaller cis coupling (10 Hz).

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/d3d0e846be51e0e2aa000a93f48af0eaab9dc752dc99d6f62a32b611fd0e64cb.jpg]]

Of the five CH₂ groups, the quintet at small chemical shift must be C7. Those at C4, C6, and C8 have two neighbours and are basically triplets, but that at C3 couples to three protons and must be the quartet at 2.32 ppm.

**中文解析**：

关键要点：
1. **测量和列表**：首先精确测量化学位移和偶合常数，列出所有数据
2. **烯烃区域分析**：
   - δ 5.6 (1H, m)：H²，同时与C3的CH₂和另外两个烯H偶合
   - δ 5.05 (1H, d, J=16.3 Hz)：H¹ᵃ，反式偶合（大J值）
   - δ 4.97 (1H, d, J=10.4 Hz)：H¹ᵇ，顺式偶合（较小J值）
3. **五个CH₂的归属**：通过化学位移和多重性逐一归属——最远端的CH₂（C7）位移最小，C3的CH₂因邻近三个H呈四重峰

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | 复杂分子的¹H NMR系统归属 | 直接 |
| [[偶合常数]] | 反式（16 Hz）vs 顺式（10 Hz）烯H偶合 | 直接 |
| [[化学位移]] | 烯H、炔H、CH₂的化学位移差异 | 直接 |
| [[烯烃]] | 烯烃的偶合模式和化学位移特征 | 间接 |

## 解题思路

1. **读题定位**：题目要求归属烯炔酮的400 MHz ¹H NMR——需精确测量化学位移和偶合常数
2. **🔑 关键转换**：先识别烯烃区域的三个H→用J值区分顺/反式→再归属五个CH₂（通过多重性和化学位移排序）→炔H为宽单峰
3. **验证**：检查每个信号的积分、多重性和偶合常数是否与结构一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 混淆顺式和反式偶合常数 | 不熟悉烯H偶合常数范围 | 反式J ≈ 12–18 Hz，顺式J ≈ 6–12 Hz | 为什么反式偶合常数比顺式大？ |
| 忽略精细分裂 | 只看主要分裂不看精细结构 | 400 MHz下可见精细分裂，提供更多连接信息 | 如何从精细分裂推断邻近H的数目？ |
| 无法区分五个CH₂ | 没有系统地分析多重性 | 用n+1规则：三重峰=2个邻近H，四重峰=3个邻近H | C3的CH₂为什么是四重峰而不是三重峰？ |