# -*- coding: utf-8 -*-
r"""O2 十卡：**卡题面 ↔ L0 源 md 反向覆盖**检查（建卡期内容丢失排查）。

判据：在 L0 源 md 中，取「该卡小问号标签序列的首→末」区间为问题范围；
      对该范围内每个 8-gram，检查是否出现在卡题面中。**连续未命中 ≥ 24 字** ⇒ 候选丢失。
⚠️ 只筛「值得看」；阈值类假阳性 ⇒ **终判人工逐字核对**（回源补录口径）。
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)

O = ".workbuddy/tmp/opt_pipe/"


def hz(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s)


def grams(s, n=8):
    return {s[i:i + n] for i in range(0, max(0, len(s) - n + 1))}


def read(p):
    with io.open(p, encoding="utf-8-sig", errors="replace") as fh:
        return fh.read().replace("\r\n", "\n")


def section(txt, *names):
    for nm in names:
        m = re.search(r"^##[ \t]*" + nm + r"[ \t]*\n(.*?)(?=^##(?!#)|\Z)",
                      txt, re.S | re.M)
        if m:
            return m.group(1)
    return txt


cards = [l.strip() for l in io.open(O + "o2_cards.txt", encoding="utf-8") if l.strip()]
print("卡数 =", len(cards))

QN = re.compile(r"(?<![\d.])(\d{1,2}-\d{1,2}(?:-\d{1,2})*)(?![\d])")

for idx, cp in enumerate(cards, 1):
    txt = read(cp)
    q = section(txt, "题目")
    qz = hz(re.sub(r"!\[\[[^\]]*\]\]", " ", q))
    src_rel = re.search(r'^source_file:[ \t]*"([^"]+)"', txt, re.M)
    sn = re.search(r"^source_norm:[ \t]*(.+)$", txt, re.M)
    print("\n" + "=" * 78)
    print("%2d %s" % (idx, os.path.basename(cp)[:52]))
    print("    source_norm = %s" % (sn.group(1).strip() if sn else "?"))
    print("    题面汉字 = %d" % len(qz))
    if not src_rel:
        print("    ⛔ 无 source_file")
        continue
    p = src_rel.group(1)
    cand = [p, os.path.join("06-外部资料导入/OCR", p)]
    l0 = next((c for c in cand if os.path.isfile(c)), None)
    if not l0:
        print("    ⛔ L0 未找到: %s" % p)
        continue
    lt = read(l0)
    lz = hz(re.sub(r"!\[\[[^\]]*\]\]", " ", lt))
    # 卡题面里的（源号）小问标签
    labs = []
    for m in QN.finditer(re.sub(r"!\[\[[^\]]*\]\]", " ", q)):
        labs.append(m.group(1))
    labs = list(dict.fromkeys(labs))
    if not labs:
        print("    (无小问标签，跳过区间定位)")
        continue
    # 在 L0（含数字，未剥）中定位首/末标签
    raw = re.sub(r"!\[\[[^\]]*\]\]", " ", lt)
    pos = [raw.find(l) for l in (labs[0], labs[-1])]
    if min(pos) < 0:
        print("    (标签 %s/%s 在 L0 未命中 ⇒ L0 编号口径不同)" % (labs[0], labs[-1]))
        continue
    seg = hz(raw[pos[0]:pos[1] + 40])
    g = grams(seg)
    if not g:
        continue
    miss = [x for x in g if x not in qz]
    cov = 1 - len(miss) / len(g)
    print("    L0 区间 %s…%s ｜ 8-gram %d ｜ 未命中 %d ｜ 覆盖 %.3f"
          % (labs[0], labs[-1], len(g), len(miss), cov))
    if not miss:
        continue
    # 找连续未命中段（用滑窗标出）
    seg_g = [seg[i:i + 8] for i in range(len(seg) - 7)]
    runs, cur = [], []
    for i, gg in enumerate(seg_g):
        if gg not in qz:
            cur.append(i)
        else:
            if len(cur) >= 3:
                runs.append((cur[0], cur[-1]))
            cur = []
    if len(cur) >= 3:
        runs.append((cur[0], cur[-1]))
    for a, b in runs[:6]:
        span = seg[max(0, a - 4):b + 12]
        print("      ⚠️ 未命中段(≈%d 字): %s" % (b - a + 8, span[:110]))
