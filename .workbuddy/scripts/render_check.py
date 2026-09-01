# -*- coding: utf-8 -*-
"""渲染校验：docx -> PDF(Word COM) -> PNG(PyMuPDF)，用于目视检查排版"""
import sys, io, os
from pathlib import Path
import win32com.client as wc
import fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def docx2pdf(docx_path: Path, pdf_path: Path):
    word = wc.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        doc = word.Documents.Open(str(docx_path), ReadOnly=True)
        doc.SaveAs(str(pdf_path), FileFormat=17)  # wdFormatPDF
        doc.Close(False)
    finally:
        word.Quit()


def pdf2png(pdf_path: Path, out_dir: Path, pages=(1, 2, 3), dpi=110, prefix='p'):
    d = fitz.open(str(pdf_path))
    out = []
    for i in pages:
        if i > len(d):
            continue
        pg = d[i - 1]
        pix = pg.get_pixmap(dpi=dpi)
        fp = out_dir / f"{prefix}{i}.png"
        pix.save(str(fp))
        out.append(fp)
    d.close()
    return out, len(d)


def main():
    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = sys.argv[3] if len(sys.argv) > 3 else 'p'
    npages_want = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    pdf = out_dir / "_render.pdf"
    docx2pdf(src, pdf)
    pages = tuple(range(1, npages_want + 1))
    imgs, total = pdf2png(pdf, out_dir, pages=pages, prefix=prefix)
    print(f"[OK] {src.name}: 共 {total} 页 -> {[i.name for i in imgs]}")


if __name__ == '__main__':
    main()
