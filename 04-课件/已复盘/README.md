---
title: 已复盘课件归档说明
type: 索引
updated: 2026-06-29
---

# 已复盘课件归档

## 归档规则

1. **何时归档**：某课件授课后，根据实际教学反馈完成复盘记录，即可移入本目录
2. **文件命名**：`<日期>-<主题>-<班型>-复盘.md`
3. **frontmatter 要求**：
   ```yaml
   ---
   title: <主题>复盘
   type: 复盘
   lesson_type: 新授课 / 复习课 / 习题课
   lesson_date: YYYY-MM-DD
   audience_level: 基础班 / 提高班 / 决赛班
   duration_planned: 45
   duration_actual: 45
   referenced_lesson: "[[<原课件路径>]]"
   ---
   ```
4. **复盘内容结构**：
   - 一、预设 vs 实际对比
   - 二、学生反馈摘要
   - 三、知识库改进点（关联到具体 KP）
   - 四、下次迭代建议

---

*空目录占位文件。删除本文件不会影响 Dataview 查询，但建议保留作为归档入口。*
