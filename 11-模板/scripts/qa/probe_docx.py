import sys, zipfile, re
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
path = sys.argv[1]
keys = sys.argv[2:]

z = zipfile.ZipFile(path)
xml = z.read("word/document.xml")
root = ET.fromstring(xml)
body = root.find(W + "body")

def para_text(p):
    return "".join(t.text or "" for t in p.iter(W + "t"))

def para_kind(p):
    ppr = p.find(W + "pPr")
    sty = ""
    if ppr is not None:
        s = ppr.find(W + "pStyle")
        if s is not None:
            sty = s.get(W + "val") or ""
    n_tbl = len(p.findall(W + "tbl"))
    return sty

blocks = []  # (kind, text)
for child in body:
    tag = child.tag.replace(W, "")
    if tag == "p":
        blocks.append(("P[" + para_kind(child) + "]", para_text(child)))
    elif tag == "tbl":
        rows = []
        for tr in child.findall(W + "tr"):
            cells = []
            for tc in tr.findall(W + "tc"):
                cells.append(" ".join(para_text(p) for p in tc.findall(W + "p")))
            rows.append(" | ".join(cells))
        blocks.append(("TBL", " || ".join(rows)))

for i, (k, t) in enumerate(blocks):
    if any(kk in t for kk in keys):
        lo = max(0, i - 3)
        hi = min(len(blocks), i + 6)
        print("=" * 70)
        print("HIT@%d  keys=%s" % (i, [kk for kk in keys if kk in t]))
        for j in range(lo, hi):
            mark = ">>" if j == i else "  "
            print("%s [%d] %-22s %s" % (mark, j, blocks[j][0], blocks[j][1][:300]))
