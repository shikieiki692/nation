# -*- coding: utf-8 -*-
r"""verify_img_decodable.py —— 入库/替换图片的「PIL 可解码性」巡检闸门。

背景（2026-10-14 卷 XVI 实伤两例）：
  ① `fitz.extract_image()` 对 **SMask 位图**返回的主层是全黑 ⇒ 字节/尺寸/mode 全部正常，
     只有解码后统计亮度才能发现；
  ② 个别源 PDF 内嵌 JPEG，**本 venv 的 PIL 解码输出全黑**，而 LibreOffice/浏览器渲染正常
     （f7919657 实伤）⇒ 构建器读图即得黑图进 docx。
  ⇒ 凡「回源重制/替换/升级」产出的 jpg，**入库前必须过本断言**：PIL 解码 → 灰度 mean
     不得低于阈值（默认 100），且 std 不得近 0（纯色块）。

用法：
  python verify_img_decodable.py <img1.jpg> [img2.jpg ...]   # 显式清单
  python verify_img_decodable.py --dir <images目录> [--min 100]  # 整目录
  python verify_img_decodable.py --hashes <清单文件>          # 每行一个 hash（前缀或全串）
退出码：0 = 全部通过；1 = 有失败（打印 FAIL 行）。
"""
import glob
import hashlib
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
IMGS_ROOT = os.path.join(ROOT, "04-题库", "2026机构初赛模拟题")


def check(path, min_mean=100.0, min_std=8.0):
    try:
        im = Image.open(path)
        im.load()
    except Exception as e:
        return False, "PIL open/load 异常: %s" % e
    a = np.asarray(im.convert("L"), dtype=np.uint8)
    mean, std = float(a.mean()), float(a.std())
    if mean < min_mean and std < min_std * 4:
        return False, "疑似全黑/全暗 (mean=%.1f std=%.1f)" % (mean, std)
    if std < min_std:
        return False, "疑似纯色块 (std=%.1f)" % std
    return True, "mean=%.1f std=%.1f %dx%d %s" % (mean, std, a.shape[1], a.shape[0], im.mode)


def resolve_hashes(hashes):
    """hash 前缀/全串 → 文件路径"""
    out = []
    for h in hashes:
        hits = glob.glob(os.path.join(IMGS_ROOT, "*", "images", h + "*.jpg"))
        out.extend(hits or [None])
    return out


def main(argv):
    min_mean = 100.0
    files = []
    if "--dir" in argv:
        d = argv[argv.index("--dir") + 1]
        files = sorted(glob.glob(os.path.join(d, "*.jpg")))
        if "--min" in argv:
            min_mean = float(argv[argv.index("--min") + 1])
    elif "--hashes" in argv:
        hf = argv[argv.index("--hashes") + 1]
        with open(hf, encoding="utf-8") as f:
            hashes = [l.strip().split()[0] for l in f if l.strip() and not l.startswith("#")]
        files = resolve_hashes(hashes)
    else:
        files = [a for a in argv if not a.startswith("--")]
        if "--min" in argv:
            min_mean = float(argv[argv.index("--min") + 1])
    files = [f for f in files if f]
    if not files:
        print("no input files"); return 1
    fail = 0
    for fn in files:
        ok, msg = check(fn, min_mean)
        tag = "OK  " if ok else "FAIL"
        print("%s %s  %s" % (tag, os.path.relpath(fn, ROOT), msg))
        if not ok:
            fail += 1
    print("== %d/%d passed ==" % (len(files) - fail, len(files)))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
