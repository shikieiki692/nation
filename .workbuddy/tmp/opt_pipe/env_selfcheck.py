# -*- coding: utf-8 -*-
"""env_selfcheck.py —— 管线「环境自检」（P2-12，2026-10-11）。

为什么需要：本日实测两次「不是内容问题、而是环境被重置」的事故：
  ① pre-commit 闸门（render-gate）硬编码受管 py3.13.12 ⇒ 该解释器缺
     pyyaml / python-docx / pypandoc 时，**任何提交都会失败**（报的是「公式渲染问题」，极易误判）；
  ② 受管 venv 缺 pymupdf/PIL/numpy 时，渲染机检与视觉核验脚本直接崩。
本脚本把两条链路的关键依赖与外部程序一次性验掉，**在动工前**跑 3 秒即可定位环境问题。

用法：python env_selfcheck.py        # 退出码 0=全绿；1=有缺项（附修复命令）
"""
import importlib
import os
import subprocess
import sys

HOOK_PY = r"C:\Users\蕾赛\.workbuddy\binaries\python\versions\3.13.12\python.exe"
VENV_PY = r"C:\Users\蕾赛\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
PY312 = r"C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe"
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

CHECKS = [
    # (解释器, 模块, 用途, 修复命令模板)
    (HOOK_PY, "yaml", "pre-commit render-gate（render_gate.py）", "pip install pyyaml"),
    (HOOK_PY, "docx", "render-gate 载入 build-all-handout-docx", "pip install python-docx"),
    (HOOK_PY, "pypandoc", "render-gate 真跑 pandoc 断言渲染", "pip install pypandoc_binary"),
    (VENV_PY, "pymupdf", "qa_vol_render / 视觉核验 / 源 PDF 抽取", "pip install pymupdf"),
    (VENV_PY, "PIL", "qa_vol_render 像素分析 / 拼图 / 裁图", "pip install pillow"),
    (VENV_PY, "numpy", "qa_vol_render 向量化 ink 统计", "pip install numpy"),
    (PY312, "ruamel.yaml", "FM 严格解析（js-yaml4 等价）", "pip install ruamel.yaml"),
]


def probe(py, mod):
    if not os.path.exists(py):
        return None, "解释器不存在"
    code = "import %s, sys; print('ok')" % mod
    r = subprocess.run([py, "-c", code], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode == 0:
        return True, ""
    return False, (r.stderr or "").strip().splitlines()[-1][:70] if r.stderr else "导入失败"


def main():
    global CHECKS
    if "--selftest" in sys.argv:          # ★ 自证：注入一个必然缺失的依赖，必须报 FAIL 且退出码 1
        CHECKS = CHECKS + [(VENV_PY, "_no_such_module_", "自证用假依赖", "pip install <不存在>")]
    bad = []
    print("== 解释器 ==")
    for p in (HOOK_PY, VENV_PY, PY312):
        print("  %-70s %s" % (p, "OK" if os.path.exists(p) else "缺失"))
        if not os.path.exists(p):
            bad.append(("解释器", p, "重新安装受管运行时"))
    print("\n== 依赖 ==")
    for py, mod, why, fix in CHECKS:
        ok, err = probe(py, mod)
        tag = "OK  " if ok is True else ("缺失" if ok is False else "跳过")
        print("  [%s] %-12s %-46s %s" % (tag, mod, why, err))
        if ok is not True:
            bad.append((mod, os.path.basename(py), fix))
    print("\n== 外部程序 ==")
    ok = os.path.exists(SOFFICE)
    print("  [%s] LibreOffice %s" % ("OK  " if ok else "缺失", SOFFICE))
    if not ok:
        bad.append(("soffice", SOFFICE, "安装 LibreOffice（docx→PDF 全链路依赖）"))
    print("\n" + "=" * 72)
    if not bad:
        print("✅ 全绿：环境可支撑组卷／闸门／提交全链路。")
        return 0
    print("⛔ 缺 %d 项，修复建议：" % len(bad))
    for name, where, fix in bad:
        print("   · %-14s @%-22s → %s" % (name, where, fix))
    print("\n提示：受管 3.13.12 的包用 `%s -m pip install <pkg>`（该解释器被 pre-commit 钩子硬编码）。" % HOOK_PY)
    return 1


if __name__ == "__main__":
    sys.exit(main())
