#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_ansbook.py —— 通用回源救卡：从「题目+答案」合排的源 PDF 按题裁图，回填卡答案区。

--pdf  <PDF路径>  --inst <机构目录名>  --pat <卡文件名 glob>  --mode <next|last>
  mode=next：答案在「下一题标题所在页的页首」（GM-25 / 汇智 交错型）
  mode=last：答案在「题目区之后该题号再次出现处」（无机化学一 前题后解析型）
"""
import glob, hashlib, io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
import fitz
from PIL import Image
try:
    fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
except Exception:
    pass

R = r"C:\Obsidion\妙妙屋"
argv = sys.argv
def opt(k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d
PDF = opt("--pdf"); INST = opt("--inst"); PAT = opt("--pat", "题-*.md"); MODE = opt("--mode", "next")
apply = "--apply" in argv
IMGDIR = os.path.join(R, "04-题库/2026机构初赛模拟题", INST, "images")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/ansbook_backup")
os.makedirs(BK, exist_ok=True); os.makedirs(IMGDIR, exist_ok=True)
doc = fitz.open(PDF)


def marks_all():
    """→ {n: [(page, y), ...]} 按出现顺序"""
    mm = {}
    for i in range(doc.page_count):
        for blk in doc[i].get_text("dict").get("blocks", []):
            for ln in blk.get("lines", []):
                txt = "".join(s.get("text", "") for s in ln.get("spans", [])).replace(" ", "")
                m = re.match(r"第(\d+)题", txt)
                if m:
                    mm.setdefault(int(m.group(1)), []).append((i, float(ln["bbox"][1])))
    return mm


MA = marks_all()
print("题号出现：%s" % {k: len(v) for k, v in sorted(MA.items())})


def save(pg, p, top, bot):
    pix = pg.get_pixmap(dpi=190, clip=fitz.Rect(pg.rect.x0 + 14, top, pg.rect.x1 - 14, bot))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90, optimize=True, subsampling=0)
    data = buf.getvalue(); h = hashlib.sha256(data).hexdigest()
    fp = os.path.join(IMGDIR, h + ".jpg")
    if not os.path.exists(fp):
        open(fp, "wb").write(data)
    return h + ".jpg", p + 1, im.width, im.height


def crop(n):
    occ = MA.get(n, [])
    if not occ:
        return []
    if MODE == "last":
        # 取该题号的最后一次出现（解析区）→ 直到下一题号的解析出现处/文末
        p0, y0 = occ[-1]
        later = [(k, v) for k, v in MA.items() for v in v if (v[0], v[1]) > (p0, y0)]
        later.sort(key=lambda x: x[1])
        # 下一题的解析起点：不同题号、位置在其后
        nxt = [v for k, v in later if k != n]
        p1, y1 = nxt[0] if nxt else (doc.page_count - 1, doc[doc.page_count - 1].rect.y1)
    else:
        p0, y0 = occ[0]
        order = sorted(MA)
        nx = [k for k in order if k > n]
        if nx:
            p1, y1 = MA[nx[0]][0]
        else:
            p1, y1 = doc.page_count - 1, doc[doc.page_count - 1].rect.y1
    out = []
    for p in range(p0, p1 + 1):
        pg = doc[p]
        top = max(0.0, y0 - 8) if p == p0 else 0.0
        bot = (y1 - 8) if p == p1 else pg.rect.y1
        if bot - top < 50:
            continue
        out.append(save(pg, p, top, bot))
    return out


files = sorted(glob.glob(os.path.join(R, "04-题库/2026机构初赛模拟题", INST, PAT)))
SRCF = opt("--src", "")            # ★ 只处理 source 含该关键词的卡（防误改同前缀卡）
if SRCF:
    hit = []
    for f in files:
        t0 = open(f, encoding="utf-8-sig", errors="replace").read()
        s0 = (re.search(r'^source:\s*["\']?(.*?)["\']?\s*$', t0, re.M) or [None, ""])[1]
        if SRCF in s0 or SRCF in (re.search(r'^source_file:\s*["\']?(.*?)["\']?\s*$', t0, re.M) or [None, ""])[1]:
            hit.append(f)
    print("按 source 过滤：%d → %d 张" % (len(files), len(hit)))
    files = hit
print("卡 %d 张" % len(files))
for f in files:
    t = open(f, encoding="utf-8-sig", errors="replace").read()
    src = (re.search(r'^source:\s*["\']?(.*?)["\']?\s*$', t, re.M) or [None, ""])[1]
    m = re.search(r"第\s*(\d+)\s*题", src)
    if not m:
        print("   %-46s 题号未解析（%s）" % (os.path.basename(f)[:46], src[:30])); continue
    n = int(m.group(1))
    ims = crop(n)
    print("   %-46s 第%2d题 → %d 片 %s" % (os.path.basename(f)[:46], n, len(ims),
                                        ", ".join("p%d %dx%d" % (p, w, h) for _, p, w, h in ims)))
    if apply and ims:
        newans = ["## 参考答案", "",
                  "📎 **答案出处**：源卷《%s》**第 %d 题**（题目与解答同册，按题界裁图，共 %d 片）；含解答与评分标注。"
                  % (os.path.basename(PDF)[:28], n, len(ims)), ""]
        for nm, _, _, _ in ims:
            newans += ["![](images/%s)" % nm, ""]
        tt = open(f, encoding="utf-8-sig").read().replace("\r\n", "\n")
        j = tt.find("## 参考答案"); k = tt.find("## 知识点映射")
        bfp = os.path.join(BK, os.path.basename(f) + ".orig")
        if not os.path.exists(bfp):
            open(bfp, "w", encoding="utf-8", newline="\n").write(tt)
        open(f, "w", encoding="utf-8", newline="\n").write(tt[:j] + "\n".join(newans) + "\n" + tt[k:])
print("\n%s" % ("已写入" if apply else "（dry-run）"))
