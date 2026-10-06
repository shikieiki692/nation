# -*- coding: utf-8 -*-
"""通用 docx → PDF → PNG 渲染（只读，产物落 .workbuddy/tmp/opt_pipe/render_out/）。

用法：python render_any.py <docx路径> <输出子目录名> [起始页] [页数]
"""
import glob
import os
import subprocess
import sys
from pathlib import Path

SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
ROOT = Path(r"C:\Obsidion\妙妙屋")
OUTBASE = ROOT / ".workbuddy" / "tmp" / "opt_pipe" / "render_out"


def main():
    src = sys.argv[1]
    tag = sys.argv[2]
    p0 = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    cnt = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    out = OUTBASE / tag
    out.mkdir(parents=True, exist_ok=True)
    # 清旧
    for f in glob.glob(str(out / "*")):
        os.remove(f)
    subprocess.run([SOFFICE, "--headless", "--convert-to", "pdf",
                    "--outdir", str(out), src], capture_output=True, timeout=420)
    pdfs = glob.glob(str(out / "*.pdf"))
    if not pdfs:
        print("PDF 生成失败"); return 1
    sys.path.insert(0, r"C:\Users\蕾赛\.workbuddy\binaries\python\envs\default\Lib\site-packages")
    import pymupdf as fitz
    d = fitz.open(pdfs[0])
    print("PDF 页数:", d.page_count)
    for i in range(p0 - 1, min(p0 - 1 + cnt, d.page_count)):
        p = d[i].get_pixmap(dpi=110)
        p.save(str(out / ("p%02d.png" % (i + 1))))
    print("→", out, "共", min(cnt, d.page_count - p0 + 1), "页")
    d.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
