# -*- coding: utf-8 -*-
"""卷 XIII 答案区二轮：清理 OCR 残迹（\dot、^{0} 当态符号、断下标）。"""
import io, os, sys, shutil
sys.stdout.reconfigure(encoding="utf-8")
NL = "\n"
R = r"C:\Obsidion\妙妙屋"
B = "04-题库/2026机构初赛模拟题"
BAK = os.path.join(R, ".workbuddy/tmp/opt_pipe/fixans2_bak")
DRY = "--dry" in sys.argv

FIX = [
    (f"{B}/汇智/题-HZ-03-06-工业上制备氢气的一种方法是于.md", [
        ("Kp0", r"$K_{p}^{0}$", r"$K_{p}^{\ominus}$"),
    ]),
    (f"{B}/清北营/题-QBY-10-01-11298K下在一弹式热量计.md", [
        ("dotH", r"\Delta_{\mathrm{r}}\dot{\mathrm{H}}_{\mathrm{m}}^{\ominus}",
                 r"\Delta_{\mathrm{r}}\mathrm{H}_{\mathrm{m}}^{\ominus}"),
        ("dotD", r"\dot {\Delta} _ {r} U _ {m 2} ^ {0}", r"\Delta_ {\mathrm{r}} U _ {\mathrm{m}} ^{\ominus}"),
        ("th1", r"$\Delta_fH^{\ominus} m(\mathrm{kJ\cdot mol^{-1}})$",
                r"$\Delta_{\mathrm{f}}H_{\mathrm{m}}^{\ominus}/(\mathrm{kJ}\cdot\mathrm{mol}^{-1})$"),
        ("th2", r"$\Delta_{f}H^{0}m(\mathrm{kJ\cdot mol^{-1}})$",
                r"$\Delta_{\mathrm{f}}H_{\mathrm{m}}^{\ominus}/(\mathrm{kJ}\cdot\mathrm{mol}^{-1})$"),
    ]),
]

os.makedirs(BAK, exist_ok=True)
tf = th = 0
un = []
for rel, rules in FIX:
    fp = os.path.join(R, rel)
    raw = io.open(fp, encoding="utf-8-sig", newline="").read()
    new = raw
    hits = []
    for tag, old, tgt in rules:
        n = new.count(old)
        if n == 0:
            un.append((os.path.basename(rel)[:20], tag)); continue
        new = new.replace(old, tgt); hits.append((tag, n))
    if new == raw:
        print("  [无改动]", os.path.basename(rel)[:44]); continue
    tf += 1; th += sum(n for _, n in hits)
    print("  %-46s %s" % (os.path.basename(rel)[:44], " ".join("%s×%d" % t for t in hits)))
    if DRY:
        continue
    bp = os.path.join(BAK, os.path.basename(rel))
    if not os.path.isfile(bp):
        shutil.copy2(fp, bp)
    io.open(fp, "w", encoding="utf-8", newline="").write(new)
print(NL + "%s：%d 文件 / %d 处" % ("[dry]" if DRY else "[apply]", tf, th))
if un:
    print("⚠ 未命中：", un)
