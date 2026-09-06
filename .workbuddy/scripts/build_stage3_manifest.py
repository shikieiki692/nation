#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶段3 删除清单构建 —— 无争议桶 + 自动编号孤儿

相比阶段2 多加一道【全库字节级引用扫描】闸门：
  对每个候选文件的 basename，当作原始字节串，在全库每一个非图片文件里全文搜索。
  任何人（无论 md / html / xml / json / csv / py / 日志）提到过，就不删。
  这道闸门不依赖正则，因此不会因为「引用写法没被正则覆盖」而漏判。

输入: .workbuddy/tmp/orphan_risk.json
输出: .workbuddy/tmp/cleanup_stage3.txt      相对路径清单
      .workbuddy/tmp/stage3_plan.json        明细（含体积、所在目录）
"""
import json
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.join(VAULT, ".workbuddy", "tmp")

# 不参与删除的目录（同 image_usage_stats.py 的 SKIP_DIRS，另加 .git 之外的仓库元数据）
SKIP_DIRS = {".git", ".workbuddy", "node_modules", ".obsidian", "__pycache__",
             ".trash", "_归档", "_archive", "备份"}
# 扫描引用时要跳过的目录：仓库元数据 + 本工具自己产出的中间文件
SCAN_SKIP_DIRS = {".git", "node_modules", ".obsidian", "__pycache__", ".trash"}

# 噪源：这些地方「提到」图片名并不等于在用它——
#   .workbuddy 本脚本自己的统计结果、.claudian 会话日志、
#   10-索引与统计 图谱/清单、09-审计报告 正文把图片名当证据抄写。
# 不排除的话闸门会把 100% 候选拦下（实测：338/338 全被自己的 json 拦住）。
SCAN_NOISE_PATH_PAT = re.compile(
    r"(^|[\\/])("
    r"\.workbuddy|"
    r"\.claudian|"
    r"10-索引与统计|"
    r"09-审计报告|"
    r"构建中间产物"
    r")([\\/]|$)"
)

IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp", ".tif", ".tiff"}

# 无争议桶：用户自己标注过「待清理·零引用」或明显是渲染中间产物
# 注：.claude 原本在列，但它的 formula-assets/* 被 generate_formula_pngs.ps1、
#     render-eqs.js 真实引用（是脚本产出而非孤儿），且仅 80 KB，故移出删除范围。
SAFE_DIR_PATS = [
    re.compile(r"(^|[\\/])10-附件[\\/]待清理[\\/]决赛提取图片-零引用-20260723([\\/]|$)"),
    re.compile(r"(^|[\\/])04-课件[\\/]试点产出[\\/][^\\/]*-render([\\/]|$)"),
]

# 自动编号命名：page-N / image-N / img_001 / 纯数字 / 图1 ...
RE_AUTONUM = re.compile(
    r"^(page|image|img|fig|figure|slide|sheet|p|scene|frame|图|第)?"
    r"[_\-\s]?\d+([_\-\s]?\d+)*$", re.I)

MAX_SCAN_BYTES = 30 * 1024 * 1024   # 单文件超过 30 MB 不读（几乎不存在这么大的文本文件）


def load_risk():
    with open(os.path.join(TMP, "orphan_risk.json"), encoding="utf-8") as f:
        return json.load(f)


def pick_candidates(risk):
    """返回 {relpath: (来源标签, size)}"""
    t3 = risk["T3_unique"]          # {relpath: {"size": int}}
    t0 = set(risk["T0_false"]) if isinstance(risk["T0_false"], dict) else set(risk["T0_false"])
    out = {}

    for p, meta in t3.items():
        if p in t0:
            continue
        stem = p.split("\\")[-1].rsplit(".", 1)[0]
        hit_safe = any(pat.search(p) for pat in SAFE_DIR_PATS)
        hit_num = bool(RE_AUTONUM.match(stem))
        if hit_safe and hit_num:
            tag = "无争议桶+自动编号"
        elif hit_safe:
            tag = "无争议桶"
        elif hit_num:
            tag = "自动编号"
        else:
            continue
        out[p] = (tag, meta["size"])
    return out


def byte_scan_gate(cands):
    """全库字节级引用扫描：返回 {basename: [(提到它的文件, ...), ...]}"""
    names = {}
    for p in cands:
        bn = os.path.basename(p).rsplit(".", 1)[0].encode("utf-8")
        names.setdefault(bn, []).append(p)

    pats = [(bn, re.compile(re.escape(bn))) for bn in names]
    hits = {bn: [] for bn in names}

    scanned = skipped_big = 0
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SCAN_SKIP_DIRS]
        rel_root = os.path.relpath(root, VAULT)
        if SCAN_NOISE_PATH_PAT.search(rel_root):
            continue
        for fn in files:
            fp = os.path.join(root, fn)
            if os.path.splitext(fn)[1].lower() in IMG_EXT:
                continue
            try:
                sz = os.path.getsize(fp)
            except OSError:
                continue
            if sz == 0 or sz > MAX_SCAN_BYTES:
                skipped_big += 1
                continue
            try:
                with open(fp, "rb") as f:
                    blob = f.read()
            except OSError:
                continue
            scanned += 1
            for bn, pat in pats:
                if pat.search(blob):
                    hits[bn].append(fp)
    return hits, scanned, skipped_big


def main():
    risk = load_risk()
    cands = pick_candidates(risk)
    print(f"[1] T3 中命中规则: {len(cands):,} 个")

    # 预检：文件必须存在
    alive = {}
    for p, (tag, size) in cands.items():
        fp = os.path.join(VAULT, p)
        if os.path.isfile(fp):
            alive[p] = (tag, os.path.getsize(fp))
    print(f"[2] 磁盘上仍存在: {len(alive):,} 个")

    print(f"[3] 全库字节级引用扫描中（这一步最慢，请稍候）...")
    hits, scanned, skipped = byte_scan_gate(alive)
    print(f"    扫描非图片文件 {scanned:,} 个，跳过超大/空 {skipped:,} 个")

    ok, blocked = {}, {}
    for p, (tag, size) in alive.items():
        bn = os.path.basename(p).rsplit(".", 1)[0].encode("utf-8")
        h = [x for x in hits.get(bn, []) if os.path.abspath(x) != os.path.join(VAULT, p)]
        if h:
            blocked[p] = (tag, size, h[:3])
        else:
            ok[p] = (tag, size)

    print(f"[4] 闸门结果: 放行 {len(ok):,} 个 / 拦截 {len(blocked):,} 个")

    if blocked:
        print("\n---- 被引用而拦截（保留）样例 ----")
        for p, (tag, size, h) in list(blocked.items())[:15]:
            print(f"  [{tag}] {p}  ({size/1024:.0f} KB)")
            for x in h:
                print(f"      提到于: {os.path.relpath(x, VAULT)}")

    tot = sum(v[1] for v in ok.values())
    by_tag = {}
    by_dir = {}
    for p, (tag, size) in ok.items():
        by_tag[tag] = by_tag.get(tag, [0, 0])
        by_tag[tag][0] += 1
        by_tag[tag][1] += size
        d = p.split("\\")[0] if "\\" in p else p.split("/")[0]
        by_dir[d] = by_dir.get(d, [0, 0])
        by_dir[d][0] += 1
        by_dir[d][1] += size

    print(f"\n==== 阶段3 放行合计 {len(ok):,} 个 / {tot/1024/1024:.2f} MB ====")
    print("按来源:")
    for k, (n, s) in sorted(by_tag.items(), key=lambda x: -x[1][1]):
        print(f"  {s/1024/1024:8.2f} MB  {n:6,} 张  {k}")
    print("按目录 Top15:")
    for k, (n, s) in sorted(by_dir.items(), key=lambda x: -x[1][1])[:15]:
        print(f"  {s/1024/1024:8.2f} MB  {n:6,} 张  {k}")

    print("\n自动编号样例（前 20 个，人工过目）:")
    sample = [p for p, (t, _) in ok.items() if "自动编号" in t][:20]
    for p in sample:
        print("   ", p)

    with open(os.path.join(TMP, "cleanup_stage3.txt"), "w", encoding="utf-8", newline="") as f:
        for p in sorted(ok):
            f.write(p + "\n")
    with open(os.path.join(TMP, "stage3_plan.json"), "w", encoding="utf-8", newline="") as f:
        json.dump({"files": {p: {"tag": t, "size": s} for p, (t, s) in ok.items()},
                   "blocked": {p: {"tag": t, "size": s, "hit": h}
                               for p, (t, s, h) in blocked.items()}},
                  f, ensure_ascii=False, indent=1)
    print(f"\n清单已写入: .workbuddy/tmp/cleanup_stage3.txt  ({len(ok):,} 行)")


if __name__ == "__main__":
    main()
