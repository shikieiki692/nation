/**
 * kb_delete - 删除工具（软弃用 + 快照）
 * 包含隐式验证链：Session → Task → state → intentType
 */
import * as fs from 'fs/promises';
import * as path from 'path';
/**
 * 查询文件的反向引用数
 */
async function getRefCount(filePath, vaultRoot) {
    try {
        const fileName = path.basename(filePath, path.extname(filePath));
        const { exec } = await import('child_process');
        const { promisify } = await import('util');
        const execAsync = promisify(exec);
        const { stdout } = await execAsync(`grep -r "\\[\\[${fileName}\\]\\]" "${vaultRoot}" --include="*.md" -l --exclude-dir=.git --exclude-dir=.claude --exclude-dir=.trash | wc -l`, { timeout: 10000 });
        return parseInt(stdout.trim()) || 0;
    }
    catch {
        return 0;
    }
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
    // 检查是否有 frontmatter
    if (content.startsWith('---')) {
        // 在 frontmatter 中添加弃用字段
        content = content.replace(/^(---\n)/, `$1deprecated: true\ndeprecatedDate: ${dateStr}\nsunsetDate: ${sunsetDate}\n${supersededBy ? `supersededBy: ${supersededBy}\n` : ''}`);
    }
    else {
        // 添加 frontmatter
        content = `---\ndeprecated: true\ndeprecatedDate: ${dateStr}\nsunsetDate: ${sunsetDate}\n${supersededBy ? `supersededBy: ${supersededBy}\n` : ''}---\n${content}`;
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
//# sourceMappingURL=kb_delete.js.map