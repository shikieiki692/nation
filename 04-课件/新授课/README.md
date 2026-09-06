---
title: 新授课目录
type: 索引
subject: 系统
module: 课件体系
tags: [化竞, 课件, 新授课]
updated: 2026-05-20
---

# 新授课目录

> 新授课课件存放处。
>
> **生成方式**：[[Agent提示词-知识库使用]] Agent 10（备课 Agent）→ 选择 `lesson_type: 新授课`。

---

## 现有课件

```dataview
TABLE
  subject as 模块,
  audience_level as 层次,
  duration as 时长,
  start_date as 授课日期,
  file.mtime as 修改时间
FROM "04-课件/新授课"
WHERE lesson_type = "新授课"
SORT start_date DESC
```

---

## 快捷入口

- **模板**：[[模板-新授课]]
- **最近复盘**：[[../复盘索引]]
