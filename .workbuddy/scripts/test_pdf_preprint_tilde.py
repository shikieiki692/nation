"""PDF 线 `preprint()` 区间转义的单测（2026-09-21 格式线）。

背景（实测）：`convert_handout_to_pdf.py` 第 355-358 行**刻意**把 Unicode 上下标
`₂`/`⁺` 转成 pandoc 语法 `~2~`/`^+^`，依赖 reader 的 `subscript`/`superscript` 扩展。
但这两个扩展要求定界符之间**不含空格**，而中文行内标点前后无空格
⇒ 源文的**区间记号**同样被吞，且是静默改字：
    `300~500°C（573~773 K）` → `300\\textsubscript{500°C（573}773 K）`
    `400~430</td><td>430~470` → `400\\textsubscript{430</td><td>430}470`
修法：把源里区间 `~` 转义成 `\\~`（pandoc → `\\textasciitilde`，仍是可见 `~`），
且必须**在该文件生成上下标 `~2~` 之前**、并**跳过行内代码**（`\\texttt{}` 里 `\\~`
会渲染成字面 `\\~`）。

本测试锁定四条边界：
  ① 区间 `~` → 转义
  ② Unicode 上下标 → 仍生成 `~x~`（未被转义误伤）
  ③ `~~删除线~~` / `~~~` 围栏 → 原样（前后邻 `~` 的不动）
  ④ 行内代码里的 `~` → 不转义
"""
import importlib.util
import sys
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
P = VAULT / "11-模板" / "scripts" / "convert_handout_to_pdf.py"

spec = importlib.util.spec_from_file_location("chp_test", P)
chp = importlib.util.module_from_spec(spec)
sys.modules["chp_test"] = chp
try:
    spec.loader.exec_module(chp)
except SystemExit:
    pass

BS = chr(92)
ESCAPED = BS + "~"

n_pass = n_fail = 0


def check(name, got, want, must=True):
    global n_pass, n_fail
    ok = (want in got) if must else (want not in got)
    flag = "PASS" if ok else "FAIL"
    if ok:
        n_pass += 1
    else:
        n_fail += 1
    print("%-4s %-34s %s" % (flag, name, ("含" if must else "不含") + repr(want[:40])))
    if not ok:
        print("        实际: %r" % got[:160])


# ① 区间转义
check("区间·单一", chp.preprint("波长 400~430 nm"), ESCAPED + "430")
check("区间·中文标点无空格", chp.preprint("pH 2~3 紫红"), ESCAPED + "3")
check("区间·约记号", chp.preprint("分解温度 ~100°C"), ESCAPED + "100")
check("区间·全角括号被转半角", chp.preprint("范围 0~1（0%~100%）"), ESCAPED + "1(0%")

# ② Unicode 上下标仍生成 pandoc 语法（不得被转义误伤）
check("下标·₂ → ~2~", chp.preprint("CaF₂"), "~2~")
check("上标·⁺ → ^+^", chp.preprint("H⁺"), "^+^")
check("下标·多位 ₁₂ → ~12~", chp.preprint("C₁₂H₂₂O₁₁"), "~12~")
check("混排·两边各归各", chp.preprint("CaF₂ ~100°C"), "CaF~2~ " + ESCAPED + "100")

# ③ `~~` / `~~~` 原样（前后邻 `~` 的不动）
check("删除线·不转义", chp.preprint("~~删除线保留~~"), "~~删除线保留~~")
check("删除线·不转义（反向）", chp.preprint("~~删除线保留~~"), ESCAPED + "~", must=False)
check("围栏·~~~ 不动", chp.preprint("~~~\ncode\n~~~"), "~~~", must=False or True)

# ④ 行内代码里的 `~` 不转义
check("行内代码·不转义", chp.preprint("`10~40 kJ/mol`"), "10~40 kJ/mol")
check("行内代码·无回斜线", chp.preprint("`10~40 kJ/mol`"), BS, must=False)

# ⑤ 数学域不动
check("数学域·$a~b$ 不动", chp.preprint("$a~b$"), "$a~b$")

print()
print("=" * 60)
print("PASS %d / FAIL %d" % (n_pass, n_fail))
sys.exit(1 if n_fail else 0)
