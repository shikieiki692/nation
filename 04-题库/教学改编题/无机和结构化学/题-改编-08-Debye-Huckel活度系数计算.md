---
title: "题-改编-08-Debye-Huckel活度系数计算"
type: 题目
fidelity: 自编
submodule: 电解质溶液
exam_stage: 初赛
subject: 无机和结构化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: []
knowledge_points: ["[[离子强度与Debye-Hückel极限定律]]", "[[活度与活度系数]]"]
tags: [化竞, 题库, 改编题, 电解质溶液, Debye-Huckel, 活度系数]
updated: 2026-07-09
aliases: ["改编-电解质-DebyeHuckel", "活度系数计算"]
source: "教学改编题（知识点补充）"
module: 电解质溶液
status: 已填充
subject_module: 元素与分析
pack: 章节练习
---
# 题-改编-08-Debye-Huckel活度系数计算

## 题目

Debye-Hückel 极限公式为：

$$\log_{10} \gamma_{\pm} = -A |z_+ z_-| \sqrt{I}$$

其中 $A = 0.509\ (\text{mol}^{-1/2} \cdot \text{kg}^{1/2})$（25°C 水溶液），$z_+$、$z_-$ 为离子电荷数，$I$ 为离子强度。

(a) 计算 0.005 mol/kg NaCl 溶液在 25°C 时的离子强度和平均活度系数 $\gamma_{\pm}$。

(b) 计算 0.001 mol/kg CaCl₂ 溶液在 25°C 时的离子强度和平均活度系数 $\gamma_{\pm}$。

(c) 比较上述两种溶液的活度系数，并解释为什么高价离子溶液的活度系数偏离 1 更多。

## 参考答案

**(a) NaCl 溶液（$m = 0.005$ mol/kg）：**

离子强度：

$$I = \frac{1}{2} \sum_i m_i z_i^2 = \frac{1}{2} (m_{Na^+} \times 1^2 + m_{Cl^-} \times 1^2)$$

$$I = \frac{1}{2} (0.005 \times 1 + 0.005 \times 1) = \frac{1}{2} \times 0.010 = 0.005\ \text{mol/kg}$$

平均活度系数：

$$\log_{10} \gamma_{\pm} = -0.509 \times |1 \times 1| \times \sqrt{0.005} = -0.509 \times 0.0707 = -0.0360$$

$$\gamma_{\pm} = 10^{-0.0360} = 0.920$$

**(b) CaCl₂ 溶液（$m = 0.001$ mol/kg）：**

$$\text{CaCl}_2 \rightarrow \text{Ca}^{2+} + 2\text{Cl}^-$$

离子强度：

$$I = \frac{1}{2} (m_{Ca^{2+}} \times 2^2 + m_{Cl^-} \times 1^2) = \frac{1}{2} (0.001 \times 4 + 0.002 \times 1)$$

$$I = \frac{1}{2} (0.004 + 0.002) = 0.003\ \text{mol/kg}$$

平均活度系数：

$$\log_{10} \gamma_{\pm} = -0.509 \times |2 \times (-1)| \times \sqrt{0.003} = -0.509 \times 2 \times 0.0548 = -0.0558$$

$$\gamma_{\pm} = 10^{-0.0558} = 0.879$$

**(c) 比较与解释：**

- NaCl：$I = 0.005$，$\gamma_{\pm} = 0.920$
- CaCl₂：$I = 0.003$，$\gamma_{\pm} = 0.879$

尽管 CaCl₂ 溶液的离子强度更低，但其活度系数偏离 1 的程度更大。

原因：Debye-Hückel 公式中，$\log \gamma_{\pm}$ 与 $|z_+ z_-| \sqrt{I}$ 成正比。CaCl₂ 中离子电荷的乘积 $|z_+ z_-| = |2 \times 1| = 2$，而 NaCl 中 $|z_+ z_-| = 1$。因此，即使离子强度较低，高价离子间的静电相互作用更强，离子氛效应更显著，导致活度系数偏离理想值（$\gamma = 1$）更多。

## 解题思路

1. 离子强度公式：$I = \frac{1}{2} \sum m_i z_i^2$，注意每个离子都要计算，包括其浓度乘以电荷数的平方。
2. 对于 $M_aX_b$ 型电解质：$I = \frac{1}{2}(a \cdot m \cdot z_M^2 + b \cdot m \cdot z_X^2) = \frac{1}{2} m \cdot (a z_M^2 + b z_X^2)$。
3. Debye-Hückel 极限公式适用于稀溶液（$I < 0.01$ mol/kg），浓度越稀，公式越准确。
4. 易错点：$|z_+ z_-|$ 取绝对值，活度系数始终小于 1（对于正常电解质溶液）。