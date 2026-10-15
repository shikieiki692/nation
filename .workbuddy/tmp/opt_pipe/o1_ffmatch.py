# -*- coding: utf-8 -*-
"""O1 回源定位 v5：FFT 归一化互相关模板匹配，把「卡内图」对回源 PDF 的具体页。

背景：卡内图是建卡时从源页**重裁/重编码**的 ⇒ sha 匹配失效（v3 证伪）；
chemy 合集为扫描页、无文字层 ⇒ 关键词定位失效。改走像素级模板匹配（numpy FFT）。

用法: o1_ffmatch.py <卡路径> <PDF路径> <页码起> <页码止> [图数上限]
输出: 每页最佳相关系数（归一化互相关 NCC，1.0＝完全一致），按页排序。
"""
import os, re, sys
import numpy as np
import fitz
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def gray(path):
    im = Image.open(path).convert("L")
    return np.asarray(im, dtype=np.float64)


def ncc(page, tpl):
    """归一化互相关最大值（page >= tpl）。"""
    ph, pw = page.shape
    th, tw = tpl.shape
    if th > ph or tw > pw:
        return -1.0
    H = int(2 ** np.ceil(np.log2(ph + th)))
    W = int(2 ** np.ceil(np.log2(pw + tw)))
    F = np.fft.rfft2(page, s=(H, W))
    T = np.fft.rfft2(np.flipud(np.fliplr(tpl)), s=(H, W))
    corr = np.fft.irfft2(F * T, s=(H, W))
    corr = corr[:ph - th + 1, :pw - tw + 1]
    # 归一化：减去局部均值、除以局部标准差
    win = np.ones((th, tw))
    s1 = corr / (th * tw)
    # 局部平方和（积分图）
    cs = np.cumsum(np.cumsum(np.pad(page ** 2, ((1, 0), (1, 0))), 0), 1)
    ss = (cs[th:, tw:] - cs[:-th, tw:] - cs[th:, :-tw] + cs[:-th, :-tw])
    tsq = (tpl ** 2).sum()
    tmean = tpl.mean()
    denom = np.sqrt(np.maximum(ss - (th * tw) * (s1 / max(1e-9, 1)) ** 2 * (th * tw) / (th * tw), 0)
                    * max(tsq - (th * tw) * tmean ** 2, 0))
    with np.errstate(divide="ignore", invalid="ignore"):
        r = (corr - (th * tw) * s1 * tmean) / np.where(denom == 0, np.nan, denom)
    return float(np.nanmax(r))


def main():
    card, pdf, p0, p1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    lim = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    t = open(card, encoding="utf-8-sig", errors="replace").read()
    hs = re.findall(r'images/([0-9a-f]{64}\.(?:jpg|png))', t)
    seen, paths = set(), []
    for h in hs:
        if h in seen:
            continue
        seen.add(h)
        p = os.path.join(os.path.dirname(card), "images", h)
        if os.path.exists(p):
            paths.append((h, p))
    paths = paths[:lim]
    print("模板图 %d 张（卡内共 %d）" % (len(paths), len(seen)))
    d = fitz.open(pdf)
    for pg in range(p0, min(p1, d.page_count) + 1):
        fp = os.path.join(HERE, "_ffm_pg.png")
        d[pg - 1].get_pixmap(dpi=72).save(fp)
        page = gray(fp)
        best = -2.0
        for h, tp in paths:
            tpl = gray(tp)
            # 按宽度比例缩放到页面尺度（图在页上占约 30%~70% 宽）
            for frac in (0.30, 0.45, 0.60, 0.80):
                tw = max(24, int(page.shape[1] * frac))
                sc = tw / tpl.shape[1]
                th = max(12, int(tpl.shape[0] * sc))
                tt = np.asarray(Image.open(tp).convert("L").resize((tw, th)), dtype=np.float64)
                r = ncc(page, tt)
                best = max(best, r)
        print("  p%02d  NCC_max=%.3f" % (pg, best))
    d.close()


main()
