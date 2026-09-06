---
title: LaTeX PDF生成策略文档
type: 系统
updated: 2026-06-29
---

# LaTeX PDF 生成策略文档

> 目的：记录当前 LaTeX 管线的完整流程、各步骤职责、关键决策原因、血泪教训和快速上手指南，便于后续优化和全员接手。

---

## ⚡ 快速上手指南

### 管线一句话
```
源 .md → convert_handout_to_pdf.py (preprint + Pandoc) → .tex → xelatex×2 → .pdf
```

### 关键文件位置

| 文件/目录 | 路径 | 说明 |
|:---|:---|---|
| **管线入口** | `11-模板/scripts/convert_handout_to_pdf.py` | 唯一入口，预处理→Pandoc→编译全在这 |
| **LaTeX 导言** | `11-模板/scripts/chemistry-preamble.tex` | ctexart + mhchem + 自定义box环境 |
| **图片Lua过滤** | `11-模板/scripts/wrap_images.lua` | Pandoc filter，纯图段落包 figure[H] |
| **中英别名** | `11-模板/scripts/chem_media_aliases.json` | 中文↔ASCII图片文件名映射 |
| **策略文档** | **本文件** | 全管线说明 + 决策理由 + 血泪教训 |
| 源讲义（MD） | `04-课件/学生讲义/*.md` | **只读！永远不修改** |
| 正式media | `media/` | 图片源目录（唯一正式路径） |
| 图片缓存 | `11-模板/scripts/.chem_media/` | workspace-local 图片复制品（xelatex 实际读这里） |
| PDF 成品 | `00-首页/学生讲义PDF/*.pdf` | 编译成功后的统一落点（自动创建目录） |
| 预处理产物 | `11-模板/scripts/_pre_xxx.md` | 预处理后的 Markdown（调试用） |
| LaTeX body | `11-模板/scripts/_body_xxx.tex` | Pandoc 产物（debug 格式问题查这里） |
| 完整 LaTeX | `11-模板/scripts/_handout_xxx.tex` | 拼接后的完整文档 |
| 编译日志 | `11-模板/scripts/_handout_xxx.log` | xelatex 日志（查 ! Error / Missing character / Overfull） |
| 目录文件 | `11-模板/scripts/_handout_xxx.toc` | PDF 目录内容，检查标题降级是否生效 |

### 常用命令

```bash
# 生成单本
python 11-模板/scripts/convert_handout_to_pdf.py "原子结构-超级充实版（自学完整）.md"

# 生成全部6本（并行3路，更快）
python 11-模板/scripts/convert_handout_to_pdf.py ALL --parallel

# 指定输出
# PDF 自动放到 00-首页/学生讲义PDF/同名.pdf
```

### 回归验证工作流（2026-06-28 确认）

1. 先跑 `pdf_preflight.py`，把 `error` 清零后再编译
2. 单本或小批量验证时，优先用 **PowerShell 直接跑 Python**
3. 如果 `ALL` 或 `.bat` / `cmd` 链路显示“整批全挂”，不要立刻判失败；先抽一本文档做 direct Python 复核
4. 最终回归结论以三件事为准：
   - 真实生成出的 PDF
   - `_handout_*.log` 中的错误/警告
   - CLI 汇总统计（页数、图数、`全图 OK / 缺图=N [WARN]`）

> 当前 Codex 桌面环境已确认存在一种假失败：嵌套 `cmd /c` / `.bat` 可能误报 `xelatex 输出为空`，而 PowerShell 直接调用 Python 实际可以成功出 PDF。

### ⛔ 红线规则（每次操作前先读）

1. **永远不修改 `04-课件/学生讲义/*.md`** — 源文件是 Obsidian 知识库的资产，格式/图片引用/RGB值 全是用户手写的。管线只能改**预处理副本**（`_pre_xxx.md`）。需要任何格式修复（图片大小、转义、标题降级），都在 `preprint()` 函数里做。
2. **永远不改 `media/*` 下的图片引用** — 用户写了什么路径就是什么路径。图片加载不了一样是管线的错，不是源文件的错。
3. **`chem_media_aliases.json` 中的 SVG→JPG 别名会破坏图片** — 不要把 `.svg` 映射为 `.jpg` 或 `.png` 扩展名。SVG 应自动转成真正的 PNG（见管线 SVG→PNG 逻辑）。
4. **`\pandocbounded{` 剥离后必须同时清理多余的 `}`** — 参考 `convert_handout_to_pdf.py` 第 284 行的 regex。

### 常见问题排障（简版）

| 症状 | 第一步 |
|:---|---|
| PDF 只有几页/很小 | 检查 `.log` 中 `! Error` — 大概率 `Division by 0`（图片问题） |
| 图片显示 [⛔ 缺图] | 检查 `11-模板/scripts/.chem_media/` 有没有该文件，文件头是否有效 |
| 文字变成 `(r,,)` | Unicode 希腊字母 θ φ 在 text mode 丢失 — `preprint()` 中 `fix_caption_greek` 没覆盖到 |
| 出现 `****` 格式垃圾 | emoji 替换顺序问题 — `⭐` 的删除必须在例题 `]` 清理之后 |
| PDF 目录太深 | 典型例题/练习题下的 `###` 三级标题由 `preprint()` 自动降级为加粗文本 |
| 公式溢出边界 | 检查 `Overfull \hbox` 警告个数，调整图片 width 或表格列宽 |

---

## 一、管线总览

```
Atom.md (Obsidian源文件)
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ convert_handout_to_pdf.py (Python)                   │
│                                                      │
│ Phase 1: preprint()                                  │
│  输入: .md                                           │
│  输出: _preprocessed.md                              │
│  操作:                                                │
│    · 剥 YAML frontmatter（--- ... ---）               │
│    · 剥元数据引用块（> **适用**: 等）保留教学 callout │
│    · Unicode下标→数字（₂→2, ₃→3）                   │
│    · ![[media/xxx]] → ![](media/xxx)                 │
│    · [[wikilink]] → 纯文本                           │
│    · 去 <center>/<br>/<sup>/<sub>                    │
│    · 去 ```dataview/dataviewjs 块                     │
│    · 去 \mathrm{...}（防 LaTeX 外出错）              │
│    · 去 来源行（**来源**:, *来源*, 来源于等）        │
│    · 去 --- 分隔线                                    │
│                                                      │
│ Phase 2: Pandoc MD→LaTeX                              │
│  输入: _preprocessed.md                              │
│  输出: _handout_body.tex                              │
│  filter: wrap_images.lua                              │
│  关键参数:                                            │
│    --from=markdown+tex_math_dollars+raw_tex+pipe_tables+grid_tables │
│    --to=latex                                         │
│    --lua-filter=wrap_images.lua                       │
│    --wrap=preserve                                    │
│                                                      │
│ Phase 3: 拼接完整文档                                  │
│  输入: _handout_body.tex + chemistry-preamble.tex     │
│  输出: _handout.tex                                   │
│  操作:                                                │
│    · 读取 preamble 模板文件                           │
│    · 插入 \graphicspath                               │
│    · 插入 \title / \maketitle / \tableofcontents      │
│    · 拼接 body                                        │
│    · 后处理：                                         │
│      - 去 \pandocbounded{}                             │
│      - 去 {media/ 前缀                                 │
│      - .md} → .png} (Excalidraw源文件→渲染图)         │
│      - 中文明→ASCII别名                               │
│      - 缺图检查 → [⛔ 缺图: xxx]                      │
│      - 表格压缩 \small + \tabcolsep=3.5pt             │
│                                                      │
│ Phase 4: xelatex 两遍编译                              │
│  输入: _handout.tex                                   │
│  输出: _handout.pdf                                   │
│  操作: pass1 (正常) → pass2 (更新目录/引用)           │
│  回退: 如果 pass2 失败, 用 pass1 的输出               │
│                                                      │
└─────────────────────────────────────────────────────┘
    │
    ▼
_Final.pdf (输出到 00-首页/学生讲义PDF/)
```

## 二、各文件职责

### 11-模板/scripts/chemistry-preamble.tex
LaTeX 导言区模板（当前版本 v4），包含：
- 文档类: `ctexart`（中文支持）
- 化学: `mhchem`（\ce{H2O}）
- 数学: `amsmath`, `amssymb`, `breqn`（自动换行长公式）, `mathtools`
- 图片: `graphicx` + `float`（支持 [H]）
- 表格: `booktabs`, `xltabular`（longtable + tabularx 合并）, `array`
- 颜色: `xcolor`（\definecolor 自定义浅底色）
- 页面: `geometry`（A4, 2.2cm边距）, `fancyhdr`（页眉蓝色细线+章节名）
- 超链接: `hyperref`（linkcolor=black 无红框）
- 提示框: 4 个 colorbox 环境（浅底色，无 tcolorbox，兼容 dvipdfmx）
- 列表间距: `enumitem` + `\setlist{nosep}`
- 溢出控制: `microtype`, `\sloppy`, `\emergencystretch`
- 代码: `listings`
- 图片尺寸: `\AtBeginDocument{\setkeys{Gin}{width=\textwidth,keepaspectratio}}`
- 防跨节浮动: `placeins`

### 11-模板/scripts/wrap_images.lua
Pandoc Lua filter，在 AST 层做：
- 检测 `Para` 节点是否包含 `Image`
- 如果是纯图片段落 → 替换为 `\begin{figure}[H]\centering\includegraphics{...}\end{figure}`
- 如果图片后跟 `Emph`（*图注*）→ 加入 `\caption{}`
- 使用 `[H]`（不是 `[h!]`）强制图片在当前文本位置

### 11-模板/scripts/convert_handout_to_pdf.py
Python 调度器，关键参数：
- `PANDOC`: pandoc.exe 路径
- `XELATEX`: xelatex.exe 路径  
- `_CHEM_MEDIA`: 图片缓存目录（`11-模板/scripts/.chem_media/`）
- `LUA_FILTER`: wrap_images.lua
- `PREAMBLE_FILE`: chemistry-preamble.tex

### 11-模板/scripts/.chem_media/
图片缓存目录。所有根目录 `media/` 下的真实图片会同步到此目录。
使用 workspace-local 路径，避免受限环境下向 `C:\Temp` 写入失败。

## 三、关键决策理由

| 决策 | 原因 | 可选方案 |
|:---|---|:---|
| 不用 tcolorbox | tcolorbox + dvipdfmx 冲突导致图片无法加载 | ← 当前方案 |
| 用文本提示框替代 | 无宏包依赖，稳定 | tcolorbox（已放弃）|
| [H] 替代 [h!] | [h!] 空间不足时仍会浮动；[H] 完全强制 | [h!]+FloatBarrier（不够彻底）|
| graphicspath 用 workspace-local 缓存 | 避开外部 temp 目录权限问题，同时保留“编译副本”隔离层 | 外部 temp 缓存方案 |
| Pandoc Lua filter 包裹图片 | 在 AST 层操作，不受 Markdown 语法变化影响 | Python 后处理 regex（易出错）|
| 源文件不改 | 保持 Obsidian 知识库的浏览体验 | 修改源文件（当前方向）|
| preprocessing 图片引用不改源 | 图片路径问题应在管线层解决，避免污染源 MD | —— |

## 四、血泪教训（2026-06-28 新增）

> 以下教训记录在此次 PDF 管线调试中踩过的坑，**必须在后续所有管道改动前阅读**。

### ❌ 教训 1：永远不修改源 .md 文件
**事件**：为修复图片大小问题，把源 MD 中的 `![[media/s.jpg]]` 替换成了 `![[media/11-13-orbital-shapes-s-p-d.jpg]]`。
**后果**：用户发现自己的正确图片引用被覆盖，非常不满。
**原则**：管线只能处理**预处理副本**（`_pre_xxx.md`），源 `xxx.md` 不可以写。所有格式修复（图片大小、转义、对齐等）都在管线后处理阶段做。

### ❌ 教训 2：别名映射 SVG→JPG 会摧毁图片
**事件**：`chem_media_aliases.json` 中 `"构造原理-填充顺序.svg": "aufbau.jpg"` 
**后果**：别名声明的同步操作把 SVG 文本内容写入 `aufbau.jpg`，xelatex 遇到伪 JPG 报 `Division by 0`→PDF 损坏。
**修复**：
- 管线加图片格式签名检测（检查每个 JPG 文件头是否为 `FFD8`，PNG 是否为 `89504E47`）
- 移除了别名中的 SVG 映射
- 所有 SVG 在 `chem_media` 中自动转 PNG（用 cairosvg，不可用时跳过）

### ❌ 教训 3：`\pandocbounded{}` 括号残留
**事件**：`full_tex.replace('\\pandocbounded{', '')` 只剥左括号不剥右括号。
**后果**：`\pandocbounded{\includegraphics{img.jpg}}` → `\includegraphics{img.jpg}}` → `Extra }` 错误。
**修复**：加后处理 regex：`re.sub(r'(\\includegraphics(?:\[[^\]]*\])?\{[^}]+\})\}', r'\1', full_tex)`

### ❌ 教训 4：JPG/PNG 文件被 YAML 污染
**事件**：`11-13-orbital-shapes-s-p-d.jpg` 和 `构造原理-填充顺序.matrix.png` 头部被写入了 YAML frontmatter（`---\ndeprecated: true...`），文件不再以 `FFD8`/`89504E47` 开头。
**后果**：xelatex 无法加载图片。文件系统尺寸正常但文件头错误。
**修复**：从 git 恢复原图。后续措施：管线图片同步阶段检查文件魔数（magic bytes），非图片格式报 `⚠️ 格式异常`。

### ❌ 教训 5：emoji 替换顺序导致 `****` 格式垃圾
**事件**：源 MD 中 `### 例1 [电子排布书写] ⭐⭐`，预处理中 `⭐→*` 在 `]→空` 之前执行。
**后果**：先变 `### 例1 [电子排布书写] **`，然后 `]` 无法匹配 ⭐ 被移除，残留 `### 例1 电子排布书写] **` → Pandoc 把 `] **` 解释为加粗。
**修复**：顺序改为 ① 清理例题 `]`（匹配 ⭐/★）→ ② 删除 ⭐★ 及所有 emoji。且 ⭐ 直接删为空（''），不转 `*`。

### ❌ 教训 6：Unicode 希腊字母在 LaTeX text mode 被丢弃
**事件**：`*图 1 ...从(x,y,z)到(r,θ,φ)：x = r sinθ cosφ...*` 中的 `θ φ` 在 lmroman 字体中没有对应字形。
**后果**：LaTeX 静默丢弃 → PDF 中显示为 `(r,,)`。
**修复**：预处理中精准替换 `*图 xxx*` caption 内的 Unicode 希腊字母为 `$\theta$` 等 LaTeX 数学模式写法。

### ❌ 教训 7：全局替换 `≤≥≠∝⇔σ` 会破坏已有 $...$ 数学模式
**事件**：试图用全局 `string.replace` 替换所有 Unicode 符号为 LaTeX 数学模式。
**后果**：`Z≤54` → `Z$\leq$54`（正常）；`$E_{3d}\propto$Z^*/r^2$` → `$E_{3d}$\propto$$Z^*/r^2$`（数学模式断裂！）
**教训**：只能在 caption 或 text mode 上下文中替换。对于已有 $...$ 包裹的内容，不做替换。

### ❌ 教训 8：stale 旧产物会制造“假成功”
**事件**：一次失败编译后，目录里仍残留旧的 `_handout_*.pdf/.log/.aux/.toc/.out`。
**后果**：后续脚本如果只检查“文件是否存在”，就可能把上一次的旧 PDF 误判成这一次的成功产物。
**修复**：每次编译前先清理同 `build_key` 对应的中间产物，再看本轮新生成的 PDF 与日志。

### ❌ 教训 9：临时产物名必须使用 ASCII build key
**事件**：中间产物直接沿用中文讲义名，进入 Pandoc / xelatex / 临时缓存链路后出现工具级波动。
**后果**：部分环境下日志、缓存命中和编译结果会变得不稳定，排障成本极高。
**修复**：统一为每本讲义生成 ASCII `build_key`，所有 `_pre_` / `_body_` / `_handout_` 产物都挂在这个 key 下。

### ❌ 教训 10：当前 Codex 的 `cmd` 链路可能误报“全挂”
**事件**：通过嵌套 `cmd /c` / batch 做批量回归时，日志出现整批 `xelatex 输出为空`。
**后果**：表面上像是 6 本全失败，但实际用 PowerShell 直接调用 Python / `convert_one()` 复核后，真实结果是 6 本里 5 本成功、1 本仅缺 2 张图。
**教训**：当前环境里，**batch 输出不是回归真相源**。遇到整批异常，先用 direct Python 复核，再下结论。

## 五、后续优化方向

### 高优先级
1. **图片魔数校验** — 在 `_CHEM_MEDIA` 同步后检查所有图片文件头的 magic bytes
2. **自动 SVG 转 PNG** — 配合 cairosvg 或 PIL 渲染
3. **预检脚本** — 在 build 前扫描 .md 中的图片引用是否在 `media/` 下存在

### 中优先级
4. **思源字体** — 替代系统宋体的更好选择
5. **ctexbook** — 支持 chapter 级标题
6. **公式溢出警告** — 收集 overfull hbox 诊断

### 低优先级
7. **封面页** — 讲义封面自定义
8. **双栏排版** — 表格密集段落
9. **代码高亮** — listings 美化

| 决策 | 原因 | 替代方案 |
|:---|---|:---|
| 不用 tcolorbox | tcolorbox + dvipdfmx 冲突导致图片无法加载 | colorbox 浅底色 ✅ |
| [H] 替代 [h!] | [H] 完全强制图片在当前位置 | [h!]+FloatBarrier（不够彻底）|
| graphicspath 用 workspace-local 缓存 | 避开外部 temp 权限问题，同时保留编译副本隔离 | 外部 temp 缓存方案 |
| Pandoc Lua filter 包裹图片 | AST 层操作，不受 Markdown 语法变化影响 | Python 后处理 regex（易出错）|
| xltabular 替代 longtable+tabularx | 跨页+自动列宽一次完成 | 两者分别用（需同步）|
| breqn 替代 amsmath 手动换行 | 长公式自动断行，不溢出 | manual split/multline |
| microtype | 字符级伸缩改善断行质量 | 无（默认LaTeX断行较差）|
| colorbox 不加边框 | 视觉清爽，无 tcolorbox | tcolorbox（冲突）|

## 六、历史补充：早期优化方向（归档）

> 以下条目保留作历史参考；当前执行优先看上方 `## 五、后续优化方向`。

### 高优先级
1. **源文件质量** — 确保图在正确段落、格式统一
2. **图片补齐** — 为缺图下载/绘制真实教材图

### 中优先级
3. **思源字体** — 安装 Source Han Serif/Sans，替代系统宋体/黑体
4. **ctexbook** — 切换到 ctexbook 文档类，支持 \chapter 级别

### 低优先级
5. **自定义标题页** — 讲义封面设计
6. **双栏布局** — 表格密集章节双栏排版
7. **列表ings 代码高亮** — 改善代码段显示

## 七、复现步骤

```bash
# 环境要求
Python 3.8+
MiKTeX (含 xelatex, 推荐 26.5+)
Pandoc 3.2+

# 安装依赖
pip install python-docx pypandoc_binary pyyaml

# 生成单本
cd 11-模板/scripts
python convert_handout_to_pdf.py "原子结构-超级充实版（自学完整）.md"

# 生成全部
python convert_handout_to_pdf.py ALL

# 图片缓存由主脚本自动同步（无需手动单独跑）
# convert_handout_to_pdf.py 会把 media/ 复制到 11-模板/scripts/.chem_media/

# 输出位置
00-首页/学生讲义PDF/xxx.pdf
```

## 八、FAQ

### Q: 为什么不用 Overleaf / 在线编辑器？
A: 源文件在本地 Obsidian 知识库中，需要本地管线。且 MiKTeX + Pandoc 本地编译比在线更快。

### Q: 模型之间的输出差异在哪里？
A: 管线是确定性的（Markdown → LaTeX → PDF），同一输入永远产生同一输出。差异只在：
- 源文件的质量（图片引用位置、例题格式、表格设计）
- 预处理阶段是否能正确处理源文件的特殊语法

### Q: 为什么图片还有错位？
A: 两个原因：① figure[H] 在页面空间不足时会跳到下一页（不可避免）；② 源文件里 `![[media/xxx]]` 的位置决定了图片出现在 PDF 的哪个章节。如果源文件把图放在了错误的段落，PDF 也会一样错。
