/**
 * kb_read - 指纹比对读取工具
 * 只读工具，不检查 Task 状态
 */
import * as fs from 'fs/promises';
import * as path from 'path';
// 入口文件列表
const ENTRY_FILES = [
    '状态摘要.md',
    '00-首页/Agent标准作业流程.md',
    '00-首页/Agent最小执行协议.md',
    '00-首页/Agent战略方向.md',
    '00-首页/Agent任务分解指南.md',
    '00-首页/经验沉淀.md'
];
/**
 * 检查是否是入口文件
 */
function isEntryFile(relativePath) {
    return ENTRY_FILES.some(entry => relativePath.includes(entry));
}
/**
 * 处理 kb_read 请求
 */
export async function handleKbRead(args, stateManager, vaultRoot) {
    const { path: filePath, offset, limit } = args;
    // 解析完整路径
    const fullPath = path.isAbsolute(filePath) ? filePath : path.resolve(vaultRoot, filePath);
    const relativePath = path.relative(vaultRoot, fullPath);
    // 验证路径在 vault 内
    if (!fullPath.startsWith(path.resolve(vaultRoot))) {
        return {
            success: false,
            error: {
                code: 'PATH_OUTSIDE_VAULT',
                detail: `路径不在 vault 内: ${filePath}`
            }
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
                error: {
                    code: 'FILE_NOT_FOUND',
                    detail: `文件不存在: ${relativePath}`
                }
            };
        }
        // 读取文件内容
        let content = await fs.readFile(fullPath, 'utf-8');
        // 应用 offset 和 limit
        if (offset !== undefined || limit !== undefined) {
            const lines = content.split('\n');
            const start = offset ? offset - 1 : 0;
            const end = limit ? start + limit : lines.length;
            content = lines.slice(start, end).join('\n');
        }
        // 计算当前指纹
        const currentFingerprint = await stateManager.computeFingerprint(fullPath, content);
        // 如果是入口文件，进行指纹比对
        if (isEntryFile(relativePath)) {
            const readRegistry = stateManager.getReadRegistry();
            const previousFingerprint = readRegistry.get(relativePath);
            // 检查是否已读且未变化
            if (previousFingerprint && currentFingerprint.contentHash === previousFingerprint.contentHash) {
                return {
                    success: true,
                    skipped: true,
                    content,
                    fingerprint: currentFingerprint
                };
            }
        }
        // 更新读取注册表
        stateManager.updateReadRegistry(relativePath, currentFingerprint);
        return {
            success: true,
            content,
            fingerprint: currentFingerprint
        };
    }
    catch (error) {
        return {
            success: false,
            error: {
                code: 'READ_ERROR',
                detail: `读取文件失败: ${error.message}`
            }
        };
    }
}
/**
 * kb_read 工具定义
 */
export const kbReadTool = {
    name: 'kb_read',
    description: '读取文件内容，对入口文件进行指纹比对。若文件未变化则跳过读取。只读工具，可随时调用。',
    inputSchema: {
        type: 'object',
        properties: {
            path: {
                type: 'string',
                description: '文件路径（绝对路径或相对于 vault 根目录的路径）'
            },
            offset: {
                type: 'number',
                description: '起始行号（1-indexed，可选）'
            },
            limit: {
                type: 'number',
                description: '读取行数限制（可选）'
            }
        },
        required: ['path']
    }
};
//# sourceMappingURL=kb_read.js.map