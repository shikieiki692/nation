# -*- coding: utf-8 -*-
"""修复第3题 5-2 式：把「行尾 $$」畸形改为两个段落式行内公式。"""
import io, os, sys, shutil
sys.stdout.reconfigure(encoding="utf-8")
NL = "\n"
R = r"C:\Obsidion\妙妙屋"
fp = os.path.join(R, "04-题库/2026机构初赛模拟题/清北营/题-QBY-02-05-本题记丙酮为A二氯甲烷为B在.md")
BAK = os.path.join(R, ".workbuddy/tmp/opt_pipe/fixans_bak")

VAP = r"\frac{\Delta \text{vapHm}^{\ominus}"
TAIL = r"}{R}\left( {\frac{1}{313.15} - \frac{1}{T}}\right)\right]"
EA = r"\exp\left[" + VAP + r"(\mathrm{A})" + TAIL
EB = r"\exp\left[" + VAP + r"(\mathrm{B})" + TAIL

OLD = ("**5-2(5分)** $\\gamma_A=\\exp(A \\cdot x_B^2)=1.058$ (1分) $\\gamma_B=\\exp(A \\cdot x_A^2)=1.659$ (1分) $$" + NL
       + r"1={0.75} \times {0.42} \times " + EA + r" \times \gamma_A" + NL
       + "$$" + NL + NL + "$$" + NL
       + r"+\ {0.25} \times {0.98} \times " + EB + r" \times \gamma_B" + NL
       + "$$" + NL + NL + "（1 分）解得 T=321.9K (2分)")

NEW = ("**5-2(5分)** $\\gamma_A=\\exp(A \\cdot x_B^2)=1.058$ (1分) $\\gamma_B=\\exp(A \\cdot x_A^2)=1.659$ (1分)" + NL + NL
       + r"$1={0.75} \times {0.42} \times " + EA + r" \times \gamma_A$" + NL + NL
       + r"$+\ {0.25} \times {0.98} \times " + EB + r" \times \gamma_B$" + NL + NL
       + "（1 分）解得 T=321.9K (2分)")

raw = io.open(fp, encoding="utf-8-sig", newline="").read()
n = raw.count(OLD)
print("命中:", n)
if n != 1:
    print("⚠ 未唯一命中，放弃"); raise SystemExit(1)
out = raw.replace(OLD, NEW)
if not os.path.isfile(os.path.join(BAK, os.path.basename(fp))):
    shutil.copy2(fp, os.path.join(BAK, os.path.basename(fp)))
io.open(fp, "w", encoding="utf-8", newline="").write(out)
print("已修复。当前区域：")
for ln in out.split(NL)[73:84]:
    print("   ", ln[:120])
