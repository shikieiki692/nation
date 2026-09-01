---
title: validate_kb 每周运行（定时巡检）
type: 活跃任务卡
task_type: 系统维护
status: active
priority: P3
area: 知识库系统
owner: Agent
created: 2026-08-02
updated: 2026-09-01
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
  - "2026-08-10: 08-10 精选重组归档移动后合规补跑（--full 6237 文件）——0 error / 1926 warning / 7406 info / 断链 1885 / 图片缺失 3。精选重组断链旧→新路径平移数量不变，未引入体系性断链；新增 ~68 断链为 08-09 晚间真题三方审计 knowledge_points 补全产物（目标 KP 缺失，已入断链内容建设backlog）；图片缺失 +1 为 04-课件/习题集/第一轮结构化学-晶体结构练习题组 mineru 图引用（08-10 07:59 修改）。"
  - "2026-08-13: 任务卡大规模迁移（104 张移出活跃任务+引用修复+索引重建）后合规补跑（--full 6266 文件）——0 error / 1366 warning / 7442 info / 断链 1355 / 图片缺失 3。对比 08-10：Warning -560、断链 -530，迁移零新断链（短名歧义修复使断链大幅下降）；首跑检出 2 个 frontmatter 缺字段 Error（08-13 新建的化学原理-跨模块同源题答案口径一致性审计 + 化学原理-重复题目去重记录，缺 title/updated），已补全归零。基线更新为 0 error / 1366 warning。"
  - "2026-08-14: 低危格式修复后重跑（--full 6266 文件）——0 error / 1358 warning / 7442 info / 标题跳跃 0（7→0）/ 断链 -7。修复内容：①配位题组 8 个 `# 第X部分` 降为 `##` + 第四部分 3 个分组降 `###`，消除 7 处标题跳跃；②资料提炼-周坤-定量化学分析 `[[minerU 图片缺失清单]]`（不存在的目标）改指 `[[00-首页/图片待补清单]]`，消除持续 5 轮报告的断链。基线更新为 0 error / 1358 warning。"
  - "2026-08-14(第二轮): 3 个同源 kp_target 断链修复后重跑（--full 6266 文件）——0 error / 1355 warning / 7442 info / 断链 -3。修复内容：资料提炼-周坤-定量化学分析 3 个指向未建文档的 kp_target 断链（[[OCR 公式修复指南]]、[[术语统一规范]]、[[OCR 噪声识别与过滤]]）统一改指 [[经验沉淀]]，消除自 08-02 起持续 7 轮报告的断链。基线更新为 0 error / 1355 warning。"
  - "2026-08-14(第三轮): 12 处同类 kp_target 断链修复后重跑（--full 6266 文件）——0 error / 1343 warning / 7442 info / 断链 -12。修复内容：周坤资料提炼 3 文件（原子结构与分子结构、热力学与化学平衡、电化学与溶液）踩坑回流段 12 个指向未建规划文档的 kp_target 断链——9 处改指 [[经验沉淀]]（OCR/格式、术语、OCR噪声/标题不匹配），3 处 10.3 mineru 漏图改指 [[00-首页/图片待补清单]]（与定量化学分析修复同型）。基线更新为 0 error / 1343 warning。"
  - "2026-08-28: 全库 --full 补跑——6591 文件 · 0 error / 456 warning / 7750 info。Warning 从 1343 降至 456（-66%），断链从 1355 降至 337（-75%）。新增图片缺失 73（学而思 XES 题 50 张 + 33 届决赛 19 张）和标题跳跃 46（习题书）。基线更新为 0 error / 456 warning。"
  - "2026-08-31: validate_kb 盲区合并（题库六字段枚举检查仅题目类 + frontmatter 内 wikilink 断链检查）后 full 实测——6160 文件 · 0 error / 2660 warning（枚举 0；frontmatter 断链暴露存量 KP 红链 1724，与 audit 同源，用户指示暂不处理）；2 个习题书附录 Error 已补 frontmatter 清零。"
  - "2026-08-31(终检): 全链收尾后 full 实测——6162 文件 · 0 error / 2578 warning（较 2660 -82：路径式断链 34→0、KP 改指 50 处、汇智补题 4 恢复引用 9 处等）。基线更新为 0 error / 2578 warning；三件套纳入周检（diag_remaining + scan_question_quality）。"
---

# validate_kb 每周运行（定时巡检）

## 触发

- **cron**: `23 8 * * 1`（周一 08:23，Asia/Shanghai），会话级。
- **补跑触发**：目录/文件重组后立即跑一次（07-25 重组后 ~450 断链未被捕获的教训）。

## 执行命令

```powershell
cd "C:/Obsidion/妙妙屋"
# 三件套（2026-08-31 起纳入周检）——需用系统 Python 3.12（已装 PyYAML）
python "11-模板/scripts/validate_kb.py" --full          # 全量校验（frontmatter/断链/图片/枚举）
python "11-模板/scripts/diag_remaining.py"              # 答案缺口 + 命名 + 题目计数
python "11-模板/scripts/scan_question_quality.py"       # 逐题质量扫描（OCR 特征/选项/答案/格式）
```

## 巡检逻辑

1. 读取 `09-审计报告/auto-validation/YYYY-MM-DD-validation.md`
2. 对比基线（0 error / 1,641 warning，2026-09-01 深夜终检 full 实测；枚举 0，图片缺失 0，正文断链 45 + frontmatter 1,590 存量按指示暂不处理）
3. 周报写入 `09-审计报告/周巡检-YYYY-MM-DD.md`，**仅报异常增量**；三件套对比基线：
   - diag_remaining：`no_answer` 必须保持 0；题目计数 3,942（diag 工具口径：type=题目 3,879 + 真题 63，09-01 实测；grep 原始 3,883+63=3,946，差 4 为 YAML 解析盲区，属已知偏差）漂移即报
   - scan_question_quality：候选总数 256 基线（答案占位 192 + 已核验误报/合法项），新增问题类即报
4. 检查上轮 follow-up 断链清单是否已清
5. 顺带刷新媒体备份：`python scripts/backup_media.py`（manifest 落 10-索引与统计/媒体仓库清单.json），并检查 `09-审计报告/备份/media-backup-*.zip` 新鲜度（>7 天则重建 zip）
6. 完成后桌面通知

## 关键基线（2026-08-31 终检 full 实测）

| 指标 | 值 |
|:---|:---|
| 受检文件 | 6167 |
| Error | 0 |
| Warning | 1641（枚举 0；图片缺失 0；存量 = 正文断链 45 + frontmatter 断链 1590，按用户指示分批消解；另标题跳跃 3 + stage-门禁 3） |
| Info | 7338 |
| 答案缺口 | no_answer 0 / placeholder 211（合法）/ short 27（ABOC 思路占位无源可补） |
| 题目计数 | 3,946（grep 逐桶实测：type=题目 3,883【含 9 例题】+ 真题 63 @05-真题库；diag 工具口径 3,942。较 08-31 的 3,933 +13 = 教材习题 +10【无机例题与习题 +9（Ch09 例题转正等）+ 结构化学基础 +1】+ 教学改编 +3【择优补入】） |
| 质量扫描 | 候选 256（2026-08-31 终检；答案占位 192 = ABOC/初赛讲义已知欠账 + 已核验误报/合法项，无可自动修复） |

## 最近运行记录

- **2026-09-01 full（深夜终检）**：6167 文件 · **0 error / 1641 warning**。较 08-31（2,578）**-937**：图片缺失 357→0（355 处校验器误报修复 + 缺图恢复 + EDTA 真图挂接）、正文断链 554→45（子编号 26 处 + 阶段七~九治理 + 新建 4 个高频 KP）、frontmatter 1,642→1,590（非术语值 17 个 51 处清除）。报告 [[09-审计报告/auto-validation/2026-09-01-validation]]
- **2026-08-31 full（终检）**：6162 文件 · **0 error / 2578 warning**。较盲区补齐基线（2,660）-82：路径式断链 34→0、KP 改指 50 处（frontmatter 断链 1,724→1,642）、汇智补题 4 题并恢复 9 处引用；status-枚举 4 处（补题 status 值）已修为 `已补全答案` 归零。报告 [[09-审计报告/auto-validation/2026-08-31-validation]]
- **2026-08-31 full（盲区补齐后）**：6160 文件 · 0 error / 2660 warning。validate_kb 新增题库六字段枚举检查（仅题目类）+ frontmatter 内 wikilink 断链检查；枚举 0 告警，frontmatter 断链暴露存量 KP 红链 1724（knowledge_points 挂载不存在的 KP 标题，与 audit 同源，暂不处理）；2 个习题书附录 Error 已补 frontmatter 清零。报告 [[09-审计报告/auto-validation/2026-08-31-validation]]
- **2026-08-28 full 最终**：6509 文件 · 0 error / 2 warning / 7674 info · 断链 1 / 图片缺失 1 / 标题跳跃 0。修复：XES 50 条+33 届决赛 19 条+模块习题集 87 条+标题跳跃 2357 处+验证器排除噪音 254 条。报告 [[09-审计报告/auto-validation/2026-08-29-validation]]
- **2026-08-28 full 中间**：6591 文件 · 0 error / 456 warning · 断链 337 / 图片缺失 73（修复前基线）
- **2026-08-27 quick**：6591 文件 · 0 error / 0 warning（quick 模式不检测断链）
- **2026-08-16 full**：6266 文件 · 0 error / 1343 warning · 断链 1355（历史基线）

## 说明

- 预期 REDLINK（如 `合成设计`、`推断技术`、`13C NMR`）指向规划中的待建 KP，不是错误，与 [[00-首页/待建KP优先级清单]] 对齐。
- 模板占位符（`{…}`、`某知识点`、`KP-N`、`图名.png` 等）已被脚本排除，不再计为断链。
