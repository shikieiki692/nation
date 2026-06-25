/**
 * kb_dirty - 脏模块标记/报告/清除工具
 * 依赖活跃 Task 的 intentType 生成特异性收工清单
 */
/**
 * 处理 kb_dirty 请求
 */
export async function handleKbDirty(args, stateManager) {
    const { action, module, file, changeType } = args;
    try {
        switch (action) {
            case 'mark': {
                // 标记脏模块
                if (!module) {
                    return {
                        success: false,
                        action: 'mark',
                        error: {
                            code: 'MISSING_MODULE',
                            detail: 'mark 操作需要指定 module 参数'
                        }
                    };
                }
                stateManager.markDirtyModule(module, file, changeType || 'modify');
                return {
                    success: true,
                    action: 'mark',
                    module
                };
            }
            case 'report': {
                // 生成脏模块报告
                const report = stateManager.generateDirtyReport();
                return {
                    success: true,
                    action: 'report',
                    report
                };
            }
            case 'clear': {
                // 清除脏模块标记
                if (module) {
                    // 清除指定模块
                    stateManager.clearDirtyModule(module);
                    return {
                        success: true,
                        action: 'clear',
                        module
                    };
                }
                else {
                    // 清除所有模块
                    stateManager.clearAllDirtyModules();
                    return {
                        success: true,
                        action: 'clear'
                    };
                }
            }
            default:
                return {
                    success: false,
                    error: {
                        code: 'INVALID_ACTION',
                        detail: `未知操作: ${action}`
                    }
                };
        }
    }
    catch (error) {
        return {
            success: false,
            error: {
                code: 'DIRTY_ERROR',
                detail: `脏模块操作失败: ${error.message}`
            }
        };
    }
}
/**
 * kb_dirty 工具定义
 */
export const kbDirtyTool = {
    name: 'kb_dirty',
    description: '脏模块管理。mark: 标记模块为脏; report: 生成脏模块报告和收工清单; clear: 清除脏模块标记。',
    inputSchema: {
        type: 'object',
        properties: {
            action: {
                type: 'string',
                enum: ['mark', 'report', 'clear'],
                description: '操作类型'
            },
            module: {
                type: 'string',
                description: '模块名称（如 03-知识点）'
            },
            file: {
                type: 'string',
                description: '文件路径（用于 mark）'
            },
            changeType: {
                type: 'string',
                description: '变更类型（write/edit/move/delete，默认 modify）'
            }
        },
        required: ['action']
    }
};
//# sourceMappingURL=kb_dirty.js.map