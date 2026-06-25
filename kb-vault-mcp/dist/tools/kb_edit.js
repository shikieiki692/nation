/**
 * kb_edit - old_string 唯一性验证编辑工具
 * 包含隐式验证链：Session → Task → state → intentType
 */
import * as fs from 'fs/promises';
import * as path from 'path';
/**
 * 查找字符串在文本中的所有出现位置
 */
function findAllOccurrences(text, search) {
    const positions = [];
    let index = text.indexOf(search);
    while (index !== -1) {
        positions.push(index);
        index = text.indexOf(search, index + 1);
    }
    return positions;
}
/**
 * 处理 kb_edit 请求
 */
export async function handleKbEdit(args, stateManager, vaultRoot) {
    const { path: filePath, edits, confirm } = args;
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
    // 🔒 隐式验证链：检查 Session 和 Task 状态
    const validationError = stateManager.validateModification('edit', relativePath);
    if (validationError) {
        return {
            success: false,
            error: validationError
        };
    }
    try {
        // 读取文件内容
        let content;
        try {
            content = await fs.readFile(fullPath, 'utf-8');
        }
        catch (error) {
            if (error.code === 'ENOENT') {
                return {
                    success: false,
                    error: {
                        code: 'FILE_NOT_FOUND',
                        detail: `文件不存在: ${relativePath}`
                    }
                };
            }
            throw error;
        }
        // 检查 edits 数量是否需要确认
        if (edits.length > 5 && !confirm) {
            return {
                success: false,
                error: {
                    code: 'NEED_CONFIRM',
                    detail: `编辑操作超过5个（共${edits.length}个），请设置 confirm=true 确认执行`
                }
            };
        }
        // 验证每个 edit 的唯一性
        for (let i = 0; i < edits.length; i++) {
            const edit = edits[i];
            const occurrences = findAllOccurrences(content, edit.oldText);
            if (occurrences.length === 0) {
                return {
                    success: false,
                    error: {
                        code: 'OLD_TEXT_NOT_FOUND',
                        detail: `编辑操作 ${i} 的 oldText 未找到: "${edit.oldText.substring(0, 50)}..."`
                    },
                    conflictDetails: {
                        editIndex: i,
                        occurrences: 0,
                        positions: []
                    }
                };
            }
            if (occurrences.length > 1) {
                return {
                    success: false,
                    error: {
                        code: 'OLD_TEXT_NOT_UNIQUE',
                        detail: `编辑操作 ${i} 的 oldText 不唯一，找到 ${occurrences.length} 处: "${edit.oldText.substring(0, 50)}..."`
                    },
                    conflictDetails: {
                        editIndex: i,
                        occurrences: occurrences.length,
                        positions: occurrences
                    }
                };
            }
        }
        // 验证 edits 之间无重叠
        for (let i = 0; i < edits.length; i++) {
            for (let j = i + 1; j < edits.length; j++) {
                const pos1 = content.indexOf(edits[i].oldText);
                const pos2 = content.indexOf(edits[j].oldText);
                if (pos1 !== -1 && pos2 !== -1) {
                    const end1 = pos1 + edits[i].oldText.length;
                    const end2 = pos2 + edits[j].oldText.length;
                    // 检查是否重叠
                    if (pos1 < end2 && pos2 < end1) {
                        return {
                            success: false,
                            path: relativePath,
                            appliedEdits: 0,
                            error: {
                                code: 'EDITS_OVERLAP',
                                detail: `编辑操作 ${i} 和 ${j} 存在重叠`
                            }
                        };
                    }
                }
            }
        }
        // 按位置倒序执行编辑（避免位置偏移）
        const editsWithPosition = edits.map((edit, index) => ({
            ...edit,
            index,
            position: content.indexOf(edit.oldText)
        }));
        editsWithPosition.sort((a, b) => b.position - a.position);
        let modifiedContent = content;
        for (const edit of editsWithPosition) {
            modifiedContent =
                modifiedContent.substring(0, edit.position) +
                    edit.newText +
                    modifiedContent.substring(edit.position + edit.oldText.length);
        }
        // 写入文件
        await fs.writeFile(fullPath, modifiedContent, 'utf-8');
        // 标记脏模块
        const module = stateManager.extractModule(relativePath);
        stateManager.markDirtyModule(module, relativePath, 'edit');
        // 更新读取注册表
        const newFingerprint = await stateManager.computeFingerprint(fullPath, modifiedContent);
        stateManager.updateReadRegistry(relativePath, newFingerprint);
        return {
            success: true,
            path: relativePath,
            appliedEdits: edits.length,
            dirtyModule: module
        };
    }
    catch (error) {
        return {
            success: false,
            error: {
                code: 'EDIT_ERROR',
                detail: `编辑文件失败: ${error.message}`
            }
        };
    }
}
/**
 * kb_edit 工具定义
 */
export const kbEditTool = {
    name: 'kb_edit',
    description: '编辑文件，验证 oldText 唯一性并自动标记脏模块。需要 Task 处于 EXECUTING 状态。',
    inputSchema: {
        type: 'object',
        properties: {
            path: {
                type: 'string',
                description: '文件路径（绝对路径或相对于 vault 根目录的路径）'
            },
            edits: {
                type: 'array',
                items: {
                    type: 'object',
                    properties: {
                        oldText: { type: 'string', description: '要替换的原始文本' },
                        newText: { type: 'string', description: '替换后的新文本' }
                    },
                    required: ['oldText', 'newText']
                },
                description: '编辑操作列表'
            },
            confirm: {
                type: 'boolean',
                description: '当编辑操作超过5个时，需要设置为 true 确认执行'
            }
        },
        required: ['path', 'edits']
    }
};
//# sourceMappingURL=kb_edit.js.map