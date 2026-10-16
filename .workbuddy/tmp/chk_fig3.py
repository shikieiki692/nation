# -*- coding: utf-8 -*-
"""核实三处缺陷的源图文件存在性与内容 sha（复刻 verify_fig_coverage.content_key）。"""
import glob
import hashlib
import os

ROOT = r"C:\Obsidion\妙妙屋"
IMG_DIRS = glob.glob(os.path.join(ROOT, "04-题库", "**", "images"), recursive=True)

CAND = {
    "X Q6": ["b820c9b294946eae7e961f0511d94691cbb1b6e7c2d0a839b7dc40498e7b5dd6.jpg"],
    "XI Q10": ["143ca87a54061c3956ccb480feb22aef092f177264fe6e25c062ca85fb9e12bc.jpg",
               "7e7ab009ad656c8c262b775a4dfb6692be5c809399d19217d5cd2eb924073f3f.jpg",
               "8d3112e549b32ad877253a55e22aa27113fe7f10ef479397353d90738c45fc25.jpg"],
    "XIp Q7": ["490596bc3de9bbd3421a390c55ce4108f6d50dc039a635472223103c9ff8dc0d.jpg"],
}
EXPECT = {"X Q6": "14e72c9d70", "XI Q10": "c5aa01ceb2 / 5b30830532", "XIp Q7": "94e83b5843"}

for k, names in CAND.items():
    print("== %s（期望缺失 key: %s）" % (k, EXPECT[k]))
    for n in names:
        hit = ""
        for d in IMG_DIRS:
            p = os.path.join(d, n)
            if os.path.isfile(p):
                sha = hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]
                hit = "%s  ← %s" % (sha, os.path.relpath(p, ROOT))
                break
        print("   %s : %s" % (n[:16], hit or "❌ 未在 04-题库/**/images 找到"))
    print()
