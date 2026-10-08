# -*- coding: utf-8 -*-
"""fix_xiv_cards2.py —— 卷 XIV 源卡「回源修复」（仅据原 PDF）。

用法: python -X utf8 fix_xiv_cards2.py [--apply]
mode: one=唯一命中 / all=全替换(≥1) / nth2=命中恰 2 处、改第 2 处
"""
import datetime
import os
import shutil
import sys

Q = os.path.join(r"C:\Obsidion\妙妙屋", "04-题库", "2026机构初赛模拟题")
EDITS = []


def E(rel, desc, pairs):
    EDITS.append((os.path.join(Q, rel), desc, pairs))


# 第1题 CM-01-05：1-1-2 题干补全（定义式＋晶胞参数＋坐标表＋提示），从答案区移回题面
E("chemy/题-CM-01-05-很多具有钙钛矿结构的化合物是.md",
  "第1题: 1-1-2 题干补全 + 答案区去重", [
    ("R", "one",
     "\n其中 $\\beta$ 为八面体中处于相对位置的 X-B-X 键角。对于理想情况下的八面体其 "
     "$\\sigma_{2}^{2}=0$ 。 $\\mathrm{BaTiO}_{3}$ 晶体属四方晶系, 其晶胞参数 "
     "$a=b=400.0\\ \\mathrm{pm}$ , $c=401.7\\ \\mathrm{pm}$ , 晶胞中部分原子坐标如下表所示。"
     "计算 $\\mathrm{CaTiO}_{3}$ 和 $\\mathrm{BaTiO}_{3}$ 的 $\\sigma_{2}^{2}$ 参数。\n\n"
     "<table><tr><td>原子种类</td><td>x</td><td>y</td><td>z</td></tr><tr><td>Ba</td><td>0</td>"
     "<td>0</td><td>0</td></tr><tr><td>Ti</td><td>0.500</td><td>0.500</td><td>0.482</td></tr>"
     "<tr><td>O</td><td>0.500</td><td>0.500</td><td>0.016</td></tr><tr><td>O</td><td>0.500</td>"
     "<td>0</td><td>0.515</td></tr></table>\n\n提示：晶胞图中给出的原子并不都在晶胞内。\n", ""),
    ("R", "one",
     "5-1-2 钙钛矿型晶体中八面体的畸变参数可用 $\\sigma_{2}^{2}$ 描述, 其定义式为\n",
     "5-1-2 钙钛矿型晶体中八面体的畸变参数可用 $\\sigma_{2}^{2}$ 描述, 其定义式为 "
     "$\\sigma_{2}^{2} = \\frac{1}{2}\\sum_{i=1}^{3}(\\beta_{i}-180^{\\circ})^{2}$ 。"
     "其中 $\\beta$ 为八面体中处于相对位置的 X-B-X 键角。对于理想情况下的八面体其 "
     "$\\sigma_{2}^{2}=0$ 。 $\\mathrm{BaTiO}_{3}$ 晶体属四方晶系, 其晶胞参数 "
     "$a=b=400.0\\ \\mathrm{pm}$ , $c=401.7\\ \\mathrm{pm}$ , 晶胞中部分原子坐标如下表所示。"
     "计算 $\\mathrm{CaTiO}_{3}$ 和 $\\mathrm{BaTiO}_{3}$ 的 $\\sigma_{2}^{2}$ 参数。\n\n"
     "<table><tr><td>原子种类</td><td>x</td><td>y</td><td>z</td></tr><tr><td>Ba</td><td>0</td>"
     "<td>0</td><td>0</td></tr><tr><td>Ti</td><td>0.500</td><td>0.500</td><td>0.482</td></tr>"
     "<tr><td>O</td><td>0.500</td><td>0.500</td><td>0.016</td></tr><tr><td>O</td><td>0.500</td>"
     "<td>0</td><td>0.515</td></tr></table>\n\n提示：晶胞图中给出的原子并不都在晶胞内。\n"),
  ])

# 第2题 CM-125-06：补 6-2 / 6-3-1 / 6-3-2 答案（原答案合集 p197）
E("chemy/题-CM-125-06-下图为理想钙钛矿的立体结构图.md",
  "第2题: 补 6-2/6-3-1/6-3-2 答案", [
    ("R", "one",
     "6-1 $Ln_{2}CuO_{4}$ $Ln_{2}CuO_{4}$ $Ln_{2}CuO_{4}$ （每个 0.5 分）\n",
     "6-1 $Ln_{2}CuO_{4}$ $Ln_{2}CuO_{4}$ $Ln_{2}CuO_{4}$ （每个 0.5 分）\n\n"
     "6-2 Cu：四方锥配位（1 分）；Ln：四棱柱（1.5 分）与单加帽四方反棱柱（1 分）；"
     "后者答四方锥得 0.5 分。\n\n"
     "6-3-1 $N_{n}MO_{2+n}$（1 分）\n\n"
     "6-3-2 $a=\\sqrt{2}d$（1 分）；一个钙钛矿层的高度为 $\\sqrt{2}d$；"
     "$n$ 个连续岩盐层的高度为 $(n-1)d$（1 分）；若 $n$ 为奇数，晶体为体心点阵，"
     "$c=2\\sqrt{2}d+2(n-1)d$（1 分）；若 $n$ 为正偶数，晶体为简单点阵，"
     "$c=\\sqrt{2}d+(n-1)d$（1 分）。\n"),
  ])

# 第3题 CM-150-06：Å 同形字修复 + 两处残留碎片删除
E("chemy/题-CM-150-06-在不同的温度和压力下锗酸钡具.md",
  "第3题: Å 修复 + 删残留碎片", [
    ("R", "all", "\\mathrm{mathring A}", "\\text{Å}"),
    ("R", "one", "4 指出[GeO6]八面体的连接方式。6-3\n", ""),
    ("R", "one", "绕该轴旋转60°，然后平移6c，晶体结\n\n", ""),
  ])

# 第5题 HYS-01-02：补 2-2-3-1/2/3 答案 + 密度式乱码修复
E("化英社/题-HYS-01-02-研究钙钛矿衍生结构时常用Ra.md",
  "第5题: 补 2-2-3 答案 + 密度式修复", [
    ("R", "one",
     "2-2-3 晶体B在Jagodzinski 符号规则下可以记作ccc'cchhh排列，其中c'层代表发生了氧空位缺陷变为[BaO2]层， "
     "同时Ο 原子在层内的位置发生变化使得单层仍保留六方对称性。\n",
     "2-2-3 晶体B在Jagodzinski 符号规则下可以记作ccc'cchhh排列，其中c'层代表发生了氧空位缺陷变为[BaO2]层， "
     "同时Ο 原子在层内的位置发生变化使得单层仍保留六方对称性。\n\n"
     "2-2-3-1 16H（2 分）\n\n"
     "2-2-3-2 $\\mathrm{Ba_{8}Ca_{2}Mn_{6}O_{23}}$（2 分）\n\n"
     "2-2-3-3 +4 价的 Mn：ch 层间和 hh 层间，八面体空隙；+5 价的 Mn：c'c 层间和 cc 层间"
     "（仅答其中一种亦可），四面体空隙（共 6 分；价态各 1 分，将 +4、+5 换成 +3、+7 亦可；"
     "层间和空隙各 1 分）\n"),
    ("R", "one",
     "八面体边长d=√2d(m-o) = 2.874Å（1 分）晶胞参数a=2d=5.747Å （1 分）\n",
     "八面体边长 $d=\\sqrt{2}d_{\\mathrm{M-O}}=2.874$ Å（1 分）晶胞参数 $a=2d=5.747$ Å（1 分）\n"),
    ("R", "one",
     "\\6层间距h= \\d=2.346A,a 故晶胞参数c=12h= 28.16Å（1 分）对于一层cchh， 填入了一层Ca，一层Mn， "
     "两层 0.5Mn+0.5Mo故A化学式为 CaMoMn2Ba4O12 （2 分），Z=3Z· M(A)PA = ac·sin120°.NA = 6.106 g/cm³ "
     "（2 分）（共 7 分）\n",
     "层间距 $h=\\frac{\\sqrt{6}}{3}d=2.346$ Å，故晶胞参数 $c=12h=28.16$ Å（1 分）。对于一层 cchh，"
     "填入了一层 Ca、一层 Mn、两层 0.5Mn+0.5Mo，故 A 化学式为 $\\mathrm{CaMoMn_{2}Ba_{4}O_{12}}$（2 分），"
     "$Z=3$，$\\rho_{A}=\\frac{ZM(A)}{a^{2}c\\sin120^{\\circ}N_{\\mathrm{A}}}=6.106\\ \\mathrm{g/cm^{3}}$"
     "（2 分）（共 7 分）\n"),
  ])

# 第7题 QBY-08-06：7-2-4 密度式分数压平修复
E("清北营/题-QBY-08-06-611堆积层永远是晶体结构问.md",
  "第7题: 7-2-4 密度式修复", [
    ("R", "one",
     "**6-2-4** 1.假设同层Ge-Tb距离为2.81Å,竖直方向Ge-Tb距离为2.98Å,计算得晶胞参数a=b=√3×2.81=4.867Å,"
     "c=2.98×2+2.55=8.51Åρ=ZM/NAabc=158.9+54.94×6+72.61×66.022×1023×4.867×4.867×8.51×10-24×sin120°"
     "=8.79g/cm3不符合条件2.假设同层Ge-Tb距离为2.98Å,竖直方向Ge-Tb距离为2.81Å,计算得晶胞参数a=b=√3×2.98"
     "=5.16Å,c=2.81×2+2.55=8.17Åρ=ZM/NAabc=158.9+54.94×6+72.61×66.022×1023×5.16×5.16×8.17×10-24×sin120°"
     "=8.15g/cm3...1分综上所述,真实密度为8.15g/cm3无过程不得分,必须分别讨论,允许一定误差",
     "**6-2-4** 1. 假设同层 Ge-Tb 距离为 2.81 Å，竖直方向 Ge-Tb 距离为 2.98 Å，计算得晶胞参数 "
     "$a=b=\\sqrt{3}\\times2.81=4.867$ Å，$c=2.98\\times2+2.55=8.51$ Å，"
     "$\\rho=\\frac{ZM}{N_{\\mathrm{A}}abc}=\\frac{158.9+54.94\\times6+72.61\\times6}"
     "{6.022\\times10^{23}\\times4.867\\times4.867\\times8.51\\times10^{-24}\\times\\sin120^{\\circ}}"
     "=8.79\\ \\mathrm{g/cm^{3}}$，不符合条件。2. 假设同层 Ge-Tb 距离为 2.98 Å，竖直方向 Ge-Tb 距离为 "
     "2.81 Å，计算得晶胞参数 $a=b=\\sqrt{3}\\times2.98=5.16$ Å，$c=2.81\\times2+2.55=8.17$ Å，"
     "$\\rho=\\frac{ZM}{N_{\\mathrm{A}}abc}=\\frac{158.9+54.94\\times6+72.61\\times6}"
     "{6.022\\times10^{23}\\times5.16\\times5.16\\times8.17\\times10^{-24}\\times\\sin120^{\\circ}}"
     "=8.15\\ \\mathrm{g/cm^{3}}$……（1 分）综上所述，真实密度为 8.15 g/cm³。无过程不得分，"
     "必须分别讨论，允许一定误差"),
  ])

# 第8题 HZ-11-05：OCR 同形字修复 + 补 5-2-3 答案
E("汇智/题-HZ-11-05-在晶体结构的研究中将晶胞拆分.md",
  "第8题: OCR 修复 + 补 5-2-3 答案", [
    ("R", "one", "结构基元: $Co_{4}AsI_{2}$ （1 分）", "结构基元: $\\mathrm{Co_{4}As_{12}}$（1 分）"),
    ("R", "one", "设立方体的棱长为  $a_{1}$ ，小立方体的棱长为  $u_{2}$ ， $u_{1}=u/2$\n",
     "设立方体的棱长为 $a_{1}$ ，小立方体的棱长为 $a_{2}$ ， $a_{2}=a_{1}/2$\n"),
    ("R", "one", "由图可得， $d_{Al-O}=u_{2}$ $u_{2}+3d_{Al-O}=a$ ，解得  $a_{2}=a/4=a_{1}/2$\n",
     "由图可得， $d_{\\mathrm{Al-O}}=a_{2}$ ， $a_{2}+3d_{\\mathrm{Al-O}}=a$ ，解得 $a_{2}=a/4=a_{1}/2$\n"),
    ("R", "one", "p = Z M / (\\nabla \\cdot N _ {A}) = 3.58", "\\rho = Z M / (V \\cdot N_{A}) = 3.58"),
    ("R", "all", "$C_{\\mathrm{J}}$", "$C_{3}$"),
    ("R", "nth2",
     "5-2-3 “CoAs $_{3}$ 的晶体结构由立方 ReO $_{3}$ 结构畸变而来” 可以按如下方式理解：设原晶胞参数为 a，"
     "则当 As-As 键长为 \\_\\_\\_\\_ (用含 a 的表达式表示，下同) 时，该晶胞即与 ReO $_{3}$ 结构完全相同，"
     "此时新晶胞的晶胞参数 a' = \\_\\_\\_\\_。",
     "5-2-3 “CoAs $_{3}$ 的晶体结构由立方 ReO $_{3}$ 结构畸变而来” 可以按如下方式理解：设原晶胞参数为 a，"
     "则当 As-As 键长为 \\_\\_\\_\\_ (用含 a 的表达式表示，下同) 时，该晶胞即与 ReO $_{3}$ 结构完全相同，"
     "此时新晶胞的晶胞参数 a' = \\_\\_\\_\\_。\n\n$a/2$ ； $a/2$（各 1 分）"),
  ])


def main():
    apply = "--apply" in sys.argv
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    ok = True
    for path, desc, pairs in EDITS:
        with open(path, encoding="utf-8-sig") as f:
            txt = f.read().replace("\r\n", "\n")
        orig = txt
        for mode_tag, mode, old, new in pairs:
            n = txt.count(old)
            good = (n == 1) if mode == "one" else (n >= 1 if mode == "all" else (n == 2))
            if not good:
                print(f"❌ [{os.path.basename(path)}] {desc}: mode={mode} 命中 {n} → {old[:42]!r}")
                ok = False
                continue
            if mode == "nth2":
                i = txt.find(old, txt.find(old) + 1)
                txt = txt[:i] + new + txt[i + len(old):]
            elif mode == "all":
                txt = txt.replace(old, new)
            else:
                txt = txt.replace(old, new, 1)
        if txt != orig and apply:
            shutil.copy2(path, path + f".bak-{stamp}")
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(txt)
            print(f"✅ [{os.path.basename(path)}] {desc}  已写  Δ={len(txt)-len(orig):+d}")
        else:
            print(f"·  [{os.path.basename(path)}] {desc}  {'无变化' if apply else '待写'}")
    print("APPLIED" if apply else "DRY-RUN", "OK" if ok else "HAS-ERRORS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
