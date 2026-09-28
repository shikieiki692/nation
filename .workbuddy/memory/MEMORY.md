# 妙妙屋·长期记忆（v39，2026-09-28 精简）

> 只留高频规则＋指针。**上一版完整内容**在 `.workbuddy/memory/2026-09-28-MEMORY细则归档.md`；规范在 `11-模板/规范/`；逐日经过在 `YYYY-MM-DD.md`、`09-审计报告/`。

## ★ 讲义线（活跃）

- 现役讲义＝**73**（六栏目非 README）；全库 md 145＝六栏目 74＋数学工具 9＋综合 2＋根 1＋归档 59（**三值禁互减**）。
- 度量唯一入口＝`11-模板/scripts/handout_metrics.py`（旧 `vault_deep_audit.py` 判据作废）。
- **四闸门**：① `11-模板/scripts/qa/validate_handout.py --changed` ② `render_gate.py --changed`（改渲染必须再跑 full；`--regression` 只判"是否变差"）③ `build-all-handout-docx.py --path <md> --output-dir 06-学生侧材料/讲义` ④ 纯净度断言（违规引用框 / body bullets / 机械标签 / 噱头黑话）。pre-commit 回归红→先跑 full 自证，再登记 `11-模板/scripts/render_gate_allowlist.txt`，⛔ 禁 `--no-verify`。
- **讲义口径**：25 题 100% 取自题库 + 独立 `### 参考答案与精解`（先全题后答案）；按 `04-课件/备课大纲/<讲>-*.md` 的 `deferred_topics` 剪裁超纲；合规化（去黑话/噱头）；双轨（母版 + 学生专用版 25 处 `<br><br><br>`，留白须插在**整题之后**）；配图逐张目检化学式下标（无下标**直接剔除**，宁可留白）；图注 `> 图 N-M：`。
- **进度**：Batch 4 无机 9 份全收口；4-分析化学 5 份收口；**3-物理化学 12 份已完成 2**（气体基础 `330029886`、沉淀溶解平衡 `ad4c12855`）。
- 🔴 **物化 10 份待办**：工作区是「旧式长版」，**HEAD 是新式规范版**（与络合滴定相反）→ 动工前先比两版节标题，取更规范者；若取 HEAD 须 `git checkout -- <file>`。
- 题源主力：`04-题库/化学原理/Ch02–Ch10`（原书逐字）、`教材习题/无机化学例题与习题/`（按章）、`HChO方程式专题`、`05-真题库/`、`04-题库/真题/`。⛔ `04-题库/分析化学/`、`元素化学/过渡-*/` 为 B- 自编池不可用。

## 一、环境与闸门

- Py `C:\Users\蕾赛\.workbuddy\binaries\python\versions\3.13.12\python.exe -X utf8`；Node `…/22.22.2/node.exe` + `NODE_PATH=…/node/workspace/node_modules`。
- 双闸门：`jsyaml_verify.js --list`（须 `PYTHON=<系统 Py3.12>`）＋ `validate_kb.py --changed`；跑完**必删** `09-审计报告/auto-validation/<日期>-validation.md`。

## 二、铁律（坑·高频）

- **js-yaml4 遇重复键/非法转义 THROW ⇒ 文件在 Obsidian 消失（P0）**：值含裸 `: `、以 `*`/`[`/`{` 开头 ⇒ 加引号；FM 内 wikilink 用 `/`；禁反斜杠 LaTeX。
- **texmath 三条硬边界**：① `\frac` 3 层嵌套必炸；② array 单元格 `\text{}` 不可含 `_`/`^`（2 行 array 必炸）；③ 单元格行首 `[` 触发 `\\[` 解析 ⇒ 写 `\mathrm{[…]}`。另 `\]`／`\atop`／`\cdotK` 不支持。
- **`$$` 三坑**：后换行以 `:` 开头 ⇒ pandoc 判非数学；被空行切断同理；块内嵌行内 `$` 须去。
- **行内数学 `$` 后不可紧跟空格**（写 `$a>0.5$` 而非 `$ a>0.5 $`）。
- 🔴 **正则处理 `$$…$$` 会定界符配对错位** ⇒ 先暂存 `$$` 块，再处理行内 `$…$`，最后还原。
- **写盘铁律**：`open(p,"w").write(...)` 先截断 ⇒ 一律**先算后写 + 断言长度**。
- 含正则/emoji/非 ASCII 脚本必须 Write 成 `.py`；批量替换先 dry-run；锚点未命中先 `repr()`；含 `|`/`*`/`[` 串禁 `grep -E`。
- ⛔ 禁 `os.removedirs()`／`git rm -r`／统一转 LF；自写校验先自证（扫 0＝静默失效）。

## 三、git

- 中文路径 `-z`；只 add 本会话文件；⛔ `git add -- <目录>`。
- 🔴 **每次 commit 先锁基线**：`BASE=$(git rev-parse HEAD); export GIT_INDEX_FILE=.workbuddy/tmp/index_xxx; git read-tree $BASE; git add -- <files>; NOW=$(git rev-parse HEAD); [ "$BASE" != "$NOW" ] && { git read-tree $NOW; git add -- <files>; }`。
- 提交后核 `diff-tree --no-commit-id --name-only -r HEAD | wc -l` = 本会话文件数；对缺失条目补 `git add`（否则出 `D ` 伪信号）。临时索引用后即删。
- push 走 Clash 7897；未推送只信 `ls-remote`。

## 四、红线与协作

- 🔴 禁改：`04-题库/`（除约定区）、`05-真题库/`、`_归档/`；不动并行会话未跟踪文件。
- **疑问句＝只核验不执行**；隔离判据 mtime（静默 >45min 才动）。
- 改数前先自校验——对得上就别改。机检清零 ≠ 达标，须换维度目检。

## 五、题库口径（判据索引）

- 组卷池 6,062 ＝ 04-题库非 deprecated 6,021 ＋ 05-真题库 41；README 登记 6,793；**三口径禁互减**。
- deprecated ＝ `^status:\s*deprecated`；`used_in` 累积台账禁相减；禁改 `teaching_level`。
- 2026 机构初赛模拟题专区 ＝ **3,009 卡**（13 机构）；源 PDF 646（全 OCR）。
- 判「有没有答案」终判 ＝ **题面汉字指纹（16 字）回搜该机构全部 md**；⛔ 不用 `source_file` 链接（会漏「题面+答案合并本」）。
- 机构模拟题**参考答案多为考生答卷 OCR**（公式破损）⇒ ⛔ 不可直接引用；题面可取自题库，**解答须基于题面重推**。
- 图片完整性 ＝ 21,432 引用 / 缺失 0；`.workbuddy/tmp/mineru_raw/…/ocr/images/` 存唯一副本 → **禁清理**。
- ⚠️ `difficulty` 全库恒为 4；`subject_module` 与重判一致率 96.8%。
