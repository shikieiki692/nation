---
title: "题-128-ABOC-Ch4-4.13.1-Cannizzaro反应的同位素示踪与动力学"
type: 题目
fidelity: 原书逐字
submodule: Ch.4
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["34"]
knowledge_points: ["[[Cannizzaro反应]]", "[[醛酮化学]]", "[[同位素示踪]]", "[[反应动力学]]"]
tags: [化竞, ABOC, 有机化学]
updated: 2026-09-24
source_file: "[[07-资料提炼/书籍提炼/提炼-ABOC-第4章-取代与消除]]"
aliases: [ABOC-Ch4-4.13.1]
source: ABOC 第4章 自学练习（ARX's Basic Organic Chemistry 第3版）
module: 基础要求-有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 竞赛导向·竞赛教材
source_grade: B
source_tier: 4
source_norm: "ABOC 有机化学"
---
# 题-128：Cannizzaro 反应的同位素示踪与动力学

> **来源**：ABOC 第4章 自学练习 4.13.1
> **难度**：⭐⭐⭐
> **教学层级**：巩固

---

## 题目

Cannizzaro（康尼查罗）反应是醛在强碱浓溶液中发生的歧化反应。以苯甲醛为底物，根据所给条件和信息，回答以下问题：

1. 当反应在重水 $\\mathrm{D_2O}$ 中进行，产物苯甲醇是否含有氘？
2. 当反应在 $\\mathrm{H_2^{18}O}$ 中进行，画出含 $^{18}\\mathrm{O}$ 产物的结构简式。
3. 动力学研究发现，该反应的速率方程可以表达为

$$
v = k_a[\\mathrm{PhCHO}]^2[\\mathrm{OH^-}] + k_b[\\mathrm{PhCHO}]^2[\\mathrm{OH^-}]^2
$$

解释此方程中出现这两项的原因。

---

## 参考答案

1. **含有氘，但不形成新的 C-D 键。** 负氢转移后生成的 $\\mathrm{PhCH_2O^-}$ 会从 $\\mathrm{D_2O}$ 获取 D，得到 $\\mathrm{PhCH_2OD}$；苄位的两个氢仍来自苯甲醛/负氢转移。
2. 含 $^{18}\\mathrm{O}$ 的产物可写为 $\\mathrm{PhCO^{18}O^-}$（最直接产物）。由于 $\\mathrm{OH^-}$ 对羰基的可逆加成使氧原子能够交换，苯甲酸根的两个氧以及苯甲醇的氧均可能被 $^{18}\\mathrm{O}$ 标记。
3. 两条并行的预平衡路径分别形成单负离子中间体 $\\mathrm{T_1}$ 和双负离子中间体 $\\mathrm{T_2}$：

$$
[\\mathrm{T_1}] = K_1[\\mathrm{PhCHO}][\\mathrm{OH^-}],\\qquad
[\\mathrm{T_2}] = K_2[\\mathrm{PhCHO}][\\mathrm{OH^-}]^2
$$

负氢迁移为决速步，且与另一分子 $\\mathrm{PhCHO}$ 反应，故两条路径分别给出对 $\\mathrm{PhCHO}$ 二级、对 $\\mathrm{OH^-}$ 一级和二级的两项速率贡献。

---

## 解题思路

1. 区分负氢转移与质子交换：$\\mathrm{H^-}$ 决定苄位碳上的氢来源，$\\mathrm{D^+}$ 只进入羟基。
2. $^{18}\\mathrm{O}$ 的去向取决于亲核加成是否可逆；至少溶剂氧可进入羧酸根的羰基位置。
3. 将实验速率方程拆成两个快平衡形成的中间体浓度，再分别乘以共同决速步中的另一分子苯甲醛浓度。

> 来源：ABOC 第4章自学练习 4.13.1；题干按原书恢复，公式排版规范化。

---

## 知识点

- Cannizzaro 反应的负氢转移与后续质子交换不是同一步。
- 羰基与 $\\mathrm{OH^-}$ 的可逆加成可导致氧同位素交换。
- 实验速率方程对应两条形成单负离子/双负离子中间体的并行路径。

---

## 相关题目

- [[04-题库/真题/省预赛/讲评重组/真题-有机-Cannizzaro-001]]
- [[题-062-ABOC-Ch1-1.1.1-离去基判断]]
- [[题-063-ABOC-Ch1-1.2.2-1-S-C反键轨道与端基效应]]
- [[题-064-ABOC-Ch1-1.3.1-3-金刚烷合成（碳正离子重排）]]
