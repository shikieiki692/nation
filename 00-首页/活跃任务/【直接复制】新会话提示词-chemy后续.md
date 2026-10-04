你是 Obsidian vault「妙妙屋」（`C:\Obsidion\妙妙屋`）的执行助手，负责**题库提炼线**的 chemy 试题后续工作。请仔细读完本提示词再动手，脚踏实地，不要抢跑到下一个任务。

## 一、任务背景

`chemy试题/` 目录下的矿物uPDF（mineru）OCR 源料已**全部切分成题库卡并入库**，共 **1268 张**，五道闸门全绿。本会话要收掉两项遗留。

| 目录 | 卡数 | 套号 | images |
|:--|--:|:--|--:|
| `04-题库/2026机构初赛模拟题/chemy/` | 1201 | 138 个（CM-01~CM-191） | 8899 |
| `04-题库/真题/chemy/` | 67 | 7 个（CM-43~CM-49） | 438 |

**下一个可用套号：CM-192**（台账 `04-题库/2026机构初赛模拟题/chemy/CM编号台账.md`）

## 二、本会话的任务（按优先级，不许跳序）

### 🔴 P0-1：补 KP 锚点 244 张

`knowledge_points` 字段目前只覆盖 1024/1268（80.8%），**244 张为空**：

| 号段 | 批次 | 已填 | **待补** |
|:--|:--|--:|--:|
| CM-01~CM-40 | 早期（40~42 届） | 109 | **56** |
| CM-41~CM-60 | P1（37 届决赛） | 140 | **69** |
| CM-61~CM-90 | P2-b（33/34 届） | 270 | **28** |
| CM-91~CM-173 | P2-c（35~38 届） | 502 | **76** |
| CM-174~CM-181 | P3（39 届 HiChO） | 3 | **5** |
| CM-182~CM-191 | P5（39 届 XChem） | 0 | **10（全空）** |

已核实现有 3738 条 KP 引用**页不存在 0｜指向 deprecated 0**，质量可靠，只是覆盖不足。

**做法**：走既有技能 `~/.workbuddy/skills/qbank-anchor-manual-tagging`（人工精标流水线）。
⛔ **纯自动映射不可用**（启发式实测准确率仅约 55%，同尾词会误判，如 `硫化学→锇化学`），只做**语义等价**变体映射，改 FM 时**只替换 `knowledge_points` 段内**的 `[[X]]→[[Y]]`，不要动其他字段。

**硬约束（违反会写坏库）**：
- 选的目标页名必须**真实存在**于 `03-知识点/`（950 页）
- ⛔ **deprecated 页一律拒写**（两式并查 `status: deprecated` ＋ 老式 `deprecated: true`，实测各漏过一次）
- `syllabus_codes` 按 `02-考纲条目` 的**实测集合**校验，⛔ 不可硬编码 `1..56`（会误拒合法的 `57`「化学动力学」与「决赛NN」）
- 写库护栏用 `tag_apply.py`；写完跑 `r3_dep_check.py`
- 🔴 **判「是否已补」必须按 `knowledge_points` 的「值非空」** —— ⛔ 不能按「键是否存在」（导入管线预置 `[]`，按键判会得「100% 已补」的假阳性）
- 建议分批（每批 40~60 张），每批跑完闸门再进下一批，不要一次全量

### 🟡 P0-2：源侧OCR 丢图复原 31 处

`04-题库/2026机构初赛模拟题/chemy/` 里有 **31 处图片断链**，已用全库 91809 个哈希索引逐一确认「源侧无实体」⇒ 只能从**原 PDF** 重新提取（原 PDF 在 `06-外部资料导入/`，910 个 pdf）。

🔴 **终检口径**：`media 数 == md 图数`，且**必须同时扫** `![](...)` 与 `<img src=…>`（⛔ 只扫前者会漏 202 处表内图）。
🔴 **反斜杠翻倍＝docx静默丢图**（`\|320` 写成 `\\|320` ⇒ 图消失而闸门全绿），改图脚本必带图数守恒断言。

### 🟢 P2：源卷未做的 2 项 —— **owner 已指示跳过，不要开工**

- `chemy试题/第39届模拟试题合集.*` —— 题面缺源，只有答案 2 块（无法配对）
- `chemy试题/第1~38届初赛真题合集.md`（538 KB）—— 真题库已有，不重复建卡

## 三、开工前必读（4 个文件，按序）

1. `00-首页/活跃任务/交接提示词-2026-10-05-chemy题库提炼线.md` —— **最新自包含交接**（五闸门完整命令、11 条提交纪律、血泪判据速查）
2. `00-首页/活跃任务/交接提示词-2026-10-02-chemy试题精修与题库提炼.md` —— 原始工单（P0~P3 批次定义、CM 卡 FM 模板、**红线清单**）
3. `04-题库/2026机构初赛模拟题/chemy/CM编号台账.md` —— 已占用套号/ 下号 / 每套源文件与卡数
4. `~/.workbuddy/skills/qbank-anchor-manual-tagging/SKILL.md` —— 精标流水线（读它的 SKILL ＋ pitfalls）
   顺带读 `~/.workbuddy/skills/ocr-card-build-pipeline/SKILL.md`（建卡/闸门/回滚纪律）

**本机工具链（勿换）**
- 受管 Python 3.13：`C:\Users\蕾赛\.workbuddy\binaries\python\versions\3.13.12\python.exe -X utf8`
- ⚠️ **`ruamel.yaml` 只装在系统 Python 3.12** ⇒ 跑 FM 严格校验必须用
  `C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe -X utf8`
- 工作脚本放 `.workbuddy/scripts/`（已 gitignore，不入库）

## 四、五闸门（全部通过才算完成，基线值必须先跑一遍确认环境一致）

```bash
PY="C:/Users/蕾赛/.workbuddy/binaries/python/versions/3.13.12/python.exe"
PY312="C:/Users/蕾赛/AppData/Local/Programs/Python/Python312/python.exe"

# G0 清单（🔴 改名/新建后必须重生成，否则闸门报「文件不存在」被计入失败）
$PY -X utf8 -c "
import glob,os
new=[f.replace(chr(92),'/') for D in [r'04-题库/2026机构初赛模拟题/chemy', r'04-题库/真题/chemy']
     for f in glob.glob(os.path.join(D,'题-CM-*.md'))]
open('.workbuddy/tmp/manifest.txt','w',encoding='utf-8',newline=chr(10)).write(chr(10).join(new)+chr(10))
print('清单 %d 张'%len(new))"

# G1 专项审计
$PY -X utf8 11-模板/scripts/audit_question_bank.py --dir "04-题库/2026机构初赛模拟题/chemy" | grep -E "受检|P0="
# G2 frontmatter 严格校验（23 字段 + 三节 + $ 行级配对 + 答案区非空）—— 必须用 PY312
$PY312 -X utf8 .workbuddy/scripts/p2a_fm_check.py 1 250
# G3 图片断链（双口径）
$PY -X utf8 .workbuddy/scripts/p2a_linkcheck.py 1 250
# G4 渲染闸门（⛔ 失败数是唯一止损信号，改完立刻跑并与基线比对）
$PY -X utf8 11-模板/scripts/render_gate.py --manifest .workbuddy/tmp/manifest.txt --regression -q --time-budget 1800
# G5 全库 frontmatter/结构
$PY -X utf8 11-模板/scripts/validate_kb.py --dir "04-题库" | grep -E "受检:|Error:"
```

**当前基线（务必先跑一遍对齐）**
G1 受检 **1202** / **P0=0**（P1=121／P2=6681）｜G2 **596 张 / Error 0**｜G3 引用 **6405 处 / 断链 31**｜G4 受检 **1268 / 失败 0**｜G5 受检 **10765 / Error 0**｜真撞库 **0**

## 五、提交纪律（本库特有，必须遵守）

1. ⛔ **永不 `git add -A`、永不目录级 `git add`** —— 只能**逐路径精确 add**（中文/空格路径必加引号，分批 ≤100）
2. ⛔ **本库有并行会话** —— add 前记录暂存区基线，add 后**精确核对「暂存区 == 本会话路径集合」**，多一个就`git reset` 掉并中止
3. ⛔ **隔离索引（`GIT_INDEX_FILE`）在本库会混入并行会话的 add**（实测带入 130+ 个他人卡片）⇒ 正解＝**主索引 + 逐路径 add**（参考 `.workbuddy/scripts/p2bc_commit2.py`）
4. 🔴 **回滚目标 ref 必须是「误修复之前」的 commit** —— `git checkout HEAD --` 在已提交后是**空操作**；应`git checkout <误修复commit>^ -- <路径>`。动手前先 `git log --oneline -3` 记住 HEAD
5. 🔴 **备份文件本身可能被污染** ⇒ `git show <ref>:<路径>` 回源对照才是权威
6. `git ls-files` 输出**带引号＋octal 转义** ⇒ 路径比对必须加 `-c core.quotepath=false`
7. `git commit` 给 **600 s** 超时（pre-commit钩子含 75 s render_gate ＋ 18 MB 索引 read-tree）
8. `git status` 会折叠未跟踪目录 ⇒ 核体量必须 `-uall`
9. 推送用 `git -c credential.helper=manager push origin master`（本机 `~/.gitconfig` 有空 `helper = ` 会挡），推完用 `git ls-remote` 核对
10. 🔴 **「让闸门变差」的修复一律回滚**，不「再修一修试试」（本项目已踩 **4 次**：P2-a 花括号兜底／P2-b `\cdot` 批量／P2-c 跨行 `$`／P2-c 行内公式首尾空白）
11. 🔴 **任何「删信息」操作先备份**，`--dry` 必须真不写盘

## 六、环境红线

- ⛔ **禁改 `04-题库/`（除标注类 FM 字段 `knowledge_points` / `syllabus_codes` ）、`05-真题库/`、`_归档/`**
- ⛔ 不动并行会话的未跟踪文件；疑问句＝只核验不执行

## 七、血泪判据速查（最容易踩的）

**卡片结构**
- 三节固定 `## 题目` / `## 参考答案` / `## 知识点映射`；H3 标题**必须含题号**（`### 第 N 题`）
- 🔴 **卡名不得含连续横线 `---`**（YAML 会当文档分隔符 ⇒ `validate_kb` 报缺字段）
- FM 块列表**必须写 `- `**（裸 `[[…]]` ⇒ js-yaml4 THROW ⇒ 文件在 Obsidian 消失）
- 🔴 **FM 解析必须抗 CRLF ＋ 抗行内数组**：先 `read_bytes().decode('utf-8-sig').replace('\r\n','\n')`，配`^key:(.*)$` ＋ `[^\r\n]+`
- 🔴 **「某状态突然大量报错」时先质疑判据是否过期**，别急着修数据。实例：`p2a_fm_check.py` 的「kp 非空」判据（P2-a 时期「建卡不带锚点」假设）在 T4 锚点线补锚点后误报 557 个 Error

**渲染（pandoc ＋ texmath）**
- 🔴 渲染失败最大单一原因＝`<div class="mineru-algorithm">`（CommonMark 下行首 `<div>` 吞掉块内 markdown）
- 🔴 **表格cell 内 pandoc 不解析公式** ⇒ `$…$` 落在 `<td>` 里会原样输出 `$`
- 🔴 **行内公式首/尾不得有空格**（`$60 $`、`$ P 7.03 % $` 都判为字面）
- ⛔ **texmath 边界**：`\frac` 三层嵌套必炸；array 单元格 `\text{}` 不可含 `_`/`^`；忌 `\dfrac`
- ⛔ **`$$` 三坑**：后换行以 `:` 开头 ⇒ pandoc 判非数学；被空行切断同理；行内 `$` 后不可紧跟空格
- 🔴 **跨段配对型正则（`$…$`／`$$…$$`）动手前必须验「配对跨度」** —— 两次定界符之间若含中文标点/换行/表格竖线，**不是公式**，不许动

**图片**
- 🔴 搬图必须在写盘前，且**引用扩展名按实体真实扩展名对齐**（卡里写 `.jpg`、实体 `.png` ⇒ 断链）
- 🔴 拼接路径易产生**双扩展名** `hash..jpg` ⇒ 改完必跑断链检查
- ⛔ **配图只用现有教材图，禁 AI 自绘/生成**（图上化学式缺下标或英文标注即不合格）

## 八、收工要求

1. 更新 `00-首页/工作日志/2026-10-05.md`（新建）记录本会话做了什么、遗留什么
2. 更新 `00-首页/状态摘要.md` 顶部条目
3. 更新 `04-题库/2026机构初赛模拟题/chemy/CM编号台账.md` 的收官状态段
4. 更新 `00-首页/活跃任务/交接提示词-2026-10-05-chemy题库提炼线.md` 的「§七 本次会话追加」与「§三 剩余工作」
5. 追加 `.workbuddy/memory/2026-10-05.md` 日志
6. 逐路径精确提交 ＋ 推送 ＋ `git ls-remote` 核对远端
7. 汇报格式：结论先行 → 量化表格（命令/受检/失败数）→ 遗留清单（带优先级与数量）→ 本轮新踩的坑及判据

**请先复现一遍 §四 的基线数字确认环境一致，再开始 P0-1。动手前若有疑问，先问我，不要猜。**
