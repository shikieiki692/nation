---
title: Word管线图片路径规范
type: 方法论
role: 技术规范
tags: [化竞, 方法论, Word管线, 图片]
created: 2026-07-15
---

# Word管线图片路径规范

> **用法**：在Markdown文件中嵌入图片时，参照此规范选择路径格式。
> **配套文档**：[[exercise-build-workflow]] · [[错误模式知识库]]

---

## 一、支持的图片路径模式

Word管线（`build-all-handout-docx.py`）支持以下图片嵌入格式：

### 1.1 标准media目录
```markdown
> **结构参考**：
> 八面体场d轨道分裂: ![[media/octahedral-d-orbital-splitting.jpg]]
```
- **路径**：`media/` 目录（与Markdown文件同级或在vault根目录）
- **用途**：手绘/编辑的示意图
- **命名**：英文描述性名称，如 `square-planar-splitting-textbook.jpg`

### 1.2 mineru OCR图片
```markdown
> **结构参考**：
> PtCl₄²⁻结构: ![[mineru/02-真题解析/ptcl4-structure.jpg]]
```
- **路径**：`mineru/` 目录（OCR扫描结果）
- **用途**：从教辅/真题中OCR提取的图表
- **注意**：OCR结果可能有误，需要人工校验

### 1.3 外部导入资料
```markdown
> **结构参考**：
> 晶胞示意图: ![[06-外部资料导入/crystal-unit-cell.png]]
```
- **路径**：`06-外部资料导入/` 目录
- **用途**：从外部PDF/图片导入的资料

---

## 二、管线处理流程

### 2.1 图片保留逻辑
`_strip_non_image_wikilink_lines()` 函数负责在Word清稿中保留图片：

```python
def _strip_non_image_wikilink_lines(text: str) -> str:
    """Remove non-image knowledge-base link lines from a Word clean copy."""
    kept_lines: list[str] = []
    for line in text.splitlines():
        if "[[" in line and "! [[" not in line:
            continue
        kept_lines.append(line)
    return "\n".join(kept_lines)
```

**关键逻辑**：
- ✅ 保留：任何包含 `![[` 的行（图片嵌入）
- ❌ 移除：包含 `[[` 但不包含 `![[` 的行（wiki链接）

### 2.2 图片路径解析
Pandoc通过 `--resource-path` 参数解析图片路径，搜索顺序：
1. Markdown文件所在目录
2. 文件所在目录的 `media/` 子目录
3. Vault根目录
4. Vault根目录的 `media/` 目录
5. 输出目录

### 2.3 图片格式转换
管线自动处理以下格式：
- `![[file.excalidraw]]` → 渲染为PNG后嵌入
- `![[file.svg]]` → 转换为PNG后嵌入
- `![[file.md]]` → 查找对应PNG后嵌入
- `![[file.png]]` / `![[file.jpg]]` → 直接嵌入

---

## 三、常见错误与修复

### 3.1 图片丢失（已修复）
**问题**：Word清稿中图片全部丢失
**根因**：旧版代码只检查 `![[media/` 前缀，漏掉 `![[mineru/` 和 `![[06-外部资料导入/`
**修复**：改为检查所有 `![[` 前缀
**状态**：✅ 2026-07-15 已修复

### 3.2 图片路径不存在
**问题**：Pandoc报错 "Could not find image"
**根因**：图片文件路径错误或文件不存在
**修复**：检查图片文件是否在正确位置，路径是否正确

### 3.3 图片格式不支持
**问题**：某些图片格式无法嵌入
**根因**：Pandoc不支持某些图片格式（如WebP）
**修复**：转换为PNG/JPG格式

---

## 四、最佳实践

### 4.1 文件命名
- ✅ 使用英文命名：`octahedral-d-orbital-splitting.jpg`
- ❌ 避免中文命名：`八面体场分裂.jpg`（可能有编码问题）

### 4.2 图片尺寸
- 建议宽度：800-1200px
- 建议格式：JPG（照片）或 PNG（图表）
- 文件大小：单张≤2MB

### 4.3 嵌入格式
- 在 `> **结构参考**：` 块引用中嵌入
- 图片前加描述文字：`> 八面体场d轨道分裂: ![[media/...]]`
- 多张图片连续排列

### 4.4 路径选择
| 场景 | 推荐路径 |
|:---|:---|
| 手绘示意图 | `![[media/...]]` |
| OCR提取图表 | `![[mineru/...]]` |
| 外部导入资料 | `![[06-外部资料导入/...]]` |

---

*v1.0 — 2026-07-15 创建*
*记录了图片路径硬编码陷阱的修复（v1.2错误模式知识库）*
