/**
 * kb_gate - 状态迁移确认工具
 * 创建 Task、确认计划、确认归档
 * Phase B 增强：确认栅栏 + REWORK 计数
 */
/**
 * 处理 kb_gate 请求
 */
export async function handleKbGate(args, stateManager, hookRuntime, orchestrator, vaultRoot) {
    const { action, intentType, agentId, scale, persistence, plan, taskId, confirm, filesModified, parentId } = args;
    try {
        // 检查 Session 是否存在
        const session = stateManager.getSession();
        if (!session) {
            return {
                success: false,
                action,
                error: {
                    code: 'NO_ACTIVE_SESSION',
                    detail: '请先通过 kb_session init 初始化会话'
                }
            };
        }
        switch (action) {
            case 'create': {
                // 创建 Task 实例 → Task.state = ASSESSING
                if (!intentType) {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'MISSING_INTENT_TYPE',
                            detail: 'action=create 需要指定 intentType'
                        }
                    };
                }
                const task = stateManager.createTask({
                    intentType,
                    agentId,
                    scale,
                    persistence,
                    parentId
                });
                // 保存检查点
                await stateManager.saveCheckpoint();
                return {
                    success: true,
                    action: 'create',
                    task
                };
            }
            case 'confirm': {
                // 确认计划 → Task.state = EXECUTING
                const task = taskId
                    ? stateManager.getTask(taskId)
                    : stateManager.getCurrentTask();
                if (!task) {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'NO_ACTIVE_TASK',
                            detail: '没有活跃 Task，请先通过 action=create 创建'
                        }
                    };
                }
                if (task.state !== 'ASSESSING' && task.state !== 'PLANNING') {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'INVALID_TASK_STATE',
                            detail: `Task 当前在 ${task.state} 状态，只有 ASSESSING 或 PLANNING 状态可以迁移到 EXECUTING`,
                            currentState: task.state
                        }
                    };
                }
                // Phase B: H-P03 确认栅栏检查
                if (hookRuntime) {
                    const barrierResult = hookRuntime.checkConfirmationBarrier(task, filesModified || 0);
                    if (barrierResult.requiresConfirmation && !confirm) {
                        return {
                            success: false,
                            action,
                            requiresConfirmation: true,
                            error: {
                                code: 'REQUIRES_CONFIRMATION',
                                detail: barrierResult.reason || '需要用户确认'
                            }
                        };
                    }
                }
                // 如果有计划，保存到 Task
                if (plan) {
                    task.plan = plan;
                }
                // 如果当前是 ASSESSING，先迁移到 PLANNING
                if (task.state === 'ASSESSING') {
                    const successToPlanning = stateManager.updateTaskState(task.id, 'PLANNING');
                    if (!successToPlanning) {
                        return {
                            success: false,
                            action,
                            error: {
                                code: 'STATE_TRANSITION_FAILED',
                                detail: `无法从 ASSESSING 迁移到 PLANNING`
                            }
                        };
                    }
                }
                // 更新状态到 EXECUTING
                const success = stateManager.updateTaskState(task.id, 'EXECUTING');
                if (!success) {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'STATE_TRANSITION_FAILED',
                            detail: `无法从 ${task.state} 迁移到 EXECUTING`
                        }
                    };
                }
                // 保存检查点
                await stateManager.saveCheckpoint();
                return {
                    success: true,
                    action: 'confirm',
                    task
                };
            }
            case 'verify': {
                // 执行完成 → Task.state = VERIFYING
                const task = taskId
                    ? stateManager.getTask(taskId)
                    : stateManager.getCurrentTask();
                if (!task) {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'NO_ACTIVE_TASK',
                            detail: '没有活跃 Task'
                        }
                    };
                }
                if (task.state !== 'EXECUTING') {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'INVALID_TASK_STATE',
                            detail: `Task 当前在 ${task.state} 状态，只有 EXECUTING 状态可以迁移到 VERIFYING`,
                            currentState: task.state
                        }
                    };
                }
                // 更新状态到 VERIFYING
                const success = stateManager.updateTaskState(task.id, 'VERIFYING');
                if (!success) {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'STATE_TRANSITION_FAILED',
                            detail: `无法从 ${task.state} 迁移到 VERIFYING`
                        }
                    };
                }
                // 保存检查点
                await stateManager.saveCheckpoint();
                return {
                    success: true,
                    action: 'verify',
                    task
                };
            }
            case 'close': {
                // 验证通过 → Task.state = CLOSING
                const task = taskId
                    ? stateManager.getTask(taskId)
                    : stateManager.getCurrentTask();
                if (!task) {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'NO_ACTIVE_TASK',
                            detail: '没有活跃 Task'
                        }
                    };
                }
                if (task.state !== 'VERIFYING') {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'INVALID_TASK_STATE',
                            detail: `Task 当前在 ${task.state} 状态，只有 VERIFYING 状态可以迁移到 CLOSING`,
                            currentState: task.state
                        }
                    };
                }
                // Phase B: H-V02 REWORK 计数检查
                if (hookRuntime) {
                    const reworkResult = hookRuntime.checkReworkLimit(task.id);
                    if (!reworkResult.allowed) {
                        // 转为 ERROR 状态
                        stateManager.updateTaskState(task.id, 'ERROR');
                        await stateManager.saveCheckpoint();
                        return {
                            success: false,
                            action,
                            requiresHumanIntervention: true,
                            error: {
                                code: 'REWORK_LIMIT_EXCEEDED',
                                detail: `REWORK 次数超过限制（${reworkResult.reworkCount} > 2），需要人工干预`
                            }
                        };
                    }
                }
                // 更新状态到 CLOSING
                const success = stateManager.updateTaskState(task.id, 'CLOSING');
                if (!success) {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'STATE_TRANSITION_FAILED',
                            detail: `无法从 ${task.state} 迁移到 CLOSING`
                        }
                    };
                }
                // 保存检查点
                await stateManager.saveCheckpoint();
                return {
                    success: true,
                    action: 'close',
                    task
                };
            }
            case 'archive': {
                // 归档 → Task.state = ARCHIVED
                const task = taskId
                    ? stateManager.getTask(taskId)
                    : stateManager.getCurrentTask();
                if (!task) {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'NO_ACTIVE_TASK',
                            detail: '没有活跃 Task'
                        }
                    };
                }
                if (task.state !== 'CLOSING' && task.state !== 'VERIFYING') {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'INVALID_TASK_STATE',
                            detail: `Task 当前在 ${task.state} 状态，只有 CLOSING 或 VERIFYING 状态可以归档`,
                            currentState: task.state
                        }
                    };
                }
                // Phase B: H-V02 REWORK 计数检查
                if (hookRuntime && task.state === 'VERIFYING') {
                    const reworkResult = hookRuntime.checkReworkLimit(task.id);
                    if (!reworkResult.allowed) {
                        // 转为 ERROR 状态
                        stateManager.updateTaskState(task.id, 'ERROR');
                        await stateManager.saveCheckpoint();
                        return {
                            success: false,
                            action,
                            requiresHumanIntervention: true,
                            error: {
                                code: 'REWORK_LIMIT_EXCEEDED',
                                detail: `REWORK 次数超过限制（${reworkResult.reworkCount} > 2），需要人工干预`
                            }
                        };
                    }
                }
                // 更新状态到 ARCHIVED
                const success = stateManager.updateTaskState(task.id, 'ARCHIVED');
                if (!success) {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'STATE_TRANSITION_FAILED',
                            detail: `无法从 ${task.state} 迁移到 ARCHIVED`
                        }
                    };
                }
                // Phase B: H-L03 出口清理
                if (hookRuntime && orchestrator) {
                    await hookRuntime.onTaskArchived(task.id, orchestrator);
                }
                // Phase C: H-L02 任务卡自动生成
                if (hookRuntime && task.persistence === 'FORMAL' && vaultRoot) {
                    await hookRuntime.generateTaskCard(task, vaultRoot);
                }
                // 保存检查点
                await stateManager.saveCheckpoint();
                return {
                    success: true,
                    action: 'archive',
                    task
                };
            }
            case 'spawn': {
                // 动态孵化子 Task（支持单个或批量）
                // 获取父 Task
                const parentTask = taskId
                    ? stateManager.getTask(taskId)
                    : stateManager.getCurrentTask();
                if (!parentTask) {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'NO_ACTIVE_TASK',
                            detail: '没有活跃 Task 作为父 Task'
                        }
                    };
                }
                // 验证父 Task 状态
                if (parentTask.state !== 'EXECUTING') {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'INVALID_TASK_STATE',
                            detail: `父Task当前在 ${parentTask.state} 状态，只有 EXECUTING 状态可以孵化子Task`,
                            currentState: parentTask.state
                        }
                    };
                }
                // 批量孵化：如果有 children 数组
                const children = args.children;
                if (children && Array.isArray(children) && children.length > 0) {
                    const childTasks = [];
                    for (const child of children) {
                        const childTask = stateManager.createTask({
                            intentType: child.intentType || intentType || 'BUILD',
                            agentId: child.agentId ?? agentId,
                            scale: child.scale || scale,
                            persistence: child.persistence || persistence,
                            parentId: parentTask.id
                        });
                        // 子 Task 直接进入 EXECUTING 状态
                        stateManager.updateTaskState(childTask.id, 'PLANNING');
                        stateManager.updateTaskState(childTask.id, 'EXECUTING');
                        childTasks.push(childTask);
                    }
                    // 子 Task 创建完成后，父 Task 进入 AWAITING 状态
                    if (orchestrator) {
                        orchestrator.awaitChildren(parentTask.id);
                    }
                    // 保存检查点
                    await stateManager.saveCheckpoint();
                    return {
                        success: true,
                        action: 'spawn',
                        parentTask,
                        childTasks,
                        spawnManifest: {
                            parentId: parentTask.id,
                            children: childTasks.map(t => ({
                                taskId: t.id,
                                intentType: t.intentType,
                                instruction: `调用 kb_gate action=confirm 启动子Task ${t.id}`
                            }))
                        }
                    };
                }
                // 单子 Task 创建（兼容旧接口）
                if (!intentType) {
                    return {
                        success: false,
                        action,
                        error: {
                            code: 'MISSING_INTENT_TYPE',
                            detail: 'action=spawn 需要指定 intentType（单子Task模式）'
                        }
                    };
                }
                const childTask = stateManager.createTask({
                    intentType,
                    agentId,
                    scale,
                    persistence,
                    parentId: parentTask.id
                });
                // 子 Task 直接进入 EXECUTING 状态
                stateManager.updateTaskState(childTask.id, 'PLANNING');
                stateManager.updateTaskState(childTask.id, 'EXECUTING');
                // 子 Task 创建完成后，父 Task 进入 AWAITING 状态
                if (orchestrator) {
                    orchestrator.awaitChildren(parentTask.id);
                }
                // 保存检查点
                await stateManager.saveCheckpoint();
                return {
                    success: true,
                    action: 'spawn',
                    task: childTask,
                    parentTask
                };
            }
            default:
                return {
                    success: false,
                    action,
                    error: {
                        code: 'INVALID_ACTION',
                        detail: `未知操作: ${action}，支持 create、confirm、verify、close、archive、spawn`
                    }
                };
        }
    }
    catch (error) {
        return {
            success: false,
            action,
            error: {
                code: 'GATE_ERROR',
                detail: `状态迁移失败: ${error.message}`
            }
        };
    }
}
/**
 * kb_gate 工具定义
 */
export const kbGateTool = {
    name: 'kb_gate',
    description: '状态迁移确认点。action=create: 创建 Task; action=confirm: 确认计划进入 EXECUTING; action=archive: 归档 Task; action=spawn: 动态孵化子 Task。',
    inputSchema: {
        type: 'object',
        properties: {
            action: {
                type: 'string',
                enum: ['create', 'confirm', 'verify', 'close', 'archive', 'spawn'],
                description: '操作类型：create=创建Task, confirm=确认计划, verify=执行完成, close=验证通过, archive=归档, spawn=孵化子Task'
            },
            intentType: {
                type: 'string',
                enum: ['BUILD', 'MAINTAIN', 'USE', 'META'],
                description: '意图类型（action=create 必需）'
            },
            agentId: {
                type: 'number',
                description: 'Agent ID（可选）'
            },
            scale: {
                type: 'string',
                enum: ['TRIVIAL', 'NORMAL', 'BATCH', 'COMPOUND'],
                description: '规模（可选）'
            },
            persistence: {
                type: 'string',
                enum: ['FORMAL', 'EXPLORATORY', 'NONE'],
                description: '持久化类型（可选）'
            },
            plan: {
                type: 'object',
                description: '执行计划（action=confirm 可选）',
                properties: {
                    sources: { type: 'array', items: { type: 'string' } },
                    targets: { type: 'array', items: { type: 'string' } },
                    batches: { type: 'array', items: { type: 'array', items: { type: 'string' } } },
                    risks: { type: 'array', items: { type: 'string' } }
                }
            },
            taskId: {
                type: 'string',
                description: '指定 Task ID（可选，默认使用当前 Task）'
            },
            confirm: {
                type: 'boolean',
                description: '用户确认标志（MAINTAIN≥5/META 时需要）'
            },
            filesModified: {
                type: 'number',
                description: '已修改文件数（用于确认栅栏检查）'
            },
            parentId: {
                type: 'string',
                description: '父 Task ID（用于创建子 Task）'
            },
            children: {
                type: 'array',
                description: '子Task列表（批量孵化时使用）',
                items: {
                    type: 'object',
                    properties: {
                        intentType: { type: 'string', enum: ['BUILD', 'MAINTAIN', 'USE', 'META'] },
                        agentId: { type: 'number' },
                        scale: { type: 'string', enum: ['TRIVIAL', 'NORMAL', 'BATCH', 'COMPOUND'] },
                        persistence: { type: 'string', enum: ['FORMAL', 'EXPLORATORY', 'NONE'] }
                    }
                }
            }
        },
        required: ['action']
    }
};
//# sourceMappingURL=kb_gate.js.map