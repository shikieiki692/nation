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

## 五、验收记录（2026-09-15）

在 tmp 与 qa 两处各跑一次同样脚本，**逐字节比对 stdout / 产物**，结论见任务卡
`任务卡-2026-09-14-习题书裸下标收口与git健壮性复核` §P0-2。

---

*固化：2026-09-15（习题书·排版线）。原 `tmp` 副本暂留作安全网，清理并入 P2-5。*
