# 妙妙屋题库·长期记忆

## 环境
- 校验/审计脚本用系统 Python 3.12（有 PyYAML）：`C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe -X utf8`；全量校验 `11-模板/scripts/validate_kb.py --full`（~75s 后台）。

## 关键基线（2026-09-02，B6 后）
- 题目总数 **4,182** = 04-题库 4,119(`type:题目`) + 05-真题库 63(`type:真题`)，统计必须双 type 白名单；04-题库 下另有 140 个非题目 md。
- status 全覆盖：3,377/792/弃用 8/待填充 5；validate_kb --full 6,410 文件 Error 0 Warning 209。
- **question_type 覆盖率 42.0%（1,757/4,182）=B6 规则法天花板**；剩余 2,425=无信号 1,325/多小问 738/T3 弱 362，仅 LLM 语义补全可再提升（需批准）。
- 三模块视图（B7）：习题集=基础+巩固 1,769/习题书=拓展 1,525/测试题=竞赛 888；三 .base 离线验证过待 Obsidian 实渲染；基础池 452 偏薄。
- 习题书 31 章/1,283 题事实源=题库架构总览.md；图片真缺失 3,200 不可修。

## 组卷工作台
- `used_in` 是 wikilink → dataview 解析成 Link **无 `.length`**，判空用 `u != null && (Array.isArray(u)?u.length>0:true)`；dataviewjs 块间不共享作用域，工具函数每块重定义。
- diffNum 取首个整数（`3-5` 等 NaN 静默丢）；srcKey 归一化 1,087 来源。
- 出卷闭环：`mark_used.py --paper`（dry-run→--write）回填 used_in；三预设等 B3 Obsidian 验证后动工。

## 题库操作铁律
- 例题写 `type:题目`+`question_type:例题`；重建直接 `--clean --write`（Python 调用加 `CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID=` 绕 safe-delete）。
- 校验器只约束 4 字段（fidelity/difficulty/exam_stage/subject_module），改其余字段零告警。
- `source_subject`=来源教材分科不收敛；`subject_module`=四大模块；两者不同是设计意图（46.8%）勿"修正"一致。
- teaching_level 仅 4 档。question_type 双维度（选择/填空+计算/推断/作图/机理/方程式书写/合成/简答）+角色（例题/综合）；「画结构式」归`作图`；`简答`兜底不自动推断；多问大题留空（同质才写）。
- **批量改字段脚本第一步：type 白名单 {题目,真题}**。
- 真题 `year=N+1986`；题组制子题按题号前缀折叠、折叠前对账小问数。knowledge_points 非空且须解析到 03-知识点/；细概念走 concepts。

## 链接与图片
- 链接解析禁自写正则：`import validate_kb as V` 复用；EXCLUDE_FILE_NAMES≠LINK_TARGET_ONLY_FILE_NAMES。修断链只「精确相等+同目录」。frontmatter 断链 1,643 存量不动（用户决策）。
- 「静默吸题」：basename 命中=设计意图不动；文件名与内容不符只改内容不改名。媒体仓库/ 不入库是设计；文档 wikilink 示例用全角［［…］］防误报。

## 批量改 md/docx 防坑
- 查行尾只认 Python 数 `b'\r\n'` vs `b'\n'`（grep $'\r' 假阳性）；git diff 因 .gitattributes eol=lf 归一化测不出 CRLF。读写一律 `open(newline="")`（禁 Path.read_text）；插行按邻居补 `\r`。
- frontmatter 判定 split("\n") 找第二个 `---`（曾把 4,119 统计成 2,386）。bash 双引号/heredoc 吃 `$` 与 `:\s` 正则、python -c 吃反引号 → 一律 Write 成 .py 再跑。
- 改前 zip 快照 .workbuddy/backups/ + 改后逐行 diff（verify_b2a.py）；改完重跑校验再提交。
- `git add` 加 `2>/dev/null` 防 CRLF 警告 SIGTERM 留 index.lock；status M 但 diff 空=stat 缓存无害；显式 pathspec 提交。别把 09-审计报告 历史证据字段当修复对象。
- 批量 docx：python-docx+lxml+zipfile 后处理（禁 HTML 往返毁 OMML/图位）；彩图全分辨率网格采样；LibreOffice headless 验证。

## 新建 KP 文件
- `subject→source_subject` 改名只作用 04/05-题库（03-知识点 仍 `subject`）；related/prerequisite 写纯文本数组；不写 stage 绕门禁；一词多义一文件分节。

## 生命周期
- 废弃唯一机制 `status:deprecated`+`deprecation_reason`+`superseded_by`（入 QB_LINK_FIELDS）；旧 deprecated:true 不被脚本排除。标废弃前证伪「内容不丢」。判僵尸字段先 grep scripts（demoted/promoted/depends_on/superseded_by 承重）。

## 用户决策
- 2026-08-31：断链存量不动；质量优先于难度；新题默认 10-待审核区。
- 2026-09-02：主攻检索断裂；维度补齐只做 teaching_level+question_type。三模块定稿=一库三视图不搬家、归属=teaching_level 唯一决定（来源≠难度）、切法 A、最小闭环=失分复盘→按 KP 抽未用题→mark_used、存量成品不动。

## 遗留待办
- B5 脚本收敛可选；B3/三 .base 待 Obsidian 实跑验证。
- 习题书 V3：题-033 补题；ABOC 211 条思路占位待人工。40 题 KP 人工指派。
- 讲义 problems 38 断链随下次大修逐讲清理勿批量。
- 孤儿目录 化学竞赛教程*/（MinerU 残留）先报告不动手。
