# 妙妙屋·长期记忆（2026-09-11 精简重写）

## 一、环境与工具链
- Python `C:/Users/蕾赛/.workbuddy/binaries/python/versions/3.13.12/python.exe -X utf8`。
- **双闸门**：`11-模板/scripts/jsyaml_verify.js`（`NODE_PATH="C:/Users/蕾赛/.workbuddy/binaries/node/workspace/node_modules"`，`--list <清单>`/`--dir`）+ `validate_kb.py`（`--full` 全量；`--changed` **必须显式列文件，无参检出 0**，每批 ≤8，该 git 版本无 `--pathspec-from-file`）。
- 讲义导出 `11-模板/scripts/build-all-handout-docx.py`（须 `CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID=` 绕 safe-delete）；讲义索引 `generate_handout_readme.py`（**必须 `--apply`**）；KP 巡检四件套 `kp_link_patrol/kp_dep_redirect/kp_bclass/kp_triage_v2.py`（前三者已入周一 08:00 自动化）。
- git 路径须 `-c core.quotepath=false`；Obsidian 索引只看 `.obsidian/app.json` 的 `userIgnoreFilters`。

## 二、铁律：YAML / 链接 / 批量改 md
- **js-yaml4 遇重复键或非法转义直接 THROW → 整条文件在 Obsidian 消失（P0）**；PyYAML 不报错，只有 js-yaml 闸门能抓。值含裸 `: ` 或 `*`/`[`/`{` 开头→加引号；**含反斜杠的值一律单引号**；FM 内 wikilink 用 `/` 禁 `\`；FM 内禁独立行 `![[...]]`。
- 链接解析：basename_map（文件名）优先、alias_map（title/alias）兜底；**存量断链不动**；带锚点链接丢锚点须人工确认。
- 写 L2 前**必须 ls/grep 验证 KP 名真实存在**（英文/带空格/带 `-` 的名字 90% 不存在）。
- 批量改 md：读写一律 `open(newline="")`（否则整文件行尾被改写）；重拼 fm 用 `t[e:]` 拼 `"---"+new_fm+body`；断言行数；改前 zip 快照 + 改后逐行 diff；**同一文件多处 Edit 必须串行**；批量插行用 while-walk，禁 `for`+手动 i。
- 三个已踩坑：① bash 内联 python 会吃 `\$`/反引号 → **含正则的脚本必须 Write 成 .py 再跑**；② heredoc 含 emoji/非 ASCII 正则会 mojibake 出假统计；③ `printf` 拼路径 `\04-题库` 被当八进制转义 → 清单一律用 Write/python 写盘。
- 只 add 本会话改动文件；**commit 前必须单独核 `git diff --cached --name-only | wc -l`**（禁 add→commit 一条龙）；核对推送用 `git ls-remote origin master` 比对 `git rev-parse HEAD`（本仓库**无** origin/master tracking ref，`git log origin/master..HEAD` 会静默输出 0）。

## 三、红区与协作纪律（用户定）
- **红区**：`04-题库/`、`05-真题库/`、`_归档/` 严禁触碰（除显式授权）；不动并行会话未跟踪文件。
- 成品规则：①题目显示名禁现「一分册测试-/化学能力测试-」；②模拟卷 ≤15 题；③模拟卷与专项卷一律教师版＋学生版双份；④随堂学生版除真题外无来源行/难度分布行；⑤ docx 无封面；⑥图引用纯哈希名 `![[hash.jpg]]`，禁别名。
- 其他：质量优先难度；新题默认 10-待审核；每批 L2 完立即追加索引；合并孪生页先判重复 vs 分层（分层带「深化」）；废弃唯一机制 `status:deprecated` + `deprecation_reason` + `superseded_by`。

## 四、Word 产物：口径、教训与守卫
- **等宽段口径（2026-09-11 实测纠正，原任务卡有误）**：81 份活跃产物 `VerbatimChar` 段 818 = **真代码块（pStyle=SourceCode）158 + 正文夹行内反引号 660**（后者样式为 Compact/BodyText/FirstParagraph/BlockText/…，本来就是正文、无围栏可拆）。**pandoc 把整个代码块塞进一个 `<w:p>`（块内换行用 `<w:br/>`）→ 1 代码块 = 1 段**，"多行块展开成多段"是错的。**活跃产物不存在 Courier 等宽渲染**（`styles.xml` 无任何等宽字体）；带等宽的只有 `_archive/` 3 份旧产物。
  - 治理工具（`.workbuddy/tmp/`）：`verbatim_report.py`（产物侧，按 `w:pStyle` 分 SourceCode/行内并三分类；基线快照 `verbatim_baseline_pre.json`）、`verbatim_worklist.py`（源侧，按 ``` 切块记录起止行号 + 建议分型 + 与 docx 对账 + 未闭合围栏检测，输出 `verbatim_worklist.csv`）。旧 `scan_verbatim.py` 保留未改，以便复现旧口径。
  - **活跃源集合口径**：`04-课件/学生讲义/**/*.md` 只排除 `_归档`、首层 `_` 目录、`README`、`讲义升级模式-` 前缀；**绝不能加 `超级充实/基础版/复习/-新课` marker 过滤** —— 该过滤只在批量默认路径生效，大量产物（`自由基反应`/`醛酮羧酸`/`有机波谱分析`…）是显式 `--path` 构建的。
  - 对账：源 md 围栏块数与 docx `SourceCode` 段数**逐 stem 精确对应**（残留 1 处为下述缺陷）。
  - **未闭合围栏缺陷**：`有机化学/醇醚胺酚.md` L396 全文只有 1 个 ``` → pandoc **不识别**，``` 会字面印进 Word（`FirstParagraph`）。已确认另 `分光光度法`/`氧化还原滴定与沉淀滴定` 的"奇数围栏"是 ``` ```` ```text ```` 带信息串造成的误报，判据已修正。
  - **试点结论（已验证，可铺开）**：判断树(`├─└─`)→**嵌套列表**（pandoc 保真 3 层，`ilvl` 0/1/2）、压平有序步骤→**有序列表**（`numFmt=decimal`）、竖向管道流程→有序列表 三条路径均通；单文件 `SourceCode` 3→0，行内 660 不受影响，A=0/B=0 未破坏，`qa_comprehensive` 汇总空，双闸门 0 Error/0 Warning，**行尾零抖动**。
  - **可复用转换器 `.workbuddy/tmp/convert_batch.py`**：判断树→嵌套列表 / 压平步骤→有序列表，含自测（用试点块反推校验）、严格准入（含 `$`/反引号/`*`/`_`/`[]`/`\`/`<`/`|` 或列对齐空格即整块放弃）、`--only` 限定、`--apply` 才落盘、逐文件断言 行数/CRLF 变化量、幂等。**三个必记 bug**：①层级要取前缀里**最后**一个分支符的列号（取行首 `│` 会把 `│ └──` 嵌套压平）；②围栏断言勿写死 `== "```"`（要容 ```text 信息串）；③新行行尾**跟随该块自身**，勿一律补 `\r`（会把纯 LF 文件写成混合行尾）。
  - **批次进展**：批次1（判断树 10 + 步骤 3 = 13 块 / 10 文件）已落盘并重导 → 全库 818→**802**，真代码块 158→**142**，**源 md 142 块 ↔ 产物 142 段 0 不匹配**，未闭合围栏清零（`醇醚胺酚.md` 已修）。
  - **批次2 + 阶段6**：①扩 `try_inline` 规则（无缩进/无列对齐/无活性字符才出块）→ 38 块 / 13 文件，全库 802→**764**（真代码块 142→**104**）；②**字体修复**——等宽被**两处**抹掉：样式层 `for style in doc.styles` + **run 层**（run 级直格式覆盖样式，只改样式无效），已新增 `MONO_FONT="SimSun"` / `MONO_STYLES={"VerbatimChar","SourceCode"}` 两层豁免；③`patch_mono_font.py` 给历史产物打补丁，**81/81 生效、0 损坏、幂等**（注意 styles.xml 前缀是**混合**的：VerbatimChar 用 ns0:、SourceCode 用 w:）。
  - **启发式分型桶并不纯**：`文字型`/`反应式` 里混着 `Br` 竖排骨架、坐标轴等真示意图 → 禁止按桶批处理，必须靠"缩进/列对齐"守卫挡在门外。
  - 剩余 104 段：几何结构式/结构图连线居多（真图，需转图片或留等宽），判断树/步骤/数据表剩余部分需逐块人工。
  - 行内反引号高度集中：660 段中 **430 段（65%）在数学工具区**（第1/4/5/6讲各 76-95 段）→ 后续单独治理优先攻这里。
  - 具体清单与复现命令见 `09-审计报告/讲义等宽段治理-口径与清单-2026-09-11.md`。
- **字体被归一化抹掉**：`docx_utils.py` 的 `postprocess_pandoc_docx()` 中 `for style in doc.styles:` 会把模板里 `VerbatimChar` 的 `SimSun` **强制替换成 `FangSong`**、ascii 统一成 TNR → ASCII 图失去等宽网格而错位。治等宽必须豁免 `VerbatimChar`/`SourceCode` 两个样式。
- **「（Word清稿）」不是孤儿产物**：由 `--word-clean` 生成，源 md 即同名 `-超级充实版（自学完整）.md`。活跃区 7 份：方程式书写专项/化学动力学/化学平衡/溶液与相图/热力学初步/晶体学与晶体结构/配位化合物基础。**改源后必须单独跑 `--path <md> --word-clean`**。
- `NORMALIZE_SIMPLE_INLINE_SCRIPTS = False`（commit `6267e2b68`）：曾把 `$MT^{-2}$` 降级成 Unicode 文本 → 不是 OMML。
- 排版污染已四轮清零（活跃 81 份：A 类 LaTeX 源码态 0 / B 类花括号上标泄漏 0，OMML ≈7.8k，图片 665 引用 0 缺失）。
  - **最痛教训：连续 3 轮都「以为修完」，下一轮换维度复检又冒出几十处。收官前必须换维度再查一轮**（只查 A/B 两类必漏）。
  - pandoc 限制：不支持 `\ce{}`（须预处理成 LaTeX）；**math 内禁 `\textbf`**（被截成 `\textb`+`f{}`，整个 `cases` 不转）；定界符内侧空格不识别为数学；不支持 `\displaylines`。
  - **oMath 口径勿混**：82,978 = 全库含 `_archive`；≈7.8k = 活跃 81 份。
  - 导出报 WinError 5（docx 被 Word 占用）→ 重试即可；剥离 tmp 后缀正则须写 `\.d+-d+\.tmp(?=\.docx$)`。
  - 技能 `docx-math-leak-qa` 固化全流程；单测 `test_ce_conversion.py`（**`scripts/` 被 .gitignore，须 `git add -f`**）。
- 遗留：学生版 docx 2 处 mismatch（11-反应机理与推断、3-烷烯炔）待排查。

## 五、学生讲义 / 13-教案 / 数学工具
- 源 `04-课件/学生讲义/` 按模块分目录，产物 `06-学生侧材料/讲义/<同名子目录>/`。**讲义不分教师/学生版**，正文含练习+答案，教师信息放 HTML 注释。**导出扫描口径**：递归 `*.md`，排除 `_归档` 与 `_` 开头目录、stem 为 `README`、前缀 `讲义升级模式-`，并**只保留 stem 含 `超级充实`/`基础版`/`复习`/`-新课` 者**。
- 数学工具区（commit `8668785f6`/`839794043`）：8 个分讲文件 + 导言 README（README 前缀→不进统计、不导出）。**铁律：行内数学一律裸 `$...$`，禁反引号包裹**（反引号→code span→Obsidian 不渲染、pandoc 不转 OMML，导出后 `<m:oMath` 为 0）；表格内绝对值写 `\lvert x\rvert`；文件级 `$` 数须偶。数学条目用 `type: 工具卡` 放 `03-知识点/数学工具/`（不进知识点 README 统计，须手写补一行）。教材：Mortimer 中译主线 + Atkins 打底 + McQuarrie 中译（`Mathematics for Physical Chemistry/` 留 vault 根目录不归位）。
- 13-教案（人教版必修一）52 md + 45 docx + 18 张 Mermaid 概念图（`.mmd` 源）：核心素养统领、含逐字稿、三层作业、一课时一 md。C14005 内嵌图 docx 腾讯预览打不开＝预览器缺陷，**勿反复重出**。
- 断链修复 `fix_moved_links.py`：先判真实失效再按文件名归位，**禁先 `Path(stem).stem` 剥子目录**。

## 六、mineru OCR 公式字符拆分（P0，已收官）
- 两形态：①相邻数字被空格拆 `3 8 7. 8`；②小数点被空格包围（**行内也中招**，只查块级会严重低估）。规则：`(?<![\d.])\d(?: \d)+`→去空格；`(\d)\s*\.\s+(\d)`→`\1.\2`。
- **安全策略 7 条（复用必读）**：①只在公式内（行内禁跨行）②文件级 `$` 数须偶 ③区间级跳过（含裸中文／含空行但无 `\begin{`／长且无 LaTeX 命令）④`\text|\mathrm|\ce` 内容保护 ⑤位数防护（整数 ≥8 位、或 ≥6 位纯 0/1 且无小数点→不合并）⑥行数守恒 ⑦红区/归档/未跟踪/20 分钟内改动不碰。
- 踩坑：①手写花括号匹配在 `\ce{...\ce{...}}` 嵌套上算错闭合（破坏性）→ 回退简单正则保守跳过；②「文件级」判据误杀（中文合法存在于 `\mathrm{静电键强度}`）→ 下沉区间级。
- **关键教训：SCAN 是硬编码白名单**，根目录散装教材（无机化学习题集/结构化学习题与解析/clayden/中级无机化学/人教版初中）从未进范围，漏约 1.4 万处 → 白名单式扫描要定期对照根目录 `ls` 复核。普查报告会被脚本整体重写 → 手写内容另落文件。
- 遗留：`$` 奇数 13 文件/30 处（OCR 把 `$` 与 `()` 互识，自动补必错，清单 `09-审计报告/OCR符号误识人工修复清单-2026-09-11.md`）；**字母拆分仅普查未修**（916 文件）。工具在 `.workbuddy/tmp/`：`audit_ocr_split_v2.py`、`fix_ocr_split_gray{,2,3}.py`、`verify_gray2.py`、`audit_letter_split.py`。

## 七、题库线与历史快照
- 题库 5,369 题；KP 挂载率 100%；利用率 10.2%（09-06 收官已 push）。坑：git 对象库损坏 → `fetch --refetch` + read-tree 恢复（**盲用错误信息的哈希会致坏 commit**）；group 捕获组改动须同步取值列。
- 待办：34决理-2-6-1 / 平衡题25 原书复核（待外部材料）；d2~d3 基础题待随堂化。
- 09-07 题目利用收官：专项卷 24 卷 600 题 + 随堂卷 11 卷 235 题。09-08 取证：7,076 删除＝未引用 OCR 孤儿图（**不提交不恢复，待清理方自行 commit**）。`6caedd1b1`（红区治理）本地待推。
- 30 天以上日志按主题并入本文件后再删除；明细见同目录 `YYYY-MM-DD.md`。
