---
title: 原子结构讲义样板管线总结与质量守则
type: 系统
updated: 2026-06-29
---

# 原子结构讲义样板 · 管线总结与质量守则

## 一、管线架构

```
Markdown (Obsidian源文件)
    │  preprint() — 预处理剥离YAML/来源/blockquote表格/wikilink/HTML
    ▼
Pandoc (markdown → LaTeX)
    │  --lua-filter=wrap_images.lua  (图片包figure[H]+caption+自适应宽度)
    │  +superscript+subscript       (Unicode上标^2^ → \textsuperscript{2})
    │  -yaml_metadata_block         (防止正文---被误解析)
    ▼
Python LaTeX后处理
    │  \pandocbounded{} 移除
    │  {media/} → 直接路径
    │  .md} → .png}
    │  Caption逃逸: %→\%, _→\_（仅$...$外部）
    │  中文→ASCII别名替换
    │  缺图检查(PIL GIF→JPG转码)
    ▼
XeLaTeX × 2 passes
    ▼
PDF (完整性校验%PDF- / %%EOF)
```

## 二、源文件规则（每修必查）

### 2.1 表格
- **表格绝不能放在 `>` blockquote 内** → Pandoc 不会识别 pipe_table，输出 `\textbar{}` 导致格式断裂
- 表格前后必须有空行分隔
- 对齐线 `|:---|:---:|:---|` 中的中文破折号 `——` 必须在预处理阶段替换为 `---`
- mhchem 化学式示例：`\ce{^{A}_{Z}X}` 或 `\ce{^{238}_{92}U}`（上下标用 ^ 和大括号）

### 2.2 图片
- 图片引用格式：`![[media/文件名.扩展名]]`
- 图注格式：下一行 `<center>图 描述文字</center>`
- 图注文字中**严禁**出现 `$...$` 内的复杂 LaTeX（如 `$d_{xy}$`、`$E_{4s}<E_{3d}$`） → 纯文本替代
- 同一图片不要重复引用（如轨道密度图出现两次）
- captions 过长（>80字）容易在 LaTeX 中断裂 → 控制在简短清晰

### 2.3 文件命名与替换
- `chem_media_aliases.json` 管理中文→ASCII文件名映射（必须在 json 新增）
- 文件实际格式必须与扩展名一致（PNG→.png, JPG→.jpg, GIF→自动转JPG）
- 替换图片前检查新旧 MD5 是否相同（避免误覆盖）

### 2.4 上标/下标/根号
- 上标：`$^{n}$`（LaTeX数学模式）或 `^n^`（Pandoc扩展）
- 下标：`$_{n}$` 或 `~n~`（Pandoc扩展）
- 根号：`$\sqrt{...}$`（不要用 √[...] 这种格式）
- 离子电荷：`$\ce{Fe^{3+}}$` 或 `$\mathrm{Fe}^{3+}$`

### 2.5 教学文本
- 不要用「课堂原话」「教学洞察」「质心课堂原话」
- 用「理解要点」「易错提醒」「深层理解」「名师点拨」
- 不要在讲义中写「详见教学洞察-原子结构」「发生率~X%」等教师视角表述
- 不要写「元方法提醒」「以下是初赛讲义§2.6提炼的」

## 三、Lua Filter 图片宽度规则

| 图片类别 | 宽度 | 示例 |
|---|---|---|
| Excalidraw | `0.45\textwidth` | slater流程图、三原则、坐标变换 |
| 教材图(11-xx) | `0.45\textwidth` | Pauling、Cotton、轨道图、RDF图 |
| 趋势图 | `0.45\textwidth` | 原子半径、电离能、电负性 |
| 氢光谱 | `0.6\textwidth` | 需看清谱线 |
| 矩阵/流程图/因果链 | `0.5\textwidth` | 构造原理矩阵、次级周期性 |
| 默认 | `0.45\textwidth` | |

## 四、反复踩坑记录（重点关注）

| # | 问题 | 根因 | 对策 |
|---|------|------|------|
| 1 | **`\textbar{}` 格式乱** | 表格在blockquote内 → Pandoc不解析pipe_table | 表格绝不放 `>` 内 |
| 2 | **图注 `fffff` 断裂** | caption中 `_` 被LaTeX当作下标 → `d_{xy}` 断裂 | convert.py 自动 math-mode 感知 `_` 逃逸；图注中不用 $...$ |
| 3 | **缺图/重复图** | 图片被误覆盖、或同一文件引用两次 | 替换前查MD5；用 `Grep !\[\[media/` 检查引用分布 |
| 4 | **caption 中 `$...$` 导致 `fffff` 断裂** | caption内`$E_{4s}<E_{3d}$` → LaTeX把`_`当下标 → `E\_{4s}`断裂成乱码 | **图注中绝对禁止 $\LaTeX$ 公式**，只用纯中文描述。`convert.py` 已加math-mode-aware `_`逃逸 |
| 5 | **α/β/γ 不显示** | Unicode希腊字母在XeLaTeX字体中缺失 | 用 `$\alpha$` `$\beta$` `$\gamma$` 数学模式 |
| 6 | **γ和中微子丢失** | Unicode特殊字符被Pandoc丢弃 | 反中微子写 `\bar{\nu}_e`，gamma写 `$\gamma$`，全部在`\ce{}`内用mhchem语法 |
| 7 | **核反应表格格式乱** | blockquote嵌套 + Pandoc `|` 转义 | 表格不放在 `>` 内 |
| 8 | **核反应化学式 `He2+` 非上标** | `\frac{4}{2}` 在 `\ce{}` 内不工作 | 用 `^{4}_{2}He^{2+}` 而非 `\frac{4}{2}` |
| 9 | **轨道图与实际内容不符** | vault media中`11-13.png` 被杂化图覆盖 | 从 `handout/media` 取25KB版本，不走 `vault/media` |
| 10 | **图注与图片内容不一致（反复发生）** | 只改了文字没看图片实际内容 | 每张图必须**肉眼打开确认**图片里画的是什么，再写图注 |
| 11 | **图片重复引用（轨道密度图出现2次）** | 修完其他内容后没检查`Grep ![[media/` | 每次修改后用 `Grep` 检查所有图片引用，确认无重复 |
| 12 | **图片太大/太小** | `wrap_images.lua` 宽度规则不够细 | 分类别设置精确宽度 |
| 13 | **嵌入计算 → 练习** | 学生用词不友好 | 改为"练习" |
| 14 | **`\sqrt{}` 根号非标准** | 用 `√[n(n+2)]` 而非 $\LaTeX$ | 统一用 `$\sqrt{...}$` |
| 15 | **A2+ 没上标** | 直接写 `A2+` 而非 $\LaTeX$ | 统一用 `$A^{2+}$` |
| 16 | **图片文件实际格式与扩展名不一致** | PNG命名为.jpg导致graphicx报错 | 实际格式必须匹配扩展名，不符合的用PIL检查并转码 |

## 五、检查清单（生成PDF前，逐条打勾）

### 5.1 源文件
- [ ] `Grep` 所有图片引用不重复
- [ ] 所有 `>` blockquote 内部无 pipe_table
- [ ] 所有图片实际格式 == 扩展名
- [ ] 所有"嵌入式计算"改成"练习"
- [ ] 无「课堂原话」「教学洞察」「质心」「元方法」「初赛讲义§X」

### 5.2 图注（最容易出错，必须逐条检查）
- [ ] caption 中**绝对不能有 `$...$` 复杂格式**（只能用纯中文）
- [ ] caption 中不能有裸 `_`（如 `d_{xy}`、`E_{4s}`） → 统一用纯文本 `dxy`、`E4s`
- [ ] 每张图的**文件实际内容**与图注描述一致（**打开图片文件肉眼确认**）
- [ ] 原书编号在图注末尾标注：`（普化原理第4版 图11.XX）`

### 5.3 核反应表格
- [ ] 表格不在 `>` blockquote 内
- [ ] 对齐线：`|:---|:---|:---|`
- [ ] 化学式用 `\ce{^{A}_{Z}X}` mhchem 格式
- [ ] $\alpha$ $\beta$ $\gamma$ 用数学模式（`$\alpha$`）
- [ ] 反中微子写为 `\bar{\nu}_e`
- [ ] 用 `^{4}_{2}He^{2+}` 而非 `\frac{4}{2}`

### 5.4 特殊符号
- [ ] `$\sqrt{...}$` 而非 `√[...]`
- [ ] `$A^{2+}$` 而非 `A2+`
- [ ] 化学式全部用 `$...$` 或 `\ce{...}` 包裹
- [ ] α/β/γ 用 `$\alpha$` 等数学模式

### 5.5 图片文件
- [ ] 所有图片实际格式与扩展名一致（PNG→.png，JPG→.jpg）
- [ ] PDF完整性通过
- [ ] 文件非0KB（空文件=下载失败）

### 5.6 管线文件
- [ ] `wrap_images.lua` 设置了正确的宽度分类
- [ ] `chem_media_aliases.json` 包含所有中文→ASCII映射
- [ ] `convert_handout_to_pdf.py` 的 caption 逃逸逻辑匹配

## 六、图片文件对照表（原子结构讲义）

以下为本讲义中全部图片的文件名与实际内容对照，修图时必须确认对应关系，**不能只改图注不改图片**。

| 编号 | 文件名 | 实际内容 | 备注 |
|:---:|:---|---|:---|
| 图1 | `hydrogen_emission_series.jpg` | 氢放电管可见光光谱（Balmer系4条谱线） | |
| 图2 | `excalidraw-原子结构-schrodinger-coordinate-transform.png` | 坐标变换示意图 | Excalidraw |
| 图3 | `11-13-orbital-shapes-s-p-d.jpg` | s/p/d轨道角度分布 | 25KB版本 |
| 图4 | `orbital_2p_three_orientations.jpg` | p轨道三维形状（三个取向） | |
| 图5 | `orbital_3d_five_orientations.jpg` | d轨道三维形状（五个取向） | |
| 图6 | `11-21-radial-distribution-3s-3p-3d.jpg` | 3s/3p/3d径向分布函数对比 | |
| **图7** | `11-22-4s-3d-radial-distribution.jpg` | **4s与3d径向分布对比** | **图注必须写"4s在主峰外有靠近核的小峰"** |
| 图8 | `orbital_density_1s_2s_3s.jpg` | s轨道径向概率密度 | |
| 图9 | `构造原理-填充顺序.matrix.png` | 构造原理电子填充顺序矩阵 | |
| 图10 | `11-19-pauling-energy-levels.jpg` | Pauling近似能级图 | |
| 图11 | `11-20-cotton-orbital-energy-vs-Z.jpg` | Cotton图（轨道能量随Z变化） | |
| 图12 | `atomic_radius_trend.jpg` | 原子半径随Z变化趋势图 | 来自 `11-23-atomic-radius-periodic-trend.jpg` |
| 图13 | `first_ionization_energy_trend.png` | 第一电离能随Z变化趋势图 | 来自 `ionization_energy_trend.png` |
| 图14 | `electronegativity_table.jpg` | 电负性(Pauling)随Z变化趋势图 | 来自 `11-25-electronegativity-periodic-trend.jpg` |
| 图15 | `次级周期性因果链.causal-chain.png` | 次级周期性因果链 | |

## 七、模板改进

### 7.1 chemistry-preamble.tex（导言区）
- 已包含：行距1.15、段落间距0.3em、首行缩进2em、blockquote缩小字号/缩进
- 已包含：子段落格式设置 `subsubsection` `paragraph`
- 已包含：`float` 包 + `[H]` 强制定位，`topfraction=0.9` 减少跨页断裂
- 后续讲义可直接复用此版本

### 7.2 wrap_images.lua（图片宽度控制）
- 分类别（Excalidraw/教材图/趋势图/矩阵图）设置不同宽度
- 图注通过 `<center>图 ...</center>` 转换为 Emph 节点 → LaTeX `\caption{}`
- 原子结构已验证，其他讲义可直接复用

### 7.3 convert_handout_to_pdf.py（主管线）
- caption 逃逸：`%→\%`、`$`外`_→\_`
- 缺图检查自动转码GIF→JPG
- 并行构建 `--parallel ALL`
- 已有原子结构案例验证通过

### 7.4 checklist.md（快速检查脚本）
- 生成PDF前逐条打勾
- 最常出错的图注/表格/核反应已前置高亮

## 八、扩展至其他讲义的步骤

迁移到其他5本超级充实版讲义：
1. 执行 checklist.md 修复源文件格式
2. `chem_media_aliases.json` 补充该讲义的中文→ASCII映射
3. 复制 `chem_media/` 缺失图片
4. `python convert.py "讲义名.md"` 单本测试
5. **打开PDF逐页检查每张图的图注与图片内容是否一致**
6. 全部通过后：`python convert.py --parallel ALL`
