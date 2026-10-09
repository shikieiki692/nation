# -*- coding: utf-8 -*-
"""r9：两卷源卡 OCR 化学式/评分标记规范化（每处唯一命中断言 + 备份）。"""
import os, shutil, datetime

Q = "04-题库/2026机构初赛模拟题"
BAK = ".workbuddy/tmp/opt_pipe/card_bak_r9"
os.makedirs(BAK, exist_ok=True)

EDITS = [
    # ── HZ-07-04（卷 XV 第1题）答案区：Au 混价化学式（源 p14 核：Cs2[Au^I Cl2][Au^III Cl4]）
    (f"{Q}/汇智/题-HZ-07-04-41著名的钙钛矿型晶体想必大.md",
     "Cs2[Au1Cl2][AuIIICl4]（2 分）",
     r"$\mathrm{Cs}_{2}[\mathrm{Au}^{\mathrm{I}}\mathrm{Cl}_{2}][\mathrm{Au}^{\mathrm{III}}\mathrm{Cl}_{4}]$（2 分）",
     "HZ-07-04 Au 混价化学式"),

    # ── HZ-08-05（卷 XIV 第4题）答案区：BC2 / BC4
    (f"{Q}/汇智/题-HZ-08-05-以下是某四方晶体沿a轴和c轴.md",
     "**5-3-1** （2 分）BC2（2 分）写 BC4也得分",
     r"**5-3-1** （2 分）$\mathrm{BC}_{2}$（2 分）写 $\mathrm{BC}_{4}$ 也得分",
     "HZ-08-05 BC2/BC4"),

    # ── GChO-80-04（卷 XV 第3题）答案表：评分标记 + 化学式
    (f"{Q}/质心GChO/题-GChO-80-04-41二维材料呈现出丰富的晶体.md",
     "<td>面心立方/cF 1分</td><td>4-3-2（2 分）</td><td>(c)萤石 2分</td>",
     "<td>面心立方/cF（1 分）</td><td>4-3-2（2 分）</td><td>(c) 萤石（2 分）</td>",
     "GChO-80-04 表内评分标记 a"),
    (f"{Q}/质心GChO/题-GChO-80-04-41二维材料呈现出丰富的晶体.md",
     'Cu对应F-, Al对应Ca2+ 2分',
     "Cu 对应 F⁻，Al 对应 Ca²⁺（2 分）",
     "GChO-80-04 Cu/Al 对应式"),
    (f"{Q}/质心GChO/题-GChO-80-04-41二维材料呈现出丰富的晶体.md",
     "Abc&#x27;ABca&#x27;BCab&#x27;CA3分,严格注意顺序和大小写",
     "Abc'ABca'BCab'CA（3 分），严格注意顺序和大小写",
     "GChO-80-04 Abc 序列 + 评分标记"),

    # ── CM-13-05（卷 XV 第2题）：纯文本化学式 → 数学式
    (f"{Q}/chemy/题-CM-13-05-人们研究了一系列化学式为其中.md",
     "KCrF3:体心四方点阵（1 分）,四方晶系（1 分）RbCrF3:简单四方点阵（1 分）,四方晶系（1 分）",
     r"$\mathrm{KCrF}_{3}$：体心四方点阵（1 分），四方晶系（1 分）；$\mathrm{RbCrF}_{3}$：简单四方点阵（1 分），四方晶系（1 分）",
     "CM-13-05 5-1 答案化学式"),
    (f"{Q}/chemy/题-CM-13-05-人们研究了一系列化学式为其中.md",
     "5-2 计算RbCrF3的键长m、s。",
     r"5-2 计算 $\mathrm{RbCrF}_{3}$ 的键长 m、s。",
     "CM-13-05 5-2"),
    (f"{Q}/chemy/题-CM-13-05-人们研究了一系列化学式为其中.md",
     "5-3 在RbCrF3的晶体结构中",
     r"5-3 在 $\mathrm{RbCrF}_{3}$ 的晶体结构中",
     "CM-13-05 5-3"),
    (f"{Q}/chemy/题-CM-13-05-人们研究了一系列化学式为其中.md",
     "5-5 虽然NaCrF3也是钙钛矿结构",
     r"5-5 虽然 $\mathrm{NaCrF}_{3}$ 也是钙钛矿结构",
     "CM-13-05 5-5 化学式"),
    (f"{Q}/chemy/题-CM-13-05-人们研究了一系列化学式为其中.md",
     "对于钙钛矿ABX3,Goldschmidt",
     r"对于钙钛矿 $\mathrm{ABX}_{3}$，Goldschmidt",
     "CM-13-05 ABX3"),

    # ── HYS-01-02（卷 XIV 第5题）题面 2-2-1：下标（源 p2 逐字核）
    (f"{Q}/化英社/题-HYS-01-02-研究钙钛矿衍生结构时常用Ra.md",
     "堆积层为[MO3]时，全c层中的[O6]八面体和全h层中的[Oa]八面体分别以何种方式连接",
     "堆积层为[MO₃]时，全c层中的[O₆]八面体和全h层中的[O₆]八面体分别以何种方式连接",
     "HYS-01-02 2-2-1 下标"),
]

apply_ = "--apply" in os.sys.argv
cache, ok = {}, True
for path, old, new, tag in EDITS:
    t = open(path, encoding="utf-8-sig").read()
    n = t.count(old)
    if n != 1:
        print("!! [%s] 命中 %d 次（应为 1）" % (tag, n))
        ok = False
        continue
    if old == new:
        print("!! [%s] old==new" % tag)
        ok = False
        continue
    print("OK [%s]" % tag)
    cache[path] = cache.get(path, t).replace(old, new, 1)

if not ok:
    print("存在失败项，未写盘")
    os.sys.exit(1)

if apply_:
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    for path, body in cache.items():
        if not os.path.exists(os.path.join(BAK, os.path.basename(path) + ".bak-" + stamp)):
            shutil.copy2(path, os.path.join(BAK, os.path.basename(path) + ".bak-" + stamp))
        open(path, "w", encoding="utf-8", newline="\n").write(body)
    print("已写盘 %d 个文件" % len(cache))
else:
    print("(dry) 待写盘 %d 个文件" % len(cache))
