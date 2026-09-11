---
title: Maxwell关系
aliases: ["Maxwell关系式", "麦克斯韦关系", "麦克斯韦关系式", "热力学关系式"]
type: 工具卡
subject: 数学工具
module: 数学工具
tags: [化竞, 数学工具, Maxwell关系, 热力学, 状态函数, 混合偏导]
related: [偏导数与全微分]
prerequisite: [偏导数与全微分]
difficulty: 5
importance: 4
status: 已填充
stage: published
sources: ["Mortimer《Mathematics for Physical Chemistry》§7.6", "Atkins《Physical Chemistry》MB2 / 第3章"]
source_type: [教材]
syllabus_stage: []
syllabus_code: []
syllabus_module: []
syllabus_note: "数学工具层——中国化学奥林匹克考纲无对应条目，故 syllabus_* 留空"
handout_ref: "[[数学工具-第5讲-偏导与全微分]]"
template_version: v1.0
updated: 2026-09-11
has_images: false
image_count: 0
---

# Maxwell关系

## 一句话

四条 Maxwell 关系**不用背口诀**——它们全是「混合偏导相等」作用在四个热力学势的全微分上的结果，可以 30 秒内现推。

## 出发点：四个全微分

```
dU = T dS − p dV
dH = T dS + V dp
dA = −S dT − p dV
dG = −S dT + V dp
```

对 $df = Mdx+Ndy$ 形式，混合偏导相等 $\dfrac{\partial M}{\partial y}=\dfrac{\partial N}{\partial x}$ 直接给出关系式。

## 四条关系

```
(∂T/∂V)_S = −(∂p/∂S)_V        （由 dU）
(∂T/∂p)_S =  (∂V/∂S)_p        （由 dH）
(∂S/∂V)_T =  (∂p/∂T)_V        （由 dA）
(∂S/∂p)_T = −(∂V/∂T)_p        （由 dG）
```

**现推示范**（由 $dG=-S\,dT+V\,dp$）：$M=-S$、$x=T$、$N=V$、$y=p$，故

$-\left(\dfrac{\partial S}{\partial p}\right)_T = \left(\dfrac{\partial V}{\partial T}\right)_p \quad\Longrightarrow\quad \left(\dfrac{\partial S}{\partial p}\right)_T = -\left(\dfrac{\partial V}{\partial T}\right)_p$

## 怎么用

Maxwell 关系的价值在于**把不可测的量换成可测的量**：

- $\left(\dfrac{\partial S}{\partial V}\right)_T=\left(\dfrac{\partial p}{\partial T}\right)_V$：熵随体积的变化 → 换成 $pVT$ 数据。
- $\left(\dfrac{\partial S}{\partial p}\right)_T=-\left(\dfrac{\partial V}{\partial T}\right)_p$：熵随压力的变化 → 换成热膨胀。
- 配合 $\left(\dfrac{\partial U}{\partial V}\right)_T = T\left(\dfrac{\partial p}{\partial T}\right)_V - p$（内压公式），可由状态方程求内压。
- 焦耳-汤姆逊系数 $\mu_{JT}=\dfrac1{C_p}\left[T\left(\dfrac{\partial V}{\partial T}\right)_p-V\right]$。

## 易错点

1. **死背口诀记混符号**——务必现推。推的时候先写全微分，再套混合偏导相等。
2. 下标写错（把被固定的量写成变化的量）是最常见失分点。
3. 忘记负号：$dU$ 与 $dG$ 推出的两条**带负号**，$dH$ 与 $dA$ 的不带。
4. Maxwell 关系只对**状态函数**成立；$\delta Q$、$\delta W$ 不是全微分，不能套。

## 与已有页的分工

本卡给**推导方法与四式**；它们在具体热力学问题中的应用见 [[决赛要求/物理化学深化/吉布斯-亥姆霍兹方程]]、[[决赛要求/物理化学深化/化学势与平衡]]。

## 参见

数学基础见 [[偏导数与全微分]]；讲义 [[数学工具-第5讲-偏导与全微分]]。
