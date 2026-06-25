/**
 * kb_move - 移动文件工具（含反向引用检查）
 * 包含隐式验证链：Session → Task → state → intentType
 */
import * as fs from 'fs/promises';
import * as path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
const execAsync = promisify(exec);
/**
 * 查找引用指定文件的 wikilink
 */
async function findReferences(filePath, vaultRoot) {
    const fileName = path.basename(filePath, path.extname(filePath));
    const references = [];
    try {
        // 使用 grep 查找 wikilink 引用
        const { stdout } = await execAsync(`grep -r "\\[\\[${fileName}\\]\\]" "${vaultRoot}" --include="*.md" -l`, { timeout: 10000 });
        const files = stdout.trim().split('\n').filter(f => f.length > 0);
        // 排除自身
        for (const file of files) {
            const relativePath = path.relative(vaultRoot, file);
            if (relativePath !== filePath && !relativePath.endsWith(filePath)) {
                references.push(relativePath);
            }
        }
    }
    catch (error) {
        // grep 返回空结果时会抛出异常，忽略
    }
    return references;
}
/**
 * 自动修复引用
 */
async function fixReferences(fromPath, toPath, references, vaultRoot, stateManager) {
    const fromName = path.basename(fromPath, path.extname(fromPath));
    const toName = path.basename(toPath, path.extname(toPath));
    for (const refFile of references) {
        const fullPath = path.join(vaultRoot, refFile);
        try {
            let content = await fs.readFile(fullPath, 'utf-8');
            // 替换 wikilink
            const oldLink = `[[${fromName}]]`;
            const newLink = `[[${toName}]]`;
            content = content.replace(new RegExp(oldLink.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), newLink);
            await fs.writeFile(fullPath, content, 'utf-8');
            // 标记脏模块
            const module = stateManager.extractModule(refFile);
            stateManager.markDirtyModule(module, refFile, 'edit');
        }
        catch (error) {
            console.error(`修复引用失败: ${refFile}`, error);
        }
    }
}
/**
 * 处理 kb_move 请求
 */
export async function handleKbMove(args, stateManager, vaultRoot) {
    const { from, to, autoFix = false } = args;
    // 解析完整路径
    const fullFrom = path.isAbsolute(from) ? from : path.resolve(vaultRoot, from);
    const fullTo = path.isAbsolute(to) ? to : path.resolve(vaultRoot, to);
    const relativeFrom = path.relative(vaultRoot, fullFrom);
    const relativeTo = path.relative(vaultRoot, fullTo);
    // 验证路径在 vault 内
    if (!fullFrom.startsWith(path.resolve(vaultRoot)) || !fullTo.startsWith(path.resolve(vaultRoot))) {
        return {
            success: false,
            error: {
                code: 'PATH_OUTSIDE_VAULT',
                detail: '路径不在 vault 内'
            }
        };
    }
    // 🔒 隐式验证链
    const validationError = stateManager.validateModification('move', relativeFrom);
    if (validationError) {
        return {
            success: false,
            error: validationError
        };
    }
    try {
        // 检查源文件是否存在
        try {
            await fs.access(fullFrom);
        }
        catch {
            return {
                success: false,
                error: {
                    code: 'FILE_NOT_FOUND',
                    detail: `源文件不存在: ${relativeFrom}`
                }
            };
        }
        // 查找引用
        const references = await findReferences(relativeFrom, vaultRoot);
        // 如果有引用
        if (references.length > 0) {
            if (!autoFix) {
                // 返回阻断信息
                return {
                    success: false,
                    error: {
                        code: 'HAS_REFERENCES',
                        detail: `文件被 ${references.length} 个文件引用，需要设置 autoFix=true 自动修复`
                    },
                    referencedBy: references
                };
            }
            // 自动修复引用
            await fixReferences(relativeFrom, relativeTo, references, vaultRoot, stateManager);
        }
        // 确保目标目录存在
        const toDir = path.dirname(fullTo);
        await fs.mkdir(toDir, { recursive: true });
        // 移动文件
        await fs.rename(fullFrom, fullTo);
        // 标记脏模块
        const fromModule = stateManager.extractModule(relativeFrom);
        const toModule = stateManager.extractModule(relativeTo);
        stateManager.markDirtyModule(fromModule, relativeFrom, 'move');
        if (fromModule !== toModule) {
            stateManager.markDirtyModule(toModule, relativeTo, 'move');
        }
        return {
            success: true,
            from: relativeFrom,
            to: relativeTo,
            referencedBy: references.length > 0 ? references : undefined,
            autoFixed: autoFix && references.length > 0
        };
    }
    catch (error) {
        return {
            success: false,
            error: {
                code: 'MOVE_ERROR',
                detail: `移动文件失败: ${error.message}`
            }
        };
    }
}
/**
 * kb_move 工具定义
 */
export const kbMoveTool = {
    name: 'kb_move',
    description: '移动文件，自动检查反向引用并可选择自动修复。需要 Task 处于 EXECUTING 状态。',
    inputSchema: {
        type: 'object',
        properties: {
            from: {
                type: 'string',
                description: '源文件路径'
            },
            to: {
                type: 'string',
                description: '目标文件路径'
            },
            autoFix: {
                type: 'boolean',
                description: '是否自动修复引用（默认 false）'
            }
        },
        required: ['from', 'to']
    }
};
//# sourceMappingURL=kb_move.js.map