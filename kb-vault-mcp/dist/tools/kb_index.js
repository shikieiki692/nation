/**
 * kb_index - 反向引用索引工具
 * 构建和管理 reverse_index.json 缓存
 */
import * as fs from 'fs/promises';
import * as path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
const execAsync = promisify(exec);
const INDEX_FILE = '.kb/state/reverse_index.json';
/**
 * 扫描全库构建反向索引
 */
async function buildReverseIndex(vaultRoot) {
    const index = {};
    let totalFiles = 0;
    let totalLinks = 0;
    try {
        // 使用 grep 查找所有 wikilink
        const { stdout } = await execAsync(`grep -rn "\\[\\[" "${vaultRoot}" --include="*.md" --exclude-dir=.git --exclude-dir=.claude --exclude-dir=.trash --exclude-dir=node_modules`, { timeout: 60000, maxBuffer: 1024 * 1024 * 50 });
        const lines = stdout.trim().split('\n').filter(l => l.length > 0);
        const fileSet = new Set();
        for (const line of lines) {
            const match = line.match(/^(.+?):(\d+):(.+)$/);
            if (!match)
                continue;
            const [, file, lineNum, content] = match;
            const relativeFile = path.relative(vaultRoot, file);
            fileSet.add(relativeFile);
            // 提取所有 wikilink
            const wikilinkRegex = /\[\[([^\]]+?)\]\]/g;
            let linkMatch;
            while ((linkMatch = wikilinkRegex.exec(content)) !== null) {
                const linkText = linkMatch[1];
                // 规范化链接目标（去掉 # 锚点和 | 别名）
                const target = linkText.split('#')[0].split('|')[0].trim();
                if (target) {
                    if (!index[target]) {
                        index[target] = [];
                    }
                    index[target].push({
                        file: relativeFile,
                        line: parseInt(lineNum),
                        linkText: linkText
                    });
                    totalLinks++;
                }
            }
        }
        totalFiles = fileSet.size;
    }
    catch (error) {
        // grep 返回 1 表示没有匹配，不是错误
        if (error.code !== 1) {
            throw error;
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
//# sourceMappingURL=kb_index.js.map