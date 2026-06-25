---
title: KP复习清单
type: 系统
status: active
updated: 2026-06-15
tags: [系统, 复习, KP, Dataview]
---

# KP复习清单

> 用途：按 `review_cycle` 聚合 `03-知识点/` 中的 KP，给学生侧材料、闪卡与后续 Anki 导出提供最小复习调度入口。
>
> 它只负责“哪些 KP 该按什么周期复习”，不负责闪卡模板、Anki 导入细节或学生反馈闭环本身。
>
> 当前启用口径：
> - `7d`：短周期高频复习
> - `30d`：常规主干复习
> - `90d`：长周期回顾

---

## 推荐入口（先用这里）

| 场景 | 优先入口 | 为什么 |
|---|---|---|
| 想知道这周该复习哪些 KP | 本页 | 这里就是 `review_cycle` 的最小调度入口 |
| 想做闪卡 / 纸质卡 | [[06-学生侧材料/闪卡/README]] | 材料产出和目录组织不在本页维护 |
| 想导出 Anki | [[06-学生侧材料/闪卡/anki-export/README]] | 导出字段、CSV、导入建议都在那边 |
| 想看学生侧整体结构 | [[06-学生侧材料/README]] | 学生侧材料总入口不在本页 |

> 一句话记忆：本页负责“排节奏”，学生侧材料目录负责“放材料”，Anki README 负责“怎么导出”。

---

## 一、总览

```dataview
TABLE
  length(rows) as 总数,
  length(filter(rows, (r) => r.review_cycle = "7d")) as "7d",
  length(filter(rows, (r) => r.review_cycle = "30d")) as "30d",
  length(filter(rows, (r) => r.review_cycle = "90d")) as "90d"
FROM "03-知识点"
WHERE type = "知识点"
  AND review_cycle
```

---

## 二、全部已设置 review_cycle 的 KP

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
SORT review_cycle ASC, importance DESC, updated ASC, file.name ASC
```

---

## 三、7d 短周期复习

> 适合：高频易错、工具型、当课后需要连续刷熟的 KP。

```dataview
TABLE WITHOUT ID
  file.link as KP,
  subject as 学科,
  module as 模块,
  importance as 重要度,
  updated as 最近更新
FROM "03-知识点"
WHERE type = "知识点"
  AND review_cycle = "7d"
SORT importance DESC, updated ASC, file.name ASC
```

---

## 四、30d 常规主干复习

> 适合：大多数主干知识点，作为默认复习档。

```dataview
TABLE WITHOUT ID
  file.link as KP,
  subject as 学科,
  module as 模块,
  importance as 重要度,
  updated as 最近更新
FROM "03-知识点"
WHERE type = "知识点"
  AND review_cycle = "30d"
SORT importance DESC, updated ASC, file.name ASC
```

---

## 五、90d 长周期回顾

> 适合：稳定概念、方法总览、专题结束后的阶段性回顾。

```dataview
TABLE WITHOUT ID
  file.link as KP,
  subject as 学科,
  module as 模块,
  importance as 重要度,
  updated as 最近更新
FROM "03-知识点"
WHERE type = "知识点"
  AND review_cycle = "90d"
SORT importance DESC, updated ASC, file.name ASC
```

---

## 六、使用建议

1. 新授课后优先看 `7d` 清单，抽取闪卡或周内复习材料。
2. 周末复习优先看“本专题相关的 `7d + 30d`”。
3. 专题结束或阶段复盘时，再看 `90d` 做长周期回顾。
4. 若某一类 KP 真实使用中明显“记不住”或“太容易忘”，再把对应条目从 `30d` 调整到 `7d`。
5. 若要继续做成学生可见材料，请从本页跳转到学生侧目录或 Anki 导出说明，不在这里继续堆流程说明。

---

## 七、相关入口

- [[活跃任务/任务卡-KP-review-cycle字段启用方案]]
- [[06-学生侧材料/README]]
- [[06-学生侧材料/闪卡/README]]
- [[06-学生侧材料/闪卡/anki-export/README]]
- [[11-模板/模板-学生闪卡]]
