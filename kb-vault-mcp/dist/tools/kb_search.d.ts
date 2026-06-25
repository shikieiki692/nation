/**
 * kb_search - 搜索工具
 * 支持 grep/glob/crossref 三种模式
 * 只读工具，不检查状态
 */
export interface SearchResult {
    success: boolean;
    type: 'grep' | 'glob' | 'crossref';
    results?: any[];
    stale?: boolean;
    message?: string;
    error?: {
        code: string;
        detail: string;
    };
}
export interface GrepResult {
    file: string;
    line: number;
    column: number;
    match: string;
    context: string;
}
export interface CrossRefResult {
    target: string;
    referencedBy: Array<{
        file: string;
        line: number;
        linkText: string;
    }>;
}
/**
 * 处理 kb_search 请求
 */
export declare function handleKbSearch(args: {
    type: 'grep' | 'glob' | 'crossref';
    query?: string;
    pattern?: string;
    scope?: string;
    caseSensitive?: boolean;
}, vaultRoot: string): Promise<SearchResult>;
/**
 * kb_search 工具定义
 */
export declare const kbSearchTool: {
    name: string;
    description: string;
    inputSchema: {
        type: "object";
        properties: {
            type: {
                type: string;
                enum: string[];
                description: string;
            };
            query: {
                type: string;
                description: string;
            };
            pattern: {
                type: string;
                description: string;
            };
            scope: {
                type: string;
                description: string;
            };
            caseSensitive: {
                type: string;
                description: string;
            };
        };
        required: string[];
    };
};
//# sourceMappingURL=kb_search.d.ts.map