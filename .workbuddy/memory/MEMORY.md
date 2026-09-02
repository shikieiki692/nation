# 项目长期记忆（妙妙屋化学竞赛知识库）

## 环境与运行（硬性）
- `11-模板/scripts/` 校验/审计脚本必须用系统 Python 3.12：`C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe`（有 PyYAML）；managed 3.13.12 无 PyYAML。
- 跑校验器：`...Python312\python.exe -X utf8 11-模板/scripts/validate_kb.py --full`（约 75 秒，后台跑）。

## 关键基线（2026-09-02 实测，B2b 后）
- 题目总数 **4,134** = 04-题库 4,071（type=题目）+ 05-真题库 63（type=真题，非"题目"）。两仓 md 文件数：04-题库 4,260 / 05-真题库 64。
- validate_kb --full：6,410 文件 · **Error 0 · Warning 209**（正文断链 45 + frontmatter 断链 158 + 标题跳跃 3 + stage 门禁 3）。基线 1,641 → 209 由 B1（拆 KP 两级）+ B2a 达成，B2b 后持平。
- 字段覆盖（4,119 题文件口径）：source_subject 4,184 / subject_module 4,186 / teaching_level 4 档共 4,226 / year 960 / concepts 723 / **question_type 1,209（29.4%）**，仍缺 2,970。
- 习题书 **31 章 / 1,283 题**，单一事实源 = 04-题库/题库架构总览.md；docx 三版本在 `00-首页/题组Word/习题书/`。
- 全库图片引用 23,654：真缺失 3,200 属资产丢失脚本不可修；剥 `../` 可修 440 全在归档目录；统计"可修"必须先排除根兜底命中 1,092。巡检脚本 `.workbuddy/scripts/audit_vault_images.py` + `gen_vault_img_report.py`。

## 组卷工作台（04-题库/组卷工作台.md，B3 后）
- 三块 dataviewjs：快速筛选器 / 智能组卷器（梯度 2:5:3 + 模块配额 + 同来源限流 ≤3 + 可复现种子）/ 已用题回看。
- **`used_in` 是 wikilink**（`used_in: "[[结构化学阶段测试卷]]"`，344 条全指向 4 份阶段测试卷且文件存在）。
  → dataview 解析成 **Link 对象，没有 `.length`**；写 `p.used_in.length` 判空会**恒为假、静默失效**。
  一律用 `hasUsed = u => u != null && (Array.isArray(u) ? u.length > 0 : true)`。
- **dataviewjs 代码块之间不共享作用域**，三个工具函数（`hasUsed` / `diffNum` / `stageHit`）每块都要单独定义一遍。
- `diffNum()` 取第一个整数：9 条例外写法（`3-5`/`4-5`/`3 # 1-5`）用 `Number()` 得 NaN 会被静默丢弃。
- `stageHit()` 用 split("/")+some：`exam_stage` 有 `/` 多值。
- 来源归一化 `srcKey()`：1,228 → 1,087 个来源（化学竞赛初赛讲义 496 / 赵鑫光 482 / 普通化学原理 306 / 周公度 285）。
  不归一化「同来源限流 ≤3」形同虚设。改规则后用 `check_workbench_js.py` 比对 JS 版与 Python 版是否仍逐条一致。
- **出卷闭环**：试卷写好题目链接后跑 `mark_used.py --paper "<试卷>.md"`（默认 dry-run，确认后 `--write`），
  否则 `EXCLUDE_USED` 是摆设。它按 wikilink 回填，单值写标量、多值写数组。
- `depends_on` 全库仅 4 条，承接题无法自动处理，只能人工看题面顶部 ⚠️ 提示。

## 题库操作铁律
- 例题写 `type: 题目` + `question_type: 例题`（`type: 例题` 不被构建 gather 识别）。
- 重建直接 `--clean --write`（已内置文件锁重试），勿先 rm；Python 调用加 `CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID=` 绕 safe-delete shim + `-X utf8`。
- 导入新题一律走 04-题库/新题入库SOP；文档里写语法示例用全角方括号防误报断链。
- 汇智源编号 = 题库编号；答案只有图的题不要编造文字答案。
- 六字段枚举仅限题目类文件（QB_TYPES）；difficulty 允许区间、exam_stage 允许 `/` 多值。
- **校验器只约束 4 个字段**（QB_ENUM：fidelity/difficulty/exam_stage/subject_module）；teaching_level、question_type、source_subject **完全不校验** → 改它们零告警风险，但规范只能靠 SOP，改错也无人拦。
- **字段分工（2026-09-02 定，勿再混淆）**：`source_subject` = 来源教材自己怎么分科（16 值，不收敛、不校验）；`subject_module` = 四大模块（QB_ENUM 约束，组卷与成书用它筛选）。**两者值不同是设计意图**（1,906 处，46.8%），切勿"修正"成一致。
- `teaching_level` 只有 4 档：**基础 / 巩固 / 拓展 / 竞赛**（2026-09-02 由 14 种收敛）。长尾落点依据：`拔高/提高/进阶/决赛/高级` 100% 落在真题目录→竞赛；`强化/挑战` 全在教材习题→拓展。
- **`question_type` 是两个维度并存**（2026-09-02 定）：作答形式 `选择`/`填空` + 内容题型 `计算`/`推断`/`作图`/`机理`/`方程式书写`/`简答`，另有角色值 `例题`/`综合`。求 pH 的选择题 → `[选择, 计算]`。
  - **「画出 A 的结构式/构型」统称 `作图`**，不拆给 `推断`（作图档 164 条里 114 条画结构、10 条画装置图/相图，拆开会让"作图"失去意义）。
  - **`简答` 是兜底值不参与自动推断**——它是"没识别出题型"的委婉说法（T3 档 542 条只统计不写）。
  - **一题多问的大题留空**（701 条），宁可留空也不要只写第一问的题型。例外：各小问同质（如三问全是计算）才写（25 条）。
- **批量改字段的脚本第一件事是加 type 白名单**：`{题目, 真题}`。04-题库 下混着 140 个非题目文件（索引 55 / 系统 33 / 答案 19 / 题组 7 / 真题卷 5 / 真题答案 5 / 图片索引、题库工具等），漏了这道闸会把字段写进它们（B2b 误写 19 个，已回滚）。
- 真题届数 → 年份：**`year = N + 1986`**（第27届=2013 … 第39届=2025；11 组配对 + 全量 356 条反查均 0 冲突）。
- `knowledge_points` 只放能解析到 `03-知识点/` 的项，**不允许为空**；更细的概念走 `concepts`（纯文本，不校验断链）。
- 真题「一题一文件」题组制：一个大题=一个 md，文件名取首问描述 → `[[题-037-1-2-X]]` 内容在 `题-037-1-*` 父文件里，**按题号前缀折叠**（描述不同是常态），折叠前对账小问数。
- 构建防漂移：`build_module_book.py --write` 自动回写 README；`溯源映射.json` 成书题↔源文件；自检跑 `audit_book_quality.py`。

## 链接与图片治理
- 表格内 wikilink `[[目标\|别名]]`（转义竖线）是**正确写法**（505 处），只换目标名、转义竖线原样保留，替换覆盖 `[[X]]`/`[[X|`/`[[X\|` 三种形式。
- validate_kb：`LINK_RESOLUTION_EXTRA_PREFIXES` 目录 = 不扫描内容但**可作链接目标**，新解析函数必须豁免这些前缀；`EXCLUDE_FILE_NAMES`（不校验 schema）≠ `LINK_TARGET_ONLY_FILE_NAMES`（仍是合法目标）。**禁止自写正则重写链接解析**——`sys.path.insert` 后 `import validate_kb as V` 复用 collect_md_files/scan_file。
- 修断链只用「精确相等 + 同目录」，禁模糊匹配（题号近似会误叠）。
- 断链-frontmatter 1,643 处 = KP 未创建真红链、极端长尾，按主题分批建，勿批量新建；存量暂不处理（用户决策）。
- 「静默吸题」：`find_wikilink_target()` 三级兜底（路径→basename→title/aliases），只有靠 title/aliases 兜底连到题目文件的才是错位（basename 命中 = 显式指题设计意图，不动）；文件名与内容不符（如 Aldol缩合.md 实为逆羟醛缩合）只能改内容不能改名。巡检脚本 `find_kp_links_to_questions.py` 等。
- `媒体仓库/` 被 .gitignore 不入库，来源仓（`06-外部资料导入/**_images` 等）反而入库 → 图片治理一律「复制进媒体仓库 + 源图保留」；12,413 basename 两仓共存是标准做法非异常。
- 批量改 md 前用 zipfile 打快照到 `.workbuddy/backups/`。

## 行尾与 shell 防坑（2026-09-02 补）
- **查行尾只能用 Python 数 `b.count(b'\r\n')` vs `b.count(b'\n')`**。`grep -c $'\r' file` 在 Git Bash 下是**假阳性**（把纯 LF 文件报成"全行含 CR"）。
- `git diff --stat` **证明不了行尾**：`.gitattributes` 有 `*.md text eol=lf`，diff 会归一化 CRLF。要验行尾必须读磁盘字节。
- 题库是**真混合行尾**：04-题库+05-真题库 里 1,326 个全 CRLF + 2,557 个全 LF。插入新行必须按邻居风格补 `\r`（`mark_used.py` 的 `term_at()` / `line_term()` 是标准做法）。
- **bash 双引号里 inline `python -c` 写含 `$` 的正则会被转义搞坏**：`r"^type:\s*(.+?)\s*$"` 直接失配（统计结果全变"无 type"且无报错）。含 `$` 或「冒号+反斜杠」的正则一律写成 .py 文件再跑。

## 批量改 md 防坑
- frontmatter 判定：首行 `---` 且头部含 `^[\w\-]+:`；自动补别名取路径末段；别把 `09-审计报告/` 报告的历史证据字段当修复对象。
- **行尾检测（2026-09-02 重要修正）**：本库 `.gitattributes` 有 `*.md text eol=lf`，**git 在 diff/add 时会做 CRLF 归一化**——旧的「`git diff --stat` vs `--ignore-cr-at-eol --stat` 对比」在本库**根本测不出 CRLF 污染**。改用：改前 zip 快照 + 改后逐行 diff（模板 `.workbuddy/scripts/verify_b2a.py`），断言 diff 只含 equal / replace(1:1) / insert 三种操作，且插入行行尾与邻居一致。
- 读写一律 `newline=""`，且**必须用 `open()`**——`Path.read_text()` 不接受该参数，其默认 `newline=None` 会折叠 CRLF→LF，检测行尾时正好毁掉要测的东西。
- 本库是**混合行尾**（抽样 4,189 文件含 134,919 个 CRLF）：`split("\n")` 后 `\r` 留在行尾 —— 原地改值安全（`\r` 落在正则 `\s*$` 里），但**插入新行必须按邻居风格补 `\r`**，否则在 CRLF 文件里插进裸 LF 行。
- **bash heredoc 会吃掉紧跟冒号的反斜杠**：`:\s` → `:/s`，正则静默失效（`\s` 前是中文/括号/行首则无事）。含「冒号+反斜杠」的正则一律用 Write 写成 .py 文件，不走 heredoc。
- **`git add` 会刷 ~150KB CRLF 警告**（归一化所致），不 `2>/dev/null` 会被 SIGTERM 打断并留下 `.git/index.lock` 空文件，之后所有 git 命令报 exit=128；用 PowerShell `Remove-Item` 清锁。
- **改完文档要重跑校验再提交**：B1 在 题库架构总览.md 写了 `[[wikilink]]` 示例被当真实链接（Warning 209→210），B2a 才发现并改全角修回。文档里的语法示例一律全角 `［［…］］`。
- git status 报 `M` 但 `git diff` 为空 = stat 缓存过期（内容字节相同），无害；提交时按显式 pathspec 暂存以避开无关目录。
- **找 frontmatter 不能用 `re.match(r"^---\n", t)`**：本库有 CRLF 文件，字面 `\n` 匹配不上，会静默漏掉半壁江山（B2b 曾把 4,119 题统计成 2,386）。一律 `split("\n")` 后找第二个 `---`。（继 git diff 之后，第二次栽在"行尾影响匹配"上。）
- **遍历题库目录必须过滤 type**：`04-题库` 下 140 个文件是索引/系统/答案/题组/真题卷/图片索引，不是题目。白名单 `{题目, 真题}`。

## 批量 docx 经验
- 走 python-docx + lxml + zipfile 后处理，**不走** tencent-docx HTML 往返（毁 OMML 公式与图位）。
- 彩图检测用全分辨率网格采样（resize 会漏检小面积彩色）；覆盖写直接 `zipfile.ZipFile(path,'w')`（shutil.move 触发 safe-delete 批删拦截）。
- XML 颜色归一化：注意自闭合 `/>` 与非闭合两种形态都要匹配。
- 渲染验证用 LibreOffice headless `--convert-to pdf` 兜底（Word COM 沙箱下报错）。
- 页脚 PAGE/NUMPAGES 需完整 fldChar begin→instrText→separate→占位文本→end。

## 新建知识点文件字段安全写法
- 注意：2026-09-02 的 `subject → source_subject` 改名**只作用于 04-题库 / 05-真题库**，03-知识点 仍用 `subject`。
- 必填 title/type/subject/status/updated；`subject_module` 才有枚举（subject/module 没有）；`related`/`prerequisite` 写纯文本数组（在 QB_LINK_FIELDS 里，写 wikilink 会被查断链）；不写 `stage` 字段绕 published 门禁；一词多义建一个文件内部分节，勿拆重名。

## 用户决策（2026-08-31）
- 断链类存量暂不处理；索引口径历史数字保留原值；33 个非题目文件命名豁免。
- 质量优先于难度：不做难度分级，构建排序 fidelity 优先（🟢逐字>🟡改写>🔵自编）。
- 新题分层入库：默认 10-待审核区 P1 流程，P0 小额已核验直入。

## 用户决策（2026-09-02 题库升级）
- 主攻检索断裂；交付形态 = Bases 打底 + 工作台升级 + 保留 CLI。
- 真题双仓（04-题库/真题=仓储层求全，05-真题库=交付层求深）**视图层合并，不移动文件**；真题统一收口到 `02-数据库/真题.base`。
- 维度补齐只做 `teaching_level` 收敛 4 档 + `question_type`；不做 syllabus_codes、不强制补 used_in 历史。
- 缺失值处置：能从 difficulty 推断就推断并紧贴 difficulty 行插入；**双重缺失（difficulty 也缺）不推断，留空**——与 B1「40 题 KP 不硬造」同一哲学。
- 只排除错题回流闭环；B5 历史脚本收敛降为可选。讲义映射仅新讲义强制，历史按需。

## IMA / 资料库导出
- IMA：md+相对路径图打 ZIP → 笔记模块 Notion 类型导入 → 关联知识库；双链转纯文本勿转 md 链接；批量 20~50/次。
- `vault_to_ima_convert.py` 已跑通 03-知识点 → 943 篇 → `C:\Obsidion\导出_IMA\03-知识点.zip`（图解析 99.9%）。

## 遗留待办
- **B3 已完（提交 97709278）**；剩下 B4 生命周期（pack 准入 / status 收敛 / 僵尸字段豁免 / 新讲义强制 `problems`）、B5 可选。
- **B3 待用户在 Obsidian 实跑验证**：三块 dataviewjs 的实际渲染（命令行只验了 JS 语法与 `srcKey` 跨语言一致性）；
  重点看 `EXCLUDE_USED` 是否真把 344 条已用题排掉、智能组卷器的分档诊断有没有出现「候选不足」。
- **2,970 条待补 question_type**：71% 在 `04-题库/教材习题`（结构化学 972 / 有机 962 / 元素与分析 597 / 化学原理 439），真题 254。走 `题库.base` → 「题型待标注（按目录批量补）」，按 `所在目录` 排序后同目录批量标。脚本 `.workbuddy/scripts/infer_question_type.py` 幂等可重跑。
- **需在 Obsidian 里人工验证**：两个 base 的 `or` 嵌套 `and` 双仓 filter 是否真的同时拉到 04-题库/真题 与 05-真题库；新增的 `file.folder` 属性与「题型待标注·真题优先」视图（命令行无法验证 Bases 渲染）。
- 40 题 knowledge_points 全部解析不出，需人工指派（清单 `.workbuddy/backups/kp_empty_list_files.txt`）。
- 11 条 `question_type: 综合题` 无法拆分成原子题型，保持原样（上海中学 8 条 + 28 届决赛 2 条 + 1 条）。
- B3 组卷器升级（`组卷工作台.md` 加 EXCLUDE_USED/配额/难度梯度/随机种子；注：组内「文末写 question_type 字段目前仅 7% 覆盖」已过时，应改 29.4%）／B4 生命周期与讲义映射／B5 历史脚本收敛（177+，可选）。
- 习题书 V3：题-033 查纸质原书补题补答；ABOC 211 条思路占位待人工。
- Word precheck 少量 `^\circ`/裸下标 warning，源稿后续统一写 `\theta`。
- 学生版-打印版 ~51% 图有效 DPI<150（源 72 DPI），是否回溯换源图待用户定。
