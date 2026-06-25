# KB Vault MCP Server - Stateful Implementation

基于设计文档实现的**有状态** MCP Server，在内存中维护 Session 和 Task 状态机，所有修改文件的工具调用时**隐式验证** Task 状态。

## 核心特性

### 1. 有状态架构

MCP Server 在内存中维护运行时状态：
- **Session**: 会话生命周期容器
- **Task**: 工作单元状态机
- **ReadRegistry**: 文件指纹缓存
- **DirtyModules**: 脏模块追踪

### 2. 隐式验证链

所有修改文件的工具（kb_write/kb_edit/kb_move/kb_delete）调用时**自动执行**以下验证：

```
1. Session 存在且状态为 ACTIVE？
   → 否 → 返回 NO_ACTIVE_SESSION

2. 当前有活跃 Task？
   → 否 → 返回 NO_ACTIVE_TASK

3. Task.state ∈ { EXECUTING, VERIFYING }？
   → 否 → 返回 TASK_NOT_EXECUTING

4. intentType 允许此操作？
   → USE 写入 03-知识点/ → 返回 USE_CANNOT_WRITE_KP
```

### 3. 状态机强制

Agent 无法绕过状态机——不调用 kb_gate 就无法写文件。

## 工具列表

| 工具 | 功能 | 状态检查 |
|:---|:---|:---|
| `kb_read` | 指纹比对读取 | ❌ 不检查 |
| `kb_write` | 冲突检测写入 | ✅ 隐式验证 |
| `kb_edit` | old_string 唯一性验证 | ✅ 隐式验证 |
| `kb_bash` | 只读白名单 | ❌ 不检查 |
| `kb_session` | 会话生命周期管理 | — |
| `kb_gate` | 状态迁移确认点 | — |
| `kb_dirty` | 脏模块管理 | — |

## 状态流转

```
kb_session init
  → Session.state = ACTIVE
  → 若有检查点 → 恢复 Task 树到内存

kb_gate phase=0
  → 创建 Task 实例 → Task.state = ASSESSING

kb_gate phase=1
  → 确认计划 → Task.state = PLANNING → EXECUTING

Agent 调用 kb_write/kb_edit
  → MCP Server 内部自动验证:
    ✓ Session ACTIVE
    ✓ Task EXECUTING
    ✓ intentType 允许
  → 执行写入 + 标脏模块

kb_gate phase=4
  → Task.state = ARCHIVED

kb_session clear
  → 清理内存状态
```

## 安装

```bash
cd kb-vault-mcp
pnpm install
pnpm build
```

## 测试

```bash
cd kb-vault-mcp
pnpm test
```

测试覆盖：
- ✅ 状态机强制机制（NO_ACTIVE_SESSION, NO_ACTIVE_TASK, TASK_NOT_EXECUTING）
- ✅ USE 意图约束（USE_CANNOT_WRITE_KP）
- ✅ kb_read 不检查状态
- ✅ kb_bash 不检查状态
- ✅ kb_edit 唯一性验证
- ✅ 脏模块报告

## 配置

### `.claude/mcp.json`

```json
{
  "mcpServers": {
    "kb-vault": {
      "command": "node",
      "args": ["kb-vault-mcp/dist/index.js"],
      "env": {
        "KB_VAULT_ROOT": "${workspaceFolder}"
      }
    }
  }
}
```

### `.claude/settings.json`

```json
{
  "permissions": {
    "allow": ["kb_read", "kb_write", "kb_edit", "kb_bash", "kb_session", "kb_gate", "kb_dirty"],
    "deny": ["Read", "Write", "Edit", "Bash"]
  }
}
```

## 设计文档

- 主设计：`H:\妙妙屋\00-首页\Agent生命周期与MCP工具层设计.md`
- 追加修正：`H:\妙妙屋\00-首页\设计修正-状态机强制机制.md`

## 关键技术实现

### 1. 内存状态管理

```typescript
class StateManager {
  private session: Session | null = null;
  private tasks: Map<string, Task> = new Map();
  
  validateModification(operation: string, targetPath?: string): ValidationError | null {
    // 隐式验证链
  }
}
```

### 2. 原子检查点

所有状态变更时**原子增量写入** `checkpoint.json`。进程重启时从检查点恢复。

### 3. 状态迁移验证

```typescript
private isValidStateTransition(from: TaskState, to: TaskState): boolean {
  const validTransitions = {
    'ASSESSING': ['PLANNING', 'ERROR'],
    'PLANNING': ['EXECUTING', 'ERROR'],
    'EXECUTING': ['VERIFYING', 'AWAITING', 'CLOSING', 'ERROR'],
    // ...
  };
  return validTransitions[from]?.includes(to) || false;
}
```

## 总结

Phase A 已成功实现，核心特性：

1. ✅ **有状态 MCP Server**：内存维护 Session 和 Task 状态机
2. ✅ **隐式验证链**：所有修改工具自动验证 Task 状态
3. ✅ **状态机强制**：Agent 无法绕过状态机直接写文件
4. ✅ **检查点恢复**：进程重启时从检查点恢复状态
5. ✅ **28个测试全部通过**
