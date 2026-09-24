# -*- coding: utf-8 -*-
"""把「原生文字版」PDF 的文字层抽成 md（不做 OCR），供线索/A 级延伸源使用。
- 逐页抽文本，保留 `## 第 N 页（原 PDF pN）` 便于回查
- 只做保守清洗：去「扫描全能王 创建」类水印行、压空白，**不改内容、不校 OCR 噪声**
- 写 FM：标注 source_pdf / pages / nature=待核验 / 明确「不得作概念定义基准」
"""
import sys, io, re, argparse
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import fitz

WATER = re.compile(r'^(扫描全能王\s*创建|CamScanner|Created by|第\s*\d+\s*页\s*$|xzy)', re.I)
OUT_DIR = Path(r"C:\Obsidion\妙妙屋\06-外部资料导入\40届备考-已抽文本")


def clean_page(t: str) -> str:
    lines = []
    for ln in t.splitlines():
        s = ln.strip()
        if not s:
            continue
        if WATER.match(s) and len(s) <= 24:
            continue
        lines.append(s)
    return '\n'.join(lines)


def build(pdf: Path, title: str, nature: str, tags: list, note: str) -> str:
    doc = fitz.open(str(pdf))
    pages = doc.page_count
    body = []
    for i in range(pages):
        t = clean_page(doc.load_page(i).get_text() or "")
        body.append(f"## 第 {i+1} 页（原 PDF p{i+1}）\n\n{t if t else '（本页无可抽取文本，疑为整页图 → 需 OCR）'}\n")
    doc.close()
    rel = str(pdf.relative_to(Path(r"C:\Obsidion\妙妙屋"))).replace('\\', '/')
    fm = f"""---
title: "{title}"
type: 教辅线索
source_pdf: "{rel}"
pages: {pages}
nature: "{nature}"
grade: A（延伸源·题型与解法视角）｜⛔ 不得作为概念定义的基准源（基准仍走教材原文）
ocr_status: 原生文字层（未 OCR）；含 OCR 噪声，需人工核验后引用
syllabus_codes: []
created: 2026-09-25
updated: 2026-09-25
tags: [40届备考, 教辅, 线索源, {', '.join(tags)}]
related:
  - "[[11-模板/教材选用与内容编排规范]]"
  - "[[11-模板/讲义生产流程与质量评判总纲]]"
---

# {title}

> **来源**：`{rel}`（{pages} 页，PDF 原生文字层抽取，**未经 OCR、未校核**）
> **用法**：① 题型与解法视角（对应讲义的「真题实战／推断信号」）② 考点清单补漏 ③ 可独立作答的题→题库化
> **禁止**：不得据此写概念定义／数值基准；引用前须人工核验该段可读性。
> {note}

"""
    return fm + '\n'.join(body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--nature', default='教辅讲义（课堂板书/题型总结）')
    ap.add_argument('--tags', default='')
    ap.add_argument('--note', default='')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    pdf = Path(args.pdf).resolve()
    md = build(pdf, args.title, args.nature, [t for t in args.tags.split(',') if t], args.note)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / args.out
    out.write_text(md, encoding='utf-8')
    print('已写出:', out, '| 字数:', len(md))


if __name__ == '__main__':
    main()
