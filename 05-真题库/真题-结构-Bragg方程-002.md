---
title: "Bragg方程应用-从XRD衍射角和波长计算晶面间距"
aliases: [X射线衍射, 晶面间距, 衍射角]
type: 真题
year: 2019
source: "中国化学奥林匹克(省级初赛)"
type_tag: "计算"
difficulty: 2
knowledge_points:
  - "Bragg方程"
tags:
  - 化竞
  - 真题
  - Bragg方程
  - XRD
  - 晶体结构
related_notes:
  - "[[专题-晶体结构计算]]"
updated: 2026-06-22
---

# Bragg方程应用-从XRD衍射角和波长计算晶面间距

## 题目

在某立方晶体的粉末 X 射线衍射（XRD）实验中，使用 $\mathrm{Cu\ K\alpha}$ 辐射（$\lambda = 154.18\ \mathrm{pm}$）。

(1) 测得 $(111)$ 晶面的一级衍射峰（$n = 1$）出现在 $2\theta = 38.20^\circ$。计算 $(111)$ 晶面的晶面间距 $d_{111}$。

(2) 立方晶系中 $d_{hkl} = \dfrac{a}{\sqrt{h^2 + k^2 + l^2}}$，求该晶体的晶胞参数 $a$。

(3) 同一晶体的 $(200)$ 晶面一级衍射峰应出现在 $2\theta$ 为多少？（$\sin 19.10^\circ = 0.3272$，$\sin 22.38^\circ = 0.3807$）


![[13-4-bragg-reflection.jpg]]

## 解析

### 分析

1. Bragg 方程：$n\lambda = 2d\sin\theta$，其中 $\theta = 2\theta / 2$ 为 Bragg 角（入射线与晶面的夹角）
2. 注意区分 $2\theta$（衍射仪读数）和 $\theta$（Bragg 角）
3. 同一晶体不同晶面的 $d$ 值不同但 $a$ 相同，可由已求得的 $a$ 反推其他衍射峰位置

### 解答

**(1) 计算 $d_{111}$**

Bragg 角：$\theta = \dfrac{2\theta}{2} = \dfrac{38.20^\circ}{2} = 19.10^\circ$

一级衍射（$n = 1$），代入 Bragg 方程：

$$d_{111} = \frac{n\lambda}{2\sin\theta} = \frac{1 \times 154.18}{2 \times \sin 19.10^\circ} = \frac{154.18}{2 \times 0.3272} = \frac{154.18}{0.6544} = 235.6\ \mathrm{pm}$$

**(2) 计算晶胞参数 $a$**

立方晶系：

$$d_{111} = \frac{a}{\sqrt{1^2 + 1^2 + 1^2}} = \frac{a}{\sqrt{3}}$$

$$a = d_{111} \times \sqrt{3} = 235.6 \times 1.732 = 408.1\ \mathrm{pm}$$

**(3) 预测 $(200)$ 的 $2\theta$**

$$d_{200} = \frac{a}{\sqrt{2^2 + 0^2 + 0^2}} = \frac{408.1}{2} = 204.05\ \mathrm{pm}$$

由 Bragg 方程（$n = 1$）：

$$\sin\theta_{200} = \frac{\lambda}{2d_{200}} = \frac{154.18}{2 \times 204.05} = \frac{154.18}{408.1} = 0.3778$$

$$\theta_{200} = \arcsin(0.3778) \approx 22.20^\circ$$

$$2\theta_{200} = 2 \times 22.20^\circ = 44.40^\circ$$

**验证**：$\sin 22.20^\circ \approx 0.3778$，与题给 $\sin 22.38^\circ = 0.3807$ 接近但略有差异（因 $a$ 的舍入误差）。

精确计算：若 $a = 408.1\ \mathrm{pm}$，$d_{200} = 204.05\ \mathrm{pm}$，$\sin\theta_{200} = 154.18/(2 \times 204.05) = 0.3778$，$\theta_{200} = 22.20^\circ$，$2\theta_{200} \approx 44.4^\circ$。

### 反思

Bragg 方程的计算要点：(1) 严格区分 $\theta$ 和 $2\theta$——这是最常见的错误来源；(2) 立方晶系 $d_{hkl}$ 公式中的分母是 $\sqrt{h^2+k^2+l^2}$，不是 $h^2+k^2+l^2$；(3) 粉末 XRD 的 $2\theta$ 是实测值，$\theta$ 才是代入公式的值。

## 答案

(1) $d_{111} = 235.6\ \mathrm{pm}$。

(2) $a = 408.1\ \mathrm{pm}$。

(3) $2\theta_{200} \approx 44.4^\circ$。

