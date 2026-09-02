# 妙妙屋题库·长期记忆

## 环境
- 脚本用系统 Python 3.12（有 PyYAML）：`C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe -X utf8`；全量校验 `11-模板/scripts/validate_kb.py --full`。

## 关键基线（09-03）
- 题目总数 **4,182** = 04-题库 4,119(`type:题目`) + 05-真题库 63(`type:真题`)；双 type 白名单，04-题库 另有 142 个非题目 md。
- status 3,377/792/弃8/待填5 全覆盖；--full Error 0 Warning 209。
- question_type 42.1%；LLM 放量清单就绪（批1 池 1,314，Gate ③ ≥23/25）。
- 三模块视图：习题集=基础+巩固 1,766/习题书=拓展 1,521/测试题=竞赛 882（teaching_level 唯一决定）；三 .base 待实渲染；基础池 452 偏薄。
- 习题书 31 章/1,283 题事实源=题库架构总览.md；图片真缺失 3,200 不可修。

## YAML 卫生（09-03，导入器必读）
- **js-yaml 4（Dataview/Bases 同源）遇重复键/非法转义直接 THROW——整条文件在 Obsidian 消失**；PyYAML 只后值覆盖不报错。导入闸门必含「js-yaml 解析 0 失败」。
- 已修：94 重复键（fix_fm_dup_keys.py 语义选值）+ 60 个 03-知识点 缺陷（fix_kp_yaml_syntax.py：A `\`→`/` 41 / B FM 内 `![[...]]` 挪正文 9 / D key_images[] 空壳挂回 5 / E tags 断行拼接+引号 5）。
- frontmatter wikilink 路径一律 `/` 禁 `\`；FM 内禁独立行 `![[...]]`；QB_LINK_FIELDS 仅 knowledge_points/depends_on/cross_references/related/superseded_by；解析同名键取最后一次（行级 `\s*` 会吃换行误捕）。

## 组卷与出卷
- `used_in` 是 wikilink → Link **无 `.length`**（判空用 hasUsed 模式）；dataviewjs 块间不共享作用域；diffNum 取首整数；srcKey 归一 1,087 来源；出卷闭环 `mark_used.py --paper`。
- 补弱卷 `gen_weak_drill.py --kp <KP> [--write]`：降档链 15 题、KP 精确命中（rglob 子目录）、贪心覆盖、产物 06-学生侧材料/练习卷/。
- 三预设 staged `.workbuddy/staging/`，过 Gate ①② 贴工作台；`check_workbench_js.py --file` 校验。knowledge_points 三写法（inline/scalar/block）。

## 题库铁律
- 例题写 `type:题目`+`question_type:例题`；重建直接 `--clean --write`（`CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID=` 绕 safe-delete）。
- 校验器只约束 4 字段（fidelity/difficulty/exam_stage/subject_module）；`source_subject`=来源教材分科、`subject_module`=四大模块，两者不同是设计意图勿"修正"。
- teaching_level 仅 4 档；question_type 双维度+角色并存，画结构式归`作图`、`简答`兜底不推断、多问留空。
- **批量改字段脚本第一步：type 白名单 {题目,真题}**。真题 `year=N+1986`；题组子题按题号前缀折叠、折叠前对账小问数；细概念走 concepts。

## 链接与图片
- 链接解析禁自写正则：`import validate_kb as V` 复用；修断链只「精确相等+同目录」；frontmatter 断链 1,643 存量不动；basename 命中=设计意图、名实不符只改内容不改名；媒体仓库/ 不入库是设计；wikilink 示例用全角［［…］］防误报。

## 批量改 md/docx 防坑
- **split("\n") 行列表元素禁含 `\n`**（join 翻倍成多余空行）；插入/替换行行尾用 tr_of()（`"\r"` 或 `""`）且**取实际行而非模板串**；读写 `open(newline="")`；插行按邻居补 `\r`。
- 查行尾只认 Python 数 `b'\r\n'`（grep $'\r' 假阳性）；git diff 因 eol=lf 测不出 CRLF；frontmatter 判定 split("\n") 找第二个 `---`；bash 双引号/heredoc 吃 `$`、`:\s` 与反引号 → 一律 Write 成 .py。
- 改前 zip 快照 + 写后与快照逐行 diff（difflib 断言结构+新行行尾=邻居）；zip arcname 正斜杠；`git add 2>/dev/null` 防警告 SIGTERM 留 index.lock。
- docx 批量：python-docx+lxml+zipfile（禁 HTML 往返毁 OMML）+LibreOffice 验证；09-审计报告 证据字段不当修复对象。

## 新建 KP 与生命周期
- 新建 KP：`subject→source_subject` 只作用 04/05-题库（03-知识点 仍 `subject`）；related/prerequisite 纯文本；不写 stage 绕门禁；一词多义分节。
- 废弃唯一机制 `status:deprecated`+`deprecation_reason`+`superseded_by`；标废弃前证伪「内容不丢」；判僵尸字段先 grep scripts。

## 用户决策
- 2026-08-31：断链存量不动；质量优先于难度；新题默认 10-待审核区。
- 2026-09-02：三模块=一库三视图；最小闭环=失分复盘→按 KP 抽未用题→mark_used；LLM 放量=抽25核验≥90% 分批≤300；巡检周一0800 异常才报；--changed 入 SOP。
- 导入：四类来源全选、几百题分批；计划在另一对话，汇合前库保持 js-yaml 0 失败底座。

## 遗留待办
- Gate ①② 实渲染/实跑→贴三预设；Gate ③→LLM 放量 5 批。习题书 V3 题-033；ABOC 211 占位；40 题 KP 指派；讲义 38 断链勿批量；孤儿目录先报告。
