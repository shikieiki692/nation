# -*- coding: utf-8 -*-
"""卷 XIII 答案区「视觉核验」发现问题的源卡修复。
RMW（读当前磁盘 → 精确替换 → 写回）；幂等；备份；规则级 unmatched 报告。
用法：--dry 预览 / --apply 落盘
"""
import io, os, sys, shutil

sys.stdout.reconfigure(encoding="utf-8")
NL = "\n"
R = r"C:\Obsidion\妙妙屋"
B = "04-题库/2026机构初赛模拟题"
BAK = os.path.join(R, ".workbuddy/tmp/opt_pipe/fixans_bak")
DRY = "--dry" in sys.argv

VAP = r"\frac{\Delta \text{vapHm}^{\ominus}"
TAIL = r"}{R}\left( {\frac{1}{313.15} - \frac{1}{T}}\right)\right]"
EXP_A_OLD = r"\exp\left[" + VAP + r"(\Lambda)" + TAIL
EXP_A = r"\exp\left[" + VAP + r"(\mathrm{A})" + TAIL
EXP_B = r"\exp\left[" + VAP + r"(\mathrm{B})" + TAIL

FIX = [
    # ── 第2题：源答案 ΔmelSm 计算笔误（15355/1808≈8.494 ≠ 8.5924）⇒ 径改整链 + 校勘注
    (f"{B}/质心UChO/题-UChO-01-04-标准压力下Fes的熔点为18.md", [
        ("sm1808",
         r"= 8.5924 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1} 1",
         r"= 8.494 \mathrm{J} \cdot \mathrm{K} ^ {- 1} \cdot \mathrm{mol} ^ {- 1} （1 分）"),
        ("sm1673",
         r"= 8.4950 \mathrm{JK} ^ {- 1} \mathrm{mol} ^ {- 1}",
         r"= 8.397 \mathrm{J} \cdot \mathrm{K} ^ {- 1} \cdot \mathrm{mol} ^ {- 1}"),
        ("dGm",
         r"= 973.44 \mathrm{Jmol} ^ {- 1}",
         r"= 1138 \mathrm{J} \cdot \mathrm{mol} ^ {- 1}"),
        ("Kpp",
         r"K^{\ominus} = \exp \left[ - \Delta_ {\mathrm{mel}} G _ {\mathrm{m}}^{\ominus} / R T \right] = 0.931" + NL + "$$" + NL + NL + "也可以直接利用",
         r"K^{\ominus} = \exp \left[ - \Delta_ {\mathrm{mel}} G _ {\mathrm{m}}^{\ominus} / R T \right] = 0.921" + NL + "$$" + NL + NL
         + r"（校勘：源答案将 $\Delta_{\mathrm{mel}}S_{\mathrm{m}}(1808\ \mathrm{K})$ 印作 8.5924，与 $15355/1808 \approx 8.494$ 不符，系笔误；此处已更正，$K^{\ominus}$ 相应为 0.921。）"
         + NL + NL + "也可以直接利用"),
        ("mark1", "，1分代入", "，（1 分）代入"),
        ("mark2", r"\mathrm{J mol^{-1}}$ 1分", r"\mathrm{J mol^{-1}}$ （1 分）"),
        ("mark3",
         r"\frac {13086}{T} + I ^ {\prime} 2 \text {分}" + NL + "$$",
         r"\frac {13086}{T} + I ^ {\prime}" + NL + "$$" + NL + NL + "（2 分）"),
        ("mark4", r"2.175T$ 2分", r"2.175T$ （2 分）"),
        ("mark5", "代入 1673 K 数据即可求解 2 分", "代入 1673 K 数据即可求解 （2 分）"),
        ("mark6", r"= 0.93 / 0.87 = 1.1$ 2 分", r"= 0.92 / 0.87 = 1.1$ （2 分）"),
    ]),
    # ── 第3题：5-2 长式拆行（超页宽被裁）；A 被 OCR 成 Λ
    (f"{B}/清北营/题-QBY-02-05-本题记丙酮为A二氯甲烷为B在.md", [
        ("split",
         r"$1=0.75 \times {0.42} \times " + EXP_A_OLD + r" \times \gamma_A+0.25 \times {0.98} \times " + EXP_B + r" \times \gamma_B$ (1分)",
         "$$" + NL + r"1={0.75} \times {0.42} \times " + EXP_A + r" \times \gamma_A" + NL + "$$" + NL + NL
         + "$$" + NL + r"+\ {0.25} \times {0.98} \times " + EXP_B + r" \times \gamma_B" + NL + "$$" + NL + NL + "（1 分）"),
        ("Lambda", r"\text{vapHm}^{\ominus}(\Lambda)", r"\text{vapHm}^{\ominus}(\mathrm{A})"),
    ]),
    # ── 第4题：源题号行；β₂ 分母应为平方；双括号
    (f"{B}/北京夏令营/题-BJLY-01-05-已知51计算1L100mol.md", [
        ("head", "## 参考答案" + NL + NL + "第5题" + NL + NL + "5-1" + NL + NL + "电荷守恒：", "## 参考答案" + NL + NL + "5-1 电荷守恒："),
        ("beta", r"\beta_2[NH_3]_2}", r"\beta_2[NH_3]^{2}}"),
        ("p1", r"\left(（1 分）\right)", "（1 分）"),
        ("p2", r"\left(（2 分）\right)", "（2 分）"),
    ]),
    # ── 第6题：源题号行
    (f"{B}/chemy/题-CM-100-01-氯苯A和溴苯B可以形成理想液.md", [
        ("head", "## 参考答案" + NL + NL + "第1题（10分）" + NL + NL, "## 参考答案" + NL + NL),
    ]),
    # ── 第7题：7-3 答案表格首列应为 SO₂
    (f"{B}/壹尖培优/题-YJ-02-02-酸雨是指pH小于56的降水主.md", [
        ("tbl", r"<table><tr><td> $SO_{3}$ </td><td> $O_{2}$ </td><td> $SO_{3}$ </td></tr><tr><td>1-2x</td>",
                r"<table><tr><td> $SO_{2}$ </td><td> $O_{2}$ </td><td> $SO_{3}$ </td></tr><tr><td>1-2x</td>"),
    ]),
    # ── 第8题：源题号行
    (f"{B}/chemy/题-CM-83-03-3-1向20mL浓度为mol.md", [
        ("head", "## 参考答案" + NL + NL + "第3题（8分）" + NL + NL, "## 参考答案" + NL + NL),
    ]),
    # ── 第9题：源答案编号标记残留
    (f"{B}/汇智/题-HZ-03-06-工业上制备氢气的一种方法是于.md", [
        ("mark", "2' 也可以用勒夏特列原理解释.", "（亦可由勒夏特列原理解释。）"),
    ]),
]

os.makedirs(BAK, exist_ok=True)
tf = th = 0
unmatched = []
for rel, rules in FIX:
    fp = os.path.join(R, rel)
    if not os.path.isfile(fp):
        print("  [MISS 文件]", rel); continue
    raw = io.open(fp, encoding="utf-8-sig", newline="").read()
    new = raw
    hits = []
    for tag, old, tgt in rules:
        n = new.count(old)
        if n == 0:
            unmatched.append((os.path.basename(rel)[:28], tag)); continue
        new = new.replace(old, tgt)
        hits.append((tag, n))
    if new == raw:
        print("  [无改动]", os.path.basename(rel)[:46]); continue
    tf += 1; th += sum(n for _, n in hits)
    print("  %-48s %s" % (os.path.basename(rel)[:46], " ".join("%s×%d" % (t, n) for t, n in hits)))
    if DRY:
        continue
    bp = os.path.join(BAK, os.path.basename(rel))
    if not os.path.isfile(bp):
        shutil.copy2(fp, bp)
    io.open(fp, "w", encoding="utf-8", newline="").write(new)

print(NL + "%s：%d 文件 / %d 处" % ("[dry]" if DRY else "[apply]", tf, th))
if unmatched:
    print("⚠ 未命中规则：", unmatched)
