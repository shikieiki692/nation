---
title: 口径与对账工具（部分索引）
type: 系统
role: 工具索引
updated: 2026-09-21
tags: [系统, 工具, 题库, 口径, 对账]
---

# 口径与统计对账工具（`.workbuddy/scripts/`）

> ⚠️ **本索引只收录「题库口径 / 统计对账」类工具**（2026-09-21 新建）；本目录共 200+ 个文件，
> 其余为各线一次性/专项脚本，未逐一登记。
> ⚠️ 本目录被 `.gitignore` 的 `scripts/` 规则遮蔽 ⇒ 新增文件须 `git add -f`
> （判据 `git check-ignore -v --no-index <路径>`）。
> ⚠️ 统一跑法：`"C:/Users/蕾赛/.workbuddy/binaries/python/versions/3.13.12/python.exe" -X utf8 <脚本>`
> （在仓库根执行）。

| 工具 | 用途 | 通过判据 |
|:--|:--|:--|
| `qb_full_measure.py` | **题库全量口径实测**：仓储 / 组卷池 / md 数 / 各学科模块 / 视图三档 / pack / fidelity。任何「刷数字」前先跑它取准数 | 输出无 `校验 ❌`，且组卷池＝仓储＋`05-真题库`真题 |
| `verify_source_map.py` | **溯源映射 vs 成书逐章对账**（每次重建习题书后必跑） | `分组数 = 36` 且 `不一致条目数 = 0`（逐章 `question_count` 全等） |
| `measure_dir_tree.py` | **目录树 / 源头表实测**：逐子目录 md 计数（供 `04-题库/README.md` 目录树、`教材习题/README.md` 表重写） | 各分行之和 ＝ 根总数（如 6,399） |
| `scan_stale_stats.py` | **过期统计数字全库扫描**：千分位 ＋ 三位数同表；**十六进制边界排除**避开 SHA1/行号假阳性；行内须含「题库/题目/教材/…」上下文词 | 命中项逐条定性后，只剩历史流水（`归档/`、`工作日志/`、已完成的卡） |

## 相关（不在本目录）

| 工具 | 位置 | 用途 |
|:--|:--|:--|
| `build_source_map.py` | `11-模板/scripts/` | 生成/重建 `04-课件/习题集/溯源映射.json`（成书题 ↔ 题库源文件；**重建后必须跑本目录的 `verify_source_map.py` 对账**） |
| `build_module_book.py` | `11-模板/scripts/` | 生成习题书 md 源（成书取题池＝`gather_questions` 口径，见 `04-题库/题库架构总览.md` §四c） |
| `validate_module_book.py` | `11-模板/scripts/` | 成书双版本校验（目录 vs 章节文件一致性） |
| `validate_kb.py` / `jsyaml_direct.js` | `11-模板/scripts/`、`.workbuddy/tmp/` | 改 md 后的双闸门（受检数须按**域内**文件数核） |
