# -*- coding: utf-8 -*-
"""locate_source_pdf.py —— 机构题卡「回源定位器」
用途：给一张(或一批)机构题卡，定位它的**原 PDF** 并找到**该题所在页码**，
      用于「对照原 PDF 核验 题目/图片/答案」这条硬流程。

用法：
  python -X utf8 locate_source_pdf.py <卡路径|卡所在目录> [<卡路径> ...]
  python -X utf8 locate_source_pdf.py 04-题库/2026机构初赛模拟题/清北营      # 整个机构目录
  python -X utf8 locate_source_pdf.py <卡路径> --dump png                   # 顺带把命中页渲染成 png 存 .workbuddy/tmp/opt_pipe/locate_out/

定位原理（实测 4032 卡）：
  L0 同名直中 62.3% / L1 归一化 11.9% / L2 模糊 0.4% ⇒ 合计 74.6% 自动可达。
  余下 25.4% 集中在 chemy 第32~38届「题目合集」等合并本（无同名 PDF），需人工在
  06-外部资料导入/OCR/ 下按机构目录翻（见交接文档 §机构→目录映射表）。
"""
import os, re, sys, json, difflib, glob

ROOT = r"C:\Obsidion\妙妙屋"
OCR = os.path.join(ROOT, "06-外部资料导入", "OCR")
OUT = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "locate_out")
FM_SF = re.compile(r'^source_file:[ \t]*(.*?)[ \t]*$', re.M)


def norm(s):
    s = s.lower().replace("（", "(").replace("）", ")").replace("，", ",").replace("：", ":")
    s = re.sub(r"[_\- ]?\d+$", "", s)
    s = re.sub(r"已优化|参考答案|答案版|答案|解析|试题|试卷|题目|合集|讲稿|讲义|文字版|v\d+(\.\d+)*", "", s)
    return re.sub(r"[\s_\-\.·、,，:：()（）\[\]【】<>《》/\\'\"+]", "", s)


def build_index():
    idx, nidx = {}, {}
    for dp, _, fs in os.walk(OCR):
        for f in fs:
            if f.lower().endswith(".pdf"):
                b = os.path.splitext(f)[0]
                idx.setdefault(b, os.path.join(dp, f))
                nidx.setdefault(norm(b), os.path.join(dp, f))
    return idx, nidx


def norm_pdf_index():
    """全 OCR 目录（含 01-题目 之外的 chemy试题 等）——用宽口径，提高可达率。"""
    idx, nidx = {}, {}
    for dp, _, fs in os.walk(OCR):
        for f in fs:
            if f.lower().endswith(".pdf"):
                b = os.path.splitext(f)[0]
                idx.setdefault(b, os.path.join(dp, f))
                nidx.setdefault(norm(b), os.path.join(dp, f))
    return idx, nidx, list(nidx.keys())


def get_source_file(card_path):
    head = open(card_path, encoding="utf-8-sig").read(3000)
    m = FM_SF.search(head)
    return (m.group(1).strip().strip('"').strip("'") if m else "")


def get_question_text(card_path):
    """取 ## 题目 段的正文纯文本（剥 LaTeX/图片/标题标记）。"""
    txt = open(card_path, encoding="utf-8-sig").read()
    m = re.search(r"^##[ \t]*题目[ \t]*\n(.*?)(?=^##[ \t]*参考答案|^##[ \t]*答案|\Z)",
                  txt, re.S | re.M)
    body = m.group(1) if m else txt
    body = re.sub(r"!\[\[?[^\]]*\]?\]", " ", body)
    body = re.sub(r"\$\$.*?\$\$", " ", body, flags=re.S)
    body = re.sub(r"\$[^$]*\$", " ", body)
    body = re.sub(r"\\[a-zA-Z]+", " ", body)
    body = re.sub(r"^#{1,6}.*$", " ", body, flags=re.M)
    body = re.sub(r"[^\u4e00-\u9fff]", "", body)      # 只留汉字
    return body


def locate_pdf(sf, idx, nidx, keys):
    base = os.path.splitext(os.path.basename(sf))[0]
    if idx.get(base):
        return idx[base], "L0"
    nb = norm(base)
    if nidx.get(nb):
        return nidx[nb], "L1"
    c = difflib.get_close_matches(nb, keys, n=1, cutoff=0.86)
    if c:
        return nidx[c[0]], "L2"
    return None, "MISS"


def find_pages(pdf, qtext, min_win=8):
    """在 PDF 里搜题面汉字串，返回命中页(1-based,去重) + 是否有文字层。"""
    import fitz
    hit, has_text = [], False
    with fitz.open(pdf) as d:
        pages = [d[i].get_text() for i in range(d.page_count)]
    full = "\n".join(pages)
    has_text = len(full.strip()) > 80
    if not has_text:
        return [], False
    for w in (14, 12, 10, min_win):
        if len(qtext) < w:
            continue
        key = qtext[:w]
        if key in full:
            for i, t in enumerate(pages):
                if key in t:
                    hit.append(i + 1)
            return hit, True
    # 退一步：用中间片段
    for start in (10, 20, 30):
        if len(qtext) > start + 12:
            key = qtext[start:start + 12]
            for i, t in enumerate(pages):
                if key in t:
                    hit.append(i + 1)
            if hit:
                return hit, True
    return [], True


def render_page(pdf, pno, tag):
    import fitz
    os.makedirs(OUT, exist_ok=True)
    with fitz.open(pdf) as d:
        p = d[pno - 1]
        pix = p.get_pixmap(dpi=140)
        fp = os.path.join(OUT, f"{tag}_p{pno}.png")
        pix.save(fp)
        return fp


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dump = "--dump" in sys.argv
    cards = []
    for a in args:
        p = a if os.path.isabs(a) else os.path.join(ROOT, a)
        if os.path.isdir(p):
            cards += sorted(glob.glob(os.path.join(p, "题-*.md")))
        elif p.endswith(".md"):
            cards.append(p)
    if not cards:
        print(__doc__); return
    idx, nidx, keys = norm_pdf_index()
    stats = {"L0": 0, "L1": 0, "L2": 0, "MISS": 0}
    rows = []
    for cp in cards:
        sf = get_source_file(cp)
        pdf, way = locate_pdf(sf, idx, nidx, keys)
        stats[way] += 1
        pages, has_text = ([], False) if not pdf else find_pages(pdf, get_question_text(cp))
        rows.append({"card": os.path.relpath(cp, ROOT), "source_file": sf, "way": way,
                     "pdf": os.path.relpath(pdf, ROOT) if pdf else "", "pages": pages,
                     "text_layer": has_text})
        tag = os.path.basename(cp)[2:22]
        print(f"[{way:>4}] {os.path.basename(cp)[:34]:<36} -> "
              f"{(os.path.relpath(pdf, OCR) if pdf else '(找不到原PDF，需人工)')}")
        if pdf:
            print(f"        文字层={'有' if has_text else '无(扫描件)'}  命中页={pages or '未自动命中(按页人工翻)'}")
            if dump and pages:
                for pn in pages[:2]:
                    print("        渲染:", os.path.relpath(render_page(pdf, pn, tag), ROOT))
    n = len(cards)
    print(f"\n★ {n} 卡：L0={stats['L0']} L1={stats['L1']} L2={stats['L2']} 不可达={stats['MISS']} "
          f"⇒ 自动可达 {(n-stats['MISS'])/n*100:.0f}%")
    json.dump(rows, open(os.path.join(os.path.dirname(__file__), "locate_source_pdf.json"), "w",
                         encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
