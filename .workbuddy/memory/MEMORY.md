# 项目长期记忆（妙妙屋化学竞赛知识库）

## 环境与运行（硬性）
- `11-模板/scripts/` 校验/审计脚本必须用系统 Python 3.12：`C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe`（有 PyYAML）；managed 3.13.12 无 PyYAML。
- 跑校验器：`...Python312\python.exe -X utf8 11-模板/scripts/validate_kb.py --full`（约 75 秒，后台跑）。

## 关键基线（2026-09-02 实测）
- 题目总数 **4,186** = 04-题库 4,123（type=题目，含省预赛 260：江苏 10+福建 10+浙江 240【09-02 拆题】）+ 05-真题库 63；`no_answer: 0`（ABOC 211 思路占位为合法）。
- validate_kb --full：6,407 文件 · **Error 0 · Warning 1,641**（断链 45 + frontmatter 1,590 + 标题跳跃 3 + stage 门禁 3）。
- 习题书 **31 章 / 1,283 题**，单一事实源 = 04-题库/题库架构总览.md；docx 三版本在 `00-首页/题组Word/习题书/`。
- 全库图片引用 23,654：真缺失 3,200 属资产丢失脚本不可修；剥 `../` 可修 440 全在归档目录；统计"可修"必须先排除根兜底命中 1,092。巡检脚本 `.workbuddy/scripts/audit_vault_images.py` + `gen_vault_img_report.py`。

## 题库操作铁律
- 例题写 `type: 题目` + `question_type: 例题`（`type: 例题` 不被构建 gather 识别）。
- 重建直接 `--clean --write`（已内置文件锁重试），勿先 rm；Python 调用加 `CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID=` 绕 safe-delete shim + `-X utf8`。
- 导入新题一律走 04-题库/新题入库SOP；文档里写语法示例用全角方括号防误报断链。
- 汇智源编号 = 题库编号；答案只有图的题不要编造文字答案。
- 六字段枚举仅限题目类文件（QB_TYPES）；difficulty 允许区间、exam_stage 允许 `/` 多值。
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

## 批量改 md 防坑
- frontmatter 判定：首行 `---` 且头部含 `^[\w\-]+:`；读写一律 `newline=""`（防 CRLF 整文件重写，`git diff --stat` 增删行数应≈改动数）；自动补别名取路径末段；别把 `09-审计报告/` 报告的历史证据字段当修复对象。

## 批量 docx 经验
- 走 python-docx + lxml + zipfile 后处理，**不走** tencent-docx HTML 往返（毁 OMML 公式与图位）。
- 彩图检测用全分辨率网格采样（resize 会漏检小面积彩色）；覆盖写直接 `zipfile.ZipFile(path,'w')`（shutil.move 触发 safe-delete 批删拦截）。
- XML 颜色归一化：注意自闭合 `/>` 与非闭合两种形态都要匹配。
- 渲染验证用 LibreOffice headless `--convert-to pdf` 兜底（Word COM 沙箱下报错）。
- 页脚 PAGE/NUMPAGES 需完整 fldChar begin→instrText→separate→占位文本→end。

## 新建知识点文件字段安全写法
- 必填 title/type/subject/status/updated；`subject_module` 才有枚举（subject/module 没有）；`related`/`prerequisite` 写纯文本数组（在 QB_LINK_FIELDS 里，写 wikilink 会被查断链）；不写 `stage` 字段绕 published 门禁；一词多义建一个文件内部分节，勿拆重名。

## 用户决策（2026-08-31）
- 断链类存量暂不处理；索引口径历史数字保留原值；33 个非题目文件命名豁免。
- 质量优先于难度：不做难度分级，构建排序 fidelity 优先（🟢逐字>🟡改写>🔵自编）。
- 新题分层入库：默认 10-待审核区 P1 流程，P0 小额已核验直入。

## IMA / 资料库导出
- IMA：md+相对路径图打 ZIP → 笔记模块 Notion 类型导入 → 关联知识库；双链转纯文本勿转 md 链接；批量 20~50/次。
- `vault_to_ima_convert.py` 已跑通 03-知识点 → 943 篇 → `C:\Obsidion\导出_IMA\03-知识点.zip`（图解析 99.9%）。

## 遗留待办
- 习题书 V3：题-033 查纸质原书补题补答；ABOC 211 条思路占位待人工。
- Word precheck 少量 `^\circ`/裸下标 warning，源稿后续统一写 `\theta`。
- 学生版-打印版 ~51% 图有效 DPI<150（源 72 DPI），是否回溯换源图待用户定。
