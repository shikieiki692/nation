# -*- coding: utf-8 -*-
"""生成卷 XVI 的 volpost --patch 配置（源卡级精确替换）。"""
import json
import io

R = r"C:\Obsidion\妙妙屋"

def rd(p):
    return io.open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")

cfg = {}

# 1) HYS-15-04：4.2.2 答案图残片 → 完整框图（源答案 PDF p7 重裁 d30ac8db）；Mo2ttz 错形
cfg["04-题库/2026机构初赛模拟题/化英社/题-HYS-15-04-近年来随着金属有机框架MOF.md"] = [
    ["images/b43c0e9450387458eb66067c3f82803dc59005a6c39c7f26a9e8e2ffbe99dbae.jpg",
     "images/d30ac8db123e48dbb01b550e33aece2016e273b429f8fc776937840925f157ae.jpg"],
    ["$Mo_{2}ttz$", "$Me_{2}ttz$"],
]

# 2) CM-12-05：题面补图 2；删答案区尾部他题残留（保留校勘注）
t = rd(r"04-题库/2026机构初赛模拟题/chemy/题-CM-12-05-DNA碱基之间的特异性配对即.md")
i = t.find("在乙腈")
assert i > 0
k = t.find("## 知识点映射")
seg = t[i:k]
cut_end = seg.find("> ⛔ 校勘")
assert cut_end > 0
resid = seg[:cut_end]          # 「在乙腈…cd30baca.jpg)\n\n」
assert "0262b706" in resid and "cd30baca" in resid and "PdCl_{2}" in resid
cfg["04-题库/2026机构初赛模拟题/chemy/题-CM-12-05-DNA碱基之间的特异性配对即.md"] = [
    ["图 2 DXL-4 二聚体基序",
     "![](images/ff0f77a73636e174d037b4cb8ea6a320550c4ee2aabf41f8a60053b041b107f7.jpg)\n图 2 DXL-4 二聚体基序"],
    [resid, ""],
]

# 3) HZ-01-06：6-1-2 碎片答案 → 源 PDF p18 完整句
cfg["04-题库/2026机构初赛模拟题/汇智/题-HZ-01-06-CuI由于具有灵活多变的配位.md"] = [
    ["$$\n\\mathrm{NaHSO} _ {3}\n$$\n\n$$\n(\\mathrm{CN}) _ {2}\n$$",
     "更温和的反应条件和 $\\mathrm{NaHSO_{3}}$ 的溶液避免了 $(\\mathrm{CN})_{2}$ 的释放（2 分）"],
]

# 4) GChO-82-04：4-2-1 的答案标签被源卷错印为 4-1-2（C19H40 行唯一）
cfg["04-题库/2026机构初赛模拟题/质心GChO/题-GChO-82-04-正烷烃是目前人们研究最为深入.md"] = [
    ["**4-1-2(2分)** $C_{19}H_{40}$  2分", "**4-2-1(2分)** $C_{19}H_{40}$  2分"],
]

# 5) XeC-40-06：答案「線」→「縓」（与题面颜色表 605 nm 一致，源 PDF p10 已核）
cfg["04-题库/2026机构初赛模拟题/XeChem/题-XeC-40-06-量子点是一种半导体纳米晶粒径.md"] = [
    ["故颜色为線（或答介于線和鞅之间也可）", "故颜色为縓（或答介于縓和鞅之间也可）"],
]

# 6) QBY-16-05：5-5-1 补 σc 数值行（源答案 PDF p12 印「√3 倍」「σc ≈ 1.76」，卡漏抄）
cfg["04-题库/2026机构初赛模拟题/清北营/题-QBY-16-05-液体中的起泡现象广泛存在于多.md"] = [
    ["$$\n\\sqrt {3}\n$$",
     "$$\n\\sqrt {3}\n$$\n\n临界半径为饱和二氧化碳溶液中气泡半径的 $\\sqrt{3}$ 倍；"
     "代入 $P_{l}=1\\ \\mathrm{atm}$、$\\alpha=72\\ \\mathrm{mN/m}$、$r_{0}=0.284\\ \\mathrm{\\mu m}$ "
     "得 $\\sigma_{c}\\approx 1.76$。"],
]

out = r".workbuddy/tmp/opt_pipe/xvi_patch.json"
io.open(out, "w", encoding="utf-8").write(json.dumps(cfg, ensure_ascii=False, indent=1))
print("written", out, "cards:", len(cfg),
      "rules:", sum(len(v) for v in cfg.values()))
