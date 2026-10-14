# -*- coding: utf-8 -*-
r"""登记 render_gate 允许清单（2 卡：×10 $^{n}$ 合并致 oMath −1，full PASS）。"""
import io, os
os.chdir(r'C:\Obsidion\妙妙屋')
P = '11-模板/scripts/render_gate_allowlist.txt'
t = io.open(P, encoding='utf-8', newline='').read()
if not t.endswith('\n'):
    t += '\n'
ADD = [
    ('04-题库/真题/第34届决赛/理论/题-34决理-2-3-2-MOF溶剂分子推断.md',
     'fspace_g 修「×10 $^{10}$」→「×10$^{10}$」（科学计数法指数应与 10 同公式）；oMath 13→12 系相邻公式合并，full 模式 PASS'),
    ('04-题库/真题/第38届决赛/理论/题-38决理-5-乙醇代谢中的反应.md',
     'fspace_g 修「×10 $^{-5}$」→「×10$^{-5}$」（同上）；oMath 110→109 系相邻公式合并，full 模式 PASS'),
]
n = 0
for p, why in ADD:
    if p in t:
        print('已存在，跳过:', p[-30:]); continue
    t += p + '\t' + why + '\n'
    n += 1
io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('新增 %d 条' % n)
u = io.open(P, encoding='utf-8').read()
for l in u.strip().split('\n')[-2:]:
    print('  ', l[:120])
