---
title: 题-583-Clayden-Ch31-P14-偶合常数大小用于结构确定
type: 题目
submodule: 立体电子效应
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学, 立体化学]
updated: 2026-07-25
aliases: [Clayden-Ch31-P14]
source: Clayden Organic Chemistry 2nd Ed. Chapter 31 Problem 14
cross_references: ["[[题-551-Clayden-Ch29-P2-烷基吡啶LHMDS侧链延伸]]", "[[题-550-Clayden-Ch29-P1-杂环上亲电亲核取代产物预测]]"]
module: 有机化学
status: 已填充
---
# 题-583: 偶合常数大小用于结构确定

## 题目

Treatment with base of the two compounds shown here gives an unknown compound with the spectra given below. What is its structure?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/203bd75592dcc5c078aeaf8ce527455771d758cbdc215138ba8b5c390afed613.jpg]]

m/z: 241 (M⁺, 60%), 90 (100%), 89 (62%)

$\delta_{H}$ (ppm in CDCl₃) 3.89 (1H, d, J 3 Hz), 4.01 (1H, d, J 3 Hz), 7.31 (5H, s), 7.54 (2H, d, J 10 Hz) and 8.29 (2H, d, J 10 Hz)

$\delta_{C}$ (ppm in CDCl₃) 62, 64, 122, 125, 126, 127, 130, 136, and 148 (the last three are weak).

**原文题目**：Determine the structure of the unknown compound from mass spec and NMR data.

## 参考答案

**Answer (English)**: The compound is an epoxide: the coupling constants around the three-membered ring are small (3 Hz: contrast 10 Hz on the benzene ring) because of ring size and the oxygen atom. All the Hs on the Ph ring happen to come at the same chemical shift. Those on the nitrated ring are at lower field and separated by the nitro group.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/c2f32b02025e54d9e889676498916c9101749e92a8c78fbf8c638fecf87404f0.jpg]]

**中文解析**：

关键步骤：
1. **质谱分析**：M⁺=241→分子量241；基峰90和89提示碎片模式
2. **¹H NMR分析**：
   - 3.89和4.01 (d, J=3 Hz each)：两个氢，小偶合→三元环（环氧乙烷）上的两个氢
   - 7.31 (5H, s)：单取代苯环（5个等价氢）
   - 7.54和8.29 (d, J=10 Hz each)：对位取代苯环（AA'BB'系统），硝基使邻位氢去屏蔽
3. **¹³C NMR分析**：
   - 62和64 ppm：环氧乙烷碳（小环碳在高场）
   - 122-148 ppm：芳香碳
4. **结构确定**：环氧乙烷连接两个苯环——一个是苯基，一个是对硝基苯基
5. **偶合常数对比**：
   - 环氧乙烷：J=3 Hz（三元环+氧原子导致小偶合）
   - 苯环：J=10 Hz（正常芳香偶合）

> **注意**：偶合常数的大小直接反映结构——三元环的J很小(3 Hz)，六元环芳烃的J正常(10 Hz)，这种对比是解题的关键。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | 环氧乙烷小偶合vs芳烃正常偶合的对比 | 直接 |
| [[偶合常数]] | 三元环偶合常数(~3 Hz)与六元环(~10 Hz)的显著差异 | 直接 |
| [[立体化学]] | 环氧乙烷的顺式取代模式 | 间接 |

## 解题思路

1. **读题定位**：碱处理两个底物得到未知物，需要质谱+NMR确定结构
2. **🔑 关键转换**：M⁺=241→NMR显示两个苯环+两个小偶合氢→小偶合(3 Hz)=三元环环氧乙烷→硝基苯+苯基
3. **验证**：检查分子量是否匹配，所有NMR信号归属是否合理，¹³C信号数是否与结构一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将J=3 Hz误认为是其他基团 | 不了解三元环偶合特征 | 三元环+氧原子→极小偶合(3 Hz)，与芳烃(10 Hz)形成鲜明对比 | 为什么三元环的偶合常数特别小？ |
| 忽略质谱碎片信息 | 只关注NMR | m/z=90和89提示硝基苯基碎片 | 如何从质谱碎片推断结构？ |
| 误判AA'BB'系统 | 对芳烃偶合不熟悉 | 对位取代苯环的AA'BB'系统表现为两组双峰(J=10 Hz) | AA'BB'和AB系统有何区别？ |