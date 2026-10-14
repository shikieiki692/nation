# -*- coding: utf-8 -*-
r"""render_vol_docx.py —— 规范化「docx → PDF → 逐页 PNG」渲染脚本（替代每轮现写的一次性脚本）。

护栏（2026-10-14 卷 XVI 教训）：
  ① 渲染前**清空**输出目录中同名旧产物（防旧 PDF/PNG 冒充）；
  ② 转换后**断言 PDF mtime > docx mtime**（LibreOffice 静默失败时不会拿旧产物继续）；
  ③ 断言页数 > 0。

用法：
  python render_vol_docx.py --docx "<docx路径>" [--outdir <目录>] [--prefix stu] [--dpi 150]
  python render_vol_docx.py --vol XVI --kind stu          # 按卷名+版本在真题版式目录定位
"""
import argparse
import glob
import os
import subprocess
import sys
import time

import pymupdf as fitz

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
D = os.path.join(ROOT, "00-首页", "题组Word", "初赛模拟卷", "真题版式")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
DEFAULT_OUT = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe")


def render(docx, outdir, prefix, dpi):
    docx = os.path.abspath(docx)
    if not os.path.isfile(docx):
        print("⛔ docx 不存在:", docx); return 1
    os.makedirs(outdir, exist_ok=True)
    name = os.path.basename(docx)
    want_pdf = os.path.join(outdir, name.replace(".docx", ".pdf"))
    # ① 清旧
    for f in glob.glob(os.path.join(outdir, prefix + "_p*.png")) + [want_pdf]:
        if os.path.exists(f):
            os.remove(f)
    subprocess.run([SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", outdir, docx],
                   capture_output=True, timeout=600)
    if not os.path.exists(want_pdf):
        print("⛔ PDF 转换失败:", name); return 1
    # ② mtime 断言
    d_m, p_m = os.path.getmtime(docx), os.path.getmtime(want_pdf)
    if p_m <= d_m:
        print("⛔ PDF mtime(%s) 早于 docx(%s) —— 疑似旧产物" % (
            time.strftime("%H:%M:%S", time.localtime(p_m)),
            time.strftime("%H:%M:%S", time.localtime(d_m))))
        return 1
    # ③ 渲染
    doc = fitz.open(want_pdf)
    if doc.page_count <= 0:
        print("⛔ 页数 0"); return 1
    for i, page in enumerate(doc):
        page.get_pixmap(dpi=dpi).save(os.path.join(outdir, "%s_p%02d.png" % (prefix, i + 1)))
    n = doc.page_count
    doc.close()
    print("OK %s → %d 页 → %s_p*.png (dpi=%d)" % (name[:40], n, prefix, dpi))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx")
    ap.add_argument("--vol", help="卷号，如 XVI；与 --kind 二选一搭配")
    ap.add_argument("--kind", choices=["学生版", "答案与解析版", "答题卡"])
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--prefix", default="vol")
    ap.add_argument("--dpi", type=int, default=150)
    a = ap.parse_args()
    if a.docx:
        docx = a.docx
    elif a.vol and a.kind:
        # ★ 罗马卷号互为前缀（XV⊂XVII）⇒ 必须带「（」分隔符匹配
        hits = glob.glob(os.path.join(D, "*%s（*%s*.docx" % (a.vol, a.kind)))
        if not hits:
            print("⛔ 未找到 docx:", a.vol, a.kind); return 1
        docx = hits[0]
    else:
        print("用法：--docx <path> 或 --vol <V> --kind <版>"); return 1
    outdir = a.outdir or os.path.join(DEFAULT_OUT, "render_" + (a.vol or os.path.basename(docx)[:6]))
    return render(docx, outdir, a.prefix, a.dpi)


if __name__ == "__main__":
    sys.exit(main())
