# -*- coding: utf-8 -*-
"""批60 P2 修复：14 题补 exam_stage、3 题答案扩充、题-1066 分裂记号合并"""
import io, os

BASE = r"C:\Obsidion\妙妙屋\04-题库\教材习题\高中化学竞赛教程第二分册"

# 1) 补 exam_stage（14 个实战题文件）
stage_files = [
    "题-1055-二分册-L12实1-1211灭火剂命名.md",
    "题-1056-二分册-L12实2-溴乙烷除乙醇杂质.md",
    "题-1057-二分册-L12实3-二溴环己烯系统命名.md",
    "题-1058-二分册-L12实4-钠法合成环丙烷.md",
    "题-1059-二分册-L12实5-Mr84双烃AB结构推断.md",
    "题-1060-二分册-L12实6-单一氢C6H12推断与双烯转化.md",
    "题-1061-二分册-L12实7-溴代甲基环己烷制6羰基庚酸.md",
    "题-1062-二分册-L12实8-E式烯烃转Z式多步合成.md",
    "题-1063-二分册-L12实9-AG转化链五结构推导.md",
    "题-1064-二分册-L12实10-锂亚铜偶联填框.md",
    "题-1065-二分册-L12实11-八溴醚三问.md",
    "题-1067-二分册-L12实13-C7H8芳烃转化链.md",
    "题-1068-二分册-L12实14-C8H10卤代转换关系图.md",
    "题-1069-二分册-L12实15-氯甲烷制备与氧化验证实验.md",
]
for fn in stage_files:
    p = os.path.join(BASE, fn)
    t = io.open(p, encoding="utf-8", newline="").read()
    assert "exam_stage" not in t, fn
    anchor = "teaching_level: 竞赛"
    assert t.count(anchor) == 1, fn
    t = t.replace(anchor, anchor + "\nexam_stage: 初赛")
    io.open(p, "w", encoding="utf-8", newline="").write(t)
print("exam_stage 14 ok")

# 2) 答案扩充（3 个选择题）
ans_fix = {
    "题-1055-二分册-L12实1-1211灭火剂命名.md": (
        "**B**\n\n",
        "**B**（B 项 CF₂Br₂ 按 C、F、Cl、Br 顺序应为 1202 而非 122；A 项 CF₃Br＝1301、C 项 C₂F₄Cl₂＝242、D 项 C₂ClBr₂ 顺序计数均不合命名原则中 B 的「122」写法，B 不正确）\n\n",
    ),
    "题-1056-二分册-L12实2-溴乙烷除乙醇杂质.md": (
        "**D**\n\n",
        "**D**（乙醇与水互溶，溴乙烷不溶于水且密度大于水，加水振荡静置分层后分液即可除去乙醇；A/B 会引入新杂质或损耗主产物，C 与大量溴乙烷无作用且钠 primarily 与微量水反应危险）\n\n",
    ),
    "题-1058-二分册-L12实4-钠法合成环丙烷.md": (
        "**C**\n\n",
        "**C**（仿题给 Wurtz 型反应，1,3-二溴丙烷 CH₂BrCH₂CH₂Br 与 2Na 发生分子内偶联成环得环丙烷＋2NaBr；其余选项碳链/溴位不匹配）\n\n",
    ),
}
for fn, (old, new) in ans_fix.items():
    p = os.path.join(BASE, fn)
    t = io.open(p, encoding="utf-8", newline="").read()
    assert t.count(old) == 1, (fn, t.count(old))
    t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
print("answer expand 3 ok")

# 3) 题-1066 分裂记号合并
p = os.path.join(BASE, "题-1066-二分册-L12实12-三甲苯与氟乙烷中间体正离子.md")
t = io.open(p, encoding="utf-8", newline="").read()
old = "A. $^{*}$ CH≡CH"
assert t.count(old) == 1, t.count(old)
t = t.replace(old, "A. $^{*}\\mathrm{CH{\\equiv}CH}$")
io.open(p, "w", encoding="utf-8", newline="").write(t)
print("xref 1066 ok")
