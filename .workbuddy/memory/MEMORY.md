# 妙妙屋·长期记忆（2026-09-15 精简重写）

## 一、环境与工具链
- Python `C:/Users/蕾赛/.workbuddy/binaries/python/versions/3.13.12/python.exe -X utf8`。
- **双闸门**：`11-模板/scripts/jsyaml_verify.js`（`NODE_PATH="C:/Users/蕾赛/.workbuddy/binaries/node/workspace/node_modules"`）+ `validate_kb.py`（`--full` 全量；`--changed` **必须显式列文件**，每批 ≤8）。
- 讲义/习题书导出：`build-all-handout-docx.py`、`build_module_book.py`；索引 `generate_handout_readme.py`（**必须 `--apply`**）；KP 巡检 `kp_link_patrol/kp_dep_redirect/kp_bclass/kp_triage_v2.py`。
- 需绕 safe-delete 时加前缀 `CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID=`；git 路径须 `-c core.quotepath=false`。

## 二、铁律：YAML / 链接 / 批量改 md
- **js-yaml4 遇重复键/非法转义直接 THROW → 文件在 Obsidian 消失（P0）**；PyYAML 不报错。值含裸 `: ` 或 `*`/`[`/`{` 开头→加引号；含反斜杠→单引号；FM 内 wikilink 用 `/`；FM 内禁独立行 `![[...]]`。
- 链接解析：basename_map 优先、alias_map 兜底；存量断链不动；带锚点丢锚点须人工确认。
- 写 L2 前必须 ls/grep 验证 KP 名真实存在。
- 批量改 md：`open(newline="")`；重拼 fm 用 `t[e:]`；断言行数；改前快照 + 改后逐行 diff；同文件多处 Edit 必须串行；插行用 while-walk。
- 踩坑：① bash 内联 python 会吃 `\$`/反引号 → **含正则脚本必须 Write 成 .py 再跑**；② heredoc 非 ASCII 会 mojibake；③ `printf` 路径 `\04` 被当八进制 → 清单一律用 Write/python 写盘。
- **只 add 本会话文件；commit 前核 `git diff --cached --name-only | wc -l`**（禁 add→commit 一条龙）；同步核对用 `git ls-remote origin master` 比 `git rev-parse HEAD`（本仓库 tracking ref 会被沙箱吞，不可信）。

## 三、红区与协作纪律（用户定）
- **红区**：`04-题库/`、`05-真题库/`、`_归档/` 严禁触碰（除显式授权）；不动并行会话未跟踪文件。
- 成品规则：①题目显示名禁现「一分册测试-/化学能力测试-」；②模拟卷 ≤15 题；③模拟卷/专项卷教师版+学生版双份；④随堂学生版除真题外无来源行/难度分布行；⑤ docx 无封面；⑥图引用纯哈希名 `![[hash.jpg]]`。
- 其他：质量优先难度；新题默认 10-待审核；每批 L2 完立即追加索引；废弃机制 `status:deprecated` + `deprecation_reason` + `superseded_by`。

## 四、Word 产物：pandoc/texmath 限制与守卫
- **pandoc 限制**：不支持 `\ce{}`（须预处理）；math 内禁 `\textbf`；定界符内侧空格不识别为数学；`$$` 与内容夹空行 → 整体放弃识别（须删块内空行，奇数 `$$` 须跳过）；闭合 `$` 不得后跟数字；不支持 `\displaylines`。
- **texmath 拒绝转换两类**：①字体开关 `\bf/\sf/\rm/\it/\sl/\sc/\tt`（含 `\boldsymbol{\rm …}`）→ 换等义命令、**必须保留外层花括号**；②`\text{}` 内反斜杠命令（`\cdot/\sim/\times`）→ 换等义 Unicode。**诊断铁律：`pandoc -t native` 的 InlineMath 会骗人，必须 `pandoc -t docx` 抓 `Could not convert TeX math`**。
- **等宽段**：`VerbatimChar` 段 = 真代码块（pStyle=SourceCode）+ 正文行内反引号，1 代码块 = 1 段；`docx_utils.postprocess_pandoc_docx()` 的**样式层 + run 层**都会抹掉等宽 → `MONO_FONT="SimSun"` + `MONO_STYLES={"VerbatimChar","SourceCode"}` **两层**豁免；补历史产物用 `patch_mono_font.py`。行内反引号 65% 集中在数学工具区。代码块转列表禁用 `for`+手动 i，层级取前缀**最后**一个分支符列号。
- **`attachments/`**：Obsidian 默认附件目录须进 pandoc `--resource-path` 与图片解析候选，否则 `--strict-images` 拒收整份导出。
- **CRLF/LF**：`.gitattributes` 声明 `*.md eol=lf` → `git diff` 看不见行尾变化；"零抖动"只能靠脚本内断言或 `newline=""` 计数；仓库同时存在纯 LF 的 md。
- `NORMALIZE_SIMPLE_INLINE_SCRIPTS = False`：曾把 `$MT^{-2}$` 降级成 Unicode 文本。
- **最痛教训**：连续多轮「以为修完」，下一轮换维度复检又冒出几十处 → **收官前必须换维度再查一轮**；扫描口径一旦排除某类产物（如打印版），那类就永远"干净"；校验器"通过"前先看它扫了多少文件（扫 0 文件也是静默失效）。
- 「（Word清稿）」由 `--word-clean` 生成，源 md 即同名 `-超级充实版（自学完整）.md`；**改源后必须单独 `--path <md> --word-clean`**。
- 活跃区 docx A 类（LaTeX 源码态）/ B 类（花括号上下标）已全归零；**推送很慢（>5 分钟），前台会 SIGTERM，须 `run_in_background`**。

## 五、学生讲义 / 13-教案 / 数学工具
- 源 `04-课件/学生讲义/` 分模块，产物 `06-学生侧材料/讲义/<同名子目录>/`；**讲义不分教师/学生版**，含练习+答案，教师信息放 HTML 注释。
- 批量导出扫描口径：递归 `*.md`，排除 `_归档`/`_` 开头目录、`README`、`讲义升级模式-` 前缀，且**只保留 stem 含 `超级充实`/`基础版`/`复习`/`-新课` 者**（该 marker 过滤仅用于批量默认路径，**单文件 `--path` 不受限**）。
- 数学工具区：**行内数学一律裸 `$...$`，禁反引号包裹**；表格内绝对值写 `\lvert x\rvert`；文件级 `$` 数须偶。
- 13-教案（必修一）52 md + 45 docx + 18 张 Mermaid（`.mmd` 源）：核心素养统领、含逐字稿、三层作业、一课时一 md。

## 六、mineru OCR 公式字符拆分（已收官）
- 两形态：①相邻数字被空格拆；②小数点被空格包围（行内也中招）。规则：`(?<![\d.])\d(?: \d)+`→去空格；`(\d)\s*\.\s+(\d)`→`\1.\2`。
- **安全策略**：只在公式内（行内禁跨行）；文件级 `$` 须偶；区间级跳过（裸中文/空行无 `\begin{`/长且无命令）；`\text|\mathrm|\ce` 内容保护；位数防护；行数守恒；红区/归档/未跟踪/20 分钟内改动不碰。
- **SCAN 是硬编码白名单** → 须定期对照根目录 `ls` 复核（曾漏根目录散装教材约 1.4 万处）。
- 遗留：`$` 奇数 13 文件/30 处（OCR 把 `$` 与 `()` 互识）；字母拆分仅普查未修。

## 七、题库线与 git 事故教训
- 题库 5,369 题；KP 挂载率 100%；专项卷 24 卷 600 题 + 随堂卷 11 卷 235 题。
- **沙箱 safe-delete 会把 `.git/objects/` 的删除移入回收站**（`$I` 存原始路径含 `.git\objects\XX\YYY`，同名 `$R` 是内容）→ **回收站是第一恢复源**。
- **本仓库 `fsck` 不可信**（畸形 pack 空 `.idx` 会漏报），判据用 `git cat-file -e`；promisor 会制造假绿（须取消后重跑真实 fsck）；`git fetch <sha>` / `gc` / `repack` / `prune` / `--refetch` 属红线。
- 30 天以上日志按主题并入本文件后再删；明细见同目录 `YYYY-MM-DD.md`。
