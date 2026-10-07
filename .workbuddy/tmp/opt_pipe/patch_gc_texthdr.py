#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patch_gc_texthdr.py —— 给 gcho_crop.py 加「文字层题头定位」：
手稿的**题干是印刷体、带文字层**，可用 get_text 精确定位「第N题」行，
优于（手写题头识别不稳的）OCR 定位。文字层优先、OCR 补缺。
"""
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8")
P = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe\gcho_crop.py"
s = io.open(P, encoding="utf-8").read()

# ① 插入 text_markers 函数（放在 markers 之前）
if "def text_markers(" not in s:
    anchor = "def markers(idx, dpi):"
    fn = '''def text_markers(pdf):
    """用 PDF **文字层**定位印刷题头「第N题」→ {qno: (page, y_pt, x_pt, page_w_pt)}。
    手稿的题干是印刷体（有文字层），手写的是解答 ⇒ 文字层比 OCR 可靠。"""
    out = {}
    try:
        doc = fitz.open(pdf)
    except Exception:
        return out
    for i in range(doc.page_count):
        pg = doc[i]; W = pg.rect.width
        d = pg.get_text("dict")
        for blk in d.get("blocks", []):
            for ln in blk.get("lines", []):
                txt = "".join(sp.get("text", "") for sp in ln.get("spans", [])).replace(" ", "")
                m = re.match(r"^第(\\d{1,2})题", txt)
                if m:
                    q = int(m.group(1))
                    if 1 <= q <= 30 and q not in out:
                        x0, y0, x1, y1 = ln["bbox"]
                        out[q] = (i + 1, float(y0), float(x0), float(W))
    doc.close()
    return out


'''
    assert anchor in s, "锚点缺失"
    s = s.replace(anchor, fn + anchor, 1)

# ② main 里：文字层优先，OCR 补缺
old = "    mks = markers(idx, 150)\n"
new = '''    mks = markers(idx, 150)
    # ★ 文字层优先（印刷题干定位，优于手写题头 OCR）
    _k = 150.0 / 72.0
    _tm = text_markers(pdf)
    if _tm:
        tm = [(q, p, y * _k, x * _k, w * _k) for q, (p, y, x, w) in sorted(_tm.items())]
        tm.sort(key=lambda t: (t[1], _col(t[3], t[4]), t[2]))
        have = {t[0] for t in tm}
        mks = tm + [m for m in mks if m[0] not in have]
        mks.sort(key=lambda t: (t[1], _col(t[3], t[4]), t[2]))
        print("  [文字层定位] %d 题：%s" % (len(tm), [t[0] for t in tm]))
'''
assert old in s, "main 锚点缺失"
s = s.replace(old, new, 1)

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("✔ patch 完成")
