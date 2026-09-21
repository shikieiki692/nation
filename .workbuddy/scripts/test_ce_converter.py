#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""`\\ce{}` 转换器「↑ / ↓ 箭头」单测（2026-09-21 新增能力）。

正向：`^` / `v` 作为**独立记号** → `\\uparrow` / `\\downarrow`（并顺带补下标）。
反向：`Mn^{2+}` / `Al^3+` 这类**电荷上标**绝不能被动；常规式输出必须与改前逐字一致。

⚠️ 已知既有瑕疵（本次不修，报备）：
   `\\ce{M_xA_y \\cdot nH2O}` —— 同一个「species」里若同时含 `_` 与裸数字，
   `_parse_species` 的 early-return 分支只规范 `^`/`_`、**不补裸数字下标**，
   故 `nH2O` 保持原样（不在 `\\cdot` 那个 token 里的 `nH2O` 则正常）。
   这是改前就有、且不导致渲染失败的问题，故用例按**现状**锁定，避免掩盖。
"""
import importlib.util
import sys
from pathlib import Path

P = Path(r"C:\Obsidion\妙妙屋\11-模板\scripts\build-all-handout-docx.py")
spec = importlib.util.spec_from_file_location("bh", P)
bh = importlib.util.module_from_spec(spec)
sys.modules["bh"] = bh
try:
    spec.loader.exec_module(bh)
except SystemExit:
    pass

f = bh._preprocess_ce_in_math
BS = chr(92)
UP = BS + "uparrow"
DOWN = BS + "downarrow"
fails = []


def conv(inner: str) -> str:
    return f("$" + BS + "ce{" + inner + "}$")


def check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        print("   got :", repr(got))
        print("   want:", repr(want))
        fails.append(name)


# ── 正向：气体 ↑（含顺带补下标）────────────────────────────────
check("气体↑·KClO3", conv("2KClO3 -> 2KCl + 3O2 ^"),
      "$2KClO_{3} " + BS + "rightarrow 2KCl + 3O_{2} " + UP + "$")
check("气体↑·MCO3", conv("MCO3 -> MO + CO2 ^"),
      "$MCO_{3} " + BS + "rightarrow MO + CO_{2} " + UP + "$")
check("气体↑·两个箭头", conv("ROH + SOCl2 -> RCl + SO2 ^ + HCl ^"),
      "$ROH + SOCl_{2} " + BS + "rightarrow RCl + SO_{2} " + UP + " + HCl " + UP + "$")
check("气体↑·NO", conv("3As2S3 -> 6H3AsO4 + 28NO ^"),
      "$3As_{2}S_{3} " + BS + "rightarrow 6H_{3}AsO_{4} + 28NO " + UP + "$")
check("已知瑕疵·\\cdot token 内裸数字不补下标",
      conv("M_xA_y " + BS + "cdot nH2O -> M_xA_y + nH2O ^"),
      "$M_{x}A_{y} " + BS + "cdot nH2O " + BS + "rightarrow M_{x}A_{y} + nH_{2}O " + UP + "$")

# ── 正向：沉淀 ↓ ─────────────────────────────────────────────
check("沉淀↓·Al(OH)3", conv("Al^3+ + 3OH- -> Al(OH)3 v"),
      "$Al^{3}+ + 3OH^{-} " + BS + "rightarrow Al(OH)_{3} " + DOWN + "$")
check("沉淀↓·NaBr", conv("CH3CH2CHBrCH3 + NaI -> CH3CH2CHICH3 + NaBr v"),
      "$CH_{3}CH_{2}CHBrCH_{3} + NaI " + BS + "rightarrow CH_{3}CH_{2}CHICH_{3} + NaBr " + DOWN + "$")

# ── 正向：`\bond{...}` 键型记号（mhchem）─────────────────────
ARROW = BS + "rightarrow"
check("配位键·H3N->BF3", conv("NH3 + BF3 -> H3N" + BS + "bond{->}BF3"),
      "$NH_{3} + BF_{3} " + ARROW + " H_{3}N " + ARROW + " BF_{3}$")
check("配位键·R2C=O", conv("R2C=O" + BS + "bond{->}Al(OiPr)3"),
      "$R_{2}C=O " + ARROW + " Al(OiPr)_{3}$")
print("   （Stille 实际行）->", repr(conv(
    "Br-Ar-CHO(OH) + " + BS + "bond{1} SnBu3 ->[?] " + BS + "bond{1}-Ar-CHO(OH)")))

# ── 反向：电荷上标不得被改、不得引入箭头 ─────────────────────
for src, must in [("Mn^{2+} + 2e- -> Mn", "Mn^{2+}"),
                  ("Al^3+ + 3OH- -> Al(OH)3", "Al^{3}+"),
                  ("H+ + OH- -> H2O", "H^{+}")]:
    out = conv(src)
    ok = (UP not in out) and (DOWN not in out) and (must in out)
    print(("PASS " if ok else "FAIL ") + "反向·" + src)
    if not ok:
        print("   out:", repr(out))
        fails.append("反向·" + src)

# ── 反向：常规式（无箭头记号）输出逐字不变 ───────────────────
check("常规式不变", conv("PCl3 + Cl2 -> PCl5"),
      "$PCl_{3} + Cl_{2} " + BS + "rightarrow PCl_{5}$")

print()
if fails:
    print("❌ 失败 %d 项：%s" % (len(fails), fails))
    sys.exit(1)
print("✅ 全部通过")
