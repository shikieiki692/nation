from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

F = r"C:/Users/蕾赛/Desktop/第一轮-4.5小时综合测试（A卷+B卷）.docx"

# safety copy
import shutil
shutil.copy(F, F.replace('.docx', '（修间距前）.docx'))

d = Document(F)
ps = d.paragraphs

def set_section_cols_2(sectPr):
    cols = sectPr.find(qn('w:cols'))
    if cols is None:
        cols = OxmlElement('w:cols'); sectPr.append(cols)
    cols.set(qn('w:num'), '2')
    cols.set(qn('w:space'), '681')  # ~12mm column gap

def add_span2(p):
    """Make paragraph span all columns; insert w:cols before w:sectPr to respect schema order."""
    pPr = p._p.get_or_add_pPr()
    sectPr = pPr.find(qn('w:sectPr'))
    cols = pPr.find(qn('w:cols'))
    if cols is None:
        cols = OxmlElement('w:cols')
        if sectPr is not None:
            sectPr.addprevious(cols)
        else:
            pPr.append(cols)
    cols.set(qn('w:span'), '2')

def set_spacing(p, before=None, after=None):
    pPr = p._p.get_or_add_pPr()
    spc = pPr.find(qn('w:spacing'))
    if spc is None:
        spc = OxmlElement('w:spacing'); pPr.append(spc)
    if before is not None: spc.set(qn('w:before'), str(before))
    if after is not None: spc.set(qn('w:after'), str(after))

title = ps[0]      # 大标题（满宽）
avol  = ps[1]      # A卷 卷头（满宽，且是 S0 的 sectPr 所在段落）
bvol  = ps[112]    # B卷 卷头（满宽，且是 S2 的 sectPr 所在段落）

# 1) 把承载 sectPr 的卷头段落所在“节”改为双栏（消除 单栏→双栏 的连续分节断点间隙）
a_sect = avol._p.get_or_add_pPr().find(qn('w:sectPr'))
b_sect = bvol._p.get_or_add_pPr().find(qn('w:sectPr'))
set_section_cols_2(a_sect)
set_section_cols_2(b_sect)

# 2) 标题 / A卷 / B卷 跨双栏满宽显示
add_span2(title)
add_span2(avol)
add_span2(bvol)

# 3) 顺手把卷头与首道大题标题之间的间距收一下（原来 160+280≈7.8mm，略紧一点）
set_spacing(avol, after=120)     # A卷 下方
set_spacing(bvol, after=120)     # B卷 下方
# 紧跟卷头的第一道大题标题（PARA 2 / PARA 113）前距从 280 降到 160
set_spacing(ps[2], before=160)
set_spacing(ps[113], before=160)

d.save(F)
print("done: header sections now 2-col with full-width spans; spacing tightened")
