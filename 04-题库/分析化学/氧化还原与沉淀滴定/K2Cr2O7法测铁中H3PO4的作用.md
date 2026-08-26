---
title: "K2Cr2O7法测铁中H3PO4的作用"
aliases: ["题-分析-04", "题-0658"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 拓展
source: "专题页提炼"
source_author: "资料提炼综合"
module: "氧化还原与沉淀滴定"
subject: 分析化学
syllabus_codes: ["57"]
knowledge_points: ["[[氧化还原滴定]]", "掩蔽", "[[Nernst方程]]"]
tags: [化竞, 题目]
updated: 2026-06-06
status: 已填充
exam_stage: 初赛
subject_module: 元素与分析
pack: 模块习题集
submodule: 化学基础与计量
---
# K₂Cr₂O₇ 法测铁中 H₃PO₄ 的双重作用

## 题目

用 $\mathrm{K_2Cr_2O_7}$ 标准溶液滴定 $\mathrm{Fe^{2+}}$ 时，常加入 $\mathrm{H_3PO_4}$。问 $\mathrm{H_3PO_4}$ 在该滴定体系中的**双重作用**是什么？分别说明原理。

---

## 参考答案

**作用一：掩蔽 Fe³⁺，消除颜色干扰**

滴定反应为：
$$\mathrm{Cr_2O_7^{2-} + 6Fe^{2+} + 14H^+ \longrightarrow 2Cr^{3+} + 6Fe^{3+} + 7H_2O}$$
生成的 $\mathrm{Fe^{3+}}$ 在溶液中呈黄色（形成氯合铁配合物 $\mathrm{[FeCl_4]^-}$ 等），会干扰指示剂（常用二苯胺磺酸钠）终点的颜色观察——$\mathrm{Fe^{3+}}$ 的黄色与指示剂变色（无色 → 紫红色）叠加，使终点判别困难。加入 $\mathrm{H_3PO_4}$ 后，$\mathrm{PO_4^{3-}}$ 与 $\mathrm{Fe^{3+}}$ 形成无色的 $[\mathrm{Fe(HPO_4)}]^+$ 络合物：
$$\mathrm{Fe^{3+} + HPO_4^{2-} \longrightarrow [Fe(HPO_4)]^+}$$
从而消除 $\mathrm{Fe^{3+}}$ 的黄色背景，使终点变色更易观察。

**作用二：降低 $\varphi(\mathrm{Fe^{3+}/Fe^{2+}})$，扩大滴定突跃**

根据 Nernst 方程：
$$\varphi(\mathrm{Fe^{3+}/Fe^{2+}}) = \varphi^{\ominus}(\mathrm{Fe^{3+}/Fe^{2+}}) + 0.0592\lg\frac{[\mathrm{Fe^{3+}}]}{[\mathrm{Fe^{2+}}]}\quad(25^{\circ}\mathrm{C})$$
加入 $\mathrm{H_3PO_4}$ 后，$\mathrm{Fe^{3+}}$ 被络合，游离 $[\mathrm{Fe^{3+}}]$ 大幅降低，使得条件电极电位 $\varphi^{\ominus'}(\mathrm{Fe^{3+}/Fe^{2+}})$ 降至约 $0.51\,\mathrm{V}$（原 $\varphi^{\ominus} = 0.771\,\mathrm{V}$），与 $\varphi^{\ominus'}(\mathrm{Cr_2O_7^{2-}/Cr^{3+}}) \approx 1.00\,\mathrm{V}$（在 $1\,\mathrm{mol\cdot L^{-1}}\,\mathrm{H_2SO_4}$ 中）的差距增大，使滴定突跃范围更宽、电位突跃更明显，指示剂变色更敏锐。

> **方法要点**：氧化还原滴定中加入络合剂（如 $\mathrm{H_3PO_4}$、$\mathrm{HF}$、$\mathrm{EDTA}$ 等）调节条件电极电位是常用的技术手段，可同时实现消除干扰和改善突跃两个目的。

---

## 知识点映射

- [[氧化还原滴定]]
- 掩蔽
- [[Nernst方程]]
