# Agent 执行规范

## MCP Server

本 vault 配备 KB Vault MCP Server（`kb-vault-mcp/`），提供 12 个 kb_* 工具。**原生 Read/Write/Edit/Bash 已禁用**，所有文件操作必须通过 MCP 工具。

### 启动流程

1. `kb_session init` — 初始化或恢复会话
2. `kb_gate action=create` — 创建 Task 实例
3. `kb_gate action=confirm` — 确认计划，进入 EXECUTING
4. `kb_write` / `kb_edit` / `kb_move` / `kb_delete` — 文件操作（自动状态检查）
5. `kb_gate action=verify` → `action=close` → `action=archive` — 完成归档

### 关键约束

- `kb_write` 在 ASSESSING 或 PLANNING 状态调用会被拒绝（TASK_NOT_EXECUTING）
- USE 类型 Task 写入 03-知识点/ 会被拒绝（USE_CANNOT_WRITE_KP）
- `kb_move` 会检查反向引用，有引用则阻断
- 每 10 次文件操作自动写检查点（`checkpoint.jsonl`）

### 设计文档

`00-首页/Agent生命周期与MCP工具层设计.md` — 完整架构文档（Session/Task 状态机、钩子系统、MCP 工具规范）

## 工作目录

```bash
cd product-merge && claude -p "..."
```
