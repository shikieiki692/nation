/**
 * KB Vault MCP Server - State Machine Manager
 * 在内存中维护 Session 和 Task 状态机
 */
import { Session, Task, TaskState, IntentType, FileFingerprint, ValidationError } from '../types.js';
export declare class StateManager {
    private session;
    private tasks;
    private vaultRoot;
    constructor(vaultRoot: string);
    /**
     * 初始化 Session
     */
    initSession(): Promise<{
        session: Session;
        recovered: boolean;
    }>;
    /**
     * 获取当前 Session
     */
    getSession(): Session | null;
    /**
     * 创建新 Task
     */
    createTask(params: {
        intentType: IntentType;
        agentId?: number;
        scale?: string;
        persistence?: string;
        parentId?: string;
    }): Task;
    /**
     * 获取当前活跃 Task
     */
    getCurrentTask(): Task | null;
    /**
     * 设置当前活跃 Task
     */
    setCurrentTaskId(taskId: string | null): void;
    /**
     * 获取指定 Task
     */
    getTask(taskId: string): Task | null;
    /**
     * 更新 Task 状态
     */
    updateTaskState(taskId: string, newState: TaskState): boolean;
    /**
     * 验证状态迁移合法性
     */
    private isValidStateTransition;
    /**
     * 获取所有根 Task（没有 parent 的 Task）
     */
    getRootTasks(): Task[];
    /**
     * 检查所有子 Task 是否都已 ARCHIVED
     */
    areAllChildrenArchived(taskId: string): boolean;
    /**
     * 增加 reworkCount
     */
    incrementReworkCount(taskId: string): number;
    /**
     * 获取 reworkCount
     */
    getReworkCount(taskId: string): number;
    /**
     * 清除指定脏模块
     */
    clearDirtyModule(module: string): void;
    /**
     * 清除所有脏模块
     */
    clearAllDirtyModules(): void;
    /**
     * 标记脏模块
     */
    markDirtyModule(module: string, file?: string, changeType?: string): void;
    /**
     * 获取读取注册表
     */
    getReadRegistry(): Map<string, FileFingerprint>;
    /**
     * 更新读取注册表
     */
    updateReadRegistry(path: string, fingerprint: FileFingerprint): void;
    /**
     * 验证修改操作的前置条件
     * 这是核心的隐式验证链
     */
    validateModification(operation: string, targetPath?: string): ValidationError | null;
    /**
     * 验证 intentType 约束
     */
    private validateIntentConstraint;
    /**
     * 保存检查点（追加写入 JSONL）
     */
    saveCheckpoint(): Promise<void>;
    /**
     * Rotate checkpoint files
     */
    private rotateCheckpoint;
    /**
     * 加载检查点（从 JSONL 恢复）
     */
    private loadCheckpoint;
    /**
     * 清除检查点和内存状态
     */
    clear(): Promise<void>;
    /**
     * 计算文件指纹
     */
    computeFingerprint(filePath: string, content?: string): Promise<FileFingerprint>;
    /**
     * 从文件路径提取模块名
     */
    extractModule(filePath: string): string;
    /**
     * 生成脏模块报告
     */
    generateDirtyReport(): {
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
    };
}
//# sourceMappingURL=manager.d.ts.map