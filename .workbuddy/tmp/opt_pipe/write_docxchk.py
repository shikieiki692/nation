# -*- coding: utf-8 -*-
"""追加：卷族 docx 交付件与图源核查"""
import io, os
os.chdir(r'C:\Obsidion\妙妙屋')

NOTE = """
## 23:3x 卷族 docx 交付件与图源核查（发现「按当前构建器重出＝整卷丢图」，已回滚）

- **docx 盘点**：`初赛模拟卷/真题版式/` **27**（X~XVII ＋ XIp，9 卷 × 3 版）；`（老·I~IX）/真题版式/` **27** ⇒ 齐全。
  **6 卷答案版落后于 md**（X／XI／XIp／XIV／XVI／XVII，≈610 分；XVI 170 分）；**XV 已由并行线 23:02 重出**。
  **学生版／答题卡不含来源行** ⇒ 无需重出。
- 🔴🔴 **重出实验＝整卷丢图**：`build_chusai_zhenti_layout.py --answer XIp XVI XVII` 后
  `word/media`：XIp 80→**11**、XVI 80→**0**、XVII 56→**5** ⇒ **已从备份回滚**（复原 80/80/56），git 无差异。
- **根因**：构建器 `resolve_images()`（:283）**只查 `MEDIA = VAULT/'媒体仓库'`**，无 fallback；
  **新卷图全在 `04-题库/2026机构初赛模拟题/<机构>/images/`**（媒体仓库命中：X 0/75、XI 6/70、XIp 11/80、
  XIV 0/54、XV 0/33、XVI 0/80、XVII 5/56）；
  **老卷（I~IX）图在媒体仓库（命中 100%：I 10/10、III 11/11、V 13/13、VII 31/31、IX 14/14）⇒ 只有老卷可重建**。
- **处置**：**未擅自重出**（涉及组卷线工具与共享 `媒体仓库/`，按铁律「跨线动工先对齐」）；
  已登记任务卡 **⑨**，给出三方案（A 修 resolve_images 多路径＋命中率断言／B 重出前临时复制图再清理／C 交并行线）。
- **报告**：`09-审计报告/2026-10-14-卷族docx交付件与图源核查.md`

### 新增判据
- 🔴🔴 **重出 docx 前必验「媒体数守恒」**（`docx word/media` 数 == 卷 md 图引用数）——构建器静默丢图，
  脚本仍报「完成 3/3」。
- 🔴🔴 **`resolve_images` 只有 `媒体仓库/` 一个搜索根** ⇒ 新卷（图在卡片 `images/`）必丢图；**单卷成功不可外推**。
- 🔴 **构建脚本报「完成 N/N」≠ 产物正确** ⇒ 必叠加内容级断言（图数/页数）。
- 📌 交付件 docx **入 git** ⇒ 重出前先备份，出问题即时回滚。
"""

for P in ['.workbuddy/memory/2026-10-14.md', '00-首页/工作日志/2026-10-14.md']:
    t = io.open(P, encoding='utf-8').read() if os.path.exists(P) else ''
    if t and not t.endswith('\n'):
        t += '\n'
    io.open(P, 'w', encoding='utf-8', newline='').write(t + NOTE)
    print('追加完成:', P)
