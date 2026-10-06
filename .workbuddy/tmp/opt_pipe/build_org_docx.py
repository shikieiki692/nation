# -*- coding: utf-8 -*-
"""初赛模拟卷 X 的 md → docx（机构题源：图片散在 13 个机构 images/）。

与 build_simvol_docx.py 的差异：媒体解析不用单一「媒体仓库」，而是
① 先建暂存媒体目录，把本卷引用的机构图复制进去；② 再 fallback 媒体仓库。
"""
import os, re, sys, shutil, glob
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
QB = VAULT / "04-题库"
MEDIA = VAULT / "媒体仓库"
ORGBASE = QB / "2026机构初赛模拟题"
SCRIPTS = VAULT / "11-模板" / "scripts"
REF_DOC = SCRIPTS / "templates" / "custom-reference.docx"
OUT_DIR = VAULT / "00-首页" / "题组Word" / "初赛模拟卷"
WORK = VAULT / ".workbuddy" / "tmp" / "org_docx_build"
STAGE = WORK / "media"
for d in (OUT_DIR, WORK, STAGE):
    d.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SCRIPTS))
import pypandoc
from docx_utils import postprocess_pandoc_docx

PANDOC_FROM = ("markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+raw_tex"
               "-superscript-subscript")
FILES = [("初赛模拟卷X（非有机·答案版）.md", "初赛模拟卷X（非有机·答案版）.docx"),
         ("初赛模拟卷X（非有机·学生版）.md", "初赛模拟卷X（非有机·学生版）.docx")]

# 机构图索引（hash -> 路径）
IMG_IDX = {}
for p in glob.glob(str(ORGBASE / "*" / "images" / "*")):
    IMG_IDX.setdefault(os.path.basename(p), p)


def strip_fm(t):
    if not t.startswith("---"):
        return t
    e = t.find("\n---", 3)
    return t[e + 4:].lstrip("\n") if e >= 0 else t


# ── 本系列图片尺寸上限（比 docx_utils 全库默认更紧；**高度也封顶**）──────
# 全库默认：横 10cm 宽 / 纵 7cm 宽（高度不限）/ 方 9cm —— 机构题图多且多为
# 竖长截图 ⇒ 竖图能到 10cm+ 高，一页塞不下几张。本系列改为宽高**双封顶**。
CAP = {           # (最大宽 cm, 最大高 cm)
    "land": (7.6, 5.8),    # 横图 aspect > 1.3
    "port": (5.2, 7.0),    # 竖图 aspect < 0.7
    "sq":   (6.0, 6.0),    # 方形
}
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
CM = 360000


def clamp_series_images(path):
    """把 docx 内所有插图按本系列上限**等比缩小**（绝不放大）。

    表格内插图已由 docx_utils `_clamp_table_images` 收到列宽；本函数只做
    「宽高双封顶」的进一步收紧，故不会与列宽钳制冲突。
    """
    from docx import Document
    doc = Document(str(path))
    n = 0
    for drawing in doc.element.body.iter("{%s}drawing" % W_NS):
        inline = drawing.find("{%s}inline" % WP_NS)
        if inline is None:
            continue
        ext = inline.find("{%s}extent" % WP_NS)
        if ext is None:
            continue
        try:
            cx, cy = int(ext.get("cx") or 0), int(ext.get("cy") or 0)
        except ValueError:
            continue
        if cx <= 0 or cy <= 0:
            continue
        asp = cx / cy
        key = "land" if asp > 1.3 else ("port" if asp < 0.7 else "sq")
        mw, mh = CAP[key]
        MW, MH = int(mw * CM), int(mh * CM)
        scale = min(1.0, MW / cx, MH / cy)
        if scale >= 0.999:
            continue
        ncx, ncy = int(cx * scale), int(cy * scale)
        ext.set("cx", str(ncx)); ext.set("cy", str(ncy))
        for aext in drawing.iter("{%s}ext" % A_NS):
            try:
                acx, acy = int(aext.get("cx", "0")), int(aext.get("cy", "0"))
            except (ValueError, TypeError):
                continue
            if acx > 0 and acy > 0 and abs(acx / acy - cx / cy) < 0.1:
                aext.set("cx", str(ncx)); aext.set("cy", str(ncy))
                break
        n += 1
    if n:
        doc.save(str(path))
    return n


def callout_to_quote(b):
    return re.sub(r"^(>+\s*)\[!\w+\][-+]?\s*(.*)$", lambda m: (m.group(1) + m.group(2).strip()).rstrip(), b, flags=re.M)


def resolve_images(body, log):
    def rep(m):
        name = m.group(1).strip()
        src = IMG_IDX.get(name) or (str(MEDIA / name) if (MEDIA / name).exists() else None)
        if not src:
            log.append("   [缺图] " + name)
            return ""
        shutil.copyfile(src, STAGE / name)
        return f"![]({name})"
    return re.sub(r"!\[\[([^\]\|\\]+?)(?:\\?\|\d+)?\]\]", rep, body)


def dewikilink(b):
    b = re.sub(r"\[\[[^\]\|]*\|([^\]]*)\]\]", r"\1", b)
    b = re.sub(r"\[\[([^\]]*)\]\]", r"\1", b)
    return b


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for md_name, docx_name in FILES:
        log = []
        src = QB / md_name
        body = strip_fm(src.read_text(encoding="utf-8"))
        body = callout_to_quote(body)
        n_before = len(re.findall(r"!\[\[", body))
        body = resolve_images(body, log)
        body = dewikilink(body)
        tmp_md = WORK / (Path(md_name).stem + ".md")
        tmp_md.write_text(body, encoding="utf-8")
        tmp_docx = WORK / docx_name
        pypandoc.convert_file(str(tmp_md), "docx", outputfile=str(tmp_docx),
                              extra_args=[f"--from={PANDOC_FROM}", "--to=docx",
                                          f"--resource-path={STAGE}", f"--reference-doc={REF_DOC}"])
        postprocess_pandoc_docx(tmp_docx, tmp_docx)
        nclamp = clamp_series_images(tmp_docx)
        out = OUT_DIR / docx_name
        try:
            shutil.copyfile(tmp_docx, out)
            print(f"OK {docx_name}  {out.stat().st_size/1024:.0f} KB  源图 {n_before}  尺寸收紧 {nclamp}")
        except PermissionError:
            alt = WORK / ("NEW_" + docx_name)
            shutil.copyfile(tmp_docx, alt)
            print(f"🔒 被占用，已存暂存：{alt}  （{tmp_docx.stat().st_size/1024:.0f} KB 源图 {n_before}）")
        for l in log:
            print(l)
    return 0


if __name__ == "__main__":
    sys.exit(main())
