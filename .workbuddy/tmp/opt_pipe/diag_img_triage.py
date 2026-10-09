# -*- coding: utf-8 -*-
"""对「被剔出卷 md 的卡图」做机器分诊：尺寸 / 长宽比 / 暗度 / 中灰占比。"""
import glob, json, os, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe"))
import build_org as BO

manual = BO.load_noise()
keep = BO.load_keep()

HASHES = """c0ab232a0f4c417b 2ed21d28e62aacac 3352dff0d9604b07 4ab949e194d3574d 4cc205f0878ad488
9321cece39e5f1d8 938072624ab64647 f21863c46f3febace 3ecb6a8a1b7fd32a c1c8f6c039e39d48
4ff91afe046f91b8 15f705caa38b1d00 3dd7a6fc14155c53 e67ecd53a4b9a426 6420235fcfdd95fc
fc55dd9d8f546f7a c3a16d55e20bbc48 e8d0ed8e6bfbc246 869c6a8e9bd28369 ec25ca675cadba61
1a271a40156d6782""".split()


def stats(p):
    im = Image.open(p)
    w, h = im.size
    g = im.convert("L").resize((min(w, 200), min(h, 200)))
    px = list(g.getdata())
    n = len(px)
    dark = sum(1 for v in px if v < 110) / n
    midgray = sum(1 for v in px if 110 <= v < 245) / n
    return w, h, dark, midgray


print("%-20s %5s %5s %7s %7s %-8s %s" % ("hash", "w", "h", "dark", "midgray", "清单", "尺寸KB"))
for hs in HASHES:
    g = glob.glob(os.path.join(ROOT, "04-题库/**/" + hs + "*"), recursive=True)
    if not g:
        print("%-20s  ! 未找到" % hs); continue
    p = g[0]
    try:
        w, h, d, m = stats(p)
    except Exception as e:
        print("%-20s  ! 打不开 %s" % (hs, e)); continue
    tag = ("M" if os.path.basename(p) in manual else "-") + ("K" if os.path.basename(p) in keep else "-")
    print("%-20s %5d %5d %7.4f %7.4f %-8s %.1f" % (hs, w, h, d, m, tag, os.path.getsize(p) / 1024))
