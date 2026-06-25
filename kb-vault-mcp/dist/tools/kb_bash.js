/**
 * kb_bash - 只读白名单工具
 * 只检查白名单，不检查 Task 状态
 */
import { exec } from 'child_process';
import { promisify } from 'util';
const execAsync = promisify(exec);
// 只读命令白名单
const READONLY_COMMANDS = [
    'grep', 'rg', 'find', 'ls', 'stat', 'echo', 'cat', 'head', 'tail', 'wc',
    'pwd', 'whoami', 'date', 'env', 'printenv', 'which', 'type',
    'du', 'df', 'file', 'md5sum', 'sha256sum', 'sort', 'uniq', 'cut', 'tr',
    'diff', 'comm', 'paste', 'column', 'less', 'more'
];
// git 子命令白名单
const GIT_READONLY_SUBCOMMANDS = ['log', 'diff', 'status', 'show', 'branch', 'tag', 'remote'];
// 写入命令黑名单
const WRITE_COMMANDS = [
    'rm', 'mv', 'cp', 'chmod', 'chown', 'chgrp',
    'sed -i', 'awk -i', 'tee', 'dd',
    'mkdir', 'rmdir', 'touch', 'ln',
    'truncate', 'shred', 'wipe'
];
/**
 * 解析命令的第一个 token
 */
function parseCommand(cmd) {
    const trimmed = cmd.trim();
    const parts = trimmed.split(/\s+/);
    return {
        base: parts[0] || '',
        args: parts.slice(1)
    };
}
/**
 * 检查是否是 git 只读命令
 */
function isGitReadonly(args) {
    if (args.length === 0)
        return false;
    const subcommand = args[0];
    return GIT_READONLY_SUBCOMMANDS.includes(subcommand);
}
/**
 * 检查命令是否包含写入操作
 */
function containsWriteOperation(cmd) {
    const lowerCmd = cmd.toLowerCase();
    // 检查黑名单命令
    for (const writeCmd of WRITE_COMMANDS) {
        const regex = new RegExp('\\b' + writeCmd + '\\b');
        if (regex.test(lowerCmd)) {
            return true;
        }
    }
    // 检查重定向操作符
    if (lowerCmd.match(/\s>>?\s/) || lowerCmd.startsWith('>')) {
        return true;
    }
    return false;
}
/**
 * 处理 kb_bash 请求
 */
export async function handleKbBash(args, stateManager, vaultRoot) {
    const { command, timeout = 30 } = args;
    try {
        // 检查是否包含写入操作
        if (containsWriteOperation(command)) {
            return {
                success: false,
                blocked: true,
                error: {
                    code: 'WRITE_OPERATION_BLOCKED',
                    detail: '文件修改必须通过 kb_write/kb_edit/kb_move/kb_delete 工具'
                }
            };
        }
        const { base, args: cmdArgs } = parseCommand(command);
        // 特殊处理 git 命令
        if (base === 'git') {
            if (!isGitReadonly(cmdArgs)) {
                return {
                    success: false,
                    blocked: true,
                    error: {
                        code: 'GIT_WRITE_BLOCKED',
                        detail: 'git 写入操作必须通过 kb_write/kb_edit 工具'
                    }
                };
            }
        }
        else {
            // 检查是否在白名单中
            if (!READONLY_COMMANDS.includes(base)) {
                return {
                    success: false,
                    blocked: true,
                    error: {
                        code: 'COMMAND_NOT_ALLOWED',
                        detail: `命令 "${base}" 不在只读白名单中，文件修改必须通过 kb_write/kb_edit/kb_move/kb_delete 工具`
                    }
                };
            }
        }
        // 执行命令
        const { stdout, stderr } = await execAsync(command, {
            cwd: vaultRoot,
            timeout: timeout * 1000,
            maxBuffer: 1024 * 1024 * 10
        });
        return {
            success: true,
            stdout,
            stderr,
            exitCode: 0
        };
    }
    catch (error) {
        return {
            success: false,
            stdout: error.stdout || '',
            stderr: error.stderr || error.message,
            exitCode: error.code || 1
        };
    }
}
/**
 * kb_bash 工具定义
 */
export const kbBashTool = {
    name: 'kb_bash',
    description: '执行只读 bash 命令。写入操作会被阻断。只读命令可随时调用。',
    inputSchema: {
        type: 'object',
        properties: {
            command: {
                type: 'string',
                description: '要执行的 bash 命令'
            },
            timeout: {
                type: 'number',
                description: '超时时间（秒，默认30）'
            }
        },
        required: ['command']
    }
};
//# sourceMappingURL=kb_bash.js.map