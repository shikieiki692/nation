---
title: 题-414-Clayden-Ch13-P1-五个化合物1H NMR信号和化学位移预测
type: 题目
fidelity: 原书逐字
submodule: NMR谱学
exam_stage: 初赛
source_subject: 有机化学
difficulty: 2
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch13-P1]
source: Clayden Organic Chemistry 2nd Ed. Chapter 13 Problem 1
cross_references: ["[[题-536-Clayden-Ch18-P1-C6H5FO的13C NMR C-F偶合结构确定]]", "[[题-537-Clayden-Ch18-P2-Bullatenone结构A预测NMR并纠正]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]", "[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
source_grade: B
---
# 题-414: 五个化合物¹H NMR信号数与化学位移预测

## 题目

How many signals will there be in the ¹H NMR spectrum of each of these compounds? Estimate the chemical shifts of the signals.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/41a3fee36e3f166718e0354dc366caa9e2362270b639dded4e57f07fcd19dde4.jpg]]

## 参考答案

**Answer (English)**: Considerations of symmetry apply equally to ¹H and to ¹³C NMR. Different types of proton are marked with different letters:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/215d6dbaa81b119babf18e97f633031071b18f93cc6ac2e184039712294f1e00.jpg]]

Estimating the chemical shift in ¹H NMR requires modifying your experience of ¹³C NMR to the narrower range of proton shifts and considering that aromatic protons are in a distinct region from alkene protons:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/5cfe74016b02e20578e280cf12eba415d6997a037b59ad5a77036b116f5ce426.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/7ca86d6ea1d001c9635548349ef3327566fc2226816c83fba91c030d2b5210d1.jpg]]

**中文解析**：

关键要点：
1. **对称性分析**：判断等价质子是NMR信号数目的核心。对称操作（旋转轴、镜面）使等价质子产生同一信号
2. **化学位移预测**：¹H化学位移范围远窄于¹³C（通常0–12 ppm vs 0–220 ppm），需特别注意：
   - 连接两个氮原子的sp²碳上的H位移极大
   - 连接电正性硅的甲基H位移极小
   - 芳香H（6.5–8.5 ppm）与烯H（4.5–6.5 ppm）处于不同区域
3. **实际值与预测值**：若预测值与实际值接近已很好；若接近真实值则非常出色

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | 对称性决定等价质子数目和信号数 | 直接 |
| [[化学位移]] | 不同化学环境的H在不同区域出峰 | 直接 |
| [[1H NMR]] | ¹H NMR的信号数、积分和化学位移 | 直接 |
| [[对称性]] | 分子对称性与NMR信号等价性 | 间接 |

## 解题思路

1. **读题定位**：题目要求预测五个化合物的¹H NMR信号数和化学位移——核心是分析分子对称性和化学环境
2. **🔑 关键转换**：先画出每个分子的对称元素→找出等价H组→根据化学环境（邻近基团、杂原子、不饱和键）估算化学位移区域
3. **验证**：检查等价H组的数目是否与信号数一致，化学位移是否在合理范围内

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 忽略分子对称性 | 没有识别旋转轴或镜面 | 对称等价的H出现在同一信号，先找对称元素 | 这个分子有几个对称面？ |
| 混淆¹H和¹³C化学位移范围 | 直接套用¹³C的数值 | ¹H范围窄得多（0–12 ppm），芳香和烯区需区分 | 芳香H和烯H的化学位移范围分别是多少？ |
| 忽略杂原子对位移的影响 | 只考虑碳骨架 | 邻近O、N、卤素等杂原子会显著改变H的化学位移 | 连接两个N的sp²碳上的H为什么位移特别大？ |