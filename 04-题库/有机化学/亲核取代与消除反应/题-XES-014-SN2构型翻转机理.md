---
title: "题-XES-014-SN2构型翻转机理"
type: 题目
source: "学而思有机化学基础 第4-5讲"
source_file: "06-外部资料导入/学而思 有机化学基础 学生讲义/04-05第六章卤代烃学生版.md"
source_subject: 有机化学
year: 2023
difficulty: 4
question_type: [机理]
teaching_level: 拓展
knowledge_points: ["[[SN2反应]]", "[[构型翻转]]"]
status: 已填充
tags: [化竞, 有机化学, 学而思]
created: 2026-08-27
updated: 2026-08-31
subject_module: 有机化学
pack: 模块习题集
fidelity: 原书逐字
exam_stage: 初赛
source_category: 其他类型·自编章节题
---

# 题-XES-014：SN2构型翻转机理

> **来源**：学而思有机化学基础 第4-5讲 卤代烃
> **难度**：⭐⭐⭐⭐
> **教学层级**：中难

---

## 题目

> 📌 *本题原含 1 张学而思讲义图片，源文件图片未导入 vault*

习题 18. $\mathrm{S_N2}$ 反应伴随着构型翻转而发生， $\mathrm{S_N1}$ 反应伴随着消旋化发生。然而下列反应以完全的构型保持而发生。提出机理。

<details>
<summary>chemical</summary>

Chemical reaction equation showing bromoalkane hydrolysis with sodium bicarbonate and water to form a cyclic alcohol
</details>

---

## 参考答案

该反应**以完全的构型保持**发生，说明既不是简单的 $\rm{S_N}1$（消旋），也不是简单的 $\rm{S_N}2$（单次翻转）。其机理为**邻基参与（Neighboring Group Participation，NGP）**，经历**两次连续翻转**，净结果为构型保留。

**机理分析（双反转 = 净保留）**：

**第一步：邻基参与的分子内 $\rm{S_N}2$（第一次翻转）**

底物中存在邻近的亲核基团（如 $\rm{-OH}$ 或酯氧）。在碱性条件（$\rm{NaHCO_3}$）下，该基团被活化为亲核体，**从离去基 $\rm{Br^-}$ 的同侧反面**对手性中心进行**分子内亲核取代**（backside attack），形成**环状中间体**（如三元环或五元环）。

$$\rm{Nuc{:}^-}_{分子内} + \text{手性C-Br} \xrightarrow{\text{内部 S}_N\text{2}} \text{环状中间体} + \rm{Br^-}$$

此步骤发生**一次构型翻转**。

**第二步：$\rm{H_2O}$ 开环（第二次翻转）**

$\rm{H_2O}$ 作为外部亲核试剂，从环状中间体的**背面**进攻开环，又发生**一次 $\rm{S_N}2$ 翻转**。

$$\rm{H_2O} + \text{环状中间体} \xrightarrow{\text{S}_N\text{2开环}} \text{醇产物（构型保留）}$$

**两次翻转的净结果**：

$$\text{翻转} \times 2 = \text{保留}$$

相对于原底物手性中心，构型完全保留。

**关键条件**：

| 条件 | 作用 |
|:---|:---|
| $\rm{NaHCO_3}$（弱碱）| 中和 HBr，活化邻近亲核基团（如去质子 OH）|
| 中性水 | 第二步开环的亲核试剂 |
| 邻近亲核基团 | 使第一步成为分子内 $\rm{S_N}2$（快速，立体选择性高）|

**总结**：邻基参与机理通过"两次 $\rm{S_N}2$ 翻转"实现净构型保留，是解释完全构型保持的标准解释。

---
