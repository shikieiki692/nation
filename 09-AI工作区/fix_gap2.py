from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import shutil

F = r"C:/Users/蕾赛/Desktop/第一轮-4.5小时综合测试（A卷+B卷）.docx"
shutil.copy(F, F.replace('.docx', '（二次修间距前）.docx'))

d = Document(F)
ps = d.paragraphs
body = d.element.body

def remove_sectPr(p):
    pPr = p._p.find(qn('w:pPr'))
    if pPr is not None:
        sect = pPr.find(qn('w:sectPr'))
        if sect is not None:
            pPr.remove(sect)

# Collapse the isolated header sections into the question sections.
# - Remove PARA 1 (A卷) sectPr -> A卷 joins A卷 questions in one section (Sec B, defined by PARA 111).
# - Remove PARA 112 (B卷) sectPr -> B卷 joins B卷 questions in one section (Sec D, defined by body sectPr).
# - Keep PARA 111's nextPage 2-col sectPr (B卷 starts a NEW PAGE).
remove_sectPr(ps[1])
remove_sectPr(ps[112])

# Ensure the two remaining section defs are 2-col with proper footer wiring.
def ensure_cols_2(sectPr, footer_rid):
    cols = sectPr.find(qn('w:cols'))
    if cols is None:
        cols = OxmlElement('w:cols'); sectPr.append(cols)
    cols.set(qn('w:num'), '2')
    cols.set(qn('w:space'), '681')
    # make sure a default footer reference exists
    if sectPr.find(qn('w:footerReference')) is None and footer_rid:
        fr = OxmlElement('w:footerReference')
        fr.set(qn('w:type'), 'default')
        fr.set(qn('r:id'), footer_rid)
        sectPr.append(fr)

# PARA 111 sectPr = Sec B (A卷)
s111 = ps[111]._p.get_or_add_pPr().find(qn('w:sectPr'))
ensure_cols_2(s111, 'rId38')
# body sectPr = Sec D (B卷)
bsect = body.find(qn('w:sectPr'))
ensure_cols_2(bsect, 'rId40')

# Tighten the spacing just under the volume headers (optional polish)
def set_spacing(p, before=None, after=None):
    pPr = p._p.get_or_add_pPr()
    spc = pPr.find(qn('w:spacing'))
    if spc is None:
        spc = OxmlElement('w:spacing'); pPr.append(spc)
    if before is not None: spc.set(qn('w:before'), str(before))
    if after is not None: spc.set(qn('w:after'), str(after))

set_spacing(ps[1], after=80)      # A卷 -> 一、
set_spacing(ps[2], before=120)    # 一、 -> 紧跟
set_spacing(ps[112], after=80)    # B卷 -> 一、
set_spacing(ps[113], before=120)

d.save(F)
print("done: header sections merged into question sections; only B卷 nextPage remains")
