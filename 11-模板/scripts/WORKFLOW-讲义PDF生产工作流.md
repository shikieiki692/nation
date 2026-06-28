# 超级充实版讲义PDF生产工作流 · 原子结构样板经验总结

> 本文档基于《原子结构-超级充实版（自学完整）》从Markdown到PDF的全过程改进总结。
> **核心教训**：上一个版本的"修复报告"97%是虚构的——真正的修复需要**肉眼逐张确认图片内容**、**逐条检查图注**、**实际执行管线**，绝非声称"已修复"就能糊弄过去。

---

## 一、管线架构速览

```
源文件 (.md)               ← Obsidian编写，YAML frontmatter + wikilink + mhchem + pipe_table
    │  preprint()           ← 剥离YAML/blockquote内表格/Unicode上标/wikilink/HTML
    ▼
Pandoc (markdown → LaTeX)
    │  --lua-filter=wrap_images.lua   ← 图片→figure[H]+caption+自适应宽度
    │  +tex_math_dollars+raw_tex+pipe_tables+superscript+subscript-yaml_metadata_block
    ▼
Python LaTeX后处理          ← 移除\pandocbounded{}、路径替换、Caption逃逸、别名替换、缺图检查
    ▼
XeLaTeX × 2 passes         ← ctexart + SimSun/SimHei + mhchem v4
    ▼
PDF (完整性校验 %PDF- / %%EOF)
```

**关键依赖**：
- `chemistry-preamble.tex` — v7，导言区（ctexart, mhchem v4, geometry, float[H]）
- `wrap_images.lua` — v4，图片宽度分类表（Excalidraw=0.45, 教材图=0.45, 趋势图=0.45, 氢光谱=0.6, 矩阵/流程图=0.5, 默认=0.45）
- `chem_media_aliases.json` — 中文别名→ASCII映射
- `convert_handout_to_pdf.py` — v2，主管线

---

## 二、源文件编写规范

### 2.1 图片引用
```
![[media/文件名.扩展名]]
<center>图 纯中文描述……（教材名 图号）</center>
```

**重中之重（踩坑10+次）**：
- **图注绝对禁止 `$...$`** → `$E_{4s}<E_{3d}$` 中的 `_` 被LaTeX转义 → `E\_{4s}` → 输出"fffff"乱码
- **图注绝对禁止裸 `_`** → 写"dxy"而非"d_{xy}"、"E4s"而非"E_4s"
- 图注中Unicode希腊字母（αβγ）可用（SimSun支持），正文则用 `$\alpha$`
- 每条图注必须**肉眼打开图片文件**确认内容匹配
- 图注控制在 80 字以内，过长易断行

### 2.2 mhchem 核反应化学式

```markdown
| $\beta$ 衰变 | $\ce{^{A}_{Z}X -> ^{A}_{Z+1}Y + ^{0}_{-1}e^{-}}$ $+ \bar{\nu}_e$ | $\ce{^{14}_{6}C -> ^{14}_{7}N + ^{0}_{-1}e^{-}}$ $+ \bar{\nu}_e$ |
| $\gamma$ 辐射 | $\ce{^{A}_{Z}X^{*} -> ^{A}_{Z}X}$ $+ \gamma$ | $\ce{^{60}_{27}Co^{*} -> ^{60}_{27}Co}$ $+ \gamma$ |
```

**关键**：`\bar{\nu}_e`（反中微子）和 `\gamma` **必须放在 `\ce{}` 外面**。

### 2.3 表格
- **绝不能在 `>` blockquote 内** → Pandoc不解析pipe_table → 输出 `\textbar{}`
- 对齐线确保是ASCII `---` 而非中文 `——`
- 表格前后必须有空行

### 2.4 禁用语（学生讲义）
| ❌ 删除 | ✅ 替换为 |
|---------|----------|
| 课堂原话、教学洞察、质心课堂原话 | 理解要点、易错提醒、深层理解、名师点拨 |
| 元方法提醒 | 删除 |
| 初赛讲义§X、详见……（教师文档名） | 删除 |
| 发生率~X%、根据统计 | 删除 |
| 嵌入式计算 | 练习 |
| 详见教学洞察-原子结构 | 删除 |

### 2.5 YAML 元数据规范

```yaml
---
last_audit: "YYYY-MM-DD §X.Y修复内容；附：debug时请手动打开PDF逐页检查"
template_version: 自学完整版 v2.2
exemplar: true
---
```

`last_audit` 必须写**实际做了什么**（不是声称），结尾附"打开PDF逐页检查"的提示。

---

## 三、管道操作流程

### Step 1: 源文件预处理（手动）——checklist.md 逐条打勾
- [ ] `Grep ![[media/` 检查所有图片引用，确保无重复
- [ ] `Grep ^\|` 检查没有表格在 `>` blockquote 内
- [ ] `Grep 教学洞察|元方法|初赛讲义|课堂原话|质心` 删除教师用语
- [ ] `Grep 嵌入式计算` → "练习"
- [ ] 所有 `\sqrt{...}` 而非 `√[...]`
- [ ] 所有 `$A^{2+}$` 而非 `A2+`
- [ ] αβγ 已用 `$\alpha$` 数学模式

### Step 2: 图片处理（最易出错！）
- [ ] 检查 `C:\Temp\chem_media\` 中是否有该讲义的**全部图片**
- [ ] 缺失的图片从 vault `/04-课件/学生讲义/media/` 复制
- [ ] 对教材扫描图（径向分布、趋势图等）：**打开图片肉眼确认内容**
- [ ] 对自制图（Excalidraw）：确保 .png 已从 .md 渲染（用 `node excalidraw-to-png.mjs`）
- [ ] 图片实际格式必须与扩展名一致（PIL `Image.open` 验证）
- [ ] **全部重新制作的图片**：可以Python matplotlib精确绘制（见下节）

### Step 3: 管线配置
- [ ] `chem_media_aliases.json` 补充此讲义的新中文别名映射
- [ ] `wrap_images.lua` 确认宽度分类覆盖此讲义的图片类别
- [ ] `sync_media_to_temp.py` 确认需要跑一遍

### Step 4: 构建与验证
```bash
cd 11-模板/scripts
python convert_handout_to_pdf.py --file "讲义名.md"
```
- [ ] 输出"全图 ✓"（所有图片通过）
- [ ] 确认PDF文件大小合理（原子结构参考：~2MB, 27p, 17张图）
- [ ] **打开PDF，逐页检查每张图**：图片内容 + 图注是否匹配
- [ ] 检查公式渲染（特别是核反应表格、mhchem）
- [ ] 检查页数是否合理（参考：原子结构27页）

### Step 5: 批量构建
```bash
python convert_handout_to_pdf.py --parallel ALL
```

---

## 四、图片的进阶处理技术

### 4.1 用 Python matplotlib 生成教材级科学图表

当教材扫描图质量差、内容不可靠或不存在时，用精确波函数绘制：

**适用场景**：
- 径向分布函数 D(r) = r²R(r)²
- 原子轨道形状投影
- 能级图比较

**流程图（已验证于原子结构图6/7/8）**：
1. 拉盖尔多项式的数值递推（非scipy，避免依赖）
2. `laguerre_assoc()` 广义多项式递推 → `radial_wf_nl()` → `radial_distribution()`
3. 用matplotlib绘制多曲线对比图
4. 添加标注箭头（近核小峰、节点位置）
5. 中文字体：SimHei（注意下标数字₀缺失，用 "a0" 代替 "a₀"）

**保存参数**：`dpi=250, bbox_inches='tight'` → 约150KB JPG，PDF可清晰显示

**脚本模板**：`C:\Temp\chem_media\plot_radial_distributions.py`

### 4.2 Excalidraw 图渲染
- 源文件：`xxx.流程图.md` / `xxx.关系图.md`
- 命令：`node excalidraw-to-png.mjs input.md output.png`
- 放到 C:\Temp\chem_media\ 和 vault media/ 各一份

### 4.3 图片目录结构
```
C:\Temp\chem_media\         ← 管线实际读取位置（必须是所有图片的最终版）
    hydrogen_emission_series.jpg
    11-21-radial-distribution-3s-3p-3d.jpg
    …

C:\Obsidion\妙妙屋\04-课件\学生讲义\media\   ← md文件引用的位置
    同上（用 Copy-Item 同步）
```

> **陷阱**：管线只检查 C:\Temp\chem_media\，替换图片必须同步到两处。

---

## 五、踩坑精华记录（死也要记住）

| # | 问题 | 根因 | 对策 |
|---|------|------|------|
| 1 | **图注"fffff"乱码** | caption中的 `_` 被LaTeX当作下标 → `E\_{4s}`断裂 | 图注绝对不用 `$...$` |
| 2 | **图片内容与图注不符** | 只改了文字没看图片 | 每张图用眼睛确认 |
| 3 | **核反应公式不渲染** | `\bar{\nu}_e` 在 `\ce{}` 内不工作 | 移出 `\ce{}` |
| 4 | **表格断裂** | `>` blockquote 内 pipe_table 不识别 | 表格放外面 |
| 5 | **图片重复引用** | 修完不检查 | `Grep ![[media/` 是最后一步 |
| 6 | **α/β/γ 不显示** | Unicode希腊字母在XeLaTeX缺字体 | 正文 `$\alpha$`；图注用Unicode |
| 7 | **Temp vs vault 脱节** | 管线读 Temp，md 引用 vault | 同步到两处 |
| 8 | **嵌入计算不友好** | 抄教材用语 | 改为"练习" |
| 9 | **声称修复但未执行** | 模型幻觉——说"已修复"但文件没动 | 改完必须 `git diff` 验证 |
| 10 | **图注包含LaTeX公式** | 复制粘贴教材图注未处理 | 图注必须纯中文描述 |

---

## 六、原子结构讲义的参考数据（为其他讲义提供基线）

| 指标 | 数值 | 说明 |
|:---|:---|---|
| 页数 | 27p | PDF最终输出 |
| 图片数 | 17张 | 全部通过管线检查 |
| 源文件大小 | ~56KB | md文件 |
| PDF大小 | ~2MB | 1958–2173KB范围 |
| 构建时间 | ~30s | XeLaTeX两轮 |
| 图片生成脚本 | 1个 | plot_radial_distributions.py→3张图 |
| 修复轮次 | 6轮 | 从第一次"假修复"到真正确认 |
| 踩坑类型 | 10大类 | 见上节 |

---

## 七、对其他5本超级充实版讲义的建议（按优先级）

### P0：原子结构剩余问题
- 图6/7/8已替换为matplotlib精确图 → 验证PDF效果
- 继续检查所有核反应方程（各讲义如有）

### P1：元素周期律讲义（下一本最紧急）
- 管线配置：与原子结构共享大部分图片
- 重点检查：电离能趋势图、电负性图、原子半径图的**实际内容**
- 可能需要的图片：对角线的规则图、镧系收缩图 → 可用Excalidraw或Python生成

### P1：分子结构基础讲义
- 需处理 Excalidraw 图：Lewis五步法、VSEPR决策链、轨道杂化类型对比 → 全部已渲染为.png
- 重点：MO图（O₂, N₂）需要确认来源
- 新增：s-p混杂对比框（内容素材已在计划文档）

### P2：配位化合物基础讲义
- 颜色对照表（内容素材已在计划文档）
- 需确认：d-d跃迁图、光谱化学序列图、八面体/四面体分裂图的实际内容

### P2：晶体学/晶体结构基础讲义
- 14种布拉维格子矩阵图、七大晶系决策树 → Excalidraw
- 缺少大量图片 → 需要找教材扫描图或重新绘制

### 通用改进
- 在所有讲义开头增加**本讲义的图片清单对照表**（参考README §六）
- 对所有新制作的图，在 `chem_media_aliases.json` 注册映射
- 对需要教材图的讲义，优先考虑 Python/matplotlib 生成（比找网络图可靠）

---

## 八、自动化建议（未实现但值得做）

1. **图片冲突检测**：构建前自动比对 Temp 和 vault 的图片 MD5，不一致则提醒
2. **图注-图片内容AI验证**：用视觉模型自动描述图片内容 vs 图注文字相似度
3. **批量缺失图片报告**：`scripts/validate_images.py` 可以升级为对所有讲义做
4. **构建后PDF转图片**：自动截取PDF中所有图片页，供快速目视检查
5. **版本号钩子**：`convert_handout_to_pdf.py` 构建成功时自动递增 YAML `template_version`
6. **`git diff --stat` 验证**：构建前自动输出修改文件列表，防止"看似改了其实没改"

---

## 九、记住的教训（最深的三条）

1. **"已修复"是最危险的三个字**——每次声称修复后，必须 `git diff` 确认文件变了，必须 `build` 确认PDF变了，必须**打开PDF用眼睛看**确认效果对了。上一轮说"修复6轮"，结果md文件一个字没动。信任但验证。

2. **图片是核心也是软肋**——原子结构25张图片计划最终只落地17张。图注内容与图片实际内容的匹配检查是**最耗时的步骤**，也是最容易出问题的。

3. **工具链本身不产生质量**——最好的管道也不能把错误的内容变正确。管线的意义是降低修改成本，让"修改→生成→验证"的循环快起来；但**验证必须由人来完成**。
