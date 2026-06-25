/**
 * kb_session - 会话生命周期管理工具
 * 初始化 Session、保存检查点、清除状态
 */

import { SessionResult, Session } from '../types.js';
import { StateManager } from '../state/manager.js';

/**
 * 处理 kb_session 请求
 */
export async function handleKbSession(
  args: {
    action: 'init' | 'checkpoint' | 'clear';
    session?: Partial<Session>;
  },
  stateManager: StateManager
): Promise<SessionResult> {
  const { action } = args;
  
  try {
    switch (action) {
      case 'init': {
        // 初始化 Session（可能从检查点恢复）
        const { session, recovered } = await stateManager.initSession();
        
        return {
          success: true,
          action: 'init',
          session,
          ...(recovered ? { checkpoint: undefined } : {})
        };
      }
      
      case 'checkpoint': {
        // 保存检查点
        const session = stateManager.getSession();
        if (!session) {
          return {
            success: false,
            action: 'checkpoint',
            error: {
              code: 'NO_ACTIVE_SESSION',
              detail: '没有活跃会话，请先执行 init'
            }
          };
        }
        
        await stateManager.saveCheckpoint();
        
        return {
          success: true,
          action: 'checkpoint',
          session
        };
      }
      
      case 'clear': {
        // 清除检查点和内存状态
        const session = stateManager.getSession();
        await stateManager.clear();
        
        return {
          success: true,
          action: 'clear',
          session: session || undefined
        };
      }
      
      default:
        return {
          success: false,
          error: {
            code: 'INVALID_ACTION',
            detail: `未知操作: ${action}`
          }
        };
    }
    
  } catch (error: any) {
    return {
      success: false,
      error: {
        code: 'SESSION_ERROR',
        detail: `会话操作失败: ${error.message}`
      }
    };
  }
}

/**
 * kb_session 工具定义
 */
export const kbSessionTool = {
  name: 'kb_session',
  description: '会话生命周期管理。init: 初始化/恢复会话; checkpoint: 写入检查点; clear: 清除检查点。',
  inputSchema: {
    type: 'object' as const,
    properties: {
      action: {
        type: 'string',
        enum: ['init', 'checkpoint', 'clear'],
        description: '操作类型'
      },
      session: {
        type: 'object',
        description: '会话状态更新（可选）',
        properties: {
          id: { type: 'string' },
          state: { type: 'string' }
        }
      }
    },
    required: ['action']
  }
};
