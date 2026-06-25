---
title: 自动汇总-KP库存统计
type: 系统
role: 自动库存汇总
tags: [系统, 自动汇总, KP库存]
updated: 2026-06-13
---

# 自动汇总 · KP库存统计

> 本页只汇总知识点库存和图片覆盖率。
> 阶段判断、完成度解读和“下一步做什么”不在本页维护。

## 知识点库存

```dataview
TABLE
  length(rows) AS 知识点数,
  length(filter(rows, (r) => r.status = "已填充")) AS "✅ 已填充",
  length(filter(rows, (r) => r.status = "初稿")) AS "📝 初稿",
  length(filter(rows, (r) => r.status = "骨架")) AS "🔶 骨架",
  round(length(filter(rows, (r) => r.status = "已填充")) / length(rows) * 100, 1) + "%" AS 完成率
FROM "03-知识点"
WHERE type = "知识点"
GROUP BY subject
SORT 完成率 DESC
```

## 图片覆盖率

```dataview
TABLE
  length(rows) AS 总数,
  length(filter(rows, (r) => r.has_images = true)) AS "✅ 已配图",
  length(filter(rows, (r) => r.images_priority = "high" AND r.has_images != true)) AS "🔴 高优待补",
  length(filter(rows, (r) => r.images_priority = "medium" AND r.has_images != true)) AS "🟡 中优待补"
FROM "03-知识点"
WHERE type = "知识点"
GROUP BY subject
SORT 总数 DESC
```
