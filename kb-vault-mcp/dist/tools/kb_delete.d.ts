/**
 * kb_delete - 删除工具（软弃用 + 快照）
 * 包含隐式验证链：Session → Task → state → intentType
 */
import { ToolResult } from '../types.js';
import { StateManager } from '../state/manager.js';
export interface DeleteResult extends ToolResult {
    path?: string;
    soft?: boolean;
    refCount?: number;
    needsConfirmation?: boolean;
    snapshotPath?: string;
    deprecated?: boolean;
}
/**
 * 处理 kb_delete 请求
 */
export declare function handleKbDelete(args: {
    path: string;
    confirm?: boolean;
    soft?: boolean;
    supersededBy?: string;
}, stateManager: StateManager, vaultRoot: string): Promise<DeleteResult>;
/**
 * kb_delete 工具定义
 */
export declare const kbDeleteTool: {
    name: string;
    description: string;
    inputSchema: {
        type: "object";
        properties: {
            path: {
                type: string;
                description: string;
            };
            confirm: {
                type: string;
                description: string;
            };
            soft: {
                type: string;
                description: string;
            };
            supersededBy: {
                type: string;
                description: string;
            };
        };
        required: string[];
    };
};
//# sourceMappingURL=kb_delete.d.ts.map