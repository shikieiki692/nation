# Obsidian 化学资料阅读配置指南

> 针对 MinerU 提取的化学竞赛资料（含大量 LaTeX 公式）优化 Obsidian 阅读体验。

---

## 一、必做：开启 Obsidian 原生公式支持

MinerU 提取的化学式大量使用 `$...$` 行内公式语法，Obsidian 默认**不渲染**单行 `$`，需要手动开启。

### 操作步骤

1. 打开 **设置（Settings）** → **编辑器（Editor）**
2. 找到 **"显示行内公式"**（Display inline math）或 **"解析 LaTeX 数学公式"**
3. **开启**该选项

> 开启后，`$\mathrm{N}_2$` 会立即渲染为 N₂，而不再是灰色代码文本。

### 验证是否生效

打开任意真题文件，找到包含 `$$` 或 `$` 的行：

- **生效**：公式变为渲染后的化学式（如下标、上标、箭头）
- **未生效**：仍显示为灰色 `\mathrm{...}` 代码

---

## 二、推荐安装的社区插件

### 1. Latex Suite（强烈推荐）

**作用**：
- 输入 `mk` 自动展开为 `$|$`（光标居中，快速输入行内公式）
- 输入 `dm` 自动展开为 `$$|$$`（块级公式）
- 提供大量常用 LaTeX 符号的缩写补全
- **可自定义化学专用 snippets**

**安装**：
1. 设置 → 社区插件 → 浏览 → 搜索 "Latex Suite"
2. 安装并启用

**针对化学竞赛的推荐配置**：

安装后，进入 **Latex Suite 设置 → Snippets**，添加以下自定义代码片段：

```json
[
    // 快速输入行内化学式
    {
        "trigger": "chem",
        "replacement": "\\mathrm{$0}",
        "options": "mA",
        "description": "化学正体"
    },
    // 快速输入反应箭头
    {
        "trigger": "ra",
        "replacement": "\\rightarrow",
        "options": "mA",
        "description": "反应箭头"
    },
    // 快速输入可逆箭头
    {
        "trigger": "eq",
        "replacement": "\\rightleftharpoons",
        "options": "mA",
        "description": "可逆箭头"
    },
    // 快速输入 Delta（焓变等）
    {
        "trigger": "dd",
        "replacement": "\\Delta",
        "options": "mA",
        "description": "Delta符号"
    },
    // 快速输入温度上标
    {
        "trigger": "deg",
        "replacement": "^{\\circ}",
        "options": "mA",
        "description": "度符号"
    },
    // 快速输入标准态圆圈
    {
        "trigger": "std",
        "replacement": "^{\\ominus}",
        "options": "mA",
        "description": "标准态符号"
    }
]
```

> 将上述 JSON 添加到 Latex Suite 的 Snippets 设置中，即可在公式内使用缩写快速输入。

---

### 2. Math Booster（原 Math+）

**作用**：
- 为公式添加编号和引用功能
- 在笔记中快速跳转公式定义
- 改善长公式的阅读体验（适合教材中的推导过程）

**安装**：
1. 设置 → 社区插件 → 浏览 → 搜索 "Math Booster"
2. 安装并启用

**推荐设置**：
- 开启 **"自动编号"**（Auto-numbering）：教材中的公式会自动编号
- 开启 **"公式提示"**（Equation popover）：鼠标悬停在引用上可预览公式

---

### 3. Hider（可选）

**作用**：隐藏 Obsidian 的 UI 元素（标题栏、工具栏等），最大化阅读空间。

适合长时间阅读真题解析和教材时使用。

---

## 三、Obsidian 外观优化建议

### 1. 更换适合代码/公式的字体

设置 → 外观 → 字体：

- **等宽字体（Monospace）**：推荐 `JetBrains Mono` 或 `Fira Code`
  - 这些字体对 `$`、`_`、`^` 等 LaTeX 符号的显示更清晰
- **正文字体**：推荐 `思源宋体` 或 `Noto Serif CJK SC`（中文阅读舒适）

### 2. 行宽设置

化学式较长时，默认行宽可能导致公式换行混乱：

- 设置 → 外观 → **可读行宽（Readable line length）**
- 建议**关闭**或调宽，让长公式在一行内显示完整

### 3. 主题推荐

- **默认主题**：公式渲染最稳定
- **Minimal Theme**：简洁，公式显示清晰
- **Things Theme**：代码块和公式区分明显

避免使用过度装饰的主题，可能干扰公式渲染。

---

## 四、阅读技巧

### 1. 快速定位公式

在 Obsidian 搜索框输入 `$` 可以搜索所有包含公式的段落。

### 2. 编辑模式 vs 阅读模式

- **编辑模式（Edit）**：显示原始 LaTeX 代码，方便复制修改
- **阅读模式（Reading）**：渲染后的公式，适合阅读

按 `Ctrl/Cmd + E` 快速切换。

### 3. 公式过长时的处理

MinerU 提取的部分块级公式（`$$...$$`）可能一行很长，在 Obsidian 中会自动换行。如果渲染异常，可以手动在适当位置加换行：

```latex
$$
\begin{array}{l}
\mathrm{CH}_4(g) + \mathrm{H}_2\mathrm{O}(g) \\
\longrightarrow \mathrm{CO}(g) + 3\mathrm{H}_2(g)
\end{array}
$$
```

---

## 五、常见问题 FAQ

### Q1：为什么有些公式还是显示为灰色代码？

**原因**：
- 行内公式用了单个 `$`，但 Obsidian 设置中未开启"显示行内公式"
- 公式语法本身有错误（如括号不匹配）

**解决**：按"必做"步骤开启设置。

---

### Q2：`$$` 块级公式和 `$` 行内公式有什么区别？

| 语法 | 用途 | 示例 |
|:---|:---|:---|
| `$...$` | 行内公式，嵌入段落中 | 水中溶解了 `$\mathrm{O}_2$` |
| `$$...$$` | 块级公式，独立居中 | 化学平衡方程式 |

MinerU 提取的资料中两种都有使用。

---

### Q3：Latex Suite 会干扰正常打字吗？

**默认会**，因为它自带很多缩写（如输入 `a` 可能展开为 `\alpha`）。

**建议**：在 Latex Suite 设置中：
1. 开启 **"仅在数学模式触发"**（Trigger only in math mode）
2. 或删除不常用的默认 snippets，只保留你需要的

这样只有在 `$...$` 内部才会触发自动补全，不影响正常中文输入。

---

### Q4：手机/平板端也能正常看吗？

**可以**，但需确保：
- Obsidian 移动端同样开启了"显示行内公式"
- 社区插件（如 Latex Suite）需要在桌面端安装后会同步到移动端（Obsidian Sync 用户）
- 无 Sync 的用户需要在移动端重新安装插件

---

## 六、快速检查清单

安装配置完成后，逐项确认：

- [ ] 设置 → 编辑器 → **显示行内公式** 已开启
- [ ] 社区插件 **Latex Suite** 已安装并启用
- [ ] Latex Suite 中添加了化学专用 snippets（可选）
- [ ] 社区插件 **Math Booster** 已安装（可选）
- [ ] 打开 `01-真题/第28届中国化学奥林匹克初赛试题.md`，确认 `$\mathrm{N}_2$` 渲染为 N₂
- [ ] 打开 `03-教材书籍/普通化学原理（第4版）/index.md`，确认行间公式正常显示

---

*配置完成！享受流畅的化学资料阅读体验吧。*
