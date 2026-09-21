---
title: 讲义产线与只读诊断工具（部分索引）
type: 系统
role: 工具索引
updated: 2026-09-21
tags: [系统, 工具, 讲义, 诊断, 产线]
---

# 讲义产线与只读诊断工具（`.workbuddy/scripts/`）

> 与 [[.workbuddy/scripts/README-口径与对账工具]] 同族：那份管「题库口径/对账」，本份管「讲义产线 + 只读诊断」。
> 统一跑法：`"C:/Users/蕾赛/.workbuddy/binaries/python/versions/3.13.12/python.exe" -X utf8 <脚本>`（仓库根执行）。
> ⚠️ 本目录被 `.gitignore` 的 `scripts/` 规则遮蔽 ⇒ 新增文件须 `git add -f`。
> ⚠️ 2026-09-21 自 `tmp/` **逐字节**提升入库（此前活文档承诺「可复跑」却只存在于易失目录）；提升前自证：UTF-8 ＋ 语法编译通过。

## 一、讲义产线（ASCII 图 / 等宽段 治理）

| 工具 | 用途 | 备注 |
|:--|:--|:--|
| `stage5_match.py` | 主题级命中匹配（**命中后必须逐条目看「内容描述」列**） | 先匹配后画图 |
| `stage5_draw.py` | 8 张图生成器（RDKit 骨架式 ＋ matplotlib 能级/势能/机理） | 产出 PNG |
| `stage5_ingest.py` | 按 sha256 入 `媒体仓库/` ＋ 输出映射 JSON | 纯哈希命名 |
| `stage5_apply.py` | 逐块签名断言 ＋ 行尾跟随 ＋ 围栏计数断言的落盘器 | **默认 dry-run** |
| `stage5_index.py` | 索引登记（追加行，不动导航与计数） | — |
| `stage5_audit.py` | 逐块上下文导出（含「上方 14 行是否已有图片/表格」） | 供人工定规则 |
| `verbatim_worklist.py` | 扫活跃讲义源 md，按 ``` 围栏切块 → 逐块处置清单（CSV）＋ 双向对账 ＋ 未闭合围栏检测 | 源侧 |
| `verbatim_report.py` | 产物侧口径（SourceCode 段 / 行内）统计 | 产物侧 |
| `convert_batch.py` | 代码块→列表/表格 转换器（`--selftest` / dry-run / `--apply` / `--only`） | 带单测入口 |
| `dump_blocks.py` | 按分型导出块内容，供人工定规则 | 只读 |
| `patch_mono_font.py` | 阶段 6 字体补丁（`--apply`） | docx 后处理 |
| `push_batches.py` | 网络抖动时**按 ~5 MB 分批推送** | 配合 `github-push-proxy-recovery` |

## 二、只读诊断（不落盘，可随时复跑）

| 工具 | 用途 |
|:--|:--|
| `kp_consumption_audit.py` | 统计指定 KP 在 学生讲义／备课大纲／专题页／题库 四类消费端的 `[[ ]]` 引用次数 |
| `triage_html_img3.py` | 全库 `<img src>` 分层（四层判据），复现「175 个 md 含 img」清单 |
| `triage_archived_links_0916.py` | 归档区链接三形态分诊 ＋ 报告 |
| `verify_kp_links_0916.py` | frontmatter 内 wikilink 目标存在性 + 弃用页核查 |
| `audit_first_round.py` | 第一轮化学原理习题集机检（题数/图数/答案） |

## 三、未提升（有意保留在 `tmp/`）

`simul*.py`（综合模拟卷/专项卷的**一次性选题脚本**，带 seed 与期次，属历史生成记录）、
`special_papers*.py`（同族；其中 `special_papers.py` 已在别处入库）、以及各种 `_commit_msg_*` 等**命名示例占位**。
