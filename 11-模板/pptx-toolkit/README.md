---
title: "pptx-toolkit README"
type: "系统"
updated: 2026-06-29
tags: ["系统", "PPTX", "模板"]
---

# PPT 生成工具包（pptx-toolkit）

> 位置：`11-模板/pptx-toolkit/`
>
> 本工具包用于将备课内容（Markdown）转换为含 LaTeX 公式的 PowerPoint 课件。

---

## 文件清单

| 文件 | 职责 | 修改频率 |
|:---|:---|:---:|
| `latex-render.js` | LaTeX → PNG 渲染引擎 | ❌ 不修改 |
| `ppt-engine.js` | PPT 生成引擎（html2pptx + PptxGenJS + 公式插入） | ❌ 不修改 |
| `模板-PPT生成.js` | 标准化生成脚本模板 | ✅ 每节课复制后修改 |
| `formula-cache/` | 公式 PNG 缓存目录（自动创建） | — |

---

## 快速开始

### 1. 首次安装依赖

```bash
cd pptx-workspace   # 或任意工作目录
npm install pptxgenjs katex sharp playwright
npx playwright install chromium
```

### 2. 复制模板

```bash
cp "11-模板/pptx-toolkit/模板-PPT生成.js" "04-课件/PPT/化学计量与气体-提高班.js"
```

### 3. 填写课程专属内容

编辑复制的脚本，修改三个区域：

#### 区域 A：公式注册表

```javascript
const formulas = {
    f_ideal_gas: 'pV = nRT',
    f_dalton: 'p_i = p_{\\text{总}} \\cdot x_i',
    f_molar_mass: 'M = \\rho \\dfrac{RT}{p}',
};
```

规则：
- key 以 `f_` 前缀 + 语义命名
- value 是纯 LaTeX 代码（**不要**包裹 `$` 或 `$$`）
- 支持所有 KaTeX 语法：`\\frac`, `\\sqrt`, `\\mathrm`, `\\lg` 等

#### 区域 B：幻灯片定义

```javascript
const slides = [
    // 纯文字页
    {
        type: 'html',
        html: makeHtmlSlide({ title: '标题', contentHtml: '...' })
    },

    // 带公式页
    {
        type: 'html',
        html: makeHtmlSlide({ title: '核心公式', contentHtml: '...' }),
        formulas: [
            { key: 'f_ideal_gas', x: 2, y: 0.8, h: 0.5 },
        ]
    },

    // 表格页
    {
        type: 'table',
        title: '对比表',
        tableData: [ ... ],
        tableOptions: { x: 0.5, y: 1.2, w: 9, h: 2 }
    },
];
```

公式坐标说明（PptxGenJS 使用英寸）：
- `x`: 水平位置（0 = 左边缘，10 = 右边缘）
- `y`: 垂直位置（0 = 顶部，5.625 = 底部）
- `h`: 公式图片高度（英寸），宽度自动等比缩放

#### 区域 C：输出路径

```javascript
const OUTPUT_PATH = path.join(__dirname, '化学计量与气体-提高班.pptx');
```

### 4. 运行生成

```bash
node 化学计量与气体-提高班.js
```

---

## 公式书写规范

### ✅ 正确写法

```javascript
// 化学式用 \\mathrm 包裹
'\\mathrm{[H_3O^+]} = \\sqrt{K_a \\cdot c}'

// 分式用 \\frac 或 \\dfrac
'\\frac{c}{K_a} \\geq 400'

// 对数、三角函数用 \\lg, \\ln, \\sin
'\\mathrm{pH} = \\mathrm{p}K_a + \\lg\\frac{[A^-]}{[HA]}'

// 下标用上标用 _ 和 ^
'K_{a2}, \\alpha^2, 10^{-5}'

// 文本插入公式用 \\text
'E^\\ominus = \\text{常数}'
```

### ❌ 错误写法

```javascript
// 不要包裹 $ 或 $$
'$pV = nRT$'          // ❌
'pV = nRT'            // ✅

// 不要直接用中文（部分符号不支持）
'温度 = 298K'         // ❌
'T = 298\\ \\mathrm{K}'  // ✅
```

---

## 技术细节

### 缓存机制

`latex-render.js` 使用 MD5 缓存：
- 同一 LaTeX 代码 + 同一字体大小 + 同一颜色 → 只渲染一次
- 缓存文件保存在工作目录的 `formula-cache/` 下
- 缓存可安全删除，下次运行时自动重建

### 渲染流程

```
LaTeX 字符串
    → katex.renderToString() → HTML (含 SVG)
    → 包装为 SVG (foreignObject)
    → sharp() 光栅化为 PNG (高 DPI)
    → 保存到 formula-cache/
```

### 尺寸估算

`latex-render.js` 自动估算 PNG 尺寸：
- 简单公式：`width ≈ latex.length × fontSize × 1.5`
- 复杂公式（含 frac/sqrt）：`width ≈ latex.length × fontSize × 2.5`
- 最大宽度限制 700px，防止溢出

---

## 故障排除

| 问题 | 原因 | 解决 |
|:---|:---|:---|
| `Cannot find module 'katex'` | 未安装依赖 | 运行 `npm install katex sharp` |
| Playwright 浏览器报错 | Chromium 未下载 | 运行 `npx playwright install chromium` |
| 公式图片太宽/溢出 | 公式太长或字号太大 | 减小 `fontSize` 或拆分公式 |
| 公式颜色不对 | 颜色格式错误 | 使用 `'333333'` 而非 `'#333333'` |
| 缓存不更新 | 修改了公式但 key 没变 | 删除 `formula-cache/` 目录 |

---

## 与备课内容的对应关系

```
备课大纲（04-课件/备课大纲/）
    ├── 媒介分工表 ──→ 决定哪些内容放 PPT
    │
新授课讲义（04-课件/新授课/）
    ├── 核心结论 ──→ PPT 第 2 页
    ├── 知识内容 ──→ PPT 第 3-8 页
    ├── 例题 ──────→ PPT 第 9-11 页
    ├── 易错点 ────→ PPT 第 12 页
    └── 总结 ──────→ PPT 第 13 页
```

---

*本工具包版本：v1.0 | 创建日期：2026-05-26*
