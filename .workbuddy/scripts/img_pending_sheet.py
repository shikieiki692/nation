# -*- coding: utf-8 -*-
"""待目检视觉核验：印相表生成器（大格 300x250 + 中文字体标注 + zoom 原尺寸复核）。

复跑前置（工单已入库；上下文与待目检清单属可重建的中间产物）：
    # 1) 上下文地图（必需）
    python -X utf8 .workbuddy/scripts/img_asset_audit.py --context \
        --json .workbuddy/tmp/img_audit/img_context.json
    # 2) 待目检三份索引的条目（pending_audit.json：{索引名: [行记录…]}）
    #    —— 由 .workbuddy/tmp/pending_audit.py 的建单段产出
    # 3) 主工单（已入库）：.workbuddy/scripts/img_pending_wo.json（589 条）
用法：
    python -X utf8 .workbuddy/scripts/img_pending_sheet.py sheet <起> <止>
    python -X utf8 .workbuddy/scripts/img_pending_sheet.py zoom <i> [<i> …]

原文说明：

为什么升级：上一版 236x200 格 + PIL 默认位图字体，中文标注糊成一团，
判读时只能看图、看不到「索引声称内容」，两路证据无法在同屏对照。
本版：格 300x250、4 列 × 5 行 = 20/板，标注用系统中文字体（微软雅黑/宋体）。

用法:
  pend_sheet2.py sheet <起> <止>    出板
  pend_sheet2.py zoom <i1> <i2> ... 原尺寸放大复核（并排原样 / 2x）
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

V = Path(r"C:\Obsidion\妙妙屋")
M = V / "媒体仓库"
O = V / ".workbuddy/tmp/img_audit"
# 工单可切换：主工单=在库×被引用（589）；副工单=在库×未引用（img_pending_wo_sec.json）
#   用环境变量 IMG_PENDING_WO 指定，默认主工单
import os as _os
WO = V / _os.environ.get("IMG_PENDING_WO", ".workbuddy/scripts/img_pending_wo.json")
print("[wo]", WO.name)
CTX = json.load(open(O / "img_context.json", encoding="utf-8"))
PA = json.load(open(O / "pending_audit.json", encoding="utf-8"))

# 声称内容（索引描述）按 basename 建索引
DESC, ROWOF = {}, {}
for tag, rows in PA.items():
    for r in rows:
        ROWOF[r["name"]] = r.get("row")
        row = r.get("row") or []
        DESC[r["name"]] = row[2] if len(row) > 2 else ""

FONT = None
for cand in (r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simsun.ttc",
             r"C:\Windows\Fonts\simhei.ttf"):
    if Path(cand).exists():
        try:
            FONT = ImageFont.truetype(cand, 13)
            FONT_S = ImageFont.truetype(cand, 11)
            break
        except Exception:
            pass


def put(dr, xy, text, fill=(0, 0, 0), small=False):
    if FONT:
        dr.text(xy, text, fill=fill, font=FONT_S if small else FONT)
    else:
        dr.text(xy, text, fill=fill)


WOL = json.load(open(WO, encoding="utf-8"))
mode = sys.argv[1]
nums = [int(x) for x in sys.argv[2:]]

if mode == "zoom":
    W = 900
    rows = []
    for i in nums:
        e = WOL[i]
        with Image.open(V / e["path"]) as im:
            im = im.convert("RGB")
            k = min(3.0, max(1.0, W / max(1, im.width)))
            rows.append((i, e, im, im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS), k))
    H = sum(min(r[4] and r[3].height, 1000) + 46 for r in rows) + 10
    cv = Image.new("RGB", (2 * W + 40, H), (250, 250, 250))
    dr = ImageDraw.Draw(cv)
    y = 4
    for i, e, im, big, k in rows:
        put(dr, (4, y), f"[{i}] {e['name'][:26]} {e['w']}x{e['h']} ×{k:.1f}　声称：{DESC.get(e['name'],'')[:56]}")
        cv.paste(im, (4, y + 18))
        cv.paste(big, (W + 30, y + 18))
        y += min(big.height, 1000) + 46
    f = O / "pend_zoom2.png"
    cv.save(f)
    print("->", f, cv.size, len(rows), "张")
    sys.exit(0)

lo, hi = nums[0], nums[1]
part = WOL[lo:hi]
TW, TH, PAD, LBL = 300, 250, 8, 36
cols = 4
rows_n = (len(part) + cols - 1) // cols
cv = Image.new("RGB", (cols * (TW + PAD) + PAD, rows_n * (TH + LBL + PAD) + 32), (246, 246, 246))
dr = ImageDraw.Draw(cv)
put(dr, (PAD, 8), f"待目检核验 第 {lo}–{hi-1} 张（共 {len(WOL)}）　"
                  f"标注＝编号/尺寸/声称内容")
for k, e in enumerate(part):
    rr, cc = divmod(k, cols)
    x0 = PAD + cc * (TW + PAD)
    y0 = 32 + rr * (TH + LBL + PAD)
    dr.rectangle([x0, y0, x0 + TW, y0 + TH], outline=(165, 165, 165))
    p = V / e["path"]
    try:
        with Image.open(p) as im:
            if im.mode in ("RGBA", "LA", "P"):      # 透明底合成到白底（本库踩过：直接 convert 会变黑）
                bg = Image.new("RGB", im.size, (255, 255, 255))
                im2 = im.convert("RGBA")
                bg.paste(im2, mask=im2.getchannel("A"))
                im = bg
            else:
                im = im.convert("RGB")
            im.thumbnail((TW - 8, TH - 8))
            cv.paste(im, (x0 + (TW - im.width) // 2, y0 + (TH - im.height) // 2))
    except Exception as ex:
        put(dr, (x0 + 8, y0 + 8), f"打不开 {type(ex).__name__}", fill=(200, 0, 0))
    desc = DESC.get(e["name"], "")
    tag = "【机器误判修正】" if "机器误判修正" in desc else ("【视觉核验】" if "视觉核验" in desc else "—")
    put(dr, (x0 + 3, y0 + TH + 2), f"[{lo+k}] {e['w']}x{e['h']} {tag}", fill=(0, 0, 0))
    put(dr, (x0 + 3, y0 + TH + 19), desc.replace("【机器误判修正】", "").replace("【视觉核验】", "")[:26],
        fill=(70, 70, 70), small=True)
f = O / f"p2_{lo:04d}_{hi:04d}.png"
cv.save(f)
print("->", f, cv.size, f"{len(part)} 格")
