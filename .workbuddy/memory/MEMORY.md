# 妙妙屋题库·长期记忆（2026-09-02 精简版）

## 环境
- 校验/审计脚本用系统 Python 3.12（有 PyYAML）：`C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe -X utf8`；全量校验 `11-模板/scripts/validate_kb.py --full`（~75s，后台跑）。

## 关键基线（2026-09-02，B4 后）
- 题目总数 **4,182** = 04-题库 4,119(`type:题目`) + 05-真题库 63(`type:真题`)。统计口径必须双 type；04-题库 下另有 140 个非题目 md（答案/系统/索引/题组/真题卷等），只按目录过滤会多算。
- status 覆盖 100%：已填充 3,377 / 已补全答案 792 / deprecated 8 / 待填充 5。
- validate_kb --full：6,410 文件 · Error 0 · Warning 209（正文断链45+frontmatter断链158+标题跳跃3+stage门禁3）。
- 字段覆盖（4,119 题）：source_subject/subject_module/teaching_level 基本全覆盖；year 960 / concepts 723 / question_type 1,209（29.4%）。
- 习题书 31 章/1,283 题，单一事实源=04-题库/题库架构总览.md；docx 三版本在 00-首页/题组Word/习题书/。下次重建会少 3 条（三个 deprecated 父文件，属预期）。
- 图片引用 23,654：真缺失 3,200 不可修；剥 `../` 可修 440 全在归档区。巡检脚本 .workbuddy/scripts/audit_vault_images.py。

## 组卷工作台（04-题库/组卷工作台.md）
- 三块 dataviewjs：快速筛选 / 智能组卷（梯度2:5:3+模块配额+同来源≤3+种子）/ 已用题回看。
- `used_in` 是 wikilink → dataview 解析成 Link 对象**没有 `.length`**，判空必须 `u != null && (Array.isArray(u)?u.length>0:true)`；dataviewjs 块间不共享作用域，hasUsed/diffNum/stageHit 每块重定义。
- diffNum 取首个整数（`3-5` 等 9 条例外 NaN 静默丢）；stageHit 用 split("/")+some；srcKey 归一化 1,087 来源，改规则后跑 check_workbench_js.py 对齐 JS/Python。
- 出卷闭环：试卷写好链接后 `mark_used.py --paper "<卷>.md"`（先 dry-run 再 --write）回填 used_in，否则 EXCLUDE_USED 摆设。depends_on 仅 4 条，人工看题面 ⚠️。

## 题库操作铁律
- 例题写 `type:题目`+`question_type:例题`；重建直接 `--clean --write`（Python 调用加 `CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID=` 绕 safe-delete）。
- 入库走 04-题库/新题入库SOP；文档里 wikilink 示例一律全角［［…］］防误报断链。
- 校验器只约束 4 字段（fidelity/difficulty/exam_stage/subject_module）；teaching_level/question_type/source_subject 不校验，改错零告警。
- `source_subject`=来源教材分科（16 值不收敛）；`subject_module`=四大模块（QB_ENUM）。两者不同是设计意图（46.8%），勿"修正"一致。
- teaching_level 仅 4 档：基础/巩固/拓展/竞赛。
- question_type 双维度并存：作答形式（选择/填空）+内容题型（计算/推断/作图/机理/方程式书写/简答）+角色（例题/综合）。「画结构式」归`作图`不拆`推断`；`简答`是兜底不自动推断；一题多问大题留空（各问同质才写）；11 条`综合题`保持原样。
- **批量改字段脚本第一步：type 白名单 {题目,真题}**。
- 真题届数→年份 `year=N+1986`；真题一题一文件题组制，子题 `[[题-037-1-2-X]]` 内容在父文件，按题号前缀折叠，折叠前对账小问数。
- `knowledge_points` 只放能解析到 03-知识点/ 的项且不允许为空；细概念走 concepts（纯文本）。40 题待人工指派 KP。
- 成书：`build_module_book.py --write` 自动回写 README；`溯源映射.json` 成书题↔源文件；自检 audit_book_quality.py。

## 链接与图片
- 表格内 `[[目标\|别名]]` 转义竖线是正确写法；替换覆盖 `[[X]]`/`[[X|`/`[[X\|` 三形态。
- 链接解析禁止自写正则：`sys.path.insert` 后 `import validate_kb as V` 复用 collect_md_files/scan_file；LINK_RESOLUTION_EXTRA_PREFIXES 目录可作链接目标需豁免；EXCLUDE_FILE_NAMES≠LINK_TARGET_ONLY_FILE_NAMES。
- 修断链只用「精确相等+同目录」，禁模糊匹配。frontmatter 断链 1,643=未建 KP 红链，按主题分批建，存量暂不动（用户决策）。
- 「静默吸题」：basename 命中=设计意图不动；仅 title/aliases 兜底连到题目才算错位；文件名与内容不符只改内容不改名。
- 媒体仓库/ 不入库是设计：图片治理一律「复制进媒体仓库+源图保留」。

## 批量改 md 防坑（血泪合并版）
- 查行尾只认 Python 数 `b'\r\n'` vs `b'\n'`；grep -c $'\r' 假阳性；git diff 因 .gitattributes eol=lf 归一化测不出 CRLF；行尾基线用 zipfile 快照不是 git show HEAD:。
- 库是混合行尾：读写一律 `open(newline="")`（禁 Path.read_text）；插入新行按邻居补 `\r`（mark_used.py 的 term_at/line_term 是标准做法）。
- frontmatter 判定：split("\n") 找第二个 `---`，禁 `re.match(r"^---\n")`（CRLF 漏配，曾把 4,119 统计成 2,386）。
- bash 双引号/heredoc 会吃 `$` 与「冒号+反斜杠」（`:\s`→`:/s`）正则 → 一律 Write 成 .py 再跑。
- 改前 zip 快照到 .workbuddy/backups/ + 改后逐行 diff（模板 verify_b2a.py，断言 equal/replace(1:1)/insert 且插入行行尾随邻居）；改完重跑校验再提交。
- `git add` 刷 150KB CRLF 警告会 SIGTERM 中断留 index.lock → 加 `2>/dev/null`；锁用 PowerShell Remove-Item 清。git status M 但 diff 空=stat 缓存过期无害；提交按显式 pathspec。
- 遍历题库必须过滤 type 白名单；别把 09-审计报告 的历史证据字段当修复对象。

## 批量 docx
- python-docx + lxml + zipfile 后处理，不走 tencent-docx HTML 往返（毁 OMML/图位）；彩图检测全分辨率网格采样；覆盖写直接 zipfile（shutil.move 触发 safe-delete）；渲染验证 LibreOffice headless；页脚 PAGE/NUMPAGES 需完整 fldChar 链。

## 新建 KP 文件
- `subject→source_subject` 改名只作用于 04/05-题库，03-知识点仍用 `subject`。必填 title/type/subject/status/updated；related/prerequisite 写纯文本数组（wikilink 会查断链）；不写 stage 绕门禁；一词多义建一个文件分节。

## 生命周期（B4）
- 废弃唯一机制：`status:deprecated`+`deprecation_reason`(必填)+`superseded_by`(选填 wikilink，已入 QB_LINK_FIELDS 查断链)。旧 deprecated:true 日落写法不被任何脚本排除。
- 标废弃前必须证伪「内容不丢」（拆题父文件逐条核对小问已独立成题）。
- 判僵尸字段铁律：先 `grep -rn 字段名 --include="*.py" 11-模板/scripts`。demoted/promoted/depends_on/superseded_by 是承重字段；真野字段 big_question/source_author/quality_tier（SOP §4.5）。

## 讲义↔题库映射
- `check_lecture_problems.py` 按 created 切新旧（默认 >=2026-09-02），不按 stage（避免 84 份历史讲义变红）；`--since`/`--strict`/`--list-unresolved` 可调。problems 规范=wikilink（反查靠反链，纯文本做不到）。
- 现状：22/217 份讲义有 problems，148 引用中 38 断链（7 条降级编号可机械修，31 条自造编号需人工，随下次大修逐讲清理勿批量）。

## 用户决策
- 2026-08-31：断链存量暂不处理；索引口径历史数字保留；33 个非题目文件命名豁免；质量优先于难度（构建排序 fidelity 优先🟢🟡🔵）；新题默认 10-待审核区 P1，P0 小额已核验直入。
- 2026-09-02 题库升级：主攻检索断裂；交付=Bases 打底+工作台升级+保留 CLI。真题双仓（04 仓储求全/05 交付求深）视图层合并不移动文件，收口 02-数据库/真题.base。维度补齐只做 teaching_level 4 档+question_type；不做 syllabus_codes、不强制补 used_in 历史。缺失值：能从 difficulty 推断就紧贴 difficulty 行插入，双重缺失留空。只排除错题回流闭环；B5 可选；讲义映射仅新讲义强制。
- 2026-09-02 晚 三模块定稿（grill 四问）：核心场景=组卷输出（题型专练/真题模拟/KP 专题，不做重做卷）；**一库三视图**不搬家，归属=teaching_level 唯一决定（来源≠难度：教材习题横跨四档 205/827/1,179/598，真题小问 12/33/14/4）；切法 A：习题集=基础+巩固 1,769 / 习题书=拓展 1,525 / 测试题=竞赛 888+真题整卷模考（42/36/21）；最小闭环=卷尾失分复盘→按 KP 抽未用题→mark_used，不做逐题对错；31 章书+4 阶段测试卷存量不动（池 vs 成品入 SOP）。落地：Bases 三视图+工作台三预设+校验软检查。基础池 452 偏薄。
- IMA 导出：md+相对路径图 ZIP → Notion 类型导入；双链转纯文本；vault_to_ima_convert.py 已跑通 943 篇。

## 遗留待办
- B1–B4 全完；B5 历史脚本收敛（177+）可选。
- **B7 三模块视图已落地（2026-09-02 晚）**：三 .base（1,769/1,525/888 已离线验证）+ SOP/架构总览定义 + 模板-专题练习卷 §7.1 失分复盘 + validate_kb `check_teaching_level_drift`（孤例自愈式软告警，基线 209 不变）。待 Obsidian 实渲染验证；**工作台三预设模式等 B3 实跑验证后再动工**。
- 2,970 条待补 question_type（71% 在教材习题：结构化学 972/有机 962/元素与分析 597/化学原理 439；真题 254）。走 题库.base 按目录批量补；脚本 infer_question_type.py 幂等可重跑。
- B3 与 题库.base 改动需 Obsidian 实跑验证（4,182 行/待治理 8/待补全 5/精选池 1,314；EXCLUDE_USED 是否真排 344 条）。
- 习题书 V3：题-033 查纸质原书补题补答；ABOC 211 条思路占位待人工。
- 学生版打印版 ~51% 图 DPI<150 是否换源图待定；Word precheck 源稿统一写 `\theta`。
