---
title: "题-071-一分册测试-Ch4B-3-CoO热还原与温度控制"
type: 题目
aliases: ["一分册测试Ch4B题3"]
source_subject: 化学原理
submodule: 冶金热力学
subject_module: 化学原理
exam_stage: 初赛
question_type: [计算, 简答]
difficulty: 5
teaching_level: 竞赛
fidelity: 原书逐字
knowledge_points: ["[[Gibbs自由能]]", "[[化学平衡]]"]
concepts: ["ΔG-T线性式", "还原反应耦合", "气相平衡组成与温度函数", "冶金优势区图"]
pack: 模块习题集
tags: [化竞, 一分册测试, 计算]
created: 2026-09-03
updated: 2026-09-03
source: 高中化学竞赛教程第一分册·配套能力测试 第4章
source_file: "[[07-资料提炼/习题提炼/习题-一分册测试-Ch4-化学反应中的能量变化]]"
cross_references: []
status: 已填充
source_category: 竞赛导向·竞赛教辅
source_grade: A-
---

# 题-071-一分册测试-Ch4B-3-CoO热还原与温度控制

## 题目

金属冶炼最常用的方法之一就是热还原法。如金属钴可用 CO 还原其氧化物制得：

$\mathrm{CoO(s) + CO(g)\longrightarrow Co(s) + CO_2(g)}$。已知：$\Delta G^0 = -RT\ln K^0$

$$
2 \mathrm{CO} + \mathrm{O} _ {2} \longrightarrow 2 \mathrm{CO} _ {2} \quad \Delta_ {\mathrm{r}} G _ {1} ^ {0} = - 564.8 \times 10 ^ {3} + 173.6 T
$$

$$
2 \mathrm{Co} + \mathrm{O} _ {2} \longrightarrow 2 \mathrm{CoO} \quad \Delta_ {\mathrm{r}} G _ {2} ^ {0} = - 457.8 \times 10 ^ {3} + 143.7 T
$$

3-1 求反应达平衡时气相中 CO 的体积分数与反应温度之间的函数关系。

3-2 在 $1500 \mathrm{~K}$ 时用 $\mathrm{CO}$、$\mathrm{CO}_{2}$ 混合气体还原 $\mathrm{CoO}$，问气相中 $\mathrm{CO}$ 的体积分数 $(\mathrm{CO} \%)$ 应至少控制在多大？

3-3 冶金工业中常用如图判断产物的组成及反应控制的温度。若平衡浓度 $\mathrm{CO}\% = \mathrm{CO}_{2}\%$，问反应应控制在什么温度范围？

![[96a2994f24400188e0ac06d7ce642301dde8c0321f98ccdeeb2ff56971c4dde8.jpg]]
第3题图

## 参考答案

<details>
<summary>📖 查看答案与解析</summary>

(1) $\mathrm{CoO} + \mathrm{CO} \longrightarrow \mathrm{Co} + \mathrm{CO}_{2}$

$\Delta_{\mathrm{r}} G_{3}^{0} = (\Delta_{\mathrm{r}} G_{1}^{0} - \Delta_{\mathrm{r}} G_{2}^{0}) / 2 = -48.5 \times 10^{3} + 14.95 T$

$\Delta_{\mathrm{r}} G_{3}^{0} = -RT \ln [c(\mathrm{CO}_{2}) / c(\mathrm{CO})] = -RT \ln [(1 - \mathrm{CO}\%) / \mathrm{CO}\%]$

$\ln [(1 - \mathrm{CO}\%) / \mathrm{CO}\%] = 5833.5 / T - 1.798$

(2) 将 $T = 1500$ 代入解得 $\mathrm{CO}\% = 11.0\%$

(3) 因为 $\mathrm{CO}\% = \mathrm{CO}_{2}\% = 50\%$，故有 $5833.5 / T = 1.798$，解得 $T = 3243$

</details>

<!-- 校勘注: B卷第3题题号在试题 md 中丢失（孤立「(10 分) <<<」标记，按分值块连续性重建为第3题）；答案 3-1 原书写作「ln[(1-CO%)/CO%] = -5833.5/T + 1.798」，符号与 3-2 数值结果（T=1500 代入得 CO%=11.0%）及 3-3 用法（ln=0 → 5833.5/T=1.798）均矛盾，按自洽性修正为「= 5833.5/T - 1.798」（验证：ΔG₃⁰=-RTlnK → lnK=48500/RT-14.95T/RT=5833.5/T-1.798，K=p(CO₂)/p(CO)=(1-x)/x，置信度高）；3-3 题问「温度范围」答案仅给分界温度 T=3243 K，照录；题图 96a2994f 为原书扫描件（CO%-T 坐标框），曲线信息在扫描中模糊缺失，不影响解答（答案不依赖曲线读数），照实入库；余为原书逐字 -->
