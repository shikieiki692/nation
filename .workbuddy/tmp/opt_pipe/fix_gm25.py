#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_gm25.py —— 从「gamma晶体结构习题.pdf」（题目+答案交错）按题裁图，
回填 题-GM-25-* 等「源确缺答案」卡的答案区。"""
import glob, hashlib, io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
import fitz
from PIL import Image
try:
    fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
except Exception:
    pass
R = r"C:\Obsidion\妙妙屋"
PDF = os.path.join(R, "06-外部资料导入/OCR/01-题目/2026伽马寒假线上班/无机/2026年1.18无机/gamma晶体结构习题.pdf")
IMGDIR = os.path.join(R, "04-题库/2026机构初赛模拟题/伽马/images")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/gm25_backup")
os.makedirs(BK, exist_ok=True); os.makedirs(IMGDIR, exist_ok=True)
apply = "--apply" in sys.argv

doc = fitz.open(PDF)
# 1) 用文字层定位每题起点 (page_idx, y) —— 逐行匹配（search_for 对「第 1 题」空格字形无效）
marks = {}
for i in range(doc.page_count):
    for blk in doc[i].get_text("dict").get("blocks", []):
        for ln in blk.get("lines", []):
            txt = "".join(s.get("text", "") for s in ln.get("spans", [])).replace(" ", "")
            m = re.match(r"第(\d+)题", txt)
            if m:
                n = int(m.group(1))
                if n not in marks:
                    marks[n] = (i, float(ln["bbox"][1]))
print("定位到题号：", sorted(marks.items()))

# 2) 逐题裁图
def crop(n):
    """题 N 的答案位于「第 N+1 题标题所在页」的页首 → 该标题之前。
    末题则取其所在页的标题之后 → 页末。"""
    order = sorted(marks)
    if n not in marks:
        return []
    nxt = [k for k in order if k > n]
    out = []
    if nxt:
        p1, y1 = marks[nxt[0]]
        if y1 < 80:
            return []
        pg = doc[p1]; Rc = pg.rect
        pix = pg.get_pixmap(dpi=190, clip=fitz.Rect(Rc.x0 + 14, 0, Rc.x1 - 14, y1 - 6))
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=90, optimize=True, subsampling=0)
        data = buf.getvalue(); h = hashlib.sha256(data).hexdigest()
        fp = os.path.join(IMGDIR, h + ".jpg")
        if not os.path.exists(fp):
            open(fp, "wb").write(data)
        out.append((h + ".jpg", p1 + 1, im.width, im.height))
    else:
        p0, y0 = marks[n]
        for p in range(p0, doc.page_count):
            pg = doc[p]; Rc = pg.rect
            top = max(0.0, y0 - 6) if p == p0 else 0.0
            if Rc.y1 - top < 50:
                continue
            pix = pg.get_pixmap(dpi=190, clip=fitz.Rect(Rc.x0 + 14, top, Rc.x1 - 14, Rc.y1))
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            buf = io.BytesIO(); im.save(buf, "JPEG", quality=90, optimize=True, subsampling=0)
            data = buf.getvalue(); h = hashlib.sha256(data).hexdigest()
            fp = os.path.join(IMGDIR, h + ".jpg")
            if not os.path.exists(fp):
                open(fp, "wb").write(data)
            out.append((h + ".jpg", p + 1, im.width, im.height))
    return out

# 3) 处理 10 张卡：卡题号 = 源 PDF 的「第N题」n（卡 qno 为 01..06 → 需按 source 的「第 N 题」）
cards = []
for f in sorted(glob.glob(R + "/04-题库/2026机构初赛模拟题/伽马/题-GM-25-*.md")):
    t = open(f, encoding="utf-8-sig", errors="replace").read()
    src = (re.search(r'^source:\s*["\']?(.*?)["\']?\s*$', t, re.M) or [None, ""])[1]
    m = re.search(r"第\s*(\d+)\s*题", src)
    if m and os.path.basename(PDF)[:-4][:6] in src or ("晶体结构习题" in src or "题源" in src):
        pass
    cards.append((f, int(m.group(1)) if m else None, src[:44]))
print("\n伽马 GM-25 卡 %d 张" % len(cards))
for f, n, src in cards:
    if not n:
        print("   %-46s 题号未解析" % os.path.basename(f)[:46]); continue
    ims = crop(n)
    print("   %-46s 第%2d题 → %d 片 %s" % (os.path.basename(f)[:46], n, len(ims),
                                       ", ".join("p%d %dx%d" % (p, w, h) for _, p, w, h in ims)))
    if apply and ims:
        newans = ["## 参考答案", "",
                  "📎 **答案出处**：源卷《gamma晶体结构习题》**第 %d 题**（题目与解答同页，按题界裁图，共 %d 片）；"
                  "含结构图与评分标注。" % (n, len(ims)), ""]
        for nm, _, _, _ in ims:
            newans += ["![](images/%s)" % nm, ""]
        t = open(f, encoding="utf-8-sig").read().replace("\r\n", "\n")
        j = t.find("## 参考答案"); k = t.find("## 知识点映射")
        bfp = os.path.join(BK, os.path.basename(f) + ".orig")
        if not os.path.exists(bfp):
            open(bfp, "w", encoding="utf-8", newline="\n").write(t)
        open(f, "w", encoding="utf-8", newline="\n").write(t[:j] + "\n".join(newans) + "\n" + t[k:])
print("\n%s" % ("已写入" if apply else "（dry-run）"))
