#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全库图片引用「真缺失」精确核查 v2
--------------------------------
v1 的缺陷：只做 4 路路径解析（相对 / 根兜底 / 剥 ../ / 挂 03-知识点），
           没有建立全库 basename 索引，所以把所有"路径指错但文件其实还在"的情况
           一律判成"真缺失（脚本无法修复）"。
v2 补上这一层：解析失败后，再用 basename 在全库图片文件索引里找。

分类：
  R1  路径直接命中（相对）
  R2  vault 根兜底命中
  R3  basename 全库唯一命中        -> 可机械修复（重写路径）
  R4  basename 全库多处命中        -> 需就近/人工判定（本脚本给候选，不自动改）
  R5  basename 全库不存在          -> 真缺失（资产本身没有）
  NOISE 占位示例 / 归档快照

只读，不修改任何文件。输出 JSON 明细到 .workbuddy/tmp/missing_img_v2.json
"""
import os, re, json, sys, collections

VAULT = r"C:\Obsidion\妙妙屋"
OUT = os.path.join(VAULT, ".workbuddy", "tmp", "missing_img_v2.json")

SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__", ".workbuddy"}
IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp", ".tif", ".tiff"}

# 归档/备份：历史快照，不修
ARCHIVE = re.compile(r"(_归档|_archive|[/\\]archive|[/\\]备份|备份[/\\]|[/\\]old[/\\]|_old[/\\]|\.bak)", re.I)
# 占位示例噪音
PLACEHOLDER = re.compile(
    r"^(<[^>]*>|xxx?\.[a-z]{3,4}|yyy?\.[a-z]{3,4}|path|图片\.jpg|image\.png|示例.*|.*示例|"
    r"[0-9a-f]{0,8}\.\.\.[0-9a-f]{0,8}\.jpg|hash\.jpg|name\.jpg|file\.jpg)$", re.I
)
# 64 位哈希名（真实资产，绝不是占位）
HASHNAME = re.compile(r"^[0-9a-f]{32,64}$", re.I)

MDIMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")     # ![alt](path)
WIKIIMG = re.compile(r"!\[\[([^\]\|#]+)(?:\|([^\]]*))?\]\]")  # ![[name|alias]]


def is_probably_placeholder(basename):
    if HASHNAME.match(os.path.splitext(basename)[0]):
        return False          # 64 位哈希一律算真实资产
    return bool(PLACEHOLDER.match(basename))


def build_file_index():
    """全库图片文件 basename -> [相对路径]"""
    idx = collections.defaultdict(list)
    total = 0
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if os.path.splitext(fn)[1].lower() in IMG_EXT:
                total += 1
                idx[fn].append(os.path.relpath(os.path.join(root, fn), VAULT))
    for k in idx:
        idx[k].sort()
    return idx, total


def resolve(raw, md_dir):
    """返回 (命中绝对路径 or None, 方式)"""
    raw = raw.strip()
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", raw):
        return None, "EXTLINK"
    p = os.path.normpath(os.path.join(md_dir, raw))
    if os.path.isfile(p):
        return p, "R1_rel"
    p2 = os.path.normpath(os.path.join(VAULT, raw))
    if os.path.isfile(p2):
        return p2, "R2_root"
    return None, None


def main():
    idx, total_imgs = build_file_index()
    print("[index] 全库图片文件 %d 个，去重 basename %d 个" % (total_imgs, len(idx)), file=sys.stderr)

    stats = collections.Counter()
    unresolved = []          # R3 / R4 / R5
    noise = []

    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.lower().endswith(".md"):
                continue
            abspath = os.path.join(root, fn)
            rel = os.path.relpath(abspath, VAULT)
            try:
                text = open(abspath, encoding="utf-8").read()
            except Exception:
                continue

            items = []
            for m in MDIMG.finditer(text):
                items.append(("md", m.group(2).strip(), m.group(0), m.start()))
            for m in WIKIIMG.finditer(text):
                items.append(("wiki", m.group(1).strip(), m.group(0), m.start()))

            for kind, raw, whole, pos in items:
                if not raw:
                    continue

                # wiki 语法：Obsidian 按 basename 全库匹配，命中即视为正常显示
                if kind == "wiki":
                    base0 = os.path.basename(raw.replace("\\", "/").split("/")[-1])
                    if idx.get(base0):
                        stats["W_OK_basename_found"] += 1
                        continue
                    # 落在媒体仓库也算正常
                    if os.path.isfile(os.path.join(VAULT, "媒体仓库", base0)):
                        stats["W_OK_basename_found"] += 1
                        continue

                hit, how = resolve(raw, root)
                if how == "EXTLINK":
                    stats["EXTLINK"] += 1
                    continue
                if hit:
                    stats[how] += 1
                    continue

                # 解析失败
                base = os.path.basename(raw.replace("\\", "/").split("/")[-1])
                if is_probably_placeholder(base):
                    stats["NOISE_PLACEHOLDER"] += 1
                    noise.append({"file": rel, "kind": kind, "raw": raw, "why": "placeholder"})
                    continue
                if ARCHIVE.search(rel):
                    stats["NOISE_ARCHIVE"] += 1
                    noise.append({"file": rel, "kind": kind, "raw": raw, "why": "archive"})
                    continue

                cands = idx.get(base, [])
                line = text.count("\n", 0, pos) + 1
                rec = {
                    "file": rel, "line": line, "kind": kind,
                    "raw": raw, "basename": base,
                    "candidates": cands[:6], "n_cands": len(cands),
                }
                if len(cands) == 1:
                    stats["R3_unique_basename"] += 1
                    rec["cls"] = "R3"
                elif len(cands) > 1:
                    stats["R4_multi_basename"] += 1
                    rec["cls"] = "R4"
                else:
                    stats["R5_truly_missing"] += 1
                    rec["cls"] = "R5"
                # 按语法再分一层
                stats[("R3" if len(cands) == 1 else "R4" if len(cands) else "R5") + "_" + kind] += 1
                unresolved.append(rec)

    total_refs = sum(stats[k] for k in ["R1_rel", "R2_root", "R3_unique_basename",
                                        "R4_multi_basename", "R5_truly_missing",
                                        "NOISE_PLACEHOLDER", "NOISE_ARCHIVE", "EXTLINK",
                                        "W_OK_basename_found"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"stats": dict(stats), "unresolved": unresolved, "noise": noise,
               "total_refs": total_refs, "total_img_files": total_imgs},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("\n引用总数 %d\n" % total_refs)
    order = ["R1_rel", "R2_root", "W_OK_basename_found",
             "R3_unique_basename", "R4_multi_basename", "R5_truly_missing",
             "NOISE_PLACEHOLDER", "NOISE_ARCHIVE", "EXTLINK",
             "R3_md", "R3_wiki", "R4_md", "R4_wiki", "R5_md", "R5_wiki"]
    for k in order:
        if stats.get(k):
            print("  %-22s %6d" % (k, stats[k]))
    print("\n明细 -> %s" % OUT)


if __name__ == "__main__":
    main()
