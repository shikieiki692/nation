# -*- coding: utf-8 -*-
"""把课程计划 md 转成与原样板同版式的 docx。

原样板版式（已逐项提取自 C:\\Users\\蕾赛\\Downloads\\初三未央化学竞赛课程计划..docx）：
  - 页面  A4(11906x16838)，页边距 上下 1440 / 左右 1800，docGrid lines linePitch 312
  - 字体  西文 Times New Roman，中文 宋体
  - 字号  标题 14pt（居中），章节标题与表格正文 一律 10pt，全程不加粗
  - 段落  段后 0，行距 240(auto=单倍)
  - 表格  框线 single sz=4；单元格垂直居中、文本水平居中
  - 表1   3 列 1560/1275/2835，含表头行
  - 模块表 4 列，无表头行，第 1、4 列按「章」纵向合并
"""
from pathlib import Path
import re

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Twips

SRC = Path(r"C:\Obsidion\妙妙屋\备课思路\未央化学竞赛课程计划（初二至高二）.md")
OUT = Path(r"C:\Obsidion\妙妙屋\备课思路\未央化学竞赛课程计划（初二至高二）.docx")

SEP = "｜"
EAST, WEST = "宋体", "Times New Roman"

W_SUMMARY = [1560, 1275, 2835]              # 表1（照样板）
W_MODULE = [1450, 1750, 2550, 2641]         # 模块表（章列 737 -> 1450，总宽仍 8391）
MODULE_HEADER = ["章", "节", "知识点", "教材来源"]


# ---------------- 底层工具 ----------------

def set_run(run, hp):
    run.font.size = Pt(hp / 2)
    rPr = run._element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rPr.insert(0, rf)
    rf.set(qn("w:ascii"), WEST)
    rf.set(qn("w:hAnsi"), WEST)
    rf.set(qn("w:cs"), WEST)
    rf.set(qn("w:eastAsia"), EAST)
    for tag in ("w:sz", "w:szCs"):
        e = rPr.find(qn(tag))
        if e is None:
            e = OxmlElement(tag)
            rPr.append(e)
        e.set(qn("w:val"), str(hp))


def style_para(p, align=None, hp=20):
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    if align is not None:
        p.alignment = align
    for r in p.runs:
        set_run(r, hp)
    return p


def add_block(doc, text, align=None, hp=20):
    p = doc.add_paragraph()
    p.add_run(text)
    return style_para(p, align, hp)


def set_cell(cell, items, hp=20):
    """把 items 逐条写成单元格内的多个段落。"""
    if not items:
        return
    first = True
    for it in items:
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.add_run(it)
        style_para(p, WD_ALIGN_PARAGRAPH.CENTER, hp)


def table_borders(tbl):
    tblPr = tbl._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    for tag in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + tag)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), "auto")
        b.append(e)
    tblPr.append(b)


def set_grid(tbl, widths):
    tblPr = tbl._tbl.tblPr
    for old in tblPr.findall(qn("w:tblW")):
        tblPr.remove(old)
    w = OxmlElement("w:tblW")
    w.set(qn("w:w"), str(sum(widths)))
    w.set(qn("w:type"), "dxa")
    tblPr.append(w)

    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)

    old = tbl._tbl.find(qn("w:tblGrid"))
    if old is not None:
        tbl._tbl.remove(old)
    grid = OxmlElement("w:tblGrid")
    for ww in widths:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(ww))
        grid.append(gc)
    tblPr.addnext(grid)

    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False


def set_vmerge(cell, val=None):
    tcPr = cell._tc.get_or_add_tcPr()
    vm = tcPr.find(qn("w:vMerge"))
    if vm is None:
        vm = OxmlElement("w:vMerge")
        ref = tcPr.find(qn("w:tcW"))
        if ref is None:
            ref = tcPr.find(qn("w:gridSpan"))
        if ref is not None:
            ref.addnext(vm)
        else:
            tcPr.insert(0, vm)
    if val is not None:
        vm.set(qn("w:val"), val)


def layout_cells(tbl, widths):
    n = len(widths)
    for row in tbl.rows:
        for ci, cell in enumerate(row.cells):
            if ci >= n:
                continue
            cell.width = Twips(widths[ci])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                style_para(p, WD_ALIGN_PARAGRAPH.CENTER, 20)
                if not p.runs:
                    r = p.add_run("")
                    set_run(r, 20)


# ---------------- 解析 md ----------------

lines = SRC.read_text(encoding="utf-8").split("\n")
title = None
blocks = []          # [(kind, name, rows)]  kind: 'table'
i = 0
cur_mod = None
while i < len(lines):
    s = lines[i].strip()
    if s.startswith("# ") and not s.startswith("## "):
        title = s[2:].strip()
        i += 1
        continue
    if s.startswith("## "):
        blocks.append(("h2", s[3:].strip(), None))
        cur_mod = None
        i += 1
        continue
    if s.startswith("### "):
        cur_mod = s[4:].strip()
        blocks.append(("h3", cur_mod, None))
        i += 1
        continue
    if s.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            raw = lines[i].strip()
            cells = [c.strip() for c in raw.strip("|").split("|")]
            rows.append(cells)
            i += 1
        # 去掉分隔行
        rows = [r for r in rows if not (set("".join(r)) <= set(":- ") and r)]
        blocks.append(("table", cur_mod, rows))
        continue
    i += 1

assert title, "未找到 H1 标题"

# ---------------- 生成 docx ----------------

doc = Document()
sec = doc.sections[0]
sec.page_width = Twips(11906)
sec.page_height = Twips(16838)
sec.top_margin = Twips(1440)
sec.bottom_margin = Twips(1440)
sec.left_margin = Twips(1800)
sec.right_margin = Twips(1800)

# Normal 样式兜底（宋体 + Times New Roman / 10pt / 段后0 / 单倍行距）
normal = doc.styles["Normal"]
normal.font.size = Pt(10)
normal.font.name = WEST
rpr = normal.element.get_or_add_rPr()
rf = rpr.find(qn("w:rFonts"))
if rf is None:
    rf = OxmlElement("w:rFonts")
    rpr.insert(0, rf)
rf.set(qn("w:ascii"), WEST)
rf.set(qn("w:hAnsi"), WEST)
rf.set(qn("w:cs"), WEST)
rf.set(qn("w:eastAsia"), EAST)
normal.paragraph_format.space_after = Pt(0)
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.line_spacing = 1.0

sect_pr = sec._sectPr
dg = sect_pr.find(qn("w:docGrid"))
if dg is None:
    dg = OxmlElement("w:docGrid")
    sect_pr.append(dg)
dg.set(qn("w:type"), "lines")
dg.set(qn("w:linePitch"), "312")

# 标题
add_block(doc, title, WD_ALIGN_PARAGRAPH.CENTER, hp=28)

n_summary = 0
n_module_tables = 0
n_merge_start = 0
stats = []

for kind, name, rows in blocks:
    if kind == "h2":
        add_block(doc, name, None, hp=20)
        continue
    if kind == "h3":
        add_block(doc, name, None, hp=20)
        continue

    # ---- 表格 ----
    hdr = rows[0] if rows else []
    is_module = len(hdr) == 4 and hdr[:4] == MODULE_HEADER
    if len(hdr) == 3:
        # 表1 式：3 列，保留表头行
        widths = W_SUMMARY
        kind = "summary"
        body = rows
    elif len(hdr) == 4:
        # 模块式：4 列，丢弃 md 表头行（与原样板一致：docx 内不出现表头）
        widths = W_MODULE
        kind = "module"
        body = rows[1:]
        n_module_tables += 1
    else:
        raise SystemExit("未识别的表格列数: %r" % (hdr,))

    ncol = len(widths)
    tbl = doc.add_table(rows=len(body), cols=ncol)
    set_grid(tbl, widths)
    table_borders(tbl)

    # 补全「章」与「教材来源」的纵向继承
    cur_cha = ""
    cur_src = ""
    filled = []
    for r in body:
        c0 = r[0] if len(r) > 0 else ""
        c1 = r[1] if len(r) > 1 else ""
        c2 = r[2] if len(r) > 2 else ""
        c3 = r[3] if len(r) > 3 else ""
        if c0.strip():
            cur_cha = c0.strip()
            cur_src = c3.strip()
            new_group = True
        else:
            new_group = False
        filled.append({"cha": cur_cha, "jie": c1.strip(),
                       "kp": [x for x in c2.split(SEP) if x.strip()],
                       "src": [x for x in cur_src.split(SEP) if x.strip()],
                       "start": new_group})

    # 写入单元格
    for ri, f in enumerate(filled):
        if kind == "summary":
            # 表1：三列原样
            set_cell(tbl.cell(ri, 0), [f["cha"]])
            set_cell(tbl.cell(ri, 1), [f["jie"]])
            set_cell(tbl.cell(ri, 2), f["kp"])
        else:
            # 模块式 4 列：首列与末列按「章」纵向继承
            if f["start"]:
                set_cell(tbl.cell(ri, 0), [f["cha"]])
            set_cell(tbl.cell(ri, 1), [f["jie"]] if f["jie"] else [])
            set_cell(tbl.cell(ri, 2), f["kp"])
            if f["start"]:
                set_cell(tbl.cell(ri, 3), f["src"])

    # 纵向合并（仅真模块表：同「章」的行）
    if is_module:
        gs = [i for i, f in enumerate(filled) if f["start"]] + [len(filled)]
        for a, b in zip(gs, gs[1:]):
            if b - a > 1:
                set_vmerge(tbl.cell(a, 0), "restart")
                set_vmerge(tbl.cell(a, 3), "restart")
                for k in range(a + 1, b):
                    set_vmerge(tbl.cell(k, 0), None)
                    set_vmerge(tbl.cell(k, 3), None)
                n_merge_start += 2

    layout_cells(tbl, widths)
    stats.append((name, len(body), ncol, kind))

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(str(OUT))

print("[ok]", OUT)
print("[size]", OUT.stat().st_size, "bytes")
for s in stats:
    print("   表 %-16s 行=%-4d 列=%d [%s]" % s)
print("模块表数:", n_module_tables, " 纵向合并起点:", n_merge_start)
