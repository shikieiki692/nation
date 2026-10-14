# -*- coding: utf-8 -*-
r"""CM-48-05：更新校勘注（写实——原注称已核实但实际未改；本轮已 16 处径改）。"""
import io, os
os.chdir(r'C:\Obsidion\妙妙屋')
B = chr(92)
p = '04-题库/真题/chemy/题-CM-48-05-向含有少量酚酞指示剂的水溶液.md'
t = io.open(p, encoding='utf-8-sig').read()
old = ('> [!note] ⛔ 校勘注（本卡公式已回原 PDF 逐条核实）\n'
       '> PDF p10~p13：Kₐ(H₂SO₃)=1.2×10⁻²、第二级 K₂(HSO₃⁻)；速率常数 k(HSO₃⁻)=4.5×10⁻³、'
       'k(SO₃²⁻)=54 dm³·mol⁻¹·s⁻¹；a=0.10 mol·dm⁻³、c(Na₂SO₃)=0.010 mol·dm⁻³。源把下标 a 误识为 `' + B + 'bullet`、'
       'K₂ 误识为 `K_*`、l 误识为数字 1（「11 SO₃」＝lSO₃⁻）、「Nall SO₃」＝NaHSO₃、O⁻ 误识为 `' + B + 'bar{O}`，'
       '均已径改。物料/电荷守恒两式按 p13 原卷补正。')
new = ('> [!note] ⛔ 校勘注（2026-10-14：已回原**扫描 PDF** 逐条核实重录）\n'
       '> 源件是**扫描件**（文本层为空、每页仅 8 字页码戳）⇒ 只能**渲图目读**：5-1 原文见 PDF **p12**，5-2~5-3 见 **p13**。\n'
       '> 讹变类型：`l` 被误识为数字 `1`（「11 SO₃」＝ lSO₃⁻）、「Nall SO₃」＝ NaHSO₃、`O⁻`→`' + B + 'bar{O}`、'
       '`[H⁺]`→`|' + B + 'mathrm{II}^{*}|`、`HOCH₂SOj`＝ HOCH₂SO₃⁻、`' + B + D if False else '`' + B + 'Delta 3 =`＝脱漏片段。\n'
       '> **本轮径改 16 处**：题面 4 处（NaHSO₃ 不带电荷／(HSO₃⁻)／[SO₃²⁻][HSO₃⁻]／尾随 `e`）；'
       '答案 5-1 三处、5-2-1 三处（物料守恒／电荷守恒／注1）、注2 两式、5-2-2 两式（两量顺序＋[HSO₃⁻]）、'
       '5-3-1（速率式＋a 式＋注2/注3 断行）、5-3-3（删游离 `(HCHO]`）。')
print('命中:', t.count(old))
assert t.count(old) == 1, '校勘注未按预期命中，未写盘'
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(old, new))
print('✅ 已更新校勘注；%d 字节' % len(t))
