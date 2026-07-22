/**
 * kb_delete - 删除工具（软弃用 + 快照）
 * 包含隐式验证链：Session → Task → state → intentType
 */
import * as fs from 'fs/promises';
import * as path from 'path';
// 统一排除目录（与 kb_search/kb_index/kb_move 保持一致）
const EXCLUDED_DIRS = new Set(['.git', '.claude', '.trash', 'node_modules']);
/**
 * 递归遍历 vault 内所有 .md 文件（纯 Node 实现，Windows/POSIX/中文路径通用）
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
 * 提取文本中的所有 wikilink 目标（去掉 # 锚点和 | 别名）
 */
function extractWikilinkTargets(content) {
    const targets = [];
    const re = /\[\[([^\]]+?)\]\]/g;
    let m;
    while ((m = re.exec(content)) !== null) {
        const target = m[1].split('#')[0].split('|')[0].trim();
        if (target) {
            targets.push(target);
        }
    }
    return targets;
}
/**
 * 判断 wikilink 目标是否指向指定文件名
 * 兼容 [[文件名]]、[[路径/文件名]]、[[文件名|别名]]、[[文件名#锚点]]，正/反斜杠均可
 */
function linkTargetsFile(target, fileName) {
    const base = target.replace(/\\/g, '/').split('/').pop() || target;
    return base === fileName || base === `${fileName}.md`;
}
/**
 * 查询文件的反向引用数
 */
async function getRefCount(filePath, vaultRoot) {
    const fileName = path.basename(filePath, path.extname(filePath));
    let count = 0;
    // 一次遍历统计所有引用文件（纯 Node 实现，Windows 上不再静默返回 0）
    const files = await walkMarkdownFiles(vaultRoot);
    for (const file of files) {
        let content;
        try {
            content = await fs.readFile(file, 'utf-8');
        }
        catch {
            continue; // 读失败的文件跳过
        }
        const targets = extractWikilinkTargets(content);
        if (targets.some(t => linkTargetsFile(t, fileName))) {
            count++;
        }
    }
    return count;
}
/**
 * 创建文件快照
 */
async function createSnapshot(filePath, vaultRoot) {
    const fileName = path.basename(filePath);
    const date = new Date().toISOString().split('T')[0];
    const trashDir = path.join(vaultRoot, '.claude/trash', date);
    await fs.mkdir(trashDir, { recursive: true });
    const snapshotPath = path.join(trashDir, fileName);
    await fs.copyFile(filePath, snapshotPath);
    return path.relative(vaultRoot, snapshotPath);
}
/**
 * 软弃用文件（修改 frontmatter）
 */
async function softDeprecate(filePath, supersededBy) {
    let content = await fs.readFile(filePath, 'utf-8');
    const now = new Date();
    const dateStr = now.toISOString().split('T')[0];
    const sunsetDate = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    // 兼容 LF/CRLF：沿用文件原有换行符，避免 frontmatter 插入错位
    const eol = content.includes('\r\n') ? '\r\n' : '\n';
    const fields = `deprecated: true${eol}` +
        `deprecatedDate: ${dateStr}${eol}` +
        `sunsetDate: ${sunsetDate}${eol}` +
        (supersededBy ? `supersededBy: ${supersededBy}${eol}` : '');
    // 检查是否有 frontmatter（同时兼容 ---\n 和 ---\r\n）
    if (/^---\r?\n/.test(content)) {
        // 在 frontmatter 中添加弃用字段
        content = content.replace(/^---\r?\n/, `---${eol}${fields}`);
    }
    else {
        // 添加 frontmatter
        content = `---${eol}${fields}---${eol}${content}`;
    }
    await fs.writeFile(filePath, content, 'utf-8');
}
/**
 * 处理 kb_delete 请求
 */
export async function handleKbDelete(args, stateManager, vaultRoot) {
    const { path: filePath, confirm = false, soft = false, supersededBy } = args;
    // 解析完整路径
    const fullPath = path.isAbsolute(filePath) ? filePath : path.resolve(vaultRoot, filePath);
    const relativePath = path.relative(vaultRoot, fullPath);
    // 验证路径在 vault 内
    if (!fullPath.startsWith(path.resolve(vaultRoot))) {
        return {
            success: false,
            error: { code: 'PATH_OUTSIDE_VAULT', detail: '路径不在 vault 内' }
        };
    }
    // 🔒 隐式验证链
    const validationError = stateManager.validateModification('delete', relativePath);
    if (validationError) {
        return {
            success: false,
            error: validationError
        };
    }
    try {
        // 检查文件是否存在
        try {
            await fs.access(fullPath);
        }
        catch {
            return {
                success: false,
                error: { code: 'FILE_NOT_FOUND', detail: `文件不存在: ${relativePath}` }
            };
        }
        // 查询引用数
        const refCount = await getRefCount(relativePath, vaultRoot);
        // 检查是否需要确认
        if (!confirm) {
            return {
                success: false,
                needsConfirmation: true,
                path: relativePath,
                refCount,
                error: {
                    code: 'NEEDS_CONFIRMATION',
                    detail: `文件被 ${refCount} 个文件引用，需要 confirm=true 确认删除`
                }
            };
        }
        // 获取当前 Task
        const task = stateManager.getCurrentTask();
        // 判断是否需要软弃用
        const shouldSoftDelete = soft || (task?.intentType === 'MAINTAIN' && refCount > 0);
        if (shouldSoftDelete) {
            // 软弃用
            await softDeprecate(fullPath, supersededBy);
            // 标脏模块
            const module = stateManager.extractModule(relativePath);
            stateManager.markDirtyModule(module, relativePath, 'delete');
            return {
                success: true,
                path: relativePath,
                soft: true,
                refCount,
                deprecated: true
            };
        }
        else {
            // 物理删除
            // 1. 创建快照
            const snapshotPath = await createSnapshot(fullPath, vaultRoot);
            // 2. 删除原文件
            await fs.unlink(fullPath);
            // 标脏模块
            const module = stateManager.extractModule(relativePath);
            stateManager.markDirtyModule(module, relativePath, 'delete');
            return {
                success: true,
                path: relativePath,
                soft: false,
                refCount,
                snapshotPath
            };
        }
    }
    catch (error) {
        return {
            success: false,
            error: { code: 'DELETE_ERROR', detail: `删除文件失败: ${error.message}` }
        };
    }
}
/**
 * kb_delete 工具定义
 */
export const kbDeleteTool = {
    name: 'kb_delete',
    description: '删除文件。支持软弃用（保留文件+标记deprecated）和物理删除（先快照再删除）。需要 Task 处于 EXECUTING 状态。',
    inputSchema: {
        type: 'object',
        properties: {
            path: {
                type: 'string',
                description: '文件路径'
            },
            confirm: {
                type: 'boolean',
                description: '确认删除（默认 false）'
            },
            soft: {
                type: 'boolean',
                description: '是否软弃用（默认 false，MAINTAIN 意图有引用时自动启用）'
            },
            supersededBy: {
                type: 'string',
                description: '替代文件（软弃用时可选）'
            }
        },
        required: ['path']
    }
};
