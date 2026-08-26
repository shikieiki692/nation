---
title: "题-037-5-2-1-HSNO的Lewis结构"
aliases: [37届初赛-5.2.1]
type: 题目
fidelity: 原书逐字
exam_stage: 初赛
year: 2023
exam_date: 2023-09-03
source: "第37届中国化学奥林匹克（初赛）第5题第(5-2-1)小问"
subject: 无机和结构化学
module: 无机和结构化学
submodule: "价键理论"
question_type: 简答题
difficulty: 3
teaching_level: 巩固
syllabus_codes: []
knowledge_points: ["[[Lewis结构式]]", "[[共振论]]", "[[电负性]]"]
tags: [化竞, 真题, 37届, 元素化学]
updated: 2026-05-11
status: 已填充
big_question: "第5题"
subject_module: 结构化学
pack: 模块习题集
---

## 题目

> 关联小问：[[题-037-5-1-NO与H2S反应方程式|5-1]] · [[题-037-5-2-2-HSNO异构体|5-2-2]] · [[题-037-5-2-3-HSSNO酸解离常数|5-2-3]] · [[题-037-5-3-1-Ru配合物结构推断|5-3-1]] · [[题-037-5-3-2-Ru配合物反应方程式|5-3-2]] · [[题-037-5-3-3-d轨道分裂图|5-3-3]]
> 来源：[[mineru/02-真题解析/37届初赛试题解析|37届初赛试题解析]] · [[07-资料提炼/提炼-第37届初赛试题解析|提炼笔记]]

HSNO (A) 表达式给出的原子次序就是其连接方式。画出 A 及其共轭碱 B 的 Lewis 结构式（要求最稳定的形式）。

## 参考答案

**A (HSNO) 的 Lewis 结构**：

$$
\mathrm{H}-\ddot{\mathrm{S}}-\ddot{\mathrm{N}}=\ddot{\mathrm{O}}:
$$

或更准确地表示为：

$$
\mathrm{H}_{\ddot{\mathrm{S}}} \stackrel{\ddot{\mathrm{N}}}{=} \mathrm{O}:
$$

**B ($SNO^{-}$) 的 Lewis 结构**（最稳定形式）：

两种共振极限式均有合理之处：

$$
\ddot{\mathbf{s}}^{-} \!\!\!-\!\!\dot{\mathbf{N}} = \!\!\dot{\mathbf{O}}: \quad :\mathbf{s} = \!\!\dot{\mathbf{N}} - \!\!\ddot{\mathbf{O}}:
$$

**说明**：
- 负电荷位于硫原子上的共振式可能更优：硫原子半径较大，对负电荷的稳定作用较好；且由于硫为第三周期元素，N=S 双键弱于 N=O 双键。
- 但两种共振式均有合理之处，负电荷在 O 上（电负性大）也是合理的。
- $SNO^{-}$ 的最高占据分子轨道主要集中在 S 一侧，反映 S 端亲核性强于 O 端。

## 知识点映射

| 知识点 | 关联程度 | 说明 |
|:---|:---:|:---|
| Lewis结构 | 直接 | 满足八隅律的结构式 |
| 共振论 | 直接 | SNO⁻的多种共振极限式 |
| 电负性 | 直接 | 判断负电荷的稳定位置 |
| 原子半径 | 间接 | S半径大，可更好稳定负电荷 |

## 解题思路

1. **确定原子连接方式**：HSNO按原子次序连接为 H-S-N-O。
2. **画HSNO的Lewis结构**：S连H和N，N连S和O（双键），满足八隅律。
3. **确定共轭碱**：HSNO失去H⁺得SNO⁻。
4. **判断最稳定形式**：考虑负电荷在S或O上的稳定性。
5. **写出共振式**：两种主要共振极限式均应画出。

## 易错分析

- **连接方式错误**：题目明确原子次序即连接方式，不能写成H-N-S-O等。
- **忽略共振**：只画一种结构，未考虑共振。
- **八隅律不满足**：确保所有原子（除H外）满足八隅体。

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
