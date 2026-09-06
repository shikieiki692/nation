---
title: 题-410-化学能力测试-Ch7B-5-Fe配位竞争pH计算
type: 题目
aliases:
  - Fe SCN F 竞争配位
source_subject: 化学竞赛能力测试·第7章B卷
submodule: Fe³⁺/SCN⁻/F⁻ 双配位竞争 + HF 酸效应
subject_module: 元素与分析
exam_stage: 初赛
question_type:
  - 计算
difficulty: 5
teaching_level: 竞赛
fidelity: 原书逐字
knowledge_points:
  - "[[配合物]]"
  - "[[酸碱平衡]]"
  - "[[化学平衡]]"
concepts:
  - "Fe³⁺+SCN⁻⇌FeSCN²⁺ K₁=10³；Fe³⁺+F⁻⇌FeF²⁺ K₂=10⁵"
  - "HF Ka=10⁻³·²；[F⁻]=Ka/([H⁺]+Ka)·c_F⁻"
  - "[H⁺]=10⁻³·² → pH=3.2（刚出现橙红）"
pack: 模块习题集
tags:
  - 化竞
  - 教材习题
  - 化学能力测试
  - 第7章
created: 2026-09-03
updated: 2026-09-03
source: 化学竞赛能力测试·第7章 溶液中的平衡·B卷第5题
source_file: "[[化学竞赛教程/（已压缩）化学竞赛能力测试]]"
status: 已填充
source_category: 竞赛导向·竞赛教辅
---

# Fe³⁺/SCN⁻/F⁻ 竞争配位 pH

> **来源**：化学竞赛能力测试·第7章·B卷第5题（10 分）

1.0×10⁻³ M Fe³⁺、0.10 M SCN⁻、0.20 M F⁻ 的 1.0 L 混合液，滴 HCl 至刚现橙红色，[FeSCN²⁺]=1×10⁻⁵ M。求此时溶液 pH。

已知：Fe³⁺+SCN⁻⇌FeSCN²⁺ K₁=10³；HF Ka=10⁻³·²；Fe³⁺+F⁻⇌FeF²⁺ K₂=10⁵。

<details>
<summary>📖 查看答案与解析</summary>

SCN⁻ 强酸根不受 pH 影响，但 F⁻ 受 HF 酸效应：

$$[\mathrm{F^-}] = \frac{K_a}{[\mathrm H^+] + K_a}\times c_{\mathrm{F^-}}$$

Fe³⁺ 同时满足两配位平衡：

$$[\mathrm{Fe^{3+}}] = \frac{[\mathrm{FeSCN^{2+}}]}{K_1[\mathrm{SCN^-}]} = \frac{1.0\times 10^{-5}}{10^3\times 0.10} = 10^{-7}\ \mathrm M$$

$$[\mathrm{FeF^{2+}}] \approx c_{\mathrm{Fe^{3+}}} - [\mathrm{FeSCN^{2+}}] \approx 1.0\times 10^{-3}\ \mathrm M$$

由 Fe³⁺ 双平衡联立（FeSCN²⁺ 与 FeF²⁺ 共享 Fe³⁺）：

$$\frac{[\mathrm{FeSCN^{2+}}]}{K_1[\mathrm{SCN^-}]} = \frac{[\mathrm{FeF^{2+}}]([\mathrm H^+] + K_a)}{K_2\cdot K_a\cdot c_{\mathrm{F^-}}}$$

$$[\mathrm H^+] = \frac{[\mathrm{FeSCN^{2+}}]}{[\mathrm{Fe^{3+}}][\mathrm{SCN^-}]}\cdot\frac{K_2K_ac_{\mathrm{F^-}}}{K_1} - K_a = 10^{-3.2}$$

**pH = 3.2**

</details>

<!-- 校勘注: ①解算核心：双配位平衡共享 [Fe³⁺]，[F⁻] 用酸效应分布系数表达，反解 [H⁺]；②[FeSCN²⁺]=1e-5 很小 → [SCN⁻]≈0.10（HSCN 强酸全电离）、[FeF²⁺]≈1e-3 ✓；③[H⁺]=Ka 巧合使 HF 半解离。 -->

## 知识点映射

| 知识点 | 本题应用 |
|---|---|
| [[配合物]] | 双配位竞争平衡 |
| [[酸碱平衡]] | F⁻ 酸效应 |
| [[化学平衡]] | 共享 Fe³⁺ 联立 |