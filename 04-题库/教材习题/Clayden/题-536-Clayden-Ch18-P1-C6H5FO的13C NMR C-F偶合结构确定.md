---
title: 题-536-Clayden-Ch18-P1-C6H5FO的13C NMR C-F偶合结构确定
type: 题目
submodule: 波谱综合解析
exam_stage: 决赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch18-P1]
source: Clayden Organic Chemistry 2nd Ed. Chapter 18 Problem 1
cross_references: ["[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]", "[[题-415-Clayden-Ch13-P2-酐加MeMgBr产物用IR 13C 1H NMR区分]]", "[[题-414-Clayden-Ch13-P1-五个化合物1H NMR信号和化学位移预测]]"]
module: 有机化学
status: 已填充
---
# 题-536: C₆H₅FO 的 ¹³C NMR C-F 偶合结构确定

## 题目

A compound C₆H₅FO has a broad peak in the infrared at about 3100–3400 cm⁻¹ and the following signals in its (proton decoupled) ¹³C NMR spectrum. Suggest a structure for the compound and interpret the spectra.

δC (ppm) 157.4 (d, J 229 Hz), 151.2 (s), 116.3 (d, J 7.5 Hz), and 116.0 (d, J 23.2 Hz).

**Purpose of the problem**: A reminder that coupling may occur in ¹³C NMR spectra too and can be useful.

## 参考答案

**Answer (English)**: All the signals are in the sp² region and two (at >150 ppm) are of carbons attached to electronegative elements. As the formula contains C₆, a benzene ring is strongly suggested. The IR spectrum tells us that we have an OH group, so the compound is one of three possible structures:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/b16e5fa62fac806b5f39d172de0f359bf3c786955d0a2fc75d0c90302b29eac3.jpg]]

The symmetry of the spectrum suggests the para disubstituted compound as there are only four types of carbon atom. We can assign the spectrum by noting that the very large coupling (J 229) must be a ²J_CF and the zero coupling must be the carbon furthest from F, i.e. the para carbon. The intermediate couplings are for the other two carbons and the CF coupling diminishes with distance.

116.3 (d, J 7.5 Hz) → 157.4 (d, J 229 Hz)

151.2 (s) HO — 116.0 (d, J 23.2 Hz)

**中文解析**：

关键解析步骤：

1. **IR分析**：3100–3400 cm⁻¹ 宽峰 → 确认含 OH 基团
2. **分子式分析**：C₆H₅FO，不饱和度 = 4 → 强烈暗示苯环
3. **¹³C NMR 分析**：
   - 所有信号均在 sp² 区域（>100 ppm），证实苯环
   - 仅出现4种碳信号 → 对位二取代苯（具有对称性）
   - δ 157.4 (d, J = 229 Hz)：巨大的 F-C 偶合常数 → 这是与 F 直接相连的碳（¹J_CF ≈ 250 Hz 量级）
   - δ 151.2 (s)：无偶合 → 距 F 最远的碳（对位碳），与 OH 相连
   - δ 116.0 (d, J = 23.2 Hz)：中等偶合 → ²J_CF（F的邻位碳）
   - δ 116.3 (d, J = 7.5 Hz)：小偶合 → ³J_CF（F的间位碳）
4. **结论**：结构为 **4-氟苯酚（对氟苯酚）**

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | ¹³C NMR 中 F-C 偶合常数的大小与距离关系 | 直接 |
| [[波谱分析]] | 综合 IR 和 NMR 数据确定分子结构 | 直接 |
| [[13C NMR]] | ¹³C 化学位移区域判断杂化类型 | 直接 |
| [[氟代芳烃]] | C-F 偶合常数随键数增加而递减的规律 | 间接 |

## 解题思路

1. **读题定位**：分子式 C₆H₅FO + IR 宽峰(3100–3400) → 含 OH 的芳香化合物；¹³C NMR 仅4组信号 → 高对称性（对位取代）
2. **🔑 关键转换**：利用 ¹³C NMR 中 F-C 偶合常数判断各碳的位置——J 值越大，碳与 F 的距离越近；无偶合的碳在对位
3. **验证**：对氟苯酚具有 C₂v 对称性，恰好产生4种等价碳，与实验数据完全吻合

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将 J = 229 Hz 误认为 ¹J_CH | 未注意是 C-F 偶合 | C-H 偶合一般 ≤ 250 Hz，但在去偶谱中不会出现；J = 229 Hz 是典型的 ²J_CF | 为什么质子去偶后还能看到 d 峰？ |
| 误判为邻位或间位取代 | 未利用碳信号数量判断对称性 | 4组信号 = 4种碳 → 必须是对称的对位取代；邻位/间位各会产生6种碳 | 邻氟苯酚应出现几组 ¹³C 信号？ |
| 忽略 IR 3100–3400 cm⁻¹ 信息 | 只关注 NMR 数据 | 该宽峰明确指示 OH 基团，排除了 C₆H₅F（氟苯）的可能性 | 如果 IR 没有这个峰，可能是什么结构？ |