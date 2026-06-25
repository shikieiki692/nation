---
title: Arrhenius方程
aliases: [Arrhenius Equation, 阿伦尼乌斯方程, 速率常数温度公式]
type: 知识点
template_version: v1.3
subject: 化学原理
module: 化学原理
submodule: 化学动力学
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-化学原理
syllabus_code: [7, 决赛07]
syllabus_module: [化学原理]
tags: [化竞, 化学动力学]
related: [活化能, 反应速率, 速率方程, 反应级数]
prerequisite: [反应速率, 活化能]
problem_types: [题型-Arrhenius方程计算, 题型-活化能求解]
difficulty: 3
importance: 5
status: 已填充
stage: published
sources:
  - 提炼-普化原理-第7章-化学反应速率
  - 专题-化学动力学初步
source_type:
  - 书籍提炼
  - 专题归纳
source_notes:
  - "[[提炼-普化原理-第7章-化学反应速率]]"
  - "[[专题-化学动力学初步]]"
  - "[[04-课件/新授课/2026-06-02-化学动力学初步-基础班]]"
review_cycle: 30d
has_images: false
image_count: 0
images_priority: low
images_note: "当前以公式、作图法与两点法计算为主，文字足够；后续如补图可加入lnk-1/T直线示意。"
teaching_ready: false
key_images: []
updated: 2026-06-04
---

# Arrhenius方程

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-化学原理]]
- 对应考纲条目：[[07-化学平衡]]

## 一、定义
**Arrhenius方程**描述速率常数 $k$ 与温度 $T$ 的定量关系：

$$k = A e^{-E_a/RT}$$

其中 $A$ 为指前因子，$E_a$ 为活化能，$R$ 为气体常数。

## 二、考纲对应
- [[07-化学平衡]]：温度对反应速率的影响、活化能、Arrhenius公式

## 三、核心原理

### 指数形式
$$k = A e^{-E_a/RT}$$

- 温度升高，指数项变大，$k$ 增大，反应加快
- 活化能越大，反应对温度越敏感
- 催化剂本质上是降低 $E_a$，从而增大 $k$

### 对数形式
对上式取对数，得：

$$\ln k = \ln A - \frac{E_a}{RT}$$

因此作 $\ln k$ 对 $1/T$ 图可得直线：

- 斜率 $= -E_a/R$
- 截距 $= \ln A$

### 两点法
同一反应在两个温度下有：

$$\ln \frac{k_2}{k_1} = \frac{E_a}{R}\left(\frac{1}{T_1} - \frac{1}{T_2}\right)$$

这是竞赛和课堂中最常用的计算形式。

## 四、关键结论

1. **温度影响速率常数，而不是直接改变化学计量关系。**
2. **Arrhenius方程连接了宏观速率与微观能垒。**
3. **$R$ 的单位必须和 $E_a$ 匹配**：
   - 若 $R = 8.314\ \mathrm{J\cdot mol^{-1}\cdot K^{-1}}$，则 $E_a$ 算出为 $\mathrm{J\cdot mol^{-1}}$
   - 若答案要写成 $\mathrm{kJ\cdot mol^{-1}}$，需再除以 1000

## 五、常见分类或情形

### 1. 已知两温度下的 $k$
直接用两点法求 $E_a$ 或外推另一温度下的 $k$。

### 2. 已知多组温度与 $k$
作 $\ln k$ 对 $1/T$ 图，利用斜率求 $E_a$，通常比两点法稳定。

### 3. 催化前后比较
若催化后速率明显增大，本质是 $E_a$ 降低；但平衡常数 $K$ 与反应热 $\Delta H$ 不因此改变。

## 六、适用条件与限制
- 主要适用于一定温度区间内的经验拟合
- 对复杂多步反应，求得的往往是**表观活化能**
- 使用时必须统一温度单位为 K

## 七、常见错误
- 把摄氏温度直接代入公式
- 混淆 $\ln$ 与 $\lg$
- 用错 $R$ 的单位，导致 $E_a$ 数量级错误
- 误以为催化剂会改变平衡常数

## 八、与其他知识点的连接
- 与 [[活化能]]：Arrhenius方程是活化能最直接的计算入口
- 与 [[反应速率]]：解释温度为什么改变速率常数
- 与 [[反应级数]]：级数决定积分形式，Arrhenius方程决定 $k$ 的温度依赖

## 九、一句话记忆
**Arrhenius方程是“温度如何通过能垒改变速率常数”的标准表达式。**
