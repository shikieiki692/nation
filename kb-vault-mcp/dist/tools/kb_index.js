/**
 * kb_index - 反向引用索引工具
 * 构建和管理 reverse_index.json 缓存
 */
import * as fs from 'fs/promises';
import * as path from 'path';
const INDEX_FILE = '.kb/state/reverse_index.json';
// 统一排除目录（与原 grep --exclude-dir 规则保持一致）
const EXCLUDED_DIRS = new Set(['.git', '.claude', '.trash', 'node_modules']);
/**
 * 递归遍历 vault 内所有 .md 文件（纯 Node 实现，兼容中文路径与 LF/CRLF）
 */
async function walkMarkdownFiles(root) {
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
            else if (entry.isFile() && entry.name.endsWith('.md')) {
                results.push(full);
            }
        }
    }
    await walk(root);
    return results;
}
/**
 * 扫描全库构建反向索引
 */
async function buildReverseIndex(vaultRoot) {
    const index = {};
    let totalFiles = 0;
    let totalLinks = 0;
    // 一次遍历收集所有结果，避免重复读盘
    const files = await walkMarkdownFiles(vaultRoot);
    const wikilinkRegex = /\[\[([^\]]+?)\]\]/g;
    for (const file of files) {
        let content;
        try {
            content = await fs.readFile(file, 'utf-8');
        }
        catch {
            continue; // 读失败的文件跳过，不计入 totalFiles
        }
        totalFiles++;
        const relativeFile = path.relative(vaultRoot, file);
        // 兼容 LF/CRLF 逐行扫描
        const lines = content.split(/\r?\n/);
        for (let i = 0; i < lines.length; i++) {
            const lineText = lines[i];
            wikilinkRegex.lastIndex = 0;
            let linkMatch;
            while ((linkMatch = wikilinkRegex.exec(lineText)) !== null) {
                const linkText = linkMatch[1];
                // 规范化链接目标（去掉 # 锚点和 | 别名）
                const target = linkText.split('#')[0].split('|')[0].trim();
                if (target) {
                    if (!index[target]) {
                        index[target] = [];
                    }
                    index[target].push({
                        file: relativeFile,
                        line: i + 1,
                        linkText: linkText
                    });
                    totalLinks++;
                }
            }
        }
    }
    return { index, totalFiles, totalLinks };
}
/**
 * 保存索引到文件
 */
async function saveIndex(vaultRoot, index) {
    const indexPath = path.join(vaultRoot, INDEX_FILE);
    const tmpPath = indexPath + '.tmp';
    await fs.mkdir(path.dirname(indexPath), { recursive: true });
    const data = {
        ...index,
        generatedAt: new Date().toISOString()
    };
    await fs.writeFile(tmpPath, JSON.stringify(data, null, 2), 'utf-8');
    await fs.rename(tmpPath, indexPath);
}
/**
 * 检查索引状态
 */
async function getIndexStatus(vaultRoot) {
    try {
        const indexPath = path.join(vaultRoot, INDEX_FILE);
        const content = await fs.readFile(indexPath, 'utf-8');
        const data = JSON.parse(content);
        const indexAge = Date.now() - new Date(data.generatedAt).getTime();
        return {
            exists: true,
            stale: indexAge > 60 * 60 * 1000, // 1 小时
            generatedAt: data.generatedAt
        };
    }
    catch {
        return { exists: false, stale: true };
    }
}
/**
 * 处理 kb_index 请求
 */
export async function handleKbIndex(args, vaultRoot) {
    const { action } = args;
    try {
        switch (action) {
            case 'rebuild': {
                const { index, totalFiles, totalLinks } = await buildReverseIndex(vaultRoot);
                await saveIndex(vaultRoot, { index });
                return {
                    success: true,
                    action: 'rebuild',
                    totalFiles,
                    totalLinks,
                    generatedAt: new Date().toISOString()
                };
            }
            case 'status': {
                const status = await getIndexStatus(vaultRoot);
                return {
                    success: true,
                    action: 'status',
                    stale: status.stale,
                    generatedAt: status.generatedAt
                };
            }
            default:
                return {
                    success: false,
                    action,
                    error: { code: 'INVALID_ACTION', detail: `未知操作: ${action}` }
                };
        }
    }
    catch (error) {
        return {
            success: false,
            action,
            error: { code: 'INDEX_ERROR', detail: error.message }
        };
    }
}
/**
 * kb_index 工具定义
 */
export const kbIndexTool = {
    name: 'kb_index',
    description: '反向引用索引工具。action=rebuild 重建索引；action=status 查看索引状态。',
    inputSchema: {
        type: 'object',
        properties: {
            action: {
                type: 'string',
                enum: ['rebuild', 'status'],
                description: '操作类型'
            }
        },
        required: ['action']
    }
};
