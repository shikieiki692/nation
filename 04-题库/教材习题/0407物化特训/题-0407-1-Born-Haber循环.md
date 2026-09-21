---
title: 题-0407-1-Born-Haber循环
type: 题目
submodule: 化学热力学
exam_stage: 初赛
source_subject: 物理化学
question_type: [计算]
difficulty: 3
teaching_level: 巩固
fidelity: 原书逐字
knowledge_points: ["[[热力学循环]]", "[[电子亲合能]]", "[[焓变计算]]"]
tags: [化竞, 0407物化特训, Born-Haber循环, 晶格能, 水溶液计算特训]
created: 2026-09-21
updated: 2026-09-21
source: 0407物化水溶液平衡计算大题特训 第1题（15分）
source_file: "[[bdwp资源/0407物化水溶液平衡计算大题特训]]"
module: 化学热力学
subject_module: 化学原理
pack: 章节练习
status: 已填充
source_category: 竞赛导向·竞赛教辅
---

# 题-0407-1 Born-Haber 循环（15 分）

## 题目

已知 NaCl 的热化学数据（298 K）：

- Na(s) → Na(g)　ΔH_sub(Na) = 108 kJ·mol⁻¹
- Na(g) → Na⁺(g) + e⁻　I₁(Na) = 496 kJ·mol⁻¹
- ½Cl₂(g) → Cl(g)　½D(Cl₂) = 121 kJ·mol⁻¹
- Na⁺(g) + Cl⁻(g) → NaCl(s)　U(NaCl) = −787 kJ·mol⁻¹
- Na(s) + ½Cl₂(g) → NaCl(s)　ΔfH°(NaCl) = −411 kJ·mol⁻¹

1-1 计算氯原子的电子亲和能 EA(Cl)，并用 eV 表示。（8 分）

1-2 利用 1-1 中得到的 EA(Cl) 计算 KCl 的晶格能 U(KCl)。规定晶格能为 K⁺(g)+Cl⁻(g) → KCl(s) 对应的焓变，放热为负。另有 ΔH_sub(K) = 89 kJ·mol⁻¹，I₁(K) = 418 kJ·mol⁻¹，ΔfH°(KCl) = −437 kJ·mol⁻¹，1 eV = 96.485 kJ·mol⁻¹。（4 分）

1-3 比较 NaCl 和 KCl 晶格能绝对值大小，并从离子半径角度简要解释原因。（3 分）

## 解答

**1-1** 由 Born-Haber 循环：

ΔfH°(NaCl) = ΔH_sub(Na) + I₁(Na) + ½D(Cl₂) − EA(Cl) + U(NaCl)

−411 = 108 + 496 + 121 − EA − 787

EA = 349 kJ·mol⁻¹ = 349 / 96.485 = 3.62 eV

**1-2** ΔfH°(KCl) = ΔH_sub(K) + I₁(K) + ½D(Cl₂) − EA(Cl) + U(KCl)

U(KCl) = −437 − (89 + 418 + 121 − 349) = −716 kJ·mol⁻¹

**1-3** |U(NaCl)| > |U(KCl)|。Na⁺ 半径小于 K⁺，Cl⁻ 相同，Na⁺ 与 Cl⁻ 离子间距更小，静电吸引更强，晶格形成时放热更多，晶格能绝对值更大。（比较 1 分，解释 2 分）

## 解析要点

- 晶格能符号约定（放热为负）是易错点；EA 作为"放热项"在循环中取负号；
- 单位换算 eV↔kJ·mol⁻¹ 常用 96.485。
