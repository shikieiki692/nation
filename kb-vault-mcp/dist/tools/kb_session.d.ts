/**
 * kb_session - 会话生命周期管理工具
 * 初始化 Session、保存检查点、清除状态
 */
import { SessionResult, Session } from '../types.js';
import { StateManager } from '../state/manager.js';
/**
 * 处理 kb_session 请求
 */
export declare function handleKbSession(args: {
    action: 'init' | 'checkpoint' | 'clear';
    session?: Partial<Session>;
}, stateManager: StateManager): Promise<SessionResult>;
/**
 * kb_session 工具定义
 */
export declare const kbSessionTool: {
    name: string;
    description: string;
    inputSchema: {
        type: "object";
        properties: {
            action: {
                type: string;
                enum: string[];
                description: string;
            };
            session: {
                type: string;
                description: string;
                properties: {
                    id: {
                        type: string;
                    };
                    state: {
                        type: string;
                    };
                };
            };
        };
        required: string[];
    };
};
//# sourceMappingURL=kb_session.d.ts.map