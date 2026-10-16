# -*- coding: utf-8 -*-
r"""o2_sheet.py —— 把 locate_out/o2v/<tag>/ 下的 thumb_*.png 拼成 3x3 接触表（带页码标签），
便于「一屏看 9 页」定位/目检，避免逐张读图。输出 sheet_<kind>_<k>.png。"""
import os
import re
import sys

from PIL import Image, ImageDraw

O2V = r"C:/Obsidion/妙妙屋/.workbuddy/tmp/opt_pipe/locate_out/o2v"
CW = 780          # 单元格宽（高按比例）
PAD = 8
LBL = 30


def main():
    only = sys.argv[1:] or None
    for tag in sorted(os.listdir(O2V)):
        if only and not any(o in tag for o in only):
            continue
        d = os.path.join(O2V, tag)
        thumbs = [f for f in os.listdir(d) if f.startswith("thumb_")]
        bykind = {}
        for f in thumbs:
            m = re.match(r"thumb_([qa])_p(\d+)\.png$", f)
            if m:
                bykind.setdefault(m.group(1), []).append((int(m.group(2)), f))
        for kind, items in sorted(bykind.items()):
            items.sort()
            for k in range(0, len(items), 9):
                chunk = items[k:k + 9]
                cells = []
                for _, f in chunk:
                    im = Image.open(os.path.join(d, f)).convert("RGB")
                    w, h = im.size
                    nh = int(CW * h / w)
                    cells.append(im.resize((CW, nh)))
                rows = (len(cells) + 2) // 3
                ch = max(c.size[1] for c in cells) + LBL
                sheet = Image.new("RGB", (3 * (CW + PAD) + PAD, rows * (ch + PAD) + PAD), "white")
                dr = ImageDraw.Draw(sheet)
                for i, (pno, _) in enumerate(chunk):
                    r, c = divmod(i, 3)
                    x = PAD + c * (CW + PAD)
                    y = PAD + r * (ch + PAD)
                    dr.rectangle([x, y, x + CW, y + LBL - 4], fill=(230, 230, 230))
                    dr.text((x + 8, y + 6), "p%d" % pno, fill=(0, 0, 0))
                    sheet.paste(cells[i], (x, y + LBL))
                out = os.path.join(d, "sheet_%s_%d.png" % (kind, k // 9 + 1))
                sheet.save(out, quality=88)
                print("  %-32s %s  %d页 → %s" % (tag[:30], kind, len(chunk), os.path.basename(out)))


if __name__ == "__main__":
    main()
