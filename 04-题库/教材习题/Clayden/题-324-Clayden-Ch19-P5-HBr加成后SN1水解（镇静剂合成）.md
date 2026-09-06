---
title: 题-324-Clayden-Ch19-P5-HBr加成后SN1水解（镇静剂合成）
type: 题目
fidelity: 原书逐字
submodule: 烯烃的亲电加成
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
question_type: [机理]
teaching_level: 拓展
syllabus_codes: ["2.3", "3.2"]
knowledge_points: ["[[亲电加成]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch19-P5]
source: Clayden Organic Chemistry 2nd Ed. Chapter 19 Problem 5
cross_references: ["[[题-320-Clayden-Ch19-P1-HCl对三个烯烃加成方向]]", "[[题-327-Clayden-Ch19-P8-烯烃区域立体选择性转化试剂选择]]", "[[题-401-Clayden-Ch22-P11-NMR揭示共轭加成过程]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
source_grade: B
---
# 题-324: HBr加成后SN1水解（镇静剂合成）

## 题目

Propose a mechanism for the following two-step sequence in a tranquilizer synthesis:

Step 1: An alkene (e.g., 2-methylbut-2-ene) reacts with HBr → alkyl bromide
Step 2: The alkyl bromide is heated in water → alcohol

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/4b5ff85f540ec5b5a31a8d7dc836b44714a07a6eac0ad8d97f3c16bfe9846fd5.jpg]]

**原文题目**：

为镇静剂合成中的以下两步反应提出机理：

步骤 1：烯烃（如 2-甲基-2-丁烯）与 HBr 反应 → 烷基溴化物
步骤 2：烷基溴化物在水中加热 → 醇

## 参考答案

**Answer (English)**:

**Step 1 — HBr electrophilic addition**:
- H⁺ protonates the double bond of 2-methylbut-2-ene at C-2 (less substituted terminal = Markovnikov), generating the **tertiary carbocation** at C-2 (CH₃C⁺(CH₃)CH₂CH₃).
- Br⁻ captures the tertiary carbocation to give 2-bromo-2-methylbutane (tertiary alkyl bromide).

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/d4e5012f2ff192d3b41900379ff41a8dc186c226042a73909197eed69b8b3231.jpg]]

**Step 2 — SN1 hydrolysis**:
- Water (nucleophile) attacks the tertiary carbon of the alkyl bromide. Since tertiary substrates are too sterically hindered for SN2, the C-Br bond dissociates first to form the tertiary carbocation (SN1 rate-determining step).
- Water captures the carbocation → protonated alcohol (oxonium ion).
- Deprotonation by water gives the final alcohol: 2-methylbutan-2-ol.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/2e008e5d459e27af6134112982cf8782de9f639143e3ca049da111da063d9e0e.jpg]]

**中文解析**：

**步骤 1（HBr 亲电加成）**：
- H⁺ 作为亲电试剂进攻 2-甲基-2-丁烯的 C-3（含氢较少的末端碳=反 Markovnikov 方向质子化），在 C-2 上形成**叔碳阳离子** CH₃C⁺(CH₃)CH₂CH₃。这是最稳定的碳阳离子中间体（三级）。
- Br⁻ 捕获叔碳阳离子，得到 2-溴-2-甲基丁烷（叔溴代烷）。

**步骤 2（SN1 水解）**：
- 叔碳底物空间位阻大，无法进行 SN2。C-Br 键先异裂生成叔碳阳离子（SN1 决速步）。
- 水分子捕获碳阳离子 → 氧鎓离子。
- 另一水分子去质子化 → 2-甲基丁-2-醇。

**总体效果**：烯烃 → Markovnikov 溴化 → SN1 水解 → Markovnikov 醇。等价于酸催化水合，但通过两步实现，避免了直接酸催化水合可能产生的副反应。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[亲电加成]] | HBr对烯烃的Markovnikov加成→叔碳阳离子→Br⁻捕获 | 直接 |
| SN1反应 | 叔溴代烷的SN1水解：碳阳离子形成→水捕获→去质子化 | 直接 |
| [[消除反应]] | 叔碳阳离子可能的E1竞争副产物 | 间接 |

## 解题思路

1. **读题定位**：两步序列——HBr加成（亲电加成）→ 水解（SN1取代），中间体均为叔碳阳离子
2. **🔑 关键转换**：烯烃质子化 → 叔碳阳离子 → Br⁻捕获 → 水解时Br⁻离去 → 再次叔碳阳离子 → H₂O捕获 → 去质子化
3. **验证**：两步都通过叔碳阳离子；最终产物是Markovnikov醇；水解条件温和不引起消除

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 步骤2写成SN2机理 | 忽视了叔碳底物完全不支持SN2 | 叔碳空间位阻太大，SN2极慢，只能走SN1 | 什么级别的碳底物适合SN2？ |
| 忘记水解步骤中的去质子化 | 水捕获碳阳离子后得到的是氧鎓离子 | 需要另一个水分子夺去质子才能得到中性醇 | 水解为什么需要加热？ |
| 认为两步中碳阳离子不同 | 两步都形成相同的叔碳阳离子 | HBr加成和水解都经过同一个叔碳阳离子中间体 | 为什么叔碳阳离子如此稳定？ |