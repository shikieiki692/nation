#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""`\\ce{}` 转换器单测。

覆盖四组能力（均为 2026-09-21 格式线所加/所修）：
  ① mhchem「↑ / ↓ 箭头」：`^` / `v` 作为**独立记号** → `\\uparrow` / `\\downarrow`
  ② mhchem `\\bond{...}` 键型记号（配位键 / 单键）
  ③ **裸电荷并组**：`Cr2O7^2-` → `Cr2O7^{2-}`（正负号必须进上标）
  ④ **带脚本物种的裸数字补下标**：`MnO4^-` → `MnO_{4}^{-}`
  ⑤ **多位数下标**：`C6H12O6` → `C_{6}H_{12}O_{6}`（`\\d` 曾只吃第一位）
  ⑥ **无箭头时 `+` / `-` 是分隔符**：`SiF4 + 2F-` → `SiF_{4} + 2F^{-}`（曾被抬成 `^{+}`）

反向用例（同等重要，防"按形状猜"）：
  - `Mn^{2+}` / `Al^3+` 之类电荷上标不得被动
  - **`R^1-X` / `Ar^1-N=N-Ar^2` 是「上标标号 + 连接号」**，`^1-` 绝不能并成 `^{1-}`
    （全库 26 处；靠负向先行断言 `(?![A-Za-z0-9])` 区分）
  - `\\cdot5H2O` 的系数 5 绝不能被下标到命令上（`\\cdot_{5}`）
  - 常规式（`PCl3`、`2H2O`、`H2O`）输出不得回归
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
ARROW = BS + "rightarrow"
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


# ── ① 正向：气体 ↑（含顺带补下标）────────────────────────────────
check("气体↑·KClO3", conv("2KClO3 -> 2KCl + 3O2 ^"),
      "$2KClO_{3} " + ARROW + " 2KCl + 3O_{2} " + UP + "$")
check("气体↑·MCO3", conv("MCO3 -> MO + CO2 ^"),
      "$MCO_{3} " + ARROW + " MO + CO_{2} " + UP + "$")
check("气体↑·两个箭头", conv("ROH + SOCl2 -> RCl + SO2 ^ + HCl ^"),
      "$ROH + SOCl_{2} " + ARROW + " RCl + SO_{2} " + UP + " + HCl " + UP + "$")
check("气体↑·NO", conv("3As2S3 -> 6H3AsO4 + 28NO ^"),
      "$3As_{2}S_{3} " + ARROW + " 6H_{3}AsO_{4} + 28NO " + UP + "$")

# ── ① 正向：沉淀 ↓ ─────────────────────────────────────────────
check("沉淀↓·Al(OH)3", conv("Al^3+ + 3OH- -> Al(OH)3 v"),
      "$Al^{3+} + 3OH^{-} " + ARROW + " Al(OH)_{3} " + DOWN + "$")
check("沉淀↓·NaBr", conv("CH3CH2CHBrCH3 + NaI -> CH3CH2CHICH3 + NaBr v"),
      "$CH_{3}CH_{2}CHBrCH_{3} + NaI " + ARROW + " CH_{3}CH_{2}CHICH_{3} + NaBr " + DOWN + "$")

# ── ② 正向：`\bond{...}` 键型记号（mhchem）─────────────────────
check("配位键·H3N->BF3", conv("NH3 + BF3 -> H3N" + BS + "bond{->}BF3"),
      "$NH_{3} + BF_{3} " + ARROW + " H_{3}N " + ARROW + " BF_{3}$")
check("配位键·R2C=O", conv("R2C=O" + BS + "bond{->}Al(OiPr)3"),
      "$R_{2}C=O " + ARROW + " Al(OiPr)_{3}$")

# ── ③ 正向：裸电荷并组（正负号进上标）──────────────────────────
check("裸电荷·重铬酸根", conv("Cr2O7^2-"),
      "$Cr_{2}O_{7}^{2-}$")
check("裸电荷·单原子", conv("N^3-"), "$N^{3-}$")

# ── ④ 正向：带脚本物种的裸数字补下标（本次修复的核心）───────────
check("补下标·MnO4^-", conv("MnO4^-"), "$MnO_{4}^{-}$")
check("补下标·CO3^{2-}", conv("CO3^{2-}"), "$CO_{3}^{2-}$")
check("补下标·Li_xC6", conv("Li_xC6"), "$Li_{x}C_{6}$")
check("补下标·[Fe(CN)6]^{3-}", conv("[Fe(CN)6]^{3-}"), "$[Fe(CN)_{6}]^{3-}$")
check("补下标·[Cr(H2O)6]^{3+}", conv("[Cr(H2O)6]^{3+}"), "$[Cr(H_{2}O)_{6}]^{3+}$")
check("补下标·链式 L_nM-CH2-CH2-R", conv("L_nM-CH2-CH2-R"), "$L_{n}M-CH_{2}-CH_{2}-R$")
check("补下标·\\cdot 前段（含箭头）", conv("M_xA_y " + BS + "cdot nH2O -> M_xA_y + nH2O ^"),
      "$M_{x}A_{y} " + BS + "cdot nH_{2}O " + ARROW + " M_{x}A_{y} + nH_{2}O " + UP + "$")
check("补下标·\\cdot 前段（无箭头）", conv("M_xA_y " + BS + "cdot nH2O"),
      "$M_{x}A_{y} " + BS + "cdot nH_{2}O$")

# ── ⑤ 正向：多位数下标（`\d` 曾只吃第一位）────────────────────
check("多位下标·C6H12O6", conv("C6H12O6"), "$C_{6}H_{12}O_{6}$")
check("多位下标·C12H22O11", conv("C12H22O11"), "$C_{12}H_{22}O_{11}$")
check("多位下标·C10H8", conv("C10H8"), "$C_{10}H_{8}$")
check("多位下标·P4O10", conv("P4O10"), "$P_{4}O_{10}$")
check("多位下标·同位素 ^{288}115", conv("^{288}115"), "$^{288}_{115}$")

# ── ⑥ 正向：无箭头时 `+` / `-` 是分隔符，不是带电荷物种 ─────────
check("分隔符·SiF4 + 2F-", conv("SiF4 + 2F-"), "$SiF_{4} + 2F^{-}$")
check("分隔符·H2SO4 + 2NaOH", conv("H2SO4 + 2NaOH"), "$H_{2}SO_{4} + 2NaOH$")
check("分隔符·缓冲对 NH4+ - NH3", conv("NH4+ - NH3"), "$NH_{4}^{+} - NH_{3}$")
check("分隔符·键号 R3P^+ - CHR2^-", conv("R3P^+ - CHR2^-"), "$R_{3}P^{+} - CHR_{2}^{-}$")

# ── 🔴 反向：上标标号 + 连接号，绝不能吞连接号 ─────────────────
check("反向·R^1-X 连接号保住", conv("R^1-X"), "$R^{1}-X$")
check("反向·R^2-CONHR^1", conv("R^2-CONHR^1"), "$R^{2}-CONHR^{1}$")
check("反向·Ar^1-N=N-Ar^2", conv("Ar^1-N=N-Ar^2"), "$Ar^{1}-N=N-Ar^{2}$")

# ── 🔴 反向：命令尾字母不得当下标锚点 ───────────────────────────
check("反向·\\cdot5H2O 系数不并进命令", conv("CuSO4" + BS + "cdot5H2O"),
      "$CuSO_{4}" + BS + "cdot5H_{2}O$")

# ── 🔴 反向：电荷上标不得被改、不得引入箭头 ────────────────────
for src, must in [("Mn^{2+} + 2e- -> Mn", "Mn^{2+}"),
                  ("Al^3+ + 3OH- -> Al(OH)3", "Al^{3+}"),
                  ("H+ + OH- -> H2O", "H^{+}")]:
    out = conv(src)
    ok = (UP not in out) and (DOWN not in out) and (must in out)
    print(("PASS " if ok else "FAIL ") + "反向·" + src)
    if not ok:
        print("   out:", repr(out))
        fails.append("反向·" + src)

# ── 🔴 反向：常规式输出不得回归（无脚本分支的裸数字补下标）──────
check("常规范式·PCl3/Cl2/PCl5", conv("PCl3 + Cl2 -> PCl5"),
      "$PCl_{3} + Cl_{2} " + ARROW + " PCl_{5}$")
check("常规范式·2H2O 系数不被吃", conv("2H2O"), "$2H_{2}O$")
check("常规范式·H2O", conv("H2O"), "$H_{2}O$")

print()
if fails:
    print("❌ 失败 %d 项：%s" % (len(fails), fails))
    sys.exit(1)
print("✅ 全部通过")
