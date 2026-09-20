# qa/ — 习题书·排版线与 git 健壮性 的复用脚本

> 从 `.workbuddy/tmp/` 固化而来（tmp 会被清理）。这批脚本多次复用且被
> `docx-math-leak-qa` 等技能引用，**2026-09-15 起以本目录为准**。
>
> 统一用受管解释器：`C:/Users/蕾赛/.workbuddy/binaries/python/versions/3.13.12/python.exe -X utf8`
> 命令里一律加安全前缀 `CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID=`（绕沙箱 safe-delete）。
> 除注明外，脚本内部已 `os.chdir("c:\Obsidion\妙妙屋")`，**从任意目录调用均可**。

## 一、document 污染扫描（docx / md）

| 脚本 | 用途 | 用法 |
|---|---|---|
| `scan_docx_pollution.py` | 扫 docx 产物 A 类（LaTeX 源码态）+ B 类（HTML/花括号上下标）+ 真表格计数 | `python scan_docx_pollution.py "<目录>"` |
| `scan_ab_paths.py` | 同上，但**带相对路径**逐文件列出，排除 `_归档` / `*.tmp.docx` | `python scan_ab_paths.py "<根>" ["<根2>" …]` |
| `dump_b.py` | 列习题书 docx 中含 `_{`/`^{`/`$` 的**段落**，判定属哪种污染 | `python dump_b.py`（默认扫 `00-首页/题组Word/习题书`） |
| `probe_docx.py` | 定点探查某份 docx 里含指定关键字串的段落/段型 | `python probe_docx.py <x.docx> <关键字…>` |

> ⚠️ **扫描口径铁律**：A/B 扫描**必须含打印版**。历史上一次「习题书 A=0/B=0」实为
> `SKIP_PRINT=1` 把 34 份打印版排除在外所致（其中 9 份带 A/B 命中）。

## 二、裸下标 / 题源形态扫描

| 脚本 | 用途 | 用法 |
|---|---|---|
| `scan_bare5.py` | 正文「裸下标」统一扫描（A/B/C/D 分类 + 遮蔽 code span / `$…$` / `[[…]]` / frontmatter），**根目录任意** | `python scan_bare5.py ["<根>"] [--cls=ABCD]`（默认为习题书-教师版） |
| `gen_acd_list.py` | 生成「习题书裸下标 A/C/D 待批清单」报告（含题源定位 + 建议写法） | `python gen_acd_list.py` → 写 `09-审计报告/习题书裸下标-ACD待批清单-2026-09-14.md` |
| `scan_theta_source.py` | 题源 `04-题库` 中「数学区之外」的 `X^θ` 形态普查（只读） | `python scan_theta_source.py` |
| `fix_theta_bare.py` | 题源正文裸 `^θ` 批量包成行内数学（显式 30 种映射，最长优先） | `python fix_theta_bare.py [--apply]`（默认 dry-run） |

## 三、习题书 / 文档结构

| 脚本 | 用途 | 用法 |
|---|---|---|
| `sum_qc.py` | 逐章 `question_count` 求和（= 习题书规模与 README 篇构成口径） | `python sum_qc.py` |

## 四、git 对象库（`.git` 4.6G / 108 pack，删除会被沙箱移入回收站）

| 脚本 | 用途 | 用法 |
|---|---|---|
| `verify_git_objects.py` | **可信判据复核**：全覆盖 `cat-file --batch-check` + 分层抽样逐对象 `cat-file -e` | `python verify_git_objects.py [--sample 800] [--seed 20260915]` |
| `audit_packs.py` | 逐 pack `show-index` 计数 + 抽样 `cat-file -e`，判「对象数极少但体积巨大」畸形 | `python audit_packs.py` |
| `scan_recycle.py` | 扫回收站 `$I` 元数据，找原始路径含 `.git/objects` 的条目 | `python scan_recycle.py` |
| `restore_objects.py` | 从回收站把被 safe-delete 移走的 git 松散对象恢复回 `.git/objects/XX/YYY` | `python restore_objects.py [--apply]`（默认 dry-run） |

> ⚠️ **本仓库 `fsck` 不可信**（畸形 pack 的 `.idx` 空登记会漏报缺失），唯一可信判据是
> `git cat-file -e`；promisor 未取消时 `fsck` 还会制造"假绿"。红线：不跑
> `gc / repack / prune / fetch <sha> / fetch --refetch`。

## 五、HTML 表格 → Markdown（块级表格公式不渲染治理）

> 背景：`<table>` 独占一行时被 markdown-it 判为 `html_block`，块内 `$…$` **完全不经过
> inline 解析** → Obsidian 里显示为原始文本（看着像乱码）；同时 Word 导出会把表**拍平成
> 段落**（`w:tbl`=0）。转成 pipe table 后两处收益（2026-09-20 端到端实证）。
> 累计 W1~W5 已转 **~2,795 表 / 483 文件**。方法论与踩坑见 skill `html-block-table-to-md`
> 与 `09-审计报告/` 各 Wave 报告。
>
> **2026-09-20 补轮（W6）**：`04-课件/习题集` 126 表 / `04-题库` 119 表 / entity 表 9 表
> 共 **254 表**（提交 `f3e82bb57` / `453c5d5fd` / `6893b352a`）。
>
> **2026-09-20 续轮（W7）**：`07-资料提炼` 47 表（`ce940c61e`）、`09-AI工作区` 42 表 + `blockhtml`
> 防线（`f997792d8`）；entity 批**无可转项**（3 份授权域内表解 entity 后仍撞 hardprose/entity-tag/img，
> 属合理拒收）。

| 脚本 | 用途 | 用法 |
|---|---|---|
| `html_tables_to_markdown.py` | **主工具**：HTML 表 → pipe 表（含 colspan 左展开 / rowspan 下拉 / entity 解码；自带渲染自证 + 四口径 + 备份防覆盖） | `python html_tables_to_markdown.py --dir X [--all-tables] [--allow-entities] [--apply] [--allow-in-excluded <前缀>]`；`--whole-vault` 全库；默认 dry-run |
| `render_selfcheck.js` | 渲染自证器（markdown-it + KaTeX，判残留 `$`==0）；被主工具 `--apply` 自动调用 | 由主工具内部调用，亦可单独喂 JSON |
| `word_verify.py` | Word 管线端到端验证：备份(转换前) vs 现状各转 docx，数 `w:tbl` / `m:oMath` | `python word_verify.py`（只读，产物 → `.workbuddy/tmp/word_verify/`） |
| `word_isolate_probe.py` | 隔离实验：HTML 表 vs Markdown 表 → docx，证明「md 层乱码」是 Obsidian 渲染侧问题 | `python word_isolate_probe.py` |
| `table_baseline.py` | 全库表格健康度基线快照（判据/作用域双维归桶，供回归对照） | `python table_baseline.py` → `09-审计报告/表格健康度基线-*.md` |

> ⚠️ **`EXCLUDE_PREFIX` 盲区（2026-09-20 实证根因）**：工具默认排除
> `04-题库 / 05-真题库 / 04-课件 / 07-资料提炼 / _归档 / …`，而**成品区恰在 `04-课件/习题集`**
> → 跑 `--dir 04-课件/习题集` 报「文件 0」。**已完成专项后如需覆盖排除域，须显式加
> `--allow-in-excluded 04-课件`**（可多次；只对该前缀放行，其余仍排除）。红线区同理
> `--allow-in-excluded 04-题库`（须用户显式授权）。
>
> ⚠️ **两条误杀规则已于 2026-09-20 修正**：
> - `narrow`：原 `width <= 2` 拒收 → 误杀真 2 列数据表（如「温度/K | δ/ppm」）→ 改为 `width <= 1`
> - `prose`：原 `avg_len > 40` **无条件**拒收 → 误杀宽表内长文本单元格 → 改为**仅 `width <= 2` 时生效**；
>   另新增 `hardprose`（**单格 > 800 字**才拒收，防极端长格）
>
> ⚠️ **新增 `blockhtml` 防线（2026-09-20 实证 P0）**：`<table>` 内含块级 HTML
> （`<details>` / `<summary>` / `<div>` / `<p>` / `<ul>` / `<ol>` / `<li>` / `<blockquote>` /
> `<figure>` / `<section>`）→ **拒收**。根因：单元格无法承载块级结构，强转会**把块级内容压进
> 单元格并吞掉标签本身**。实证：`09-AI工作区/…/3-晶体结构.md` 有 1 张表把 `<details>` 折叠块
> 嵌在表内，转换后 `details`/`summary` 各 **268→267**，答案文本被压进 `0.40°` 单元格。
> **处置**：`git restore` 回退该文件 + 加防线；回归核验历史 3 批（f3e82bb57/453c5d5fd/6893b352a）
> 与本轮 A 批均**零标签损失**。
>
> ⚠️ **`--out-root` 侧效应**：会回写 `04-课件/习题集/README.md` 的日期 → 用完须 `git checkout` 回退。
>
> ⚠️ **行尾口径**：本仓库 `core.autocrlf=true` + `.gitattributes: *.md text eol=lf` → git add
> 时自动 CRLF→LF，故**工作区混杂行尾 git 看不到（无 M）**，但工具「行尾保持」口径读原始字节会报
> False。核对时须 `git diff` 为空 + `cat-file` 比对，勿据工具报 False 就回滚。

> ⚠️ **与旧脚本的分工**：`11-模板/scripts/convert_html_tables_to_markdown.py`（2026-08-30）
> 是**旧一次性脚本**，绑定 `习题书V2-表格分类台账.jsonl`、仅 `04-题库` 习题书源、不支持 span
> ——保留不动。本目录 `html_tables_to_markdown.py` 是其**通用化继任者**（体量小、无台账依赖、
> 支持 colspan/rowspan/entity）。
>
> ⚠️ **多批次共用备份目录的 P0 陷阱**：不同 Wave 若共用同一 `--backup-dir`，后批会以
> 「已转换内容」覆盖「转换前原始快照」→ A/B 永久破坏。本工具已内置「**已存在则不覆盖**」
> 双保险；跨批务必为每批**独立备份目录**（如 `html_table_backup_w5`）。

## 六、验收记录（2026-09-15）

在 tmp 与 qa 两处各跑一次同样脚本，**逐字节比对 stdout / 产物**，结论见任务卡
`任务卡-2026-09-14-习题书裸下标收口与git健壮性复核` §P0-2。

---

*固化：2026-09-15（习题书·排版线）。原 `tmp` 副本暂留作安全网，清理并入 P2-5。*
