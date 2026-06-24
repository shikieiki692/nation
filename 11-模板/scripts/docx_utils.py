"""
docx_utils.py — 学生讲义 Word 输出共享风格库 (v2)

字体口径（依据用户反馈修正）：
  - 中文正文：宋体 SimSun（备选仿宋 FangSong）
  - 中文标题/表头：黑体 SimHei
  - 英文/数字/变量：Times New Roman

本库提供两类使用方式：
  A) 手动构建：base_doc() → title_block() → heading() → para() → simple_table()
  B) Pandoc 后处理：postprocess_pandoc_docx() 修正 pypandoc 生成文档的字体

提取自 tmp/docs/polarity-bridge-docx/build-polarity-bridge-docx.py
          tmp/docs/crystal-structure-docx/build-crystal-structure-docx.py
"""

from pathlib import Path
from typing import Optional
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

# ── 字体常量 ──────────────────────────────────────────────
CN_BODY_FONT = "SimSun"       # 宋体 — 中文正文 / 表格正文
CN_HEAD_FONT = "SimHei"       # 黑体 — 中文标题 / 表头
EN_FONT = "Times New Roman"    # 英文 / 数字 / 变量
CN_CAPTION_FONT = "FangSong"  # 仿宋 — 图例题注（仿宋五号居中）

TITLE_COLOR = RGBColor(23, 50, 77)    # 深蓝 — 标题/表头
SUB_COLOR = RGBColor(91, 105, 117)    # 灰蓝 — 副标题/注释

# ── 页面设置 ──────────────────────────────────────────────
PAGE_WIDTH = Cm(21)
PAGE_HEIGHT = Cm(29.7)
MARGIN_LEFT = Cm(2.2)
MARGIN_RIGHT = Cm(2.2)
MARGIN_TOP = Cm(2.0)
MARGIN_BOTTOM = Cm(2.0)


# ── 字体设置函数 ──────────────────────────────────────────

def set_run_font(
    run,
    size: float = 11.5,
    bold: bool = False,
    color: Optional[RGBColor] = None,
    cn_font: str = CN_BODY_FONT,
    en_font: str = EN_FONT,
) -> None:
    """同时设置中文字体（eastAsia）和英文字体（ascii/hAnsi）。"""
    run.font.name = en_font
    rpr = run._element.rPr
    rpr.rFonts.set(qn("w:eastAsia"), cn_font)
    rpr.rFonts.set(qn("w:ascii"), en_font)
    rpr.rFonts.set(qn("w:hAnsi"), en_font)
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = color


def set_paragraph_spacing(
    paragraph,
    after: float = 6,
    before: float = 0,
    line: float = 1.3,
) -> None:
    fmt = paragraph.paragraph_format
    fmt.space_after = Pt(after)
    fmt.space_before = Pt(before)
    fmt.line_spacing = line


def add_text(
    paragraph,
    text: str,
    size: float = 11.5,
    bold: bool = False,
    color: Optional[RGBColor] = None,
    cn_font: str = CN_BODY_FONT,
) -> None:
    """给段落追加一个 run，自动设置字体。"""
    run = paragraph.add_run(text)
    set_run_font(run, size=size, bold=bold, color=color, cn_font=cn_font)


# ── 手动构建函数（用于非 pandoc 场景）─────────────────────

def base_doc() -> Document:
    """A4 竖排页面，标准页边距，Normal 默认为 SimSun + TNR。"""
    doc = Document()
    section = doc.sections[0]
    section.page_width = PAGE_WIDTH
    section.page_height = PAGE_HEIGHT
    section.left_margin = MARGIN_LEFT
    section.right_margin = MARGIN_RIGHT
    section.top_margin = MARGIN_TOP
    section.bottom_margin = MARGIN_BOTTOM

    normal = doc.styles["Normal"]
    normal.font.name = EN_FONT
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), CN_BODY_FONT)
    normal._element.rPr.rFonts.set(qn("w:ascii"), EN_FONT)
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), EN_FONT)
    normal.font.size = Pt(11.5)
    return doc


def title_block(doc: Document, title: str, subtitle: Optional[str] = None) -> None:
    """居中标题块：大标题（SimHei 24pt）+ 副标题（灰色 11pt）。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, after=3, line=1.15)
    add_text(p, title, size=24, bold=True, color=TITLE_COLOR, cn_font=CN_HEAD_FONT)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p2, after=12, line=1.15)
    if subtitle:
        add_text(p2, subtitle, size=11, color=SUB_COLOR, cn_font=CN_BODY_FONT)
    else:
        add_text(p2, "", size=11)


def heading(doc: Document, text: str, level: int = 1) -> None:
    """标题段落（SimHei，level 1=15pt，level 2=12.5pt）。"""
    sz = 15 if level == 1 else 12.5
    before = 8 if level == 1 else 4
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=before, after=4, line=1.2)
    add_text(p, text, size=sz, bold=True, color=TITLE_COLOR, cn_font=CN_HEAD_FONT)
    return p


def para(doc: Document, text: str) -> None:
    """正文段落（SimSun 11.5pt）。"""
    p = doc.add_paragraph()
    set_paragraph_spacing(p, after=5)
    add_text(p, text, size=11.5, cn_font=CN_BODY_FONT)
    return p


def bullet(doc: Document, text: str, level: int = 0) -> None:
    """项目符号段落（SimSun 11.5pt）。"""
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(0.74 + 0.5 * level)
    p.paragraph_format.first_line_indent = Cm(-0.45)
    set_paragraph_spacing(p, after=3)
    add_text(p, text, size=11.5, cn_font=CN_BODY_FONT)
    return p


def simple_table(doc: Document, rows: list[list[str]],
                 widths: Optional[list] = None, font_size: float = 10.5) -> None:
    """简单表格：表头自动黑体加粗，正文自动宋体，内容居中。"""
    if not rows:
        return
    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    table.style = "Table Grid"
    table.autofit = False
    if widths is None:
        widths_cm = [Cm(3.2)] * len(rows[0])
    else:
        widths_cm = widths
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            cell.width = widths_cm[c]
            cell_p = cell.paragraphs[0]
            cell_p.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 内容居中
            set_paragraph_spacing(cell_p, after=0, line=1.15)
            add_text(cell_p, str(value), size=font_size,
                     bold=(r == 0), color=TITLE_COLOR if r == 0 else None,
                     cn_font=CN_HEAD_FONT if r == 0 else CN_BODY_FONT)
    doc.add_paragraph()


def picture_block(doc: Document, image_path: str, caption: str = "",
                  width_cm: float = 12.0) -> None:
    """图片 + 居中题注（仿宋五号）。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, after=2, before=2, line=1.0)
    run = p.add_run()
    run.add_picture(str(image_path), width=Cm(width_cm))

    if caption:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(cap, after=6, line=1.0)
        add_text(cap, caption, size=10.5, color=SUB_COLOR, cn_font=CN_CAPTION_FONT)


# ── OMML 公式字号辅助函数（v3 新增）────────────────────────

def _set_display_math_font_size(paragraph, size_pt: float = 14) -> bool:
    """将段落中 OMML 显示公式（m:oMathPara）的默认字号设为 size_pt。

    Pandoc 将 $$\\dots$$ 显示公式转换为 m:oMathPara 包装的 OMML 结构，
    默认继承段落正文的 11.5pt。本函数在 m:ctrlPr 中插入 w:sz/w:szCs，
    使公式以 size_pt（四号 = 14pt）渲染。

    返回 True 表示已处理，False 表示该段落无显示公式。
    """
    para_elem = paragraph._element
    oMathPara = para_elem.find(qn("m:oMathPara"))
    if oMathPara is None:
        # Also check inline math (m:oMath without oMathPara wrapper)
        # Only resize if formula text content > 5 chars
        oMath_list = para_elem.findall(qn("m:oMath"))
        handled = False
        for oMath in oMath_list:
            # Skip if this oMath is inside an oMathPara (already handled above)
            if oMath.getparent() is not None and oMath.getparent().tag == qn("m:oMathPara"):
                continue
            # Measure text content of the formula
            text_parts = []
            for t_elem in oMath.iter(qn("m:t")):
                if t_elem.text:
                    text_parts.append(t_elem.text)
            formula_text = "".join(text_parts)
            # Count non-whitespace characters
            char_count = sum(1 for c in formula_text if not c.isspace())
            if char_count > 5:
                _inject_ctrlpr_font_size(oMath, qn("m:oMathPr"), "m:oMathPr", size_pt)
                handled = True
        return handled

    _inject_ctrlpr_font_size(oMathPara, qn("m:oMathParaPr"), "m:oMathParaPr", size_pt)
    return True


def _inject_ctrlpr_font_size(
    parent_elem,
    pr_qn_tag: str,      # namespace-qualified tag for find()
    pr_prefix_tag: str,   # prefix:localname tag for OxmlElement()
    size_pt: float,
) -> None:
    """在 parent_elem（oMathPara 或 oMath）的 pr 子元素中插入字号设置。"""
    pr = parent_elem.find(pr_qn_tag)
    if pr is None:
        pr = OxmlElement(pr_prefix_tag)
        parent_elem.insert(0, pr)

    ctrlPr = pr.find(qn("m:ctrlPr"))
    if ctrlPr is None:
        ctrlPr = OxmlElement("m:ctrlPr")
        pr.append(ctrlPr)

    rPr = ctrlPr.find(qn("w:rPr"))
    if rPr is None:
        rPr = OxmlElement("w:rPr")
        ctrlPr.append(rPr)

    half_pts = str(int(size_pt * 2))
    sz = rPr.find(qn("w:sz"))
    if sz is None:
        sz = OxmlElement("w:sz")
        rPr.append(sz)
    sz.set(qn("w:val"), half_pts)

    szCs = rPr.find(qn("w:szCs"))
    if szCs is None:
        szCs = OxmlElement("w:szCs")
        rPr.append(szCs)
    szCs.set(qn("w:val"), half_pts)


# ── Pandoc 后处理函数（v2 新增）───────────────────────────

def postprocess_pandoc_docx(
    input_path: Path,
    output_path: Optional[Path] = None,
    body_font: str = CN_BODY_FONT,
    head_font: str = CN_HEAD_FONT,
) -> Document:
    """修正 pandoc 生成 docx 的字体和样式。

    参数
    ----------
    input_path : Path
        Pandoc 输出的 .docx 文件路径。
    output_path : Path or None
        修正后保存路径。为 None 时覆盖原文件。
    body_font : str
        中文正文字体（默认 SimSun）。
    head_font : str
        中文标题/表头字体（默认 SimHei）。

    返回
    -------
    docx.Document
    """
    doc = Document(str(input_path))

    # ── 全库样式字体清理：遍历所有样式，移除主题引用 ──
    for style in doc.styles:
        try:
            sid = style.style_id
        except AttributeError:
            continue
        # 先确保 rPr 存在（font.name 的 setter 会创建它）
        try:
            style.font.name = EN_FONT
        except Exception:
            continue

        rPr = style._element.rPr
        if rPr is None:
            continue
        rFonts = rPr.find(qn("w:rFonts"))
        if rFonts is None:
            continue

        # 判断类别：标题类用 head_font，正文类用 body_font
        is_heading = bool(
            re.match(r"^(heading|Heading|Heading\s*\d+)", sid)
            or sid in ("Title", "Subtitle", "TOCHeading")
        )
        cn = head_font if is_heading else body_font

        # 补 eastAsia（若缺失）
        if not rFonts.get(qn("w:eastAsia")):
            rFonts.set(qn("w:eastAsia"), cn)
        # 补 ascii/hAnsi（若缺失）
        if not rFonts.get(qn("w:ascii")):
            rFonts.set(qn("w:ascii"), EN_FONT)
        if not rFonts.get(qn("w:hAnsi")):
            rFonts.set(qn("w:hAnsi"), EN_FONT)

        # 移除全部主题引用 → 等线（DengXian）根源
        for _attr in (
            "w:eastAsiaTheme", "w:asciiTheme",
            "w:hAnsiTheme", "w:cstheme",
        ):
            key = qn(_attr)
            if key in rFonts.attrib:
                del rFonts.attrib[key]

    # ── 全库段落级 run 字体清理 ──
    for para in doc.paragraphs:
        # 判断段落属于标题还是正文
        pPr = para._element.find(qn("w:pPr"))
        if pPr is None:
            continue
        pStyle = pPr.find(qn("w:pStyle"))
        sv = pStyle.get(qn("w:val"), "") if pStyle is not None else ""
        is_heading = bool(
            sv.startswith("Heading") or sv in ("Title", "Subtitle", "TOCHeading")
        )
        cn = head_font if is_heading else body_font

        for run in para.runs:
            rPr = run._element.rPr
            if rPr is None:
                continue
            rFonts = rPr.find(qn("w:rFonts"))
            if rFonts is None:
                continue
            # 有主题引用才处理（避免不必要的改动）
            has_theme = any("Theme" in str(k) for k in rFonts.attrib)
            if not has_theme and rFonts.get(qn("w:eastAsia")):
                continue
            rFonts.set(qn("w:eastAsia"), cn)
            if not rFonts.get(qn("w:ascii")):
                rFonts.set(qn("w:ascii"), EN_FONT)
            if not rFonts.get(qn("w:hAnsi")):
                rFonts.set(qn("w:hAnsi"), EN_FONT)
            for _attr in (
                "w:eastAsiaTheme", "w:asciiTheme",
                "w:hAnsiTheme", "w:cstheme",
            ):
                key = qn(_attr)
                if key in rFonts.attrib:
                    del rFonts.attrib[key]

    # ── 表格字体 + 内容居中 ──
    for table in doc.tables:
        for i, row in enumerate(table.rows):
            cf = head_font if i == 0 else body_font
            for cell in row.cells:
                for para in cell.paragraphs:
                    # 表格内容居中
                    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in para.runs:
                        run.font.name = EN_FONT
                        rPr = run._element.rPr
                        if rPr is None:
                            continue
                        rFonts = rPr.find(qn("w:rFonts"))
                        if rFonts is None:
                            continue
                        rFonts.set(qn("w:eastAsia"), cf)
                        rFonts.set(qn("w:ascii"), EN_FONT)
                        rFonts.set(qn("w:hAnsi"), EN_FONT)
                        for _attr in (
                            "w:eastAsiaTheme", "w:asciiTheme",
                            "w:hAnsiTheme", "w:cstheme",
                        ):
                            key = qn(_attr)
                            if key in rFonts.attrib:
                                del rFonts.attrib[key]
                        if i == 0:
                            run.bold = True

    # ── 图例题注：识别以"图"/"表"开头的居中短段落 → 仿宋五号 ──
    #    Pandoc 将 ![*caption*](image.png) 输出为居中图片+居中斜体段落，
    #    这些斜体段落通常格式为：纯文本、居中、以"图 "或"表 "开头。
    for para in doc.paragraphs:
        text_content = para.text.strip()
        if not text_content:
            continue
        if text_content.startswith("图 ") or text_content.startswith("表 "):
            # 强制居中（不论 pandoc 原始对齐方式）
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                run.font.size = Pt(10.5)  # 五号
                run.font.bold = False
                run.font.italic = False  # 去斜体
                rPr = run._element.rPr
                if rPr is None:
                    continue
                rFonts = rPr.find(qn("w:rFonts"))
                if rFonts is None:
                    continue
                rFonts.set(qn("w:eastAsia"), CN_CAPTION_FONT)
                rFonts.set(qn("w:ascii"), EN_FONT)
                rFonts.set(qn("w:hAnsi"), EN_FONT)

    # ── OMML 公式字号：显示公式（$$...$$）→ 四号（14pt）──
    #    长行内公式（>5 非空字符）→ 同样 14pt
    for para in doc.paragraphs:
        _set_display_math_font_size(para, size_pt=14)

    # ── 页面设置 ──
    section = doc.sections[0]
    section.page_width = PAGE_WIDTH
    section.page_height = PAGE_HEIGHT
    section.left_margin = MARGIN_LEFT
    section.right_margin = MARGIN_RIGHT
    section.top_margin = MARGIN_TOP
    section.bottom_margin = MARGIN_BOTTOM

    # 保存
    save_path = output_path or input_path
    doc.save(str(save_path))
    return doc
