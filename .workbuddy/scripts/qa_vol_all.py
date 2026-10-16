# -*- coding: utf-8 -*-
r"""卷级「一键闸门」：串跑 ④ 系列全部交付前检查，退出码可直接用于流水线。

用法：
  python qa_vol_all.py --vol XVII              # 跑全部（不含渲染机检）
  python qa_vol_all.py --vol XVII --with-render # 追加 ⑫ 渲染机检（慢，需 LibreOffice）
  python qa_vol_all.py --all                    # 全部已交付卷（X~XVII）

串跑步骤（每步独立进程，失败即计入 FAIL 但**不中断**，末尾统一汇总）：
  ① ④    结构终检        qa_volX2.py --vol <V>
  ② ④-b  交付件综合审计  qa_vol_deliver.py --vol <V>
  ③ ④-c  Å 误包/mathtyping 扫描   scan_mathring.py --vol <V>
  ④ ④-d  表格单元格 OMML 裁切扫描 scan_table_cell_clip.py --vol <V>   （须 pymupdf 解释器）
  ⑤ ④-e  图源覆盖核验（逐题比对源卡图 vs 卷内图）verify_fig_coverage.py --vol <V> --strict
  ⑤ ④-f  单元格越界扫描（渲染几何级：文字跨表格竖线）scan_cell_cross.py --vol <V> --strict
  ⑤ 师/生题面一致        gate_s_t_<V>.py（若存在）
  ⑥ 折行审计            table_wrap_audit.py <学生版.docx> <答案版.docx>
  ⑦ ⑫    渲染机检        qa_vol_render.py --vol <V>                  （仅 --with-render）

★ ④-f 补 ④-d 的结构性盲区（2026-10-15 卷 XII 实测）：
  ④-d 用「PDF 文字层最长前缀匹配」判裁切 ⇒ 对「LibreOffice **视觉裁切**、但文字**仍留在文字层**」
  的形态**会漏报**（XII 第二处热力学表裁切 ④-d 零命中，只报出 1/3）。
  ④-f 改从**渲染几何**判：文字 span 包围盒跨过长竖线（≥12pt）即候选；白名单
  `cellcross_keep.json`。⚠️ 两者**自带独立 PDF 缓存**（`cellcross_out/` vs `render_gate_out/`），
  **重出 docx 后须各自刷新**再扫 —— ④-f 按 docx mtime 自动重渲染，④-d 须手动刷。

★ 与 SOP 的关系：本脚本是 ④ 系列的**执行入口**，判据定义仍以 SOP 为准。
"""
import os, sys, glob, subprocess

ROOT = r"C:\Obsidion\妙妙屋"
O = os.path.join(ROOT, '.workbuddy', 'tmp', 'opt_pipe')
S = os.path.join(ROOT, '.workbuddy', 'scripts')
DOCX = os.path.join(ROOT, '00-首页', '题组Word', '初赛模拟卷', '真题版式')

PY_SYS = r'C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe'
PY_VENV = r'C:\Users\蕾赛\.workbuddy\binaries\python\envs\default\Scripts\python.exe'
# ★ 卷名中缀（有机/非有机）运行时解析：见 .workbuddy/scripts/volname.py
try:
    import volname as VN
except Exception:
    sys.path.insert(0, r'C:\Obsidion\妙妙屋\.workbuddy\scripts')
    import volname as VN


ALL_VOLS = ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'O1']

VOLS = []
for i, a in enumerate(sys.argv):
    if a == '--vol' and i + 1 < len(sys.argv):
        VOLS.append(sys.argv[i + 1])
if '--all' in sys.argv:
    VOLS = ALL_VOLS
WITH_RENDER = '--with-render' in sys.argv
if not VOLS:
    print('用法：qa_vol_all.py --vol <卷号> [--with-render] ｜ --all')
    sys.exit(2)


def step(title, py, args, optional=False):
    cmd = [py, '-X', 'utf8'] + args
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (r.stdout or '') + (r.stderr or '')
    ok = (r.returncode == 0)
    # 抓关键行
    key = ''
    for line in reversed(out.splitlines()):
        s = line.strip()
        if any(k in s for k in ('问题数', 'VERDICT', 'RESULT', '汇总', '结果：', '全部通过')):
            key = s; break
    tag = 'PASS' if ok else ('SKIP' if optional and 'No such file' in out else 'FAIL')
    print('  %-4s %-30s %s' % (tag, title, key[:64]))
    return ok, out


overall_fail = 0
for V in VOLS:
    print('=' * 92)
    print('卷 %s —— 一键闸门' % V)
    print('-' * 92)
    res = []
    res.append(step('④ 结构终检', PY_SYS, [os.path.join(O, 'qa_volX2.py'), '--vol', V]))
    res.append(step('④-b 交付件审计', PY_SYS, [os.path.join(O, 'qa_vol_deliver.py'), '--vol', V]))
    res.append(step('④-c Å误包扫描', PY_SYS, [os.path.join(S, 'scan_mathring.py'), '--vol', V]))
    res.append(step('④-d 表格裁切扫描', PY_VENV, [os.path.join(S, 'scan_table_cell_clip.py'), '--vol', V]))
    res.append(step('④-e 图源覆盖核验', PY_SYS, [os.path.join(S, 'verify_fig_coverage.py'), '--vol', V, '--strict']))
    # ★ 2026-10-15 新增：④-f 渲染几何级单元格越界（补 ④-d 的「视觉裁切但文字仍在文字层」盲区）
    res.append(step('④-f 单元格越界扫描', PY_VENV, [os.path.join(S, 'scan_cell_cross.py'), '--vol', V, '--strict']))
    # ★ 2026-10-16：⑤ 师/生题面一致 **通用化** —— 原仅 XVI/XVII 有专用脚本、其余卷恒 SKIP（A 线盲区）。
    #   优先级：专用 gate_s_t_<V>.py → 旧 <vol>_consistency.py → **通用 scripts/gate_s_t.py --vol V**。
    st = os.path.join(O, 'gate_s_t_%s.py' % V)
    if not os.path.exists(st):
        st = os.path.join(O, '%s_consistency.py' % V.lower())
    if os.path.exists(st):
        res.append(step('⑤ 师/生题面一致', PY_SYS, [st]))
    else:
        res.append(step('⑤ 师/生题面一致', PY_SYS, [os.path.join(S, 'gate_s_t.py'), '--vol', V]))
    d_stu = VN.docx_path(V, '学生版·真题版式')
    d_ans = VN.docx_path(V, '答案与解析版·真题版式')
    if os.path.isfile(d_stu) and os.path.isfile(d_ans):
        res.append(step('⑥ 折行审计', PY_SYS, [os.path.join(S, 'table_wrap_audit.py'), d_stu, d_ans]))
    if WITH_RENDER:
        res.append(step('⑦ 渲染机检', PY_VENV, [os.path.join(O, 'qa_vol_render.py'), '--vol', V]))
    fails = [i for i, (ok, _) in enumerate(res) if not ok]
    overall_fail += len(fails)
    print('  → 本卷结果：%s' % ('全部通过 ✅' if not fails else '%d 项 FAIL ❌' % len(fails)))

print('=' * 92)
print('总结果：%s' % ('ALL PASS ✅' if overall_fail == 0 else '%d 项失败 ❌' % overall_fail))
sys.exit(1 if overall_fail else 0)
