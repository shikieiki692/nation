# LaTeX PDF 生成策略文档

> 目的：记录当前 LaTeX 管线的完整流程、各步骤职责、关键决策原因，便于后续优化和他人接手。

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
_Final.pdf (输出到 04-课件/学生讲义/)
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
- `_CHEM_MEDIA`: ASCII 图片目录（C:/Temp/chem_media/）
- `LUA_FILTER`: wrap_images.lua
- `PREAMBLE_FILE`: chemistry-preamble.tex

### C:\Temp\chem_media\
图片缓存目录。所有 media/ 下的真实图片会同步到此目录。
必须是纯 ASCII 路径（无中文字符），否则 dvipdfmx 无法加载。

## 三、关键决策理由

| 决策 | 原因 | 可选方案 |
|:---|---|:---|
| 不用 tcolorbox | tcolorbox + dvipdfmx 冲突导致图片无法加载 | ← 当前方案 |
| 用文本提示框替代 | 无宏包依赖，稳定 | tcolorbox（已放弃）|
| [H] 替代 [h!] | [h!] 空间不足时仍会浮动；[H] 完全强制 | [h!]+FloatBarrier（不够彻底）|
| graphicspath 用 ASCII 路径 | dvipdfmx 不认含中文的路径 | 临时目录 C:\Temp\chem_media |
| Pandoc Lua filter 包裹图片 | 在 AST 层操作，不受 Markdown 语法变化影响 | Python 后处理 regex（易出错）|
| 源文件不改 | 保持 Obsidian 知识库的浏览体验 | 修改源文件（当前方向）|

## 四、当前瓶颈

1. **源文件图片位置不对** — `![[media/xxx]]` 放在源文件的哪个段落，PDF 里就在哪个位置附近。如果源文件把图放在了不相关的段落，PDF 里也会一样错。
2. **源文件缺图片文件** — 引用的图片路径在 `media/` 下不存在，导致 [⛔ 缺图] 标记。
3. **长公式溢出** — 已用 `breqn` 缓解。
4. **例题格式不一致** — 源文件里有些例题有 "**题目**"→"**答案**" 结构，有些只有 "**答案**"。
5. **断链检测** — `[[wikilink]]` 在预处理中被转为纯文本，但引用目标可能不存在。

## 五、关键决策理由（v4）

| 决策 | 原因 | 替代方案 |
|:---|---|:---|
| 不用 tcolorbox | tcolorbox + dvipdfmx 冲突导致图片无法加载 | colorbox 浅底色 ✅ |
| [H] 替代 [h!] | [H] 完全强制图片在当前位置 | [h!]+FloatBarrier（不够彻底）|
| graphicspath 用 ASCII 路径 | dvipdfmx 不认含中文的路径 | C:\Temp\chem_media |
| Pandoc Lua filter 包裹图片 | AST 层操作，不受 Markdown 语法变化影响 | Python 后处理 regex（易出错）|
| xltabular 替代 longtable+tabularx | 跨页+自动列宽一次完成 | 两者分别用（需同步）|
| breqn 替代 amsmath 手动换行 | 长公式自动断行，不溢出 | manual split/multline |
| microtype | 字符级伸缩改善断行质量 | 无（默认LaTeX断行较差）|
| colorbox 不加边框 | 视觉清爽，无 tcolorbox | tcolorbox（冲突）|

## 六、后续优化方向

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

## 六、复现步骤

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

# 图片同步（media → C:\Temp\chem_media）
python sync_media_to_temp.py

# 输出位置
04-课件/学生讲义/xxx.pdf
```

## 七、FAQ

### Q: 为什么不用 Overleaf / 在线编辑器？
A: 源文件在本地 Obsidian 知识库中，需要本地管线。且 MiKTeX + Pandoc 本地编译比在线更快。

### Q: 模型之间的输出差异在哪里？
A: 管线是确定性的（Markdown → LaTeX → PDF），同一输入永远产生同一输出。差异只在：
- 源文件的质量（图片引用位置、例题格式、表格设计）
- 预处理阶段是否能正确处理源文件的特殊语法

### Q: 为什么图片还有错位？
A: 两个原因：① figure[H] 在页面空间不足时会跳到下一页（不可避免）；② 源文件里 `![[media/xxx]]` 的位置决定了图片出现在 PDF 的哪个章节。如果源文件把图放在了错误的段落，PDF 也会一样错。
