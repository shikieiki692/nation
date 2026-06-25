/**
 * kb_dirty - 脏模块标记/报告/清除工具
 * 依赖活跃 Task 的 intentType 生成特异性收工清单
 */
import { DirtyResult } from '../types.js';
import { StateManager } from '../state/manager.js';
/**
 * 处理 kb_dirty 请求
 */
export declare function handleKbDirty(args: {
    action: 'mark' | 'report' | 'clear';
    module?: string;
    file?: string;
    changeType?: string;
}, stateManager: StateManager): Promise<DirtyResult>;
/**
 * kb_dirty 工具定义
 */
export declare const kbDirtyTool: {
    name: string;
    description: string;
    inputSchema: {
        type: "object";
        properties: {
            action: {
                type: string;
                enum: string[];
                description: string;
            };
            module: {
                type: string;
                description: string;
            };
            file: {
                type: string;
                description: string;
            };
            changeType: {
                type: string;
                description: string;
            };
        };
        required: string[];
    };
};
//# sourceMappingURL=kb_dirty.d.ts.map