/**
 * KB Vault MCP Server - Type Definitions
 * 基于设计文档的状态机类型系统
 */

// 意图类型
export type IntentType = 'BUILD' | 'MAINTAIN' | 'USE' | 'META';

// 规模类型
export type Scale = 'TRIVIAL' | 'NORMAL' | 'BATCH' | 'COMPOUND';

// 持久化类型
export type Persistence = 'FORMAL' | 'EXPLORATORY' | 'NONE';

// Task 状态
export type TaskState = 
  | 'ASSESSING' 
  | 'PLANNING' 
  | 'EXECUTING' 
  | 'VERIFYING' 
  | 'CLOSING' 
  | 'ARCHIVED' 
  | 'AWAITING' 
  | 'SUSPENDED' 
  | 'ERROR' 
  | 'REWORK';

// Session 状态
export type SessionState = 'INIT' | 'ACTIVE' | 'CLOSING' | 'END';

// 策略类型
export type Strategy = 'PURE_AGENT' | 'SKILL_DRIVEN' | 'HYBRID';

// 文件指纹
export interface FileFingerprint {
  path: string;
  version?: string;
  updated?: string;
  contentHash: string;
  readAt: string;
}

// Task 定义
export interface Task {
  id: string;
  state: TaskState;
  intentType: IntentType;
  agentId: number | null;
  strategy: Strategy;
  scale: Scale;
  persistence: Persistence;
  parent: string | null;
  children: string[];
  awaitingChildren: string[];
  reworkCount: number;
  dirtyModules: Set<string>;
  plan?: {
    sources: string[];
    targets: string[];
    batches?: string[][];
    risks: string[];
  };
  decisions: string[];
  createdAt: string;
  updatedAt: string;
}

// Session 定义
export interface Session {
  id: string;
  state: SessionState;
  startedAt: string;
  lastCheckpoint?: string;
  currentTaskId: string | null;
  context: {
    readRegistry: Map<string, FileFingerprint>;
    aggregateDirtyModules: Set<string>;
  };
}

// 检查点数据
export interface CheckpointData {
  session: {
    id: string;
    state: SessionState;
    startedAt: string;
    lastCheckpoint?: string;
    currentTaskId: string | null;
  };
  tasks: Array<[string, Task]>;
  readRegistry: Array<[string, FileFingerprint]>;
  timestamp: string;
}

// 编辑操作
export interface EditOperation {
  oldText: string;
  newText: string;
}

// 验证错误
export interface ValidationError {
  code: string;
  detail: string;
  currentState?: string;
}

// 工具结果
export interface ToolResult {
  success: boolean;
  error?: ValidationError;
  [key: string]: any;
}

// kb_read 返回
export interface ReadResult extends ToolResult {
  content?: string;
  skipped?: boolean;
  fingerprint?: FileFingerprint;
}

// kb_write 返回
export interface WriteResult extends ToolResult {
  path?: string;
  dirtyModule?: string;
}

// kb_edit 返回
export interface EditResult extends ToolResult {
  path?: string;
  appliedEdits?: number;
  dirtyModule?: string;
  conflictDetails?: {
    editIndex: number;
    occurrences: number;
    positions: number[];
  };
}

// kb_bash 返回
export interface BashResult extends ToolResult {
  blocked?: boolean;
  stdout?: string;
  stderr?: string;
  exitCode?: number;
}

// kb_session 返回
export interface SessionResult extends ToolResult {
  action?: 'init' | 'checkpoint' | 'clear';
  session?: Session;
  checkpoint?: CheckpointData;
}

// kb_dirty 返回
export interface DirtyResult extends ToolResult {
  action?: 'mark' | 'report' | 'clear';
  module?: string;
  report?: DirtyReport;
}

// 脏模块报告
export interface DirtyReport {
  modules: Array<{
    module: string;
    changeTypes: string[];
    files: string[];
  }>;
  syncChecklist: Array<{
    target: string;
    mandatory: boolean;
    reason: string;
  }>;
  intentType?: IntentType;
}

// kb_gate 返回
export interface GateResult extends ToolResult {
  action?: string;
  task?: Task;
  parentTask?: Task;
  childTasks?: Task[];
  spawnManifest?: {
    parentId: string;
    children: Array<{
      taskId: string;
      intentType: string;
      instruction: string;
    }>;
  };
  requiresConfirmation?: boolean;
  requiresHumanIntervention?: boolean;
}

// kb_move 返回
export interface MoveResult extends ToolResult {
  from?: string;
  to?: string;
  referencedBy?: string[];
  autoFixed?: boolean;
}

// kb_search 返回
export interface SearchResult extends ToolResult {
  type?: 'grep' | 'glob' | 'crossref';
  results?: any[];
  stale?: boolean;
  message?: string;
}

// kb_delete 返回
export interface DeleteResult extends ToolResult {
  path?: string;
  soft?: boolean;
  refCount?: number;
  needsConfirmation?: boolean;
  snapshotPath?: string;
  deprecated?: boolean;
}

// kb_index 返回
export interface IndexResult extends ToolResult {
  action?: 'rebuild' | 'status';
  totalFiles?: number;
  totalLinks?: number;
  generatedAt?: string;
  stale?: boolean;
}
