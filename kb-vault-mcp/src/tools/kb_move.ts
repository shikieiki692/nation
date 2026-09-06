/**
 * kb_move - 移动文件工具（含反向引用检查）
 * 包含隐式验证链：Session → Task → state → intentType
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { MoveResult } from '../types.js';
import { StateManager } from '../state/manager.js';

// 统一排除目录（与 kb_search/kb_index/kb_delete 保持一致）
const EXCLUDED_DIRS = new Set(['.git', '.claude', '.trash', 'node_modules']);

/**
 * 递归遍历 vault 内所有 .md 文件（纯 Node 实现，Windows/POSIX/中文路径通用）
 */
async function walkMarkdownFiles(root: string): Promise<string[]> {
  const results: string[] = [];

  async function walk(dir: string): Promise<void> {
    let entries;
    try {
      entries = await fs.readdir(dir, { withFileTypes: true });
    } catch {
      return; // 目录不可读时跳过
    }
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!EXCLUDED_DIRS.has(entry.name)) {
          await walk(full);
        }
      } else if (entry.isFile() && entry.name.endsWith('.md')) {
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
function extractWikilinkTargets(content: string): string[] {
  const targets: string[] = [];
  const re = /\[\[([^\]]+?)\]\]/g;
  let m: RegExpExecArray | null;
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
function linkTargetsFile(target: string, fileName: string): boolean {
  const base = target.replace(/\\/g, '/').split('/').pop() || target;
  return base === fileName || base === `${fileName}.md`;
}

/**
 * 查找引用指定文件的 wikilink
 */
async function findReferences(filePath: string, vaultRoot: string): Promise<string[]> {
  const fileName = path.basename(filePath, path.extname(filePath));
  const references: string[] = [];

  // 统一为正斜杠用于自身路径比较
  const normalize = (p: string) => p.replace(/\\/g, '/');
  const selfNorm = normalize(filePath);

  // 一次遍历收集所有结果
  const files = await walkMarkdownFiles(vaultRoot);

  for (const file of files) {
    const relativePath = path.relative(vaultRoot, file);

    // 排除自身
    const relNorm = normalize(relativePath);
    if (relNorm === selfNorm || relNorm.endsWith(selfNorm)) {
      continue;
    }

    let content: string;
    try {
      content = await fs.readFile(file, 'utf-8');
    } catch {
      continue; // 读失败的文件跳过
    }

    const targets = extractWikilinkTargets(content);
    if (targets.some(t => linkTargetsFile(t, fileName))) {
      references.push(relativePath);
    }
  }

  return references;
}

/**
 * 自动修复引用
 */
async function fixReferences(
  fromPath: string,
  toPath: string,
  references: string[],
  vaultRoot: string,
  stateManager: StateManager
): Promise<void> {
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
    } catch (error) {
      console.error(`修复引用失败: ${refFile}`, error);
    }
  }
}

/**
 * 处理 kb_move 请求
 */
export async function handleKbMove(
  args: {
    from: string;
    to: string;
    autoFix?: boolean;
  },
  stateManager: StateManager,
  vaultRoot: string
): Promise<MoveResult> {
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
    } catch {
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
    
  } catch (error: any) {
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
    type: 'object' as const,
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
