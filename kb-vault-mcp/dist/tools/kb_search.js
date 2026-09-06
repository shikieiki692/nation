/**
 * kb_search - 搜索工具
 * 支持 grep/glob/crossref 三种模式
 * 只读工具，不检查状态
 */
import * as fs from 'fs/promises';
import * as path from 'path';
// 统一排除目录（与原 shell 命令的 --exclude-dir / ! -path 规则保持一致）
const EXCLUDED_DIRS = new Set(['.git', '.claude', '.trash', 'node_modules']);
/**
 * 递归遍历文件（纯 Node 实现，Windows/POSIX/中文路径通用）
 * @param root 起始目录
 * @param filter 文件名过滤（如仅 .md），不传则收集所有文件
 */
async function walkFiles(root, filter) {
    const results = [];
    async function walk(dir) {
        let entries;
        try {
            entries = await fs.readdir(dir, { withFileTypes: true });
        }
        catch {
            return; // 目录不可读时跳过
        }
        for (const entry of entries) {
            const full = path.join(dir, entry.name);
            if (entry.isDirectory()) {
                if (!EXCLUDED_DIRS.has(entry.name)) {
                    await walk(full);
                }
            }
            else if (entry.isFile()) {
                if (!filter || filter(entry.name)) {
                    results.push(full);
                }
            }
        }
    }
    await walk(root);
    return results;
}
/**
 * 把 glob 模式转正则（支持 * 单段通配、** 跨目录、? 单字符）
 */
function globToRegExp(glob) {
    const normalized = glob.replace(/\\/g, '/');
    let re = '';
    let i = 0;
    while (i < normalized.length) {
        const c = normalized[i];
        if (c === '*') {
            if (normalized[i + 1] === '*') {
                if (normalized[i + 2] === '/') {
                    re += '(?:.*/)?'; // '**/' 匹配零级或多级目录
                    i += 3;
                }
                else {
                    re += '.*';
                    i += 2;
                }
            }
            else {
                re += '[^/]*'; // '*' 不跨目录段
                i += 1;
            }
        }
        else if (c === '?') {
            re += '[^/]';
            i += 1;
        }
        else {
            re += c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            i += 1;
        }
    }
    return new RegExp(`^${re}$`);
}
/**
 * 转义正则特殊字符
 */
function escapeRegExp(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
/**
 * 执行 grep 搜索
 */
async function grepSearch(query, vaultRoot, scope, caseSensitive) {
    const results = [];
    // query 按正则处理（与原 grep 行为一致）；非法正则回退为字面量匹配
    let regex;
    const flags = caseSensitive ? 'g' : 'gi';
    try {
        regex = new RegExp(query, flags);
    }
    catch {
        regex = new RegExp(escapeRegExp(query), flags);
    }
    const searchPath = scope ? path.join(vaultRoot, scope) : vaultRoot;
    // 一次遍历收集所有结果，避免重复读盘
    const files = await walkFiles(searchPath, name => name.endsWith('.md'));
    for (const file of files) {
        let content;
        try {
            content = await fs.readFile(file, 'utf-8');
        }
        catch {
            continue; // 读失败的文件跳过
        }
        // 兼容 LF/CRLF
        const lines = content.split(/\r?\n/);
        for (let i = 0; i < lines.length; i++) {
            const lineText = lines[i];
            regex.lastIndex = 0;
            const m = regex.exec(lineText);
            if (m) {
                results.push({
                    file: path.relative(vaultRoot, file),
                    line: i + 1,
                    column: m.index + 1,
                    match: lineText.trim(),
                    context: lineText.trim()
                });
            }
        }
    }
    return results;
}
/**
 * 执行 glob 搜索
 */
async function globSearch(pattern, vaultRoot, scope) {
    const searchPath = scope ? path.join(vaultRoot, scope) : vaultRoot;
    const hasSep = /[/\\]/.test(pattern);
    const regex = globToRegExp(pattern);
    const files = await walkFiles(searchPath);
    const results = [];
    for (const file of files) {
        const relativeFile = path.relative(vaultRoot, file);
        // 含路径分隔符的模式对相对路径整体匹配（支持 **），否则只匹配文件名（与 find -name 一致）
        const target = hasSep ? relativeFile.replace(/\\/g, '/') : path.basename(file);
        if (regex.test(target)) {
            results.push(relativeFile);
        }
    }
    return results.sort();
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
                const results = await globSearch(pattern, vaultRoot, scope);
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
