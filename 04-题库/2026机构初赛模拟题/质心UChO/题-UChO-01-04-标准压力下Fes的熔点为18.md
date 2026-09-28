---
title: "题-UChO-01-04-标准压力下Fes的熔点为18"
aliases: ["题-UChO-01-04"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "质心UChO 8thZCHEM-UChO-Tour1 第 4 题"
module: "2026机构初赛模拟题"
source_subject: 化学原理
syllabus_codes: []
knowledge_points: []
tags: [化竞, 题目, 初赛, 机构模拟题, 质心UChO]
updated: 2026-09-26
status: 已填充
exam_stage: 初赛
subject_module: 化学原理
pack: 综合模拟卷
submodule: 质心UChO
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_tier: 2
source_norm: "质心UChO-8thZCHEM-UChO-Tour1"
source_file: "2026机构初赛模拟题/02-质心UChO/8thZCHEM-UChO-Tour1.md"
---

# 题-UChO-01-04-标准压力下Fes的熔点为18

## 题目

### 第 4 题（10 分，占 6%）熔融体系的热力学

标准压力下， $\delta$ -Fe(s)的熔点为 1808 K，熔化热为 15355 J mol $^{-1}$ ，可以认为 Fe(l)与 $\delta$ -Fe(s)的标准恒压摩尔热容差为 1.255 J K $^{-1}$ mol $^{-1}$ 。现又已知 $\delta$ -Fe(s)和铁溶于硫化铁的熔融液体(其中 Fe 的摩尔分数为 0.87)刚好在 1673 K 下达到相平衡，在本题的计算中认为纯的 Fe(l)为标态。

4-1 导出 $\delta-\mathrm{Fe}(\mathrm{s})$ 的熔化热 $\Delta_{\mathrm{mel}}H_{\mathrm{m}}(\text{单位 J mol}^{-1})$ 与温度(单位 K)的关系。

4-2 计算 1673 K 下， $\delta$ -Fe(s)熔化的标准平衡常数。

4-3 计算熔融液体中 Fe 的活度系数 $\gamma$ 。此问结果保留两位有效数字即可。

## 参考答案

标准压力下， $\delta$ -Fe(s)的熔点为 $1808\mathrm{K}$ ，熔化热为 $15355\mathrm{J mol}^{-1}$ ，可以认为 $\mathrm{Fe(l)}$ 与 $\delta$ -Fe(s)的标准恒压摩尔热容差为 $1.255\mathrm{JK}^{-1}\mathrm{mol}^{-1}$ 。现又已知 $\delta$ -Fe(s)和铁溶于硫化铁的熔融液体(其中 Fe 的摩尔分数为 0.87)刚好在 $1673\mathrm{K}$ 下达到相平衡，在本题的计算中认为纯的 $\mathrm{Fe(l)}$ 为标态。

4-1 导出 $\delta-\mathrm{Fe}(\mathrm{s})$ 的熔化热 $\Delta_{\mathrm{mel}}H_{\mathrm{m}}(\text{单位 J mol}^{-1})$ 与温度 (单位 K) 的关系。

易知 $\Delta_{\mathrm{mel}}H_{\mathrm{m}}(T)=\Delta C_{\mathrm{p,m}}T+I$ ，1分代入 $T=1808\ K$ ， $\Delta_{\mathrm{mel}}H_{\mathrm{m}}=15355\ J\ mol^{-1}$ 有 $I=13086\ J\ mol^{-1}$

故 $\Delta_{\mathrm{mel}}H_{\mathrm{m}} = (1.255T / K + 13086)\mathrm{J mol^{-1}}$ 1分

4-2 计算 1673 K 下， $\delta$ -Fe(s)熔化的标准平衡常数。

$$
\Delta_ {\mathrm{mel}} S _ {\mathrm{m}} (1808 \mathrm{K}) = \Delta_ {\mathrm{mel}} H _ {\mathrm{m}} (1808 \mathrm{K}) / 1808 \mathrm{K} = 8.5924 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1} 1
$$

$$
\Delta_ {\mathrm{mel}} S _ {\mathrm{m}} (1673 \mathrm{K}) = \Delta_ {\mathrm{mel}} S _ {\mathrm{m}} (1808 \mathrm{K}) + \Delta C _ {\mathrm{p}, \mathrm{m}} \ln (1673 \mathrm{K} / 1808 \mathrm{K}) = 8.4950 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1}
$$

$$
\Delta_ {\mathrm{mel}} H _ {\mathrm{m}} (1673 \mathrm{K}) = 1.255 \times 1673 + 13086 = 15186 \mathrm{J} \mathrm{mol} ^ {- 1}
$$

$$
\Delta_ {\mathrm{mel}} G _ {\mathrm{m}} ^ {\circ} (1673 \mathrm{K}) = \Delta_ {\mathrm{mel}} H _ {\mathrm{m}} (1673 \mathrm{K}) - T \Delta_ {\mathrm{mel}} S _ {\mathrm{m}} (1673 \mathrm{K}) = 973.44 \mathrm{Jmol} ^ {- 1}
$$

$$
K ^ {\circ} = \exp \left[ - \Delta_ {\mathrm{mel}} G _ {\mathrm{m}} ^ {\circ} / R T \right] = 0.931
$$

也可以直接利用 Gibbs-Helmholtz 方程的不定积分式求解:

$$
\frac {\Delta G}{T} = - \int \frac {\Delta H}{T ^ {2}} \mathrm{d} T + I = - \int \left(\frac {1.255}{T} + \frac {13086}{T ^ {2}}\right) + I = - 1.255 \ln T + \frac {13086}{T} + I ^ {\prime} 2 \text {分}
$$

代入 $T = 1808 \, K, \Delta G = 0$ ，解得 $I' = 2.175$

于是 $\Delta G = -1.255T\ln T + 13086 + 2.175T$ 2分

代入 1673 K 数据即可求解 2 分

4-3 计算熔融液体中 Fe 的活度系数 $\gamma$ 。此问结果保留两位有效数字即可。

根据题意，反应商 $Q = K^{\circ} = \gamma x$ ，故 $\gamma = Q / x = 0.93 / 0.87 = 1.1$ 2 分

## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**（OCR 原文逐字转录，可能保留原卷笔误）。