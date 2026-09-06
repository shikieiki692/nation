#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为「图片缺失」清单寻找可救援的副本，来源两处：
  1. 回收站（$I/$R 配对，解析 $I 元数据拿原始路径）
  2. git 历史（--diff-filter=D 列出所有被删过的路径，blob 仍可取回）

只做检索与报告，不写任何文件。

回收站 $I 布局（本机 version=2，实测）：
  0x00 uint32 版本(2)
  0x08 uint64 文件大小
  0x10 FILETIME 删除时间
  0x18 uint32 原始路径字符数
  0x1C       原始路径 UTF-16LE
注意网上流传的 0x14/0x18 是旧版(version=1)布局，本机会解析出乱码。
"""
import collections
import json
import os
import re
import struct
import subprocess
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.join(VAULT, ".workbuddy", "tmp")
REPORT = os.path.join(VAULT, "09-审计报告", "auto-validation", "2026-09-01-validation.md")

OFF_LEN = 0x18
OFF_PATH = 0x1C

RE_LINE = re.compile(
    r"^\s*-\s+`([^`]+)`\s*→\s*!\[\[([^\]\|#\^]+?)\]\]\s*→\s*文件不存在\s*$")


def parse_missing():
    """从校验报告里解析「图片缺失」章节"""
    out = []
    in_sec = False
    for ln in open(REPORT, encoding="utf-8"):
        if ln.startswith("**图片缺失**"):
            in_sec = True
            continue
        if in_sec:
            if ln.startswith("**") and "图片缺失" not in ln:
                break
            m = RE_LINE.match(ln.rstrip("\n"))
            if m:
                out.append((m.group(1), m.group(2)))
    return out


def bin_index():
    """回收站索引: basename -> [(原始路径, $R 路径, 大小)]"""
    idx = collections.defaultdict(list)
    n = 0
    for drv in "CDEFGH":
        root = drv + ":\\$Recycle.Bin"
        if not os.path.isdir(root):
            continue
        for d in os.listdir(root):
            sid = os.path.join(root, d)
            if not os.path.isdir(sid):
                continue
            try:
                names = os.listdir(sid)
            except OSError:
                continue
            for fn in names:
                if not fn.startswith("$I"):
                    continue
                ip = os.path.join(sid, fn)
                rp = os.path.join(sid, "$R" + fn[2:])
                try:
                    with open(ip, "rb") as f:
                        blob = f.read(OFF_PATH + 2)
                    if len(blob) < OFF_PATH + 2:
                        continue
                    clen = struct.unpack_from("<I", blob, OFF_LEN)[0]
                    if not (0 < clen < 4096):
                        continue
                    with open(ip, "rb") as f:
                        raw = f.read(OFF_PATH + clen * 2)
                    orig = raw[OFF_PATH:OFF_PATH + clen * 2].decode("utf-16-le",
                                                                    errors="ignore").rstrip("\x00")
                except OSError:
                    continue
                if not orig or not os.path.isfile(rp):
                    continue
                size = os.path.getsize(rp)
                idx[os.path.basename(orig)].append((orig, rp, size))
                n += 1
    return idx, n


def git_index():
    """git 历史索引: basename -> [(路径, 删除它的 commit)]"""
    idx = collections.defaultdict(list)
    r = subprocess.run(
        ["git", "-c", "core.quotepath=false", "log", "--all",
         "--diff-filter=D", "--name-only", "--pretty=format:__C__%H"],
        cwd=VAULT, capture_output=True)
    txt = r.stdout.decode("utf-8", errors="ignore")
    cur = None
    for ln in txt.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        if ln.startswith("__C__"):
            cur = ln[5:]
            continue
        if cur:
            idx[os.path.basename(ln)].append((ln, cur))
    return idx


def main():
    missing = parse_missing()
    print(f"校验报告里的图片缺失: {len(missing)} 处")

    names = collections.Counter()
    for _src, img in missing:
        names[img.replace("\\", "/").split("/")[-1].strip()] += 1
    print(f"去重后唯一文件名: {len(names)} 个")

    print("\n[1/2] 扫描回收站 …")
    bidx, bn = bin_index()
    print(f"      回收站条目 {bn:,} 条")

    print("[2/2] 扫描 git 历史删除记录 …")
    gidx = git_index()
    print(f"      历史删除路径 {sum(len(v) for v in gidx.values()):,} 条，"
          f"唯一文件名 {len(gidx):,} 个")

    from_bin, from_git, nowhere = [], [], []
    for name, cnt in names.items():
        b = bidx.get(name)
        g = gidx.get(name)
        if b:
            from_bin.append((name, cnt, b))
        elif g:
            from_git.append((name, cnt, g))
        else:
            nowhere.append((name, cnt))

    tot = lambda xs: sum(c for _n, c, _v in xs)
    print(f"\n==== 可救援分析 ====")
    print(f"  回收站里有副本 : {len(from_bin):4} 个名字 / {tot(from_bin):4} 处引用")
    print(f"  git 历史里有   : {len(from_git):4} 个名字 / {tot(from_git):4} 处引用")
    print(f"  两处都没有     : {len(nowhere):4} 个名字 / {sum(c for _n, c in nowhere):4} 处引用")

    print(f"\n---- 回收站可救（前 20）----")
    for name, cnt, hits in from_bin[:20]:
        print(f"  {cnt:3}处  {name[:46]:48} 原路径 {hits[0][0][:60]}")

    print(f"\n---- git 历史可救（前 20）----")
    for name, cnt, hits in from_git[:20]:
        print(f"  {cnt:3}处  {name[:46]:48} 曾位于 {hits[0][0][:60]}")

    print(f"\n---- 彻底无望（前 15）----")
    for name, cnt in nowhere[:15]:
        print(f"  {cnt:3}处  {name[:60]}")

    out = {
        "missing": [{"src": s, "img": i} for s, i in missing],
        "from_bin": [{"name": n, "refs": c,
                      "orig": h[0][0], "rpath": h[0][1], "size": h[0][2]}
                     for n, c, h in from_bin],
        "from_git": [{"name": n, "refs": c, "path": h[0][0], "commit": h[0][1]}
                     for n, c, h in from_git],
        "nowhere": [{"name": n, "refs": c} for n, c in nowhere],
    }
    with open(os.path.join(TMP, "recoverable_imgs.json"), "w",
              encoding="utf-8", newline="") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"\n明细已写入 .workbuddy/tmp/recoverable_imgs.json")


if __name__ == "__main__":
    main()
