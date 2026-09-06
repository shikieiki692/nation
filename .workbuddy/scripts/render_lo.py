# -*- coding: utf-8 -*-
"""用 LibreOffice 批量 docx -> PDF，再用 PyMuPDF 取前几页 PNG（Word COM 在本机不可用）"""
import sys, io, subprocess, argparse
from pathlib import Path
import fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"


def lo_convert(files, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = [SOFFICE, '--headless', '--norestore', '--convert-to', 'pdf',
           '--outdir', str(outdir)] + [str(f) for f in files]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=3600)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src', help='目录或单个 docx')
    ap.add_argument('outdir')
    ap.add_argument('--png-prefix', default='')
    ap.add_argument('--png-pages', type=int, default=0, help='>0 时导出前 N 页 PNG')
    ap.add_argument('--dpi', type=int, default=100)
    args = ap.parse_args()

    src = Path(args.src)
    files = [src] if src.is_file() else sorted(src.rglob('*.docx'))
    outdir = Path(args.outdir)
    print(f"转换 {len(files)} 个文件 -> {outdir}")
    r = lo_convert(files, outdir)
    if r.returncode != 0:
        print("LO stderr:", (r.stderr or '')[:800])

    pdfs = sorted(outdir.rglob('*.pdf'))
    print(f"产出 PDF {len(pdfs)} 个")

    total_pages = 0
    rows = []
    for pdf in pdfs:
        try:
            d = fitz.open(str(pdf))
            n = len(d)
            total_pages += n
            rows.append((pdf.stem, n))
            if args.png_pages > 0 and args.png_prefix:
                for i in range(1, min(args.png_pages, n) + 1):
                    pix = d[i - 1].get_pixmap(dpi=args.dpi)
                    pix.save(str(outdir / f"{args.png_prefix}{i}.png"))
            d.close()
        except Exception as e:
            rows.append((pdf.stem, f'ERR {e}'))
    print(f"\n总页数 {total_pages}")
    for name, n in rows:
        print(f"  {name:<40} {n}")


if __name__ == '__main__':
    main()
