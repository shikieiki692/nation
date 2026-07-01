---
title: "PDF生成策略-Agent一键说明"
type: "系统"
updated: 2026-06-29
tags: ["系统", "PDF", "模板"]
---

# PDF 生成策略 · 一键告知 Agent

**适用场景**：已有讲义要快速出 PDF。  
**不适用场景**：新讲义定规范、系统性重构 Markdown、批量修图片资产。那类任务先读 [[11-模板/MD到产品PDF落地方案]] 和 [[11-模板/MD讲义格式参考（原子结构样板）]]。

**一键使用时，你要做的就是：先跑 `python 11-模板/scripts/pdf_preflight.py "04-课件/学生讲义/讲义名.md"`，再跑 `python 11-模板/scripts/convert_handout_to_pdf.py "讲义名.md"`，PDF 会出现在 `00-首页/学生讲义PDF/` 下。**

> 完整策略和血泪教训见 [[11-模板/scripts/LATEX_STRATEGY.md]]

---

## 命令

```bash
# 预检
python 11-模板/scripts/pdf_preflight.py "04-课件/学生讲义/原子结构-超级充实版（自学完整）.md"

# 单本
python 11-模板/scripts/convert_handout_to_pdf.py "原子结构-超级充实版（自学完整）.md"

# 全部6本（并行3路）
python 11-模板/scripts/convert_handout_to_pdf.py ALL --parallel
```

## 输出口径

- 源 Markdown：`04-课件/学生讲义/`
- 成品 PDF：`00-首页/学生讲义PDF/`
- 学生侧 `.docx`：`06-学生侧材料/学生讲义/`

不要再把 PDF 和源 `.md` 混放在同一个目录里。

## 环境注意（2026-06-28）

- `2026-06-29` 起，`convert_handout_to_pdf.py` 会自动建立 `11-模板/scripts/.miktex-sandbox/`，并预热 MiKTeX 的 `fontconfig`
- 图片缓存已切到 `11-模板/scripts/.chem_media/`，不再依赖外部 temp 缓存
- 当前 Codex 桌面环境里，之前卡住的 `AppData\Roaming\MiKTeX\2.9` 权限问题已被这条沙箱链路绕开
- 当前 Codex 桌面环境里，嵌套 `cmd /c` / `.bat` 链路可能误报整批 `xelatex 输出为空`
- 批量回归或 `ALL` 看起来全失败时，先改用 **PowerShell 直接跑 Python** 复核，不要只看 batch 输出
- 真实结论以 PDF 产物、`_handout_*.log`、以及 `全图 OK / 缺图=N [WARN]` 统计为准

## ⛔ 三条红线（违反=事故）

1. **普通编译任务不要自动改 `04-课件/学生讲义/*.md`** — 编译和规范化是两类任务；需要改源时，单独作为“规范化任务”处理。
2. **不要在编译过程中顺手改 `media/` 路径策略** — 用户手写的 `![[media/xxx.jpg]]` 应先保留，必要修复要单独审查。
3. **别名 `chem_media_aliases.json` 不能把 `.svg` 映射为 `.jpg`/`.png`** — SVG 内容写进 JPG 文件 = PDF 损坏。

## 预检通过口径

- 出现 `error`：先修再编译。
- 只剩 `warning`：可带着说明继续编译，但要在交付前确认是否需要回到规范化任务处理。
- bare image ref（如 `![[foo.png]]`）已不再属于 warning；预检会直接报错，必须改成 `![[media/foo.png]]`。

## 常见排障（简版）

| 问题 | 查什么 |
|:---|---|
| PDF 很小/几页 | `_handout_xxx.log` 看 `! Error` |
| 缺图 | 先看根目录 `media/` 是否有源图，再看 `11-模板/scripts/.chem_media/` 是否同步成功 |
| MiKTeX 权限报错 | 先确认是否是直接跑 `convert_handout_to_pdf.py`，再检查 `11-模板/scripts/.miktex-sandbox/` 是否已生成 |
| `(r,,)` | Unicode 希腊字母在 text mode 丢失 |
| `****` 垃圾 | 旧版 `⭐→*` 的 emoji 替换时序错了；新稿不再使用 `⭐` |
| 目录太深 | 例题/练习题的 `###` 被管线自动降级 |

## 管线核心文件

```
11-模板/scripts/convert_handout_to_pdf.py     ← 唯一入口
11-模板/scripts/chemistry-preamble.tex         ← LaTeX 导言
11-模板/scripts/wrap_images.lua                ← Pandoc Lua filter
11-模板/scripts/chem_media_aliases.json        ← 中文↔ASCII 图片别名
11-模板/scripts/LATEX_STRATEGY.md              ← 完整策略 + 血泪教训（必读）
```

**详细流程、决策理由、13条血泪教训 → 读 [[11-模板/scripts/LATEX_STRATEGY.md]]**
