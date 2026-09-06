# -*- coding: utf-8 -*-
"""
阶段六补充：全库「假图片」+ 空文件 扫描

起因：EDTA 缺图破案 —— 4 个 edta-structure.jpg 其实是 LibreTexts 登录页 HTML，
后缀是 .jpg 但内容是 text/html。校验器只查「文件存在 + 后缀对得上」，
所以从不报错。这类文件既不能渲染，又是纯垃圾。

本脚本按【魔数】判定，不看后缀：
  1. 0 字节文件（全类型）
  2. 图片后缀但内容不是图片（HTML / JSON / PDF / 文本 / 其他）
"""
import os
import sys

VAULT = r"C:\Obsidion\妙妙屋"
SKIP_DIRS = {".git", "node_modules", ".obsidian", ".trash", "__pycache__"}

IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tif", ".tiff"}

MAGIC = [
    (".jpg", lambda b: b[:3] == b"\xff\xd8\xff"),
    (".jpeg", lambda b: b[:3] == b"\xff\xd8\xff"),
    (".png", lambda b: b[:8] == b"\x89PNG\r\n\x1a\n"),
    (".gif", lambda b: b[:6] in (b"GIF87a", b"GIF89a")),
    (".bmp", lambda b: b[:2] == b"BM"),
    (".webp", lambda b: b[:4] == b"RIFF" and b[8:12] == b"WEBP"),
    (".tif", lambda b: b[:4] in (b"II*\x00", b"MM\x00*")),
    (".tiff", lambda b: b[:4] in (b"II*\x00", b"MM\x00*")),
]
MAGIC_MAP = {}
for ext, fn in MAGIC:
    MAGIC_MAP.setdefault(ext, []).append(fn)


def sniff(head: bytes) -> str:
    """猜真实类型，返回人类可读标签"""
    h = head.lstrip(b"\xef\xbb\xbf")  # BOM
    low = h[:512].lower()
    if low.startswith(b"<!doctype html") or b"<html" in low[:200]:
        return "HTML"
    if low.startswith(b"<?xml") or low.startswith(b"<svg"):
        return "XML/SVG"
    if h[:1] in (b"{", b"["):
        return "JSON"
    if h[:4] == b"%PDF":
        return "PDF"
    if h[:2] == b"PK":
        return "ZIP/Office"
    if h[:5] == b"\x89PNG\r":
        return "PNG(另类魔数)"
    if h[:3] == b"\xff\xd8\xff":
        return "JPEG(偏移)"
    try:
        h.decode("utf-8")
        return "纯文本"
    except UnicodeDecodeError:
        return "未知二进制"


def main():
    empties = []
    fakes = []
    scanned = 0
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            p = os.path.join(root, fn)
            try:
                s = os.path.getsize(p)
            except OSError:
                continue
            ext = os.path.splitext(fn)[1].lower()
            if s == 0:
                empties.append((p, s))
                continue
            if ext not in MAGIC_MAP:
                continue
            scanned += 1
            try:
                with open(p, "rb") as f:
                    head = f.read(1024)
            except OSError:
                continue
            if not any(fn_(head) for fn_ in MAGIC_MAP[ext]):
                fakes.append((p, s, sniff(head)))

    print(f"扫描图片文件：{scanned}")
    print(f"\n=== A. 0 字节文件：{len(empties)} ===")
    for p, s in sorted(empties):
        print(f"  {os.path.relpath(p, VAULT)}")

    print(f"\n=== B. 假图片（后缀像图、内容不是图）：{len(fakes)} ===")
    by_kind = {}
    for p, s, kind in fakes:
        by_kind.setdefault(kind, []).append((p, s))
    for kind in sorted(by_kind, key=lambda k: -len(by_kind[k])):
        lst = by_kind[kind]
        tot = sum(s for _, s in lst)
        print(f"\n  [{kind}] {len(lst)} 个 / {tot/1024/1024:.2f} MB")
        for p, s in sorted(lst)[:40]:
            print(f"    {s/1024:8.1f} KB  {os.path.relpath(p, VAULT)}")
        if len(lst) > 40:
            print(f"    ... 另有 {len(lst)-40} 个")


if __name__ == "__main__":
    main()
