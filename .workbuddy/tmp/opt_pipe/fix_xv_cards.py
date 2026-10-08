# -*- coding: utf-8 -*-
"""fix_xv_cards.py —— 卷 XV 源卡修复（回源核对后）。

修复项（每处改前做唯一性断言 + 备份）：
  1. HYS-20-04  删手写批注乱码行 `$K_{2}NiFb$`；参考答案补 4-2/4-3-1/4-4/4-7 缺答
  2. YS-02-04   删「答案区回显题面」段；修 OCR（Eu2LiC3H / Å / N_A / g·cm⁻³ / Eu³⁺ / 4-4 标签）
  3. CM-13-05   题面补「5-2 计算 RbCrF3 的键长 m、s。」；删游离 `$$RbCrF3$$`
  4. YS-03-03   补 3-2-2 答案「…AcBCbABaC…」；删串入他题乱码行
  5. HZ-01-04   参考答案补 4-1-1 缺答「三方晶系，R心六方点阵」
用法: python -X utf8 fix_xv_cards.py [--apply]
"""
import os
import re
import shutil
import sys

Q = r"04-题库/2026机构初赛模拟题"
APPLY = "--apply" in sys.argv

edits = []   # (path, old, new, tag)


def E(path, old, new, tag):
    edits.append((path, old, new, tag))


# ── 1. HYS-20-04 ────────────────────────────────────────────────────────────
P = f"{Q}/化英社/题-HYS-20-04-ABCDE是五种元素组成相同.md"
E(P, "\n$K_{2}NiFb$\n", "\n", "HYS-20-04 删批注乱码行")
E(P,
  "(1 分, 紫色大球为 K, 灰色中球为 Ni, 蓝灰色小球为 F)\n(共 2 分)",
  "**4-2** $\\mathrm{C}$ 的化学式为 $\\mathrm{KNiF_3}$（1 分）；晶胞示意图见题面（1 分，紫色大球为 K，灰色中球为 Ni，蓝灰色小球为 F）。（共 2 分）\n\n"
  "**4-3-1** 立方晶系（1 分），面心立方点阵（1 分），结构基元 $\\mathrm{K_2NiF_6}$（1 分）。（共 3 分）\n\n"
  "**4-3-2** $a=b=c=\\sqrt{2}\\,d_1(\\mathrm{Ni-Ni})=8.003\\ \\text{Å}$（1 分）；$\\rho=\\dfrac{ZM}{N_{\\mathrm A}V}=3.251\\ \\mathrm{g\\,cm^{-3}}$（2 分）。（共 3 分）\n\n"
  "**4-4** K 原子有 2 种不同配位数（1 分）；配位数较小的 K 原子坐标为 $(0,0,0.5)$、$(0.5,0.5,0)$、$(0.5,0,0.5)$、$(0.5,0.5,0.5)$（2 分，全对才得分）。（共 3 分）",
  "HYS-20-04 补 4-2/4-3-1 缺答")
E(P,
  "写出 $\\mathsf{F}$ 的化学式, 并画出 $\\mathsf{F}$ 的晶胞示意图, 要求晶胞顶点为钾原子。\n\n(2 分, 紫色大球为 K, 紫色中球为 I, 灰色中球为 Ni, 红色小球为 O) (共 4 分)",
  "**4-7** $\\mathrm{F}$ 的化学式为 $\\mathrm{KNiIO_4}$（2 分）；晶胞示意图 2 分（紫色大球为 K，紫色中球为 I，灰色中球为 Ni，红色小球为 O）。（共 4 分）",
  "HYS-20-04 补 4-7 缺答")

# ── 2. YS-02-04 ─────────────────────────────────────────────────────────────
P = f"{Q}/一式/题-YS-02-04-碳化物因碳的电负性适中而表现.md"
E(P, "$Li_{2}LiC_{3}H$", "$Eu_{2}LiC_{3}H$", "YS-02-04 化学式 Eu2LiC3H")
E(P, "4.1 已知 $M_{1}$ 中 Li-H 距离", "4-4 已知 $M_{1}$ 中 Li-H 距离", "YS-02-04 标签 4-4")
E(P, "a = \\sqrt {2} d _ {3} = 7.1049 \\mathrm{人(2分)}",
  "a = \\sqrt{2}\\,d_3 = 7.1049\\ \\text{Å}（2 分）", "YS-02-04 a 值 Å")
E(P, "c = 2 d _ {1} = 3.9336 \\mathrm{A(2分)}",
  "c = 2d_1 = 3.9336\\ \\text{Å}（2 分）", "YS-02-04 c 值 Å")
E(P, "N _ {\\Lambda}", "N _ {\\mathrm A}", "YS-02-04 N_A")
E(P, "= 5.819 (\\mathrm{g/cm} ^ {- 1})", "= 5.819\\ \\mathrm{g\\,cm^{-3}}", "YS-02-04 密度单位")
E(P, "不易氧化为 $Eu^{3-}$", "不易氧化为 $Eu^{3+}$", "YS-02-04 Eu 价态符号")

# ── 3. CM-13-05 ─────────────────────────────────────────────────────────────
P = f"{Q}/chemy/题-CM-13-05-人们研究了一系列化学式为其中.md"
E(P,
  "5-1 分别写出 $\\mathrm{KCrF}_{3}$ 和 $\\mathrm{RbCrF}_{3}$ 的点阵、晶系类型。\n\n$$\n\\mathrm{RbCrF} _ {3}\n$$\n\n5-3 在",
  "5-1 分别写出 $\\mathrm{KCrF}_{3}$ 和 $\\mathrm{RbCrF}_{3}$ 的点阵、晶系类型。\n\n5-2 计算 $\\mathrm{RbCrF_3}$ 的键长 $m$、$s$。\n\n5-3 在",
  "CM-13-05 题面补 5-2 题干")

# ── 4. YS-03-03 ─────────────────────────────────────────────────────────────
P = f"{Q}/一式/题-YS-03-03-主族元素E的氧化物与碱金属M.md"
E(P,
  "3-2-2 用 ABC 代表 M 与 X 形成的层、用 abc 代表 E 填入的层，书写晶体的堆积-填隙式：\n\n3-2-3 选出下列说法中正确的:",
  "3-2-2 用 ABC 代表 M 与 X 形成的层、用 abc 代表 E 填入的层，书写晶体的堆积-填隙式：\n\n3-2-2（本小问共 2 分）$\\cdots\\mathrm{AcBCbABaC}\\cdots$（2 分）\n\n3-2-3 选出下列说法中正确的:",
  "YS-03-03 补 3-2-2 答案")
E(P,
  "乙二胺相比肼多出两个亚甲基单位可能改变蒽环的堆积方式,也因此蒽环和RhB环两个发色团之间无法共轭,使得开环型体不稳定。\n\n",
  "",
  "YS-03-03 删串入乱码行")

# ── 5. HZ-01-04 ─────────────────────────────────────────────────────────────
P = f"{Q}/汇智/题-HZ-01-04-刚玉corundum即是一种.md"
E(P,
  "4-1-1 请写出刚玉所属的晶系和点阵形式。\n\n4-1-2 用 A、B、C...代表 O²-层",
  "4-1-1 请写出刚玉所属的晶系和点阵形式。\n\n三方晶系（1 分），R 心六方点阵（1 分）。\n\n4-1-2 用 A、B、C...代表 O²-层",
  "HZ-01-04 补 4-1-1 缺答")

# ── 执行 ────────────────────────────────────────────────────────────────────
cache = {}


def load(p):
    if p not in cache:
        cache[p] = open(p, encoding="utf-8-sig").read()
    return cache[p]


ok = True
for path, old, new, tag in edits:
    t = load(path)
    n = t.count(old)
    if n != 1:
        print("!! [%s] 命中 %d 次（应为 1）" % (tag, n))
        ok = False
        continue
    if old == new:
        print("!! [%s] old==new" % tag)
        ok = False
        continue
    cache[path] = t.replace(old, new, 1)
    print(" OK [%s]" % tag)

# ★ 追加：YS-02-04 删「答案区回显题面」段（源《一式02答案》把整段题面复述进答案区）
_p = f"{Q}/一式/题-YS-02-04-碳化物因碳的电负性适中而表现.md"
_t = load(_p)
_t2, cnt = re.subn(r"(## 参考答案\n\n)碳化物因碳的电负性适中.*?并判断 Eu 的价态。\n",
                   r"\1", _t, count=1, flags=re.S)
if cnt != 1:
    print("!! [YS-02-04 删回显段] 命中 %d" % cnt)
    ok = False
else:
    cache[_p] = _t2
    print(" OK [YS-02-04 删回显段]")

if not ok:
    print("** 有未命中项，未写盘")
    sys.exit(1)

if not APPLY:
    print("(dry) %d 处待改；--apply 写盘" % len(edits))
    sys.exit(0)

for path, txt in cache.items():
    bak = path + ".bak-xv"
    shutil.copy2(path, bak)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print("  写盘 %s  (备份 %s)" % (path, os.path.basename(bak)))
print("done: %d 文件" % len(cache))
