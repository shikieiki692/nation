#!/usr/bin/env node
/**
 * KB Vault MCP Server - Stateful Implementation
 * Phase C: 增加 kb_search + kb_delete + kb_index
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema, } from '@modelcontextprotocol/sdk/types.js';
// 导入状态管理器
import { StateManager } from './state/manager.js';
// 导入编排器和钩子运行时
import { Orchestrator } from './orchestrator/orchestrator.js';
import { HookRuntime } from './hooks/hook-runtime.js';
// 导入工具实现
import { handleKbRead, kbReadTool } from './tools/kb_read.js';
import { handleKbWrite, kbWriteTool } from './tools/kb_write.js';
import { handleKbEdit, kbEditTool } from './tools/kb_edit.js';
import { handleKbBash, kbBashTool } from './tools/kb_bash.js';
import { handleKbSession, kbSessionTool } from './tools/kb_session.js';
import { handleKbGate, kbGateTool } from './tools/kb_gate.js';
import { handleKbDirty, kbDirtyTool } from './tools/kb_dirty.js';
import { handleKbMove, kbMoveTool } from './tools/kb_move.js';
import { handleKbSearch, kbSearchTool } from './tools/kb_search.js';
import { handleKbDelete, kbDeleteTool } from './tools/kb_delete.js';
import { handleKbIndex, kbIndexTool } from './tools/kb_index.js';
// Vault 根目录 - 从环境变量获取或使用当前工作目录
const VAULT_ROOT = process.env.KB_VAULT_ROOT || process.cwd();
// 创建核心组件实例
const stateManager = new StateManager(VAULT_ROOT);
const orchestrator = new Orchestrator(stateManager, VAULT_ROOT);
const hookRuntime = new HookRuntime(stateManager, VAULT_ROOT);
/**
 * 创建 MCP Server
 */
const server = new Server({
    name: 'kb-vault-mcp',
    version: '2.2.0',
}, {
    capabilities: {
        tools: {},
    },
});
/**
 * 列出所有可用工具
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            kbReadTool,
            kbWriteTool,
            kbEditTool,
            kbBashTool,
            kbSessionTool,
            kbGateTool,
            kbDirtyTool,
            kbMoveTool,
            kbSearchTool,
            kbDeleteTool,
            kbIndexTool
        ],
    };
});
/**
 * 调用工具
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    try {
        let result;
        switch (name) {
            case 'kb_read':
                result = await handleKbRead(args, stateManager, VAULT_ROOT);
                break;
            case 'kb_write':
                result = await handleKbWrite(args, stateManager, VAULT_ROOT);
                await hookRuntime.onOperationComplete();
                break;
            case 'kb_edit':
                result = await handleKbEdit(args, stateManager, VAULT_ROOT);
                await hookRuntime.onOperationComplete();
                break;
            case 'kb_bash':
                result = await handleKbBash(args, stateManager, VAULT_ROOT);
                break;
            case 'kb_session':
                result = await handleKbSession(args, stateManager);
                if (args.action === 'init' && result.success) {
                    await hookRuntime.onSessionInit();
                }
                break;
            case 'kb_gate':
                result = await handleKbGate(args, stateManager, hookRuntime, orchestrator, VAULT_ROOT);
                break;
            case 'kb_dirty':
                result = await handleKbDirty(args, stateManager);
                break;
            case 'kb_move':
                result = await handleKbMove(args, stateManager, VAULT_ROOT);
                if (result.success) {
                    await hookRuntime.onOperationComplete();
                }
                break;
            case 'kb_search':
                // 只读工具，不检查状态
                result = await handleKbSearch(args, VAULT_ROOT);
                break;
            case 'kb_delete':
                result = await handleKbDelete(args, stateManager, VAULT_ROOT);
                if (result.success) {
                    await hookRuntime.onOperationComplete();
                }
                break;
            case 'kb_index':
                // 只读工具，不检查状态
                result = await handleKbIndex(args, VAULT_ROOT);
                break;
            default:
                throw new Error(`未知工具: ${name}`);
        }
        return {
            content: [
                {
                    type: 'text',
                    text: JSON.stringify(result, null, 2),
                },
            ],
        };
    }
    catch (error) {
        return {
            content: [
                {
                    type: 'text',
                    text: JSON.stringify({
                        success: false,
                        error: {
                            code: 'INTERNAL_ERROR',
                            detail: error.message
                        }
                    }, null, 2),
                },
            ],
            isError: true,
        };
    }
});
/**
 * 启动服务器
 */
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error('KB Vault MCP Server 已启动');
    console.error(`Vault 根目录: ${VAULT_ROOT}`);
    console.error('版本: 2.2.0 (Phase C)');
    console.error('组件: StateManager + Orchestrator + HookRuntime');
    console.error('工具: kb_read/write/edit/bash/session/gate/dirty/move/search/delete/index');
}
main().catch((error) => {
    console.error('启动服务器失败:', error);
    process.exit(1);
});
//# sourceMappingURL=index.js.map