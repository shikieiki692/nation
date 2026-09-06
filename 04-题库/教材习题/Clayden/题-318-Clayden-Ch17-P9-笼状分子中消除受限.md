---
title: 题-318-Clayden-Ch17-P9-笼状分子中消除受限
type: 题目
fidelity: 原书逐字
submodule: 消除反应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
question_type: [简答]
teaching_level: 竞赛
syllabus_codes: ["3.2"]
knowledge_points: ["[[E2反应]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch17-P9]
source: Clayden Organic Chemistry 2nd Ed. Chapter 17 Problem 9
cross_references: ["[[题-317-Clayden-Ch17-P8-环己基溴E2困难和构象变化]]", "[[题-310-Clayden-Ch17-P1-两个消除反应机理]]", "[[题-294-Clayden-Ch14-P4-四个化合物立体化学讨论]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
---
# 题-318: 笼状分子中消除受限

## 题目

**【中文】**只有其中一个溴化物消除生成烯烃A。为什么？两个烯烃都不消除生成烯烃B。为什么？

**【原文】**
Only one of these bromides eliminates to give alkene A. Why? Neither alkene eliminates to give alkene B. Why not?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/2ea55eec559ad4d1bc7e55e5c067fa0e221b583565d1c16d9be561e0eeb7cc2e.jpg]]

## 参考答案

**Answer (English)**:

The first molecule has one H antiperiplanar to the Br atom so elimination can occur. The second has no hydrogens antiperiplanar to Br. Alkene B is a bridgehead alkene and cannot exist (see the textbook, pp. 389–390).

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/5adf006b43e676954dc910a5f911464d29e912368e6d44ef0280d31e93a288bf.jpg]]

**中文解析**：

**Bredt规则**：

Bredt规则是有机化学中关于桥环化合物的重要规则：

> **在桥环体系中，桥头碳不能形成双键（除非环足够大，通常≥8元环）。**

**为什么桥头碳不能有双键？**

- 双键要求碳原子为sp²杂化，所有相连原子共平面
- 在桥环体系中，桥头碳的几何约束使其无法达到平面结构
- 小环（<8元环）的桥头双键会产生极大的环张力
- 因此，桥头双键是不稳定的，不能形成

**问题1：消除可能**

```
    H
     \
      C---C---Br
     /     \
    (笼状骨架)
```

- 存在一个H与Br处于反式共平面位置
- E2可以发生
- 形成的双键不在桥头位置
- Bredt规则不适用
- 消除产物稳定

**问题2：消除不可能**

**情况A：没有反式共平面的H**
```
    H (不在反式位置)
     \
      C---C---Br
     /     \
    (笼状骨架)
```

- 没有H与Br处于反式共平面
- E2的立体化学要求无法满足
- 即使环翻转也无法达到反式共平面
- E2无法发生

**情况B：消除会形成桥头双键**
```
    H
     \
      C---C---Br
     /     \
    (笼状骨架，Br在桥头)
```

- 唯一可能的消除会在桥头形成双键
- Bredt规则禁止这种情况
- 桥头双键在小环中极不稳定
- 消除不可能发生

**Bredt规则的例外**：
- 大环体系（≥8元环）：桥头双键可以存在
- 例如：[4.4.1]体系的桥头烯烃是稳定的

**消除可能性判断流程**：

| 检查项 | 可能 | 不可能 |
|--------|------|--------|
| 反式共平面H | 有 | 无 |
| 产物双键位置 | 非桥头 | 桥头（Bredt规则） |
| 环大小 | ≥8元环（例外） | <8元环 |

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| E2反应 | E2的反式共平面要求 | 直接 |
| [[Bredt规则]] | 桥头双键的限制 | 直接 |
| [[消除反应]] | 笼状分子中的消除限制 | 间接 |

## 解题思路

1. **读题定位**：笼状分子中的E2消除，需要检查反式共平面和Bredt规则
2. **🔑 关键转换**：反式共平面H存在？→ 是→检查产物是否为桥头双键→否→消除可能
3. **验证**：画出可能的消除产物，检查是否违反Bredt规则

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为所有笼状分子都不能消除 | 没有区分具体情况 | 需要检查反式共平面和产物结构 | 如何判断桥头双键是否违反Bredt规则？ |
| 忽略Bredt规则 | 只考虑了反式共平面要求 | Bredt规则是额外的限制条件 | 为什么大环（≥8元环）可以有桥头双键？ |
| 混淆反式共平面和Bredt规则 | 没有理解两个规则的独立性 | 反式共平面是E2的必要条件，Bredt规则是产物稳定性的限制 | 什么情况下两个规则都会阻止消除？ |