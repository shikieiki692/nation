# -*- coding: utf-8 -*-
"""追加：构建器根治（多路径 ＋ 自动 staging）"""
import io, os
os.chdir(r'C:\Obsidion\妙妙屋')

NOTE = """
## 23:52 ✅ 根治：构建器改为多路径 ＋ 自动 staging（不再需要手工部署图片）

- **改动** `build_chusai_zhenti_layout.py`（**44 insertions / 3 deletions**，向后兼容）：
  ① 新增 `STAGE_IMG = TMP/"imgstage"`；② 新增 `img_index()`（一次性建**全库图片文件名索引**，排除 `.git/.workbuddy`）；
  ③ 重写 `resolve_images()`：查找顺序 **媒体仓库/ → 全库索引**，命中即**自动 staging**；
  ④ `--resource-path={MEDIA}{os.pathsep}{STAGE_IMG}`；⑤ `main()` 开头 `rmtree(STAGE_IMG)` 防 tmp 累积。
- **验证**：`py_compile` OK；
  · 新卷单卷实测（XVI，媒体仓库里 0 张该卷图）⇒ `[缺图]=0`、media **80/80 守恒**、**媒体仓库 15881→15881（零写入）**、staging 收 80 张；
  · **老卷回归**（I，图在媒体仓库）⇒ `[缺图]=0`、media **10/10 守恒**、媒体仓库零写入 ⇒ **老卷行为不变**；
  · **6 卷统一重出** ⇒ `rc=0`/24s/`[缺图]=0`/**75-70-80-54-80-56 全守恒**/媒体仓库零写入。
- **⇒ 新卷重建不再需要手工部署图片**（方案 A 落地，方案 B 退居备用）。
- 构建器备份：`.workbuddy/tmp/opt_pipe/_bak/builder_20261014_234950/`

### 新增判据
- 🔴🔴 **「图片多根解析」的正确形态＝索引 ＋ staging ＋ 双 resource-path**：
  直接改单根不够——pandoc 还需 `--resource-path` 能找到图，故命中后须**复制到 staging 目录**并加为第二根。
- 🔴 **改共享构建器后必须做「老卷回归」**（老卷图源不同 ⇒ 单看新卷通过不能外推）。
- 📌 **`main()` 开头清理 staging**，否则 tmp 会随每次构建持续累积（本轮实测 393 张）。
- 🔴 **`git status` 出现 `MM` 且暂存内容是「自己上一笔提交的文件被标 D/M」＝ `commit --only` 残留**；
  清法＝`git reset -q HEAD`（只动索引），清后必须复核**文件仍在**。
"""

for P in ['.workbuddy/memory/2026-10-14.md', '00-首页/工作日志/2026-10-14.md']:
    t = io.open(P, encoding='utf-8').read() if os.path.exists(P) else ''
    if t and not t.endswith('\n'):
        t += '\n'
    io.open(P, 'w', encoding='utf-8', newline='').write(t + NOTE)
    print('追加完成:', P)
