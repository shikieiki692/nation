# -*- coding: utf-8 -*-
"""把 markdown 中「独立成行」的 HTML <img src="..."/> 转成 ![](...) 语法。

背景（判据 108）：pandoc 的 markdown reader 把裸 HTML <img> 当 raw inline，
docx writer 不支持 raw HTML ⇒ **静默丢弃**，document.xml 内无任何残留、无占位、无警告。
故凡走 md→docx 管线（组卷/学生版/讲义）的卡，HTML img 等于"无图"。

安全边界（只做可证明等价的部分）：
  · 仅处理**整行只含一个 <img> 标签**（前后允许空白）的行；
  · 行内嵌图、<table> 内的 img 一律不碰（需结构重构，交人工）；
  · src 路径必须在磁盘上存在，否则跳过并报 INVALID；
  · 不改变任何文字，仅把标签换成 markdown 图片语法。

用法：
  python convert_html_img.py --list files.txt [--apply]
  python convert_html_img.py --file a.md [--apply]
"""
import io, os, re, sys, argparse

ROOT = r'C:\Obsidion\妙妙屋'
IMG_LONE = re.compile(r'^\s*<img\s+src\s*=\s*["\']([^"\']+)["\']\s*/?>\s*$', re.I)


def convert_text(text, base_dir, rel_label=''):
    """返回 (new_text, n_changed, n_invalid, details)。仅处理独立行。"""
    lines = text.split('\n')
    n_ok = n_bad = 0
    details = []
    for i, ln in enumerate(lines):
        m = IMG_LONE.match(ln)
        if not m:
            continue
        src = m.group(1)
        if src.startswith('data:'):
            n_bad += 1
            details.append('L%d INVALID(data-uri)' % (i + 1)); continue
        p = src if os.path.isabs(src) else os.path.normpath(os.path.join(base_dir, src))
        if not os.path.exists(p):
            n_bad += 1
            details.append('L%d INVALID(缺文件) %s' % (i + 1, src)); continue
        lines[i] = '![](%s)' % src
        n_ok += 1
        details.append('L%d  %s' % (i + 1, src))
    return '\n'.join(lines), n_ok, n_bad, details


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list')
    ap.add_argument('--file')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()

    paths = []
    if a.list:
        paths = [l.strip() for l in io.open(a.list, encoding='utf-8') if l.strip()]
    elif a.file:
        paths = [a.file]
    else:
        sys.exit('需要 --list 或 --file')

    tot_ok = tot_bad = 0
    for rel in paths:
        fp = rel if os.path.isabs(rel) else os.path.join(ROOT, rel)
        if not os.path.exists(fp):
            print('NOTFOUND %s' % rel); continue
        raw = io.open(fp, 'rb').read()
        bom = raw.startswith(b'\xef\xbb\xbf')
        text = raw.decode('utf-8-sig')
        crlf = '\r\n' in text
        norm = text.replace('\r\n', '\n')
        new, ok, bad, det = convert_text(norm, os.path.dirname(fp), rel)
        tot_ok += ok; tot_bad += bad
        tag = 'CONV' if ok else ('SKIP' if not bad else 'BADONLY')
        print('%-8s ok=%-3d bad=%-2d  %s' % (tag, ok, bad, os.path.basename(rel)[:66]))
        if bad:
            for d in det:
                if 'INVALID' in d:
                    print('        %s' % d)
        if ok and a.apply:
            out = new.replace('\n', '\r\n') if crlf else new
            data = out.encode('utf-8')
            if bom:
                data = b'\xef\xbb\xbf' + data
            io.open(fp, 'wb').write(data)
    print('\n合计：可转换 %d 处｜不可解析 %d 处｜%s' % (tot_ok, tot_bad, '已写入' if a.apply else 'DRY-RUN（未写入）'))


if __name__ == '__main__':
    main()
