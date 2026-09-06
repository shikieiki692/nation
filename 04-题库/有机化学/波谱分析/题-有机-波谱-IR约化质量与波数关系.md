---
title: "题-有机-波谱-IR约化质量与波数关系"
type: 题目
fidelity: 自编
submodule: 波谱分析
exam_stage: 初赛
source_subject: 有机化学
difficulty: 2
question_type: [计算]
teaching_level: 巩固
syllabus_codes: ["49"]
knowledge_points:
  - "[[红外光谱]]"
  - "[[化学键振动]]"
concepts:
  - 约化质量
tags: [化竞, 题目, 有机化学]
updated: 2026-07-10
aliases: ["题-有机-波谱-01", "题-1603"]
source: "Zchem基础有机化学"
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 其他类型·自编章节题
---
# C-H与C-C键约化质量与IR波数关系

## 题目

**(1)** 红外光谱中，化学键的振动频率近似服从：

$$\tilde{\nu} = \frac{1}{2\pi c}\sqrt{\frac{k}{\mu}}$$

其中 $k$ 为力常数，$\mu$ 为约化质量 $\mu = \frac{m_1 \cdot m_2}{m_1 + m_2}$。

已知 C-H 键和 C-C 键的力常数相近（约 $k \approx 5 \times 10^5 \text{ dyn/cm}$），分别计算 C-H 和 C-C 键的约化质量（取 $m_C = 12$，$m_H = 1$），并预测哪个键的红外吸收波数更高。

**(2)** 根据上述计算结果，解释为什么有机化合物的 C-H 伸缩振动出现在 ~2900–3000 cm⁻¹，而 C-C 伸缩振动出现在 ~800–1200 cm⁻¹。

## 参考答案

### (1) 约化质量计算

**C-H 键**：

$$\mu_{C-H} = \frac{12 \times 1}{12 + 1} = \frac{12}{13} \approx 0.923$$

**C-C 键**：

$$\mu_{C-C} = \frac{12 \times 12}{12 + 12} = \frac{144}{24} = 6.000$$

由于 $\tilde{\nu} \propto \sqrt{1/\mu}$，在力常数 $k$ 相近的前提下：

$$\frac{\tilde{\nu}_{C-H}}{\tilde{\nu}_{C-C}} = \sqrt{\frac{\mu_{C-C}}{\mu_{C-H}}} = \sqrt{\frac{6.000}{0.923}} \approx \sqrt{6.5} \approx 2.55$$

**C-H 键的红外吸收波数约为 C-C 键的 2.5 倍**。

### (2) 波数差异的物理解释

- **C-H 键**：约化质量极小（0.923），振动频率高，伸缩振动出现在 **~2900–3000 cm⁻¹** 区域。
- **C-C 键**：约化质量大（6.0），振动频率低，伸缩振动出现在 **~800–1200 cm⁻¹** 的指纹区。

本质：**轻原子参与的键振动频率更高**。这也是 O-H、N-H、C-H 伸缩振动总出现在红外光谱高波数端（>2500 cm⁻¹）的原因。

### 关键结论

| 键型 | 约化质量 $\mu$ | 典型波数范围 |
|:---|:---:|:---|
| C-H | 0.92 | 2850–3100 cm⁻¹ |
| C-C | 6.00 | 800–1200 cm⁻¹ |

> 💡 **快速记忆**：约化质量越小 → 波数越高。

## 知识点映射

- [[红外光谱]]
- 约化质量
- [[化学键振动]]