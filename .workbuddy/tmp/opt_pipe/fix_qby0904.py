#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_qby0904.py —— 修正「题-QBY-09-04」答案区错挂第1、2题页（应挂第4题）。
源：清北营暑假高二班-试卷9-参考答案.pdf（18页，有文字层），第4题在 p8。
"""
import fitz, hashlib, io, os, re, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
try:
    fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
except Exception:
    pass
R = r"C:\Obsidion\妙妙屋"
PDF = os.path.join(R, "06-外部资料导入/OCR/01-题目/2026清北营夏令营/清北营高二试卷（前13套）/2026年清北营暑假高二班-试卷9-参考答案.pdf")
CARD = os.path.join(R, "04-题库/2026机构初赛模拟题/清北营/题-QBY-09-04-含磷杂环因其独特的空间结构和.md")
IMGDIR = os.path.join(R, "04-题库/2026机构初赛模拟题/清北营/images")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/qby_backup")
os.makedirs(BK, exist_ok=True)
Q = 4
OUT_DPI = 200
apply = "--apply" in sys.argv

doc = fitz.open(PDF)
# 定位「第Q题」行
hit = None
for i in range(doc.page_count):
    for blk in doc[i].get_text("dict").get("blocks", []):
        for ln in blk.get("lines", []):
            txt = "".join(s.get("text", "") for s in ln.get("spans", [])).replace(" ", "")
            if re.match(r"^第%d题" % Q, txt):
                hit = (i + 1, float(ln["bbox"][1])); break
        if hit: break
    if hit: break
print("第%d题定位 → p%d y=%.1f" % (Q, hit[0], hit[1]))

# 题界：到「第(Q+1)题」或页末
nxt = None
for i in range(hit[0] - 1, doc.page_count):
    for blk in doc[i].get_text("dict").get("blocks", []):
        for ln in blk.get("lines", []):
            txt = "".join(s.get("text", "") for s in ln.get("spans", [])).replace(" ", "")
            if re.match(r"^第%d题" % (Q + 1), txt):
                if i + 1 > hit[0]:
                    nxt = (i + 1, float(ln["bbox"][1]))
                break
        if nxt: break
    if nxt: break
print("第%d题 → %s" % (Q + 1, nxt))

names = []
for pno in range(hit[0], (nxt[0] if nxt else doc.page_count) + 1):
    pg = doc[pno - 1]; Rc = pg.rect
    top = max(0.0, hit[1] - 6) if pno == hit[0] else 0.0
    bot = (nxt[1] - 6) if (nxt and pno == nxt[0]) else Rc.y1
    if bot - top < 60:
        continue
    pix = pg.get_pixmap(dpi=OUT_DPI, clip=fitz.Rect(Rc.x0 + 16, top, Rc.x1 - 16, bot))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    print("  p%-3d %.0f~%.0fpt → %dx%dpx" % (pno, top, bot, im.width, im.height))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90, optimize=True, subsampling=0)
    data = buf.getvalue(); h = hashlib.sha256(data).hexdigest()
    fp = os.path.join(IMGDIR, h + ".jpg")
    if not os.path.exists(fp):
        open(fp, "wb").write(data)
    names.append(h + ".jpg")
doc.close()

newans = ["## 参考答案", "",
          "📎 **答案出处**：源卷答案册《清北营暑假高二班·试卷9 参考答案》**第 4 题**（p%d，按题界裁图，共 %d 片）；"
          "解答含结构式/图，**文字化需人工转录**。组卷命中本卡时请以图为准。" % (hit[0], len(names)), ""]
for n in names:
    newans += ["![](images/%s)" % n, ""]

t = open(CARD, encoding="utf-8-sig").read().replace("\r\n", "\n")
j = t.find("## 参考答案"); k = t.find("## 知识点映射")
old = t[j:k]
print("旧引用: %s" % re.findall(r"images/([^)]+)", old))
print("新引用: %s" % names)
if apply:
    bfp = os.path.join(BK, os.path.basename(CARD) + ".orig")
    if not os.path.exists(bfp):
        open(bfp, "w", encoding="utf-8", newline="\n").write(t)
    open(CARD, "w", encoding="utf-8", newline="\n").write(t[:j] + "\n".join(newans) + "\n" + t[k:])
    print("✔ 已写入")
else:
    print("(dry-run)")
