/**
 * kb_write - 冲突检测写入工具
 * 包含隐式验证链：Session → Task → state → intentType
 */
import { WriteResult } from '../types.js';
import { StateManager } from '../state/manager.js';
/**
 * 处理 kb_write 请求
 */
export declare function handleKbWrite(args: {
    path: string;
    content: string;
}, stateManager: StateManager, vaultRoot: string): Promise<WriteResult>;
/**
 * kb_write 工具定义
 */
export declare const kbWriteTool: {
    name: string;
    description: string;
    inputSchema: {
        type: "object";
        properties: {
            path: {
                type: string;
                description: string;
            };
            content: {
                type: string;
                description: string;
            };
        };
        required: string[];
    };
};
//# sourceMappingURL=kb_write.d.ts.map