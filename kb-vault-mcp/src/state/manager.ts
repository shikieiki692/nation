/**
 * KB Vault MCP Server - State Machine Manager
 * 在内存中维护 Session 和 Task 状态机
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import * as crypto from 'crypto';
import { 
  Session, SessionState, 
  Task, TaskState, IntentType,
  FileFingerprint, CheckpointData,
  ValidationError 
} from '../types.js';

const CHECKPOINT_DIR = '.kb/state';
const CHECKPOINT_FILE = 'checkpoint.jsonl';
const MAX_LINES = 500;
const MAX_ROTATED_FILES = 3;

export class StateManager {
  private session: Session | null = null;
  private tasks: Map<string, Task> = new Map();
  private vaultRoot: string;

  constructor(vaultRoot: string) {
    this.vaultRoot = vaultRoot;
  }

  /**
   * 初始化 Session
   */
  async initSession(): Promise<{ session: Session; recovered: boolean }> {
    // 检查是否存在检查点
    const checkpoint = await this.loadCheckpoint();
    
    if (checkpoint) {
      // 恢复 Session 和 Task 树
      this.session = {
        id: checkpoint.session.id,
        state: 'ACTIVE',
        startedAt: checkpoint.session.startedAt,
        lastCheckpoint: checkpoint.session.lastCheckpoint,
        currentTaskId: checkpoint.session.currentTaskId,
        context: {
          readRegistry: new Map(checkpoint.readRegistry),
          aggregateDirtyModules: new Set()
        }
      };
      
      // 恢复 Task 树
      this.tasks = new Map(checkpoint.tasks.map(([id, task]) => {
        // 恢复 Set 类型
        const restoredTask = {
          ...task,
          dirtyModules: new Set(task.dirtyModules)
        } as Task;
        return [id, restoredTask];
      }));
      
      // 重建 aggregateDirtyModules
      for (const task of this.tasks.values()) {
        for (const mod of task.dirtyModules) {
          this.session.context.aggregateDirtyModules.add(mod);
        }
      }
      
      return { session: this.session, recovered: true };
    }
    
    // 创建新 Session
    const sessionId = `session-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
    this.session = {
      id: sessionId,
      state: 'ACTIVE',
      startedAt: new Date().toISOString(),
      currentTaskId: null,
      context: {
        readRegistry: new Map(),
        aggregateDirtyModules: new Set()
      }
    };
    
    return { session: this.session, recovered: false };
  }

  /**
   * 获取当前 Session
   */
  getSession(): Session | null {
    return this.session;
  }

  /**
   * 创建新 Task
   */
  createTask(params: {
    intentType: IntentType;
    agentId?: number;
    scale?: string;
    persistence?: string;
    parentId?: string;
  }): Task {
    if (!this.session) {
      throw new Error('NO_ACTIVE_SESSION');
    }

    const taskId = `task-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
    const task: Task = {
      id: taskId,
      state: 'ASSESSING',
      intentType: params.intentType,
      agentId: params.agentId || null,
      strategy: 'PURE_AGENT',
      scale: (params.scale as any) || 'NORMAL',
      persistence: (params.persistence as any) || 'FORMAL',
      parent: params.parentId || null,
      children: [],
      awaitingChildren: [],
      reworkCount: 0,
      dirtyModules: new Set(),
      decisions: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    // 如果有父 Task，添加到父 Task 的 children
    if (params.parentId) {
      const parentTask = this.tasks.get(params.parentId);
      if (parentTask) {
        parentTask.children.push(taskId);
      }
    }

    this.tasks.set(taskId, task);
    this.session.currentTaskId = taskId;
    
    return task;
  }

  /**
   * 获取当前活跃 Task
   */
  getCurrentTask(): Task | null {
    if (!this.session?.currentTaskId) {
      return null;
    }
    return this.tasks.get(this.session.currentTaskId) || null;
  }

  /**
   * 设置当前活跃 Task
   */
  setCurrentTaskId(taskId: string | null): void {
    if (this.session) {
      this.session.currentTaskId = taskId;
    }
  }

  /**
   * 获取指定 Task
   */
  getTask(taskId: string): Task | null {
    return this.tasks.get(taskId) || null;
  }

  /**
   * 更新 Task 状态
   */
  updateTaskState(taskId: string, newState: TaskState): boolean {
    const task = this.tasks.get(taskId);
    if (!task) {
      return false;
    }

    // 验证状态迁移合法性
    if (!this.isValidStateTransition(task.state, newState)) {
      return false;
    }

    task.state = newState;
    task.updatedAt = new Date().toISOString();
    return true;
  }

  /**
   * 验证状态迁移合法性
   */
  private isValidStateTransition(from: TaskState, to: TaskState): boolean {
    const validTransitions: Record<TaskState, TaskState[]> = {
      'ASSESSING': ['PLANNING', 'ERROR'],
      'PLANNING': ['EXECUTING', 'ERROR'],
      'EXECUTING': ['VERIFYING', 'AWAITING', 'SUSPENDED', 'ERROR'],
      'VERIFYING': ['CLOSING', 'REWORK', 'ERROR'],
      'CLOSING': ['ARCHIVED', 'ERROR'],
      'ARCHIVED': [],
      'AWAITING': ['EXECUTING', 'ERROR'],
      'SUSPENDED': ['EXECUTING', 'ERROR'],
      'ERROR': ['ARCHIVED'],
      'REWORK': ['EXECUTING']
    };

    return validTransitions[from]?.includes(to) || false;
  }

  /**
   * 获取所有根 Task（没有 parent 的 Task）
   */
  getRootTasks(): Task[] {
    const roots: Task[] = [];
    for (const task of this.tasks.values()) {
      if (!task.parent) {
        roots.push(task);
      }
    }
    return roots;
  }

  /**
   * 检查所有子 Task 是否都已 ARCHIVED
   */
  areAllChildrenArchived(taskId: string): boolean {
    const task = this.tasks.get(taskId);
    if (!task || task.children.length === 0) {
      return true;
    }
    return task.children.every(childId => {
      const child = this.tasks.get(childId);
      return child?.state === 'ARCHIVED';
    });
  }

  /**
   * 增加 reworkCount
   */
  incrementReworkCount(taskId: string): number {
    const task = this.tasks.get(taskId);
    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }
    task.reworkCount++;
    task.updatedAt = new Date().toISOString();
    return task.reworkCount;
  }

  /**
   * 获取 reworkCount
   */
  getReworkCount(taskId: string): number {
    const task = this.tasks.get(taskId);
    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }
    return task.reworkCount;
  }

  /**
   * 清除指定脏模块
   */
  clearDirtyModule(module: string): void {
    if (this.session) {
      this.session.context.aggregateDirtyModules.delete(module);
    }
  }

  /**
   * 清除所有脏模块
   */
  clearAllDirtyModules(): void {
    if (this.session) {
      this.session.context.aggregateDirtyModules.clear();
    }
  }

  /**
   * 标记脏模块
   */
  markDirtyModule(module: string, file?: string, changeType?: string): void {
    const task = this.getCurrentTask();
    if (task) {
      task.dirtyModules.add(module);
    }
    if (this.session) {
      this.session.context.aggregateDirtyModules.add(module);
    }
  }

  /**
   * 获取读取注册表
   */
  getReadRegistry(): Map<string, FileFingerprint> {
    return this.session?.context.readRegistry || new Map();
  }

  /**
   * 更新读取注册表
   */
  updateReadRegistry(path: string, fingerprint: FileFingerprint): void {
    if (this.session) {
      this.session.context.readRegistry.set(path, fingerprint);
    }
  }

  /**
   * 验证修改操作的前置条件
   * 这是核心的隐式验证链
   */
  validateModification(operation: string, targetPath?: string): ValidationError | null {
    // 1. 检查 Session 是否存在且活跃
    if (!this.session || this.session.state !== 'ACTIVE') {
      return {
        code: 'NO_ACTIVE_SESSION',
        detail: '请先通过 kb_session init 初始化会话'
      };
    }

    // 2. 检查是否有活跃 Task
    const task = this.getCurrentTask();
    if (!task) {
      return {
        code: 'NO_ACTIVE_TASK',
        detail: '请先通过 kb_gate action=create 创建 Task'
      };
    }

    // 3. 检查 Task 状态是否允许修改
    if (task.state !== 'EXECUTING' && task.state !== 'VERIFYING' && task.state !== 'CLOSING') {
      return {
        code: 'TASK_NOT_EXECUTING',
        currentState: task.state,
        detail: `Task 当前在 ${task.state} 状态，只有 EXECUTING、VERIFYING 或 CLOSING 状态允许文件修改`
      };
    }

    // VERIFYING 阶段只允许修复性编辑（写入 03-知识点/ 或 04-课件/）
    if (task.state === 'VERIFYING' && targetPath) {
      const normalizedPath = targetPath.replace(/\\/g, '/');
      if (!normalizedPath.includes('03-知识点/') && !normalizedPath.includes('04-课件/')) {
        return {
          code: 'VERIFYING_ONLY_REPAIR',
          currentState: task.state,
          detail: 'VERIFYING 阶段只允许修复性编辑（03-知识点/ 或 04-课件/）'
        };
      }
    }

    // CLOSING 阶段只允许写入工作日志和任务卡
    if (task.state === 'CLOSING' && targetPath) {
      const normalizedPath = targetPath.replace(/\\/g, '/');
      if (!normalizedPath.includes('工作日志/') && !normalizedPath.includes('活跃任务/')) {
        return {
          code: 'CLOSING_ONLY_LOGS',
          currentState: task.state,
          detail: 'CLOSING 阶段只允许写入工作日志和任务卡'
        };
      }
    }

    // 4. 检查 intentType 约束
    if (targetPath) {
      const intentError = this.validateIntentConstraint(task, targetPath, operation);
      if (intentError) {
        return intentError;
      }
    }

    return null;
  }

  /**
   * 验证 intentType 约束
   */
  private validateIntentConstraint(task: Task, targetPath: string, operation: string): ValidationError | null {
    const normalizedPath = targetPath.replace(/\\/g, '/');
    
    // USE 意图禁止写入 03-知识点/
    if (task.intentType === 'USE' && normalizedPath.includes('03-知识点/')) {
      return {
        code: 'USE_CANNOT_WRITE_KP',
        detail: 'USE 类型 Task 禁止修改知识点源文件'
      };
    }

    // META 意图写入 00-首页/ 需要警告（这里只是记录，不阻断）
    if (task.intentType === 'META' && normalizedPath.includes('00-首页/')) {
      task.decisions.push(`WARNING: META 意图修改了 00-首页/ 下的文件: ${targetPath}`);
    }

    // MAINTAIN 意图的删除操作需要软弃用（这里只是记录，实际实现在 kb_delete 中）
    if (task.intentType === 'MAINTAIN' && operation === 'delete') {
      task.decisions.push('MAINTAIN 删除操作将自动降级为软弃用');
    }

    return null;
  }

  /**
   * 保存检查点（追加写入 JSONL）
   */
  async saveCheckpoint(): Promise<void> {
    if (!this.session) return;

    const checkpointDir = path.join(this.vaultRoot, CHECKPOINT_DIR);
    await fs.mkdir(checkpointDir, { recursive: true });

    const checkpointPath = path.join(checkpointDir, CHECKPOINT_FILE);

    // 构造当前快照
    const snapshot = {
      timestamp: new Date().toISOString(),
      session: {
        id: this.session.id,
        state: this.session.state,
        currentTaskId: this.session.currentTaskId
      },
      tasks: Array.from(this.tasks.entries()).map(([id, task]) => ({
        id,
        state: task.state,
        intentType: task.intentType,
        parent: task.parent,
        children: task.children,
        awaitingChildren: task.awaitingChildren,
        dirtyModules: Array.from(task.dirtyModules)
      }))
    };

    // 追加写入
    const line = JSON.stringify(snapshot) + '\n';
    await fs.appendFile(checkpointPath, line, 'utf-8');

    // 检查是否需要 rotate
    const content = await fs.readFile(checkpointPath, 'utf-8');
    const lines = content.trim().split('\n');
    if (lines.length > MAX_LINES) {
      await this.rotateCheckpoint(checkpointPath, lines);
    }

    this.session.lastCheckpoint = new Date().toISOString();
  }

  /**
   * Rotate checkpoint files
   */
  private async rotateCheckpoint(checkpointPath: string, lines: string[]): Promise<void> {
    const dir = path.dirname(checkpointPath);
    const base = path.basename(checkpointPath, '.jsonl');

    // 移动现有 rotate 文件
    for (let i = MAX_ROTATED_FILES - 1; i > 0; i--) {
      const src = path.join(dir, `${base}.${i}.jsonl`);
      const dst = path.join(dir, `${base}.${i + 1}.jsonl`);
      try {
        await fs.rename(src, dst);
      } catch {}
    }

    // 保存当前文件为 .1
    const rotatedPath = path.join(dir, `${base}.1.jsonl`);
    await fs.rename(checkpointPath, rotatedPath);

    // 删除超过 MAX_ROTATED_FILES 的文件
    for (let i = MAX_ROTATED_FILES + 1; i <= MAX_ROTATED_FILES + 5; i++) {
      try {
        await fs.unlink(path.join(dir, `${base}.${i}.jsonl`));
      } catch {}
    }
  }

  /**
   * 加载检查点（从 JSONL 恢复）
   */
  private async loadCheckpoint(): Promise<CheckpointData | null> {
    try {
      const checkpointPath = path.join(this.vaultRoot, CHECKPOINT_DIR, CHECKPOINT_FILE);
      const content = await fs.readFile(checkpointPath, 'utf-8');
      const lines = content.trim().split('\n').filter(l => l.length > 0);

      if (lines.length === 0) return null;

      // 按 taskId 分组，取最后一行
      const taskSnapshots = new Map<string, any>();
      let lastSession: any = null;

      for (const line of lines) {
        const snapshot = JSON.parse(line);
        lastSession = snapshot.session;

        for (const task of snapshot.tasks) {
          taskSnapshots.set(task.id, task);
        }
      }

      if (!lastSession) return null;

      // 构造 CheckpointData
      return {
        session: {
          id: lastSession.id,
          state: lastSession.state,
          startedAt: lastSession.startedAt || new Date().toISOString(),
          currentTaskId: lastSession.currentTaskId
        },
        tasks: Array.from(taskSnapshots.entries()),
        readRegistry: [],
        timestamp: new Date().toISOString()
      };
    } catch (error: any) {
      if (error.code === 'ENOENT') return null;
      throw error;
    }
  }

  /**
   * 清除检查点和内存状态
   */
  async clear(): Promise<void> {
    this.session = null;
    this.tasks.clear();

    try {
      const checkpointPath = path.join(this.vaultRoot, CHECKPOINT_DIR, CHECKPOINT_FILE);
      await fs.unlink(checkpointPath);
    } catch (error: any) {
      if (error.code !== 'ENOENT') throw error;
    }
  }

  /**
   * 计算文件指纹
   */
  async computeFingerprint(filePath: string, content?: string): Promise<FileFingerprint> {
    const fileContent = content || await fs.readFile(filePath, 'utf-8');
    const contentHash = crypto.createHash('sha256').update(fileContent).digest('hex').substring(0, 16);
    
    // 提取 frontmatter
    const frontmatterMatch = fileContent.match(/^---\n([\s\S]*?)\n---/);
    let version: string | undefined;
    let updated: string | undefined;
    
    if (frontmatterMatch) {
      const frontmatter = frontmatterMatch[1];
      const versionMatch = frontmatter.match(/version:\s*(.+)/);
      const updatedMatch = frontmatter.match(/updated:\s*(.+)/);
      version = versionMatch?.[1]?.trim();
      updated = updatedMatch?.[1]?.trim();
    }
    
    return {
      path: filePath,
      version,
      updated,
      contentHash,
      readAt: new Date().toISOString()
    };
  }

  /**
   * 从文件路径提取模块名
   */
  extractModule(filePath: string): string {
    const normalized = filePath.replace(/\\/g, '/');
    const parts = normalized.split('/');
    if (parts.length > 1) {
      return parts[0];
    }
    return 'root';
  }

  /**
   * 生成脏模块报告
   */
  generateDirtyReport(): {
    modules: Array<{ module: string; changeTypes: string[]; files: string[] }>;
    syncChecklist: Array<{ target: string; mandatory: boolean; reason: string }>;
    intentType?: IntentType;
  } {
    const task = this.getCurrentTask();
    const modules: Array<{ module: string; changeTypes: string[]; files: string[] }> = [];
    const syncChecklist: Array<{ target: string; mandatory: boolean; reason: string }> = [];
    
    // 收集所有脏模块
    const dirtyModules = this.session?.context.aggregateDirtyModules || new Set();
    
    for (const mod of dirtyModules) {
      modules.push({
        module: mod,
        changeTypes: ['modify'],
        files: []
      });
    }
    
    // 根据 intentType 生成特异性收工清单
    if (task) {
      // 通用必做项
      syncChecklist.push({
        target: '工作日志',
        mandatory: true,
        reason: '始终'
      });
      
      switch (task.intentType) {
        case 'BUILD':
          if (dirtyModules.has('03-知识点')) {
            syncChecklist.push({
              target: '知识点总索引',
              mandatory: true,
              reason: '新增知识点 > 5'
            });
          }
          break;
          
        case 'MAINTAIN':
          syncChecklist.push({
            target: '审计报告归档',
            mandatory: true,
            reason: '始终'
          });
          break;
          
        case 'USE':
          syncChecklist.push({
            target: '备课与教学思路待办',
            mandatory: true,
            reason: '硬规则，不可跳过'
          });
          break;
          
        case 'META':
          if (dirtyModules.has('00-首页')) {
            syncChecklist.push({
              target: '状态摘要',
              mandatory: true,
              reason: '始终'
            });
          }
          break;
      }
      
      return { modules, syncChecklist, intentType: task.intentType };
    }
    
    return { modules, syncChecklist };
  }
}
