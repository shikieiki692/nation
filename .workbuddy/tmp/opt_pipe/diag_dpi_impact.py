# -*- coding: utf-8 -*-
"""量化「按源像素封顶贴图宽度」的影响面（只读，不改任何文件）。

对 7 卷（答案版+学生版）引用的每张图：
  当前渲染宽 = min(CONTENT_W, capw[cat], caph[cat]*aspect)
  新渲染宽   = min(当前渲染宽, px_w/MIN_DPI*2.54)
并对比 dpi。
"""
import glob
import io
import os
import re
import sys

VAULT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(VAULT, "04-题库")
ORGBASE = os.path.join(QB, "2026机构初赛模拟题")
IMG_EMB = re.compile(r"!\[\[([^\]\|\\]+?)(?:\\?\|\d+)?\]\]")

CONTENT_W = 21 - 1.9 * 2          # 17.2 cm
CAP = {"land": (7.0, 5.2), "port": (4.6, 6.6), "sq": (5.6, 5.6), "page": (16.5, 21.0)}
PAGE_MIN_LONG = 1800

try:
    MIN_DPI = float(sys.argv[sys.argv.index("--dpi") + 1]) if "--dpi" in sys.argv else 150.0
except Exception:
    MIN_DPI = 150.0

idx = {}
for p in glob.glob(os.path.join(ORGBASE, "*", "images", "*")):
    idx.setdefault(os.path.basename(p), p)

from PIL import Image  # noqa: E402


def px_of(name):
    src = idx.get(name)
    if not src or not os.path.exists(src):
        return None
    try:
        with Image.open(src) as im:
            return im.size
    except Exception:
        return None


def current_w_cm(w, h):
    a = w / h
    key = "land" if a > 1.3 else ("port" if a < 0.7 else "sq")
    mw, mh = CAP[key]
    return min(CONTENT_W, mw, mh * a), key


rows = []
for V in ("X", "XIp", "XI", "XII", "XIII", "XIV", "XV"):
    names = set()
    for ed in ("答案版", "学生版"):
        f = os.path.join(QB, "初赛模拟卷%s（非有机·%s）.md" % (V, ed))
        if not os.path.exists(f):
            continue
        names |= set(IMG_EMB.findall(io.open(f, encoding="utf-8-sig").read()))
    for n in sorted(names):
        wh = px_of(n)
        if not wh:
            rows.append((V, n, None, None, None, None, "缺图"))
            continue
        w, h = wh
        cur_w, cat = current_w_cm(w, h)
        is_page = max(w, h) >= PAGE_MIN_LONG
        if is_page:
            cur_w, cat = min(CONTENT_W, CAP["page"][0], CAP["page"][1] * w / h), "page"
        new_w = min(cur_w, w / MIN_DPI * 2.54)
        cur_dpi = w / (cur_w / 2.54)
        new_dpi = w / (new_w / 2.54)
        rows.append((V, n, (w, h), cat, cur_w, new_w, "缩" if new_w < cur_w - 1e-6 else ""))

print("MIN_DPI = %.0f  ｜  CONTENT_W = %.1fcm" % (MIN_DPI, CONTENT_W))
print("=" * 100)
print("%-5s %-34s %-12s %-6s %8s %8s %8s %8s" % ("卷", "图", "像素", "档", "现宽cm", "新宽cm", "现dpi", "新dpi"))
print("-" * 100)
shrink = []
for V, n, wh, cat, cw, nw, tag in rows:
    if wh is None:
        print("%-5s %-34s %s" % (V, n[:34], "缺图"))
        continue
    if tag == "缩":
        shrink.append((V, n, wh, cw, nw))
    cd = wh[0] / (cw / 2.54)
    nd = wh[0] / (nw / 2.54)
    flag = "★" if tag == "缩" else " "
    if tag == "缩" or cd < 150:
        print("%-5s %-34s %-12s %-6s %8.2f %8.2f %8.1f %8.1f %s"
              % (V, n[:34], "%dx%d" % wh, cat, cw, nw, cd, nd, flag))
print("-" * 100)
print("受影响（会缩小）%d 张 / 总 %d 张" % (len(shrink), len([r for r in rows if r[2]])))
tiny = [s for s in shrink if s[4] < 2.5]
print("缩到 <2.5cm 的：%d 张" % len(tiny))
for V, n, wh, cw, nw in tiny:
    print("   %-5s %-34s %s  %.2f→%.2fcm" % (V, n[:34], "%dx%d" % wh, cw, nw))
