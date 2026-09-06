---
title: "题-有机-立体-手性分子RS构型判断"
type: 题目
fidelity: 自编
submodule: 立体化学与区域选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["25"]
knowledge_points:
  - "[[手性中心]]"
concepts:
  - R/S构型标记
tags: [化竞, 题目, 有机化学, 第三轮]
updated: 2026-06-06
aliases: ["题-有机-立体-02"]
source: "专题页提炼"
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 其他类型·自编章节题
---
# 手性分子 R/S 构型判断

## 题目

用 Cahn-Ingold-Prelog (CIP) 顺序规则判断下列化合物的 R/S 构型，并简要说明判断过程。

**(1)** (S)-2-氯丁烷：判断下列 Fischer 投影式对应的实际构型是否为 S？

```
    CH3
     |
  Cl—C—H
     |
   C2H5
```

**(2)** 给出下列化合物的 C2 和 C3 的绝对构型（R 或 S）：

$$
\mathrm{HOCH_2\!-\!CHOH\!-\!CHOH\!-\!CHO}
$$

即 2,3-二羟基丁醛（赤藓糖或苏阿糖，仅需给出一般判断方法）。

**(3)** 2-溴-2-氯-1,1,1-三氟乙烷是否具有手性？是否有 R/S 构型之分？


![[chiral-center.png]]

## 参考答案

### (1) 2-氯丁烷的 R/S 判断

Fischer 投影式：竖线朝向纸面后方，横线朝向纸面前方。

CIP 优先级排序（按原子序数）：
- $\mathrm{Cl}$ (Z=17) > $\mathrm{C_2H_5}$ (直接连接 C, Z=6) > $\mathrm{CH_3}$ (直接连接 C, Z=6) > $\mathrm{H}$ (Z=1)
- $\mathrm{C_2H_5}$ 与 $\mathrm{CH_3}$ 需进一步比较：乙基的第二个原子是 C，甲基的第二个原子是 H,H,H，乙基优先。

优先级顺序：$\mathrm{Cl > C_2H_5 > CH_3 > H}$。

在 Fischer 投影式中，将最低优先级基团（H）放在竖线上（远离观察者），观察 Cl → C2H5 → CH3 的旋转方向。

如果 H 在横线上，需进行"交换法"处理：将 H 与竖线上的基团交换（同时交换另外两个基团以保持构型不变），或使用"反转规则"（直接观察的方向反转就是正确构型）。

对于给出的 Fischer 投影式，H 在横线上（朝向观察者）。此时：
- 观察 Cl → C2H5 → CH3 的顺序，若为顺时针，实际构型为 S；若为逆时针，实际构型为 R。

此处 Cl → C2H5 → CH3 为顺时针，但因 H 朝向观察者，反转：**实际构型为 S**。

### (2) 2,3-二羟基丁醛的 C2 和 C3 构型

CIP 优先级规则：
- 对于 C2：$\mathrm{OH}$ (Z=8) > $\mathrm{CHO}$ (O,O,H, 即 O 碰 O 平手，继续比较) > $\mathrm{CHOHCH_2OH}$ (O,C,H) > $\mathrm{H}$
  - $\mathrm{CHO}$ 的下一步：O,O,H（两个 O）
  - $\mathrm{CHOHCH_2OH}$ 的下一步：O,C,H（一个 O）
  - 因此：$\mathrm{OH > CHO > CH(OH)CH_2OH > H}$

- 对于 C3：$\mathrm{OH}$ (Z=8) > $\mathrm{CH_2OH}$ (O,H,H) > $\mathrm{CHOHCHO}$ (O,C,H) > $\mathrm{H}$

具体 R/S 取决于各手性中心的绝对构型（需在三维结构中确定）。本题主要考查 CIP 规则的正确应用，即比较直接连接原子 → 若相同再比较下一层原子 → 双键/三键按重复原子处理。

### (3) 2-溴-2-氯-1,1,1-三氟乙烷 $\mathrm{CF_3CBrClH}$

结构分析：中心碳 C2 连接四个基团——$\mathrm{H}$、$\mathrm{Br}$、$\mathrm{Cl}$、$\mathrm{CF_3}$。四个基团各不相同，C2 为手性中心。

CIP 排序：$\mathrm{Br}$ (Z=35) > $\mathrm{Cl}$ (Z=17) > $\mathrm{CF_3}$ (F,F,F 等效于 C 连接三个 F) > $\mathrm{H}$ (Z=1)。

**该分子具有手性**，存在一对对映异构体，可以标记 R/S 构型。

### 方法总结

**CIP 规则判断 R/S 的核心步骤：**
1. 按原子序数排列与手性中心直接连接的四个原子的优先顺序；
2. 若有相同原子，比较下一层原子，直到分出先后；
3. 双键/三键按连接重复原子处理（如 $\ce{C=O}$ 视为 C 连接两个 O）；
4. 将最低优先级基团放在远离观察者的位置；
5. 观察余下三个基团的优先顺序旋转方向：顺时针为 R，逆时针为 S；
6. 若最低优先级基团朝向观察者（如 Fischer 投影式中在横线上），则观察结果反转。

## 知识点映射

- [[手性中心]]
- R/S构型标记