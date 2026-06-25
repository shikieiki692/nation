/**
 * kb_search - 搜索工具
 * 支持 grep/glob/crossref 三种模式
 * 只读工具，不检查状态
 */
import * as fs from 'fs/promises';
import * as path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
const execAsync = promisify(exec);
/**
 * 执行 grep 搜索
 */
async function grepSearch(query, vaultRoot, scope, caseSensitive) {
    const results = [];
    try {
        const searchPath = scope ? path.join(vaultRoot, scope) : vaultRoot;
        const caseFlag = caseSensitive ? '' : '-i';
        // 排除 .git/.claude/trash/node_modules
        const excludePattern = '--exclude-dir=.git --exclude-dir=.claude --exclude-dir=.trash --exclude-dir=node_modules';
        const { stdout } = await execAsync(`grep -rn ${caseFlag} ${excludePattern} "${query}" "${searchPath}" --include="*.md"`, { timeout: 30000, maxBuffer: 1024 * 1024 * 10 });
        const lines = stdout.trim().split('\n').filter(l => l.length > 0);
        for (const line of lines) {
            // 格式: file:line:content
            const match = line.match(/^(.+?):(\d+):(.+)$/);
            if (match) {
                const [, file, lineNum, content] = match;
                const relativeFile = path.relative(vaultRoot, file);
                results.push({
                    file: relativeFile,
                    line: parseInt(lineNum),
                    column: content.indexOf(query) + 1,
                    match: content.trim(),
                    context: content.trim()
                });
            }
        }
    }
    catch (error) {
        // grep 返回空结果时会抛出异常
        if (error.code !== 1) {
            throw error;
        }
    }
    return results;
}
/**
 * 执行 glob 搜索
 */
async function globSearch(pattern, vaultRoot) {
    try {
        const { stdout } = await execAsync(`find "${vaultRoot}" -name "${pattern}" -type f ! -path "*/.git/*" ! -path "*/.claude/*" ! -path "*/.trash/*" ! -path "*/node_modules/*"`, { timeout: 10000 });
        return stdout.trim()
            .split('\n')
            .filter(f => f.length > 0)
            .map(f => path.relative(vaultRoot, f));
    }
    catch {
        return [];
    }
}
/**
 * 从缓存加载反向索引
 */
async function loadReverseIndex(vaultRoot) {
    try {
        const indexPath = path.join(vaultRoot, '.kb/state/reverse_index.json');
        const content = await fs.readFile(indexPath, 'utf-8');
        return JSON.parse(content);
    }
    catch {
        return null;
    }
}
/**
 * 检查索引是否过期
 */
async function isIndexStale(vaultRoot) {
    try {
        const indexPath = path.join(vaultRoot, '.kb/state/reverse_index.json');
        const stat = await fs.stat(indexPath);
        const indexAge = Date.now() - stat.mtimeMs;
        // 索引超过 1 小时视为过期
        return indexAge > 60 * 60 * 1000;
    }
    catch {
        return true; // 索引不存在视为过期
    }
}
/**
 * 处理 kb_search 请求
 */
export async function handleKbSearch(args, vaultRoot) {
    const { type, query, pattern, scope, caseSensitive } = args;
    try {
        switch (type) {
            case 'grep': {
                if (!query) {
                    return {
                        success: false,
                        type: 'grep',
                        error: { code: 'MISSING_QUERY', detail: 'grep 搜索需要 query 参数' }
                    };
                }
                const results = await grepSearch(query, vaultRoot, scope, caseSensitive);
                return { success: true, type: 'grep', results };
            }
            case 'glob': {
                if (!pattern) {
                    return {
                        success: false,
                        type: 'glob',
                        error: { code: 'MISSING_PATTERN', detail: 'glob 搜索需要 pattern 参数' }
                    };
                }
                const results = await globSearch(pattern, vaultRoot);
                return { success: true, type: 'glob', results };
            }
            case 'crossref': {
                if (!query) {
                    return {
                        success: false,
                        type: 'crossref',
                        error: { code: 'MISSING_QUERY', detail: 'crossref 搜索需要 query 参数（目标文件名）' }
                    };
                }
                // 尝试从缓存加载
                const index = await loadReverseIndex(vaultRoot);
                const stale = await isIndexStale(vaultRoot);
                if (index && !stale) {
                    // 从缓存查找
                    const normalizedQuery = query.replace(/\.md$/, '');
                    const indexData = (index.index || {});
                    const referencedBy = indexData[normalizedQuery] || [];
                    return {
                        success: true,
                        type: 'crossref',
                        results: [{ target: normalizedQuery, referencedBy }],
                        stale: false
                    };
                }
                else {
                    // 回退到 grep 搜索
                    const grepResults = await grepSearch(`\\[\\[${query}\\]\\]`, vaultRoot, scope, false);
                    const referencedBy = grepResults.map(r => ({
                        file: r.file,
                        line: r.line,
                        linkText: query
                    }));
                    return {
                        success: true,
                        type: 'crossref',
                        results: [{ target: query, referencedBy }],
                        stale: true,
                        message: '反向索引需更新，请运行 kb_index action=rebuild'
                    };
                }
            }
            default:
                return {
                    success: false,
                    type,
                    error: { code: 'INVALID_TYPE', detail: `未知搜索类型: ${type}` }
                };
        }
    }
    catch (error) {
        return {
            success: false,
            type,
            error: { code: 'SEARCH_ERROR', detail: error.message }
        };
    }
}
/**
 * kb_search 工具定义
 */
export const kbSearchTool = {
    name: 'kb_search',
    description: '搜索工具。type=grep 文本搜索；type=glob 文件匹配；type=crossref 反向引用查询。',
    inputSchema: {
        type: 'object',
        properties: {
            type: {
                type: 'string',
                enum: ['grep', 'glob', 'crossref'],
                description: '搜索类型'
            },
            query: {
                type: 'string',
                description: '搜索关键词（grep/crossref 必需）'
            },
            pattern: {
                type: 'string',
                description: '文件匹配模式（glob 必需，如 *.md）'
            },
            scope: {
                type: 'string',
                description: '搜索范围（子目录）'
            },
            caseSensitive: {
                type: 'boolean',
                description: '是否区分大小写（默认 false）'
            }
        },
        required: ['type']
    }
};
//# sourceMappingURL=kb_search.js.map