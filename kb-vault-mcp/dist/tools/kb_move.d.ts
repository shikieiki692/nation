/**
 * kb_move - 移动文件工具（含反向引用检查）
 * 包含隐式验证链：Session → Task → state → intentType
 */
import { MoveResult } from '../types.js';
import { StateManager } from '../state/manager.js';
/**
 * 处理 kb_move 请求
 */
export declare function handleKbMove(args: {
    from: string;
    to: string;
    autoFix?: boolean;
}, stateManager: StateManager, vaultRoot: string): Promise<MoveResult>;
/**
 * kb_move 工具定义
 */
export declare const kbMoveTool: {
    name: string;
    description: string;
    inputSchema: {
        type: "object";
        properties: {
            from: {
                type: string;
                description: string;
            };
            to: {
                type: string;
                description: string;
            };
            autoFix: {
                type: string;
                description: string;
            };
        };
        required: string[];
    };
};
//# sourceMappingURL=kb_move.d.ts.map