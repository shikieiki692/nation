/**
 * kb_index - 反向引用索引工具
 * 构建和管理 reverse_index.json 缓存
 */
export interface IndexResult {
    success: boolean;
    action: 'rebuild' | 'status';
    totalFiles?: number;
    totalLinks?: number;
    generatedAt?: string;
    stale?: boolean;
    error?: {
        code: string;
        detail: string;
    };
}
/**
 * 处理 kb_index 请求
 */
export declare function handleKbIndex(args: {
    action: 'rebuild' | 'status';
}, vaultRoot: string): Promise<IndexResult>;
/**
 * kb_index 工具定义
 */
export declare const kbIndexTool: {
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
        };
        required: string[];
    };
};
//# sourceMappingURL=kb_index.d.ts.map