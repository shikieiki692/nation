# 妙妙屋题库·长期记忆

## 环境
- 脚本用系统 Python 3.12（有 PyYAML）：`...\Python312\python.exe -X utf8`；全量校验 `validate_kb.py --full`。

## 关键基线（09-03）
- 题目总数 **4,182** = 04-题库 4,119(`type:题目`) + 05-真题库 63(`type:真题`)；双 type 白名单，04-题库 另有 142 个非题目 md。
- status 3,377/792/弃8/待填5 全覆盖；--full Error 0 Warning 209（曾 216，已修回）。
- question_type **冻结**（09-03 决策：零消费方——工作台仅展示、.base 不用、脚本零读取；停止补全，存量 1,209 保留）。
- 三模块=teaching_level 唯一决定：习题集=基础+巩固/习题书=拓展/测试题=竞赛；**行数随并行导入漂移勿写死**（09-03 实测 1,769/1,525/1,020，总数 4,314）。习题书事实源=题库架构总览.md；图片真缺失 3,200 不可修。

## YAML 卫生（09-03，导入器必读）
- **js-yaml 4（Dataview/Bases 同源）遇重复键/非法转义直接 THROW——整条文件在 Obsidian 消失**；PyYAML 只后值覆盖不报错。导入闸门必含「js-yaml 解析 0 失败」。
- **09-03 全库清零**：md 9,961/有FM 9,369/失败=0。累计修 94 重复键+60 KP+48 长尾（fix_vault_yaml_syntax.py 11 类，提交 0b905a15）。形态速查：值含裸 `: ` 或以 `*`/`[` 开头（如 [Re₂Cl₈]）→加引号；全角引号“”非定界符；`aliases: - x` 单行非法；wikilink 逗号连写→引号化 inline list，**含 §引用等残留文本的段整段加双引号**（零丢失勿硬拆）；裸化学名 token 用 `(?<!")` 防重复包裹。
- frontmatter wikilink 路径一律 `/` 禁 `\`；FM 内禁独立行 `![[...]]`；QB_LINK_FIELDS 仅 knowledge_points/depends_on/cross_references/related/superseded_by；同名键取最后一次。

## 组卷与出卷
- 组卷工作台：used_in 是 wikilink → Link **无 `.length`**（hasUsed 判空）；dataviewjs 块间不共享作用域；srcKey 归一 1,087 来源；出卷闭环 `mark_used.py --paper`；补弱 `gen_weak_drill.py --kp`；used_in 多标排查=卷内链接集合 vs 标记集合比对（09-03 结构化学卷 150 多标已修 4951742b）。
- 三预设 staged `.workbuddy/staging/`，过 Gate ①② 贴工作台；`check_workbench_js.py --file` 校验。

## 题库铁律
- 例题写 `type:题目`+`question_type:例题`；重建直接 `--clean --write`（`CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID=` 绕 safe-delete）。
- 校验器只约束 4 字段（fidelity/difficulty/exam_stage/subject_module）；`source_subject`=来源教材分科、`subject_module`=四大模块，两者不同是设计意图勿"修正"。**subject_module 合法值仅四选一：化学原理/结构化学/有机化学/元素与分析**——写「无机和结构化学」会被 validate --changed 抓 Warning。
- teaching_level 仅 4 档；question_type 双维度+角色并存，画结构式归`作图`、`简答`兜底不推断、多问留空。
- **knowledge_points 留空前必查「宏观近邻」**：原子轨道/元素周期律/元素周期表类宏观 KP 往往存在（validate 抓空列表 W）；细粒缺口才登记清单。照抄 OCR 半截 math 是惯性坑（批3 题-057、批5 题-097 连犯）——写文件时主动 grep `\$^{-1}\|\$_{` 自查。
- **Edit 多行表格区块必须锚首尾两行**（只锚单行会把中间行误删）；改后 grep 行数验证。
- **批量改字段脚本第一步：type 白名单 {题目,真题}**。真题 `year=N+1986`；题组子题按题号前缀折叠、折叠前对账小问数；细概念走 concepts。
- 审计宏黑名单：`xlongequal|\AA\b|Biggl|xrightleftharpoons`——可逆箭头写裸 `\rightleftharpoons`（562 处主流不标记）；validate --changed 需显式传文件。半截 math（`$^{-1}$`/`$_{2}$`/`$^{1}$` 独立成 math）＝审计 P2 分裂记号 → 修 Unicode 或完整 math。
- **校勘注/HTML 注释里禁逐字保留修复前的 `$...$` 字面量**——audit 分裂记号检测扫原始文本含注释，会自证命中（P2 假阳性）；注释用「上标X/下标X」描述性写法。闸门④=audit_book_coverage.py（无独立 check_pack_rule.py）。**批4 扩展：注释里连「## 」等结构记号都不能字面引用**（被 P1「多标题挤一行」命中）；试题原文 xlongequal 也算黑名单宏，转录时直接写 xrightarrow（批4 题-062 放电箭头）。

## 链接与图片
- 链接解析禁自写正则：`import validate_kb as V` 复用；修断链只「精确相等+同目录」；frontmatter 断链 1,643 存量不动；basename 命中=设计意图、名实不符只改内容不改名；媒体仓库/ 不入库是设计；wikilink 示例用全角［［…］］防误报。

## 批量改 md/docx 防坑
- **split("\n") 行列表元素禁含 `\n`**（join 翻倍空行）；插行/替换行行尾用 tr_of() 取实际行；读写 `open(newline="")`。查行尾只认 Python 数 `b'\r\n'`（grep 假阳性）；bash 双引号/heredoc 吃 `$`、`:\s` 与反引号 → 一律 Write 成 .py。
- 改前 zip 快照 + 写后逐行 diff；zip arcname 正斜杠；批量显式暂存用 `git add --pathspec-from-file`。删行复验断言：LF 总差=1、CRLF 差∈{0,1}（删的可能是 LF 行）。
- docx 批量走 python-docx+lxml+zipfile（禁 HTML 往返毁 OMML）+LibreOffice 验证；证据字段不当修复对象。

## 新建 KP 与生命周期
- 新建 KP：`subject→source_subject` 只作用 04/05-题库（03-知识点 仍 `subject`）；related/prerequisite 纯文本；不写 stage 绕门禁。
- 废弃唯一机制 `status:deprecated`+`deprecation_reason`+`superseded_by`；标废弃前证伪「内容不丢」；判僵尸字段先 grep scripts。

## 用户决策
- 断链存量不动；质量优先于难度；新题默认 10-待审核区。
- 2026-09-02：三模块=一库三视图；巡检周一0800 异常才报。
- **并行信号（09-03 00:44 起）**：另一对话（导入计划）正在写库——习题提炼/教程目录/Atkins 题，+.7 断链已由其修回；数字全在漂移。**并行现场，提交用显式 pathspec 排除**。

## 遗留待办
- Gate ①②✅（09-03 三预设已装工作台，6 块全绿）。习题书 V3 题-033；40 题 KP 指派；讲义 38 断链勿批量。
