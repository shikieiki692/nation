#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""md_sanitize 本轮新增 3 条规则的单测（含**致命反向用例** `\\cdots`）。"""
import importlib.util
import sys
from pathlib import Path

P = Path(r"C:\Obsidion\妙妙屋\11-模板\scripts\md_sanitize.py")
spec = importlib.util.spec_from_file_location("san", P)
san = importlib.util.module_from_spec(spec)
sys.modules["san"] = san
spec.loader.exec_module(san)

BS = chr(92)
fails = []


def check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        print("   got :", repr(got))
        print("   want:", repr(want))
        fails.append(name)


# ── `\cdot` 紧跟字母 ─────────────────────────────────────────
check("cdotL 补空格", san.sanitize("$c=1.0" + BS + "mathrm{mol}" + BS + "cdotL^{-1}$"),
      "$c=1.0" + BS + "mathrm{mol}" + BS + "cdot L^{-1}$")
check("cdotm 补空格", san.sanitize("$x" + BS + "cdotm$"), "$x" + BS + "cdot m$")
# 🔴 致命反向：`\cdots` 是合法命令，绝不能动（全库 296 处）
src_cdots = "$a_{1}" + BS + "cdots a_{n}$ 与 $b" + BS + "cdots c$"
check("反向·\\cdots 不得被改", san.sanitize(src_cdots), src_cdots)
check("反向·\\cdots 计数守恒", san.sanitize(src_cdots).count(BS + "cdots"), 2)
check("反向·\\cdot 后有空格不动", san.sanitize("$a" + BS + "cdot b$"), "$a" + BS + "cdot b$")

# ── `\hspace{2\mathrm{cm}}` ───────────────────────────────────
check("hspace 去 mathrm 壳",
      san.sanitize("$" + BS + "underline{" + BS + "hspace{2" + BS + "mathrm{cm}}}$"),
      "$" + BS + "underline{" + BS + "hspace{2cm}}$")
check("反向·hspace 正常不动",
      san.sanitize("$" + BS + "hspace{2cm}$"), "$" + BS + "hspace{2cm}$")

# ── `\( … \)` 内的 HTML 实体 ─────────────────────────────────
check("单反斜杠数学内实体",
      san.sanitize("<td>\\(" + " &lt;10^{-8} \\)</td>"), "<td>\\( <10^{-8} \\)</td>")
check("反向·散文里的 &lt; 不动",
      san.sanitize("正文里 a &lt; b 不是数学"), "正文里 a &lt; b 不是数学")
check("$…$ 内实体（原有能力保持）",
      san.sanitize("$x &lt; 10^{-8}$"), "$x < 10^{-8}$")

# ── 幂等 ─────────────────────────────────────────────────────
sample = ("<td>\\( &lt;10^{-8} \\)</td>\n"
          "$c=1.0" + BS + "mathrm{mol}" + BS + "cdotL^{-1}$ 与 $a" + BS + "cdots b$\n"
          "$" + BS + "underline{" + BS + "hspace{2" + BS + "mathrm{cm}}}$\n")
once = san.sanitize(sample)
check("幂等：跑两次等于跑一次", san.sanitize(once), once)

print()
if fails:
    print("❌ 失败 %d 项：%s" % (len(fails), fails))
    sys.exit(1)
print("✅ 全部通过")
