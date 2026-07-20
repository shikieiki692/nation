---
title: "Replacement Test判断分子NMR信号数"
aliases: ["题-有机-波谱-08"]
type: 题目
exam_stage: 初赛
source: "Zchem基础有机化学"
source_author: "Zchem网课提炼"
subject: 有机化学
module: 有机化学
submodule: 波谱分析
question_type: 判断题
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["49"]
knowledge_points: ["[[NMR谱学]]", "[[化学等价]]", "[[对称性分析]]"]
tags: [化竞, 题目, 有机化学]
status: 已填充
updated: 2026-07-10
---

# Replacement Test判断分子NMR信号数

## 题目

**(1)** 什么是 Replacement Test（取代测试）？简述其判断 ¹H NMR 信号数的基本步骤。

**(2)** 用 Replacement Test 判断甲苯（C₆H₅CH₃）在 ¹H NMR 中应出现几组信号（不考虑邻/间/对位芳氢的细微差别时）。

**(3)** 用 Replacement Test 判断 1,2-二氯乙烷（ClCH₂CH₂Cl）有几组 ¹H NMR 信号。

## 参考答案

### (1) Replacement Test 原理

**Replacement Test** 是判断分子中等价氢原子组数的方法：

**步骤**：
1. 逐一将分子中的每个 H 原子替换为一个标记原子 X（如 D 或任意"测试基团"）
2. 得到 N 个"取代产物"（N = H 原子总数）
3. 比较这 N 个取代产物：如果两个取代产物**完全相同**（可通过旋转、反映等对称操作重合），则原来的两个 H 是**化学等价的**
4. 将所有 H 按等价关系分组，组数 = ¹H NMR 的信号数

### (2) 甲苯的信号数

甲苯结构：Ph-CH₃

逐一替换 H：
- 替换 CH₃ 上的 H → 得到 Ph-CH₂X
- 替换邻位 H → 得到 o-X-C₆H₄-CH₃
- 替换间位 H → 得到 m-X-C₆H₄-CH₃
- 替换对位 H → 得到 p-X-C₆H₄-CH₃

CH₃ 上的三个 H 替换后产物相同（旋转等价）→ 1 组
邻位两个 H 替换后产物相同（对称面）→ 1 组
间位两个 H 替换后产物相同 → 1 组
对位 H → 1 组

**答案：4 组信号**（CH₃、邻-H、间-H、对-H）

> 注：若题目要求不区分邻/间/对，则合并为 2 组（CH₃ + 芳 H）。

### (3) 1,2-二氯乙烷的信号数

ClCH₂-CH₂Cl，结构高度对称。

逐一替换：
- 替换任意一个 H → 得到 ClCH(X)-CH₂Cl
- 由于分子有对称中心（C₂ 旋转轴），4 个 H 中任意一个被替换后的产物都可通过旋转/反映重合

**答案：1 组信号**（4 个 H 全部等价）

### 关键要点

- Replacement Test 的本质是利用**分子对称性**判断等价性
- 对称操作包括：旋转轴（C₂、C₃...）、对称面（σ）、对称中心（i）
- **化学等价** ≠ **磁等价**：Replacement Test 只判断化学等价；磁等价还需考虑与相邻核的偶合关系

> ⚠️ **易错点**：自由旋转的单键上的 H 天然等价（如 CH₃ 的三个 H），但受环或双键限制的 H 可能不等价。

## 知识点映射

- [[NMR谱学]]
- [[化学等价]]
- [[对称性分析]]
