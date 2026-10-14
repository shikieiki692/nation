# -*- coding: utf-8 -*-
"""追加：chemy 来源渠道标注（卡 183 + 卷 7）"""
import io, os
os.chdir(r'C:\Obsidion\妙妙屋')

NOTE = """
## 23:0x chemy 来源渠道标注已落库（183 卡 ＋ 7 卷 / 20 处）

- **背景**：owner 提「初赛模拟卷来源不对／chemy 都没有 40 届的题」。核查结论＝**届次没错**（源件自印「第40届」），
  **问题是渠道**：chemmy 有**公开合集（32~39届）**与**内部培训资料（2026 冬/夏令营，自编 40/41/42 届）**两条线，同挂 `chemy`。
- **定位（三处互证）**：① 源件卷头「第 40 届 Chemy 化学奥林匹克（初赛）模拟试题 10」；② `卷首须知.md` 存原卷卷首同款；
  ③ 同包勘误 PDF 同页并列「第四十一届／第四十二届 Chemy 化学竞赛联赛」＋「第 40 届…模拟试题 10」。PDF 元数据 2026-07-19~23。
- **判定**：站点 manifest `edition` 仅 34~39；全库 12,245 卡 ＋ `chemy试题/` 倒排检索 ⇒ 与 32~39 届**无同题**（新题）；
  `source_file` 指向 **vault 根** `2026机构初赛模拟题/10-chemy/`（**存在、未断链**——此前误判）。
- **处置**：保留届次 ＋ **补渠道标**。`chemy 第40届chemy初赛模拟10 第 5 题` → `chemy 2026夏令营·第40届chemy初赛模拟10 第 5 题`；
  顺带清掉误混入的 `chemy-` 前缀（`chemy chemy-初赛模拟1` → `chemy 2026寒假班·初赛模拟1`）。
- **范围**：内部资料卡 **183**（夏令营 138／寒假班 45）；卷内同步 **7 卷 / 20 处**（学生版无来源行，不含）。
- **未动 `source_norm`**（机制字段，下游 `cmy_*.py` 等消费；改则需重建组卷池）。
- **闸门**：FM strict 183/183；`validate_kb --dir chemy` 2118 文件 **0E/0W**；`render_gate` 183 卡 5 批全 PASS、7 卷 full PASS；
  7 卷 `validate_kb` 1 Warning＝卷 X 第 1578 行 `##→####` **既有标题跳跃**（改动在 229/1079/1774 行，无关）；幂等 0 处。
- **报告**：`09-审计报告/2026-10-14-chemy来源渠道标注.md`。
- **遗留**：① `source_norm` 未改 ⇒ 套名检索仍与公开合集同域；② 化英社(11)／XeChem(5)／壹尖培优(2) 的「第40届」同样疑为内部资料，**未处理**。

### 新增判据
- 🔴🔴 **同机构 ≠ 同来源**：chemmy 公开合集 vs 内部培训资料须**补渠道标**区分。
- 🔴 **届次真伪不能只看机构**：内部资料的「第N届」是自编号（同包勘误 40/41/42 并列即证）。
- 🔴 **判 source_file 断链要试两个根**：`04-题库/…` 与 **vault 根** `2026机构初赛模拟题/…`（原件目录，只读）。
- 🔴 **`source`（人读）与 `source_norm`（机制）分开对待**。
- 📌 **改 FM 脚本必先自测幂等**（本轮首版不幂等，已加守卫）。
"""

P = '.workbuddy/memory/2026-10-14.md'
t = io.open(P, encoding='utf-8').read()
if not t.endswith('\n'):
    t += '\n'
io.open(P, 'w', encoding='utf-8', newline='').write(t + NOTE)
print('memory 追加完成')

P2 = '00-首页/工作日志/2026-10-14.md'
t2 = io.open(P2, encoding='utf-8').read() if os.path.exists(P2) else ''
if t2 and not t2.endswith('\n'):
    t2 += '\n'
io.open(P2, 'w', encoding='utf-8', newline='').write(t2 + NOTE)
print('工作日志追加完成')
