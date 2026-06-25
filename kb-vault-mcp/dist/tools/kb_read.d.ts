/**
 * kb_read - 指纹比对读取工具
 * 只读工具，不检查 Task 状态
 */
import { ReadResult } from '../types.js';
import { StateManager } from '../state/manager.js';
/**
 * 处理 kb_read 请求
 */
export declare function handleKbRead(args: {
    path: string;
    offset?: number;
    limit?: number;
}, stateManager: StateManager, vaultRoot: string): Promise<ReadResult>;
/**
 * kb_read 工具定义
 */
export declare const kbReadTool: {
    name: string;
    description: string;
    inputSchema: {
        type: "object";
        properties: {
            path: {
                type: string;
                description: string;
            };
            offset: {
                type: string;
                description: string;
            };
            limit: {
                type: string;
                description: string;
            };
        };
        required: string[];
    };
};
//# sourceMappingURL=kb_read.d.ts.map