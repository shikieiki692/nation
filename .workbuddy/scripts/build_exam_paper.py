# -*- coding: utf-8 -*-
"""
题面汇编器：把索引型试卷（题号 wikilink 清单）汇编为自含型试卷 md（仅题面，无答案）。

用法： python build_exam_paper.py            # 汇编 3 卷 → .workbuddy/tmp/exam_build/
     python build_exam_paper.py --check    # 只做残留答案标记扫描

设计：
  - 题面区 = 正文去掉 FM/H1 后、到首个答案边界为止
    答案边界：## 参考答案|答案|题目与答案 / 解： / **答案：** / 解题思路 / 【解析】 / > [!note] 起始的答案块
  - 交错型（小问与答案：内联交错，如 39决理-10）：删除「答案：」起、至下一个标题/数字小问行的块
  - 汇编后全文复扫残留答案标记 → 打标供人工复核（质量优先，不静默吞）
"""
import io
import os
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

VAULT = Path(r"C:\Obsidion\妙妙屋")
QB = VAULT / "04-题库"
OUT = VAULT / ".workbuddy" / "tmp" / "exam_build"

PAPERS = [
    (QB / "结构化学阶段测试卷.md", "结构化学阶段测试卷"),
    (QB / "元素与分析阶段测试卷.md", "元素与分析阶段测试卷"),
    (QB / "综合模拟卷I.md", "综合模拟卷I"),
    (QB / "综合模拟卷II.md", "综合模拟卷II"),
    (QB / "综合模拟卷III.md", "综合模拟卷III"),
    (QB / "综合模拟卷IV.md", "综合模拟卷IV"),
]

LINK = re.compile(r"^#{2,3}\s+\[\[([^\]|]+?)(?:\|[^\]]+)?\]\](.*)$")
SEC = re.compile(r"^##\s+(.+)$")

# 无入卷价值的注记行（直接丢弃）
DROP_LINE = re.compile(r"^\s*>\s*\*\*答案\*\*[:：]?\s*原书未提供解答")

# 逐文件人工精修题面（讲评式交错文件，自动切割不可靠；key=文件 basename）
CURATED_STEMS = {
    "题-39决理-2-Co的配合物": """**第 2 题 Co 的配合物 (27 分)**

Co 配合物因其氧化数、配体和结构的不同而呈现出丰富的磁性和催化特性。

2.1 直线形过渡金属配合物在分子磁体的研究中备受关注, 其能量状态几乎不受 Jahn-Teller 畸变的影响。2018 年, 科学家报道了一例二配位的单分子磁体 Co(II) 配合物 Co(C(SiMe₂ ONaph)₃ )₂ , 其中 HONaph 为 α-萘酚, C-Co-C 位于同一条直线上。理论计算表明, 该配合物中 Co 的 d 轨道裂分为三组能级, 从低到高电子的分布几率为 42.8%、41.2% 和 16.0%。

2.1.1 假定 C-Co-C 键沿 z 轴方向，依据晶体场理论画出 Co 中心价层 d 轨道能级分裂图，标出轨道符号，然后将电子填充在轨道中，用 “|” 和 “|” 和表示电子不同的自旋状态。

2.1.2 解释该配合物金属中心 d 电子采用上述电子排布的原因。

2.2 含有端基或桥联氮配体的金属配合物可用于催化合成氨。2020年和2023年，科学家分别将含卤素配体的Co配合物与 $NaN_{3}$ 在THF中反应，合成了两个N桥联的双核Co配合物A和B，其结构如下图所示。A中Co-N-Co键角为85°；B中Co-N-Co呈直线，胍基配体的两个N和桥联N呈近似的平面三角构型， $N_{3}$ 基团近似与平面垂直。

![[1d3348016738ba08636785c23a18b7eb1aa03483d0344d951e65966736afcc0c.jpg]]

![[c37eeb27cd60c50a9d53767ba76771ad273c5be53af22c67cf2f07cb496d422d.jpg]]

2.2.1 请确定 A 和 B 中 Co 的氧化数。

2.2.2 研究表明 A 可以用于合成氨，A 与氢气等当量反应生成配合物 C。画出 C 的结构式，并标明其中 Co 的氧化数。

2.2.3 C 无法进一步与氢气反应生成 $NH_{3}$ ，但在室温下可与 LutHCl (2,6-二甲基吡啶盐酸盐) 在 THF 溶液中反应生成 $NH_{3}$ 和配合物 D，D 可以与 $NaN_{3}$ 等当量反应重新得到 A。画出 D 的结构式，并标明其中 Co 氧化数。

2.2.4 B 无法直接与 $\\mathrm{H}_{2}$ 反应, 其反应惰性与 $\\mathrm{Co}-\\mathrm{N}-\\mathrm{Co}$ 的成键特性有关, 实验和理论计算表明, $\\mathrm{Co}-\\mathrm{N}-\\mathrm{Co}$ 中同时包含 $\\sigma$ 键和 $\\pi$ 键。若以 $\\mathrm{Co}-\\mathrm{N}-\\mathrm{Co}$ 为 $x$ 轴, $\\mathrm{Co}-\\mathrm{N}_{3}$ 键方向为 $z$ 轴, 写出参与形成 $\\sigma$ 键和 $\\pi$ 键的 $\\mathrm{Co}$ 的 $d$ 轨道和 $\\mathbf{N}$ 的轨道名称。

2.2.5 研究发现溶剂可以激活 B 中桥联 N 的活性，在吡啶存在下 B 可以与氢气等当量反应得到配合物 E，E 中两个 Co 化学环境相同，均为四面体配位，其中只含有两种等价的配位 N 原子。画出 E 的结构式，需标明其中 Co 的价态，并写出该反应中除 E 和溶剂外的其他小分子产物。

2.2.6 在研究溶剂激活桥联 N 的活性时，发现在吡啶存在下 B 还可以与其他氢给体反应。例如，B 与 0.5 当量的 1,4-环己二烯反应，得到配合物 F，其中两个 Co 的配位原子均为 N，分别呈四面体和近似的四方锥配位结构。F 可以在紫外光照下与 $H_{2}$ 反应得到 E，并释放 1 当量的 $N_{2}$ 和 1 当量的吡啶。画出 F 的结构，并写出由 B 转化为 F 的反应中除 F 和溶剂外的其他小分子产物。""",
    "题-39决理-10-卡宾化学": """**第 10 题 卡宾化学 (33 分)**

含氮分子是制药、农用化工及材料行业中最重要的化合物之一。近年来 80% 以上的畅销药物都至少含有一个氮原子。因此，碳氮键的构建是有机合成化学领域的核心研究方向。烯烃是合成含氮化合物的关键前体，这得益于其在石油化工原料和天然存在的萜类化合物中含量丰富，同时也因为烯烃作为合成中间体的应用十分广泛。

10.1 1969 年，P. G. Gassman 等人以烯烃为原料与氮卡宾反应制备了一系列 1-氯吖啶衍生物，并系统研究了这些化合物的水解反应：

$$\\mathrm{R^1N(Cl)N(Cl)R^3 \\xrightarrow{H_2O} R^1C(=O)R^2 + R^3C(=O)R^4 + NH_4Cl}$$

研究发现, 反式-2,3-二甲基吖啶与次氯酸钠反应生成化合物 1; 而顺式-2,3-二甲基吖啶则生成两个混合物 2 和 3; 而且化合物 3 在室温下可以异构化为 2:

![[cf1ebf7944f4d1914a9d710b814990bcceb833e1930d52efc3acbc2c6f8bb85f.jpg]]

10.1.1 为何化合物 3 能在室温下转化为化合物 2?

10.1.2 在无银离子存在下，1-氯吖啶衍生物的水解速率如下：

<table><tr><td>化合物</td><td>溶剂</td><td>水解速率</td></tr><tr><td>1-氯吖啶</td><td> $H_{2}O$ </td><td> $(6.5 \\pm 1.3) \\times 10^{-7}$ </td></tr><tr><td>1</td><td> $H_{2}O$ </td><td> $(9.6 \\pm 0.3) \\times 10^{-4}$ </td></tr><tr><td>1</td><td> $CH_{3}OH$ </td><td> $(1.2 \\pm 0.2) \\times 10^{-5}$ </td></tr><tr><td>2</td><td> $CH_{3}OH$ </td><td> $(1.3 \\pm 0.1) \\times 10^{-3}$ </td></tr></table>

依据以上实验结果，回答以下问题：

10.1.2.1 研究发现化合物 1 和 2 的水解速率均快于 1-氯吖啶，为此给出合理解释。

10.1.2.2 研究发现化合物 1 在甲醇中的水解速率比在水中慢，为此给出合理解释。

10.1.2.3 研究发现化合物 2 在甲醇中的水解速率快于 1，为此给出合理解释。

10.2 2019 年，M. G. Suero 研究了在金属 Rh 催化下的烯烃与金属卡宾反应，形成环丙烷衍生物，接着在亲核基团的作用下，三元环开环转化为产物：

![[70ce8abccef35027bd75ee72672ac874e18a9360d6f1bb9bf9793079ffbd2e44.jpg]]

10.2.1 画出产物 A 的结构式。

结合前面的研究工作，仔细分析此反应，给出最终产物的结构：

10.2.2

![[4c50502907f9467a2cc715c5ac5c6803bddda422515aa66d3964cf4d5108b5c0.jpg]]

10.2.3

![[b59497533068b17585a90645650ba1a885bb049a6eb0f100dd825db33116479d.jpg]]

10.2.4

![[d8fbee1e6e4f9c84d77edc8a13c681413d08472802f150180fe2902b6f8cdded.jpg]]

10.3 2025 年，B. Morandi 以烯烃为原料先原位生成氮原子链接离去基团的吖丙啶衍生物，随后发生开环反应，继而被合适的亲核试剂捕获。例如，在下述反应中，用双-(三氟乙酰氧)碘苯(PIFA)作氧化剂，用氨基甲酸铵 $\\left(\\mathrm{NH}_{2}\\mathrm{COONH}_{4}\\right)$ 作氮源，可以实现低反应活性双键的氧化氨化：

![[3396e2f336dc6ce0ef85093248dbeb48ba76a91c47887fb0081197fb33044087.jpg]]

10.3.1 给出上述反应关键中间体的结构式。

10.3.2 条件筛选实验表明，1-癸烯在甲醇中不反应，在三氟乙醇或六氟异丙醇 (HFIP) 可以得到产物腈。为此给出合理解释。

10.3.3 依据以上信息，画出下列反应中 A、B 和 C 的结构式：

10.3.3.1

![[248789eb5b2c87a868a4cac9371e7e843ee8045da2a652d6343f57f37cb89149.jpg]]

10.3.3.2

![[c3f2725d9932298cb5fc7e2c2c12e23fdf454bcf34838001d204e35cb44079b7.jpg]]

10.3.4 依据以上信息，画出分别用下列烯烃做底物时主要产物的结构式：

<table><tr><td>10.3.4.1</td><td>10.3.4.2</td><td>10.3.4.3</td><td>10.3.4.4</td></tr><tr><td>![[c820b23a6b62bcbf0f2d5a395d843cc78d40135dcd0616f061f76665bd3f469b.jpg]]</td><td>![[6957e854ad7fdb990064b090707091d08a98f90a3e3204748749b7046d63541a.jpg]]</td><td>![[2cc66145ad6aa8319bb5d590e41a02f63545774624a8bc8ba950604ec48d1ba7.jpg]]</td><td>![[14ed87122331103a38ddc097fb8ce812e36e015dc9ac429ad5cc52376c9beade.jpg]]</td></tr></table>""",
}

# 节级答案边界（命中即截断题面区）
ANS_SECTION = re.compile(
    r"^(?:#{2,3}\s*(?:参考答案|题目与答案|答案)\b[^\n]*"
    r"|\*\*答案[:：][^\n]*"
    r"|解题思路\s*$"
    r"|【解析】"
    r"|解[:：]\s*\S"
    r"|\^\s*原文：)",
)
# 交错型答案块起点（行首「答案：」/「答案:」）
ANS_INLINE = re.compile(r"^答案[:：]")
# 交错型答案块的终止：下一个标题或数字小问行
SUBQ = re.compile(r"^(?:#{1,3}\s+|\d+(?:\.\d+)+\s|\(\d+\)|（\d+）)")

# 残留答案标记（汇编后复扫）
RESIDUAL = re.compile(
    r"^(?:#{2,3}\s*(?:参考答案|题目与答案)\b|\*\*答案[:：]|^答案[:：]|解题思路\s*$|【解析】|解[:：]\s*\S)",
    re.M,
)

_fm_cache = {}


def find_file(basename: str):
    for dp, _, ns in os.walk(QB):
        for n in ns:
            if n == basename + ".md":
                return Path(dp) / n
    return None


def strip_fm(text: str):
    if text.startswith("---"):
        lines = text.split("\n")
        if lines[0].strip() == "---":
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    body = "\n".join(lines[i + 1 :])
                    fm_text = "\n".join(lines[: i + 1])
                    if fm_text not in _fm_cache:
                        fm = {}
                        for ln in lines[1:i]:
                            m = re.match(
                                r"^(source|source_subject|exam_stage|fidelity):\s*(.+)$",
                                ln.strip(),
                            )
                            if m:
                                fm[m.group(1)] = m.group(2).strip().strip('"')
                        _fm_cache[fm_text] = fm
                    return body, _fm_cache[fm_text]
    return text, {}


def extract_stem(path: Path):
    """返回 (题面 md, warnings[list])"""
    t = path.read_text(encoding="utf-8", newline="").replace("\r\n", "\n")
    body, fm = strip_fm(t)
    if path.stem in CURATED_STEMS:
        return CURATED_STEMS[path.stem].strip(), fm, ["人工精修题面（CURATED_STEMS）"]
    # <details> 块整体剥离（教师侧答案折叠块）；HTML 校勘注释不入学生卷
    body = re.sub(r"<details>.*?</details>", "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    lines = body.split("\n")
    warns = []
    out = []
    mode = "normal"           # normal | interleaved-skip
    started = False
    for ln in lines:
        if not started:
            if ln.startswith("# "):        # 顶层标题行：转粗体保留信息
                out.append(f"**{ln[2:].strip()}**")
                started = True
                continue
            if not ln.strip():
                continue
            if ln.startswith("> [!info") or ln.startswith("> **来源"):
                started = True
                continue                    # 转录声明/来源块quote不入卷（来源由 FM 汇总）
            started = True
        if mode == "interleaved-skip":
            if not ln.strip() or SUBQ.match(ln):
                mode = "normal"            # 空行或新小问 → 结束跳过
                if not ln.strip():
                    continue
        if DROP_LINE.match(ln):
            continue
        if ANS_SECTION.match(ln.strip()) and ln.strip():
            break                           # 节级边界：截断
        if ANS_INLINE.match(ln.strip()):
            mode = "interleaved-skip"
            warns.append("交错答案块（答案：内联）已按块跳过")
            continue
        out.append(ln)
    stem = "\n".join(out).strip()
    # H1 降级（题面区中间出现的 # 一级标题 → ###）
    stem = re.sub(r"(?m)^# (.+)$", r"### \1", stem)
    # 复扫残留
    res = RESIDUAL.search(stem)
    if res:
        warns.append(f"残留答案标记未清: {stem[max(0,res.start()-10):res.start()+40]!r}")
    return stem, fm, warns


def short_source(fm: dict, base: str) -> str:
    """极简来源标签：真题→'第39届决赛'；教材→'《结构化学基础》习题 5.37'。"""
    src = fm.get("source") or fm.get("source_subject") or ""
    m = re.search(r"第\s*(\d+)\s*届.{0,14}?(决赛|初赛)", src)
    if m:
        return f"第{m.group(1)}届{m.group(2)}"
    bm = re.search(r"《([^》]+?)》", src)
    if bm:
        book = re.sub(r"（第\d+版）", "", bm.group(1))
        nm = re.search(r"(习题|例|T)([0-9]+(?:\.[0-9]+)*)$", base)
        tail = f" {nm.group(1)} {nm.group(2)}" if nm else ""
        return f"《{book}》{tail}"
    seg = re.split(r"[·/|]", src)[0].strip()
    seg = re.sub(r"（(忠实|逐字)转录[^）]*）|（辅导性作业）", "", seg)
    seg = seg.replace("第6版Weller", "Weller ").replace("无机化学 例题与习题", "无机化学例题与习题")
    return seg[:24]


def build(paper_path: Path, title: str):
    t = paper_path.read_text(encoding="utf-8", newline="").replace("\r\n", "\n")
    body, _ = strip_fm(t)
    lines = body.split("\n")
    header, entries, cur_sec = [], [], None
    for ln in lines:
        m = LINK.match(ln.strip())
        if m:
            entries.append((cur_sec or "题目", m.group(1).strip(), m.group(2).strip()))
            continue
        m2 = SEC.match(ln.strip())
        if m2:
            cur_sec = m2.group(1).strip()
            continue
        if not entries:
            header.append(ln)
    header_txt = "\n".join(ln for ln in header if not ln.strip().startswith("> **答案**"))
    header_txt = re.sub(r"<!--.*?-->", "", header_txt, flags=re.S)
    header_txt = re.sub(r"(?m)^#{1,3} .+$", "", header_txt)          # 去掉卷内大标题（重写）
    header_txt = re.sub(r"\n{3,}", "\n\n", header_txt).strip()

    out = [
        "---",
        f'title: "{title}（汇编版）"',
        "type: 试卷",
        f"updated: 2026-09-06",
        f"assembled_from: \"{paper_path.as_posix()}\"",
        "---",
        "",
        f"# {title}",
        "",
        "> 本卷由题库索引卷自动汇编（build_exam_paper.py），题面自含、不含答案；",
        "> 题目内容以 04-题库 源文件为准，来源与分值保持原样。",
        "",
        header_txt,
        "",
    ]
    flags, cur_sec, n = [], None, 0
    for sec, base, trail in entries:
        if sec != cur_sec:
            out += [f"## {sec}", ""]
            cur_sec = sec
        p = find_file(base)
        n += 1
        out += [f"## 第 {n} 题", ""]
        if not p:
            out += [f"> ⚠️ 未找到题文件：{base}", ""]
            flags.append((base, "文件未找到"))
            continue
        stem, fm, warns = extract_stem(p)
        meta = f"> 来源：{short_source(fm, base)}"
        out += [meta, "", stem, ""]
        for w in warns:
            flags.append((base, w))
    out += ["---", "", f"**汇编统计**：共 {n} 题。" +
            (f" 待复核 {len(flags)} 处。" if flags else " 无待复核项。"), ""]
    dst = OUT / f"{title}.md"
    dst.write_text("\n".join(out), encoding="utf-8", newline="")
    print(f"[{title}] {n} 题 → {dst.name}  待复核 {len(flags)}")
    for b, w in flags:
        print(f"   ⚠ {b}: {w}")
    return n, flags


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    total, allflags = 0, []
    for p, title in PAPERS:
        n, flags = build(p, title)
        total += n
        allflags += [(title, b, w) for b, w in flags]
    print("-" * 60)
    print(f"合计 {total} 题；待复核 {len(allflags)} 处")


if __name__ == "__main__":
    main()
