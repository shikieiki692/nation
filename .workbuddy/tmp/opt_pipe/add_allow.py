# -*- coding: utf-8 -*-
r"""登记 render_gate 允许清单（CM-55-05：删游离 $-$ 致 oMath 14→13，full 模式 PASS）。"""
import io, os
os.chdir(r'C:\Obsidion\妙妙屋')
P = '11-模板/scripts/render_gate_allowlist.txt'
B = chr(92)
entry = ('04-题库/2026机构初赛模拟题/chemy/题-CM-55-05-1961年Vaska报导了一.md'
         '\t删去答案行首游离的 `$-$`（原单独计为 1 个 oMath）⇒ 14→13；'
         '内容已按 32 届答案 PDF p41 逐字重写（原式 Δ_TC l＝IrCl 讹变、缺箭头、尾项讹变），full 模式 PASS')
t = io.open(P, encoding='utf-8', newline='').read()
if '题-CM-55-05' in t:
    print('已存在，跳过')
else:
    if not t.endswith('\n'):
        t += '\n'
    io.open(P, 'w', encoding='utf-8', newline='').write(t + entry + '\n')
    print('已登记')
u = io.open(P, encoding='utf-8').read()
print('末行:', repr(u.strip().split('\n')[-1][:120]))
