---
title: "题-WCh20.F03-trans-ML4X2分子轨道"
type: 题目
source: "无机化学第6版Weller Ch20 辅导性作业20.3"
source_file: "06-外部资料导入/无机化学Weller/无机化学第6版Welle19-21章.md"
subject: 无机和结构化学
year: 2023
difficulty: 5
knowledge_points: ["[[分子轨道理论]]", "[[八面体场]]"]
status: 已补全答案
tags: [化竞, 无机化学, Weller, 晶体场理论]
created: 2026-08-27
updated: 2026-08-30
subject_module: 结构化学
pack: 模块习题集
fidelity: 原书逐字
exam_stage: 初赛
used_in: "[[结构化学阶段测试卷]]"
---

# trans-ML4X2分子轨道

> **来源**：无机化学第6版（Weller等著，中文版）Ch20 辅导性作业20.3
> **难度**：⭐⭐⭐⭐⭐

## 题目

考虑到对称性降低时八面体轨道的分裂, 绘出 $trans-\left[ML_{4}X_{2}\right]$ 中 $\sigma$ 成键作用的对称性匹配线性组合和分子轨道能级图(假定配体 X 在光谱化学序列中的位置低于配体 L)。

## 参考答案

取 $z$ 轴为两个 X 配体所在轴，$trans-[ML_4X_2]$ 的对称性由 $O_h$ 降至 $D_{4h}$。四个面内 L 配体的 $\sigma$ 轨道构成 $a_{1g} + b_{1g} + e_u$ SALC，两个轴向 X 配体构成 $a_{1g} + a_{2u}$，合计为 $2a_{1g} + b_{1g} + a_{2u} + e_u$。

金属轨道按 $D_{4h}$ 归并：

- $s \rightarrow a_{1g} $，$p_z \rightarrow a_{2u} $，$p_x,p_y \rightarrow e_u $
- $d_{z^2} \rightarrow a_{1g} $，$d_{x^2-y^2} \rightarrow b_{1g} $
- $d_{xy} \rightarrow b_{2g} $，$d_{xz},d_{yz} \rightarrow e_g $

$\sigma$ 成键组合为：

$$a_{1g}(s) + a_{1g}(d_{z^2}) + b_{1g}(d_{x^2-y^2}) + a_{2u}(p_z) + e_u(p_x,p_y)$$

相应反键组合中以 $a_{1g}(d_{z^2})$ 和 $b_{1g}(d_{x^2-y^2})$ 为前线反键轨道。$d_{z^2}$ 只与轴向 X 及面内 $a_{1g}$ 组合重叠，$d_{x^2-y^2}$ 只与四个面内 L 的 $\sigma$ 轨道重叠。由于 X 的光谱化学位置低于 L，X 的 $\sigma$ 给予能力较弱，使轴向分量占优的 $a_{1g}(d_{z^2})$ 反键升幅小于 $b_{1g}(d_{x^2-y^2})$。

能级图自上而下应画为：

1. $\sigma^* \ b_{1g}(d_{x^2-y^2})$
2. $\sigma^* \ a_{1g}(d_{z^2})$
3. 非键或弱 $\pi$ 分裂的 $b_{2g}(d_{xy})$ 与 $e_g(d_{xz},d_{yz})$
4. 成键的 $e_u$、$a_{1g}$、$b_{1g}$、$a_{2u}$ 一组

若再考虑 $\pi$ 效应，原本八面体中简并的 $t_{2g}$ 还会进一步分裂，但题目只要求在 $\sigma$ 成键框架内画出上述 SALC 与相对能级。
