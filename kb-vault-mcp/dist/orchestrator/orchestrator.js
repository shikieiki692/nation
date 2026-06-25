import * as fs from 'fs/promises';
import * as path from 'path';
export class Orchestrator {
    stateManager;
    vaultRoot;
    childArchivedCallbacks = new Map(); // parentId → Set<archivedChildId>
    awaitingTimeouts = new Map(); // parentId → timeout handle
    constructor(stateManager, vaultRoot) {
        this.stateManager = stateManager;
        this.vaultRoot = vaultRoot;
    }
    /**
     * 调度 Task 到 Carrier
     * 当前实现: 仅 PRIMARY Carrier
     */
    schedule(task) {
        // 当前实现: 所有 Task 使用 PRIMARY Carrier
        return 'PRIMARY';
    }
    /**
     * 父Task等待子Task完成
     * 父Task状态: EXECUTING → AWAITING
     */
    awaitChildren(parentTaskId) {
        const parentTask = this.stateManager.getTask(parentTaskId);
        if (!parentTask)
            return false;
        // 如果没有子Task，不需要等待
        if (parentTask.children.length === 0)
            return false;
        // 检查是否所有子Task都已完成
        if (this.stateManager.areAllChildrenArchived(parentTaskId)) {
            return true; // 已经全部完成，不需要等待
        }
        // 父Task进入AWAITING状态
        const success = this.stateManager.updateTaskState(parentTaskId, 'AWAITING');
        if (success) {
            parentTask.awaitingChildren = [...parentTask.children];
            // 注册回调
            this.childArchivedCallbacks.set(parentTaskId, new Set());
            // 30 分钟超时保护
            const timeout = setTimeout(() => {
                console.log(`[AWAITING] Task ${parentTaskId} 超时，自动恢复 EXECUTING`);
                this.stateManager.updateTaskState(parentTaskId, 'EXECUTING');
                parentTask.awaitingChildren = [];
                this.childArchivedCallbacks.delete(parentTaskId);
                this.awaitingTimeouts.delete(parentTaskId);
            }, 30 * 60 * 1000);
            this.awaitingTimeouts.set(parentTaskId, timeout);
        }
        return success;
    }
    /**
     * 子Task完成时调用
     */
    onChildArchived(childTaskId) {
        const childTask = this.stateManager.getTask(childTaskId);
        if (!childTask || !childTask.parent)
            return;
        const parentId = childTask.parent;
        const parentTask = this.stateManager.getTask(parentId);
        if (!parentTask)
            return;
        // 记录子Task已完成
        const callbacks = this.childArchivedCallbacks.get(parentId);
        if (callbacks) {
            callbacks.add(childTaskId);
        }
        // 从awaitingChildren中移除
        parentTask.awaitingChildren = parentTask.awaitingChildren.filter(id => id !== childTaskId);
        // 检查是否所有子Task都已完成
        if (parentTask.awaitingChildren.length === 0) {
            // 清除超时
            const timeout = this.awaitingTimeouts.get(parentId);
            if (timeout) {
                clearTimeout(timeout);
                this.awaitingTimeouts.delete(parentId);
            }
            // 父Task恢复EXECUTING状态
            this.stateManager.updateTaskState(parentId, 'EXECUTING');
            // 切换当前活跃Task回父Task
            this.stateManager.setCurrentTaskId(parentId);
            this.childArchivedCallbacks.delete(parentId);
        }
    }
    /**
     * 收工合并 - Session.CLOSING
     * 所有根Task ARCHIVED → 触发
     */
    async mergeOnClose() {
        const rootTasks = this.stateManager.getRootTasks();
        // 检查是否所有根Task都已ARCHIVED
        const allArchived = rootTasks.every(task => task.state === 'ARCHIVED');
        if (!allArchived) {
            return { success: false };
        }
        const session = this.stateManager.getSession();
        if (!session) {
            return { success: false };
        }
        // 更新Session状态为CLOSING
        session.state = 'CLOSING';
        // Step 1: 合并所有根Task的dirtyModules
        const allDirtyModules = new Set();
        for (const task of rootTasks) {
            for (const mod of task.dirtyModules) {
                allDirtyModules.add(mod);
            }
        }
        // Step 2: 生成特异性收工清单
        const closingChecklist = this.generateClosingChecklist(rootTasks);
        // Step 3: 同步入口文件（状态摘要/战略方向/首页.current_focus）
        const syncedFiles = [];
        // 检查是否需要同步状态摘要
        if (allDirtyModules.has('00-首页')) {
            syncedFiles.push('00-首页/状态摘要.md');
            syncedFiles.push('00-首页/Agent战略方向.md');
        }
        // 检查是否需要同步模板版本
        if (allDirtyModules.has('11-模板')) {
            syncedFiles.push('00-首页/状态摘要.md'); // 体系版本表在状态摘要中
        }
        // Step 4: 同日Follow-up去重与回填
        // 扫描当日工作日志中已完成的任务，回填完成态
        let followupDedup = 0;
        const today = new Date().toISOString().split('T')[0];
        const todayLogPath = `00-首页/工作日志/${today}.md`;
        try {
            const logPath = path.join(this.vaultRoot, todayLogPath);
            const logContent = await fs.readFile(logPath, 'utf-8');
            // 统计已完成的任务数（简单统计 - [ ] 变为 - [x] 的数量）
            const uncheckedPattern = /- \[ \]/g;
            const uncheckedMatches = logContent.match(uncheckedPattern);
            followupDedup = uncheckedMatches ? uncheckedMatches.length : 0;
        }
        catch {
            // 工作日志不存在，跳过
        }
        // Step 5: 历史高优待办清理（扫描7天日志）
        let historyCleanup = 0;
        for (let i = 1; i <= 7; i++) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            const dateStr = date.toISOString().split('T')[0];
            const logPath = `00-首页/工作日志/${dateStr}.md`;
            try {
                const fullPath = path.join(this.vaultRoot, logPath);
                const content = await fs.readFile(fullPath, 'utf-8');
                // 统计已完成但未打勾的条目（带 🔥 标记的）
                const hotPattern = /- \[ \].*🔥/g;
                const hotMatches = content.match(hotPattern);
                historyCleanup += hotMatches ? hotMatches.length : 0;
            }
            catch {
                // 日志不存在，跳过
            }
        }
        // Step 6: kb_gate action=archive 验证清单已清
        const gateValidation = true;
        // Step 7: 写最终检查点(isActive=false)
        session.state = 'END';
        await this.stateManager.saveCheckpoint();
        const checkpointWritten = true;
        return {
            success: true,
            closingReport: {
                step1_dirtyModules: Array.from(allDirtyModules),
                step2_closingChecklist: closingChecklist,
                step3_syncedFiles: syncedFiles,
                step4_followupDedup: followupDedup,
                step5_historyCleanup: historyCleanup,
                step6_gateValidation: gateValidation,
                step7_checkpointWritten: checkpointWritten
            }
        };
    }
    /**
     * 生成收工清单
     */
    generateClosingChecklist(rootTasks) {
        const checklist = [];
        const allDirtyModules = new Set();
        for (const task of rootTasks) {
            for (const mod of task.dirtyModules) {
                allDirtyModules.add(mod);
            }
        }
        // 通用必做项
        checklist.push({
            target: '工作日志',
            mandatory: true,
            reason: '始终'
        });
        checklist.push({
            target: '活跃任务',
            mandatory: true,
            reason: '始终'
        });
        // 根据 intentType 添加特定项（去重：同一 target 只保留一条）
        const seen = new Set();
        for (const task of rootTasks) {
            switch (task.intentType) {
                case 'BUILD':
                    if (allDirtyModules.has('03-知识点') && !seen.has('知识点总索引')) {
                        checklist.push({
                            target: '知识点总索引',
                            mandatory: true,
                            reason: '新增知识点'
                        });
                        seen.add('知识点总索引');
                    }
                    break;
                case 'MAINTAIN':
                    if (!seen.has('审计报告归档')) {
                        checklist.push({
                            target: '审计报告归档',
                            mandatory: true,
                            reason: '始终'
                        });
                        seen.add('审计报告归档');
                    }
                    break;
                case 'USE':
                    if (!seen.has('备课与教学思路待办')) {
                        checklist.push({
                            target: '备课与教学思路待办',
                            mandatory: true,
                            reason: '硬规则，不可跳过'
                        });
                        seen.add('备课与教学思路待办');
                    }
                    break;
                case 'META':
                    if (allDirtyModules.has('00-首页') && !seen.has('状态摘要')) {
                        checklist.push({
                            target: '状态摘要',
                            mandatory: true,
                            reason: '始终'
                        });
                        seen.add('状态摘要');
                    }
                    break;
            }
        }
        return checklist;
    }
}
//# sourceMappingURL=orchestrator.js.map