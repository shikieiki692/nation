# 化学课件 PPT 管线（其他 Agent 遵循此文档操作）

基于「绝命毒师配色」模板（米白底 × 墨绿 × 橙黄）制作/改造高中化学课件的标准流程。已有产出样例：`开学第一课/`（从零生成）、`物质的分类/`（已有课件换皮）。

---

## 第 0 步：先判断走哪种模式（最重要）

| 用户输入 | 走哪个模式 |
|---|---|
| 给了一个**已有 PPT**，说「套用模板」 | **默认劝退**：现成课件（尤其高密度课本同步课件）套本模板效果差，已实践否决。用户坚持才走模式 A，且先做 3-5 页小样给用户确认再全量 |
| 给了大纲/文稿，说「做一份 PPT」 | **模式 B：从零生成**（本模板的主场，叙事型课件效果最好） |

### 模式 A：保内容、调结构（两个极端都踩过坑，别走回头路）

**目标判定标准：远看是我们的模板，近读是源课件的内容。**

- ❌ 过度改写（错）：把源文案压缩/重写/重新组织语言——用户原话「内容不用自己重新做」
- ❌ 纯换皮（错）：只在源文件上改背景/字体，原装饰和混乱版式全留——用户原话「有的结构还是要改一下，不然太奇怪」
- ✅ 正确做法：**文字逐字搬运 + 结构按模板重排**

**内容侧（一个字都不许动）**：
1. 所有文字逐字保留：标题（含「【思考2】利用树状分类法对……并举例说明。」这种长标题也完整保留，长就换行，不许精简）、题干、选项、解析、答案、提示语、来源行
2. 页面对应 1:1，不增页不删页不合并不拆分
3. 源文件的笔误不顺手修——列出来汇报，用户批准才改
4. 答案在源页面上的就保留在页面上
5. 源图片原样使用（从源 pptx 的 ppt/media 提取，按页对应；形状画的图用 soffice 转 PDF 后裁切还原），contain 完整显示

**结构侧（按模板重排，让成品像我们做的）**：
1. 套统一外壳：标题栏（Lucide 图标 + 橙色 Part 标签 + 源页标题）、左侧墨绿边条 + 橙黄进度段、页脚分隔线 + 页码、右上淡六边形
2. 正文块按模板组件重排：条目→要点列表、并列内容→卡片、对照内容→模板表格（墨绿表头白字、关键行列浅黄高亮）、答案→橙黄答案卡
3. 源装饰元素（卡通贴纸、花哨边框、渐变横幅）删除或替换为模板元素
4. 源的红蓝强调字可以保留（承载语义），但整体配色向模板语义色靠拢：强调用深橙/橙黄，警示用砖红
5. 字号按模板层级（正文 13-16pt），密页可降到 12pt，但**不许为了排版好看删字**
6. 化学式转 Unicode 上下标（H2SO4 → H₂SO₄）——这算格式不算内容

**验收口诀**：拿源课件和新版逐页对比——文字能对上每一个字，版式看起来像两套模板里的近亲。

### 模式 B 铁律

1. 先写 content-spec.md 并**给用户确认后再构建**；数字、案例以用户提供的素材为准，不编造。
2. 图片一律 contain 等比完整显示，**禁止 cover 裁剪**。

---

## 模式 A：已有 PPT 套模板（保内容调结构，约 30-60 分钟）

```bash
cd "C:/Obsidion/妙妙屋/09-AI工作区/pptx-化学模板"
export PATH="/c/Program Files/LibreOffice/program:$PATH"
```

1. **提取内容**：python-pptx 逐页提取全部文字（含表格）存 `源-text.txt`；逐页提取嵌入图片存 `images-src/`（shape_type==13 的 shape.image.blob）；形状绘制的图用 soffice 转 PDF 后 150dpi 裁切还原。
2. **复制模式 B 脚手架**为新课件目录，按「结构侧」规则用模板组件重排每一页——文字从 `源-text.txt` 逐字复制进 slides，一个字符不改。
3. **构建**：gen-slides → build.js → set-fonts.py（与模式 B 相同）。
4. **一致性核对**：写个小脚本，用每页特征串（方程式、选项、答案、解析末句）程序化比对源文本与新 slides，必须 0 缺失。
5. **目验**：thumbnail 全览 + 逐页 96dpi——重点看密文字页不溢出、源图完整清晰、外壳四件到位。
6. **汇报**：附「发现的源文件问题/可优化点」清单（只报告，不擅自动）。

`review-gai/reskin.py`（纯换皮脚本）保留作应急备用，**默认不用**。

---

## 模式 B：从零生成（HTML→PPTX 管线）

每份课件一个子目录，流程（详见下方目录结构与坑清单）：

1. 写 `content-spec.md`（逐页正文/图注/来源/备注），**先给用户确认**
2. 复制 `开学第一课/` 脚手架（gen-slides.py 的模板函数 light_page/hdr/卡片保留，只改 PAGES）
3. 配图：Wikimedia Commons 下载（`curl -L -A "Mozilla/5.0" "https://commons.wikimedia.org/wiki/Special:FilePath/<文件名>?width=1200" -o images/x.jpg`），**每张必须 ReadMediaFile 目验**；prep-images.js 做 contain 卡片
4. `gen-slides.py` 生成 slides/*.html → `node build.js` 构建（含 addNotes 备注）→ `set-fonts.py` 统一字体
5. 验证：html2pptx 零错误 + thumbnail 全览 + 96dpi 逐页目验 + validate.py
6. 附带产出 index.html（放映）/ overview.html（总览）

## 目录结构

```
pptx-化学模板/
├── html2pptx.js        # 修补版转换库（补丁：中文路径 img 解码、li 多 run bullet 不丢）
├── set-fonts.py        # 字体后处理：latin→Times New Roman，ea→微软雅黑
├── review-gai/reskin.py# 模式 A 换皮脚本（吃 unpack 目录）
├── icons/              # Lucide 线性图标 PNG、cell-*.png 元素格子、hex-corner.png
├── .venv/              # Pillow、python-pptx
├── node_modules/       # pptxgenjs、playwright、sharp、react-icons
└── <课件名>/            # content-spec.md → gen-slides.py → slides/ → build.js → 产出.pptx
```

## 设计规范速查

- 色板：米白底 `#FAF7F0`、墨绿 `#1B4332`、中绿 `#2D6A4F`、橙黄 `#E8A33D`（只做色块/强调）、深橙 `#B45309`（浅底上的橙字/大数字）、砖红 `#C0392B`（仅警示）、正文 `#1F2937`、次要 `#6B7280`
- 浅色页骨架：标题栏 40pt 左边距（16pt Lucide 图标 + 橙色 Part 标签 + 26pt 墨绿标题）→ 贯通细分隔线 #DDE5DD + 左端 44pt 橙锚点段；左侧 8pt 墨绿边条 + 橙黄进度段；页脚 y=384pt 分隔线 + 右下页码；右上 hex-corner.png 淡装饰
- 正文 13–16pt、行距 1.4–1.55；内容区 y≈70 到 y≈370 排饱满
- 图片：contain 禁裁剪；卡片米白衬底 + 圆角 + 1pt #DDD6C8 细边
- 方程式：Unicode 下标 ₂₃₄、上标 ⁺⁻、符号 ⇌ ═ ↑ ↓（雅黑和 Times 都已验证可渲染）
- 字体：中文微软雅黑，西文/数字/符号 Times New Roman（set-fonts.py 后处理实现）

## 依赖与版本（实测可用）

- Node v24；pptxgenjs 4.0.1、playwright 1.60.0、sharp 0.35.3、react-icons 5.7.0（playwright 锁 1.60：chromium 按此版本缓存）
- Python .venv：Pillow 12.3.0、python-pptx 1.0.2
- LibreOffice（转 PDF，需 `export PATH="/c/Program Files/LibreOffice/program:$PATH"`）；pdftoppm 在 PATH
- 技能脚本：`~/.agents/skills/pptx/scripts/thumbnail.py`、`~/.agents/skills/pptx/ooxml/scripts/{unpack,validate,pack}.py`（操作前完整读 `~/.agents/skills/pptx/html2pptx.md` 或 `ooxml.md`）

## 已知坑（实战总结，新坑继续追加）

- **中文路径**：img src 中文路径必须走修补版 html2pptx.js；控制台 print 含 ⇌ 等非 GBK 字符会崩（脚本内避免直接打印，或 PYTHONIOENCODING=utf-8）
- **`<br>` 丢行**：混合字号行内 `<br>` 后内容可能整行丢失——多行一律拆独立 `<p>`
- **显式宽度防换行**：标题/金句 `<p>` 不给 width 时 PPTX 端会意外折行——给足显式 width
- **0.5" 底缘校验**：html2pptx 要求文本底边距页底 ≥0.5"，绝对定位元素注意 top
- **PNG 透明通道**：PIL 处理带 alpha 的 PNG 先合成到米白底，直接 convert('RGB') 会黑底
- **PIL 图内文字**：雅黑没有 ₂ 等下标字形，图内混排要 CJK=雅黑 / 西文=Times 分段渲染
- **卡片尺寸对齐**：prep-images.js 的 CARDS 尺寸必须和 slides 里 `<img>` 尺寸一致（3 倍像素）
- **LibreOffice 行距**：PPTX 渲染行高略大于浏览器，深底色块里的文字宁松勿紧
- **源 PPT 固有缺陷**：外链图片（r:link file:///）、重复 sldId 等，换皮时可修复（属修坏不修内容），但要在汇报里说明
