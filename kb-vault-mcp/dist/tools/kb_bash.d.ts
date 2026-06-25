/**
 * kb_bash - 只读白名单工具
 * 只检查白名单，不检查 Task 状态
 */
import { BashResult } from '../types.js';
import { StateManager } from '../state/manager.js';
/**
 * 处理 kb_bash 请求
 */
export declare function handleKbBash(args: {
    command: string;
    timeout?: number;
}, stateManager: StateManager, vaultRoot: string): Promise<BashResult>;
/**
 * kb_bash 工具定义
 */
export declare const kbBashTool: {
    name: string;
    description: string;
    inputSchema: {
        type: "object";
        properties: {
            command: {
                type: string;
                description: string;
            };
            timeout: {
                type: string;
                description: string;
            };
        };
        required: string[];
    };
};
//# sourceMappingURL=kb_bash.d.ts.map