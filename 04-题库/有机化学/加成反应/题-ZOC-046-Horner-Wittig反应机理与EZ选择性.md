---
title: "题-ZOC-046-Horner-Wittig反应机理与EZ选择性"
type: 题目
source: "Zchem有机反应合成与机理 下册L2"
source_file: "06-外部资料导入/有机反应合成与机理 下/L2TotalSynthesisCaseStudies1[高清]_笔记.md"
source_subject: 有机化学
year: 2023
difficulty: 4
teaching_level: 拓展
knowledge_points: ["[[偶联反应]]"]
status: 已补全答案
syllabus_codes: [48]
tags: [Wittig反应, Horner-Wittig, 烯烃合成, Zchem]
created: 2026-08-27
updated: 2026-08-30
subject_module: 有机化学
pack: 模块习题集
fidelity: 原书改写
exam_stage: 初赛
source_category: 其他类型·自编章节题
source_grade: B-
---

# Horner-Wittig反应机理与EZ选择性

> **来源**：Zchem有机反应合成与机理 下册L2
> **难度**：⭐⭐⭐⭐
> **题目类型**：例题

## 题目

Horner-Wittig反应是经典Wittig反应的改良版本，选择性更好。

**题目**：
1. 画出Horner-Wittig反应的完整机理（膦酸酯 + 强碱 → 烯烃）
2. Horner-Wittig反应相比经典Wittig反应有什么优势？
3. 该反应的E/Z选择性如何？为什么主要生成E型烯烃？
4. 反应中使用tBuOK作为碱的原因是什么？

## 参考答案

题目所用“膦酸酯 + 强碱”写的是 Horner–Wadsworth–Emmons（HWE）反应；狭义的 Horner-Wittig 用二苯基氧化膦负离子，但成烯机理与立体化学判断同构，这里按膦酸酯路线作答。

### 1. 完整机理

以 $(\mathrm{EtO})_{2}\mathrm{P(O)CH_{2}R'}$ 为例：

1. tBuOK 夺取 α-H，生成膦酸酯碳负离子：

$$(\mathrm{EtO})_{2}\mathrm{P(O)CH_{2}R'}\xrightarrow{\mathrm{tBuOK}}(\mathrm{EtO})_{2}\mathrm{P(O)CH^{-}R'}$$

2. 碳负离子亲核进攻醛/酮羰基，生成 β-羟基膦酸酯烷氧负离子。
3. 烷氧负离子分子内进攻 P 原子，关环形成四元环氧膦杂环丁烷（oxaphosphetane）中间体。
4. 该中间体同步消除二乙基磷酸酯负离子并成烯，得到烯烃。

### 2. 相对经典 Wittig 的优势

- 膦酸酯负离子更容易生成、对空气和水更稳定，可用强碱直接去质子。
- 反应后副产物磷酸盐溶于水，后处理远优于三苯基氧化膦。
- 对醛酮活性更高，尤其适用于稳定化的 α-烷氧羰基膦酸酯，产率高、条件温和。
- 可通过膦酸酯 α-取代基、碱与温度精细调控 E/Z 选择性，常规稳化体系给出 E 型为主。

### 3. E/Z 选择性

稳定化膦酸酯（α 位连酯基、氰基等吸电子基）在常规 HWE 条件下主要生成 E 型烯烃。原因是加成/关环过渡态优先采取位阻较小、允许同步消除的取向，P=O 与羰基的排斥及 R 与 α-取代基的空间作用都使 E 更有利；成烯不可逆，产物构型由立体专一的 syn 消除决定。

需要 Z 型时改用 Still–Gennari 条件：氟代膦酸酯（如双(2,2,2-三氟乙基)膦酸酯）加 KHMDS/18-冠-6、低温，以改变过渡态构象，通常得到 Z 型为主的 α,β-不饱和酯。

### 4. 为什么用 tBuOK

tBuOK 碱性足够强，可快速去质子化膦酸酯 α-H 生成碳负离子，但体积大、亲核性弱，不会与酯基或羰基发生竞争性亲核加成，减少副反应。使用它得到的副产物只有 tBuOH，后处理简单，且反应可在 THF/DME 等常用溶剂中进行。对碱敏感底物还可改用 NaH、KHMDS、LDA 或温和的 DBU。
