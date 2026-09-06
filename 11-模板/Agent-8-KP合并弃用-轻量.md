---
title: Agent 8 · KP合并弃用
type: agent-prompt-lightweight
agent_id: 8
updated: 2026-06-29
version: v1.0
tags: [agent, 维护]
---

# Agent 8 · KP合并弃用（轻量版）

## 一句话定位
重复 KP 合并；过时 KP 软弃用。

## 何时使用
- 发现重复 KP（如"Lawesson试剂"和"Lawesson 试剂"）
- 决定弃用某 KP
- Agent 9 健康检查发现重复/孤立 KP

## 核心输入（必填）
| 参数 | 说明 |
|------|------|
| 模式 | 合并 / 弃用 |
| source_kps | 被合并/弃用的 KP 列表 |
| target_kp | 合并模式下保留的主 KP |
| reason | 弃用原因（弃用模式必填） |

## 执行流程（4步）
1. **读取全文**：Read 所有涉及 KP
2. **Grep 反向引用**：列出所有引用被合并/弃用 KP 的文件
3. **生成计划**：差异对照表 + 合并迁移计划，提交用户确认（≥5文件批量改动必须）
4. **执行**：内容融合→更新反向引用→软弃用 source（移入 08-待审核区/弃用归档/ + 加 deprecated + 7天缓冲）

## 完成定义（DoD）
- [ ] 所有反向引用已更新（再 Grep 一次确认 source KP 名不再出现）
- [ ] target KP 的 frontmatter 已合并 aliases
- [ ] target KP 的 status 是"已填充"
- [ ] 弃用归档文件名带日期前缀
- [ ] 工作日志已记录

## 边界（不做的事）
- 不跳过用户确认直接合并（严重违规）
- 不直接 rm 文件（必须软弃用+7天缓冲）
- 不反向引用没改完就先归档 source
- 不丢失 source 的独有内容

## 快速命令
```
用"KP合并弃用 Agent"合并 [[{source}]] 到 [[{target}]]
```
