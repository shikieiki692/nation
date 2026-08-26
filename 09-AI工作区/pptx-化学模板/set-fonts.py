# -*- coding: utf-8 -*-
"""set-fonts.py — PPTX 字体后处理：西文/数字/符号 → Times New Roman，中文保持微软雅黑。

用法（在 .venv python 下运行）：
    python set-fonts.py <input.pptx> [-o output.pptx]

- 遍历 ppt/slides/*.xml 与 ppt/notesSlides/*.xml
- 所有 <a:latin typeface="..."> 改为 Times New Roman；<a:ea> 不动（雅黑）
- 含高风险符号（⇌ 等，--fallback-chars 可配）的 run 可用 --fallback 跳过 TNR 改回雅黑
- 默认覆盖写 input；用 -o 输出到新文件
"""
import argparse
import re
import shutil
import sys
import zipfile

LATIN = 'Times New Roman'
EA = 'Microsoft YaHei'
# 经验上 Times New Roman 可能缺字形的符号（⇌ 最危险）
DEFAULT_FALLBACK_CHARS = '⇌'

TARGET_PARTS = re.compile(r'^(ppt/slides/slide\d+|ppt/notesSlides/notesSlide\d+)\.xml$')
LATIN_RE = re.compile(r'(<a:latin\b[^>]*?\btypeface=")[^"]*(")')
RUN_RE = re.compile(r'<a:r>.*?</a:r>', re.S)
TEXT_RE = re.compile(r'<a:t>(.*?)</a:t>', re.S)


def process_xml(xml: str, fallback_chars: str) -> tuple[str, int]:
    """返回 (新 xml, 修改的 latin 数)。"""
    if fallback_chars:
        risky = set(fallback_chars)

        def fix_run(m):
            block = m.group(0)
            t = TEXT_RE.search(block)
            if t and any(c in risky for c in t.group(1)):
                return block  # 含高风险符号的 run 保持雅黑
            return LATIN_RE.sub(r'\g<1>%s\g<2>' % LATIN, block)

        # 只处理 run 内部；run 外残留的 a:latin（如 defRPr）也统一处理
        out_parts, last, n = [], 0, 0
        for m in RUN_RE.finditer(xml):
            seg = xml[last:m.start()]
            seg, k = LATIN_RE.subn(r'\g<1>%s\g<2>' % LATIN, seg)
            n += k
            blk = fix_run(m)
            n += len(LATIN_RE.findall(m.group(0))) - len(LATIN_RE.findall(blk))
            out_parts.append(seg)
            out_parts.append(blk)
            last = m.end()
        tail, k = LATIN_RE.subn(r'\g<1>%s\g<2>' % LATIN, xml[last:])
        n += k
        out_parts.append(tail)
        return ''.join(out_parts), n
    else:
        return LATIN_RE.subn(r'\g<1>%s\g<2>' % LATIN, xml)


def main():
    ap = argparse.ArgumentParser(description='PPTX 西文字体统一为 Times New Roman')
    ap.add_argument('input', help='输入 pptx 路径')
    ap.add_argument('-o', '--output', help='输出路径（默认覆盖输入）')
    ap.add_argument('--fallback', action='store_true',
                    help='含高风险符号的 run 保持微软雅黑（防止豆腐块）')
    ap.add_argument('--fallback-chars', default=DEFAULT_FALLBACK_CHARS,
                    help='高风险符号集合，默认 ⇌')
    args = ap.parse_args()

    out = args.output or args.input
    if out != args.input:
        shutil.copyfile(args.input, out)

    zin = zipfile.ZipFile(args.input)
    items = []
    total = 0
    for info in zin.infolist():
        data = zin.read(info.filename)
        if TARGET_PARTS.match(info.filename):
            xml = data.decode('utf-8')
            xml, n = process_xml(xml, args.fallback_chars if args.fallback else '')
            if n:
                data = xml.encode('utf-8')
                print(f'{info.filename}: {n} 处 latin → {LATIN}')
                total += n
        items.append((info, data))
    zin.close()

    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info, data in items:
            zout.writestr(info, data)
    print(f'共修改 {total} 处；输出：{out}')
    if not args.fallback:
        print('提示：若特殊符号渲染为豆腐块，加 --fallback 重跑')
    return 0


if __name__ == '__main__':
    sys.exit(main())
