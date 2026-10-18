# -*- coding: utf-8 -*-
"""tag_cs_generic.py —— 给题卡 frontmatter 补 consumption_status（标注类 FM，只插入不替换）。

用法：
    python tag_cs_generic.py --value 隔离 --list <清单.txt> [--apply]

插入位置遵循库内惯例（cs 在前 315 : cs 在后 30）：
    优先插在 question_image_status 之前；无该字段时插在 status 之后。
幂等：已有 consumption_status 即跳过。保留原行尾（CRLF/LF）与 BOM 之外的字节不变。
"""
import io
import os
import re
import sys

ROOT = r"C:\Obsidion\妙妙屋"
KEY = "consumption_status"


def fm_bounds(lines):
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return 0, i
    return None


def parse_args(argv):
    val = lst = None
    apply_ = "--apply" in argv
    i = 1
    while i < len(argv):
        if argv[i] == "--value":
            val = argv[i + 1]; i += 2
        elif argv[i] == "--list":
            lst = argv[i + 1]; i += 2
        else:
            i += 1
    if not val or not lst:
        print("用法: --value <值> --list <清单> [--apply]")
        sys.exit(2)
    return val, lst, apply_


def find_anchor(fm):
    """返回 (插入行下标, 说明)。插在返回下标之前。"""
    for key, mode in (("question_image_status", "before"), ("status", "after")):
        pat = re.compile(r"^" + key + r"\s*:")
        hits = [i for i, ln in enumerate(fm) if pat.match(ln)]
        if hits:
            return (hits[-1] if mode == "before" else hits[-1] + 1), key + "/" + mode
    return None, None


def main():
    val, lst, apply_ = parse_args(sys.argv)
    with io.open(lst, encoding="utf-8") as f:
        paths = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

    n_ok = n_skip = n_bad = 0
    for p in paths:
        fp = os.path.join(ROOT, p)
        name = os.path.basename(p)
        if not os.path.exists(fp):
            print("[SKIP:NOTFOUND] %s" % name); n_bad += 1; continue
        raw = open(fp, "rb").read()
        bom = raw.startswith(b"\xef\xbb\xbf")
        nl = "\r\n" if b"\r\n" in raw else "\n"
        text = raw.decode("utf-8-sig")
        lines = text.split(nl)
        b = fm_bounds(lines)
        if b is None:
            print("[SKIP:NO_FM] %s" % name); n_bad += 1; continue
        s, e = b
        fm = lines[s + 1:e]
        if any(re.match(r"^" + KEY + r"\s*:", ln) for ln in fm):
            print("[SKIP:EXISTS] %s" % name); n_skip += 1; continue
        idx, how = find_anchor(fm)
        if idx is None:
            print("[SKIP:NO_ANCHOR] %s" % name); n_bad += 1; continue
        at = s + 1 + idx
        new_lines = lines[:at] + [KEY + ": " + val] + lines[at:]
        if apply_:
            out = nl.join(new_lines)
            with io.open(fp, "w", encoding="utf-8", newline="") as f:
                f.write(("\ufeff" if bom else "") + out)
        print("[%s] %-42s 插于 %-22s CRLF=%s" % ("APPLY" if apply_ else "DRYRUN",
                                                name[:42], how, b"\r\n" in raw))
        n_ok += 1
    print("\n写/计划 %d，跳过(已存在) %d，异常 %d" % (n_ok, n_skip, n_bad))


if __name__ == "__main__":
    main()
