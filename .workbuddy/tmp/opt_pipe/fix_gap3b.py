#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_gap3b.py —— 处理 3 张「整册随卡」遗留卡：
  届24 第9题 → 手稿 p9 有解答 ⇒ 按题裁图
  届26 第9题 → 手稿 4 页仅覆盖第1~8题 ⇒ 源缺答案，移除错题图
  届54 第9题 → 手稿 11 页仅覆盖第1~6题 ⇒ 源缺答案，移除错题图
"""
import fitz, glob, hashlib, io, os, re, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
try:
    fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
except Exception:
    pass
R = r"C:\Obsidion\妙妙屋"
A = os.path.join(R, "06-外部资料导入/OCR/01-题目/质心合集新/GChO模拟试题合集答案")
GDIR = os.path.join(R, "04-题库/2026机构初赛模拟题/质心GChO")
IMGDIR = os.path.join(GDIR, "images")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/gap3b_backup")
os.makedirs(BK, exist_ok=True)
apply = "--apply" in sys.argv


def card_of(rnd, q):
    for pat in ("题-GChO-%02d-%02d-*.md", "题-GChO-%d-%02d-*.md"):
        fs = glob.glob(os.path.join(GDIR, pat % (rnd, q)))
        if fs:
            return fs[0]
    return None


def save_img(im):
    buf = io.BytesIO(); im.convert("RGB").save(buf, "JPEG", quality=90, optimize=True, subsampling=0)
    data = buf.getvalue(); h = hashlib.sha256(data).hexdigest()
    fp = os.path.join(IMGDIR, h + ".jpg")
    if not os.path.exists(fp):
        open(fp, "wb").write(data)
    return h + ".jpg"


def write(c, newans):
    t = open(c, encoding="utf-8-sig").read().replace("\r\n", "\n")
    j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    bfp = os.path.join(BK, os.path.basename(c) + ".orig")
    if not os.path.exists(bfp):
        open(bfp, "w", encoding="utf-8", newline="\n").write(t)
    if apply:
        open(c, "w", encoding="utf-8", newline="\n").write(t[:j] + "\n".join(newans) + "\n" + t[k:])
        print("  ✔ 写入", os.path.basename(c)[:44])
    else:
        print("  (dry-run)", os.path.basename(c)[:44])


# ① 届24 第9题：手稿 p9（双栏整页）
c = card_of(24, 9)
doc = fitz.open(os.path.join(A, "ZCHEM-GChO24解析手稿.pdf"))
pno = 9
pg = doc[pno - 1]; Rc = pg.rect
pix = pg.get_pixmap(dpi=200, clip=fitz.Rect(Rc.x0 + 16, 0, Rc.x1 - 16, Rc.y1))
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
name = save_img(im)
print("届24：p%d → %dx%dpx → %s" % (pno, im.width, im.height, name[:16]))
doc.close()
newans = ["## 参考答案", "",
          "📎 **答案出处**：源卷**手写解析手稿**第 9 题（p9，按题界裁图）；手写笔迹，含结构式/图，"
          "**文字化需人工转录**。组卷命中本卡时请以图为准。", "",
          "![](images/%s)" % name, ""]
write(c, newans)

# ② 届26 / 届54：源缺答案
for rnd, npage, upto in ((26, 4, 8), (54, 11, 6)):
    c = card_of(rnd, 9)
    t = open(c, encoding="utf-8-sig").read().replace("\r\n", "\n")
    j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    oldims = re.findall(r"!\[\]\(images/([^)]+)\)", t[j:k])
    print("届%d：原挂 %d 张整册页图" % (rnd, len(oldims)))
    newans = ["## 参考答案", "",
              "⛔ **源确缺答案**：源卷手写解析手稿（共 %d 页）经核仅覆盖第 1~%d 题，**未含本题（第 9 题）解答**；"
              "原随卡的整册页图（%d 张，均属其他题）已移除，以免误当本题答案。"
              % (npage, upto, len(oldims)), ""]
    write(c, newans)
