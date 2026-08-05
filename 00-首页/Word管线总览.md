---
title: Word管线总览
aliases:
  - Word 讲义管线总览
  - Word讲义生成总览
type: 系统
role: Word讲义入口说明
purpose: 统一说明学生讲义 Markdown 到 Word 成品的当前主链路、依赖、脚本、目录和使用方式
version: v1.0
created: 2026-07-03
updated: 2026-08-04
related:
  - "[[00-首页/Word友好 Markdown 符号速查表]]"
  - "[[11-模板/MD通用规范（Word-PDF共同最优子集）]]"
  - "[[11-模板/MD讲义格式参考（原子结构样板）]]"
  - "[[11-模板/scripts/WORD_PIPELINE_OPTIMIZATION_V1]]"
  - "[[11-模板/scripts/build-all-handout-docx.py]]"
  - "[[11-模板/scripts/docx_utils.py]]"
---

# Word 管线总览

> **定位**：这是一页 Word 讲义主链路总入口。  
> **用途**：回答 3 个问题:
> 1. Word 管线现在到底由哪些文件组成；
> 2. 哪些是主链路，哪些只是辅助脚本；
> 3. agent 真正要生成 Word 时，应该先看什么、跑什么、检查什么。

## 一、当前主流程

```text
学生讲义 Markdown
  -> 源稿预处理
  -> Pandoc 转 docx
  -> python-docx 后处理
  -> 输出到 00-首页/学生讲义Word
  -> 可选渲染预览
```

按当前实现，Word 主管线的真实结构是：

1. 预处理：
   - 剥离 frontmatter
   - 处理 Obsidian wikilink / image embed
   - 做 Word 公式预检
   - 处理 Mermaid / 图片引用 / 部分兼容写法
2. Pandoc 转换：
   - `Markdown -> docx`
   - LaTeX 数学模式转为 Word 可编辑公式对象
3. 后处理：
   - 统一字体
   - 统一段落、标题、图注、表格风格
   - 修正文档细节
4. 可选视觉质检：
   - 渲染 docx 页面预览
   - 用于检查图、表、分页、标题和公式的实际显示

## 二、输入 / 输出 / 资源目录

### 1. 源稿目录

- `04-课件/学生讲义/`

这里放讲义源 Markdown，是 Word 管线默认扫描的输入目录。

### 2. 正式输出目录

- `00-首页/学生讲义Word/`

这是当前 Word 成品的正式输出位置。  
如果不额外指定输出目录，主管线默认把 `.docx` 输出到这里。

### 3. 图片根目录

- `媒体仓库/`（物理仓，哈希原名）

当前 Word 管线的正式图片根路径是 `媒体仓库/`（v3，2026-08-04）。  
讲义源稿里的正式图片写法应统一为：

```md
![[<物理哈希名>.jpg]]
```

- 新图一律以内容 SHA-256 哈希名落入 `媒体仓库/`，引用写 `![[哈希名.jpg]]`，禁止路径前缀。
- 历史 `media/`（根目录）引用 `![[media/xxx.jpg]]` 仍被管线兼容解析（经 VAULT_ROOT），但不再新增。
- 不要用英文别名、不要加 `mineru/` 前缀。

### 4. 脚本目录

- `11-模板/scripts/`

Word / PDF 两条生成链路都在这里，但不是这里的所有文件都属于 Word 主链路。

## 三、Word 主链路核心文件

### 1. 主管线入口

- `11-模板/scripts/build-all-handout-docx.py`

这是当前 Word 管线最核心的入口脚本，负责：

- 扫描 `04-课件/学生讲义`
- 跑 Word 源稿预检
- 预处理 Markdown
- 调用 Pandoc 生成 `.docx`
- 处理资源路径和图片解析
- 调用后处理统一版式
- 可选触发渲染预览

当前它定义的关键目录口径是：

- `HANDOUT_SRC = 04-课件/学生讲义`
- `HANDOUT_OUT = 00-首页/学生讲义Word`
- `VAULT_MEDIA = 媒体仓库`

### 2. Word 后处理风格库

- `11-模板/scripts/docx_utils.py`

这是 Word 输出共享风格库，负责：

- 中文正文、标题、图注、西文的字体口径
- 段落和页面基础设置
- 表格、图片、图注等后处理修正
- Pandoc 产出的 docx 风格收口

当前字体总原则已经明确：

- 中文正文：`SimSun`
- 中文标题 / 表头：`SimHei`
- 图注：`FangSong`
- 英文、数字、变量、一般符号：`Times New Roman`

### 3. Word 参考模板

- `11-模板/scripts/templates/custom-reference.docx`

这是 Pandoc 使用的 Word 参考模板。  
它决定了基础样式、页边距、标题层级等默认格式，是“模板层控制”的核心文件。

### 4. 参考模板生成脚本

- `11-模板/scripts/create_reference_docx.py`

作用是重建或维护 `custom-reference.docx`。  
它不一定在每次生成都直接运行，但属于 Word 管线模板层的重要维护脚本。

## 四、预检、验证与渲染预览

### 1. Word 公式预检

入口仍在：

- `11-模板/scripts/build-all-handout-docx.py`

当前预检器会在正式生成前检查高风险写法，例如：

- 半截 math
- 裸下划线公式
- Mermaid 残留
- 高风险符号 / 宏残留

可以单独运行：

```bash
python 11-模板/scripts/build-all-handout-docx.py --precheck-only
```

### 2. 生成后验证

主管线本身还会做输出文档层面的基础验证，用来减少“生成成功但成品明显坏掉”的情况。

### 3. Windows 渲染预览核心脚本

- `11-模板/scripts/render_docx_windows.py`

作用：

- 调 LibreOffice 把 `.docx` 转成 `.pdf`
- 再把 `.pdf` 栅格化成页面 PNG
- 用于视觉质检

它是一个可选 QA 辅助脚本，不是生成 `.docx` 的必需步骤，但非常适合检查：

- 图片是否过大
- 表格是否炸版
- 公式是否掉行
- 分页是否难看

### 4. Windows 预览包装脚本

- `11-模板/scripts/render-docx.ps1`
- `11-模板/scripts/render-docx.cmd`

这两个是渲染预览的调用包装层。  
`render-docx.ps1` 会把预览输出到默认的：

- `<docx同目录>/<文件名>_render/`

如果启用 `EmitPdf`，也会把中间 PDF 保留下来。

## 五、图片与资源转换辅助脚本

这些文件不一定每次都直接参与生成，但属于 Word 管线常见辅助件：

### 1. Excalidraw 转 PNG

- `11-模板/scripts/excalidraw-to-png.mjs`

当讲义素材是 Excalidraw 图时，用它转成 Word 更稳定的 PNG。

### 2. SVG 转 PNG

- `11-模板/scripts/svg-to-png.mjs`

当素材是 SVG 而 Word 兼容性不稳定时，用它落成 PNG。

### 3. 图片引用清理

- `11-模板/scripts/fix_image_refs.py`

这是图片引用修复辅助脚本，偏清洗用途，不是日常主入口。

## 六、与 Word 源稿直接相关的规范文档

agent 在生成或修改讲义前，建议按这个顺序看：

### 1. 共同源稿规范

- `11-模板/MD通用规范（Word-PDF共同最优子集）.md`

这是最重要的总规范，决定 Word / PDF 共用的源 Markdown 该怎么写。

### 2. Word 公式与符号速查

- `00-首页/Word友好 Markdown 符号速查表.md`

这是最实用的快速避坑页，尤其适合处理：

- Unicode 还是 math
- 上下标怎么写
- 哪些写法会把 Word 公式炸掉

### 3. 整份讲义结构样板

- `11-模板/MD讲义格式参考（原子结构样板）.md`

这是完整讲义结构模板，用来对齐章节组织、例题位置、图表摆法和整体风格。

### 4. Word 管线优化说明

- `11-模板/scripts/WORD_PIPELINE_OPTIMIZATION_V1.md`

这份文档偏“设计和优化路线”，不是日常写稿入口，但适合维护管线时看。

## 七、当前常用运行方式

### 1. 全量生成

```bash
python 11-模板/scripts/build-all-handout-docx.py
```

### 2. 仅看将处理哪些文件

```bash
python 11-模板/scripts/build-all-handout-docx.py --dry-run
```

### 3. 仅跑 Word 预检

```bash
python 11-模板/scripts/build-all-handout-docx.py --precheck-only
```

### 4. 单文件生成

```bash
python 11-模板/scripts/build-all-handout-docx.py --file 原子结构
```

### 5. 单文件详细日志

```bash
python 11-模板/scripts/build-all-handout-docx.py --file 原子结构 -v
```

### 6. 带渲染预览生成

```bash
python 11-模板/scripts/build-all-handout-docx.py --file 原子结构 --render-preview
```

### 7. 手动渲染某个 docx

```powershell
powershell -File 11-模板/scripts/render-docx.ps1 "00-首页/学生讲义Word/原子结构-超级充实版（自学完整）.docx"
```

## 八、当前脚本参数层面涉及的功能

当前主管线脚本已支持这些常用参数：

- `--dry-run`
- `--precheck-only`
- `--file`
- `--path`
- `--output-dir`
- `--parallel`
- `--render-preview`
- `--render-output-dir`
- `--emit-render-pdf`

理解上可以分成三类：

- 生成控制：`--file`、`--path`、`--parallel`
- 质量控制：`--precheck-only`、`--render-preview`
- 输出控制：`--output-dir`、`--render-output-dir`、`--emit-render-pdf`

## 九、依赖项

### 1. 主管线依赖

根据当前脚本头部说明，Word 主管线依赖：

- `python-docx`
- `PyYAML`
- `pypandoc`
- `pandoc 3.9+`

### 2. 渲染预览依赖

如果要跑视觉预览，还需要：

- `LibreOffice`
- `pypdfium2`

### 3. 辅助资源转换依赖

如果要处理 Excalidraw / SVG 转 PNG，还会涉及 Node 侧辅助脚本。

## 十、哪些文件属于“当前真的在用”

当前 Word 管线真正应优先关注的是这组：

- `11-模板/scripts/build-all-handout-docx.py`
- `11-模板/scripts/docx_utils.py`
- `11-模板/scripts/templates/custom-reference.docx`
- `11-模板/scripts/create_reference_docx.py`
- `11-模板/scripts/render_docx_windows.py`
- `11-模板/scripts/render-docx.ps1`
- `11-模板/scripts/render-docx.cmd`
- `11-模板/MD通用规范（Word-PDF共同最优子集）.md`
- `00-首页/Word友好 Markdown 符号速查表.md`
- `11-模板/MD讲义格式参考（原子结构样板）.md`

## 十一、哪些文件只是辅助 / 维护 / 清洗

这类文件可能有用，但不是 Word 日常主入口：

- `11-模板/scripts/excalidraw-to-png.mjs`
- `11-模板/scripts/svg-to-png.mjs`
- `11-模板/scripts/fix_image_refs.py`
- `11-模板/scripts/WORD_PIPELINE_OPTIMIZATION_V1.md`

## 十二、哪些文件在同目录里，但不是 Word 主链路

下面这些是邻近文件，容易和 Word 管线混淆，但不属于当前 Word 主管线：

- `11-模板/scripts/convert_handout_to_pdf.py`
- `11-模板/scripts/pandoc-latex-template.tex`
- `11-模板/scripts/pdf_preflight.py`
- `11-模板/scripts/LATEX_STRATEGY.md`
- `11-模板/scripts/WORKFLOW-讲义PDF生产工作流.md`

也就是说：

- 要生成 Word，先看本页和 Word 规范；
- 要生成 PDF，再去走 LaTeX / PDF 那一套说明；
- 不要因为它们都在 `11-模板/scripts/` 里，就把两条链路混成一条。

## 十三、给 Agent 的最短执行顺序

如果目标是“修改讲义并生成 Word”，建议最短顺序固定为：

1. 先读 `11-模板/MD通用规范（Word-PDF共同最优子集）.md`
2. 再读 `00-首页/Word友好 Markdown 符号速查表.md`
3. 需要整体结构样板时，再读 `11-模板/MD讲义格式参考（原子结构样板）.md`
4. 修改 `04-课件/学生讲义/*.md`
5. 运行 `build-all-handout-docx.py --precheck-only`
6. 通过后正式生成 `.docx`
7. 对重要讲义追加 `--render-preview` 做视觉复核

## 十四、一句话结论

当前 Word 管线已经收成一条比较清晰的主链路：

- 源稿入口：`04-课件/学生讲义`
- 图片入口：`媒体仓库`（哈希原名）
- 生成入口：`build-all-handout-docx.py`
- 样式核心：`custom-reference.docx` + `docx_utils.py`
- 输出目录：`00-首页/学生讲义Word`
- 规范入口：`MD通用规范` + `Word友好 Markdown 符号速查表`

后续如果还要继续优化，优先级仍然是：

1. 源稿规范统一
2. 预检更稳
3. 模板样式更强
4. 渲染预览更方便
