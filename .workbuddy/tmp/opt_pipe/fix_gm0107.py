#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_gm0107.py —— 修正「题-GM-01-07」答案区错挂第1题页的问题：
从源答案册《五一伽马杭州答案1.pdf》按题界裁出第7题（p10尾 → p11整页 → p12顶），替换原图。
"""
import fitz, glob, hashlib, os, re, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
try:
    fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
except Exception:
    pass

R = r"C:\Obsidion\妙妙屋"
PDF = os.path.join(R, "06-外部资料导入/OCR/01-题目/2026年五一伽马初赛模拟杭州班/试题➕答案/五一伽马杭州答案1.pdf")
CARD = os.path.join(R, "04-题库/2026机构初赛模拟题/伽马/题-GM-01-07-71有一系列卤代烷烃当时的转.md")
IMGDIR = os.path.join(R, "04-题库/2026机构初赛模拟题/伽马/images")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/gm_backup")
os.makedirs(BK, exist_ok=True)
apply = "--apply" in sys.argv
SRC_DPI = 150.0
OUT_DPI = 200

doc = fitz.open(PDF)
PH = doc[0].rect.height          # 页高(pt)
PW = doc[0].rect.width
pt = lambda px: px * 72.0 / SRC_DPI     # 150dpi px → pt

# 题界（150dpi 像素）：第7题 p10 y=1487 → 第8题 p12 y=1063
SLICES = [
    (10, pt(1487 - 14), PH),             # p10：第7题标题 + 7.1
    (11, 0.0, PH),                        # p11：整页 7.2~7.4
    (12, 0.0, pt(1063 - 16)),             # p12：顶 → 第8题标题前
]


def save_img(im):
    buf = im.tobytes()
    h = hashlib.sha256(buf).hexdigest()
    fp = os.path.join(IMGDIR, h + ".jpg")
    if not os.path.exists(fp):
        im.save(fp, "JPEG", quality=88, optimize=True)
    return h + ".jpg"


names = []
for pno, top, bot in SLICES:
    pg = doc[pno - 1]
    clip = fitz.Rect(pg.rect.x0 + 20, top, pg.rect.x1 - 20, bot)
    pix = pg.get_pixmap(dpi=OUT_DPI, clip=clip)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    print("  p%-3d %.0f~%.0fpt → %dx%dpx" % (pno, top, bot, im.width, im.height))
    names.append(save_img(im))
doc.close()

newans = ["## 参考答案", "",
          "📎 **答案出处**：源卷答案册《五一伽马杭州答案1》**第 7 题**（p10–p12，按题界裁图，共 %d 片）；"
          "选择题与结构式解答，**文字化需人工转录**。组卷命中本卡时请以图为准。" % len(names),
          ""]
for n in names:
    newans += ["![](images/%s)" % n, ""]

t = open(CARD, encoding="utf-8-sig").read().replace("\r\n", "\n")
j = t.find("## 参考答案"); k = t.find("## 知识点映射")
assert j > 0 and k > j, "答案区定界失败"
old = t[j:k]
print("旧答案区 %d 字，旧引用图: %s" % (len(old), re.findall(r"images/([^)]+)", old)))
print("新答案区引用: %s" % names)
if apply:
    bfp = os.path.join(BK, os.path.basename(CARD) + ".orig")
    if not os.path.exists(bfp):
        open(bfp, "w", encoding="utf-8", newline="\n").write(t)
    t2 = t[:j] + "\n".join(newans)[len("## 参考答案"):].lstrip("\n") if False else t[:j] + "\n".join(newans) + "\n" + t[k:]
    open(CARD, "w", encoding="utf-8", newline="\n").write(t2)
    print("✔ 已写入", os.path.basename(CARD))
else:
    print("(dry-run；加 --apply 生效)")
