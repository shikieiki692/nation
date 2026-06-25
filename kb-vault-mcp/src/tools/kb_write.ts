/**
 * kb_write - 冲突检测写入工具
 * 包含隐式验证链：Session → Task → state → intentType
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { WriteResult } from '../types.js';
import { StateManager } from '../state/manager.js';

/**
 * 处理 kb_write 请求
 */
export async function handleKbWrite(
  args: { path: string; content: string },
  stateManager: StateManager,
  vaultRoot: string
): Promise<WriteResult> {
  const { path: filePath, content } = args;
  
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
  const validationError = stateManager.validateModification('write', relativePath);
  if (validationError) {
    return {
      success: false,
      error: validationError
    };
  }
  
  try {
    // 冲突检测：检查文件是否被外部修改
    const readRegistry = stateManager.getReadRegistry();
    const registeredFingerprint = readRegistry.get(relativePath);
    
    if (registeredFingerprint) {
      try {
        const currentContent = await fs.readFile(fullPath, 'utf-8');
        const currentFingerprint = await stateManager.computeFingerprint(fullPath, currentContent);
        
        if (currentFingerprint.contentHash !== registeredFingerprint.contentHash) {
          return {
            success: false,
            error: {
              code: 'CONFLICT',
              detail: `文件已被外部修改，请先重新读取: ${relativePath}`
            }
          };
        }
      } catch (error: any) {
        if (error.code !== 'ENOENT') {
          throw error;
        }
      }
    }
    
    // 确保目录存在
    const dir = path.dirname(fullPath);
    await fs.mkdir(dir, { recursive: true });
    
    // 写入文件
    await fs.writeFile(fullPath, content, 'utf-8');
    
    // 标记脏模块
    const module = stateManager.extractModule(relativePath);
    stateManager.markDirtyModule(module, relativePath, 'write');
    
    // 更新读取注册表
    const newFingerprint = await stateManager.computeFingerprint(fullPath, content);
    stateManager.updateReadRegistry(relativePath, newFingerprint);
    
    return {
      success: true,
      path: relativePath,
      dirtyModule: module
    };
    
  } catch (error: any) {
    return {
      success: false,
      error: {
        code: 'WRITE_ERROR',
        detail: `写入文件失败: ${error.message}`
      }
    };
  }
}

/**
 * kb_write 工具定义
 */
export const kbWriteTool = {
  name: 'kb_write',
  description: '写入文件内容，自动检测冲突并标记脏模块。需要 Task 处于 EXECUTING 状态。',
  inputSchema: {
    type: 'object' as const,
    properties: {
      path: {
        type: 'string',
        description: '文件路径（绝对路径或相对于 vault 根目录的路径）'
      },
      content: {
        type: 'string',
        description: '要写入的文件内容'
      }
    },
    required: ['path', 'content']
  }
};
