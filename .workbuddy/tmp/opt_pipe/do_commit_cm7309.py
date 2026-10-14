# -*- coding: utf-8 -*-
r"""提交：CM-73-09 电荷修复 + T1 存疑处置（显式清单，不用目录 status）。"""
import os, subprocess, sys, time
ROOT = r'C:\Obsidion\妙妙屋'
T = '.workbuddy/tmp/opt_pipe/'
PATHS = [
    '04-题库/2026机构初赛模拟题/chemy/题-CM-73-09-簇合物在主族元素发展中起着比.md',
] + [T + x for x in ['dump_8.py', 'scan_deltasym.py', 'fix_cm7309.py', 'write_8.py']] + [
    '09-审计报告/2026-10-14-T1-chemy-D1D2修复.md',
    '00-首页/工作日志/2026-10-14.md',
    '.workbuddy/memory/2026-10-14.md',
]
MSG = ('fix(T1): CM-73-09 残缺电荷上标修复（\\Delta^2 → 2-）＋ 存疑 7 处登记；T1 全线收官\n\n'
       '- 已修：题面区 \\mathrm{\\Delta}^{2}$ - → ^{2-}$；判据＝同题参考答案区自证（答案区写 C(Nt-Bu)_3^{2-}）\n'
       '  复验 gate_docx：失败 0 / 字面$ 0 / oMath 11\n'
       '- 登记不修 7 处（属另一类＝OCR 讹变化学符号/角标，需重构）：\n'
       '  CM-56-02(5) Δφ/Δ(/Δξ 下标混入＋块前 3 行孤立「-」；CM-55-05(2) Δ_{TC}l ＝「IrCl」被讹变；CM-48-05(1) 公式整段损坏\n'
       '- 附带澄清：\\Delta_{X}（非热力学下标）不是缺陷类 —— 全库 1353 处抽样绝大多数合法\n'
       '  （Δ_fH/Δ_rH/Δ_o 晶体场分裂能/Δ_{vup}H/Δ_{sov}H）⇒ 白名单不可穷举，不立类\n'
       '- 闸门：FM strict True；validate_kb 0E/0W')

def run(a):
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')

r = run(['git', 'add', '-f', '--'] + PATHS)
if r.returncode != 0:
    print('add 失败'); print(r.stderr[-400:]); sys.exit(1)
got = [x for x in run(['git', '-c', 'core.quotepath=false', 'diff', '--cached', '--name-only']).stdout.split('\n') if x]
if sorted(got) != sorted(PATHS):
    print('⚠️ staged 不符'); print(' 额外:', sorted(set(got) - set(PATHS))[:8]); print(' 缺失:', sorted(set(PATHS) - set(got))[:8]); sys.exit(2)
print('staged == PATHS (%d) ✓' % len(PATHS))
for i in range(5):
    r = run(['git', 'commit', '--only', '-m', MSG, '--'] + PATHS)
    if r.returncode == 0:
        print(r.stdout[-140:]); break
    if 'cannot lock ref' in (r.stderr or ''):
        time.sleep(1.5); continue
    print('commit 失败'); print(r.stdout[-400:]); print(r.stderr[-400:]); sys.exit(3)
else:
    sys.exit(3)
run(['git', 'reset', '-q', 'HEAD', '--'] + PATHS)
out = run(['git', '-c', 'core.quotepath=false', 'show', '--stat', 'HEAD']).stdout
import re
print(re.findall(r'\d+ files? changed.*', out))
print('delete/rename 行:', [l for l in out.split('\n') if 'delete mode' in l or '=>' in l] or '无 ✓')
