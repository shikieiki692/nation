# -*- coding: utf-8 -*-
"""
初赛模拟卷 · 学生版 → 国初真题版式（打印友好）

产出目录：00-首页/题组Word/初赛模拟卷/真题版式/

口径（依据库内真题原件 04-题库/真题（无答案）/ 第37/38/39 届 PDF 实测标定）：
  · 页面 A4，页边距 上下 2.2cm / 左右 1.9cm（实测真题版心宽 ≈482~493pt）
  · 正文 宋体（中文）/ Times New Roman（西文），五号 10.5pt
  · 行距 多倍 1.3（实测真题行间基线距 ≈16.3~18.7pt）
  · 卷首标题 宋体加粗 16pt 居中（去掉「学生版」后缀，真卷不印版本）
  · 部分标题 宋体加粗 12pt 居中；题号行 宋体加粗 10.5pt 左对齐
  · 题干段首行缩进 2 字符；子问 1-1 / 1-1-1 顶格
  · 表格全框线；图片居中；无任何彩色
  · 页脚居中「第 X 页，共 Y 页」
  · **删除「考试说明」引用块**（用户 2026-09-23 指示）
  · 化学式由斜体改正体（OMML m:sty=p，启发式判定，见 omml_upright）

源 md 一律只读；中间产物落 .workbuddy/tmp/chusai_zhenti/。

用法：
  python build_chusai_zhenti_layout.py            # 全量 9 卷
  python build_chusai_zhenti_layout.py --only I V # 只做指定卷
  python build_chusai_zhenti_layout.py --rebuild-ref
"""
import io
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PY = sys.executable
VAULT = Path(r"C:\Obsidion\妙妙屋")
QB = VAULT / "04-题库"
MEDIA = VAULT / "媒体仓库"
OUTDIR = VAULT / "00-首页" / "题组Word" / "初赛模拟卷" / "真题版式"
TMP = VAULT / ".workbuddy" / "tmp" / "chusai_zhenti"
REF = TMP / "reference-zhenti.docx"
PANDOC = r"C:\Users\蕾赛\AppData\Local\Pandoc\pandoc.exe"

PANDOC_EXT = ("markdown+tex_math_dollars+tex_math_single_backslash"
              "+pipe_tables+raw_tex-superscript-subscript")


def blacken_colors(xml: str):
    """把 XML 里所有非黑 w:color 刷成 000000，并删掉 w:highlight。返回 (xml, 计数)。

    ⚠️ 必须对**成品 docx** 的 styles.xml 也跑一遍：pandoc 会自注入语法高亮 Token 样式
    （KeywordTok/DecValTok… 带 007020/902000/40a070 等色），不随 reference.docx 走。
    """
    n = [0]

    def _b(m):
        v = re.search(r'w:val="([0-9A-Fa-f]{6})"', m.group(0))
        if v and v.group(1).upper() != "000000":
            n[0] += 1
            return m.group(0).replace(v.group(1), "000000")
        return m.group(0)
    xml = re.sub(r"<w:color\b[^>]*/>", _b, xml)
    xml = re.sub(r"<w:highlight\b[^>]*/>", "", xml)
    return xml, n[0]

VOLS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

# ══════════════════════════════════════════════════════════════════
#  排版常量（改这里即可整批调参）
# ══════════════════════════════════════════════════════════════════
CN = "SimSun"                    # 中文正文/标题 统一宋体（真题实测为方正书宋系）
EN = "Times New Roman"
BODY_PT = 10.5                   # 五号
H1_PT = 16.0                     # 卷首标题
H2_PT = 12.0                     # 部分标题
H3_PT = 10.5                     # 题号
FOOT_PT = 9.0                    # 页脚
LINE_MULT = 1.15                 # 多倍行距（实测真题行间基线距 16.3~18.7pt）
MARGIN_TB = 2.2                  # cm
MARGIN_LR = 1.9                  # cm

# 元素符号表（用于「化学式 vs 变量」判定）
ELEMENTS = set("""
H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr
Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm
Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No
Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og
""".split())


# ══════════════════════════════════════════════════════════════════
#  1. 参照稿（reference.docx）
# ══════════════════════════════════════════════════════════════════
def build_reference(force=False):
    if REF.exists() and not force:
        return REF
    TMP.mkdir(parents=True, exist_ok=True)
    raw = TMP / "_ref_default.docx"
    r = subprocess.run([PANDOC, "--print-default-data-file", "reference.docx"],
                       capture_output=True, check=True)
    raw.write_bytes(r.stdout)

    import docx
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    doc = docx.Document(str(raw))

    # ── 页面 ──
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.top_margin = sec.bottom_margin = Cm(MARGIN_TB)
    sec.left_margin = sec.right_margin = Cm(MARGIN_LR)

    def set_pPr(style, lines=None, before=None, after=None, jc=None,
                keepnext=False, snap_off=True, first_line_chars=0):
        el = style.element
        pPr = el.find(qn("w:pPr"))
        if pPr is None:
            pPr = OxmlElement("w:pPr"); el.insert(0, pPr)
        for tag in ("w:keepNext", "w:snapToGrid", "w:spacing", "w:ind", "w:jc"):
            for e in pPr.findall(qn(tag)):
                pPr.remove(e)
        if keepnext:
            pPr.append(OxmlElement("w:keepNext"))
        if snap_off:
            e = OxmlElement("w:snapToGrid"); e.set(qn("w:val"), "0"); pPr.append(e)
        sp = OxmlElement("w:spacing")
        if before is not None:
            sp.set(qn("w:before"), str(int(before * 20)))
        if after is not None:
            sp.set(qn("w:after"), str(int(after * 20)))
        if lines is not None:
            sp.set(qn("w:line"), str(int(240 * lines)))
            sp.set(qn("w:lineRule"), "auto")
        pPr.append(sp)
        if first_line_chars:
            ind = OxmlElement("w:ind")
            ind.set(qn("w:firstLineChars"), str(first_line_chars))
            ind.set(qn("w:firstLine"), str(int(BODY_PT * first_line_chars / 100 * 20)))
            pPr.append(ind)
        if jc:
            e = OxmlElement("w:jc"); e.set(qn("w:val"), jc); pPr.append(e)

    def set_font(style, cn=CN, en=EN, size=BODY_PT, bold=False):
        style.font.name = en
        style.font.size = Pt(size)
        style.font.bold = bold
        style.font.color.rgb = None
        rPr = style.element.find(qn("w:rPr"))
        if rPr is None:
            rPr = OxmlElement("w:rPr"); style.element.append(rPr)
        for e in rPr.findall(qn("w:color")):
            rPr.remove(e)
        rf = rPr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts"); rPr.insert(0, rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs"):
            rf.set(qn(a), en)
        rf.set(qn("w:eastAsia"), cn)
        for a in ("w:eastAsiaTheme", "w:asciiTheme", "w:hAnsiTheme", "w:cstheme"):
            if qn(a) in rf.attrib:
                del rf.attrib[qn(a)]

    def has(name):
        try:
            return doc.styles[name]
        except KeyError:
            return None

    # 正文类
    for n in ("Normal", "Body Text", "First Paragraph", "Compact", "Block Text",
              "Table", "Table Caption", "Caption", "Image Caption", "Figure",
              "Captioned Figure", "Definition", "Definition Term", "Bibliography"):
        s = has(n)
        if s is None:
            continue
        set_font(s)
        if n == "Block Text":
            set_pPr(s, lines=LINE_MULT, before=6, after=6, jc="center")
        elif n in ("Table Caption", "Caption", "Image Caption"):
            set_pPr(s, lines=1.0, before=4, after=4, jc="center")
        else:
            set_pPr(s, lines=LINE_MULT, before=0, after=0)

    # 标题类
    for i in range(1, 7):
        s = has(f"Heading {i}")
        if s is None:
            continue
        if i == 1:
            set_font(s, size=H1_PT, bold=True)
            set_pPr(s, lines=LINE_MULT, before=0, after=12, jc="center", keepnext=True)
        elif i == 2:
            set_font(s, size=H2_PT, bold=True)
            set_pPr(s, lines=LINE_MULT, before=14, after=4, jc="center", keepnext=True)
        elif i == 3:
            set_font(s, size=H3_PT, bold=True)
            set_pPr(s, lines=LINE_MULT, before=13, after=2, jc="left", keepnext=True)
        else:
            set_font(s, size=BODY_PT, bold=True)
            set_pPr(s, lines=LINE_MULT, before=10, after=2, jc="left", keepnext=True)

    # ── 页脚：第 X 页，共 Y 页（居中）──
    ftr = doc.sections[0].footer
    ftr.is_linked_to_previous = False
    for p in list(ftr.paragraphs)[1:]:
        p._element.getparent().remove(p._element)
    p = ftr.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in list(p.runs):
        r._element.getparent().remove(r._element)

    def add_txt(t):
        r = p.add_run(t)
        r.font.size = Pt(FOOT_PT)
        r.font.name = EN
        r._element.rPr.rFonts.set(qn("w:eastAsia"), CN)
        return r

    def add_field(code):
        r1 = p.add_run(); r1.font.size = Pt(FOOT_PT)
        f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), "begin"); r1._element.append(f)
        r2 = p.add_run(); r2.font.size = Pt(FOOT_PT)
        it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
        it.text = f" {code} "; r2._element.append(it)
        r3 = p.add_run(); r3.font.size = Pt(FOOT_PT)
        s = OxmlElement("w:fldChar"); s.set(qn("w:fldCharType"), "separate"); r3._element.append(s)
        r4 = p.add_run("1"); r4.font.size = Pt(FOOT_PT)
        r5 = p.add_run(); r5.font.size = Pt(FOOT_PT)
        e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end"); r5._element.append(e)

    add_txt("第 ")
    add_field("PAGE")
    add_txt(" 页，共 ")
    add_field("NUMPAGES")
    add_txt(" 页")

    # ── 页眉清空 ──
    hdr = doc.sections[0].header
    hdr.is_linked_to_previous = False
    for hp in hdr.paragraphs:
        for r in list(hp.runs):
            r._element.getparent().remove(r._element)

    # ── 全样式彻底去色（含 pandoc 语法高亮 Token 样式；虽惰性，仍清成纯黑）──
    n_kill = 0
    for style in doc.styles:
        el = style.element
        for tag in ("w:color", "w:shd", "w:highlight"):
            for c in list(el.iter(qn(tag))):
                c.getparent().remove(c)
                n_kill += 1

    doc.save(str(REF))

    # ── 字符串兜底：styles.xml 里残留的 pandoc 语法高亮色（多挂在 docDefaults/latentStyles
    #    等非 w:style 节点上，python-docx 的 styles 集合扫不到）一律刷成纯黑 ──
    with zipfile.ZipFile(REF) as z:
        names = z.namelist()
        entries = {n: z.read(n) for n in names}
    st = entries["word/styles.xml"].decode("utf-8")
    st, n_str = blacken_colors(st)
    entries["word/styles.xml"] = st.encode("utf-8")

    print(f"[ref] 已生成参照稿 {REF}（对象级清色 {n_kill} 处 / 字符串级刷黑 {n_str} 处）")
    return REF


# ══════════════════════════════════════════════════════════════════
#  2. md 改写
# ══════════════════════════════════════════════════════════════════
# 以下三个预处理函数与既有的 .workbuddy/tmp/build_simvol_docx.py 保持一致
# （图引用解析 / 内链降级 / $$ 块结构规范化），改口径须两处同步。
def resolve_images(body, log):
    def rep(m):
        name = m.group(1)
        p = MEDIA / name
        if not p.exists():
            log.append(f"   [缺图] {name}")
            return ""
        return f"![]({name})"
    return re.sub(r"!\[\[([^\]\|]+\.(?:jpg|png|jpeg|svg))(?:\|\d+)?\]\]", rep, body)


def dewikilink(body):
    body = re.sub(r"\[\[[^\]\|]*\|([^\]]*)\]\]", r"\1", body)
    body = re.sub(r"\[\[([^\]]*)\]\]", r"\1", body)
    return body


def escape_blanks(text):
    """把**数学域之外**的下划线转义，避免填空题横线被 pandoc 当强调标记吃掉。

    实测（2026-09-23）：源 md 用 `____` 作填空横线，pandoc 把成对的 `____` 解析成
    strong/emph 定界符 → 卷面只剩一个孤立 `_`，甚至横线整条消失
    （如「N4 与 N2 的关系是____。A. …」→ 关系是  。A.…）。九卷已核：`__X__`
    全部是填空横线，**没有**真正的 `__粗体__`，故直接全量转义是安全的。

    ⚠️ 必须按数学域切分后再转义：`$...$` 里的 `_` 是下标，转义会破坏公式。
    """
    parts = re.split(r"(\$\$[\s\S]*?\$\$|\$[^$\n]*\$)", text)
    for i in range(0, len(parts), 2):          # 偶数下标 = 非数学域
        parts[i] = re.sub(r"(?<!\\)_", r"\\_", parts[i])
    return "".join(parts)


def separate_figure_captions(text):
    """图片行与紧接的图注行之间补空行 → 让图注独立成段。

    源 md 里 `![[hash.jpg]]\\n（第9题图：…）` 无空行 ⇒ pandoc 视为同一段，
    居中后图注被排到图片右下角（实测卷VI 1 处、卷VII 5 处）。
    """
    lines = text.split("\n")
    out, n = [], 0
    for i, ln in enumerate(lines):
        s = ln.strip()
        out.append(ln)
        if s.startswith("![](") and i + 1 < len(lines) and lines[i + 1].strip():
            out.append(""); n += 1
    return "\n".join(out), n


def normalize_dd(txt):
    """按块结构规范化 `$$` 显示数学：块外补空行 ＋ 块内删空行（必须状态机）。"""
    lines = txt.split("\n")
    out, in_math, i, n = [], False, 0, len(txt.split("\n"))
    one_line = re.compile(r"^\$\$(.+)\$\$$")
    while i < n:
        l = lines[i]
        s = l.strip()
        if not in_math:
            if s == "$$":
                if out and out[-1].strip() != "":
                    out.append("")
                out.append("$$"); in_math = True; i += 1; continue
            if one_line.match(s):
                if out and out[-1].strip() != "":
                    out.append("")
                out.append(s)
                if i + 1 < n and lines[i + 1].strip() != "":
                    out.append("")
                i += 1; continue
            out.append(l); i += 1; continue
        if s == "":
            i += 1; continue
        if one_line.match(s):
            out.append(s); in_math = False
            if i + 1 < n and lines[i + 1].strip() != "":
                out.append("")
            i += 1; continue
        if s.endswith("$$"):
            out.append(l); in_math = False
            if i + 1 < n and lines[i + 1].strip() != "":
                out.append("")
            i += 1; continue
        out.append(l); i += 1
    return "\n".join(out)


EXAM_NOTE = re.compile(r"^>\s*\*\*考试说明\*\*")


def callout_to_quote(text: str):
    """Obsidian callout `> [!type] 内容` → pandoc 不识别，会把 `[!type]` 原样渲成乱码文本。
    统一剥去 `[!type]`(+可选标题) 标记，保留 `> ` 引用块（pandoc 渲为普通引用）。
    实测卷IX 有 2 处（[!warning] 撤题说明、[!info] 复算核验）。"""
    def rep(m):
        rest = m.group(2).strip()
        return f"> {rest}" if rest else ">"
    return re.sub(r"^(>+\s*)\[!\w+\][-+]?\s*(.*)$", rep, text, flags=re.M)


def transform_md(text: str, drop_exam_note: bool = True, title_suffix: str = ""):
    # 先整块删除撤题内容：pandoc 只删注释标记、不删标记之间的正文 ⇒ 卷IX 第7题会泄漏
    text = re.sub(
        r"<!--\s*BEGIN\s+WITHDRAWN[\s\S]*?<!--\s*END\s+WITHDRAWN[^>]*-->",
        "",
        text,
    )
    text = callout_to_quote(text)
    lines = text.split("\n")
    i = 0
    # 剥 frontmatter
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
    out, title, n_drop_note, n_drop_hr = [], None, 0, 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        # 撤题行（选题清单中标记「已撤题 / 隔离」的表格行）不得出现于发布稿
        if s.startswith("|") and ("已撤题" in s or "撤题隔离" in s):
            i += 1
            continue
        if s.startswith("# ") and title is None:
            t = s[2:].strip()
            t = re.sub(r"\s*[·・]\s*(?:学生版|答案版)(?=\s*）)", "", t)   # （非有机 · 学生版）→（非有机）
            t = re.sub(r"\s*[·・]\s*(?:学生版|答案版)\s*$", "", t)        # 裸后缀
            t = re.sub(r"（\s*(?:学生版|答案版)\s*）", "", t)
            t = t + title_suffix
            title = t
            out.append(f"# {t}")
            i += 1
            continue
        if drop_exam_note and EXAM_NOTE.match(ln):
            n_drop_note += 1
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                i += 1
            continue
        if s == "---":
            n_drop_hr += 1
            i += 1
            continue
        out.append(ln.rstrip())
        i += 1
    # 折叠连续空行
    res, blank = [], 0
    for ln in out:
        if ln.strip() == "":
            blank += 1
            if blank <= 1:
                res.append("")
        else:
            blank = 0
            res.append(ln)
    return "\n".join(res).strip() + "\n", title, n_drop_note, n_drop_hr


# ══════════════════════════════════════════════════════════════════
#  3. document.xml 手术
# ══════════════════════════════════════════════════════════════════
PPR_ORDER = ["w:pStyle", "w:keepNext", "w:keepLines", "w:pageBreakBefore", "w:framePr",
             "w:widowControl", "w:numPr", "w:suppressLineNumbers", "w:pBdr", "w:shd",
             "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
             "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
             "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
             "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
             "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl",
             "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange"]

TBLPR_ORDER = ["w:tblStyle", "w:tblpPr", "w:tblOverlap", "w:bidiVisual",
               "w:tblStyleRowBandSize", "w:tblStyleColBandSize", "w:tblW", "w:jc",
               "w:tblCellSpacing", "w:tblInd", "w:tblBorders", "w:shd", "w:tblLayout",
               "w:tblCellMar", "w:tblLook", "w:tblCaption", "w:tblDescription"]


SPACING_RE = re.compile(r"<w:spacing\b[^>]*/>")
IND_RE = re.compile(r"<w:ind\b[^>]*/>")
JC_RE = re.compile(r"<w:jc\b[^>]*/>")
JC_CENTER_RE = re.compile(r'<w:jc w:val="center"')

PPR_RE = re.compile(r"<w:pPr>[\s\S]*?</w:pPr>")
PARA_RE = re.compile(r"<w:p\b[\s\S]*?</w:p>")
TBL_RE = re.compile(r"<w:tbl>[\s\S]*?</w:tbl>")
TBLPR_RE = re.compile(r"<w:tblPr>[\s\S]*?</w:tblPr>")
ROW_RE = re.compile(r"<w:tr\b[\s\S]*?</w:tr>")
CELL_RE = re.compile(r"<w:tc>[\s\S]*?</w:tc>")
GRID_RE = re.compile(r"<w:tblGrid>[\s\S]*?</w:tblGrid>")
TCW_RE = re.compile(r"<w:tcW\b[^>]*/>")

# A4 21cm − 左右各 1.9cm = 17.2cm = 9752 twips
TEXT_W_TW = 9752
WIDE = re.compile(r"[\u1100-\u115f\u2e80-\ua4cf\ua960-\ua97f\uac00-\ud7ff"
                  r"\uf900-\ufaff\ufe10-\ufe19\ufe30-\ufe6f\uff00-\uff60\uffe0-\uffe6]")


def _disp_w(s: str) -> float:
    """近似显示宽度：全角 2、半角 1、下标数字 0.6。"""
    w = 0.0
    for ch in s:
        if WIDE.match(ch):
            w += 2
        elif ch in "0123456789":
            w += 0.6
        elif ch in " ()[]{}·⋅/+-−=×":
            w += 0.5
        else:
            w += 1
    return w


def set_table_widths(xml: str, stat: dict) -> str:
    """按内容宽度分配列宽，替掉 pandoc 的「等宽列」。

    pandoc 只看分隔行的破折号个数，实测九卷 11 张表全被排成等宽：
    「外侧 EB 总浓度」这类 8 字标签被挤成两行，而右侧数字列空一大截。
    这里按每列最大内容宽度成比例分配（下限 3 字宽、上限 45% 表宽），
    并写死 tblLayout=fixed 使 Word/WPS/LO 三端一致。
    有合并单元格（列数不齐）的表跳过，不动。
    """
    def fix(m):
        t = m.group(0)
        if SHEET_TABLE_MARK in t:
            # 已由生成器写死列宽（答题卡的得分栏）→ 不参与自动分列宽
            stat["tbl_skip"] += 1
            return t
        rows = ROW_RE.findall(t)
        if not rows:
            return t
        grid = []
        ncol = max(len(CELL_RE.findall(r)) for r in rows)
        if ncol == 0 or any(len(CELL_RE.findall(r)) not in (ncol,) for r in rows):
            stat["tbl_skip"] += 1
            return t
        units = [0.0] * ncol
        cells_all = []
        for r in rows:
            cs = CELL_RE.findall(r)
            cells_all.append(cs)
            for j, c in enumerate(cs):
                txt = "".join(re.findall(r"<w:t(?:\s[^>]*)?>([\s\S]*?)</w:t>", c))
                txt = (txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"))
                units[j] = max(units[j], _disp_w(txt))
        # 权重 = max(内容宽, 3) + 1.5（吸收单元格左右边距 216twips≈1.2字宽）
        wt = [max(u, 3.0) + 1.5 for u in units]
        cap = 0.45 * sum(wt)
        wt = [min(x, cap) for x in wt]
        tot = sum(wt)
        wid = [max(600, int(TEXT_W_TW * x / tot)) for x in wt]
        # 末尾配平到 TEXT_W_TW
        wid[-1] += TEXT_W_TW - sum(wid)
        # 1) tblGrid
        g = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{w}"/>' for w in wid) + "</w:tblGrid>"
        t = GRID_RE.sub(g, t, count=1) if GRID_RE.search(t) else t
        # 2) tblW + tblLayout=fixed
        def fix_pr(pm):
            body = pm.group(0)
            body = body.replace('<w:tblW w:type="auto" w:w="0" />',
                                f'<w:tblW w:type="dxa" w:w="{TEXT_W_TW}" />')
            body = re.sub(r'<w:tblW\b[^>]*/>', f'<w:tblW w:type="dxa" w:w="{TEXT_W_TW}"/>', body, count=1)
            for e in re.findall(r"<w:tblLayout\b[^>]*/>", body):
                body = body.replace(e, "")
            lay = '<w:tblLayout w:type="fixed"/>'
            idx = TBLPR_ORDER.index("w:tblLayout")
            inner = body[len("<w:tblPr>"):-len("</w:tblPr>")]
            pos = len(inner)
            for t2 in TBLPR_ORDER[idx + 1:]:
                mm = re.search(r"<%s\b" % t2, inner)
                if mm:
                    pos = min(pos, mm.start())
            inner = inner[:pos] + lay + inner[pos:]
            return "<w:tblPr>" + inner + "</w:tblPr>"
        t = TBLPR_RE.sub(fix_pr, t, count=1)
        # 3) 每个单元格 tcW（CT_TcPr 里 tcW 在 cnfStyle 之后、gridSpan 之前）
        def fix_row(row: str) -> str:
            out, last = [], 0
            for j, cm in enumerate(CELL_RE.finditer(row)):
                cell = cm.group(0)
                tcw = f'<w:tcW w:type="dxa" w:w="{wid[min(j, len(wid)-1)]}"/>'
                if TCW_RE.search(cell):
                    cell = TCW_RE.sub(tcw, cell, count=1)
                elif "<w:tcPr/>" in cell:
                    cell = cell.replace("<w:tcPr/>", f"<w:tcPr>{tcw}</w:tcPr>", 1)
                elif "<w:tcPr>" in cell:
                    cell = cell.replace("<w:tcPr>", f"<w:tcPr>{tcw}", 1)
                else:
                    cell = cell.replace("<w:tc>", f"<w:tc><w:tcPr>{tcw}</w:tcPr>", 1)
                out.append(row[last:cm.start()]); out.append(cell)
                last = cm.end()
            out.append(row[last:])
            return "".join(out)

        # 用 split/join 重建，避免边改边用旧位置切片
        segs = ROW_RE.split(t)
        rows2 = ROW_RE.findall(t)
        t = segs[0] + "".join(fix_row(r) + (segs[k + 1] if k + 1 < len(segs) else "")
                              for k, r in enumerate(rows2))
        stat["tbl_width"] += 1
        return t
    return TBL_RE.sub(fix, xml)


def para_text(p: str) -> str:
    txt = "".join(re.findall(r"<w:t(?:\s[^>]*)?>([\s\S]*?)</w:t>", p))
    txt += "".join(re.findall(r"<m:t(?:\s[^>]*)?>([\s\S]*?)</m:t>", p))
    return (txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            .replace("&quot;", '"').replace("&apos;", "'"))


def para_style(p: str) -> str:
    m = re.search(r"<w:pStyle w:val=\"([^\"]+)\"", p)
    return m.group(1) if m else ""


def set_spacing(p: str, line_mult=None, before_pt=None, after_pt=None, exact=None) -> str:
    new = ""
    if exact:
        new = f'<w:spacing w:before="{int((before_pt or 0)*20)}" w:after="{int((after_pt or 0)*20)}" w:line="{int(exact*20)}" w:lineRule="exact"/>'
    else:
        b = f'w:before="{int((before_pt or 0)*20)}" ' if before_pt is not None else ""
        a = f'w:after="{int((after_pt or 0)*20)}" ' if after_pt is not None else ""
        l = f'w:line="{int(240*line_mult)}" w:lineRule="auto"' if line_mult else ""
        new = f"<w:spacing {b}{a}{l}/>"
    if "<w:pPr>" in p:
        if SPACING_RE.search(p):
            p = SPACING_RE.sub(new, p, count=1)
        else:
            p = _insert_into_pPr(p, "spacing", new)
    return p


def _insert_into_pPr(p: str, tag: str, xml: str) -> str:
    m = PPR_RE.search(p)
    if not m:
        return p
    body = m.group(0)
    inner = body[len("<w:pPr>"):-len("</w:pPr>")]
    idx = PPR_ORDER.index("w:" + tag)
    pos = len(inner)
    for t in PPR_ORDER[idx + 1:]:
        mm = re.search(r"<%s\b" % t, inner)
        if mm:
            pos = min(pos, mm.start())
    new_inner = inner[:pos] + xml + inner[pos:]
    return p[:m.start()] + "<w:pPr>" + new_inner + "</w:pPr>" + p[m.end():]


def add_indent(p: str, chars=200) -> str:
    xml = f'<w:ind w:firstLineChars="{chars}" w:firstLine="{int(BODY_PT*chars/100*20)}"/>'
    if IND_RE.search(p):
        return IND_RE.sub(xml, p, count=1)
    return _insert_into_pPr(p, "ind", xml)


def force_jc(p: str, val: str) -> str:
    xml = f'<w:jc w:val="{val}"/>'
    if JC_RE.search(p):
        return JC_RE.sub(xml, p, count=1)
    return _insert_into_pPr(p, "jc", xml)


# 图片尺寸上限（EMU），与 11-模板/scripts/docx_utils.py 的图片定尺逻辑保持一致
# （横向 ≤10cm / 纵向 ≤7cm / 方形 ≤9cm；小图放大到 5cm），避免两套产物图大小不一致。
CM_TO_EMU = 360000
MAX_LANDSCAPE = int(10.0 * CM_TO_EMU)
MAX_PORTRAIT = int(7.0 * CM_TO_EMU)
MAX_SQUARE = int(9.0 * CM_TO_EMU)
MIN_WIDTH = int(4.0 * CM_TO_EMU)
ENLARGE_TARGET = int(5.0 * CM_TO_EMU)
EXTENT_RE = re.compile(r'<wp:extent cx="(\d+)" cy="(\d+)"')
A_EXT_RE = re.compile(r'<a:ext cx="(\d+)" cy="(\d+)"')


def cap_image_width(p: str) -> str:
    """按宽高比限制图片尺寸（横向≤10cm/纵向≤7cm/方形≤9cm；过小图放大到 5cm）。

    pandoc 默认把图放大到页宽，真题版式原先无任何约束 ⇒ 卷VII 第1题三张小图竖排
    占满整页。此函数按 aspect 定尺，与基础版（docx_utils）口径统一。
    """
    def _size(cx, cy):
        if cx <= 0 or cy <= 0:
            return cx, cy
        aspect = cx / cy
        if aspect > 1.3:
            max_w = MAX_LANDSCAPE
        elif aspect < 0.7:
            max_w = MAX_PORTRAIT
        else:
            max_w = MAX_SQUARE
        if cx < MIN_WIDTH:
            r = ENLARGE_TARGET / cx
            return ENLARGE_TARGET, int(cy * r)
        if cx > max_w:
            r = max_w / cx
            return max_w, int(cy * r)
        return cx, cy

    def rep(m):
        cx, cy = _size(int(m.group(1)), int(m.group(2)))
        return f'<wp:extent cx="{cx}" cy="{cy}"'

    # 同步更新 drawingml 的 a:ext（与 wp:extent 成对出现，保持尺寸一致）
    def rep_a(m):
        cx, cy = _size(int(m.group(1)), int(m.group(2)))
        return f'<a:ext cx="{cx}" cy="{cy}"'

    p = EXTENT_RE.sub(rep, p)
    p = A_EXT_RE.sub(rep_a, p)
    return p


# 单元格内插图：按所在单元格宽度收缩（并排图用，防溢出单元格）
CELL_GRID_RE = re.compile(r'<w:gridCol w:w="(\d+)"')
CELL_MARGIN_EMU = int(0.3 * CM_TO_EMU)  # 单元格左右留白


def cap_table_images(tbl_xml: str) -> str:
    """把表格内每张图按所在列宽收缩（仅在超出列宽时）。

    pandoc 把表格内图片按原图比例放到「页面可用宽度」⇒ 三列并排时会溢出列宽。
    此函数按 `w:gridCol` 列宽（DXA，1/20 pt）逐个单元格收图。
    """
    grids = [int(g) for g in CELL_GRID_RE.findall(tbl_xml)]
    if not grids:
        return tbl_xml
    # DXA → EMU：1 pt = 12700 EMU，gridCol 单位是 1/20 pt ⇒ 1 dxa = 635 EMU
    col_emu = [int(g * 635) for g in grids]

    # 逐单元格处理（<w:tc>…</w:tc>），按出现顺序对应列序
    tc_re = re.compile(r"<w:tc>.*?</w:tc>", re.S)
    idx = [0]

    def fix_tc(m):
        frag = m.group(0)
        col = idx[0] % len(col_emu)
        idx[0] += 1
        limit = max(int(1.0 * CM_TO_EMU), col_emu[col] - CELL_MARGIN_EMU)

        def _size(cx, cy):
            if cx <= 0 or cy <= 0 or cx <= limit:
                return cx, cy
            r = limit / cx
            return limit, int(cy * r)

        frag = EXTENT_RE.sub(
            lambda mm: (lambda s: f'<wp:extent cx="{s[0]}" cy="{s[1]}"')(_size(int(mm.group(1)), int(mm.group(2)))), frag)
        frag = A_EXT_RE.sub(
            lambda mm: (lambda s: f'<a:ext cx="{s[0]}" cy="{s[1]}"')(_size(int(mm.group(1)), int(mm.group(2)))), frag)
        return frag

    return tc_re.sub(fix_tc, tbl_xml)


SKIP_STYLES = {"Heading1", "Heading2", "Heading3", "Heading4", "Heading5",
               "Heading6", "Title", "Subtitle", "BlockText", "SourceCode",
               "TableCaption", "ImageCaption", "Caption"}
SUBQ_RE = re.compile(r"^\s*(?:\d+-\d+|\d+\.\d+|（\d+）|\(\d+\)|[①②③④⑤⑥⑦⑧⑨⑩])")
CAPTION_RE = re.compile(r"^[（(]?第\s*\d+\s*题\s*图|^图\s*\d+")


def process_document_xml(xml: str, stat: dict) -> str:
    # —— 表格内插图先按列宽收缩（并排图防溢出），再做段落级处理 ——
    xml = TBL_RE.sub(lambda m: cap_table_images(m.group(0)), xml)
    # —— 表格外区域 vs 表格内：先记下表格区间，表格段落不做首行缩进 ——
    tbl_spans = [(m.start(), m.end()) for m in TBL_RE.finditer(xml)]

    def in_table(pos):
        return any(a <= pos < b for a, b in tbl_spans)

    out = []
    last = 0
    for m in PARA_RE.finditer(xml):
        p = m.group(0)
        pos = m.start()
        out.append(xml[last:pos])
        last = m.end()

        style = para_style(p)
        txt = para_text(p)
        has_draw = "<w:drawing" in p
        has_disp_math = "<m:oMathPara" in p
        is_list = "<w:numPr>" in p

        if style in SKIP_STYLES:
            if style == "BlockText":
                # 引用块分诊：卷尾「—— 试卷结束 ——」居中；其余（答案版的「组卷口径」/
                # 逐题「来源…｜难度」）左对齐——若一律居中，16 行来源注记会全部居中，很难看
                t = txt.strip()
                if re.match(r"^[—–\-]{2,}", t) or "试卷结束" in t:
                    p = set_spacing(p, line_mult=LINE_MULT, before_pt=6, after_pt=6)
                    p = force_jc(p, "center")
                else:
                    stat["quote"] += 1
                    p = set_spacing(p, line_mult=1.0, before_pt=4, after_pt=4)
                    p = force_jc(p, "left")
                out.append(p)
            else:
                out.append(p)
            continue
        if in_table(pos):
            out.append(p); continue
        if not txt.strip() and not has_draw:
            out.append(p); continue

        # 图片/独立公式段：行距改 auto（固定行距会裁切），居中，不缩进
        if has_draw or has_disp_math:
            p = set_spacing(p, line_mult=1.0, before_pt=6, after_pt=6)
            p = force_jc(p, "center")
            if has_draw:
                p = cap_image_width(p)      # 限制单图最大宽度，防小图被放大撑满整页
            stat["img"] += 1
            out.append(p); continue

        # 列表项：不缩进
        if is_list:
            p = set_spacing(p, line_mult=LINE_MULT, before_pt=0, after_pt=0)
            out.append(p); continue

        # 图注（「第N题图…」）：居中、不缩进
        if CAPTION_RE.match(txt.strip()):
            stat["caption"] += 1
            p = set_spacing(p, line_mult=LINE_MULT, before_pt=2, after_pt=6)
            p = force_jc(p, "center")
            out.append(p); continue

        # 子问编号顶格
        if SUBQ_RE.match(txt):
            stat["subq"] += 1
            p = set_spacing(p, line_mult=LINE_MULT, before_pt=0, after_pt=0)
            out.append(p); continue

        if JC_CENTER_RE.search(p):   # 居中段（答题卡信息栏等）不加首行缩进，否则整行被推右
            p = set_spacing(p, line_mult=LINE_MULT, before_pt=0, after_pt=0)
            out.append(p); continue
        stat["indent"] += 1
        p = set_spacing(p, line_mult=LINE_MULT, before_pt=0, after_pt=0)
        p = add_indent(p, 200)
        out.append(p)
    out.append(xml[last:])
    xml = "".join(out)

    # —— 表格：全框线 ——
    BORDERS = ('<w:tblBorders>'
               '<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
               '<w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
               '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
               '<w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
               '<w:insideH w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
               '<w:insideV w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
               '</w:tblBorders>')

    def fix_tbl(m):
        t = m.group(0)
        stat["tbl"] += 1

        def fix_pr(pm):
            body = pm.group(0)
            inner = body[len("<w:tblPr>"):-len("</w:tblPr>")]
            for e in re.findall(r"<w:tblBorders\b[\s\S]*?</w:tblBorders>", inner):
                inner = inner.replace(e, "")
            idx = TBLPR_ORDER.index("w:tblBorders")
            pos = len(inner)
            for t2 in TBLPR_ORDER[idx + 1:]:
                mm = re.search(r"<%s\b" % t2, inner)
                if mm:
                    pos = min(pos, mm.start())
            inner = inner[:pos] + BORDERS + inner[pos:]
            return "<w:tblPr>" + inner + "</w:tblPr>"

        if TBLPR_RE.search(t):
            t = TBLPR_RE.sub(fix_pr, t, count=1)
        else:
            t = t.replace("<w:tbl>", "<w:tbl><w:tblPr>" + BORDERS + "</w:tblPr>", 1)
        return t

    xml = TBL_RE.sub(fix_tbl, xml)
    xml = set_table_widths(xml, stat)

    # —— 去彩色：document.xml 里非黑 w:color 一律删 ——
    def kill_color(m):
        v = re.search(r'w:val="([0-9A-Fa-f]{6})"', m.group(0))
        if v and v.group(1).upper() not in ("000000", "AUTO"):
            stat["color"] += 1
            return ""
        return m.group(0)
    xml = re.sub(r"<w:color\b[^>]*/>", kill_color, xml)
    xml = re.sub(r"<w:highlight\b[^>]*/>", "", xml)
    return xml


# ══════════════════════════════════════════════════════════════════
#  4. OMML：化学式转正体
# ══════════════════════════════════════════════════════════════════
OMATH_RE = re.compile(r"<m:oMath>[\s\S]*?</m:oMath>")
M_RUN_RE = re.compile(r"<m:r>([\s\S]*?)</m:r>")
FONT_XML = ('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
            'w:cs="Times New Roman" w:eastAsia="SimSun"/>')
RFONTS_RE = re.compile(r"<w:rFonts\b[^>]*/>")

# 希腊字母 / 中日韩：出现即视为「符号式」（热力学量、相态、角度…），一律保持斜体。
# 关键反例：$S_m^\theta$ → 文本 "Smθ"，若不当心会被当成钐(Sm)而误改正体。
GREEK_CJK = re.compile(r"[\u0370-\u03ff\u0400-\u04ff\u2c80-\u2cff\u4e00-\u9fff\u3000-\u303f]")
# 化学惯例写正体的非元素记号
UPRIGHT_EXACT = {"pH", "pOH", "pKa", "pKb", "pKw", "pKsp", "pE", "pD", "D", "L"}
FORMULA_CHARS = re.compile(r"^[A-Za-z0-9()\[\]{}·⋅\-–—+−=→⇌/.,;:*\s°%]+$")


def _looks_formula(t: str) -> str:
    """判定一个 oMath 是否是「化学式/方程式」（应排正体）。

    保守策略：宁可漏判（保持斜体）也不误判（把变量弄成正体）。
    """
    s = re.sub(r"[\s\u200b]", "", t)
    if not s:
        return ""
    # 相态记号 α-Sn / β-Sn / γ-Fe / α-Fe2O3：希腊字母保持斜体，其后元素式排正体
    m2 = re.fullmatch(r"[\u0370-\u03ff](?:[-–—](.+))?", s)
    if m2:
        rest = m2.group(1) or ""
        if rest and (re.fullmatch(r"[A-Z][a-z]?", rest) or _looks_formula(rest)):
            return "希腊前缀相态"
    if GREEK_CJK.search(s):
        return ""
    if s in UPRIGHT_EXACT:
        return "惯例记号"
    lts = re.findall(r"[A-Z][a-z]?", s)
    two = {x for x in lts if len(x) == 2 and x in ELEMENTS}
    one = {x for x in lts if len(x) == 1 and x in ELEMENTS}
    syms = two | one
    if not syms or not FORMULA_CHARS.match(s):
        return ""
    # 裸元素符号 + 电荷（K⁺ / Cl⁻ / Fe³⁺ 之类）
    mc = re.fullmatch(r"([A-Z][a-z]?)[+\-−]+", s)
    if mc and mc.group(1) in ELEMENTS:
        return "离子"
    digits = re.findall(r"\d+", s)
    if not digits:
        # 无下标：须含 ≥2 个不同元素符号（挡掉 Sm/Tm/Ar/Cs 这类「大写字母＋下标字母」误判）
        return "多元素无下标" if len(syms) >= 2 else ""
    if len(syms) == 1:
        # 单元素带下标：下标须 ≥2（O2/I2/S8 是分子；V0/V1/c1 是变量下标 0/1）；
        # 允许尾随电荷记号（Mn²⁺ / Hg²⁺ / Mg²⁺ 等）
        m = re.fullmatch(r"([A-Z][a-z]?)(\d+)[+\-−]*", s)
        if m and m.group(1) in ELEMENTS and int(m.group(2)) >= 2:
            return "单元素带下标"
        return ""
    return "含下标式子"


ZWSP_BASE = re.compile("<m:t>\u200b</m:t>")
ZWSP_FIXED = '<m:t xml:space="preserve"> </m:t>'


def fix_empty_math_base(xml: str):
    """OMML 空基填一个空格，消掉卷面空心方框 ❑。

    成因：源 md 的前置上/下标写法（`$^{232}_{92}\\mathrm{U}$` 表示 ²³²₉₂U）
    → pandoc 产出 `<m:sSup><m:e><m:r><m:t>\\u200b</m:t></m:r></m:e>…`，
    **基为空**（ZWSP 无字形）→ 渲染器画出空框。实测九卷共 62 处。
    三方案实测选型（见 skill docx-print-polish）：填空格 有效（2→0），
    删 ZWSP / 填两个 ZWSP 均无效。
    """
    n = len(ZWSP_BASE.findall(xml))
    return (ZWSP_BASE.sub(ZWSP_FIXED, xml), n) if n else (xml, 0)


def omml_upright(xml: str, stat: dict) -> str:
    """化学式改正体：给判定为「化学式/方程式」的 oMath 内每个含字母的 `<m:r>` 加 `<m:rPr><m:sty m:val="p"/>`。

    ⚠️ 用一个统一的「单 run 改写」函数（不是整 run 重建），这样：
      · 已有 `<w:rPr>`（字体钉定）的 run 不会被打乱父子顺序；
      · `<m:rPr>` 必须排在 `<m:r>` 的第一个子元素，故用前插。
    调用顺序：必须**先于** `omml_pin_font`（后者会插 `<w:rPr>`，使按 `<m:t>` 相邻匹配的旧写法失效）。
    """
    def fix(m):
        blk = m.group(0)
        txt = "".join(re.findall(r"<m:t(?:\s[^>]*)?>([\s\S]*?)</m:t>", blk))
        txt = (txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
               .replace("&quot;", '"').replace("&apos;", "'"))
        why = _looks_formula(txt)
        if not why:
            return blk
        stat["formula"] += 1

        def fix_run(rm):
            inner = rm.group(1)
            if "<m:t" not in inner or "<m:rPr>" in inner:
                return rm.group(0)
            rt = "".join(re.findall(r"<m:t(?:\s[^>]*)?>([\s\S]*?)</m:t>", inner))
            if not re.search(r"[A-Za-z]", rt):
                return rm.group(0)
            return ('<m:r><m:rPr><m:sty m:val="p"/></m:rPr>' + inner + "</m:r>")
        return M_RUN_RE.sub(fix_run, blk)
    return OMATH_RE.sub(fix, xml)


# ── 字体统一：所有数字/西文/符号 → Times New Roman，中文与中文标点 → 宋体 ──
MATH_RPR = ('<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
            'w:cs="Times New Roman" w:eastAsia="SimSun"/></w:rPr>')


def unify_fonts(xml: str):
    """把每一处 `<w:rFonts>` 规范化成「西文 TNR + 中文宋体」，并**去掉 `w:hint="eastAsia"`**。

    为什么必须去掉 hint：pandoc 对「以汉字开头的 run」会写 `<w:rFonts w:hint="eastAsia"/>`，
    于是该 run 里的**数字与符号也用中文宋体渲染**（宋体的数字是等宽老式字形，与 TNR 明显不同）
    ⇒ 同一页里「第 1 题」的 1、`700 °C` 的 700、`pH 4.70` 的 4.70 各用不同字体。
    去掉 hint 后，Word 按字符的 Unicode 区段分派：ASCII/西文符号 → TNR，汉字与全角标点 → 宋体，
    正是需求「所有数字和符号用 TNR，特殊中文符号除外」。
    """
    n = [0]

    def rep(m):
        n[0] += 1
        return FONT_XML
    return RFONTS_RE.sub(rep, xml), n[0]


def omml_pin_font(xml: str, stat: dict) -> str:
    """给每个数学 run 钉定西文字体（`<m:r>` 内插 `<w:rPr><w:rFonts …/>`）。

    ⚠️ Schema 顺序（CT_R）＝ `m:rPr?` → `w:rPr?` → 内容(`m:t`)，故插在 `<m:t>` 之前。
    两套机制同时上：本函数管 run 级、`set_math_font` 管文档级 `m:mathPr/m:mathFont`。
    实测 LibreOffice 的 OMML 导入**不认**这两处（仍用 LiberationSerif 代排），属渲染器限制；
    Word/WPS 按规范认。
    """
    def fix(m):
        inner = m.group(1)
        if "<w:rPr>" in inner or "<m:t" not in inner:
            return m.group(0)
        i = inner.find("<m:t")
        stat["omml_font"] += 1
        return "<m:r>" + inner[:i] + MATH_RPR + inner[i:] + "</m:r>"
    return M_RUN_RE.sub(fix, xml)


def set_math_font(settings_xml: str):
    """文档级数学字体 → Times New Roman（`w:mathPr/m:mathFont`）。"""
    if "<m:mathPr" in settings_xml:
        settings_xml = re.sub(r'<m:mathFont\b[^>]*/>',
                              '<m:mathFont m:val="Times New Roman"/>', settings_xml, count=1)
        return settings_xml, 1
    mp = ('<m:mathPr><m:mathFont m:val="Times New Roman"/>'
          '<m:brkBin m:val="before"/><m:brkBinSub m:val="--"/><m:smallFrac m:val="0"/>'
          '<m:dispDef/><m:lMargin m:val="0"/><m:rMargin m:val="0"/>'
          '<m:defJc m:val="centerGroup"/><m:wrapIndent m:val="1440"/>'
          '<m:intLim m:val="subSup"/><m:naryLim m:val="undOvr"/></m:mathPr>')
    return settings_xml.replace("</w:settings>", mp + "</w:settings>"), 1


FONT_PARTS = ("word/document.xml", "word/styles.xml", "word/numbering.xml",
              "word/footnotes.xml", "word/comments.xml", "word/endnotes.xml")


# ══════════════════════════════════════════════════════════════════
#  6. 答题卡
# ══════════════════════════════════════════════════════════════════
QH_RE = re.compile(r"^###\s+第\s*(\d+)\s*题\s*（\s*(\d+)\s*分\s*）")
SEC_RE = re.compile(r"^##\s+(第[一二三]部分.*)$")
ANS_HEAD_RE = re.compile(r"^#{3,6}\s*答案")
# 每题答卷高度：按「答案篇幅」折算手写行数（手写密度约为排版的 1/2，再加 2 行余量）
SHEET_LINE_PT = 26.0        # 一行书写高度（≈0.92cm）


def _answer_lengths(vol: str):
    """从答案版 md 取：分部分标题、每题 (题号, 分值, 答案显示宽度)。

    ⚠️ 答案小节的标题层级**不统一**：常规是 `#### 答案`，另有若干 `### 答案（原书答案区 L####）`
    的溯源标注（卷VI 4 处、卷VII/IX 各 1 处）。前版用「`^#{2,3}` 即结束」的通用守卫，
    会被这类三级标题**提前截断**，导致卷VI 第2/7/11/15 题、卷IX 第6 题量到 0 字。
    现改为「只在遇到新题/分部/卷末附录时结束」，标题层级放宽到 3~6。
    """
    md = (QB / f"初赛模拟卷{vol}（非有机·答案版）.md").read_text(encoding="utf-8")
    if md.startswith("---"):
        e = md.find("\n---", 3)
        md = md[e + 4:] if e > 0 else md
    secs, items, order = [], {}, []
    cur_q, cur_ans, in_ans = None, [], False
    score = {}

    def flush():
        if cur_q is not None:
            items[cur_q] = "".join(cur_ans)

    for ln in md.split("\n"):
        if SEC_RE.match(ln):
            flush(); cur_q, cur_ans, in_ans = None, [], False
            secs.append((len(order), SEC_RE.match(ln).group(1)))
            continue
        if ln.lstrip().startswith("## 附") or ln.lstrip().startswith("## 选题清单"):
            flush(); cur_q, cur_ans, in_ans = None, [], False
            continue
        mq = QH_RE.match(ln)
        if mq:
            flush()
            cur_q = int(mq.group(1)); order.append(cur_q)
            score[cur_q] = int(mq.group(2))
            cur_ans, in_ans = [], False
            continue
        if ANS_HEAD_RE.match(ln):
            in_ans = True
            continue
        if cur_q is not None and in_ans:
            cur_ans.append(ln)
    flush()
    return secs, order, score, items


def _disp_units(s: str) -> float:
    """粗算答案「显示宽度」（全角 2 / 半角 1），剥掉 markdown 装饰但对图/表折算高度。

    图与表格按「折算宽度」计入（图 150、表行 55），否则「答案就是一张表/一张投影图」
    的题会被算成 0 字 ⇒ 答题框过小。
    """
    n_img = len(re.findall(r"!\[\]\([^)]*\)", s)) + len(re.findall(r"!\[\[[^\]]*\]\]", s))
    s = re.sub(r"!\[\]\([^)]*\)", "", s)
    s = re.sub(r"!\[\[[^\]]*\]\]", "", s)
    n_row = sum(1 for l in s.split("\n") if l.lstrip().startswith("|"))
    s = re.sub(r"\$+", "", s)
    s = re.sub(r"\\[A-Za-z]+", "x", s)          # \mathrm \frac 之类当 1 个符号
    s = re.sub(r"[{}]", "", s)
    s = re.sub(r"\|", " ", s)
    s = re.sub(r"^[>\-*#\s]+", "", s, flags=re.M)
    w = 0.0
    for ch in s:
        w += 2 if WIDE.match(ch) else 1
    return w + n_img * 150 + n_row * 55


# 答题框行数 = clamp(max(答案折算行, 分值×0.55), 4, 11)
# 分母 65 的口径：排版一行≈92 半角宽，手写一行≈65 半角宽 ⇒ 「手写占位 ≈1.4× 排版」。
# 另按分值兜底（有些题答案只给最终数值，但学生须写过程）。
# 🔴 上限 11 是被分页反推出来的：页容量 26 行、每题开销 2 行 ⇒ 每页只能放 2 个框；
#    上限若给 14，任何两框都塞不进一页，实测每页只剩 1 框、整卷 15 页且半数是空白。
def _sheet_lines(units: float, score: int) -> int:
    return max(4, min(11, max(int(round(units / 65)) + 1, int(round(score * 0.55)))))


# 答题卡版面标定：A4 版心高 717pt ÷ 行高 26pt ≈ 27.6 行；留 1.6 行安全余量 → 26 行/页
SHEET_PAGE_LINES = 26
SHEET_HEAD_LINES = 6        # 首页卷头（标题+信息栏+得分表+空行）折算行数
SHEET_Q_OVERHEAD = 2        # 每题题号行+空行的折算行数

# 答题卡用表：固定列宽（cm），交给 set_table_widths 跳过
SHEET_TABLE_MARK = '<w:tblLayout w:type="fixed"/>'


def build_answer_sheet(vol: str, ref: Path):
    """生成「答题卡」（信息栏 + 阅卷得分表 + 逐题作答框），无题面。

    分页策略：**贪心装箱**。逐题累加行数，若「已用 + 本题 + 题号开销」超过页容量，
    则在题号段上加 `pageBreakBefore` 翻页。这样既保证每个作答框不被切断（cantSplit），
    又不留大片空白——若不控页，14 页里会有近一半是空白（实测未控页时 14 页 vs 控页后 ~9 页）。
    """
    import docx
    from docx.enum.table import WD_ROW_HEIGHT_RULE
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, Cm

    secs, order, score, ans = _answer_lengths(vol)
    if not order:
        print(f"[SKIP] 答题卡 {vol}: 未解析到题目")
        return None

    doc = docx.Document(str(ref))
    body = doc.element.body
    for child in list(body):
        if child.tag.endswith("}sectPr"):
            continue
        body.remove(child)

    def para(text="", style=None, size=None, bold=None, align=None):
        p = doc.add_paragraph(style=style)
        if text:
            r = p.add_run(text)
            if size:
                r.font.size = Pt(size)
            if bold is not None:
                r.font.bold = bold
        if align is not None:
            p.alignment = align
        return p

    para(f"初赛模拟卷 {vol}（非有机）· 答题卡", style="Heading 1")

    info = para()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = info.add_run("姓名：____________　　学校：____________　　考号：____________")
    r.font.size = Pt(BODY_PT)

    para("得分栏（阅卷用）", style="Heading 4")

    # ── 阅卷得分表：列宽写死（自动分列宽会把「题号/得分」挤成两行）──
    nq = len(order)
    t = doc.add_table(rows=2, cols=nq + 2)
    t.autofit = False
    W_LBL, W_Q = 1.30, 0.90
    widths = [W_LBL] + [W_Q] * nq + [W_LBL]
    hdr = ["题号"] + [str(q) for q in order] + ["总分"]
    for j, v in enumerate(hdr):
        c = t.cell(0, j)
        c.text = ""
        pr = c.paragraphs[0]
        pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rr = pr.add_run(v)
        rr.font.size = Pt(9)
    c0 = t.cell(1, 0)
    c0.text = ""
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = p0.add_run("得分")
    r0.font.size = Pt(9)
    for row in t.rows:
        row.height = Pt(22)
        row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        for j, cell in enumerate(row.cells):
            cell.width = Cm(widths[j])
    # 写死 tblLayout=fixed（set_table_widths 见此后跳过）
    tblPr = t._tbl.tblPr
    lay = tblPr.find(qn("w:tblLayout"))
    if lay is None:
        lay = OxmlElement("w:tblLayout"); tblPr.append(lay)
    lay.set(qn("w:type"), "fixed")
    # ⚠️ 必须同时改 tblGrid：固定布局下渲染器以 tblGrid 分列，
    #    只写 tcW 不改 grid 时 LibreOffice 仍按原等宽列排，9pt 的「题号/得分/总分」会被拆成两行。
    grid = t._tbl.find(qn("w:tblGrid"))
    if grid is not None:
        t._tbl.remove(grid)
    grid = OxmlElement("w:tblGrid")
    for w in widths:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(int(Cm(w).twips)))
        grid.append(gc)
    t._tbl.insert(list(t._tbl).index(tblPr) + 1, grid)

    para("", size=6)

    # ── 贪心装箱分页 ──
    used = SHEET_HEAD_LINES
    first = True
    total_lines = 0
    for q in order:
        units = _disp_units(ans.get(q, ""))
        nlines = _sheet_lines(units, score.get(q, 0))
        total_lines += nlines
        need = nlines + SHEET_Q_OVERHEAD
        if (not first) and used + need > SHEET_PAGE_LINES:
            used = 0
            brk = True
        else:
            brk = False
        h = para(f"第 {q} 题（{score.get(q, 0)} 分）", style="Heading 3")
        if brk:
            pp = h._p.get_or_add_pPr()
            pb = OxmlElement("w:pageBreakBefore")
            pp.insert(0, pb) if pp.find(qn("w:pStyle")) is None else pp.find(qn("w:pStyle")).addnext(pb)
        box = doc.add_table(rows=1, cols=1)
        box.cell(0, 0).text = ""
        row = box.rows[0]
        row.height = Pt(nlines * SHEET_LINE_PT)
        row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
        para("", size=6)
        used += need
        first = False

    stage = TMP / f"初赛模拟卷{vol}（非有机·答题卡）.docx"
    doc.save(str(stage))

    stat = {"img": 0, "subq": 0, "indent": 0, "tbl": 0, "color": 0, "formula": 0,
            "sty_color": 0, "empty_base": 0, "tbl_width": 0, "tbl_skip": 0,
            "caption": 0, "quote": 0, "font": 0, "omml_font": 0}
    with zipfile.ZipFile(stage) as z:
        names = z.namelist()
        entries = {n: z.read(n) for n in names}
    doc_xml, stat["font"] = unify_fonts(entries["word/document.xml"].decode("utf-8"))
    doc_xml = process_document_xml(doc_xml, stat)
    entries["word/document.xml"] = doc_xml.encode("utf-8")
    for part in FONT_PARTS:
        if part in entries and part != "word/document.xml":
            v2, _n = unify_fonts(entries[part].decode("utf-8"))
            if part == "word/styles.xml":
                v2, stat["sty_color"] = blacken_colors(v2)
            entries[part] = v2.encode("utf-8")
    for n in list(entries):
        if n.startswith("word/footer") or n.startswith("word/header"):
            v2, _n = unify_fonts(entries[n].decode("utf-8"))
            entries[n] = v2.encode("utf-8")
    if "word/settings.xml" in entries:
        s2, _n = set_math_font(entries["word/settings.xml"].decode("utf-8"))
        entries["word/settings.xml"] = s2.encode("utf-8")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    target = OUTDIR / f"初赛模拟卷{vol}（非有机·答题卡）.docx"
    tmp_out = TMP / f"_w_kz_{vol}.docx"
    with zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zo:
        for n in names:
            zo.writestr(n, entries[n])
    shutil.copyfile(tmp_out, target)
    os.remove(tmp_out)
    print(f"[OK]  卡 {vol:>4}  题数={nq} 表={stat['tbl']} 框宽={stat['tbl_width']} 字体={stat['font']} "
          f"总书写行≈{sum(_sheet_lines(_disp_units(ans.get(q, '')), score.get(q, 0)) for q in order)}")
    return target


# ══════════════════════════════════════════════════════════════════
#  7. 主流程
# ══════════════════════════════════════════════════════════════════
# 版本口径：
#   student —— 学生版：删「考试说明」引用块；标题去「· 学生版」后缀
#   answer  —— 答案与解析版：**内容一字不动**（组卷口径引用块、逐题「来源…｜难度」行、
#              卷末《附：选题清单（题卡溯源）》均为规范指定的答案版内容），仅换标题与卷面
EDITIONS = {
    "student": {
        "src": "初赛模拟卷{v}（非有机·学生版）.md",
        "out": "初赛模拟卷{v}（非有机·学生版·真题版式）.docx",
        "tmp": "初赛模拟卷{v}（非有机·真题版式）",
        "drop_exam_note": True,
        "title_suffix": "",
    },
    "answer": {
        "src": "初赛模拟卷{v}（非有机·答案版）.md",
        "out": "初赛模拟卷{v}（非有机·答案与解析版·真题版式）.docx",
        "tmp": "初赛模拟卷{v}（非有机·答案与解析·真题版式）",
        "drop_exam_note": False,
        "title_suffix": "· 答案与解析",
    },
}


def convert_one(vol: str, ref: Path, edition: str = "student"):
    cfg = EDITIONS[edition]
    src = QB / cfg["src"].format(v=vol)
    if not src.exists():
        print(f"[SKIP] 源缺失 {src.name}")
        return None
    raw = src.read_text(encoding="utf-8")
    new_md, title, nd_note, nd_hr = transform_md(
        raw, drop_exam_note=cfg["drop_exam_note"], title_suffix=cfg["title_suffix"])

    log = []
    n_img_before = len(re.findall(r"!\[\[", new_md))
    new_md = resolve_images(new_md, log)
    new_md = dewikilink(new_md)
    new_md = escape_blanks(new_md)
    new_md, n_cap = separate_figure_captions(new_md)
    new_md = normalize_dd(new_md)

    stage = TMP / (cfg["tmp"].format(v=vol) + ".md")
    with open(stage, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_md)

    docx = TMP / (cfg["tmp"].format(v=vol) + ".docx")
    cmd = [PANDOC, str(stage), "-o", str(docx),
           f"--from={PANDOC_EXT}", "--to=docx",
           f"--resource-path={MEDIA}", f"--reference-doc={ref}"]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(f"[FAIL] pandoc {vol}/{edition}: {r.stderr[:400]}")
        return None

    stat = {"img": 0, "subq": 0, "indent": 0, "tbl": 0, "color": 0, "formula": 0,
            "sty_color": 0, "empty_base": 0, "tbl_width": 0, "tbl_skip": 0,
            "caption": 0, "quote": 0, "font": 0, "omml_font": 0}
    with zipfile.ZipFile(docx) as z:
        names = z.namelist()
        entries = {n: z.read(n) for n in names}

    n_media = sum(1 for n in names if n.startswith("word/media/"))
    doc = entries["word/document.xml"].decode("utf-8")
    doc = process_document_xml(doc, stat)
    doc, stat["font"] = unify_fonts(doc)          # 先统一西文/中文字体（去 eastAsia hint）
    doc = omml_upright(doc, stat)                 # 再判化学式（依赖 <m:t> 紧邻匹配）
    doc = omml_pin_font(doc, stat)                # 最后钉数学 run 的西文字体
    doc, stat["empty_base"] = fix_empty_math_base(doc)
    entries["word/document.xml"] = doc.encode("utf-8")

    for part in FONT_PARTS:
        if part in entries and part != "word/document.xml":
            v2, _n = unify_fonts(entries[part].decode("utf-8"))
            if part == "word/styles.xml":
                v2, stat["sty_color"] = blacken_colors(v2)
            entries[part] = v2.encode("utf-8")
    for n in list(entries):
        if n.startswith("word/footer") or n.startswith("word/header"):
            v2, _n = unify_fonts(entries[n].decode("utf-8"))
            entries[n] = v2.encode("utf-8")
    if "word/settings.xml" in entries:
        s2, _n = set_math_font(entries["word/settings.xml"].decode("utf-8"))
        entries["word/settings.xml"] = s2.encode("utf-8")

    has_alt = any(b"AlternateContent" in v for k, v in entries.items() if k.endswith(".xml"))
    OUTDIR.mkdir(parents=True, exist_ok=True)
    target = OUTDIR / cfg["out"].format(v=vol)
    tmp_out = TMP / f"_w_{edition}_{vol}.docx"
    with zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zo:
        for n in names:
            zo.writestr(n, entries[n])
    shutil.copyfile(tmp_out, target)
    os.remove(tmp_out)

    warn = ""
    if n_img_before != n_media:
        warn = f"  ⚠️图不守恒 源{n_img_before}→media{n_media}"
    print(f"[OK] {edition[:4]:>4} {vol:>4}  标题={title!r}  删说明={nd_note} 删线={nd_hr}  "
          f"缩进={stat['indent']} 子问={stat['subq']} 引块={stat['quote']} "
          f"图={n_media}/{n_img_before} 表={stat['tbl']}/{stat['tbl_width']} "
          f"正体={stat['formula']} 空基={stat['empty_base']} 字体={stat['font']} 数式字体={stat['omml_font']} "
          f"图注={n_cap}/{stat['caption']}"
          f"{' AlternateContent=有' if has_alt else ''}{warn}")
    for l in log:
        print("     ", l)
    return target


def main():
    args = sys.argv[1:]
    rebuild = "--rebuild-ref" in args
    only_ans = "--answer" in args
    only_stu = "--student" in args
    only_kz = "--kazhu" in args
    vols = [a for a in args if not a.startswith("--")] or VOLS
    TMP.mkdir(parents=True, exist_ok=True)
    ref = build_reference(force=rebuild)
    done = []
    editions = []
    if only_ans:
        editions = ["answer"]
    elif only_stu:
        editions = ["student"]
    elif only_kz:
        editions = []
    else:
        editions = ["student", "answer"]
    for ed in editions:
        for v in vols:
            t = convert_one(v, ref, ed)
            if t:
                done.append(t)
    if only_kz or not editions:
        for v in vols:
            t = build_answer_sheet(v, ref)
            if t:
                done.append(t)
    print(f"\n完成 {len(done)}/{len(vols) * max(len(editions), 1)} → {OUTDIR}")


if __name__ == "__main__":
    main()
