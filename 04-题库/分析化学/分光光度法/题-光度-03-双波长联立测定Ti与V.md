---
title: "题-光度-03-双波长联立测定Ti与V"
aliases: ["题-光度-03"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 挑战
source: "分析化学（第六版）第10章 教学改编"
module: "分光光度法"
subject: 分析化学
syllabus_codes: ["20"]
knowledge_points: ["[[Lambert-Beer定律]]", "[[吸光度]]", "[[分光光度法]]"]
tags: [化竞, 题目, 分光光度法, 双波长]
updated: 2026-08-04
status: 已填充
exam_stage: 初赛
---
# 题-光度-03：双波长联立测定 Ti 与 V 混合液

## 题目

含 Ti(IV) 与 V(V) 的混合溶液与 H₂O₂ 反应生成有色配合物。已知在 1 cm 吸收池中，两组分在两波长处的摩尔吸收系数（L·mol⁻¹·cm⁻¹）为：

| 波长/nm | ε(Ti) | ε(V) |
|:---:|:---:|:---:|
| 415 | $6.0\times10^{3}$ | $1.0\times10^{3}$ |
| 455 | $1.0\times10^{3}$ | $5.0\times10^{3}$ |

测得混合液 $A_{415} = 0.310$，$A_{455} = 0.260$。求混合液中 $c_{\mathrm{Ti}}$ 与 $c_{\mathrm{V}}$。

## 参考答案

由吸光度加和性列出联立方程组（$b = 1$ cm）：

$$A_{415} = 6000\,c_{\mathrm{Ti}} + 1000\,c_{\mathrm{V}} = 0.310 \quad\cdots(1)$$

$$A_{455} = 1000\,c_{\mathrm{Ti}} + 5000\,c_{\mathrm{V}} = 0.260 \quad\cdots(2)$$

由(1)得 $c_{\mathrm{V}} = 0.310\times10^{-3} - 6\,c_{\mathrm{Ti}}$，代入(2)：

$$0.260 = 1000\,c_{\mathrm{Ti}} + 5000(0.310\times10^{-3} - 6\,c_{\mathrm{Ti}}) = 1.55 - 29000\,c_{\mathrm{Ti}}$$

$$c_{\mathrm{Ti}} = \frac{1.55 - 0.260}{29000} = 4.45\times10^{-5}\ \mathrm{mol/L}$$

$$c_{\mathrm{V}} = 0.310\times10^{-3} - 6 \times 4.45\times10^{-5} = 4.3\times10^{-5}\ \mathrm{mol/L}$$

**答案**：$c_{\mathrm{Ti}} = 4.45\times10^{-5}$ mol/L，$c_{\mathrm{V}} = 4.3\times10^{-5}$ mol/L。

## 知识点映射

- 核心考点：吸光度加和性、双波长联立方程组
- 前提条件：两组分**无相互作用**、分别在两波长处 $\varepsilon$ 差异足够大
- 易错点：解方程组前统一单位（mol/L）；注意有效数字；解出后回代检验

> **题源关联**：赵鑫光-光度例3（Ti+V 与 H₂O₂ 双波长联立，[[04-题库/教材习题/赵鑫光/题-赵鑫光-容量分析-光度例3|赵鑫光-光度例3]]）
