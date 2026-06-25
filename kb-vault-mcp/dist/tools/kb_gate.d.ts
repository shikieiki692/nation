/**
 * kb_gate - 状态迁移确认工具
 * 创建 Task、确认计划、确认归档
 * Phase B 增强：确认栅栏 + REWORK 计数
 */
import { GateResult, IntentType } from '../types.js';
import { StateManager } from '../state/manager.js';
import { HookRuntime } from '../hooks/hook-runtime.js';
import { Orchestrator } from '../orchestrator/orchestrator.js';
/**
 * 处理 kb_gate 请求
 */
export declare function handleKbGate(args: {
    action: 'create' | 'confirm' | 'verify' | 'close' | 'archive' | 'spawn';
    intentType?: IntentType;
    agentId?: number;
    scale?: string;
    persistence?: string;
    plan?: {
        sources: string[];
        targets: string[];
        batches?: string[][];
        risks: string[];
    };
    taskId?: string;
    confirm?: boolean;
    planSummary?: string;
    filesModified?: number;
    parentId?: string;
}, stateManager: StateManager, hookRuntime?: HookRuntime, orchestrator?: Orchestrator, vaultRoot?: string): Promise<GateResult>;
/**
 * kb_gate 工具定义
 */
export declare const kbGateTool: {
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
            intentType: {
                type: string;
                enum: string[];
                description: string;
            };
            agentId: {
                type: string;
                description: string;
            };
            scale: {
                type: string;
                enum: string[];
                description: string;
            };
            persistence: {
                type: string;
                enum: string[];
                description: string;
            };
            plan: {
                type: string;
                description: string;
                properties: {
                    sources: {
                        type: string;
                        items: {
                            type: string;
                        };
                    };
                    targets: {
                        type: string;
                        items: {
                            type: string;
                        };
                    };
                    batches: {
                        type: string;
                        items: {
                            type: string;
                            items: {
                                type: string;
                            };
                        };
                    };
                    risks: {
                        type: string;
                        items: {
                            type: string;
                        };
                    };
                };
            };
            taskId: {
                type: string;
                description: string;
            };
            confirm: {
                type: string;
                description: string;
            };
            filesModified: {
                type: string;
                description: string;
            };
            parentId: {
                type: string;
                description: string;
            };
            children: {
                type: string;
                description: string;
                items: {
                    type: string;
                    properties: {
                        intentType: {
                            type: string;
                            enum: string[];
                        };
                        agentId: {
                            type: string;
                        };
                        scale: {
                            type: string;
                            enum: string[];
                        };
                        persistence: {
                            type: string;
                            enum: string[];
                        };
                    };
                };
            };
        };
        required: string[];
    };
};
//# sourceMappingURL=kb_gate.d.ts.map