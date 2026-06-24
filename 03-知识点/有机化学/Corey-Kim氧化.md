---
title: Corey-Kim氧化
aliases: [Corey-Kim Oxidation, NCS/DMS氧化, 醇氧化, 温和氧化]
type: 知识点
template_version: v1.3
subject: 有机化学
module: 有机化学
submodule: 氧化还原
syllabus_stage: 进阶
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-有机化学
syllabus_code: [40, 50]
syllabus_module: [有机化学]
tags:
  - 化竞
  - 有机化学
  - Corey-Kim氧化
  - 醇氧化
  - NCS
  - DMS
  - 温和氧化
  - 人名反应
related: [Swern氧化, Dess-Martin氧化, PCC, 醇的氧化, 氧化还原反应]
prerequisite: [醇的化学, 氧化还原反应, 含硫化合物]
problem_types: [题型-氧化试剂选择, 题型-机理推断]
difficulty: 3
importance: 3
status: 已填充
stage: published
sources: ["ABOC §4.12"]
source_type: []
review_cycle: 30d
has_images: false
image_count: 0
images_priority: medium
images_note: "当前未嵌入图像文件；该主题具备一定可视化价值，后续备课时可优先补充结构示意图、关系图或谱图。"
teaching_ready: false
source_notes: []
key_images: []
updated: 2026-05-10
---

# Corey-Kim 氧化（Corey-Kim Oxidation）

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-有机化学]]
- 对应考纲条目：[[40-氧化还原反应]]、[[50-有机合成]]

---

## 一、定义

**Corey-Kim 氧化**：使用 **N-氯代琥珀酰亚胺（NCS）** 和 **二甲硫醚（DMS）** 体系，在碱存在下将**伯醇/仲醇**氧化为**醛/酮**的反应。

**通式**：
$$
\ce{RCH2OH + NCS + DMS + Et3N -> RCHO}
$$

**本质**：与 Swern 氧化类似——通过 DMS 形成活性硫鎓中间体，然后碱促进消除生成羰基化合物。

---

## 二、考纲对应

- 对应考纲条目：[[40-氧化还原反应]]、[[50-有机合成]]
- 所属模块：[[基础要求-有机化学]]
- 本知识点在考纲中的作用：Corey-Kim 是**Swern 氧化的替代方法**，条件更温和，对某些敏感底物更友好。

---

## 三、核心原理

### 3.1 试剂与作用

| 试剂 | 作用 |
|:---|:---|
| **NCS** | 氯化试剂，与 DMS 反应生成活性硫鎓盐 |
| **DMS（Me₂S）** | 亲核硫醚，形成硫鎓中间体 |
| **Et₃N** | 碱，促进最终消除步骤 |

### 3.2 反应机理

**三步机理**：
```
步骤 1：NCS + DMS → 氯代硫鎓盐（Me₂S⁺Cl）
步骤 2：醇进攻硫鎓盐 → 烷氧基硫鎓中间体
步骤 3：Et3N 去质子 → 消除生成醛/酮 + DMS + Et3NH⁺Cl⁻
```

**关键特征**：
- 与 Swern 氧化**机理类似**（都通过硫鎓中间体）
- 但试剂不同：NCS/DMS vs (COCl)₂/DMSO
- **条件更温和**：不需要 -78°C
- **对酸敏感底物友好**

### 3.3 与 Swern 氧化的对比

| | **Corey-Kim** | **Swern** |
|:---|:---|:---|
| **试剂** | NCS + DMS + Et₃N | (COCl)₂ + DMSO + Et₃N |
| **温度** | 0°C ~ 室温 | -78°C |
| **中间体** | 氯代硫鎓 | 氧代硫鎓 |
| **氧化强度** | 温和 | 温和 |
| **1°醇产物** | 醛 | 醛 |
| **操作便利性** | 更简便 | 需低温 |

---

## 四、关键结论

1. **Corey-Kim = NCS/DMS/Et₃N → 醇 → 醛/酮**
2. **Swern 的"温和替代版"**——不需低温
3. **通过硫鎓中间体机理**——与 Swern 共享核心逻辑
4. **对伯醇停在醛**——不过氧化
5. **仲醇 → 酮**——通用

---

## 五、常见分类或情形

### 5.1 按底物分类

| 底物 | 产物 | 可行性 |
|:---|:---|:---:|
| **1°醇** | 醛 | ✅ |
| **2°醇** | 酮 | ✅ |
| **3°醇** | — | ❌（无法氧化）|
| **烯丙醇** | 烯丙醛/酮 | ✅ |
| **苄醇** | 苯甲醛 | ✅ |

### 5.2 与其他氧化方法的对比

| 方法 | 试剂 | 条件 | 特点 |
|:---|:---|:---|:---|
| **Corey-Kim** | NCS/DMS/Et₃N | 0°C ~ 室温 | 温和，简便 |
| **Swern** | (COCl)₂/DMSO | -78°C | 温和，无金属 |
| **Dess-Martin** | DMP | 室温 | 最温和，贵 |
| **PCC** | CrO₃/吡啶 | 室温 | 方便，停在醛 |

---

## 六、适用条件与限制

1. **需无水条件**——NCS 遇水会水解
2. **伯醇 → 醛（不过氧化）**——与 Swern/PCC/Dess-Martin 相同
3. **不氧化双键**——选择性氧化醇
4. **DMS 有恶臭**——需在通风橱操作
5. **NCS 相对安全**——比 Cr 试剂更环保

---

## 七、常见比较与易混点

### 7.1 Corey-Kim vs Swern

- 机理类似（硫鎓中间体）
- Corey-Kim 更温和（不需低温）
- Swern 更常用（文献更多）

### 7.2 Corey-Kim vs Dess-Martin

- Corey-Kim：硫化学，便宜
- Dess-Martin：碘化学，贵但选择性更高

---

## 八、与其他知识点的联系

- **前置知识**：[[醇的化学]]、[[氧化还原反应]]、[[含硫化合物]]
- **相关知识**：
  - "[[Swern氧化]]（机理兄弟）"
  - "[[Dess-Martin氧化]]、[[PCC]]（其他温和氧化）"
- **应用知识**：
  - "[[题型-有机合成设计]]（醇的氧化策略选择）"

---

## 九、典型题型

- 题型-氧化试剂选择：Corey-Kim vs Swern vs Dess-Martin 的选择
- 题型-机理推断：写出 Corey-Kim 的硫鎓中间体

---

## 十、例题

### 10.1 例题 1（★ 基础）

**题目**：1-丁醇经 Corey-Kim 氧化后的产物是什么？

**解答**：
- 1°醇 → **丁醛**
- 不会进一步氧化为丁酸

### 10.2 例题 2（★★ 对比）

**题目**：为什么 Corey-Kim 不需要像 Swern 那样低温？

**解答**：
- Swern 用 (COCl)₂ 活化 DMSO，中间体不稳定，需 -78°C
- Corey-Kim 用 NCS 活化 DMS，中间体更稳定
- 因此可在较高温度下进行

---

## 十一、易错点

1. ❌ **Corey-Kim 是还原反应** → 是**氧化反应**
2. ❌ **1°醇会被氧化到酸** → Corey-Kim **停在醛**
3. ❌ **需要低温** → Corey-Kim **不需低温**（与 Swern 不同）
4. ❌ **3°醇也能氧化** → 3°醇 **不能**氧化（无 α-H）

---

## 十二、🎯 教学视角

### 12.1 学习路径

- **前置**：[[Swern氧化]]、[[醇的化学]]
- **后续**：[[题型-有机合成设计]]、[[氧化还原反应]]

### 12.2 学生易踩的认知误区

| 误区 | 正确认识 | 辨析口诀 |
|---|---|---|
| "Corey-Kim 要低温" | 不需低温 | "Kim 温和不用冻" |
| "和 Swern 完全不同" | 机理类似 | "Kim Swern 兄弟情，硫鎓中间都同行" |

### 12.3 入门例题

**题目**：实验室只有 NCS、DMS 和 Et₃N，没有 (COCl)₂ 和 DMSO，如何氧化 1-丁醇为丁醛？

**引导**：
- 这正是 Corey-Kim 的条件
- NCS + DMS → 活性硫鎓
- 醇进攻 → 消除 → 醛

### 12.4 现实类比

**Corey-Kim 像"微波炉版 Swern"**：
- Swern 是"传统烤箱"——需要精确低温控制
- Corey-Kim 是"微波炉"——同样效果，但更方便快捷

---

## 十三、竞赛拓展

1. **Corey-Kim 在天然产物合成中的应用**：
   - 对热敏感底物的后期氧化
   - 与 Swern 互补使用

2. **其他 NCS 活化的反应**：
   - NCS/Et₃N 体系还可用于氯化反应
   - 与 DMS 组合是特定的氧化路径

---

## 十四、修订记录

- **v1.1（2026-05-10）**：首次创建。基于 ABOC §4.12 Corey-Kim 框架。涵盖 NCS/DMS 硫鎓机理、与 Swern 对比、温和条件优势、操作便利性。Phase C Ch.4 新建 KP。

---

## 十四、外部资料出处

- [待填充]

## 十五、待完善项

- [待填充]
```dataview
TABLE file.name AS "文件名", year AS "年份", type AS "题型", difficulty AS "难度"
FROM "04-题库"
WHERE contains(knowledge_points, "Corey-Kim氧化")
SORT year DESC, difficulty ASC
```
