import * as fs from 'fs/promises';
import * as path from 'path';
import { StateManager } from '../state/manager.js';
import { Task, IntentType } from '../types.js';

export class HookRuntime {
  private stateManager: StateManager;
  private vaultRoot: string;
  private operationCount: number = 0;
  private readonly CHECKPOINT_INTERVAL = 10;
  
  constructor(stateManager: StateManager, vaultRoot: string) {
    this.stateManager = stateManager;
    this.vaultRoot = vaultRoot;
  }

  /**
   * H-G01: 会话初始化
   * 时机: kb_session init
   */
  async onSessionInit(): Promise<void> {
    // 入口文件列表
    const entryFiles = [
      '状态摘要.md',
      '00-首页/Agent标准作业流程.md',
      '00-首页/Agent最小执行协议.md',
      '00-首页/Agent战略方向.md',
      '00-首页/Agent任务分解指南.md',
      '00-首页/经验沉淀.md'
    ];
    
    // 加载入口文件指纹
    for (const file of entryFiles) {
      try {
        const fullPath = path.join(this.vaultRoot, file);
        const content = await fs.readFile(fullPath, 'utf-8');
        const fingerprint = await this.stateManager.computeFingerprint(fullPath, content);
        this.stateManager.updateReadRegistry(file, fingerprint);
      } catch (error) {
        // 文件不存在时跳过
      }
    }
    
    // 扫描可用 skills
    try {
      const skillsDir = path.join(this.vaultRoot, 'skills');
      const entries = await fs.readdir(skillsDir, { withFileTypes: true });
      const skills = entries
        .filter(e => e.isDirectory())
        .map(e => e.name);
      
      // 检查每个 skill 的 SKILL.md 是否存在
      const availableSkills: string[] = [];
      for (const skill of skills) {
        try {
          await fs.access(path.join(skillsDir, skill, 'SKILL.md'));
          availableSkills.push(skill);
        } catch {
          // SKILL.md 不存在，跳过
        }
      }
      
      console.log(`[H-G01] 会话初始化完成，已加载 ${entryFiles.length} 个入口文件指纹，发现 ${availableSkills.length} 个可用 skills`);
    } catch (error) {
      console.log('[H-G01] 会话初始化完成，已加载入口文件指纹');
    }

    // 检查过期弃用文件（7天缓冲）
    try {
      const trashDir = path.join(this.vaultRoot, '.claude/trash');
      const entries = await fs.readdir(trashDir, { withFileTypes: true });
      const now = Date.now();
      const SEVEN_DAYS = 7 * 24 * 60 * 60 * 1000;

      for (const entry of entries) {
        if (entry.isDirectory()) {
          const dirPath = path.join(trashDir, entry.name);
          const dirStat = await fs.stat(dirPath);

          // 如果目录超过7天，删除
          if (now - dirStat.mtimeMs > SEVEN_DAYS) {
            await fs.rm(dirPath, { recursive: true, force: true });
            console.log(`[H-G01] 清理过期弃用目录: ${entry.name}`);
          }
        }
      }
    } catch (error) {
      // trash 目录不存在时跳过
    }
  }

  /**
   * H-E03: 进度检查点
   * 时机: kb_write/kb_edit 调用后
   */
  async onOperationComplete(): Promise<boolean> {
    this.operationCount++;
    
    // TRIVIAL 规模跳过检查点
    const task = this.stateManager.getCurrentTask();
    if (task && task.scale === 'TRIVIAL') {
      return false;
    }
    
    // 每10次操作自动写入检查点
    if (this.operationCount >= this.CHECKPOINT_INTERVAL) {
      this.operationCount = 0;
      await this.stateManager.saveCheckpoint();
      console.log('[H-E03] 进度检查点已写入');
      return true;
    }
    return false;
  }

  /**
   * H-P03: 确认栅栏
   * 时机: kb_gate action=confirm
   */
  checkConfirmationBarrier(task: Task, filesModified: number): {
    requiresConfirmation: boolean;
    reason?: string;
  } {
    // MAINTAIN 且 files_modified ≥ 5 → 需要确认
    if (task.intentType === 'MAINTAIN' && filesModified >= 5) {
      return {
        requiresConfirmation: true,
        reason: `MAINTAIN 类型任务修改 ${filesModified} 个文件（≥5），需要用户确认`
      };
    }
    
    // META → 需要确认
    if (task.intentType === 'META') {
      return {
        requiresConfirmation: true,
        reason: 'META 类型任务需要用户确认'
      };
    }
    
    return { requiresConfirmation: false };
  }

  /**
   * H-V02: REWORK 计数
   * 时机: VERIFYING → REWORK 转换时
   */
  checkReworkLimit(taskId: string): {
    allowed: boolean;
    reworkCount: number;
    requiresHumanIntervention?: boolean;
  } {
    const reworkCount = this.stateManager.getReworkCount(taskId);
    
    // REWORK > 2 → 不允许，需要人工干预
    if (reworkCount > 2) {
      return {
        allowed: false,
        reworkCount,
        requiresHumanIntervention: true
      };
    }
    
    return { allowed: true, reworkCount };
  }

  /**
   * H-L03: 出口清理
   * 时机: Task → ARCHIVED
   */
  async onTaskArchived(taskId: string, orchestrator: any): Promise<void> {
    const task = this.stateManager.getTask(taskId);
    if (!task) return;
    
    // 清除脏模块
    task.dirtyModules.clear();
    
    // 如果是子Task，通知父Task
    if (task.parent) {
      orchestrator.onChildArchived(taskId);
    }
    
    // 如果是根Task，检查是否所有根Task都已ARCHIVED
    if (!task.parent) {
      await orchestrator.mergeOnClose();
    }
    
    console.log(`[H-L03] Task ${taskId} 出口清理完成`);
  }

  /**
   * H-L02: 任务卡自动生成
   * 时机: Task → ARCHIVED 时
   */
  async generateTaskCard(task: Task, vaultRoot: string): Promise<string | null> {
    // 只对 FORMAL 持久化的任务生成任务卡
    if (task.persistence !== 'FORMAL') {
      return null;
    }
    
    const date = new Date().toISOString().split('T')[0];
    const now = new Date().toISOString();
    const title = task.decisions[0] || `任务-${task.id.substring(0, 8)}`;
    const fileName = `任务卡-${date}-${title.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_')}.md`;
    const filePath = path.join(vaultRoot, '00-首页/活跃任务', fileName);
    
    // 确保目录存在
    await fs.mkdir(path.dirname(filePath), { recursive: true });
    
    // priority 映射 (P1/P2/P3)
    let priority = 'P2';
    if (task.scale === 'COMPOUND' || task.scale === 'BATCH') {
      priority = 'P1';
    } else if (task.scale === 'TRIVIAL') {
      priority = 'P3';
    }
    
    // area 映射 (中文)
    const areaMap: Record<string, string> = {
      'BUILD': '构建',
      'MAINTAIN': '维护',
      'USE': '使用',
      'META': '系统'
    };
    const area = areaMap[task.intentType] || '系统';
    
    // status 映射
    const status = task.state === 'ERROR' ? 'blocked' : 'completed';
    
    // evidence 格式: 产出: <文件列表>
    const evidence = Array.from(task.dirtyModules).map(m => `产出: ${m}`);
    
    // 生成 frontmatter
    let frontmatter = `---
title: ${title}
type: 活跃任务卡
status: ${status}
priority: ${priority}
area: ${area}
owner: Agent
created: ${task.createdAt.split('T')[0]}
updated: ${date}
source_notes: []
related_notes: []`;

    // completed 仅在 status=completed 时添加
    if (status === 'completed') {
      frontmatter += `\ncompleted: ${date}`;
    }
    
    frontmatter += `\nevidence:\n${evidence.length > 0 ? evidence.map(e => `  - "${e}"`).join('\n') : '  - "无"'}\n---`;

    const content = `${frontmatter}

# ${title}

## 任务信息

- **意图类型**: ${task.intentType}
- **规模**: ${task.scale}
- **状态**: ${task.state}
- **完成时间**: ${now}

## 脏模块

${Array.from(task.dirtyModules).map(m => `- ${m}`).join('\n') || '无'}

## 决策记录

${task.decisions.map(d => `- ${d}`).join('\n') || '无'}
`;

    await fs.writeFile(filePath, content, 'utf-8');
    
    return filePath;
  }

  /**
   * 重置操作计数器
   */
  resetOperationCount(): void {
    this.operationCount = 0;
  }
}
