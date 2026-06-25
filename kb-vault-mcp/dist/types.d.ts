/**
 * KB Vault MCP Server - Type Definitions
 * 基于设计文档的状态机类型系统
 */
export type IntentType = 'BUILD' | 'MAINTAIN' | 'USE' | 'META';
export type Scale = 'TRIVIAL' | 'NORMAL' | 'BATCH' | 'COMPOUND';
export type Persistence = 'FORMAL' | 'EXPLORATORY' | 'NONE';
export type TaskState = 'ASSESSING' | 'PLANNING' | 'EXECUTING' | 'VERIFYING' | 'CLOSING' | 'ARCHIVED' | 'AWAITING' | 'SUSPENDED' | 'ERROR' | 'REWORK';
export type SessionState = 'INIT' | 'ACTIVE' | 'CLOSING' | 'END';
export type Strategy = 'PURE_AGENT' | 'SKILL_DRIVEN' | 'HYBRID';
export interface FileFingerprint {
    path: string;
    version?: string;
    updated?: string;
    contentHash: string;
    readAt: string;
}
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
export interface EditOperation {
    oldText: string;
    newText: string;
}
export interface ValidationError {
    code: string;
    detail: string;
    currentState?: string;
}
export interface ToolResult {
    success: boolean;
    error?: ValidationError;
    [key: string]: any;
}
export interface ReadResult extends ToolResult {
    content?: string;
    skipped?: boolean;
    fingerprint?: FileFingerprint;
}
export interface WriteResult extends ToolResult {
    path?: string;
    dirtyModule?: string;
}
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
export interface BashResult extends ToolResult {
    blocked?: boolean;
    stdout?: string;
    stderr?: string;
    exitCode?: number;
}
export interface SessionResult extends ToolResult {
    action?: 'init' | 'checkpoint' | 'clear';
    session?: Session;
    checkpoint?: CheckpointData;
}
export interface DirtyResult extends ToolResult {
    action?: 'mark' | 'report' | 'clear';
    module?: string;
    report?: DirtyReport;
}
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
export interface MoveResult extends ToolResult {
    from?: string;
    to?: string;
    referencedBy?: string[];
    autoFixed?: boolean;
}
export interface SearchResult extends ToolResult {
    type?: 'grep' | 'glob' | 'crossref';
    results?: any[];
    stale?: boolean;
    message?: string;
}
export interface DeleteResult extends ToolResult {
    path?: string;
    soft?: boolean;
    refCount?: number;
    needsConfirmation?: boolean;
    snapshotPath?: string;
    deprecated?: boolean;
}
export interface IndexResult extends ToolResult {
    action?: 'rebuild' | 'status';
    totalFiles?: number;
    totalLinks?: number;
    generatedAt?: string;
    stale?: boolean;
}
//# sourceMappingURL=types.d.ts.map