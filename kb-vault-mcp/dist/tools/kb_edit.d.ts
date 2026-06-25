/**
 * kb_edit - old_string 唯一性验证编辑工具
 * 包含隐式验证链：Session → Task → state → intentType
 */
import { EditResult, EditOperation } from '../types.js';
import { StateManager } from '../state/manager.js';
/**
 * 处理 kb_edit 请求
 */
export declare function handleKbEdit(args: {
    path: string;
    edits: EditOperation[];
    confirm?: boolean;
}, stateManager: StateManager, vaultRoot: string): Promise<EditResult>;
/**
 * kb_edit 工具定义
 */
export declare const kbEditTool: {
    name: string;
    description: string;
    inputSchema: {
        type: "object";
        properties: {
            path: {
                type: string;
                description: string;
            };
            edits: {
                type: string;
                items: {
                    type: string;
                    properties: {
                        oldText: {
                            type: string;
                            description: string;
                        };
                        newText: {
                            type: string;
                            description: string;
                        };
                    };
                    required: string[];
                };
                description: string;
            };
            confirm: {
                type: string;
                description: string;
            };
        };
        required: string[];
    };
};
//# sourceMappingURL=kb_edit.d.ts.map