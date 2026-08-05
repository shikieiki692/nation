---
title: validate_kb 每周运行（定时巡检）
type: 活跃任务卡
task_type: 系统维护
status: active
priority: P3
area: 知识库系统
owner: Agent
created: 2026-08-02
updated: 2026-08-03
description: >
  每周一 08:23 运行 validate_kb.py 全量验证，对比基线只报异常增量，
  并检查上轮 follow-up 断链清单是否已清。目录/文件重组后必须立即补跑。
source_notes:
  - "[[00-首页/状态摘要]]"
  - "[[00-首页/知识库治理待办]]"
  - "[[11-模板/scripts/validate_kb.py]]"
related_notes:
  - "[[09-审计报告/auto-validation/2026-08-02-validation]]"
  - "[[00-首页/自动汇总/自动汇总-系统库存统计]]"
evidence:
  - "2026-08-02: 机制恢复——cron 23 8 * * 1 会话级定时任务已建；validate_kb.py 降噪修复（5251→2648 warning）：图片全库 basename 解析 + status 枚举补全 + 目录链接识别 + 模板占位符排除 + 带.md后缀短链接兼容。基线 48 error / 2648 warning / 7296 info。"
  - "2026-08-02: 状态摘要 低优/定时任务区 + 知识库治理待办 已上线自动化区已同步记录。"
  - "2026-08-03: 全量验证确认基线 0 error / 2179 warning / 7293 info（6112 文件）；48 个 frontmatter 补齐后 error=0，脚本再降噪（图片全库解析+占位排除+published门禁复用图片解析），周巡检报告 [[09-审计报告/周巡检-2026-08-03]] 无异常增量。"
  - "2026-08-03(第二轮): validate_kb.py build_label_index 修复——YAML 解析失败时 aliases 退化为含方括号字符串（如 \"[a, b]\"），索引把整串当一个 label 导致别名全部丢失；改为拆分为单项。断链 2559→2020（-539）、Warning 2986→2350。附带发现 300 个 KP frontmatter 存在 `tags: [X]`+缩进块列表 YAML 损坏 → **已用 [[11-模板/scripts/fix_tags_yaml.py]] 批量修复（357 文件）**，aliases 全部恢复。最终基线：0 error / 2134 warning / 1837 断链 / 86 图片缺失 / 196 标题跳跃 / 166 过期(Info)。"
  - "2026-08-04: 巡检逻辑新增第5步——顺带刷新 backup_media.py manifest + 检查 zip 新鲜度，媒体仓库 241MB gitignore 资产纳入周期健康检查。"
---

# validate_kb 每周运行（定时巡检）

## 触发

- **cron**: `23 8 * * 1`（周一 08:23，Asia/Shanghai），会话级。
- **补跑触发**：目录/文件重组后立即跑一次（07-25 重组后 ~450 断链未被捕获的教训）。

## 执行命令

```powershell
cd "C:/Obsidion/妙妙屋"
python "11-模板/scripts/validate_kb.py" --full
```

## 巡检逻辑

1. 读取 `09-审计报告/auto-validation/YYYY-MM-DD-validation.md`
2. 对比基线（0 error / 2179 warning，2026-08-03）
3. 周报写入 `09-审计报告/周巡检-YYYY-MM-DD.md`，**仅报异常增量**
4. 检查上轮 follow-up 断链清单是否已清
5. 顺带刷新媒体备份：`python scripts/backup_media.py`（manifest 落 10-索引与统计/媒体仓库清单.json），并检查 `09-审计报告/备份/media-backup-*.zip` 新鲜度（>7 天则重建 zip）
6. 完成后桌面通知

## 关键基线（2026-08-03 确认）

| 指标 | 值 |
|:---|:---|
| 受检文件 | 6112 |
| Error | 0（2026-08-03 frontmatter 全补齐） |
| Warning | 2179（断链 1867，其中 ~1740 为预期 REDLINK） |
| Info | 7293 |

## 说明

- 预期 REDLINK（如 `合成设计`、`推断技术`、`13C NMR`）指向规划中的待建 KP，不是错误，与 [[00-首页/待建KP优先级清单]] 对齐。
- 模板占位符（`{…}`、`某知识点`、`KP-N`、`图名.png` 等）已被脚本排除，不再计为断链。
