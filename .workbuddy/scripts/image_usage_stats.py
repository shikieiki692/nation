#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
全库图片利用率统计 —— 找出可清理的图（孤儿图 / 内容重复图）

统计口径
  引用源：全库 .md / .canvas / .base 文本（Obsidian 按 basename 解析 ![[x.jpg]]）
  孤儿图：basename 从未在任何引用源出现过的图片文件
  重复图：内容 sha256 相同的图片组（组内保留 1 张，其余可删）

用法
  python image_usage_stats.py               # 孤儿统计（快）
  python image_usage_stats.py --deep        # 追加内容哈希去重统计（慢，需读全库图片）
输出
  .workbuddy/tmp/image_usage.json
"""
import os, re, sys, json, hashlib, collections

VAULT = r"C:\Obsidion\妙妙屋"
OUT = os.path.join(VAULT, ".workbuddy", "tmp", "image_usage.json")
DEEP = "--deep" in sys.argv

IMG_EXT = (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp", ".tif", ".tiff")
TXT_EXT = (".md", ".canvas", ".base")

# 图片清单：这些目录不参与统计，也就【不会成为删除候选】
SKIP_DIRS = {".git", ".workbuddy", "node_modules", ".obsidian", "__pycache__",
             ".trash", "_归档", "_archive", "备份"}

# 引用扫描：范围【更宽】——归档/备份目录里的 md 也会引用图片，
# 不扫它们的引用会把在用图片误判成孤儿（2026-09-01 阶段2 误删 110 张，即此坑）。
REF_SKIP_DIRS = {".git", ".workbuddy", "node_modules", ".obsidian", "__pycache__", ".trash"}

# 引用提取
# ① 双括号必须同时覆盖 ![[x]] 与 [[x]]：后者大量出现在 YAML frontmatter 的
#    key_images: ["[[media/xxx.jpg]]"] 里，validate_kb.py 也认这种写法。
RE_WIKI = re.compile(r"\[\[([^\]\|#\^]+)")
RE_MDIMG = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
RE_HTMLIMG = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.I)
# ② canvas 是 JSON，图片写在 {"type":"file","file":"xxx.jpg"} 里，上面三个正则都抓不到
RE_CANVAS = re.compile(r'"file"\s*:\s*"([^"]+)"')


def walk_files():
    imgs, txts = [], []
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in REF_SKIP_DIRS]
        for f in files:
            p = os.path.join(root, f)
            low = f.lower()
            if low.endswith(IMG_EXT):
                # 归档/备份目录内的图片只登记、不作为删除候选
                if not any(part in SKIP_DIRS for part in os.path.relpath(p, VAULT).split(os.sep)):
                    imgs.append(p)
            elif low.endswith(TXT_EXT):
                txts.append(p)
    return imgs, txts


def collect_refs(txts):
    """返回 (ref_basenames, per_file_refcount)"""
    refs = set()
    per_file = {}
    for p in txts:
        try:
            t = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        got = set()
        for m in RE_WIKI.finditer(t):
            got.add(m.group(1).strip().replace("\\", "/").split("/")[-1])
        for m in RE_MDIMG.finditer(t):
            v = m.group(1).strip()
            if v.startswith(("http://", "https://", "data:")):
                continue
            got.add(v.replace("\\", "/").split("/")[-1])
        for m in RE_HTMLIMG.finditer(t):
            v = m.group(1).strip()
            if v.startswith(("http://", "https://", "data:")):
                continue
            got.add(v.replace("\\", "/").split("/")[-1])
        if p.lower().endswith(".canvas"):
            for m in RE_CANVAS.finditer(t):
                got.add(m.group(1).strip().replace("\\", "/").split("/")[-1])
        per_file[os.path.relpath(p, VAULT)] = len(got)
        refs |= got
    return refs, per_file


def hsize(n):
    if n >= 1 << 30:
        return "%.2f GB" % (n / (1 << 30))
    if n >= 1 << 20:
        return "%.2f MB" % (n / (1 << 20))
    return "%.1f KB" % (n / 1024)


def main():
    imgs, txts = walk_files()
    print("图片文件 %d 个 / 文本 %d 个" % (len(imgs), len(txts)))

    refs, per_file = collect_refs(txts)
    print("引用到的唯一 basename %d 个" % len(refs))

    # 建索引
    info = []   # (relpath, size, basename)
    total = 0
    for p in imgs:
        try:
            s = os.path.getsize(p)
        except OSError:
            continue
        total += s
        info.append((os.path.relpath(p, VAULT), s, os.path.basename(p)))
    print("图片总体积 %s" % hsize(total))

    # 孤儿判定
    used = [x for x in info if x[2] in refs]
    orph = [x for x in info if x[2] not in refs]
    print()
    print("=== 孤儿图（basename 从未被引用）===")
    print("  %d 个 / %s / 占图片数 %.1f%% / 占体积 %.1f%%"
          % (len(orph), hsize(sum(x[1] for x in orph)),
             100.0 * len(orph) / max(1, len(info)),
             100.0 * sum(x[1] for x in orph) / max(1, total)))

    # 孤儿按顶层目录
    bydir = collections.defaultdict(lambda: [0, 0])
    for rel, s, b in orph:
        k = rel.replace("\\", "/").split("/")[0]
        bydir[k][0] += 1
        bydir[k][1] += s
    print()
    print("=== 孤儿按顶层目录 top15 ===")
    for k, (n, s) in sorted(bydir.items(), key=lambda kv: -kv[1][1])[:15]:
        print("  %6d 个  %10s   %s" % (n, hsize(s), k))

    # 引用数分布（md 文件维度）
    dist = collections.Counter()
    for f, n in per_file.items():
        if n == 0:
            dist["0 张"] += 1
        elif n <= 3:
            dist["1-3 张"] += 1
        elif n <= 10:
            dist["4-10 张"] += 1
        elif n <= 50:
            dist["11-50 张"] += 1
        else:
            dist[">50 张"] += 1
    print()
    print("=== md 文件的图片引用数分布 ===")
    order = ["0 张", "1-3 张", "4-10 张", "11-50 张", ">50 张"]
    for k in order:
        print("  %-10s %6d 个文件" % (k, dist.get(k, 0)))

    # 每个顶层目录的图片资产 vs 引用情况
    dir_stat = collections.defaultdict(lambda: {"imgs": 0, "size": 0, "orph": 0, "orph_size": 0})
    for rel, s, b in info:
        k = rel.replace("\\", "/").split("/")[0]
        dir_stat[k]["imgs"] += 1
        dir_stat[k]["size"] += s
    for rel, s, b in orph:
        k = rel.replace("\\", "/").split("/")[0]
        dir_stat[k]["orph"] += 1
        dir_stat[k]["orph_size"] += s
    print()
    print("=== 各顶层目录图片资产与利用率 ===")
    rows = sorted(dir_stat.items(), key=lambda kv: -kv[1]["size"])
    print("  %-28s %7s %10s %7s %10s %7s"
          % ("目录", "图片数", "体积", "孤儿数", "孤儿体积", "孤儿率"))
    for k, v in rows[:20]:
        rate = 100.0 * v["orph"] / max(1, v["imgs"])
        print("  %-28s %7d %10s %7d %10s %6.1f%%"
              % (k[:28], v["imgs"], hsize(v["size"]), v["orph"],
                 hsize(v["orph_size"]), rate))

    result = {
        "total_images": len(info),
        "total_size": total,
        "orphan": [{"path": r, "size": s} for r, s, b in orph],
        "dir_stat": {k: v for k, v in dir_stat.items()},
        "md_refcount": per_file,
    }

    if DEEP:
        print()
        print("=== 内容去重（读取全库图片，较慢）===")
        h2p = collections.defaultdict(list)
        for i, (rel, s, b) in enumerate(info):
            try:
                h = hashlib.sha256(open(os.path.join(VAULT, rel), "rb").read()).hexdigest()
            except OSError:
                continue
            h2p[h].append((rel, s))
            if (i + 1) % 20000 == 0:
                print("   ...%d/%d" % (i + 1, len(info)))
        dup_groups = {h: v for h, v in h2p.items() if len(v) > 1}
        dup_extra = sum(len(v) - 1 for v in dup_groups.values())
        dup_size = sum(sum(s for _, s in v[1:]) for v in dup_groups.values())
        print("  重复组 %d 个，冗余副本 %d 张，可回收 %s"
              % (len(dup_groups), dup_extra, hsize(dup_size)))
        result["dup_groups"] = {h: v for h, v in dup_groups.items()}
        result["dup_extra"] = dup_extra
        result["dup_size"] = dup_size

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(result, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    print()
    print("详细清单 ->", OUT)


if __name__ == "__main__":
    main()
