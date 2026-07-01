---
title: LaTeX PDF 管线使用手册
type: 系统
purpose: Agent 快速了解 MD→LaTeX→PDF 完整管线
version: v3.6
updated: 2026-06-29
related:
  - "[[11-模板/scripts/convert_handout_to_pdf.py]]"
  - "[[11-模板/scripts/chemistry-preamble.tex]]"
  - "[[11-模板/scripts/wrap_images.lua]]"
  - "[[11-模板/MD讲义格式参考（原子结构样板）]]"
  - "[[00-首页/状态摘要]]"
  - "[[00-首页/Agent入口文件关系说明]]"
---

# LaTeX PDF 管线使用手册

## 📋 一句话说明

将 `04-课件/学生讲义/` 下的 Markdown 讲义编译为 PDF，使用 **xelatex** 引擎，支持中文、化学式、复杂数学公式；成品统一输出到 `00-首页/学生讲义PDF/`。

## 🏗 管线架构

```
MD 源文件                           ← 在 Obsidian 中编写
  │  ![[media/xxx.png]]             ← 图片引用
  │  $...$ $$...$$                  ← 数学公式
  │  \ce{...}                        ← 化学式
  │  *图 N 文字*                     ← 图注（编号连续）
  │  > **理解要点** / > **易错提醒**   ← 教学 callout
  │  [[wikilink]]                    ← 内部链接
  ▼
preprint()                          ← convert_handout_to_pdf.py
  │  剥 YAML frontmatter
  │  剥顶部元信息引用块（仅限文件级字段）
  │  ![[media/xxx]] → ![](media/xxx)
  │  [[wikilink]] → 纯文本
  │  legacy <center>图注 → *图 ...*
  │  Unicode / 兼容下标 → 规范化后再交给 Pandoc
  ▼
Pandoc (markdown → LaTeX)           ← 含 Lua filter
  │  扩展: +tex_math_dollars+raw_tex+pipe_tables+superscript+subscript
  │  Lua filter (wrap_images.lua):
  │    → 图片 → figure[H] + \includegraphics{media/xxx}
  │    → 图注 → \caption{...}（保留 $...$ 数学）
  ▼
完整的 .tex 文件
  │  导言区 (chemistry-preamble.tex)
  │    → ctexart + xelatex + mhchem + amsmath + fancyhdr
  │  \graphicspath{{11-模板/scripts/.chem_media/}}
  │  media/ 图片先同步到 workspace-local 缓存，再解析引用
  │  缺图检查 → [⛔ 缺图: xxx]
  ▼
MiKTeX 沙箱预热
  │  workspace/.miktex-sandbox/{config,data,install}
  │  fc-conflist + hidden flags 生成 fontconfig 配置
  │  避开 AppData\Roaming\MiKTeX\2.9 写权限问题
  ▼
xelatex × 2                         ← 两次编译确保目录+引用
  │
  ▼
PDF 输出 → 写入首页侧成品目录
```

## 🔧 核心文件的职责

| 文件 | 职责 | 改动的场景 |
|:---|:---|---:|
| `convert_handout_to_pdf.py` | **主调度**：preprint→Pandoc→LaTeX拼装→xelatex→PDF验证 | 改预处理逻辑、编译参数 |
| `chemistry-preamble.tex` | **LaTeX导言区**：字体/页面/宏包/环境定义 | 加新宏包、调排版 |
| `wrap_images.lua` | **Pandoc Lua filter**：图片→figure、图注解析、callout | 改图片样式、加callout底色 |
| `chem_media_aliases.json` | **图片别名**：中文名→ASCII（旧版兼容） | 加新图片别名 |

其中 `convert_handout_to_pdf.py` 当前还负责：

- 给 MiKTeX 注入 workspace-local 用户态目录
- 预热 `fontconfig`
- 为 `xelatex` 注入 `--miktex-disable-installer --miktex-disable-maintenance --miktex-disable-diagnose`

## 🖼 图片管理（目标方案 + 当前实现）

### 存放位置

```
media/xxx.png                         ← 源图片唯一维护位置
11-模板/scripts/.chem_media/xxx.png ← 当前编译缓存（自动同步）
```

对使用者来说，**图片的唯一维护位置仍然是 vault 根目录 `media/`**。  
当前脚本在编译时会自动复制一份到 `11-模板/scripts/.chem_media/`，这是实现细节，不是新的人工维护目录。

### 引用方式

MD 中写：

```markdown
![[media/xxx.png]]

*图 N 图注文字——描述*
```

图片自动解析为 `\includegraphics{media/xxx.png}`。当前实现会先把 `media/` 下的文件同步到 `11-模板/scripts/.chem_media/`，再由 LaTeX 读取该缓存目录。

`![[foo.png]]` 这类 bare image ref 已不再接受。预检会直接报错，必须显式写成 `![[media/foo.png]]`。

### 文件名规范

- 使用英文/数字/短横线命名
- 分类前缀：`11-`（教材图）、`excalidraw-`（自绘图）、`orbital-`（轨道图）
- 避免中文、空格、特殊字符
- 支持格式：`.png`（推荐）、`.jpg`、`.jpeg`、`.svg`
- 当前实现仍保留 `chem_media_aliases.json` 用于中文名/旧文件名兼容，但 **新图尽量直接使用稳定英文名**

### 图注规范

```markdown
*图 1 图注文字——描述内容*
```

- `*图 N 文字*` 格式（用星号 `*` 包裹表示斜体）
- 编号 `N` 全文连续，从 1 开始
- 图注中可含 `$...$` 数学公式
- 不要用 `<center>` 标签
- 不要写来源标注（如"普化原理第4版"）

### 当前兼容写法

为了兼容旧讲义，当前管线仍接受以下 legacy 写法：

- `<center>图 ...</center>`：`preprint()` 会转为 `*图 ...*`
- 图注里残留来源尾注：目前能编译，但新稿应删掉
- 中文文件名图片：可通过 `chem_media_aliases.json` 过渡

这三项都属于 **兼容层**，不是推荐层。

## 📝 MD 格式要点

详见 [[MD讲义格式参考（原子结构样板）]]，核心规则：

| 元素 | 写法 |
|:---|---:|
| 图片 | `![[media/xxx.png]]` + `*图 N 文字*` |
| 行内公式 | `$E = mc^2$` |
| 显示公式 | `$$...$$` |
| 化学式 | `$\ce{...}$` |
| 简单下标 | 用 Unicode（mₛ、dₓᵧ），不用 `$m_s$` |
| 章节标题 | `## 一、` / `### 1.1` / `#### ①` |
| callout | `> **理解要点**：...` / `> **易错提醒**：...` / `> **名师点拨**：...` |
| 来源标注 | 不写 |
| `<center>` | 禁用 |

## 📌 目标规范与当前实现的边界

| 维度 | 目标规范 | 当前实现 |
|:---|:---|:---|
| 图注写法 | `*图 N ...*` | 兼容 `<center>图 ...</center>` |
| 图片维护位置 | vault 根目录 `media/` | 编译时自动同步到 `11-模板/scripts/.chem_media/` |
| 源文件修订 | 规范化任务中人工修订 | 普通编译任务不自动改源文件 |
| 图片命名 | 英文稳定名优先，不新增 `Pasted image ...` | 旧中文名通过 alias 过渡 |

## 🚀 使用方式

### 编译单本讲义

```powershell
cd 11-模板/scripts
python convert_handout_to_pdf.py "原子结构-超级充实版（自学完整）.md"
```

### 编译全部讲义

```powershell
python convert_handout_to_pdf.py ALL
```

### 并行编译

```powershell
python convert_handout_to_pdf.py --parallel ALL
```

### PDF 输出位置

编译成功后的 PDF 统一存放到首页侧目录：
```
00-首页/学生讲义PDF/原子结构-超级充实版（自学完整）.pdf
```

目录会在首次输出时由脚本自动创建。`04-课件/学生讲义/` 继续只放源 Markdown，避免源文件和成品 PDF 混在一起。

## ✅ 推荐回归流程（当前环境）

`2026-06-29` 在当前 Codex 桌面环境中已确认：

- `convert_handout_to_pdf.py` 已能在 workspace 内自动建立 `.miktex-sandbox/`，绕开 `AppData\Roaming\MiKTeX\2.9` 的权限阻塞
- 图片缓存也已切到 workspace-local `11-模板/scripts/.chem_media/`，避免 `C:\Temp` 在受限环境下写入失败
- 首次运行会自动预热 `fontconfig`，之后可直接正常跑 `xelatex`
- 嵌套 `cmd /c` / `.bat` 链路仍可能误报 `xelatex 输出为空`，即使真实 PDF 已成功生成
- `wrap_images.lua` 现支持同一段落内 2 图/3 图并排，`![[a]]　　![[b]]` 不再只吃第一张

因此建议：

1. 日常单本产出：先跑 `pdf_preflight.py`，再直接跑 `convert_handout_to_pdf.py`
2. 做完整回归或遇到 `ALL` 看起来“整批全挂”时：优先用 **PowerShell 直接跑 Python** 复核，不要只凭 batch 报错下结论
3. 最终结论以 **PDF 产物 + `_handout_*.log` + 页数/图数统计** 为准

简化口径就是：**先预检，再直跑 Python；批量异常先复核，不直接判死刑。**

## 🔍 输出验证

每次编译后管线自动输出：

```
  原子结构-超级充实版（自学完整）.md
  PDF → 原子结构-超级充实版（自学完整）.pdf  (3456KB, 24p, 11张图, 全图 OK)
```

- `KB` = 文件大小
- `p` = 页数
- `张图` = 图片数
- `全图 OK` / `缺图=N [WARN]` = 图片完整性

## 🐛 常见问题

| 问题 | 原因 | 解决 |
|:---|:---|---:|
| PDF 缺图显示 `[⛔ 缺图: xxx]` | 图片不存在于根目录 `media/`，或缓存未同步 | 先确认 `media/` 有源图，再检查 `11-模板/scripts/.chem_media/` 是否生成对应文件 |
| MiKTeX 报 `AppData\\Roaming\\MiKTeX\\2.9` 权限错误 | 没走脚本内沙箱，或沙箱未完成首次预热 | 直接通过 `convert_handout_to_pdf.py` 编译；必要时删除 `11-模板/scripts/.miktex-sandbox/` 后重试 |
| xelatex 编译超时 | 公式/表格太复杂 | 检查大表格拆行 |
| Pandoc 转换失败 | MD 语法错误，如 `$...$` 未闭合 | 检查数学公式闭合 |
| 中文显示为空白 | 字体未安装 | 确保 SimSun/SimHei 已安装 |
| Unicode 下标显示异常 | 旧版管线残留字符转换 | 确保 `preprint()` 已去掉上下标转换 |

## 📌 给 Agent 的启动指令

要生成 PDF 时：

```
1. 先读 [[11-模板/PDF生成策略-Agent一键说明]]（30秒速览）和 [[11-模板/scripts/LATEX_STRATEGY.md#⛔-红线规则（每次操作前先读）]]（红线）
2. 确认 MD 文件在 04-课件/学生讲义/ 下
3. 先运行 `python 11-模板/scripts/pdf_preflight.py "04-课件/学生讲义/讲义名.md"`
4. 若预检有 error，先修 Markdown / 图片 / frontmatter；其中 bare image ref 现在按 error 处理，不能带病编译
5. 再运行编译命令
6. 检查输出验证信息（全图/缺图）
```

> ⛔ **第一条红线**：普通“编译任务”不要边跑边自动重写 `04-课件/学生讲义/*.md` 或 `media/`。源文件修订应作为单独的“规范化任务”显式进行。
> ⛔ **第二条红线**：别名声明的 SVG→JPG 映射会毁掉 PDF，已在管线加魔数校验防护。

## 📌 管道更新与版本记录

| 版本 | 日期 | 变更 |
|:---|:---:|:---|
| v3.0 | 2026-06-28 | 图片策略全面重构："不碰源文件/不改图引用/管线层做所有事"。修复SVG别名覆盖JPG(魔数校验)、pandocbounded括号残留、emoji时序、Greek caption丢失。新增：图片格式签名检测、SVG自动转PNG、例题目录降级。详见 [[11-模板/scripts/LATEX_STRATEGY.md#四、血泪教训（2026-06-28 新增）]] |
| v3.1 | 2026-06-28 | 移除 bare image ref 兼容口径：预检改为直接报错，样板与工具层统一要求显式 `![[media/...]]`。 |
| v3.2 | 2026-06-28 | 补充可靠回归工作流：当前环境下优先用 PowerShell 直接跑 Python 复核，不只依赖嵌套 `cmd`/batch 报错；输出口径统一为 `全图 OK / 缺图=N [WARN]`。 |
| v3.3 | 2026-06-29 | 打通 MiKTeX 权限阻塞：脚本内新增 workspace-local `.miktex-sandbox/`、`fontconfig` 预热、XeLaTeX hidden flags；当前 Codex 环境已可直接成功产出 PDF。 |
| v3.4 | 2026-06-29 | 图片缓存迁回 `11-模板/scripts/.chem_media/`，修复受限环境下新图不同步导致的“假缺图”；`wrap_images.lua` 同步支持 2 图/3 图并排 figure。 |
| v3.5 | 2026-06-29 | 正式收口为单一路径：讲义源图统一迁到 vault 根目录 `media/`，主脚本不再读取历史讲义目录副本。 |
| v3.6 | 2026-06-29 | PDF 成品目录从 `04-课件/学生讲义/` 迁到 `00-首页/学生讲义PDF/`，明确拆分“源 Markdown”与“成品 PDF”两条路径。 |
