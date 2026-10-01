---
title: 口径与对账工具（部分索引）
type: 系统
role: 工具索引
updated: 2026-09-23
tags: [系统, 工具, 题库, 口径, 对账]
---

# 口径与统计对账工具（`.workbuddy/scripts/`）

> ⚠️ **本索引只收录「题库口径 / 统计对账」类工具**（2026-09-21 新建）；本目录共 200+ 个文件，
> 其余为各线一次性/专项脚本，未逐一登记。
> ⚠️ 本目录被 `.gitignore` 的 `scripts/` 规则遮蔽 ⇒ 新增文件须 `git add -f`
> （判据 `git check-ignore -v --no-index <路径>`）。
> ⚠️ 统一跑法：`"C:/Users/蕾赛/.workbuddy/binaries/python/versions/3.13.12/python.exe" -X utf8 <脚本>`
> （在仓库根执行）。
> **权威校验入口**：`11-模板/scripts/validate_kb.py --full`；变更批次可用 `--changed`。本目录脚本负责专项口径/对账，不替代权威校验器。

| 工具 | 用途 | 通过判据 |
|:--|:--|:--|
| `qb_full_measure.py` | **题库全量口径实测**：仓储 / 组卷池 / md 数 / 各学科模块 / 视图三档 / pack / fidelity。任何「刷数字」前先跑它取准数 | 输出无 `校验 ❌`，且组卷池＝仓储＋`05-真题库`真题 |
| `verify_source_map.py` | **溯源映射 vs 成书逐章对账**（每次重建习题书后必跑） | `分组数 = 36` 且 `不一致条目数 = 0`（逐章 `question_count` 全等） |
| `measure_dir_tree.py` | **目录树 / 源头表实测**：逐子目录 md 计数（供 `04-题库/README.md` 目录树、`教材习题/README.md` 表重写） | 各分行之和 ＝ 根总数（如 6,399） |
| `scan_stale_stats.py` | **过期统计数字全库扫描**：千分位 ＋ 三位数同表；**十六进制边界排除**避开 SHA1/行号假阳性；行内须含「题库/题目/教材/…」上下文词 | 命中项逐条定性后，只剩历史流水（`归档/`、`工作日志/`、已完成的卡） |

## 2026-09-23 校验与生命周期对账工具

| 工具 | 用途 | 通过判据 |
|:--|:--|:--|
| `question_intake_gate.py` | 题库字段与引用闸门；兼容显式生命周期 `replacement_status: 无替代` / `待人工对账` | `--strict` 无新增阻断；存量字段欠账单独统计 |
| `check_deprecation_targets.py` | 弃用替代链闭环检查；`derived_from` 只作来源证据 | `错误 0`；未闭环项必须显式为 `待人工对账`，无替代项必须显式为 `无替代` |
| `jsyaml_scan_all.js` | 全库 frontmatter 严格扫描（解析兼容层） | `未闭合 0 / 解析失败 0` |

> **YAML 后端口径**：兼容链基于 `ruamel.yaml`，只覆盖本库实际 YAML 子集与双解析器一致性检查，不宣称等价于 js-yaml 4 全部行为。
> **弃用状态口径**：`superseded_by` 必须指向可解析的完整替代卡；确实无替代写 `replacement_status: 无替代`；需人工核对来源写 `replacement_status: 待人工对账`。

## 2026-09-21 批量固化：闸门 / 题库审计 / 组卷（自 `tmp/` 提升）

> **背景**：这些脚本此前只存在于 `.workbuddy/tmp/`（**被 gitignore、换机即失**），而多份活文档
> 却把它们写成「复跑脚本 / 验收判据」。2026-09-21 逐字节提升入库，并把文档指针改指本目录。
> 提升前已自证：UTF-8 可解码 ＋ `py_compile`／`node --check` 通过 ＋ 无重名。

| 工具 | 用途 | 通过判据 |
|:--|:--|:--|
| `jsyaml_direct.js` | **双闸门之①**：直检指定文件的 frontmatter（`js-yaml` 与 `jsyaml_verify.js` 同解析方式）。`04-课件/` 不在 jsyaml 扫描域时用它直检 | manifest 传**相对 vault 路径**；`失败 0` |
| `zchem_jsyaml_check.js` | 同族 js-yaml 校验器（zchem 批次口径） | `失败 0` |
| `scan_bare5.py` | **裸下标扫描**（遮蔽加固版：code span／数学域／图片名排除） | 报「处/文件」逐条可核 |
| `scan_heading_bare.py` | 标题内裸下标扫描（含元文件标题） | 同上 |
| `audit_packs.py` | git pack 健康：逐 pack `show-index` 计数 ＋ 抽样 `cat-file -e` | `畸形 0` |
| `scan_docx_pollution.py` | docx 文本层污染扫描（如 `^θ`、字面 `$`） | `A=0 / B=0` |
| `sum_qc.py` | 逐章 `question_count` 求和（＝成书 BOOK_STATS ＝ README 篇构成） | 三处相等 |
| `gen_acd_list.py` | 裸下标 A/B/C/D 四型清单导出（习题书师版口径） | 四型计数自洽 |
| `t1_qa.py` | 讲义 T1 质检：docx vs md 题量／图数／答案泄漏 | 三项均为 0 差异 |
| `gen_source_norm.py` | **`source_norm` 字段生成**（按路径推导归一化来源；幂等＋重试 5 次＋失败清单）。组卷同源限流一律用它 | 失败清单为空、幂等（连跑两次结果一致） |
| `measure_workbench_fields.py` | 组卷工作台字段覆盖率实测（复跑即刷新分母） | 覆盖率与分母一并报出 |

## 相关（不在本目录）

| 工具 | 位置 | 用途 |
|:--|:--|:--|
| `build_source_map.py` | `11-模板/scripts/` | 生成/重建 `04-课件/习题集/溯源映射.json`（成书题 ↔ 题库源文件；**重建后必须跑本目录的 `verify_source_map.py` 对账**） |
| `build_module_book.py` | `11-模板/scripts/` | 生成习题书 md 源（成书取题池＝`gather_questions` 口径，见 `04-题库/题库架构总览.md` §四c） |
| `validate_module_book.py` | `11-模板/scripts/` | 成书双版本校验（目录 vs 章节文件一致性） |
| `validate_kb.py` | `11-模板/scripts/` | **权威校验器**；全量跑 `--full`，小批次跑 `--changed` |
| `jsyaml_scan_all.js` | `.workbuddy/scripts/` | 全库 YAML 兼容层严格扫描 |
| `question_intake_gate.py` | `.workbuddy/scripts/` | 题库字段与引用专项闸门 |
| `check_deprecation_targets.py` | `.workbuddy/scripts/` | 弃用替代链闭环检查 |
| `classify_broken_links_v5.py` | `.workbuddy/scripts/` | 当前断链分诊入口 |
| `broken_link_audit.js` | `.workbuddy/scripts/` | **已退役**；由 `classify_broken_links_v5.py` 与 `11-模板/scripts/validate_kb.py --full` 替代 |
