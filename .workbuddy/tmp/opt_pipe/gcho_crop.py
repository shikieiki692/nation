#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gcho_crop.py —— GChO 手写解析稿「按题裁图」。
对每届手稿 PDF：OCR 定位「第N题」→ 按题裁区（跨页自动切片）→ 已 apply 则把卡答案区
替换为「出处注记 + 裁图」，并备份原文。

用法：
  python gcho_crop.py --round 37                 # dry-run，只打印计划
  python gcho_crop.py --round 37 --apply         # 写盘（裁图 + 改卡）
  python gcho_crop.py --round 37 --apply --limit 2
"""
import argparse, glob, hashlib, json, os, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None
from PIL import Image

R = r"C:\Obsidion\妙妙屋"
ANS = os.path.join(R, "06-外部资料导入/OCR/01-题目/质心合集新/GChO模拟试题合集答案")
GDIR = os.path.join(R, "04-题库/2026机构初赛模拟题/质心GChO")
IMGDIR = os.path.join(GDIR, "images")
LOC = os.path.join(R, ".workbuddy/tmp/opt_pipe/ocr_loc")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/gcho_ans_backup")
DPI = 200
MARK = re.compile(r"第\s*(\d+)\s*题")


def find_manuscript(rnd):
    for pat in ("ZCHEM-GChO%d解析手稿.pdf" % rnd, "ZCHEM-GChO%d解析手稿.PDF" % rnd):
        f = os.path.join(ANS, pat)
        if os.path.exists(f):
            return f
    return None


def load_index(rnd, pdf):
    """读 ocr_index 缓存；无则返回 None（需先跑 ocr_index.py）。"""
    f = os.path.join(LOC, "GChO%d.json" % rnd)
    if not os.path.exists(f):
        return None
    return json.load(open(f, encoding="utf-8"))


def markers(idx, dpi):
    """→ [(qno, page, y_px, x_px, page_w_px)]，按「阅读流」排序（页 → 栏 → y）。
    手稿多为双页跨页扫描（左栏＝一页、右栏＝另一页），故顺序须含栏次。"""
    out = []
    for row in idx:
        for b in row["blocks"]:
            m = MARK.search(b["t"].replace(" ", ""))
            if m and len(b["t"]) <= 16:      # 只认短标题块，避免正文里的「第N题」误命中
                out.append((int(m.group(1)), row["page"], b["y"], b["x"], row["w"]))
    out.sort(key=lambda t: (t[1], 0 if t[3] < t[4] * 0.45 else 1, t[2]))
    seen, res = set(), []
    for t in out:
        if t[0] in seen:
            continue
        seen.add(t[0]); res.append(t)
    return res


def _col(x, w):
    return 0 if x < w * 0.45 else 1


SUB1 = re.compile(r"^[（(]?\s*(\d{1,2})\s*[-–—－]\s*1\s*(?![\d\-–—])")


def sub_markers(idx):
    """子问标号「N-1」作**补充**标记（仅当该题号无题头标记时启用）。→ {qno: (q,page,y,x,w)}"""
    out = {}
    for row in idx:
        for b in row["blocks"]:
            s = b["t"].strip()
            if len(s) > 14:
                continue
            m = SUB1.match(s)
            if not m:
                continue
            n = int(m.group(1))
            if 1 <= n <= 15 and n not in out:
                out[n] = (n, row["page"], b["y"], b["x"], row["w"])
    return out


def crop_q(pdf, mks, i, dpi_out=DPI):
    """按「阅读流」裁题区：从 marker[i] 顺流到 marker[i+1]（跨栏/跨页自动切片）。
    双页跨页扫描 ⇒ 一个物理页含左右两栏；栏内 y 递减。返回 [(page, PIL.Image)]。"""
    q, p0, y0, x0, w = mks[i][:5]
    c0 = _col(x0, w)
    if i + 1 < len(mks):
        _, p1, y1, x1, _ = mks[i + 1][:5]
        c1 = _col(x1, w)
    else:
        p1, y1, c1 = 10 ** 8, 10 ** 8, 1      # 末题：顺流到文档末页右栏
    SRC = 150.0
    k = dpi_out / SRC
    doc = fitz.open(pdf)
    last = doc.page_count
    out = []
    for p in range(p0, (last if p1 > last else p1) + 1):
        pg = doc[p - 1]; Rc = pg.rect
        H_out = Rc.height * dpi_out / 72.0
        W_pt = Rc.width
        regs = []
        for c in (0, 1):
            if p == p0 and c < c0:
                continue
            if p1 <= last and p == p1 and c > c1:
                continue
            top_v = (y0 * k - 10 * k) if (p == p0 and c == c0) else 0.0
            bot_v = (y1 * k + 4 * k) if (p == p1 and c == c1 and y1 < 10 ** 8) else H_out
            if bot_v - top_v < 220:
                continue
            x_a = 16.0 if c == 0 else W_pt * 0.5 + 2
            x_b = W_pt * 0.5 - 2 if c == 0 else W_pt - 16.0
            regs.append((top_v, bot_v, x_a, x_b))
        if not regs:
            continue
        # 同页多栏 → 按原版面位置拼回一张图，再裁到实际使用范围
        top_min = min(r[0] for r in regs); bot_max = max(r[1] for r in regs)
        x_min = min(r[2] for r in regs); x_max = max(r[3] for r in regs)
        px = dpi_out / 72.0
        Wc = int(round((x_max - x_min) * px)); Hc = int(round(bot_max - top_min))
        if Wc < 40 or Hc < 80:
            continue
        canvas = Image.new("RGB", (Wc, Hc), "white")
        for top_v, bot_v, x_a, x_b in regs:
            pix = pg.get_pixmap(dpi=dpi_out,
                                clip=fitz.Rect(x_a, top_v * 72.0 / dpi_out,
                                               x_b, bot_v * 72.0 / dpi_out))
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            canvas.paste(im, (int(round((x_a - x_min) * px)), int(round(top_v - top_min))))
        out.append((p, canvas))
    doc.close()
    return q, out


def save_img(im):
    """裁图落盘为 JPEG（体积远小于 PNG；手写灰度扫描 q90 无损观感）。名字＝内容 sha256。"""
    import io
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=90, optimize=True, subsampling=0)
    data = buf.getvalue()
    h = hashlib.sha256(data).hexdigest()
    fp = os.path.join(IMGDIR, h + ".jpg")
    if not os.path.exists(fp):
        with open(fp, "wb") as f:
            f.write(data)
    return h + ".jpg"


def card_qno(path):
    m = re.search(r"题-GChO-\d+-(\d+)-", os.path.basename(path))
    return int(m.group(1)) if m else None


def _norm(s):
    s = re.sub(r"!\[\]\([^)]*\)", "", s or "")
    s = re.sub(r"\$[^$]*\$", "", s)
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", s)


def locate_by_text(idx, qtext, min_cov=0.30):
    """兜底定位：用卡题面 10-gram 覆盖率找题所在页与 y。返回 (page, y) 或 None。"""
    body = re.sub(r"^\s*#{2,4}\s*第\s*\d+\s*题[^\n]*\n", "", qtext or "", count=1)
    body = _norm(body)
    if len(body) < 24:
        return None
    seg = body[:300]
    gs = [seg[i:i + 10] for i in range(0, len(seg) - 9, 5)]
    if not gs:
        return None
    best = None
    for row in idx:
        ptxt = "".join(_norm(b["t"]) for b in row["blocks"])
        cov = sum(1 for g in gs if g in ptxt) / len(gs)
        if best is None or cov > best[0]:
            best = (cov, row["page"])
    if best is None or best[0] < min_cov:
        return None
    row = idx[best[1] - 1]
    for j in range(len(row["blocks"])):
        win = "".join(_norm(b["t"]) for b in row["blocks"][j:j + 6])
        if sum(1 for g in gs if g in win) / len(gs) >= min_cov:
            b = row["blocks"][j]
            return (best[1], b["y"], b["x"], row["w"])
    b = row["blocks"][0]
    return (best[1], b["y"], b["x"], row["w"])


def cards_of(rnd):
    """卡文件 glob：届<10 用两位补零（题-GChO-02-xx）。"""
    pats = {os.path.join(GDIR, "题-GChO-%02d-*.md" % rnd),
            os.path.join(GDIR, "题-GChO-%d-*.md" % rnd)}
    out = set()
    for pat in pats:
        out |= set(glob.glob(pat))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    rnd = a.round
    pdf = find_manuscript(rnd)
    print("届 %d 手稿：%s" % (rnd, pdf))
    if not pdf:
        print("!! 未找到手稿 PDF"); return 1
    idx = load_index(rnd, pdf)
    if idx is None:
        print("!! 缺 OCR 索引，请先: python ocr_index.py <pdf> GChO%d 150" % rnd); return 1
    mks = markers(idx, 150)
    print("题标记 %d 个：%s" % (len(mks), [(t[0], t[1], _col(t[3], t[4])) for t in mks]))
    cards = cards_of(rnd)
    print("卡 %d 张" % len(cards))
    if a.limit:
        cards = cards[:a.limit]
    os.makedirs(BK, exist_ok=True)
    aug = list(mks)
    qset = {t[0] for t in aug}
    # 兜底①：第 1 题缺标记 ⇒ 文档起始
    if 1 not in qset and any(card_qno(c) == 1 for c in cards):
        w0 = idx[0]["w"]
        aug.append((1, 1, 0.0, 0.0, w0)); qset.add(1)
        print("  [起始兜底] 届%d 第1题 → p1 页首" % rnd)
    # 兜底②：子问标号 N-1（仅当题头缺失）
    sub = sub_markers(idx)
    for c in cards:
        q = card_qno(c)
        if q is None or q in qset or q not in sub:
            continue
        aug.append(sub[q]); qset.add(q)
        print("  [子问标号] 届%d 第%d题 → p%d y%.0f x%.0f" % (rnd, q, sub[q][1], sub[q][2], sub[q][3]))
    # 兜底②：题面文本匹配
    for c in cards:
        q = card_qno(c)
        if q is None or q in qset:
            continue
        t = open(c, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
        i = t.find("## 题目"); j = t.find("## 参考答案")
        loc = locate_by_text(idx, t[i:j] if i >= 0 and j > i else "")
        if loc:
            aug.append((q, loc[0], loc[1], loc[2], loc[3])); qset.add(q)
            print("  [兜底] 届%d 第%d题 → p%d y%.0f x%.0f" % (rnd, q, loc[0], loc[1], loc[2]))
        else:
            print("  [兜底失败] 届%d 第%d题" % (rnd, q))
    aug.sort(key=lambda t: (t[1], 0 if t[3] < t[4] * 0.45 else 1, t[2]))
    plan = []
    by_q = {t[0]: i for i, t in enumerate(aug)}
    for c in cards:
        q = card_qno(c)
        if q is None or q not in by_q:
            print("  跳过（无对应题标记）:", os.path.basename(c)[:40]); continue
        qq, slices = crop_q(pdf, aug, by_q[q])
        print("  %-40s 第%d题 → %d 片 %s" % (os.path.basename(c)[:40], q, len(slices),
                                            [p for p, _ in slices]))
        plan.append((c, q, slices))
    if not a.apply:
        print("\n[dry-run] 未写盘。加 --apply 执行。")
        return 0
    # 写盘
    skipped = []
    for c, q, slices in plan:
        if not slices:                       # 保护：0 片则不改卡（避免空答案区）
            skipped.append(os.path.basename(c))
            print("  !! 0 片，跳过不改：", os.path.basename(c)[:40])
            continue
        names = [save_img(im) for _, im in slices]
        t = open(c, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
        j = t.find("## 参考答案"); k = t.find("## 知识点映射")
        if j < 0:
            print("  !! 无参考答案节:", os.path.basename(c)[:40]); continue
        if k < 0:
            k = len(t)
        # 备份原文（仅首次；保证幂等，二次运行不覆盖原始备份）
        bkf = os.path.join(BK, os.path.basename(c) + ".orig")
        if not os.path.exists(bkf):
            with open(bkf, "w", encoding="utf-8", newline="\n") as f:
                f.write(t)
        # 保留原答案区里的校勘注（provenance，不得丢）
        _orr = t[j:k] if k > j else t[j:]
        _kes = [ln.strip() for ln in _orr.split("\n") if "⛔ 校勘" in ln]
        newans = ["## 参考答案", "",
                  "📎 **答案出处**：源卷**手写解析手稿**第 %d 题（p%s）已随卡；手写笔迹，含结构式/图，"
                  "**文字化需人工转录**。组卷命中本卡时请以图为准。" % (q, "、".join(str(p) for p, _ in slices)),
                  ""]
        for n in names:
            newans += ["![](images/%s)" % n, ""]
        if _kes:
            newans += _kes + [""]
        newt = t[:j] + "\n".join(newans) + "\n" + t[k:]
        open(c, "w", encoding="utf-8", newline="\n").write(newt)
        print("  写入", os.path.basename(c)[:40], "→", len(names), "图")
    print("完成（%d 卡）" % len(plan))
    return 0


if __name__ == "__main__":
    sys.exit(main())
