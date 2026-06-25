---
title: Anki CSV 导出工作流建立
type: 活跃任务卡
status: completed
priority: P3
area: 学生侧材料
owner: Agent
created: 2026-06-03
updated: 2026-06-13
completed: 2026-06-13
source_notes: [[00-首页/工作日志/2026-06-03]]
related_notes: [[00-首页/工作日志/2026-06-03]], [[11-模板/模板-学生闪卡]], [[00-首页/KP复习清单]]
evidence: [[00-首页/工作日志/2026-06-03]], [[06-学生侧材料/闪卡/anki-export/README]]
---

# Anki CSV 导出工作流建立

建立从 Obsidian / KP 到 Anki 的批量导出流程。

## 结论

已完成最小可执行版本：

1. 基于 `03-知识点/` 全量扫描 KP
2. 读取 `review_cycle` 并映射到初始 deck / tag
3. 按固定章节导出三类卡：
   - `定义` -> 概念卡
   - `关键结论` -> 总结卡
   - `易错点` -> 易错点卡
4. 自动跳过 `待填充` 占位内容
5. 已产出真实 CSV 与样例 CSV，可直接用于 Anki 导入测试

## 已落地产物

- `export_anki_csv.js`
- [[06-学生侧材料/闪卡/anki-export/README]]
- `06-学生侧材料/闪卡/anki-export/anki-kp-cards.csv`
- `06-学生侧材料/闪卡/anki-export/anki-kp-cards-sample.csv`

## 字段映射

| 导出字段 | 来源 | 用途 |
|:---|:---|:---|
| `Front` | KP 固定章节 | 卡片正面 |
| `Back` | KP 固定章节 | 卡片背面 |
| `Tags` | `subject / module / submodule / title / review_cycle` | 检索与筛选 |
| `Deck` | `review_cycle` | 初始导入分流 |
| `Source` | `title` | 回溯源 KP |
| `ReviewCycle` | `review_cycle` | 保留原始周期 |
| `NoteType` | 章节类型 | 区分卡片类型 |
| `Extra` | 互补章节 | 补充说明 |

## 当前映射口径

- `7d -> Chem::Weekly`
- `30d -> Chem::Core`
- `90d -> Chem::Review`

对应标签：

- `rc_7d`
- `rc_30d`
- `rc_90d`

## 收尾说明（2026-06-13）

- 当前工作流已能稳定输出首版可导入 CSV
- 首版目标是“可用”，不是“最佳卡面质量”
- 更复杂的能力留作后续增强项处理

## 后续增强项

1. 加入专题页对比卡 / 信号卡导出
2. 加入 `importance` / `difficulty` 标签
3. 优化公式显示与 LaTeX 清洗
4. 为第三轮有机专题加入 Image Occlusion / cloze 路径
