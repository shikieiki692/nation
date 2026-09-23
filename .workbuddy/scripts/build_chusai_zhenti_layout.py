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


def transform_md(text: str):
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
        if s.startswith("# ") and title is None:
            t = s[2:].strip()
            t = re.sub(r"\s*[·・]\s*学生版(?=\s*）)", "", t)   # （非有机 · 学生版）→（非有机）
            t = re.sub(r"\s*[·・]\s*学生版\s*$", "", t)        # 裸后缀
            t = re.sub(r"（\s*学生版\s*）", "", t)
            title = t
            out.append(f"# {t}")
            i += 1
            continue
        if EXAM_NOTE.match(ln):
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


SKIP_STYLES = {"Heading1", "Heading2", "Heading3", "Heading4", "Heading5",
               "Heading6", "Title", "Subtitle", "BlockText", "SourceCode",
               "TableCaption", "ImageCaption", "Caption"}
SUBQ_RE = re.compile(r"^\s*(?:\d+-\d+|\d+\.\d+|（\d+）|\(\d+\)|[①②③④⑤⑥⑦⑧⑨⑩])")
CAPTION_RE = re.compile(r"^[（(]?第\s*\d+\s*题\s*图|^图\s*\d+")


def process_document_xml(xml: str, stat: dict) -> str:
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
            out.append(p); continue
        if in_table(pos):
            out.append(p); continue
        if not txt.strip() and not has_draw:
            out.append(p); continue

        # 图片/独立公式段：行距改 auto（固定行距会裁切），居中，不缩进
        if has_draw or has_disp_math:
            p = set_spacing(p, line_mult=1.0, before_pt=6, after_pt=6)
            p = force_jc(p, "center")
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
LETTER_RUN_RE = re.compile(r'<m:r>(?!<m:rPr>)(<m:t(?:\s[^>]*)?>)([\s\S]*?)(</m:t>)(\s*)</m:r>')

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
            inner = rm.group(2)
            if not re.search(r"[A-Za-z]", inner):
                return rm.group(0)
            return (f'<m:r><m:rPr><m:sty m:val="p"/></m:rPr>'
                    f'{rm.group(1)}{rm.group(2)}{rm.group(3)}{rm.group(4)}</m:r>')
        return LETTER_RUN_RE.sub(fix_run, blk)
    return OMATH_RE.sub(fix, xml)


# ══════════════════════════════════════════════════════════════════
#  5. 主流程
# ══════════════════════════════════════════════════════════════════
def convert_one(vol: str, ref: Path):
    src = QB / f"初赛模拟卷{vol}（非有机·学生版）.md"
    if not src.exists():
        print(f"[SKIP] 源缺失 {src.name}")
        return None
    raw = src.read_text(encoding="utf-8")
    new_md, title, nd_note, nd_hr = transform_md(raw)

    log = []
    n_img_before = len(re.findall(r"!\[\[", new_md))
    new_md = resolve_images(new_md, log)
    new_md = dewikilink(new_md)
    new_md = escape_blanks(new_md)
    new_md, n_cap = separate_figure_captions(new_md)
    new_md = normalize_dd(new_md)

    stage = TMP / f"初赛模拟卷{vol}（非有机·真题版式）.md"
    with open(stage, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_md)

    docx = TMP / f"初赛模拟卷{vol}（非有机·真题版式）.docx"
    cmd = [PANDOC, str(stage), "-o", str(docx),
           f"--from={PANDOC_EXT}", "--to=docx",
           f"--resource-path={MEDIA}", f"--reference-doc={ref}"]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(f"[FAIL] pandoc {vol}: {r.stderr[:400]}")
        return None

    stat = {"img": 0, "subq": 0, "indent": 0, "tbl": 0, "color": 0, "formula": 0, "sty_color": 0, "empty_base": 0, "tbl_width": 0, "tbl_skip": 0, "caption": 0}
    with zipfile.ZipFile(docx) as z:
        names = z.namelist()
        entries = {n: z.read(n) for n in names}

    n_media = sum(1 for n in names if n.startswith("word/media/"))
    doc = entries["word/document.xml"].decode("utf-8")
    doc = process_document_xml(doc, stat)
    doc = omml_upright(doc, stat)
    doc, stat["empty_base"] = fix_empty_math_base(doc)
    entries["word/document.xml"] = doc.encode("utf-8")

    sx = entries.get("word/styles.xml")
    if sx:
        sx, stat["sty_color"] = blacken_colors(sx.decode("utf-8"))
        entries["word/styles.xml"] = sx.encode("utf-8")

    has_alt = any(b"AlternateContent" in v for k, v in entries.items() if k.endswith(".xml"))
    OUTDIR.mkdir(parents=True, exist_ok=True)
    target = OUTDIR / f"初赛模拟卷{vol}（非有机·学生版·真题版式）.docx"
    tmp_out = TMP / f"_w_{vol}.docx"
    with zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zo:
        for n in names:
            zo.writestr(n, entries[n])
    shutil.copyfile(tmp_out, target)
    os.remove(tmp_out)

    warn = ""
    if n_img_before != n_media:
        warn = f"  ⚠️图不守恒 源{n_img_before}→media{n_media}"
    print(f"[OK] {vol:>4}  标题={title!r}  删考试说明行={nd_note} 删分隔线={nd_hr}  "
          f"缩进段={stat['indent']} 子问段={stat['subq']} 图={n_media}/{n_img_before} "
          f"表={stat['tbl']} 公式正体={stat['formula']} 空基修补={stat['empty_base']} 表宽={stat['tbl_width']} 图注={n_cap}/{stat['caption']} AlternateContent={'有' if has_alt else '无'}{warn}")
    for l in log:
        print("     ", l)
    return target


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    rebuild = "--rebuild-ref" in sys.argv
    TMP.mkdir(parents=True, exist_ok=True)
    ref = build_reference(force=rebuild)
    vols = only if only else VOLS
    done = []
    for v in vols:
        t = convert_one(v, ref)
        if t:
            done.append(t)
    print(f"\n完成 {len(done)}/{len(vols)} → {OUTDIR}")


if __name__ == "__main__":
    main()
