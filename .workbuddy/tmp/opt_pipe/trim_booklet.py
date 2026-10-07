#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trim_booklet.py —— 16 张「整本答案册随卡」卡：OCR 其现有页图，只保留含本卡题号的页。
判据：页文字含 `第N题`（本卡题号），或含 ≥2 处 `N-K` 小问标号且不含 `第(N+1)题`。
用法：python trim_booklet.py [--apply]
"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")
CACHE = os.path.join(R, ".workbuddy/tmp/opt_pipe/ocr_loc/_pageimg.json")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/booklet_backup")
os.makedirs(BK, exist_ok=True)


def collect():
    out = []
    for p in sorted(glob.glob(os.path.join(BASE, "**", "题-*.md"), recursive=True)):
        if "质心GChO" in p:
            continue
        t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
        j = t.find("## 参考答案"); k = t.find("## 知识点映射")
        a = t[j:k] if j > 0 and k > j else ""
        if re.search(r"全部\s*\d+\s*页已随卡", a):
            m = re.search(r"题-[A-Za-z0-9]+-\d+-(\d+)-", os.path.basename(p))
            out.append((p, int(m.group(1)) if m else None, os.path.dirname(p)))
    return out


def main():
    apply = "--apply" in sys.argv
    cards = collect()
    print("整本册卡 %d 张" % len(cards))
    cache = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}
    ocr = None
    for p, qn, d in cards:
        t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
        j = t.find("## 参考答案"); k = t.find("## 知识点映射")
        a = t[j:k]
        imgs = re.findall(r"!\[\]\(images/([^)]+)\)", a)
        if not imgs or qn is None:
            print("  跳过", os.path.basename(p)[:40]); continue
        keep = []
        for idx, n in enumerate(imgs):
            fp = os.path.join(d, "images", n)
            if not os.path.exists(fp):
                continue
            if fp not in cache:
                if ocr is None:
                    from rapidocr_onnxruntime import RapidOCR
                    ocr = RapidOCR()
                res, _ = ocr(fp)
                cache[fp] = "".join(t2 for _, t2, _ in (res or []))
            txt = cache[fp]
            flat = txt.replace(" ", "")
            if re.search(r"第%s题" % qn, flat):
                keep.append((idx, n, "第%d题" % qn)); continue
            sub = len(re.findall(r"(?<!\d)%d\s*[-－]\s*\d" % qn, flat))
            nxt = bool(re.search(r"第(%d|%d|%d)题" % (qn + 1, qn + 2, qn + 3), flat)) if qn else False
            if sub >= 2 and not nxt:
                keep.append((idx, n, "%d-K ×%d" % (qn, sub)))
        json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
        print("  %-42s 题%d  原%-3d 图 → 保留 %d：%s" % (os.path.basename(p)[:42], qn, len(imgs),
                                                      len(keep), [x[2] for x in keep][:4]))
        if not keep:
            continue
        if apply:
            bkf = os.path.join(BK, os.path.basename(p) + ".orig")
            if not os.path.exists(bkf):
                open(bkf, "w", encoding="utf-8", newline="\n").write(t)
            head = re.sub(r"(📎[^\n]*全部\s*\d+\s*页已随卡[^\n]*)",
                          "📎 **答案出处**：源答案册第 %d 题所在页（已定位，见下）；" % qn, a, count=1)
            head = re.sub(r"全部\s*\d+\s*页已随卡（见下[^）]*）", "已定位到本卡题号所在页", head)
            newimgs = "".join("![](images/%s)\n\n" % n for _, n, _ in keep)
            body = head.split("![](")[0].rstrip() + "\n\n" + newimgs
            open(p, "w", encoding="utf-8", newline="\n").write(t[:j] + body + t[k:])
    print("完成" if apply else "（dry-run）")


if __name__ == "__main__":
    main()
