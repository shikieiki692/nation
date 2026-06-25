#!/usr/bin/env node
/**
 * KB Vault MCP Server 测试脚本
 * 测试状态机强制机制和隐式验证链
 */
import * as path from 'path';
import * as fs from 'fs/promises';
import { StateManager } from './state/manager.js';
import { handleKbRead } from './tools/kb_read.js';
import { handleKbWrite } from './tools/kb_write.js';
import { handleKbEdit } from './tools/kb_edit.js';
import { handleKbBash } from './tools/kb_bash.js';
import { handleKbSession } from './tools/kb_session.js';
import { handleKbGate } from './tools/kb_gate.js';
import { handleKbDirty } from './tools/kb_dirty.js';
// 测试用的 vault 根目录
const TEST_VAULT = path.join(process.cwd(), '.test-vault-stateful');
// 测试结果统计
let passed = 0;
let failed = 0;
/**
 * 断言函数
 */
function assert(condition, message) {
    if (condition) {
        console.log(`✅ ${message}`);
        passed++;
    }
    else {
        console.error(`❌ ${message}`);
        failed++;
    }
}
/**
 * 清理测试环境
 */
async function cleanup() {
    try {
        await fs.rm(TEST_VAULT, { recursive: true, force: true });
    }
    catch { }
}
/**
 * 设置测试环境
 */
async function setup() {
    await cleanup();
    await fs.mkdir(TEST_VAULT, { recursive: true });
    await fs.mkdir(path.join(TEST_VAULT, '03-知识点'), { recursive: true });
    await fs.mkdir(path.join(TEST_VAULT, '00-首页'), { recursive: true });
    // 创建测试文件
    await fs.writeFile(path.join(TEST_VAULT, 'test.md'), '---\nversion: v1.0\nupdated: 2024-01-01\n---\n# 测试文件\n\n这是测试内容。');
    await fs.writeFile(path.join(TEST_VAULT, '03-知识点', '化学.md'), '---\nversion: v1.0\nupdated: 2024-01-01\n---\n# 化学知识点\n\n有机化学是化学的一个分支。');
}
/**
 * 测试状态机强制机制
 */
async function testStateMachine() {
    console.log('\n🔒 测试状态机强制机制...');
    const stateManager = new StateManager(TEST_VAULT);
    // 测试1: 没有 Session 时写入应该失败
    const result1 = await handleKbWrite({
        path: path.join(TEST_VAULT, 'test-write.md'),
        content: '测试内容'
    }, stateManager, TEST_VAULT);
    assert(result1.success === false, '没有 Session 时写入失败');
    assert(result1.error?.code === 'NO_ACTIVE_SESSION', '返回 NO_ACTIVE_SESSION 错误');
    // 测试2: 初始化 Session
    const sessionResult = await handleKbSession({ action: 'init' }, stateManager);
    assert(sessionResult.success === true, '初始化 Session 成功');
    // 测试3: 有 Session 但没有 Task 时写入应该失败
    const result2 = await handleKbWrite({
        path: path.join(TEST_VAULT, 'test-write.md'),
        content: '测试内容'
    }, stateManager, TEST_VAULT);
    assert(result2.success === false, '没有 Task 时写入失败');
    assert(result2.error?.code === 'NO_ACTIVE_TASK', '返回 NO_ACTIVE_TASK 错误');
    // 测试4: 创建 Task（action=create）
    const gateResult = await handleKbGate({
        action: 'create',
        intentType: 'BUILD'
    }, stateManager);
    assert(gateResult.success === true, '创建 Task 成功');
    assert(gateResult.task?.state === 'ASSESSING', 'Task 状态为 ASSESSING');
    // 测试5: Task 在 ASSESSING 状态时写入应该失败
    const result3 = await handleKbWrite({
        path: path.join(TEST_VAULT, 'test-write.md'),
        content: '测试内容'
    }, stateManager, TEST_VAULT);
    assert(result3.success === false, 'Task 在 ASSESSING 状态时写入失败');
    assert(result3.error?.code === 'TASK_NOT_EXECUTING', '返回 TASK_NOT_EXECUTING 错误');
    // 测试6: 确认计划进入 EXECUTING（action=confirm）
    const gateResult2 = await handleKbGate({ action: 'confirm' }, stateManager);
    assert(gateResult2.success === true, '确认计划成功');
    assert(gateResult2.task?.state === 'EXECUTING', 'Task 状态为 EXECUTING');
    // 测试7: Task 在 EXECUTING 状态时写入应该成功
    const result4 = await handleKbWrite({
        path: path.join(TEST_VAULT, 'test-write.md'),
        content: '---\nversion: v1.0\n---\n# 测试写入\n\n新内容。'
    }, stateManager, TEST_VAULT);
    assert(result4.success === true, 'Task 在 EXECUTING 状态时写入成功');
    assert(result4.dirtyModule !== undefined, '标记脏模块');
}
/**
 * 测试 USE 意图约束
 */
async function testUseIntentConstraint() {
    console.log('\n🔒 测试 USE 意图约束...');
    const stateManager = new StateManager(TEST_VAULT);
    // 初始化 Session
    await handleKbSession({ action: 'init' }, stateManager);
    // 创建 USE 意图的 Task
    await handleKbGate({
        action: 'create',
        intentType: 'USE'
    }, stateManager);
    // 确认计划
    await handleKbGate({ action: 'confirm' }, stateManager);
    // 测试: USE 意图写入 03-知识点 应该失败
    const result = await handleKbWrite({
        path: path.join(TEST_VAULT, '03-知识点', '新知识点.md'),
        content: '新知识点内容'
    }, stateManager, TEST_VAULT);
    assert(result.success === false, 'USE 意图写入 03-知识点 失败');
    assert(result.error?.code === 'USE_CANNOT_WRITE_KP', '返回 USE_CANNOT_WRITE_KP 错误');
    // 测试: USE 意图写入其他目录应该成功
    const result2 = await handleKbWrite({
        path: path.join(TEST_VAULT, '04-课件', '课件.md'),
        content: '课件内容'
    }, stateManager, TEST_VAULT);
    assert(result2.success === true, 'USE 意图写入其他目录成功');
}
/**
 * 测试 kb_read 不检查状态
 */
async function testReadNoStateCheck() {
    console.log('\n📖 测试 kb_read 不检查状态...');
    const stateManager = new StateManager(TEST_VAULT);
    // 测试: 没有 Session 时读取应该成功
    const result = await handleKbRead({
        path: path.join(TEST_VAULT, 'test.md')
    }, stateManager, TEST_VAULT);
    assert(result.success === true, '没有 Session 时读取成功');
    assert(result.content?.includes('测试内容') === true, '读取内容正确');
}
/**
 * 测试 kb_bash 不检查状态
 */
async function testBashNoStateCheck() {
    console.log('\n📖 测试 kb_bash 不检查状态...');
    const stateManager = new StateManager(TEST_VAULT);
    // 测试: 没有 Session 时执行只读命令应该成功
    const result = await handleKbBash({
        command: 'echo "hello"'
    }, stateManager, TEST_VAULT);
    assert(result.success === true, '没有 Session 时执行只读命令成功');
    assert(result.stdout?.includes('hello') === true, '输出正确');
    // 测试: 写入命令应该被阻断
    const result2 = await handleKbBash({
        command: 'rm -rf /tmp/test'
    }, stateManager, TEST_VAULT);
    assert(result2.success === false, '写入命令被阻断');
    assert(result2.blocked === true, '返回 blocked 状态');
}
/**
 * 测试 kb_edit 唯一性验证
 */
async function testEditUniqueness() {
    console.log('\n📝 测试 kb_edit 唯一性验证...');
    const stateManager = new StateManager(TEST_VAULT);
    // 初始化 Session 和 Task
    await handleKbSession({ action: 'init' }, stateManager);
    await handleKbGate({ action: 'create', intentType: 'BUILD' }, stateManager);
    await handleKbGate({ action: 'confirm' }, stateManager);
    // 创建测试文件
    const testFile = path.join(TEST_VAULT, '03-知识点', 'edit-test.md');
    await fs.writeFile(testFile, '重复文本\n其他内容\n重复文本');
    // 测试: 重复文本编辑应该失败
    const result = await handleKbEdit({
        path: testFile,
        edits: [{ oldText: '重复文本', newText: '新文本' }]
    }, stateManager, TEST_VAULT);
    assert(result.success === false, '重复文本编辑失败');
    assert(result.error?.code === 'OLD_TEXT_NOT_UNIQUE', '返回 OLD_TEXT_NOT_UNIQUE 错误');
    assert(result.conflictDetails?.occurrences === 2, '检测到2处重复');
}
/**
 * 测试脏模块报告
 */
async function testDirtyReport() {
    console.log('\n📊 测试脏模块报告...');
    const stateManager = new StateManager(TEST_VAULT);
    // 初始化 Session 和 Task
    await handleKbSession({ action: 'init' }, stateManager);
    await handleKbGate({ action: 'create', intentType: 'BUILD' }, stateManager);
    await handleKbGate({ action: 'confirm' }, stateManager);
    // 写入一些文件
    await handleKbWrite({
        path: path.join(TEST_VAULT, '03-知识点', '物理.md'),
        content: '物理知识点'
    }, stateManager, TEST_VAULT);
    // 生成报告
    const report = await handleKbDirty({ action: 'report' }, stateManager);
    assert(report.success === true, '生成报告成功');
    assert((report.report?.modules.length ?? 0) > 0, '报告包含脏模块');
    assert(report.report?.intentType === 'BUILD', '报告包含 intentType');
}
/**
 * 主测试函数
 */
async function main() {
    console.log('🧪 KB Vault MCP Server 状态机测试开始\n');
    try {
        await setup();
        await testStateMachine();
        await testUseIntentConstraint();
        await testReadNoStateCheck();
        await testBashNoStateCheck();
        await testEditUniqueness();
        await testDirtyReport();
        console.log('\n📊 测试结果:');
        console.log(`✅ 通过: ${passed}`);
        console.log(`❌ 失败: ${failed}`);
        console.log(`总计: ${passed + failed}`);
        if (failed > 0) {
            process.exit(1);
        }
    }
    catch (error) {
        console.error('测试执行失败:', error);
        process.exit(1);
    }
    finally {
        await cleanup();
    }
}
main();
//# sourceMappingURL=test.js.map