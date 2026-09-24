# -*- coding: utf-8 -*-
"""PDF 可用性分诊（原生文字版 / 扫描件 / 图片讲义），用于决定「可直接转 md」还是「需 OCR」还是「只做影印索引」。

判据（可复算）：
- 原生文字版：正文层平均每页 ≥200 字符 且 汉字占比 >10% → 可直接抽文本转 md（不需 OCR）
- 疑似扫描件：平均每页 <50 字符 → 需 OCR（MinerU/paddle 等）
- 图片型讲义（板书/手写）：几乎无文本层但每页有整页图 → 需 OCR，且 OCR 后须按 B 类笔记口径复核（板书≠教材原文）

用法：
  python pdf_triage.py --dir "06-外部资料导入/bdwp 40届国初备考与质心 2026-09"
  python pdf_triage.py --file "xxx.pdf"
  python pdf_triage.py --dir ... --json out.json
需 PyMuPDF(fitz)：本机用 系统 Python 3.12。
"""
import argparse, json, os, re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HAN = re.compile(r'[\u4e00-\u9fff]')


def triage_one(path: Path):
    import fitz
    try:
        doc = fitz.open(str(path))
    except Exception as e:
        return {"file": str(path), "error": f"打开失败: {e}"}
    pages = doc.page_count
    tot_chars = 0
    tot_han = 0
    tot_imgs = 0
    sample = ""
    empty_pages = 0
    for i in range(pages):
        try:
            pg = doc.load_page(i)
            t = pg.get_text() or ""
            imgs = len(pg.get_images(full=False))
        except Exception:
            t, imgs = "", 0
        tot_chars += len(t)
        tot_han += len(HAN.findall(t))
        tot_imgs += imgs
        if len(t.strip()) < 20:
            empty_pages += 1
        if not sample and len(t.strip()) > 40:
            sample = re.sub(r'\s+', ' ', t.strip())[:90]
    doc.close()
    avg = tot_chars / pages if pages else 0
    han_ratio = (tot_han / tot_chars) if tot_chars else 0
    if avg >= 200 and han_ratio > 0.10:
        kind, action = "原生文字版", "可直接抽文本→md（不需 OCR）"
    elif avg >= 50:
        kind, action = "半文字/混合", "抽样核页面；文字页可抽，图页需 OCR"
    else:
        kind, action = "扫描/图片型", "需 OCR；OCR 后按 B 类口径复核（板书≠教材原文）"
    return {
        "file": str(path),
        "pages": pages,
        "chars": tot_chars,
        "han": tot_han,
        "avg_chars_per_page": round(avg, 1),
        "han_ratio": round(han_ratio, 2),
        "images": tot_imgs,
        "near_empty_pages": empty_pages,
        "kind": kind,
        "action": action,
        "sample": sample,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', help='目录（递归）')
    ap.add_argument('--file', help='单个 PDF')
    ap.add_argument('--json', help='导出 JSON')
    args = ap.parse_args()

    files = []
    if args.dir:
        files = sorted(Path(args.dir).rglob('*.pdf'))
    if args.file:
        files.append(Path(args.file))
    if not files:
        print('未指定 --dir/--file')
        return

    rows = [triage_one(p) for p in files]
    print(f"{'文件':52s} {'页':>4s} {'字数':>7s} {'汉字':>7s} {'均页':>6s} {'汉字比':>6s} {'图':>5s} {'判定':>12s}")
    print('-' * 118)
    for r in rows:
        if 'error' in r:
            print(f"{r['file'][:50]:52s} ERROR {r['error']}")
            continue
        print(f"{Path(r['file']).name[:50]:52s} {r['pages']:4d} {r['chars']:7d} {r['han']:7d} "
              f"{r['avg_chars_per_page']:6.1f} {r['han_ratio']:6.2f} {r['images']:5d} {r['kind']:>12s}")
    print()
    from collections import Counter
    print('判定分布:', dict(Counter(r.get('kind', 'ERROR') for r in rows)))
    print()
    for r in rows:
        if 'error' in r:
            continue
        print(f"  [{r['kind']}] {Path(r['file']).name}")
        print(f"      {r['action']}")
        if r['sample']:
            print(f"      首段: {r['sample']}")
    if args.json:
        Path(args.json).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
        print('\nJSON 已写出:', args.json)


if __name__ == '__main__':
    main()
