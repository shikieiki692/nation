# -*- coding: utf-8 -*-
"""fix_xiii_fmt2.py —— 卷 XIII 用卡「单位与饱和蒸气压标记」规范化（RMW · 幂等）。

A. `p^{\bullet}` / `p_A^*` ⇒ `p_{A}^{\ast}`（源卡用 bullet 表星号、且题面/答案不一致）
B. `kJ/mol`（含 \text{} / \mathrm{} / 裸写）⇒ `\mathrm{kJ\cdot mol^{-1}}`（数学模式内）或 `$\mathrm{kJ\cdot mol^{-1}}$`（正文中）
C. `(kJ/mol)` / `(J/mol·K)` ⇒ 规范单位（表格标题）

用法：python fix_xiii_fmt2.py --dry | --apply
"""
import io, json, os, re, shutil, sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
PLAN = os.path.join(R, ".workbuddy/tmp/opt_pipe/vol_plan_XIII.json")
BAK = os.path.join(R, ".workbuddy/tmp/opt_pipe/xiii_fmt2_bak")
DRY = "--dry" in sys.argv


def in_math(txt, pos):
    return txt[:pos].count("$") % 2 == 1


def fix(t):
    n = 0
    # A. 饱和蒸气压标记
    t, k = re.subn(r"p\s*_\s*\{?([AB])\}?\s*\^\s*\{?\s*\\bullet\s*\}?", r"p_{\1}^{\\ast}", t); n += k
    t, k = re.subn(r"p\s*_\s*\{?([AB])\}?\s*\^\s*\*", r"p_{\1}^{\\ast}", t); n += k
    # B1. \text{kJ/mol} / \mathrm{kJ/mol}
    t, k = re.subn(r"\\text\{\s*kJ\s*/\s*mol\s*\}", r"\\mathrm{kJ\\cdot mol^{-1}}", t); n += k
    t, k = re.subn(r"\\mathrm\{kJ\s*/\s*mol\}", r"\\mathrm{kJ\\cdot mol^{-1}}", t); n += k
    # B2. 剩余裸写 kJ/mol：按是否在数学模式内分别处理
    out, last = [], 0
    for m in re.finditer(r"kJ\s*/\s*mol", t):
        out.append(t[last:m.start()])
        out.append(r"\mathrm{kJ\cdot mol^{-1}}" if in_math(t, m.start())
                   else r"$\mathrm{kJ\cdot mol^{-1}}$")
        last = m.end(); n += 1
    out.append(t[last:])
    t = "".join(out)
    # C. 表格标题单位
    t, k = re.subn(r"\(\s*kJ\s*/\s*mol\s*\)", r"($\\mathrm{kJ\\cdot mol^{-1}}$)", t); n += k
    t, k = re.subn(r"\(\s*J\s*/\s*mol\s*[·・]\s*K\s*\)", r"($\\mathrm{J\\cdot mol^{-1}\\cdot K^{-1}}$)", t); n += k
    return t, n


def main():
    plan = json.load(io.open(PLAN, encoding="utf-8"))
    cards = [c["path"] for _m, lst in plan for c in lst]
    os.makedirs(BAK, exist_ok=True)
    tot, changed = 0, 0
    for rel in cards:
        fp = os.path.join(R, rel)
        raw = io.open(fp, encoding="utf-8-sig").read()
        if "\r\n" in raw:
            print("  [CRLF]", os.path.basename(rel)); continue
        new, n = fix(raw)
        if n == 0:
            continue
        chk, _ = fix(raw)
        if chk != new:
            print("  [复核不通过]", os.path.basename(rel)); continue
        changed += 1; tot += n
        print("   %-42s %d 处  %d→%d" % (os.path.basename(rel)[:40], n, len(raw), len(new)))
        if not DRY:
            shutil.copy2(fp, os.path.join(BAK, rel.replace("/", "__")))
            io.open(fp, "w", encoding="utf-8", newline="\n").write(new)
    print("%s：%d 卡 / %d 处" % ("(dry)" if DRY else "已写盘", changed, tot))


if __name__ == "__main__":
    main()
