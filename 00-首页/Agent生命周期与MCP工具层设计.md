---
title: Agent生命周期与MCP工具层设计
type: 系统
role: 架构设计
version: v3.0-final
tags: [系统, Agent, 生命周期, 钩子, MCP, 架构设计, 状态机, 编排器]
updated: 2026-06-24
---

# Agent 生命周期与 MCP 工具层设计

> **设计意图**：将 Agent 从"记规则的自律者"变为"被状态机和工具层推着走的执行器"。
> 规范层告诉 Agent "该做什么"，MCP 工具层保证 Agent "不会做错"。

> **本文档为唯一权威参考**。已合并 v2.1-addendum（状态机强制机制，Phase A 已验证）和 v2.2-addendum（编排器与钩子 Runtime，Phase B 已完成）。

---

## 目录

- [§1 概念模型](#1-概念模型)
- [§2 Session 协议](#2-session-协议)
- [§3 Task 状态机](#3-task-状态机)
- [§4 意图路由](#4-意图路由)
- [§5 钩子系统](#5-钩子系统)
- [§6 动态孵化](#6-动态孵化)
- [§7 收工协议](#7-收工协议)
- [§8 MCP 工具层](#8-mcp-工具层)
- [§9 状态存储](#9-状态存储)
- [§10 与现有体系的关系](#10-与现有体系的关系)
- [§11 实施路径](#11-实施路径)
- [§12 已知约束与缺口](#12-已知约束与缺口)

---

## §1 概念模型

### 1.1 四个基础概念

| 概念 | 是什么 | 不是什么 |
|------|--------|----------|
| **Session** | 一段连续的用户-Agent 对话的生命周期容器。持有活的上下文对象，管理检查点的写入与恢复，负责会话结束时所有 Task 产出的合并收工。 | Session 不是 Task。它不执行具体工作，不绑定单个意图。它是容器，Task 是内容。 |
| **Task** | 从一个用户意图衍生出的、有明确边界和状态机的工作单元。知道"做什么""谁来做""做多大""要不要保留记录"。Task 可以形成父子树。 | Task 不是操作步骤，也不是文件变更本身。Task 是工作单元的抽象封装——描述一个完整意图从诞生到验收的全过程。 |
| **Carrier** | Task 的执行环境。主会话是默认 Carrier，Subagent（隔离 worktree）是并行 Carrier。 | Carrier 不是进程也不是线程。它是逻辑上的执行上下文隔离单元。Carrier 不决定"做什么"，只决定"在哪里做"。 |
| **Orchestrator** | 调度器。负责意图→Task、策略选择、Carrier 分配、依赖树管理、状态机流转、产出合并。 | Orchestrator 不直接执行 Task，也不直接修改文件。它是流程的"大脑"，不是执行的"手"。 |

### 1.2 Task 定义与属性

```
Task {
  // === 四个核心属性（由 ASSESSING 阶段确定）===
  intentType   BUILD | MAINTAIN | USE | META
  agentId      1 | 1B | 2-11 | null
  scale        TRIVIAL | NORMAL | BATCH | COMPOUND
  persistence  FORMAL | EXPLORATORY | NONE

  // === 主状态与副状态 ===
  state        ASSESSING | PLANNING | EXECUTING | VERIFYING | CLOSING | ARCHIVED
              | AWAITING | SUSPENDED | ERROR | REWORK

  // === 派生属性 ===
  strategy     PURE_AGENT | SKILL_DRIVEN | HYBRID

  // === 树结构 ===
  parent       Task | null
  children     Task[]

  // === 执行数据 ===
  progress     { total, completed }
  dirtyModules Set<Module>
  carrier      PRIMARY | SUBAGENT_ID
  reworkCount  number              // VERIFYING→REWORK 累计次数
  awaitingChildren string[]        // AWAITING 时等待的子Task ID列表
}
```

| 属性 | 决定什么 | 取值 |
|:---|:---|:---|
| **intentType** | 对知识库的操作约束（能写哪些目录、能否删除、确认要求、验证维度、收工回写目标） | BUILD / MAINTAIN / USE / META |
| **agentId** | 用什么提示词、DoD 是什么、策略选择的基础 | 1-11, 1B, null |
| **scale** | 执行节奏（是否分批、是否拆子Task、检查点粒度、样本数） | TRIVIAL / NORMAL / BATCH / COMPOUND |
| **persistence** | 归档方式（任务卡 vs 会话清单 vs 无） | FORMAL / EXPLORATORY / NONE |

### 1.3 四种意图类型

| 意图类型 | 来源（典型触发场景） | 特征 | 核心约束 | Agent 映射 |
|:---|:---|:---|:---|:---|
| **BUILD** | 提炼/填充/建知识点/拆题/链接/审查 | 从外部源创建新知识库文件 | 禁止编造；允许写入 03-知识点/ | Agent 1-6, 1B |
| **MAINTAIN** | 优化/改进/合并/弃用/扫一遍/健康检查 | 修改已有文件，可能合并或删除 | 删除强制软弃用+7天缓冲；≥5文件改动必须确认 | Agent 7-9 |
| **USE** | 备课/做大纲/答疑 | 只读 KP，产出教学物料 | **禁止写入 03-知识点/**（MCP 工具层强制阻断） | Agent 10-11 |
| **META** | 改SOP/调整模板/重新设计/清理/压缩/修引用 | 修改系统自身，不触及知识内容 | 修改 00-首页/ 额外警告；每步确认 | null（或由意图决定） |

### 1.4 四种规模

| 规模 | 特征 | 行为差异 |
|:---|:---|:---|
| **TRIVIAL** | 单文件 ≤3 处修改 | 所有状态极简模式（秒过但不跳过），跳过用户确认 |
| **NORMAL** | 单 Agent ≤10 文件 | 标准状态机，单批次 |
| **BATCH** | >10 文件需分批 | PLANNING 批次分解，每批独立检查点 |
| **COMPOUND** | 多 Agent 或多模块 | PLANNING 预拆子Task + 依赖DAG，父Task进AWAITING |

### 1.5 策略自动推导

| agentId | 策略 | 含义 |
|:---|:---|:---|
| 1, 1B, 3, 4, 5, 6, 7, 8, 11 | **PURE_AGENT** | 完全由 Agent 提示词驱动，不使用 Skill |
| 2 | **HYBRID** (kb-kp-creator + Agent填充) | Skill 建骨架，Agent 逐文件填充内容 |
| 9 | **SKILL_DRIVEN** (kb-audit + kb-link-doctor) | Skill 自动扫描→修复→报告 |
| 10 | **HYBRID** (kb-lesson-planner + Agent审校) | Skill 生成大纲初稿，Agent 做认知判断和教学取舍 |

> `*` kb-lesson-planner 的 SKILL.md 文件不存在，是原始体系已知缺口。参见 [§12](#12-已知约束与缺口)。

---

## §2 Session 协议

### 2.1 Session 状态机

```
                    ┌─────────────┐
         用户发起    │    INIT     │  检查点存在且可恢复
         新会话 ────▶│             │──────────────────┐
                    └──────┬──────┘                  │
                           │                         ▼
                           │ 检查点不存在    ┌─────────────────┐
                           │ 或用户拒绝恢复   │   RECOVERING    │
                           │                 └────────┬────────┘
                           │                          │ 恢复成功
                           ▼                          ▼
                    ┌──────────────────────────────────────────────────┐
                    │                    ACTIVE                        │◀──────────┐
                    │   Orchestrator 管理 Task 树                       │           │
                    │   · spawn / schedule                             │  Task 完成 │
                    │   · awaitChildren / checkpoint                    │  返回结果  │
                    └──────────────┬───────────────────────────────────┘           │
                                   │                                               │
                                   │ 所有根Task → ARCHIVED                         │
                                   ▼                                               │
                          ┌─────────────────┐                                      │
                          │    CLOSING      │     仍有活跃Task                      │
                          │  合并收工        │──────────────────────────────────────┘
                          └────────┬────────┘
                                   │ 所有Task关闭
                                   ▼
                          ┌─────────────────┐
                          │      END        │
                          └─────────────────┘
```

### 2.2 Session 职责

```
Session.INIT:
  1. kb_session init → 检查点探测（checkpoint.json 是否存在且有效）
  2. 恢复模式: 读检查点 → 重建Task树 → 恢复上下文 → 跳回 ACTIVE
  3. 新建模式: H-G01 上下文加载 + 指纹注册 + 健康检查优先
  4. 进入 ACTIVE

Session.ACTIVE:
  Orchestrator 管理 Task 树的增删改，持有活的上下文对象供所有 Task 共享。
  上下文对象: { sessionId, taskTree, dirtyModules聚合, checkpointVersion,
               sop/skills/mcp 只读配置, conflicts, warnings }

Session.CLOSING:
  1. 所有根Task已ARCHIVED → 进入
  2. 合并所有根Task的dirtyModules（子Task已由父Task合并）
  3. 生成最终特异性收工清单
  4. 同步入口文件（状态摘要/战略方向/首页.current_focus）
  5. 同日Follow-up去重与回填
  6. 历史高优待办清理（扫描7天日志）
  7. kb_gate phase=4 → 验证清单已清
  8. 写最终检查点(isActive=false) → END
```

### 2.3 Session 异常处理

| 异常类型 | 触发条件 | 处理 |
|:---|:---|:---|
| **可恢复异常** | MCP 超时、文件锁定 | Task → SUSPENDED → 写检查点 → 用户选择重试/跳过 |
| **不可恢复异常** | vault 损坏、SOP 丢失 | 紧急检查点 → 所有Task → ERROR → 降级运行或强制CLOSING |
| **会话中断** | 用户关闭 Obsidian、进程崩溃 | 下次 INIT 时检测检查点 → RECOVERING → 恢复Task树 |
| **冲突处理** | 多Task改同一文件 | CLOSING 合并阶段集中检测 → 用户选择保留版本 |

---

## §3 Task 状态机

### 3.1 完整状态机图（10 个状态）

```
                    Orchestrator.spawn()
                          │
                          ▼
                   ┌───────────┐
                   │ ASSESSING │
                   │ H-A01 意图分类→四个属性
                   │ H-A02 前置条件检查(intentType)
                   │ H-A03 持久化绑定
                   └─────┬─────┘
                         │
                         ▼
                   ┌───────────┐
                   │ PLANNING  │
                   │ H-P01 策略选择    → {strategy}
                   │ H-P02 规模适应    → {batches, 子Task}
                   │ H-P03 确认栅栏    → {wait for confirm}
                   └─────┬─────┘
                         │
                         ▼
                   ┌───────────┐
                   │ EXECUTING │◄──────────────────────┐
                   │ H-E01 操作前校验(MCP)              │
                   │ H-E02 操作后追踪(标脏)              │
                   │ H-E03 进度检查点                   │
                   │ H-E04 Skill调用前                  │
                   │ H-E05 Skill调用后                  │
                   │                                     │
                   │ 动态孵化子Task → 父Task AWAITING     │
                   └─────┬───────┬───────────────────────┘
                         │       │
              ┌──────────┘       └──────────┐
              ▼                             ▼
       ┌───────────┐                 ┌───────────┐
       │ VERIFYING │                 │ AWAITING  │
       │ H-V01 样本验证              │ 等待children
       │ H-V02 问题处置              │ → ARCHIVED
       └─────┬─────┘                 └─────┬─────┘
             │                             │
      ┌──────┴──────┐                      │
      ▼             ▼                      │
┌─────────┐   ┌───────────┐                │
│ REWORK  │   │  CLOSING   │                │
│ → 回到   │   │ H-L01 脏模块审计           │
│ EXECUTING│   │ H-L02 执行收工             │
└─────────┘   │ H-L03 出口清理             │
              └─────┬─────┘                │
                    │                      │
                    ▼                      │
              ┌───────────┐                │
              │ ARCHIVED  │                │
              └─────┬─────┘                │
                    │                      │
              ┌─────┴─────┐                │
              ▼           ▼                │
         若是子Task:    若是根Task:          │
         通知父Task     所有根Task都ARCHIVED? │
         AWAITING→EXECUTING ────────────────┘
                         → Session.CLOSING

SUSPENDED: 会话中断 → 写检查点 → 恢复时从此继续
ERROR: 单文件→跳过+⚠️ / 批次级→回退批 / 系统性→回到PLANNING
       或 REWORK > 2 → 自动转 ERROR → 需要人工干预
```

### 3.2 合法状态迁移表

10 个状态，17 条合法迁移。**任何未列出的迁移在 MCP Server 中会被 `StateManager.updateTaskState()` 拒绝。**

| # | 源状态 | 目标状态 | 触发条件 | 执行方 |
|:--|:---|:---|:---|:---|
| 1 | — (spawn) | **ASSESSING** | Orchestrator 创建 Task | MCP Server |
| 2 | ASSESSING | **PLANNING** | 意图分类和前置检查完成 | Agent 自律 |
| 3 | PLANNING | **EXECUTING** | 计划确认（通过 H-P03 栅栏） | MCP Server (kb_gate phase=1) |
| 4 | EXECUTING | **VERIFYING** | 所有批次产出完成 | Agent 自律 |
| 5 | EXECUTING | **AWAITING** | 动态孵化子Task，父Task挂起 | MCP Server (Orchestrator) |
| 6 | EXECUTING | **SUSPENDED** | 会话中断，紧急写检查点 | MCP Server (checkpoint) |
| 7 | VERIFYING | **CLOSING** | 验证通过 | Agent 自律 |
| 8 | VERIFYING | **REWORK** | 验证发现需修正，reworkCount ≤ 2 | MCP Server (H-V02) |
| 9 | VERIFYING | **ERROR** | reworkCount > 2，不可恢复 | MCP Server (H-V02) |
| 10 | REWORK | **EXECUTING** | 修正后重试 | MCP Server |
| 11 | CLOSING | **ARCHIVED** | H-L02 收工清单已清，kb_gate phase=4 通过 | MCP Server (kb_gate phase=4) |
| 12 | AWAITING | **EXECUTING** | 所有子Task ARCHIVED | MCP Server (Orchestrator) |
| 13 | AWAITING | **ERROR** | 超时（30分钟无进度）或用户取消 | MCP Server (Orchestrator) |
| 14 | SUSPENDED | **EXECUTING** | 会话恢复，检查点恢复成功 | MCP Server (kb_session init) |
| 15 | 任何状态 | **ERROR** | 不可恢复异常（vault损坏、SOP丢失等） | MCP Server |
| 16 | ERROR | **ARCHIVED** | 用户手动关闭（降级收工） | MCP Server (kb_gate phase=4 force=true) |
| 17 | ARCHIVED | —（终态） | — | — |

### 3.3 10 个状态定义

| 状态 | 含义 | 允许的操作 | 典型停留时间 |
|:---|:---|:---|:---|
| **ASSESSING** | 意图分类，确定四个核心属性，做前置条件检查 | 仅 kb_read | 秒级（TRIVIAL）/ 分钟级 |
| **PLANNING** | 选择策略，做规模适应，等待用户确认 | 仅 kb_read | 秒级（TRIVIAL）/ 需要用户交互 |
| **EXECUTING** | 按策略产出文件，追踪脏模块，可孵化子Task | kb_write / kb_edit / kb_move / kb_delete / kb_read / kb_bash(只读) | 分钟至小时级 |
| **VERIFYING** | 抽样验证，跨系统检查；允许修复性修改 | kb_read + 修复性 kb_edit | 分钟级 |
| **CLOSING** | 执行收工清单，生成任务卡，出口清理 | kb_read + kb_write(工作日志/任务卡) | 分钟级 |
| **ARCHIVED** | 终态，Task 完成 | 无（只读查看） | — |
| **AWAITING** | 父Task挂起，等待所有子Task完成 | 无（被动等待） | 分钟至小时级 |
| **SUSPENDED** | 会话中断，等待恢复 | 无 | 取决于用户重连时间 |
| **ERROR** | 不可恢复错误，需人工干预 | 无（需用户决策） | — |
| **REWORK** | 验证失败，回到EXECUTING前做短暂停留 | 无（瞬间过渡） | 毫秒级 |

### 3.4 状态机强制执行机制（MCP Server）

**核心原则**：MCP Server 是有状态的状态机。所有修改文件的工具调用**隐式**经过状态验证。Agent 不需要"自律"地检查状态——它想绕过也绕不过。

```
MCP Server 内部验证链（kb_write / kb_edit / kb_move / kb_delete 内部自动执行）:

  1. Session 存在且状态为 ACTIVE？
     → 否 → 返回 { error: "NO_ACTIVE_SESSION",
              detail: "请先通过 kb_session init 初始化会话" }

  2. 当前 Carrier 上有活跃 Task？
     → 否 → 返回 { error: "NO_ACTIVE_TASK",
              detail: "请先通过 Orchestrator.spawn() 创建 Task" }

  3. Task.state ∈ {EXECUTING, VERIFYING(仅修复性修改), CLOSING(仅收工写入)}？
     → 否 → 返回 { error: "TASK_NOT_EXECUTING", currentState: "PLANNING",
              detail: "Task 当前在 PLANNING 状态，请先通过 kb_gate phase=1 确认计划" }

  4. intentType 允许此操作？
     → USE 写入 03-知识点/ → 返回 { error: "USE_CANNOT_WRITE_KP",
              detail: "USE 类型 Task 禁止修改知识点源文件" }
     → MAINTAIN 调用 kb_delete 且 soft=false → 自动降级为 soft=true + 7天缓冲
     → META 写入 00-首页/ → 自动追加 warning 日志
```

**设计要点**：
- `kb_read` **不检查状态**——只读工具可随时调用（但入口文件指纹比对和跳过逻辑仍然执行）
- `kb_bash` **不检查 Task 状态**——只检查命令白名单（只读放行，写命令阻断），与状态无关
- `kb_gate` 的角色从"状态机唯一执行者"**降级为**"显式的状态迁移确认点"——它创建 Task 对象、确认计划、确认归档，但真正的状态强制由所有修改工具的内部验证链承担

---

## §4 意图路由

### 4.1 路由表

| 用户关键词 | intentType | agentId | persistence |
|:---|:---|:---|:---|
| "提炼""填充""建知识点""拆题""链接""审查" | BUILD | 待定(1-6) | FORMAL |
| "优化""改进""合并""弃用""扫一遍""健康检查" | MAINTAIN | 待定(7-9) | FORMAL |
| "备课""做大纲""答疑" | USE | 待定(10-11) | EXPLORATORY |
| "改SOP""调整模板""重新设计""清理""压缩""修引用" | META | null | FORMAL |
| "什么是X""X怎么反应""为什么X" | QUERY（不创建Task） | — | — |
| 与化学/KB无关 | GENERAL（不创建Task） | — | — |

### 4.2 意图类型差异总表

| 维度 | BUILD | MAINTAIN | USE | META |
|:---|:---|:---|:---|:---|
| **ASSESSING前置检查** | 源文件+模板+考纲 | 目标KP全文+反向引用 | KP只读确认+备课待办 | 系统文件备份+影响面评估 |
| **PLANNING确认要求** | NORMAL自动确认 | ≥5文件强制确认 | 计划确认即可 | 每步强制确认 |
| **EXECUTING文件约束** | 允许写03-知识点/ | 允许修改已有KP | **禁止写03-知识点/** (MCP强制) | 仅写00-首页/11-模板/ |
| **EXECUTING删除行为** | 不涉及 | 软弃用+7天缓冲 (MCP强制) | 不涉及 | 强制快照+确认 |
| **VERIFYING额外维度** | +来源一致性+考纲 | +status匹配度+模板版本 | +跨系统连接 | +版本号+引用 |
| **CLOSING额外回写** | +知识点总索引 | +审计报告归档 | +备课待办(硬规则) | +体系版本表+sop_version |

### 4.3 规模判定（规范层，Agent 自律）

```
TRIVIAL:  单文件且 ≤3 处修改
          判定依据: 用户明确说"改一个词""修一行"

NORMAL:   单 Agent 且 ≤10 文件
          判定依据: 典型单次操作——建一个知识点、改一个专题页

BATCH:    >10 文件但同 Agent
          判定依据: 扫一遍、批量迁移、批量修复

COMPOUND: 多 Agent 或多模块
          判定依据: 横跨 BUILD+MAINTAIN 的复合意图、跨模块大修
```

### 4.4 持久化判定（规范层，Agent 自律）

```
FORMAL:       创建/更新独立的 任务卡-*.md 文件（H-L02 自动生成）
              适用: BUILD / MAINTAIN / META

EXPLORATORY:  追加到 Session 会话清单（不进独立任务卡）
              适用: USE / 探索性操作

NONE:         无持久化
              适用: TRIVIAL / QUERY / GENERAL
```

---

## §5 钩子系统

### 5.1 设计原则

**不依赖 LLM 判断就能执行的约束 → MCP Server Runtime。需要 LLM 语义理解的判断 → 留在规范层（SOP Markdown），Agent 自律执行。**

```
Runtime 钩子（MCP Server 代码）:
  纯逻辑检查或机械计数
  例: "Task.state 是否 == EXECUTING？"、"edits.length > 5？"、"REWORK 次数 > 2？"

规范层钩子（SOP Markdown）:
  需要 LLM 理解上下文做判断
  例: "这个用户意图是 BUILD 还是 MAINTAIN？"、"抽 3 个样本验证内容准确性"
```

### 5.2 17 个钩子分层表

| 编号 | 名称 | 状态 | 分层 | 触发 | 核心行为 |
|:---|:---|:---|:---|:---|:---|
| **H-G01** | 会话初始化 | Session.INIT | **Runtime** (Phase B) | 新建模式 | 加载三入口文件指纹、检查活跃任务健康、获取 availableSkills 列表 |
| **H-A01** | 意图分类 | ASSESSING | **规范层** | 入口 | 用户输入 → {intentType, agentId, scale, persistence}；需 LLM 语义理解 |
| **H-A02** | 前置条件检查 | ASSESSING | **规范层** | H-A01之后 | 按intentType逐项读文件检查，不通过则阻断；需 LLM 判断 |
| **H-A03** | 持久化绑定 | ASSESSING | **规范层** | H-A02之后 | LLM 决策 FORMAL→TaskCard / EXPLORATORY→会话清单 / NONE→跳过 |
| **H-P01** | 策略选择 | PLANNING | **规范层** | 入口 | agentId → PURE/SKILL/HYBRID；LLM 决策 |
| **H-P02** | 规模适应 | PLANNING | **规范层** | H-P01之后 | scale → 批次分解/子Task拆分；LLM 决策 |
| **H-P03** | 确认栅栏 | PLANNING | **Runtime** (Phase B) | H-P02之后 | MAINTAIN≥5文件 或 META → 返回 requiresConfirmation: true，不可跳过 |
| **H-E01** | 操作前校验 | EXECUTING | **Runtime** ✅ 已实现 | 每次文件操作前 | MCP Server 隐式验证链（Session→Task→state→intentType 四级检查） |
| **H-E02** | 操作后追踪 | EXECUTING | **Runtime** ✅ 已实现 | 每次文件操作后 | 自动标记 dirtyModules |
| **H-E03** | 进度检查点 | EXECUTING | **Runtime** (Phase B) | 每10次写操作 | 自动调用 kb_session checkpoint（增量写入）；TRIVIAL 跳过 |
| **H-E04** | Skill调用前 | EXECUTING | **规范层** | Skill调用前 | 校验+预估脏范围+记录意图；暂不实现（Skills 集成后续） |
| **H-E05** | Skill调用后 | EXECUTING | **规范层** | Skill返回后 | 解析产出→批量标脏→P0项注入VERIFY；暂不实现 |
| **H-V01** | 样本验证 | VERIFYING | **规范层** | 入口 | 样本选择+维度验证(按intentType×scale差异化)；需 LLM 抽查 |
| **H-V02** | REWORK 计数 | VERIFYING | **Runtime** (Phase B) | VERIFY失败时 | reworkCount > 2 → 自动转 ERROR；纯计数逻辑 |
| **H-L01** | 脏模块审计 | CLOSING | **Runtime** ✅ 已实现 | 入口 | dirtyModules → 按 intentType 生成特异性收工清单（kb_dirty report） |
| **H-L02** | 执行收工 | CLOSING | **规范层** | H-L01之后 | 写日志+更任务卡+更索引(按intentType差异化)；需 LLM 写内容 |
| **H-L03** | 出口清理 | CLOSING | **Runtime** (Phase B) | H-L02之后 | 清dirtyModules；子Task通知父Task；根Task检查触发Session.CLOSING |

**合计**：17 个钩子，**8 个 Runtime**（H-G01, H-E01, H-E02, H-E03, H-P03, H-V02, H-L01, H-L03），**9 个规范层**。

### 5.3 Runtime 钩子实现概要

```
H-G01 (kb_session init 内部):
  - 加载三入口文件指纹到 read_registry
  - 扫描 skills/ 目录获取 availableSkills 列表
  - 检查活跃 Task 健康（缺关键字段 → 标记 warning）

H-E01 (kb_write/kb_edit/kb_move/kb_delete 内部):
  - 隐式验证链: Session → Task → state → intentType
  - 已在 Phase A 实现，8/8 测试通过

H-E02 (kb_write/kb_edit 内部):
  - 自动提取文件所属模块，标记到 Task.dirtyModules
  - 已在 Phase A 实现

H-E03 (kb_write/kb_edit 调用后):
  - 累计写操作计数器，每 10 次 → 自动 checkpoint
  - TRIVIAL scale 跳过

H-P03 (kb_gate phase=1 内部):
  - MAINTAIN 且 files_modified ≥ 5 → requiresConfirmation: true
  - META → requiresConfirmation: true
  - Agent 需先获得用户确认，再调 kb_gate phase=1 confirm=true

H-V02 (kb_gate phase=4 内部):
  - VERIFY 失败时递增 reworkCount
  - reworkCount > 2 → 拒绝 phase=4，Task 自动转 ERROR

H-L01 (kb_dirty report 内部):
  - 按 activeTask.intentType 对照收工矩阵
  - 返回 { dirtyModules, syncChecklist: [{ target, mandatory, reason }] }

H-L03 (Task state → ARCHIVED 时):
  - 清除 Task.dirtyModules
  - 若是子Task → Orchestrator.onChildArchived(parentTask)
  - 若是根Task 且所有根Task ARCHIVED → Orchestrator.mergeOnClose()
```

---

## §6 动态孵化

### 6.1 三种孵化场景

| 场景 | 触发阶段 | 触发条件 | 行为 |
|:---|:---|:---|:---|
| **预拆分** | PLANNING (COMPOUND) | 规模判定为多 Agent/多模块 | PLANNING 中拆出依赖 DAG → 父Task 进入 AWAITING |
| **执行中孵化** | EXECUTING | 执行过程中发现前置缺失（如源文件不存在、模板缺失） | 创建子Task → 父Task 进入 AWAITING |
| **修正孵化** | VERIFYING | 验证发现同类问题跨多文件 | 创建修正子Task |

### 6.2 上下文继承协议

```
ContextInheritance {
  skipSessionInit: true           // 子Task不重复读三入口文件
  parentReadRegistry: {...}       // 继承父Task已读文件
  inheritSources: [...]           // 继承来源（模板路径、提炼笔记等）
  onComplete: "return_to_parent"
}
```

### 6.3 动态孵化的 MCP 协议约束

**MCP 协议约束**：MCP Server 不能主动启动进程，不能直接启动 Subagent。

因此 Orchestrator 的"调度和启动"职责**必然分裂**为两部分：

| 职责 | 执行方 | 说明 |
|:---|:---|:---|
| 状态机管理 + 孵化指令生成 | **MCP Server** (Orchestrator) | 创建子Task、设置父Task→AWAITING、生成上下文继承包 |
| Subagent 实际启动 | **Agent 侧** | 接收孵化指令，启动 Subagent 进程并注入上下文 |

### 6.4 孵化桥接：`kb_gate phase=spawn`

MCP 协议无法让 Server 启动 Agent 进程。解决方案：新增 `kb_gate phase=spawn` 作为桥接 gate。

```
孵化流程:

  1. MCP Server (Orchestrator) 检测到孵化需求
     → 创建子Task
     → 设置父Task.state = AWAITING
     → 生成孵化指令 { childTaskId, contextInheritance, childIntentType, childScale }

  2. MCP Server 返回孵化指令给 Agent（通过 kb_gate phase=spawn 的响应）

  3. Agent 侧收到孵化指令
     → 启动 Subagent
     → Subagent 连接同一 MCP Server
     → Subagent 调用 kb_session init（继承上下文）
     → MCP Server 识别 Subagent 并绑定到子Task

  4. 子Task 在 Subagent Carrier 上执行

  5. 子Task → ARCHIVED
     → Orchestrator.onChildArchived(parentTask)
     → 所有子Task完成后 → 父Task AWAITING → EXECUTING

  6. Agent 侧收到父Task恢复通知
     → 父Task 继续执行（在原本的 Carrier 上）
```

**当前 Phase B 实现范围**：仅实现 PRIMARY Carrier 的孵化逻辑。Subagent Carrier（worktree 隔离 + 进程管理）推迟到后续 Phase。Phase B 中，孵化出的子Task 仍在同一会话内**串行执行**（父Task AWAITING → 子Task 执行 → 子Task 完成后父Task 恢复）。

### 6.5 脏模块合并

```
父Task.CLOSING 时:
  dirtyModules = 自己dirty ∪ subTask1.dirty ∪ subTask2.dirty ∪ ...
  递归合并所有子孙Task的dirtyModules
```

---

## §7 收工协议

### 7.1 收工矩阵（按 intentType 映射）

#### BUILD

| 脏模块 | 必须同步的目标 | 条件 | 执行方 |
|:---|:---|:---|:---|
| `03-知识点/` | 知识点总索引 | 新增 > 5（强制） | 规范层 (H-L02) |
| `04-题库/` | 题库总索引 | 新增 > 10（强制） | 规范层 (H-L02) |
| 任何模块 | 工作日志 + 活跃任务 | 始终（强制） | 规范层 (H-L02) |
| 任何模块 | 生成任务卡到 `00-首页/活跃任务/` | FORMAL 持久化时 | Runtime (H-L02 自动生成 frontmatter) |

#### MAINTAIN

| 脏模块 | 必须同步的目标 | 条件 | 执行方 |
|:---|:---|:---|:---|
| `03-知识点/` | 知识点总索引 + 所有引用更新 | 弃用/重命名时（强制） | 规范层 (H-L02) |
| 任何模块 | 审计报告归档 + 状态变更日志 + 工作日志 | 始终（强制） | 规范层 (H-L02) |
| 任何模块 | 生成任务卡到 `00-首页/活跃任务/` | FORMAL 持久化时 | Runtime |

#### USE

| 脏模块 | 必须同步的目标 | 条件 | 执行方 |
|:---|:---|:---|:---|
| `04-课件/` | 备课与教学思路待办 | **硬规则，不可跳过** | 规范层 (H-L02) |
| `03-知识点/` | — | 若意外写入 → MCP Server 触发 ERROR 并拒绝 | Runtime (H-E01) |
| 任何模块 | 工作日志 | 始终（强制） | 规范层 (H-L02) |

#### META

| 脏模块 | 必须同步的目标 | 条件 | 执行方 |
|:---|:---|:---|:---|
| `00-首页/` | 状态摘要 + 首页.current_focus + 必要时战略方向 | 始终（强制） | 规范层 (H-L02) |
| `11-模板/` | 状态摘要体系版本表 + 首页.sop_version | 始终（强制） | 规范层 (H-L02) |
| 任何模块 | 工作日志 + 活跃任务 + 变更日志 | 始终（强制） | 规范层 (H-L02) |
| 任何模块 | 生成任务卡到 `00-首页/活跃任务/` | FORMAL 持久化时 | Runtime |

### 7.2 任务卡自动生成

#### 背景

原项目有 **17 处依赖**任务卡文件（`00-首页/活跃任务/任务卡-*.md`，frontmatter `type: 活跃任务卡`）：

- **5 处 Dataview 查询**：`活跃任务.md` 的 6 个面板、3 个自动汇总文件、`状态摘要.md` 嵌入引用
- **5 个 .base 视图**：全部/活跃/已完成/已阻塞/看板卡片
- **7 个 SOP 入口文件的流程引用**：Phase 0 启动链路、Phase 4 收工链路、入口文件关系、收工矩阵、最小执行协议

#### 设计决策

H-L02 不替代任务卡——而是**自动生成**格式完全兼容的任务卡到同一目录。Dataview 查询不关心文件是谁写的，只查 frontmatter。只要满足以下三个条件，所有消费方**完全不需要修改**：

1. 文件放入 `00-首页/活跃任务/` 目录
2. frontmatter 包含 `type: 活跃任务卡` 及所有必需字段
3. 字段语义与 `模板-活跃任务卡.md` v1.1 一致

#### 生成格式

```
H-L02 自动生成的任务卡文件: 00-首页/活跃任务/任务卡-<Task.id>.md

  Frontmatter:
    type: 活跃任务卡
    task_id: <Task.id>              # 新增字段，供 MCP Server 回溯
    status: <Task.state 映射>       # completed / blocked
    priority: <Task.scale 映射>     # HIGH / MEDIUM / LOW
    area: <Task.intentType 映射>    # KP_BUILD / KP_MAINTAIN / TEACH_USE / META
    owner: Agent
    created: <Task.createdAt>
    updated: <now>
    completed: <now>                # 仅 state=ARCHIVED时
    source_notes: ["[[来源]]"]
    related_notes: ["[[关联]]"]
    evidence: ["本次产出: <filesCreated列表>"]
    is_auto_generated: true         # 区分手动/自动任务卡

  正文（由 Agent 在 CLOSING 时提供内容）:
    # <Agent 描述> — 完成摘要
    ## 产出
    <Agent 提供>
    ## 关键决策
    <Agent 提供>
    ## 子任务
    <如有，列出子Task摘要>
```

#### 对旧任务卡的兼容

- `00-首页/活跃任务/` 中现存的 **4 张 blocked 任务卡保留不动**
- `09-审计报告/历史任务卡/` 中 **33 张 completed 任务卡保留不动**
- 新生成的自动任务卡混入同一目录，Dataview 统一聚合
- Agent 仍可在需要时手动创建任务卡（如 blocked 类需人工维护的项）

### 7.3 Session.CLOSING 流程

```
Session.CLOSING:
  1. 所有根Task已ARCHIVED → 触发
  2. Orchestrator.mergeOnClose():
     - 合并所有根Task的 dirtyModules（子Task 已由父Task合并）
     - 去重冲突文件
     - 生成最终特异性收工清单
  3. 同步入口文件（状态摘要/战略方向/首页.current_focus）
  4. 同日 Follow-up 去重与回填
  5. 历史高优待办清理（扫描7天日志）
  6. kb_gate phase=4 → 验证收工清单已清
  7. 写最终检查点 (isActive=false) → END
```

---

## §8 MCP 工具层

### 8.1 架构说明

旧架构中 Agent 直接使用原生 Read/Write/Edit/Bash，所有约束靠 Agent "自律"。三个根本缺陷：

1. **不可强制执行** — Agent 可能因上下文截断或幻觉违反约束
2. **无状态感知** — 不知道哪些文件已读、哪些模块已脏
3. **无法审计** — 无结构化操作日志

**解决方案**：禁用 Claude Code 原生工具，只暴露自定义 MCP 工具。Agent 无法绕过——文件指纹比对、脏模块标记、反向引用检查都在 MCP 服务端强制执行。

### 8.2 工具清单（10 个）

| 工具 | 替代原生 | 实现状态 | 强制约束 |
|:---|:---|:---|:---|
| `kb_read` | Read | ✅ 已实现 | 指纹比对 + 已读注册；入口文件未变化则跳过 |
| `kb_write` | Write | ✅ 已实现 | 隐式验证链 + 冲突检测 + 自动标脏模块 |
| `kb_edit` | Edit | ✅ 已实现 | 隐式验证链 + old_string 唯一性验证 + 自动标脏 |
| `kb_bash` | Bash | ✅ 已实现 | 白名单：只读命令放行；写命令阻断并提示用 kb_* 工具 |
| `kb_session` | — | ✅ 已实现 | init\|checkpoint\|clear — 会话生命周期管理 + 内存状态初始化 + 检查点恢复 |
| `kb_dirty` | — | ✅ 已实现 | mark\|report\|clear — report 按 intentType 返回特异性收工清单 |
| `kb_gate` | — | ✅ 已实现 | phase=0\|1\|4\|spawn — 状态迁移确认点；Phase B 增强 phase=1/4 |
| `kb_move` | Bash mv | ✅ 已实现 | 隐式验证链 + 反向引用检查 → 阻断或自动修复所有引用 |
| `kb_delete` | Bash rm | ✅ 已实现 | 隐式验证链 + 确认+快照+引用检查；MAINTAIN时强制软弃用 |
| `kb_search` | Grep/Glob | ✅ 已实现 | type=grep\|glob\|crossref；反向引用模式用缓存索引 |

### 8.3 关键工具详细设计

#### `kb_read` — 指纹比对

```
参数: path, offset?, limit?

强制逻辑:
  1. 验证 path 在 vault 内
  2. 若 path 是入口文件 → 计算指纹 (version + updated + 内容 hash)
     → 比对 read_registry → 未变化且本次已读 → 返回 { skipped: true }
  3. 执行读取 → 写入 read_registry { path, fingerprint, readAt }

状态检查: 无（只读工具可随时调用）
不可绕过: Agent 不知道文件是否变化，只有 MCP 有指纹缓存
```

#### `kb_write` — 冲突检测

```
参数: path, content

强制逻辑:
  1. 隐式验证链: Session ACTIVE → Task 存在 → state ∈ {EXECUTING, CLOSING}
  2. intentType 路径约束检查
  3. 冲突检测: 文件存在且 fingerprint ≠ read_registry 记录 → 拒绝
  4. 执行写入 → 自动标脏模块

不可绕过: 状态验证在 MCP Server 内部，Agent 无法跳过
```

#### `kb_edit` — old_string 唯一性验证

```
参数: path, edits: [{ oldText, newText }]

强制逻辑:
  1. 隐式验证链: Session ACTIVE → Task 存在 → state ∈ {EXECUTING, VERIFYING(修复性), CLOSING(收工)}
  2. 对每个 edit，验证 oldText 在目标文件中**唯一出现**
     → 不唯一 → 返回错误 + 列出所有出现位置
  3. 验证 edits 之间无重叠
  4. 若 edits.length > 5 → 返回要求确认
  5. 执行所有 edits → 自动标脏

不可绕过: old_string 唯一性验证是服务端强制执行
          → 彻底消除经验沉淀 1-1（全角冒号等 Edit 失败问题）
```

#### `kb_move` — 反向引用阻断

```
参数: source, target, autoFix?（默认 false）

强制逻辑:
  1. 隐式验证链（同 kb_write）
  2. 动态反向引用查询（临时方案: kb_search type=grep 实时查找）
     → 搜索 vault 中所有引用 source 的 wikilink
     → 列出引用者列表
  3. 若有引用:
     autoFix=false → 阻断，返回 { blocked: true, referencedBy: [...], fixPlan }
     autoFix=true  → 逐个 kb_edit 更新引用 → 执行 rename
  4. 标脏所有涉及文件

注: Phase B 使用动态 grep 查引用；Phase C 替换为反向引用索引缓存
不可绕过: 移动文件不可能断链——要么被阻断，要么自动修复
```

#### `kb_bash` — 只读白名单

```
白名单放行: grep, rg, find, ls, stat, git log/diff/status, echo, cat, head, tail, wc
黑名单阻断: rm, mv, cp, chmod, sed -i, awk -i, tee, dd
  → 返回 { blocked: true, reason: "文件修改必须通过 kb_write/kb_edit/kb_move" }

状态检查: 无（只检查白名单，不检查 Task 状态）
不可绕过: Agent 无法通过 Bash 裸操作文件 → 所有文件修改必须走 MCP 工具层
```

#### `kb_session` — 会话管理

```
kb_session init:
  1. MCP Server 内存中初始化 Session 对象和上下文
  2. 若 checkpoint.json 存在且有效 → 从检查点恢复 Session 和所有活跃 Task 的运行时状态
  3. 新建模式: 调用 H-G01 加载入口文件指纹、健康检查
  4. 返回 { sessionId, mode: "new" | "recovered", activeTasks: [...] }

kb_session checkpoint:
  将当前内存中 Session 和所有 Task 状态序列化写入 checkpoint.json
  原子写入: 先写 .tmp 再 mv（防止 JSON 损坏）

kb_session clear:
  清理内存状态并归档检查点
```

#### `kb_dirty` — 脏模块追踪

```
kb_dirty mark:
  参数: module, filePath
  自动由 kb_write/kb_edit/kb_move/kb_delete 调用

kb_dirty report:
  1. 检查是否有活跃 Task → 无则返回原始脏文件列表（无意图上下文）
  2. 有活跃 Task:
     dirtyModules = Task.dirtyModules ∪ children(递归).dirtyModules
     按 Task.intentType 对照收工矩阵生成特异性清单
  3. 返回: { dirtyModules, syncChecklist: [{ target, mandatory, reason }] }

kb_dirty clear:
  清除指定模块的脏标记（由 H-L03 调用）

若没有活跃 Task（Agent 没有通过 kb_gate 创建 Task 就尝试报告）:
  返回基础脏文件列表，不含意图上下文
```

#### `kb_gate` — 状态迁移确认点

```
phase=0 (Task 创建):
  验证入口文件已读 → 创建 Task 实例 → Task.state = ASSESSING
  参数: intentType, agentId?, scale?, persistence?
  返回: { taskId, state: "ASSESSING" }
  若跳过直接调 kb_write: Task 不存在 → "NO_ACTIVE_TASK"

phase=1 (确认计划):
  调用 H-P03 确认栅栏 → 通过后 Task.state = EXECUTING
  参数: taskId, planSummary, confirm?（用户确认标志）
  若 H-P03 requiresConfirmation 且 confirm=false → 拒绝
  若跳过直接调 kb_write: Task.state == PLANNING → "TASK_NOT_EXECUTING"

phase=4 (确认归档):
  调用 H-V02 REWORK 计数检查 → 通过后 Task.state = ARCHIVED
  参数: taskId, force?（ERROR 状态下强制归档）
  若 reworkCount > 2（且非force）→ 拒绝，Task 自动转 ERROR
  若未调用: Task 保持在 CLOSING，不触发 Session 收工合并

phase=spawn (孵化桥接):
  接收孵化指令，生成上下文继承包
  参数: parentTaskId, childIntentType, childScale
  返回: { childTaskId, contextInheritance, instruction }
```

### 8.4 工具-状态-钩子对照

| 工具 | 调用可用的 Task 状态 | 内部调用钩子 | 标脏 |
|:---|:---|:---|:---|
| `kb_read` | 任何状态 | — | 否 |
| `kb_write` | EXECUTING, CLOSING(收工写入) | H-E01, H-E02, H-E03 | 是 |
| `kb_edit` | EXECUTING, VERIFYING(修复性), CLOSING(收工) | H-E01, H-E02, H-E03 | 是 |
| `kb_bash` | 任何状态（仅白名单） | — | 否 |
| `kb_move` | EXECUTING | H-E01, H-E02, H-E03 | 是 |
| `kb_delete` | EXECUTING | H-E01, H-E02, H-E03 | 是 |
| `kb_search` | 任何状态 | — | 否 |
| `kb_session` | 任何状态 | H-G01(init时) | 否 |
| `kb_dirty` | 任何状态 | H-L01(report时) | 否 |
| `kb_gate` | — (状态迁移) | H-P03(phase=1), H-V02(phase=4) | 否 |

---

## §9 状态存储

### 9.1 存储结构

`.claude/state/` 目录：

```
checkpoint.json       — 会话检查点（含所有活跃 Task 的完整树 + 状态 + 进度 + 脏模块）
read_registry.json    — 已读文件注册表 { path: { fingerprint, readAt } }
dirty_modules.json    — 脏模块集合 { module: { changeTypes, files } }
reverse_index.json    — 反向引用索引（Phase C 由 kb-link-doctor 生成并缓存）
```

### 9.2 `checkpoint.json` Schema

```json
{
  "version": 1,
  "sessionId": "uuid",
  "isActive": true,
  "createdAt": "ISO8601",
  "updatedAt": "ISO8601",
  "context": {
    "readRegistry": { "path": { "fingerprint": "...", "readAt": "..." } },
    "aggregateDirtyModules": ["Module"],
    "conflicts": [],
    "warnings": []
  },
  "tasks": [
    {
      "id": "uuid",
      "intentType": "BUILD",
      "agentId": 2,
      "scale": "NORMAL",
      "persistence": "FORMAL",
      "state": "EXECUTING",
      "strategy": "HYBRID",
      "parent": null,
      "children": [],
      "progress": { "total": 5, "completed": 3 },
      "dirtyModules": ["03-知识点/有机化学/醇"],
      "carrier": "PRIMARY",
      "reworkCount": 0,
      "awaitingChildren": [],
      "createdAt": "ISO8601",
      "plan": { "sources": [], "targets": [], "batches": [], "risks": [] },
      "decisions": []
    }
  ]
}
```

### 9.3 原子写入策略

```
checkpoint 写入:
  1. 序列化当前完整状态 → /tmp/checkpoint.tmp
  2. 验证 JSON 可解析 → 否 → 放弃写入 + 记录错误
  3. mv /tmp/checkpoint.tmp → .claude/state/checkpoint.json
  4. 保留最近 3 个检查点的备份 (checkpoint.json.bak.1/2/3)

损坏处理:
  checkpoint.json 无法解析 → 尝试最近备份
  全部备份不可用 → 降级为新建会话（丢失未完成 Task 上下文，不丢失文件）
```

---

## §10 与现有体系的关系

### 10.1 完全不变的文件（~90%）

- **00-首页/**: Agent战略方向、Agent任务分解指南、入口文件关系说明、操作与导航说明、数据库使用指南、经验沉淀、方法论、Frontmatter角色词表、系统页角色索引、给Agent下指令模板
- **11-模板/**: 11个轻量提示词、3个长版提示词、22个内容模板、pptx-toolkit
- **skills/**: 11个 SKILL.md（kb-lesson-planner 除外，属已知缺口）
- **02-数据库/**: 5个 .base 文件
- **所有知识内容**: 03-知识点/、04-课件/、07-资料提炼/ 等
- **Dataview/.base/自动汇总**: 全部不受影响（H-L02 自动生成的任务卡格式兼容）

### 10.2 需要修改的文件（5 个）

| 文件 | 改动 | 改动量 |
|:---|:---|:---|
| **Agent标准作业流程.md** | 重组章节：会话级→Session协议，任务级→Task协议，规范保留附录 | ~300行重组（原1150行→精简至~650行） |
| **Agent最小执行协议.md** | 更新读取顺序描述 + 增加MCP工具速查表 | ~80行（~30%） |
| **Agent模块关系与收工同步清单.md** | 增加 intentType 到矩阵行的速查表 | ~60行（~25%） |
| **状态摘要.md** | 底部增加会话检查点 section | ~25行（~15%） |
| **.claude/settings.json** | 增加 MCP 权限配置，禁用原生工具 | ~20行 |

### 10.3 新增文件

| 文件 | 说明 |
|:---|:---|
| `00-首页/Agent生命周期与MCP工具层设计.md` | **本文档**（唯一权威设计参考） |
| `.claude/state/` 目录及 4 个 JSON 文件 | MCP 状态存储 |
| `.claude/mcp.json` | MCP Server 注册配置 |
| `kb-vault-mcp/` (Node.js 项目) | MCP Server 源码（~1200-1600行，含 Phase A+B 新增） |

### 10.4 现有内容去向映射

| 原位置 | 内容 | 新位置 | 执行方 |
|:---|:---|:---|:---|
| SOP Phase 0 默认模式 | 读三入口文件 | Session.INIT + H-G01 — 会话级，只做一次 | Runtime |
| SOP Phase 0 任务相关阅读清单 | 11种任务各自必读文件 | H-A02 前置条件检查表 — 按 intentType 查表 | 规范层 |
| SOP Phase 1 Step 2 | 前置条件6项检查 | H-A02 — Agent 自律执行 | 规范层 |
| SOP Phase 2 执行原则 | 5条原则（红线 1-6,8） | Task.EXECUTING + MCP 隐式验证链 | Runtime |
| SOP Phase 3 | 验证抽查 | Task.VERIFYING — 按 intentType 增加额外维度 | 规范层 |
| SOP Phase 4 Step 1-2 | 写日志+更新任务卡 | Task.CLOSING — 任务级归档；任务卡由 H-L02 自动生成 | Runtime + 规范层 |
| SOP Phase 4 Step 2.5-2.58 | 同步入口文件+收工矩阵核对 | Session.CLOSING — 会话级终结处理 | Runtime (mergeOnClose) |
| SOP 通用红线 1-6,8 | 路径/编造/审核/结构/可逆/用户对齐 | MCP 隐式验证链 — 强制执行 | Runtime |
| SOP 红线 7 | 图片插入规范 | 独立附录（不在此设计范围） | 规范层 |
| SOP 35条自检问句 | — | 钩子入口条件 — 不通过则阻断 | Runtime + 规范层 |

### 10.5 核心设计原则（贯穿全文）

> 只要一个约束可以在代码里纯逻辑判断而无需 LLM 语义理解，它就**不该**留在 Markdown 里等 Agent 自律——它应该进入 MCP Server Runtime。

| 在哪里 | 例子 | 分层 |
|:---|:---|:---|
| MCP Server Runtime | "Task.state 是否 == EXECUTING？""edits > 5？""REWORK > 2？""路径在 03-知识点/？" | 强制执行 |
| 规范层 (SOP) | "用户意图是 BUILD 还是 MAINTAIN？""抽 3 个样本验证内容准确性""写工作日志" | Agent 自律 |

---

## §11 实施路径

| 阶段 | 内容 | 状态 | 预估 |
|:---|:---|:---|:---|
| **Phase A** | MCP Server 核心实现（kb_read/write/edit/bash/session/dirty/gate 7 个工具）+ StateManager + 隐式验证链 | ✅ **已完成** | 5-7天（已完成） |
| **Phase B** | Orchestrator + HookRuntime + kb_move + 状态迁移补全 + kb_gate 增强 | ✅ **已完成** | 3-4天（已完成） |
| **Phase C** | 反向引用索引缓存 + kb_search crossref + kb_delete + 任务卡自动生成落地 | ✅ **已完成** | 2-3天（已完成） |
| **Phase D** | 规范层重组（SOP/最小协议/收工清单结构调整） | 🔄 **当前** | 1-2天 |
| **Phase E** | 集成测试 + 文档最终化 | ⏳ 后续 | 2-3天 |

**依赖关系**: Phase A → B → C → D → E
**总预估**: 13-19 人天（Phase A+B+C 已消耗 10-14）

### Phase A 验证结果（✅ 已完成，8/8 测试通过）

- MCP Server 有状态架构：内存维护 Session + Task 状态机 — ✅ 可行
- 隐式验证链（Session→Task→state→intentType 四级检查）— ✅ 8/8 测试通过
- `kb_gate` 角色降级为显式确认点 — ✅ 正确
- 已实现工具：kb_read, kb_write, kb_edit, kb_bash, kb_session, kb_dirty, kb_gate（7 个）
- 未实现工具：无（10/10 全部完成）

### Phase B 验证结果（✅ 已完成，4/4 测试通过）

| 测试 | 场景 | 结果 |
|:---|:---|:---|
| 1 | 父Task创建子Task（parentId） | ✅ |
| 2 | kb_move 无引用 → 直接移动 | ✅ |
| 3 | kb_move 有引用 autoFix=false → 阻断 | ✅ |
| 4 | kb_move 有引用 autoFix=true → 自动修复 | ✅ |

**Phase B 实际产出**: Orchestrator 类 + HookRuntime（8个Runtime钩子）+ kb_move + 状态迁移补全 + kb_gate parentId增强

### Phase B 文件清单（实际）

```
新增文件:
  kb-vault-mcp/src/orchestrator/orchestrator.ts   (~200行)
  kb-vault-mcp/src/hooks/hook-runtime.ts          (~150行)

修改文件:
  kb-vault-mcp/src/state/manager.ts               补全状态迁移表 (~50行)
  kb-vault-mcp/src/tools/kb_gate.ts               增强 phase=1/4/spawn (~60行)
  kb-vault-mcp/src/types.ts                       增加 reworkCount, awaitingChildren 字段
  kb-vault-mcp/src/index.ts                       注册 Orchestrator + HookRuntime

新增工具:
  kb-vault-mcp/src/tools/kb_move.ts               (~120行，原 Phase C 提前)
```

### Phase C 验证结果（✅ 已完成，7/7 测试通过）

| 测试 | 场景 | 结果 |
|:--|:---|:---|
| 1 | kb_search type=grep | ✅ |
| 2 | kb_search type=glob | ✅ |
| 3 | kb_search type=crossref 有缓存 | ✅ |
| 4 | kb_index action=rebuild | ✅ |
| 5 | kb_delete confirm=false → 阻断 | ✅ |
| 6 | kb_delete MAINTAIN 有引用 → 自动软弃用 | ✅ |
| 7 | kb_delete 无引用 confirm=true → 成功删除+快照 | ✅ |

**Phase C 实际产出**: kb_search + kb_delete + kb_index + 反向引用索引缓存 + H-L02 任务卡自动生成

### Phase D 测试清单（计划）

| # | 测试场景 | 预期 |
|:--|:---|:---|
| 1 | kb_search type=crossref → 返回反向引用 | 命中缓存索引 |
| 2 | kb_search type=crossref 索引过期 → 回退grep | 返回 stale 警告 |
| 3 | kb_delete 确认=false → 阻断 | 返回 needsConfirmation |
| 4 | kb_delete MAINTAIN soft=false → 自动软弃用 | 强制 soft=true |
| 5 | kb_delete 有引用 → 阻断 | 返回引用清单 |
| 6 | H-L02 自动生成任务卡 | frontmatter 字段完整，type=活跃任务卡 |
| 7 | 任务卡格式兼容 Dataview 查询 | 活跃任务.md 正常聚合 |
| 8 | 确认栅栏测试 | MAINTAIN≥5/META 强制确认 |
| 9 | REWORK 计数测试 | >2 自动转 ERROR |
| 10 | 进度检查点测试 | 每10次操作自动写入 checkpoint |

---

## §12 已知约束与缺口

| # | 约束/缺口 | 影响 | 缓解措施 | 状态 |
|:--|:---|:---|:---|:---|
| 1 | **kb-lesson-planner 的 SKILL.md 缺失** | Agent 10 HYBRID 策略缺少关键组件 | 短期：降级为基础检查；长期：补写 SKILL.md | 已知缺口 |
| 2 | **Orchestrator 职责分裂** | MCP Server 不能主动启动进程，schedule/awaitChildren 需要 Agent 侧配合 | Phase B 仅实现 PRIMARY Carrier 串行孵化；Subagent Carrier 推迟 | 设计约束 |
| 3 | **Subagent Carrier 推迟** | 多 Agent 并行（COMPOUND 规模）不可用 | Phase B 中子Task 在同一会话内串行执行；worktree 隔离方案后续 Phase | 设计约束 |
| 4 | **MCP Server 依赖 Claude Code 版本** | 不同版本 MCP 协议行为可能不一致 | 锁定已知可用版本；mcp.json 声明最低版本要求 | 运行时风险 |
| 5 | **禁用原生工具后调试困难** | MCP Server bug 时 Agent 无法直接读文件 | 保留只读降级通道（Read + Bash 受限模式） | 已缓解 |
| 6 | **检查点 JSON 损坏** | 会话恢复失败，丢失未完成 Task 上下文 | 原子写入（先写 .tmp 再 mv）+ 保留最近 3 个备份 | 已设计 |
| 7 | **反向引用索引过期** | 用户绕过 MCP 在 Obsidian 中手动移动文件 | Session.INIT 检测索引新鲜度；设计 kb_index rebuild 工具 | Phase C 解决 |

---

## 附录：一句话工作口径

```
旧口径:
"先用最小协议定位，再用轻量提示词执行；遇复杂问题再升级完整SOP；
 收工时按同步矩阵回写系统层。"

新口径:
"Session 管'在哪'（上下文/检查点/收工合并）
 Task 管'做什么'（十状态状态机，可动态孵化子Task）
 Orchestrator 管'怎么做'（意图→属性→策略→载体→树管理）
 Carrier 管'在哪做'（执行环境/隔离/并行）
 MCP 管'不能怎么做'（文件操作的硬约束——隐式验证链不可绕过）

 四种意图类型决定约束集，四种规模决定节奏，三种持久化决定归档。
 所有 Task 走相同状态序列，差异在钩子分支。不跳过状态，只切换模式。
 Runtime 强制能纯逻辑判断的；规范层留给需要 LLM 语义理解的。
 不依赖 Agent 记住规则——让代码保证 Agent 不会做错。"
```

---

*本设计合并了 v2.0-final 原设计、v2.1-addendum 状态机强制修正（Phase A 已验证）和 v2.2-addendum 编排器与钩子 Runtime 修正（Phase B 已完成）。*
*版本 v3.0-final。本文档是 Phase D 及后续阶段实施的唯一权威参考。*
