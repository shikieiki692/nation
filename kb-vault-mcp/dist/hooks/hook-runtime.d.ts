import { StateManager } from '../state/manager.js';
import { Task } from '../types.js';
export declare class HookRuntime {
    private stateManager;
    private vaultRoot;
    private operationCount;
    private readonly CHECKPOINT_INTERVAL;
    constructor(stateManager: StateManager, vaultRoot: string);
    /**
     * H-G01: 会话初始化
     * 时机: kb_session init
     */
    onSessionInit(): Promise<void>;
    /**
     * H-E03: 进度检查点
     * 时机: kb_write/kb_edit 调用后
     */
    onOperationComplete(): Promise<boolean>;
    /**
     * H-P03: 确认栅栏
     * 时机: kb_gate action=confirm
     */
    checkConfirmationBarrier(task: Task, filesModified: number): {
        requiresConfirmation: boolean;
        reason?: string;
    };
    /**
     * H-V02: REWORK 计数
     * 时机: VERIFYING → REWORK 转换时
     */
    checkReworkLimit(taskId: string): {
        allowed: boolean;
        reworkCount: number;
        requiresHumanIntervention?: boolean;
    };
    /**
     * H-L03: 出口清理
     * 时机: Task → ARCHIVED
     */
    onTaskArchived(taskId: string, orchestrator: any): Promise<void>;
    /**
     * H-L02: 任务卡自动生成
     * 时机: Task → ARCHIVED 时
     */
    generateTaskCard(task: Task, vaultRoot: string): Promise<string | null>;
    /**
     * 重置操作计数器
     */
    resetOperationCount(): void;
}
//# sourceMappingURL=hook-runtime.d.ts.map