---
title: KP review_cycle 字段启用方案
type: 活跃任务卡
status: completed
priority: P1
area: 知识库系统
owner: Agent
created: 2026-06-03
updated: 2026-06-13
completed: 2026-06-13
source_notes: "[[00-首页/工作日志/2026-06-03]]"
related_notes:
  - "[[00-首页/工作日志/2026-06-03]]"
  - "[[00-首页/活跃任务/任务卡-Anki-CSV导出工作流建立]]"
evidence:
  - "[[00-首页/工作日志/2026-06-03]]"
  - "[[00-首页/KP复习清单]]"
  - "[[00-首页/活跃任务/任务卡-Anki-CSV导出工作流建立]]"
---

# KP review_cycle 字段启用方案

确认字段覆盖、用途和最小落地路径，支撑闪卡 / Anki 闭环。

## 结论

`review_cycle` 值得启用，但不做“全库精细化排程”，先落成一个**最小可执行方案**：

1. 只定义 3 档节奏：`7d / 30d / 90d`
2. 先服务 2 个下游：
   - `06-学生侧材料/` 的复习清单
   - 后续 `Anki CSV` 导出字段映射
3. 先以“字段可查询、可分流、可导出”为完成标准，不追求一次性把 714 个 KP 全部重新分档

---

## 一、字段用途

### 1.1 在知识库层的作用

- 给每个 KP 一个**推荐复习节奏**
- 让 `03-知识点/` 不只描述“知识是什么”，还能描述“多久值得复习一次”
- 为学生侧材料提供最小调度信息，避免闪卡 / 练习卷 / Anki 完全靠人工挑选

### 1.2 在学生侧材料层的作用

- 用于从 KP 中筛出“本周该复习什么”
- 用于区分：
  - 高频短周期复习内容
  - 常规主干内容
  - 长周期回顾内容
- 与 [[11-模板/模板-学生闪卡]] 中的 Leitner 盒子法口径对齐

### 1.3 在 Anki 层的作用

- 不直接替代 Anki 算法
- 作为**初始标签 / 初始 deck / 初始复习策略分流字段**
- 让导出的 CSV 至少带有“这张卡属于短周期还是长周期复习”的信息

---

## 二、最小分档规则

### 2.1 三档定义

| 档位 | 含义 | 适用对象 |
|:---|:---|:---|
| `7d` | 短周期高频复习 | 高错率、工具型、需要连续刷熟的 KP |
| `30d` | 常规主干复习 | 大多数主干知识点 |
| `90d` | 长周期回顾 | 稳定概念、方法总览、低频但重要的条目 |

### 2.2 判定口径

`7d`
- 当课就要反复调用
- 易错且遗忘快
- 属于“工具类 / 判据类 / 高频套路类”

`30d`
- 一般主干知识点默认档
- 理解后仍需周期回顾，但不需要周周刷

`90d`
- 结构性总览、方法学总览、成熟稳定概念
- 更适合专题结束后做阶段性回顾

### 2.3 默认规则

- 未特殊判定时，默认保留 `30d`
- 不做空值启用；没有明确理由时不新增第四档、第五档
- 若后续真实课堂反馈表明某类内容遗忘更快，再单点改成 `7d`

---

## 三、首批启用范围

### 3.1 暂不做的事

- 不立即全库重标 714 个 KP
- 不追求所有学科都同时精细化
- 不先做复杂的“按学生个体动态改周期”

### 3.2 先做的范围

优先针对以下内容启用：

1. 第一轮 / 第二轮正在实际使用的核心 KP
2. 已经要产出闪卡或策略卡的专题
3. 工具型、高频调用型 KP
4. 已有明显周期差异的条目
   - 例如 `乙酰乙酸乙酯合成法`、`炔负离子`、`羧酸`、`醇` 这类已出现 `90d` 的条目

---

## 四、Dataview 最小落地

### 4.1 目标

先在 Obsidian 内得到一个**可直接看的复习清单**，而不是先做脚本。

### 4.2 推荐查询

```dataview
TABLE WITHOUT ID
  file.link as KP,
  subject as 学科,
  module as 模块,
  review_cycle as 复习周期,
  importance as 重要度,
  updated as 最近更新
FROM "03-知识点"
WHERE type = "知识点"
  AND review_cycle
SORT review_cycle ASC, importance DESC, updated ASC
```

### 4.3 按档查看

```dataview
TABLE WITHOUT ID
  file.link as KP,
  module as 模块,
  importance as 重要度
FROM "03-知识点"
WHERE type = "知识点"
  AND review_cycle = "7d"
SORT importance DESC, file.name ASC
```

```dataview
TABLE WITHOUT ID
  file.link as KP,
  module as 模块,
  importance as 重要度
FROM "03-知识点"
WHERE type = "知识点"
  AND review_cycle = "30d"
SORT importance DESC, file.name ASC
```

```dataview
TABLE WITHOUT ID
  file.link as KP,
  module as 模块,
  importance as 重要度
FROM "03-知识点"
WHERE type = "知识点"
  AND review_cycle = "90d"
SORT importance DESC, file.name ASC
```

### 4.4 使用方式

- 新授课后：优先看 `7d`
- 周复习：看 `7d + 本专题相关 30d`
- 专题结束后：看 `90d` 做阶段汇总

---

## 五、Anki CSV 最小映射

### 5.1 映射原则

`review_cycle` 不直接控制 Anki 的真实复习间隔，而是先作为导出字段与标签：

| KP 字段 | Anki 对应 | 用途 |
|:---|:---|:---|
| `file.name` | `note_id` / 卡片标题 | 主标识 |
| `review_cycle` | `tags` / `deck_hint` | 初始分流 |
| `subject` | `tags` | 学科标签 |
| `module` | `tags` | 模块标签 |
| `importance` | `tags` | 高优卡片筛选 |

### 5.2 推荐标签口径

- `rc_7d`
- `rc_30d`
- `rc_90d`

例如一张卡可以带：

`organic rc_7d module_机理基础 importance_5`

### 5.3 初始 deck 建议

- `Chem::Weekly` ← `7d`
- `Chem::Core` ← `30d`
- `Chem::Review` ← `90d`

这只是导入时的初始分流，之后仍由 Anki 自己排程。

---

## 六、完成标准

本任务的“最小完成”定义为：

- [x] 明确 `review_cycle` 的用途
- [x] 明确三档分档规则：`7d / 30d / 90d`
- [x] 明确 Dataview 复习清单查询口径
- [x] 明确 Anki CSV 的最小映射方式
- [x] 产出一个实际可用的复习清单页面
- [ ] 与 `任务卡-Anki-CSV导出工作流建立` 完成字段对接

---

## 已落地产物

- [[00-首页/KP复习清单]]

### 当前落地情况

- 已建成按 `review_cycle` 聚合的 Dataview 复习页面
- 已包含：
  - 总览统计
  - 全部已设置 `review_cycle` 的 KP 列表
  - `7d / 30d / 90d` 三档复习视图
- 已挂入：
  - [[首页]]
  - [[06-学生侧材料/README]]
  - [[Agent模块关系与收工同步清单]]

> 当前阶段可视为“最小可执行落地已完成”；后续重点转向：
> 1. `review_cycle` 分档抽样校正
> 2. 与 `Anki CSV` 导出任务对接

## 收尾说明（2026-06-13）

- 已将当前发现的异常 `review_cycle` 值收口回三档口径：`7d / 30d / 90d`
- 本卡按“最小可执行方案已落地”标准关闭
- 后续 `Anki CSV` 的字段映射与导出对接，转由 [[00-首页/活跃任务/任务卡-Anki-CSV导出工作流建立]] 继续承接

---

## 七、后续动作

1. 抽样检查高频有机 / 第一二轮核心 KP 的 `review_cycle` 是否需要从默认 `30d` 调整到 `7d` 或 `90d`
2. 在 Anki CSV 导出任务中，正式加入 `review_cycle -> tags/deck_hint` 映射

## 当前判断

该字段**有用**，但价值不在“字段存在”，而在“它能驱动复习清单与导出分流”。
因此当前最合理的启用方式不是继续讨论字段本身，而是让它先服务 `Dataview 复习清单 + Anki 标签映射` 这两个最小下游。
