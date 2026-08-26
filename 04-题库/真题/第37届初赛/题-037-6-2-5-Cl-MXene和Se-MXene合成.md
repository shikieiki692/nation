---
title: "题-037-6-2-5-Cl-MXene和Se-MXene合成"
aliases: [37届初赛-6.2.5]
type: 题目
fidelity: 原书逐字
exam_stage: 初赛
year: 2023
exam_date: 2023-09-03
source: "第37届中国化学奥林匹克（初赛）第6题第(6-2-5)小问"
subject: 无机和结构化学
module: 无机和结构化学
submodule: "元素化学"
question_type: 方程式书写题
difficulty: 3
teaching_level: 巩固
syllabus_codes: []
knowledge_points: ["[[氧化还原反应]]", "[[氧化还原反应方程式配平]]", "[[材料化学]]"]
tags: [化竞, 真题, 37届, 元素化学]
updated: 2026-05-11
status: 已填充
big_question: "第6题"
subject_module: 有机化学
pack: 模块习题集
---

## 题目

> 关联小问：[[题-037-6-1-MAX相通式推导|6-1]] · [[题-037-6-2-1-Ti3AlC2晶胞组成|6-2-1]] · [[题-037-6-2-2-层间距计算|6-2-2]] · [[题-037-6-2-3-碳原子坐标|6-2-3]] · [[题-037-6-2-4-MXene合成方程式|6-2-4]] · [[题-037-6-2-6-F-MXene反应性分析|6-2-6]]
> 来源：[[mineru/02-真题解析/37届初赛试题解析|37届初赛试题解析]] · [[07-资料提炼/提炼-第37届初赛试题解析|提炼笔记]]

T-MXene 的性质与端基 T 密切相关。利用熔融 $ZnCl_{2}$ 与 $Ti_{x}Al_{y}C_{z}$ 在 $550^{\circ}\mathrm{C}$ 反应 5 h，可以得到 Cl 为端基的 Cl-MXene（反应 3）。将 Cl-MXene 在 CsCl-KCl-LiCl 混合熔盐与 Li₂Se 反应 18 h，可以得到端基为 Se 的 Se-MXene（反应 4）。写出反应 3 和 4 的化学方程式。

## 参考答案

**反应 3**（熔融 $ZnCl_{2}$ 刻蚀制备 Cl-MXene）：

$$
2\mathrm{Ti}_{3}\mathrm{AlC}_{2} + 5\mathrm{ZnCl}_{2} \longrightarrow 2\mathrm{Ti}_{3}\mathrm{C}_{2}\mathrm{Cl}_{2} + 5\mathrm{Zn} + 2\mathrm{AlCl}_{3}
$$

或（考虑 $AlCl_{3}$ 在熔融 $ZnCl_{2}$ 中形成 $Zn[AlCl_{4}]_{2}$）：

$$
2\mathrm{Ti}_{3}\mathrm{AlC}_{2} + 6\mathrm{ZnCl}_{2} \longrightarrow 2\mathrm{Ti}_{3}\mathrm{C}_{2}\mathrm{Cl}_{2} + 5\mathrm{Zn} + \mathrm{Zn}[\mathrm{AlCl}_{4}]_{2}
$$

**反应 4**（端基置换制备 Se-MXene）：

$$
\mathrm{Ti}_{3}\mathrm{C}_{2}\mathrm{Cl}_{2} + \mathrm{Li}_{2}\mathrm{Se} \longrightarrow \mathrm{Ti}_{3}\mathrm{C}_{2}\mathrm{Se} + 2\mathrm{LiCl}
$$

**说明**：
- 反应 3 为固相熔融体系的氧化还原反应，$ZnCl_{2}$ 既作刻蚀剂又作氧化剂。
- 反应 4 为端基置换反应，$Se^{2-}$ 是 -2 价阴离子，而 $Cl^{-}$ 是 -1 价阴离子，结合比例不同（Se 与 MXene 片层结合比例为 1:1，Cl 为 2:1）。

## 知识点映射

| 知识点 | 关联程度 | 说明 |
|:---|:---:|:---|
| 氧化还原反应 | 直接 | Zn²⁺被还原为Zn，Al被氧化 |
| 熔盐化学 | 直接 | 高温熔融体系中的反应 |
| 端基置换 | 直接 | Cl被Se²⁻取代 |
| 电荷平衡 | 直接 | 不同价态端基的结合比例 |

## 解题思路

1. **分析反应 3**：熔融$ZnCl_{2}$刻蚀MAX相，选择性去除Al，同时Cl端基功能化。
2. **确定氧化还原**：$Zn^{2+}$被还原为Zn，Al被氧化为$Al^{3+}$。
3. **配平反应 3**：根据电子守恒和原子守恒配平。
4. **分析反应 4**：Cl-MXene与$Li_{2}Se$发生端基置换。
5. **注意结合比例**：$Se^{2-}$（-2价）与$Cl^{-}$（-1价）结合比例不同。

## 易错分析

- **产物形式错误**：$AlCl_{3}$在熔融$ZnCl_{2}$中可形成$Zn[AlCl_{4}]_{2}$，两种写法均合理。
- **端基比例错误**：Se-MXene为$Ti_{3}C_{2}Se$（不是$Ti_{3}C_{2}Se_{2}$）。
- **忽略熔盐条件**：反应3和4均在熔盐中进行，不是水溶液。

## 🔗 同大题小问

```dataviewjs
const name = dv.current().file.name;
const m = name.match(/^(题-\d+b?-\d+-)\d+-/);
if (m) {
  const prefix = m[1];
  const pages = dv.pages('"04-题库/真题"')
    .where(p => p.file.name.startsWith(prefix) && p.file.name !== name)
    .sort(p => parseInt(p.file.name.match(/-(\d+)-/)[1]));
  if (pages.length) {
    dv.header(4, "🔗 同大题小问（按序）");
    dv.list(pages.map(p => p.file.link));
  }
}
```
