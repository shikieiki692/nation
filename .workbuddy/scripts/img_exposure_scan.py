"""全库「曝光度」扫描：逐张取全分辨率最暗/最亮像素与墨量分位。

为什么要全分辨率：缩略图会把细线平均成白 ⇒ 低估墨迹、高估「空白」。
判据（沿用第二批已标定口径）：
    正常扫描/线稿  minpx   0–50
    轻欠曝         minpx  50–150
    极欠曝         minpx 150–230
    真·空白        minpx 230–255
输出 JSON；同时给出各档张数与体积。
"""
import json, sys
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

V = Path(r"C:\Obsidion\妙妙屋")
M = V / "媒体仓库"
OUT = V / ".workbuddy/tmp/img_audit/exposure_full.json"

files = [p for p in M.rglob("*")
         if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif"}
         and "_待清理" not in p.parts]
print(f"位图 {len(files)} 张", flush=True)

recs, failed = [], []
for i, p in enumerate(files):
    try:
        with Image.open(p) as im:
            g = im.convert("L")
            W, H = g.size
            # 全分辨率极值（不缩放）
            lo, hi = g.getextrema()
        recs.append(dict(name=p.name, w=W, h=H, minpx=lo, maxpx=hi,
                         kb=round(p.stat().st_size / 1024, 1)))
    except Exception as e:
        failed.append(p.name)
    if (i + 1) % 2000 == 0:
        print(f"  {i+1}/{len(files)}", flush=True)


def bucket(m):
    if m >= 230:
        return "D 真·空白(minpx≥230)"
    if m >= 150:
        return "C 极欠曝(150–230)"
    if m >= 50:
        return "B 轻欠曝(50–150)"
    return "A 正常(0–50)"


from collections import Counter, defaultdict
cnt = Counter(); vol = defaultdict(float); names = defaultdict(list)
for r in recs:
    b = bucket(r["minpx"]); cnt[b] += 1; vol[b] += r["kb"] / 1024; names[b].append(r["name"])

print("\n=== 曝光分档（全分辨率最暗像素）===")
for k in sorted(cnt):
    print(f"  {k:26s} {cnt[k]:6d} 张   {vol[k]:8.1f} MB   ({cnt[k]/len(recs)*100:5.1f}%)")
print(f"  {'合计':26s} {len(recs):6d} 张   {sum(vol.values()):8.1f} MB")
print(f"  打不开 {len(failed)}")

# 与既有 B2 类交叉（B2 是缩略图口径，可能漏）
Q = json.load(open(V / ".workbuddy/tmp/img_audit/quality_v8.json", encoding="utf-8"))
b2 = set(Q["garbage"]["B2 欠曝可救（最暗 150–230，内容在）"])
b2 |= set(Q["garbage"]["B1 真·空白（全图最暗 > 230，无墨）"])
newb = [r for r in recs if r["minpx"] >= 50 and r["name"] not in b2]
print(f"\n本次新发现（minpx≥50 且 旧 B1/B2 未覆盖）= {len(newb)} 张")
print("  按档:", dict(Counter(bucket(r['minpx']) for r in newb)))

OUT.write_text(json.dumps(dict(records=recs, failed=failed,
                               counts=dict(cnt)), ensure_ascii=False),
               encoding="utf-8")
print(f"→ {OUT} ({OUT.stat().st_size//1024} KB)")
