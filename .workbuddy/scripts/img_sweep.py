# -*- coding: utf-8 -*-
"""全量视觉扫描：机器建设 + 执行

复跑前置（工单不入库，只在本地重建；**台账入库**＝已判结果不可丢）：
    python -X utf8 .workbuddy/scripts/img_asset_audit.py --quality --json .workbuddy/tmp/img_audit/quality_v8.json
    python -X utf8 .workbuddy/scripts/img_asset_audit.py --context --json .workbuddy/tmp/img_audit/img_context.json
    python -X utf8 .workbuddy/scripts/img_sweep.py build
（工单 sweep_worklist.json 约 7.5 MB，不适合入库；台账 img_sweep_ledger.json 入库）
   worklist  —— 固定顺序的完整工单（可复现）
   ledger    —— 增量台账 {name: {verdict, note}}
   sheet     —— 生成指定区间的印相表（20 格/张）
   report    —— 进度与已判分布

用法:
  python sweep.py build                     # 建工单
  python sweep.py sheet <起> [每行] [每张格数]  # 生成下一张（自动跳过已判）
  python sweep.py text  <起> <止>            # 打印该区间的上下文/标签
  python sweep.py report                    # 进度
  python sweep.py apply <台账json片段>        # 写入判定
"""
import json, sys, re
from pathlib import Path
from collections import Counter, Counter as C

VAULT = Path(r"C:\Obsidion\妙妙屋")
MEDIA = Path(r"C:\Obsidion\妙妙屋\媒体仓库")
D = VAULT / ".workbuddy/tmp/img_audit"
OUT = D / "sweep"
OUT.mkdir(parents=True, exist_ok=True)
# ⚠️ 工单与台账必须读**已入库**的那份（scripts/ 下）；tmp/ 是草稿区不入库，
#    否则换机后无法接着扫（台账＝已判结果，丢了等于白扫）
S = VAULT / ".workbuddy" / "scripts"
WL = S / "img_sweep_worklist.json"
if not WL.exists():
    WL = D / "sweep_worklist.json"
LG = S / "img_sweep_ledger.json"
if not LG.exists():
    LG = D / "sweep_ledger.json"

CACHE = S / "img_quality_cache.json"
Q = json.load(open(CACHE if CACHE.exists() else D / "quality_v8.json", encoding="utf-8"))
CTX = json.load(open(D / "img_context.json", encoding="utf-8"))
G = Q["garbage"]
CLSOF = {n: k.split(" ")[0] for k, v in G.items() for n in v}


def build():
    recs = Q["records"]
    rows = []
    for r in recs:
        n = Path(r["f"]).name
        c = CTX.get(n) or []
        rows.append(dict(
            name=n, f=r["f"], w=r["w"], h=r["h"], kb=r["kb"], ink=r["ink"],
            colors=r["colors"], cls=CLSOF.get(n, ""),
            used=bool(c), head=(c[0]["head"] if c else ""),
            cap=next((t for t in ((c[0].get("after") or ""), (c[0].get("before") or ""))
                      if t and t.strip() and t.strip() != "[图]"), "") if c else "",
            md=(c[0]["md"] if c else "")))
    # 顺序：已判过的不动；先「有上下文」按 md 聚集，再「孤儿」按尺寸降序
    rows.sort(key=lambda x: (0 if x["used"] else 1, x["md"] or "~", -x["w"] * x["h"]))
    WL.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    print(f"工单 {len(rows)} 张 → {WL}")
    print(f"  有上下文 {sum(1 for r in rows if r['used'])}  孤儿 {sum(1 for r in rows if not r['used'])}")
    if not LG.exists():
        LG.write_text("{}", encoding="utf-8")


def load():
    return (json.load(open(WL, encoding="utf-8")),
            json.load(open(LG, encoding="utf-8")) if LG.exists() else {})


def report():
    rows, lg = load()
    done = [r for r in rows if r["name"] in lg]
    print(f"进度 {len(done)}/{len(rows)}  ({len(done)/len(rows)*100:.1f}%)")
    c = Counter(lg[r["name"]].get("v", "?") for r in done)
    for k, v in c.most_common():
        print(f"   {k:24s} {v}")
    return rows, lg


def text(a, b):
    rows, lg = load()
    for i in range(a, min(b, len(rows))):
        r = rows[i]
        if r["name"] in lg:
            continue
        print(f"#{i} {'[有上下文]' if r['used'] else '[孤儿]'} {r['w']}x{r['h']} "
              f"ink={r['ink']:.3f} kb={r['kb']} cls={r['cls'] or '-'} {r['name'][:20]}")
        if r["used"]:
            if r["head"]:
                print(f"     标题：{r['head'][:80]}")
            if r["cap"]:
                print(f"     图注：{r['cap'][:100]}")
            print(f"     md：{r['md'][:70]}")


def sheet(a, cols=5, per=20):
    from PIL import Image, ImageDraw
    Image.MAX_IMAGE_PIXELS = None
    rows, lg = load()
    items = []
    i = a
    while len(items) < per and i < len(rows):
        if rows[i]["name"] not in lg:
            items.append((i, rows[i]))
        i += 1
    if not items:
        print("区间内无待判"); return
    TW, TH, PAD, LBL = 246, 196, 8, 30
    nrow = (len(items) + cols - 1) // cols
    cv = Image.new("RGB", (cols * (TW + PAD) + PAD, 34 + nrow * (TH + LBL + PAD) + PAD),
                   (255, 255, 255))
    dr = ImageDraw.Draw(cv)
    dr.text((PAD, 10), f"全量扫描 #{items[0][0]}–#{items[-1][0]}（{len(items)} 格）", fill=(0, 0, 0))
    for k, (idx, r) in enumerate(items):
        rr, cc = divmod(k, cols)
        x0 = PAD + cc * (TW + PAD)
        y0 = 34 + rr * (TH + LBL + PAD)
        dr.rectangle([x0, y0, x0 + TW, y0 + TH], outline=(140, 140, 140))
        p = VAULT / r["f"]
        if p.exists():
            try:
                with Image.open(p) as im:
                    im = im.convert("RGB"); im.thumbnail((TW - 6, TH - 6))
                    cv.paste(im, (x0 + (TW - im.width) // 2, y0 + (TH - im.height) // 2))
            except Exception as ex:
                dr.text((x0 + 5, y0 + 5), "不开:" + type(ex).__name__, fill=(200, 0, 0))
        dr.text((x0 + 2, y0 + TH + 2),
                f"#{idx} {r['w']}x{r['h']} ink={r['ink']:.2f} {'U' if r['used'] else 'O'}",
                fill=(0, 0, 0))
        dr.text((x0 + 2, y0 + TH + 16), r["name"][:22], fill=(110, 110, 110))
    fn = OUT / f"sw_{items[0][0]:05d}_{items[-1][0]:05d}.png"
    cv.save(fn)
    print(f"→ {fn}  {cv.size}  区间 {items[0][0]}–{items[-1][0]}")


def apply(payload):
    """payload: {name: {v: 判定, n: 备注}}"""
    lg = json.load(open(LG, encoding="utf-8")) if LG.exists() else {}
    lg.update(payload)
    LG.write_text(json.dumps(lg, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"台账已更新，累计 {len(lg)} 条")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    elif cmd == "report":
        report()
    elif cmd == "sheet":
        sheet(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 5,
              int(sys.argv[4]) if len(sys.argv) > 4 else 20)
    elif cmd == "text":
        text(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "apply":
        apply(json.load(open(sys.argv[2], encoding="utf-8")))
    else:
        print(__doc__)
