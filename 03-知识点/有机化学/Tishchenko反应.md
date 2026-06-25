---
title: Tishchenko反应
aliases: [Tishchenko Reaction, 醛歧化为酯, 铝催化歧化, 酯化歧化]
type: 知识点
template_version: v1.3
subject: 有机化学
module: 有机化学
submodule: 氧化还原
syllabus_stage: 进阶
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-有机化学
syllabus_code: [40]
syllabus_module: [有机化学]
tags:
  - 化竞
  - 有机化学
  - Tishchenko反应
  - 歧化反应
  - 酯合成
  - 负氢迁移
  - 铝催化
  - 人名反应
related: [Cannizzaro反应, 氧化还原反应, 负氢迁移, 酯的化学, 醛酮化学]
prerequisite: [醛酮化学, 氧化还原反应, 负氢迁移]
problem_types: [题型-酯合成设计, 题型-歧化产物预测]
difficulty: 3
importance: 3
status: 已填充
stage: published
sources: ["ABOC §4.11"]
source_type: []
review_cycle: 30d
has_images: false
images_priority: 结构/机理 medium，纯公式 low
images_note: 
teaching_ready: false
source_notes: []
key_images: []
updated: 2026-05-25
---
# Tishchenko 反应（Tishchenko Reaction）
- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-有机化学]]
- 对应考纲条目：[[40-氧化还原反应]]
---

## 一、定义

**Tishchenko 反应**：醛在**铝醇盐（如 Al(OEt)₃）**催化下发生**分子间歧化**，生成**酯**的反应。

**通式**：
$$
\ce{2 RCHO ->[Al(OEt)3] RCOOCH2R}
$$

**本质**：是两分子醛的氧化还原——一分子醛被氧化为羧酸（进而成酯），另一分子被还原为醇（作为酯的醇部分）。

---

## 二、考纲对应

- 对应考纲条目：[[40-氧化还原反应]]
- 所属模块：[[基础要求-有机化学]]
- 本知识点在考纲中的作用：Tishchenko 是**负氢迁移机理的又一案例**，与 Cannizzaro 形成"酸/碱催化歧化"的对照。

---

## 三、核心原理

### 3.1 反应机理

**铝催化下的负氢迁移**：
```
步骤 1：Al(OEt)₃ 与醛配位 → 活化羰基
步骤 2：第二分子醛的负氢迁移到配位醛上
步骤 3：生成的醇负离子进攻另一分子醛的羰基
步骤 4：酯形成，Al(OEt)₃ 再生
```

**关键特征**：
- **负氢迁移**是核心步骤（与 Cannizzaro、MPV 共享机理）
- **Al(III) 是 Lewis 酸催化剂**——不是碱
- **产物是酯**，不是醇 + 酸盐（与 Cannizzaro 不同）

### 3.2 与 Cannizzaro 反应的对比

| | **Tishchenko** | **Cannizzaro** |
|:---|:---|:---|
| **催化剂** | Al(OEt)₃（Lewis 酸）| NaOH（强碱）|
| **产物** | **酯** | 醇 + 羧酸盐 |
| **底物要求** | 无 α-H 或有 α-H 均可 | 无 α-H |
| **机理核心** | 负氢迁移 | 负氢迁移 |
| **催化循环** | Al 催化剂可循环 | OH⁻ 消耗于产物中 |

### 3.3 交叉 Tishchenko

**两种不同醛的混合物**：
$$
\ce{RCHO + R'CHO ->[Al(OEt)3] RCOOCH2R' + R'COOCH2R}
$$

- 产物是**两种酯的混合物**
- 选择性取决于醛的活性和催化剂配位偏好

---

## 四、关键结论

1. **Tishchenko = 醛 + Al(OR)₃ → 酯**
2. **与 Cannizzaro 共享负氢迁移机理**——催化剂不同导致产物不同
3. **有 α-H 的醛也能反应**——不像 Cannizzaro 限制无 α-H
4. **Al(III) 是 Lewis 酸催化剂**——通过配位活化羰基
5. **产物酯的醇部分来自被还原的醛**

---

## 五、常见分类或情形

### 5.1 按醛类型分类

| 醛类型 | 产物 | 备注 |
|:---|:---|:---|
| **脂肪醛** | 脂肪族酯 | 通用 |
| **芳香醛** | 芳香族酯 | 苯甲醛 → 苯甲酸苄酯 |
| **α,β-不饱和醛** | 烯醇酯 | 可能竞争 1,4-加成 |

### 5.2 与 Claisen 缩合的对比

| | **Tishchenko** | **Claisen 缩合** |
|:---|:---|:---|
| **底物** | 醛 | 酯 |
| **产物** | 酯 | β-酮酯 |
| **催化剂** | Al(OR)₃ | NaOR（强碱）|
| **α-H 要求** | 不需要 | 需要 |

---

## 六、适用条件与限制

1. **需无水条件**——Al(OR)₃ 遇水分解
2. **无 α-H 或有 α-H 均可**——不像 Cannizzaro 限制严格
3. **通常需加热**——室温下反应较慢
4. **催化剂用量 5-10 mol%**——Al 可循环
5. **对酸敏感底物不友好**——Al 催化剂有一定酸性

---

## 七、常见比较与易混点

### 7.1 Tishchenko vs Cannizzaro

- 两者都是醛的歧化
- Tishchenko：酸催化（Al），产物酯
- Cannizzaro：碱催化（NaOH），产物醇 + 酸盐
- 核心机理都是负氢迁移

### 7.2 Tishchenko vs 酯化反应

- Tishchenko：两分子醛 → 酯（自身氧化还原）
- 酯化反应：酸 + 醇 → 酯（缩合）
- Tishchenko 不需要外加酸或醇

---

## 八、与其他知识点的联系

- **前置知识**：[[醛酮化学]]、[[氧化还原反应]]、[[负氢迁移]]
- **相关知识**：
  - "[[Cannizzaro反应]]（同一机理的碱催化版本）"
  - "[[酯的化学]]（产物类型）"
- **应用知识**：
  - "[[题型-有机合成设计]]（从醛制备酯）"

---

## 九、典型题型

- 题型-酯合成设计：从醛出发设计酯的合成路线
- 题型-歧化产物预测：判断 Tishchenko 产物结构

---

## 十、例题

### 10.1 例题 1（★ 基础）

**题目**：苯甲醛在 Al(OEt)₃ 催化下加热，产物是什么？

**解答**：
- 2 PhCHO → **苯甲酸苄酯**（PhCOOCH₂Ph）
- 一分子苯甲醛被氧化为苯甲酸
- 另一分子被还原为苯甲醇
- 两者缩合为酯

### 10.2 例题 2（★★ 对比）

**题目**：比较 Tishchenko 和 Cannizzaro 反应的差异。

**解答**：
- 相同：都是醛的歧化，负氢迁移机理
- 不同：催化剂（Al(OEt)₃ vs NaOH）、产物（酯 vs 醇+酸盐）、底物限制（无 vs 无 α-H 限制）

---

## 十一、易错点

1. ❌ **Tishchenko 只能用于无 α-H 醛** → **有 α-H 也能反应**
2. ❌ **产物是醇 + 酸** → 产物是**酯**
3. ❌ **需要碱催化** → 需要 **Al(III) Lewis 酸**
4. ❌ **与 Cannizzaro 产物相同** → 产物不同（酯 vs 醇+酸盐）

---

## 十二、🎯 教学视角

### 12.1 学习路径

- **前置**：[[Cannizzaro反应]]、[[氧化还原反应]]
- **后续**：[[题型-有机合成设计]]、[[酯的化学]]

### 12.2 学生易踩的认知误区

| 误区 | 正确认识 | 辨析口诀 |
|---|---|---|
| "Tishchenko 要无αH" | 有αH也能做 | "Tishchenko 不限醛" |
| "产物是醇和酸" | 产物是酯 | "铝催化下变酯" |

### 12.3 入门例题

**题目**：为什么 Tishchenko 和 Cannizzaro 的产物不同？

**引导**：
- 两者都是负氢迁移
- 但催化剂不同：Al(III) 是 Lewis 酸，NaOH 是碱
- Al 催化下，生成的醇和酸在 Al 配位下直接缩合为酯
- 碱催化下，酸以盐形式存在，不能酯化

### 12.4 现实类比

**Tishchenko 像"交换礼物"**：
- 两个人（两分子醛）各带一份礼物（一个带氧化潜力，一个带还原潜力）
- Al 催化剂是"主持人"——撮合交换
- 最后两人合成一个"组合礼物"（酯）

---

## 十三、竞赛拓展

1. **Evans-Tishchenko 反应**：
   - 醛 + β-羟基酮 → anti-1,3-二醇单酯
   - 在天然产物合成中有重要应用

2. **不对称 Tishchenko**：
   - 手性铝配合物催化
   - 对映选择性酯合成

---

## 十四、修订记录

- **v1.1（2026-05-10）**：首次创建。基于 ABOC §4.11 Tishchenko 框架。涵盖负氢迁移机理、与 Cannizzaro 的酸/碱催化对照、交叉 Tishchenko、产物预测。Phase C Ch.4 新建 KP。

---

```dataview
TABLE file.name AS "文件名", year AS "年份", type AS "题型", difficulty AS "难度"
FROM "04-题库"
WHERE contains(knowledge_points, "Tishchenko反应")
SORT year DESC, difficulty ASC
```

## 十四、外部资料出处

## 十五、待完善项
