# -*- coding: utf-8 -*-
r"""追加日志与 memory（X~XV 图片排版 P1-b）。"""
import io, os
os.chdir(r'C:\Obsidion\妙妙屋')

LOG = '00-首页/工作日志/2026-10-14.md'
add = '''
## 卷 X~XV 图片排版核验与放大（P1-b）

- **范围** X/XI/XIp/XII/XIII/XIV/XV（沿用 XVI/XVII 口径：图齐 → 机器初筛 → 目检 → 放大 → 闸门）。
- ✅ **图齐**：④-e 图源覆盖核验 **九卷全 PASS**（丢图此前已清零）。
- ✅ **机器初筛无结构性缺陷**：图注连排 0／孤立数字行 0／图注粘连 0（XV 报 2 处为**假阳性**，正则 `\\s*` 跨空行）／边缘截断 0／dpi 下限 150。
- ✅ **主修复「图幅偏小」**：X~XV **未登记 post_patches** ⇒ 构建器按朝向定尺寸后只缩不放（最小图仅 1.93cm）。用 `vol_img_upscale.py --vol <V>`（≥150dpi 下放大到 min(dpi上限, CAP_ORG×1.35, 12cm)，**幂等**）**放大 287 张**：X 62／XI 59／XIp 82／XIV 49／XV 35；登记进各卷 `vol_meta::post_patches`（重建自动重放）。图数守恒（21/75、23/70、36/80、20/54、17/35）；XIV 页数 10→11／29→32。
- ✅ **附带**：XIp 答案版渲染 **THIN −3**（放大顺带修好 3 处细长条）。
- **未动**：图内水印/装饰（XIV 第 1/2 题源图自带书签灰带＋音符/五线谱＋"CH"涂鸦）—— owner 指示暂不处理。
- **闸门**：五卷 `qa_vol_all` **ALL PASS**；`qa_vol_render` 与基线**零新增**。
- **另发现（未提交）**：XII/XIII 答案版 docx 仍是 10-12 遗留 `M`（提取文本与 media 内容 sha 均与 HEAD 一致，字节级微差）⇒ 与图片工作无关，待确认。
- 报告＝`09-审计报告/2026-10-14-卷X-XV图片排版核验.md`。
'''
d = io.open(LOG, encoding='utf-8', newline='').read()
io.open(LOG, 'w', encoding='utf-8', newline='').write(d.rstrip('\n') + '\n\n' + add)
print('worklog ok')

MEM = '.workbuddy/memory/2026-10-14.md'
addm = '''
### 卷 X~XV 图片排版（P1-b，2026-10-14 午后）

- 🔴 「图幅偏小」＝**构建器只缩不放**（`CAP_ORG` 按朝向定尺寸 → `apply_dpi_cap` 只降不升）；**X~XV 早先漏登记 `post_patches`** ⇒ 同 XVI/XVII 补丁即可治。补丁＝`vol_img_upscale.py --vol <V>`（≥150dpi 下 `min(dpi上限, CAP_ORG×1.35, 12cm)`，**幂等**）。
- 🔴 **放大顺带修 THIN**：把细长条图放大到目标宽后，`qa_vol_render` 的 THIN 判据自然消失（XIp 答案版 −3 处）。
- 🔴 **假阳性判据**：`^图\\s*\\d+\\s*\\n(?=\\S)` 会因 `\\s*` **跨空行**误报「图注粘连」⇒ 判「图注粘连」须用 `^图\\s*\\d+$` **fullmatch** 再比下一行。
- 🔴🔴 **HEAD/工作区对照必须同法**：曾用「raw XML 计数」对 HEAD、「提取 `<w:t>` 文本」对工作区 ⇒ **假报「HEAD 缺解析块」**。正解＝两边都走**提取文本**。另：docx 内图名**未必是 sha**（旧构建器用 `rIdNN.jpg`）⇒ 取像素应**直接读 docx media 字节**，勿按名找源文件。
- **口径**：卷 docx 提交前必核「提取文本 ≡ HEAD 文本」（`media` 会因补丁变，文本不应变）⇒ 保证是净增排版改进而非内容回退。
'''
d2 = io.open(MEM, encoding='utf-8', newline='').read()
io.open(MEM, 'w', encoding='utf-8', newline='').write(d2.rstrip('\n') + '\n' + addm)
print('memory ok')
