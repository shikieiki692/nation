import { StateManager } from '../state/manager.js';
import { Task } from '../types.js';
export declare class Orchestrator {
    private stateManager;
    private vaultRoot;
    private childArchivedCallbacks;
    private awaitingTimeouts;
    constructor(stateManager: StateManager, vaultRoot: string);
    /**
     * 调度 Task 到 Carrier
     * 当前实现: 仅 PRIMARY Carrier
     */
    schedule(task: Task): string;
    /**
     * 父Task等待子Task完成
     * 父Task状态: EXECUTING → AWAITING
     */
    awaitChildren(parentTaskId: string): boolean;
    /**
     * 子Task完成时调用
     */
    onChildArchived(childTaskId: string): void;
    /**
     * 收工合并 - Session.CLOSING
     * 所有根Task ARCHIVED → 触发
     */
    mergeOnClose(): Promise<{
        success: boolean;
        closingReport?: {
            step1_dirtyModules: string[];
            step2_closingChecklist: Array<{
                target: string;
                mandatory: boolean;
                reason: string;
            }>;
            step3_syncedFiles: string[];
            step4_followupDedup: number;
            step5_historyCleanup: number;
            step6_gateValidation: boolean;
            step7_checkpointWritten: boolean;
        };
    }>;
    /**
     * 生成收工清单
     */
    private generateClosingChecklist;
}
//# sourceMappingURL=orchestrator.d.ts.map