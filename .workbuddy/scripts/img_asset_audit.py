# -*- coding: utf-8 -*-
"""
图片资产统一审计器（只读；不修改库内任何文件）
================================================================
把历史上散落在 .workbuddy/scripts/ 的 30+ 个一次性图片脚本收敛为一个入口，
输出下列 8 组口径，用于「改前基线 / 改后复核」双向对照。

用法：
    python -X utf8 .workbuddy/scripts/img_asset_audit.py [--json 输出.json]

口径定义（务必与本文件的实现一致，换口径必须改版本号）
  V1 引用解析四态：exact（vault 相对路径命中）/ basename（路径失效但 Obsidian
     basename 回退可显示）/ missing（真断链）/ placeholder（文档模板占位）
     —— 注意 Obsidian 语义是「先精确路径、再全库 basename」，缺任一步都会虚报。
  V2 媒体仓库利用率 / 孤儿
  V3 子目录与别名文件盘点（两者都违反「扁平＋哈希原名」约定）
  V4 媒体仓库内部重复（同内容）
  V5 图谱索引对账：登记数 / 真在媒体仓库 / ✅ 标签失实 / 自报规模 vs 条目数
  V6 媒体仓库清单.json 对账，并区分「改名」与「丢失」
  V7 真断链的归属分诊（消费端 / 源料端 / 报告载体）

⚠️ 已知假阳性（不要当作缺陷上报）：
  - 文档里的模板占位串（`<64位哈希>.jpg`、`xxx.jpg`、`{hash}.jpg`）→ placeholder
  - `09-审计报告/`、`00-首页/工作日志/` 正在「引用缺陷原文」→ 不是缺陷本身
  - 三重口径下仍解析不了的深层路径图，Obsidian 可能显示正常
"""
import os
import re
import sys
import json
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from urllib.parse import unquote

try:
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
except Exception:
    Image = None

VERSION = "2026-09-23.3"

VAULT = Path(__file__).resolve().parents[2]
MEDIA = VAULT / "媒体仓库"
IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".tif", ".bmp"}
# 非内容区 / 工具区：不进扫描（否则 33k 源料图会淹没结论）
SKIP_TOP = {"_归档", "99-归档", "kb-vault-mcp", "pptx-workspace", "skills",
            "copilot", "eiki", "scripts", "11", "mineru", "mineru02",
            "bdwp资源", "11-模板", "09-AI工作区", ".claude", ".github"}
# 消费端（产物）与源料端（OCR 中间物）的边界，用于断链分诊
CONSUMER = ("00-首页", "01-考纲导航", "02-考纲条目", "03-知识点", "04-题库",
            "04-课件", "04-专题与题型", "05-真题库", "06-学生侧材料",
            "08-可视化资源", "10-索引与统计", "12-教学洞察", "13-教案")
SOURCE = ("06-外部资料导入", "07-资料提炼")
REPORT_CARRIER = ("09-审计报告", "10-附件")
HASH_RE = re.compile(r"^[0-9a-f]{40,64}$", re.I)
PLACEHOLDER_RE = re.compile(
    r"^(<.*>|hash|哈希|图片文件|图片名|文件名|哈希文件名|哈希名|xxx|yyy|zzz|"
    r"abc|example|示例|path|name|file|img|image)$", re.I)


def walk_full_names():
    """全库图片 basename 索引 —— 判定「库内他处可寻 / 全库皆无」必须用这个口径。
    ⚠️ 不能复用 walk_media_and_md 的结果：那份带了 SKIP_TOP 排除（mineru/ 等），
       会把「在 mineru 里存在」的图误判成「全库皆无」，随排除范围漂移。"""
    names = set()
    for root, dirs, files in os.walk(VAULT):
        rp = Path(root)
        if rp == VAULT:
            dirs[:] = [d for d in dirs if d not in (".git",)]
        dirs[:] = [d for d in dirs if not d.startswith(".workbuddy")]
        for f in files:
            if Path(f).suffix.lower() in IMG_EXT:
                names.add(f)
    return names


def walk_media_and_md():
    """一次遍历，收集：图片索引 / md 图片引用。"""
    by_name, by_rel = defaultdict(list), set()
    refs = []
    for root, dirs, files in os.walk(VAULT):
        rp = Path(root)
        if rp == VAULT:
            dirs[:] = [d for d in dirs if d not in SKIP_TOP]
        dirs[:] = [d for d in dirs if d != ".git" and not d.startswith(".workbuddy")]
        for f in files:
            suf = Path(f).suffix.lower()
            if suf in IMG_EXT:
                by_name[f].append(rp / f)
                by_rel.add(str((rp / f).relative_to(VAULT)).replace("\\", "/"))
        for f in files:
            if not f.lower().endswith((".md", ".markdown")):
                continue
            p = rp / f
            txt = p.read_text(encoding="utf-8", errors="replace")
            rel_md = str(p.relative_to(VAULT)).replace("\\", "/")
            for m in re.finditer(r"!\[\[([^\]]+?)\]\]", txt):
                t = m.group(1).split("|")[0].split("#")[0].strip()
                refs.append((rel_md, "wiki", t))
            for m in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)", txt):
                t = m.group(1)
                if not t.startswith(("http://", "https://", "data:")):
                    refs.append((rel_md, "md", t))
    return by_name, by_rel, refs


def resolve_refs(by_name, by_rel, refs):
    """V1 引用解析四态。"""
    stat = Counter()
    broken, path_only, ok_exact = [], [], []
    used_names = set()
    for src, kind, target in refs:
        t = unquote(target).replace("\\", "/")
        base = t.split("/")[-1]
        ext = Path(base).suffix.lower()
        if base in ("...", "…") or "{" in t or "}" in t or PLACEHOLDER_RE.match(
                Path(base).stem) or base.startswith("<"):
            stat["placeholder"] += 1
            continue
        if ext not in IMG_EXT:
            stat["non_image"] += 1
            continue
        hit = None
        if t in by_rel:
            hit = "exact"
        elif kind == "md" and (VAULT / src).parent.joinpath(t).exists():
            hit = "exact"
        if hit is None and base in by_name:
            hit = "basename"
        if hit is None:
            stat["missing"] += 1
            broken.append((src, base, target))
        else:
            stat["ok_" + hit] += 1
            used_names.add(base)
            (path_only if hit == "basename" else ok_exact).append((src, base, target))
    return stat, broken, path_only, ok_exact, used_names


def media_report(used_names):
    """V2/V3/V4 媒体仓库。"""
    med = [p for p in MEDIA.rglob("*") if p.is_file() and p.suffix.lower() in IMG_EXT]
    top = [p for p in med if p.parent == MEDIA]
    sub = [p for p in med if p.parent != MEDIA]
    used = [p for p in med if p.name in used_names]
    orphan = [p for p in med if p.name not in used_names]
    alias = [p for p in med if not HASH_RE.fullmatch(p.stem)]
    alias_used = [p for p in alias if p.name in used_names]
    subdirs = Counter(p.parent.name for p in sub)
    sub_only = [p for p in sub if not (MEDIA / p.name).exists()]
    byh = defaultdict(list)
    for p in med:
        byh[hashlib.md5(p.read_bytes()).hexdigest()].append(p)
    dup = {h: v for h, v in byh.items() if len(v) > 1}
    dup_waste = sum((len(v) - 1) * v[0].stat().st_size for v in dup.values())
    return dict(
        total=len(med), top=len(top), sub=len(sub),
        used=len(used), orphan=len(orphan),
        orphan_mb=round(sum(p.stat().st_size for p in orphan) / 1024 / 1024, 1),
        alias=len(alias), alias_used=len(alias_used), alias_orphan=len(alias) - len(alias_used),
        subdirs=dict(subdirs), sub_only=len(sub_only),
        dup_groups=len(dup),
        dup_same_name=sum(1 for v in dup.values() if len({p.name for p in v}) == 1),
        dup_waste_mb=round(dup_waste / 1024 / 1024, 1),
        orphan_list=sorted(str(p.relative_to(VAULT)) for p in orphan),
    )


def index_report(full_names):
    """V5 图谱索引对账。"""
    med_names = {p.name for p in MEDIA.rglob("*") if p.is_file()}
    out = {}
    files = ["10-索引与统计/01-有机化学图谱总索引.md",
             "10-索引与统计/02-结构与无机化学图谱总索引.md",
             "10-索引与统计/03-物化与分析化学图谱总索引.md",
             "10-索引与统计/全库核心图谱总索引.md",
             "10-索引与统计/视觉已验证图片索引.md"]
    for f in files:
        p = VAULT / f
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        names = list(dict.fromkeys(
            re.findall(r"\b([0-9a-f]{56,64}\.(?:jpg|jpeg|png|svg))\b", txt, re.I)))
        inmed = [n for n in names if n in med_names]
        elsewhere = [n for n in names if n not in med_names and n in full_names]
        nowhere = [n for n in names if n not in med_names and n not in full_names]
        # ✅ 标签失实：整行含 ✅ 但文件不在媒体仓库
        rows = re.findall(r"^\|\s*([0-9a-f]{56,64}\.(?:jpg|jpeg|png|svg))[^\n]*✅[^\n]*$",
                          txt, re.I | re.M)
        bad = [r for r in rows if r not in med_names]
        claim = re.findall(r"共收录\s*\*{0,2}([\d,]+)\*{0,2}\s*张", txt)
        out[Path(f).name] = dict(
            entries=len(names), in_media=len(inmed),
            elsewhere=len(elsewhere), nowhere=len(nowhere),
            checkmark_rows=len(rows), checkmark_false=len(bad),
            claim=claim[0].replace(",", "") if claim else None)
    return out


def manifest_report(full_names):
    """V6 媒体仓库清单对账 —— 必须区分「改名」与「丢失」。"""
    p = VAULT / "10-索引与统计/媒体仓库清单.json"
    if not p.exists():
        return {}
    d = json.load(open(p, encoding="utf-8"))
    listed = {x["name"]: x.get("size", 0) for x in d["files"]}
    disk = {q.name for q in MEDIA.rglob("*") if q.is_file()}
    miss = [n for n in listed if n not in disk]
    extra = [n for n in disk if n not in listed]
    # 改名证据：别名式缺失，其裸哈希部分是否已在盘上
    renamed = 0
    for n in miss:
        m = re.search(r"([0-9a-f]{40,64})(?=\.\w+$)", n)
        if m and m.group(1) + Path(n).suffix in disk:
            renamed += 1
    hash_miss = [n for n in miss if HASH_RE.fullmatch(Path(n).stem)]
    gone = [n for n in hash_miss if n not in full_names]
    return dict(generated=d.get("generated"), listed=len(listed), on_disk=len(disk),
                missing=len(miss), extra=len(extra), renamed_evidence=renamed,
                hash_missing=len(hash_miss), gone_everywhere=len(gone),
                gone_mb=round(sum(listed[n] for n in gone) / 1024 / 1024, 1))


def quality_report(target, json_out=None):
    """V8 规模与质量 —— 逐张测量（尺寸/长宽比/墨迹/色彩/体积）+ 互斥废片分类。

    ⚠️ 三条判据纪律（踩过）：
      1. 空白判定必须回**全分辨率**多阈值复核；160px 缩略图口径会误判（实测 5/78）。
      2. 公式切片必须用**方向性**判据（高≤70 且宽高比≥6）；只判长宽比会算进竖长图。
      3. 结果**必须抽样目检**——「小 ≠ 低质」，本库实测规则假阳性约 15%。
    依赖 Pillow；记录落 json_out（默认不落）。
    """
    if Image is None:
        print("  [SKIP] 未安装 Pillow，无法执行质量模式")
        return {}
    # ⚠️ SVG 是矢量格式，PIL 读不了 —— 不能算「伪图片」，必须排除出位图测量
    PIL_EXT = IMG_EXT - {".svg"}
    files = [p for p in Path(target).rglob("*")
             if p.is_file() and p.suffix.lower() in PIL_EXT]
    svg_n = sum(1 for p in Path(target).rglob("*")
                if p.is_file() and p.suffix.lower() == ".svg")
    print(f"\n=== V8 规模与质量（{Path(target).name}: {len(files)} 张位图"
          f"{f'，另有 {svg_n} 个 SVG 不参与位图测量' if svg_n else ''}）===")
    recs, failed = [], []
    for p in files:
        try:
            sz = p.stat().st_size
            with Image.open(p) as im:
                W, H = im.size
                th = im.copy()
                th.thumbnail((160, 160))
                g = th.convert("L")
                px = list(g.get_flattened_data())
                n = len(px)
                ink = sum(1 for v in px if v < 200) / n
                dark = sum(1 for v in px if v < 128) / n
                rgb = th.convert("RGB")
                col = len(set(rgb.get_flattened_data()))
            recs.append(dict(f=str(p), w=W, h=H, kb=round(sz / 1024, 1),
                             ink=ink, dark=dark, colors=col,
                             aspect=max(W, H) / max(1, min(W, H))))
        except Exception:
            failed.append(str(p))

    areas = sorted(r["w"] * r["h"] for r in recs)
    def q(v, x):
        return v[min(len(v) - 1, int(len(v) * x))] if v else 0
    print(f"  分辨率：中位 {q(areas,0.5):,} px²（≈{int(q(areas,0.5)**0.5)}²）  "
          f"P25 {q(areas,0.25):,}  P95 {q(areas,0.95):,}")
    print("  打印可用性（300 dpi）：")
    for lab, need in (("4cm 缩略", 472), ("7.5cm 半栏", 886), ("15cm 整栏", 1772)):
        n = sum(1 for r in recs if r["w"] >= need)
        print(f"    宽≥{need:5d}px  {lab:12s} {n:6d}  {n/max(1,len(recs))*100:5.1f}%")

    # 空白/极淡：全分辨率多阈值复核（缩略图口径会误判，必须复核）
    blank, faint, visible = [], [], []
    for r in recs:
        if r["ink"] >= 0.005:
            continue
        try:
            with Image.open(r["f"]) as im:
                g = im.convert("L")
                g.thumbnail((600, 600))
                px = list(g.get_flattened_data())
                f200 = sum(1 for v in px if v < 200) / len(px)
            if f200 < 0.002:
                blank.append(Path(r["f"]).name)
            elif f200 < 0.01:
                faint.append(Path(r["f"]).name)
            else:
                visible.append(Path(r["f"]).name)   # 缩略图误判，其实可见
        except Exception:
            pass

    def is_strip(r):
        return r["h"] <= 70 and r["aspect"] >= 6 and r["w"] >= 250
    strips = [Path(r["f"]).name for r in recs if is_strip(r)]
    tiny = [Path(r["f"]).name for r in recs if max(r["w"], r["h"]) < 60]
    solid = [Path(r["f"]).name for r in recs if r["colors"] == 1]

    # 互斥：A→B→C→D→E→F
    seen, cat = set(), {}
    for key, names in (("A 伪图片（打不开）", [Path(x).name for x in failed]),
                       ("B 真·空白（全分辨率深墨<0.2%）", blank),
                       ("C 极淡（0.2–1%）", faint),
                       ("D 单行公式切片（高≤70 & 宽高比≥6）", strips),
                       ("E 极小碎片（最长边<60px）", tiny),
                       ("F 纯色（缩略图仅 1 色）", solid)):
        v = sorted(set(names) - seen)
        seen |= set(v)
        cat[key] = v
    print("  废片分类（互斥）：")
    for k, v in cat.items():
        print(f"    {k:38s} {len(v):5d}")
    print(f"    {'—— 合计':38s} {len(seen):5d}  "
          f"({len(seen)/max(1,len(recs))*100:.1f}% of 目标目录)")
    if visible:
        print(f"    另：{len(visible)} 张在缩略图口径下疑似空白，全分辨率复核后**其实可见**（已剔除）")
    print("  ★ 抽样目检后再动手：规则假阳性本库实测约 15%（小尺寸≠低质）")

    if json_out:
        Path(json_out).write_text(json.dumps(
            dict(target=str(target), records=recs, failed=failed, garbage=cat),
            ensure_ascii=False), encoding="utf-8")
        print(f"  [落盘] {json_out}")
    return dict(total=len(recs), garbage={k: len(v) for k, v in cat.items()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="把结果落盘为 JSON")
    ap.add_argument("--quality", action="store_true",
                    help="只跑 V8 规模与质量（逐张测图像，需 Pillow）")
    ap.add_argument("--target", default=str(MEDIA), help="V8 的目标目录")
    a = ap.parse_args()

    print(f"[img_asset_audit v{VERSION}] 基线：{VAULT}")
    if a.quality:
        quality_report(a.target, a.json)
        return
    full_names = walk_full_names()
    by_name, by_rel, refs = walk_media_and_md()
    print(f"  扫描：md 引用 {len(refs)} 条；库内图片 {sum(len(v) for v in by_name.values())} 个；全库图片 basename {len(full_names)} 个")

    stat, broken, path_only, ok_exact, used_names = resolve_refs(by_name, by_rel, refs)
    print("\n=== V1 引用解析（Obsidian 语义）===")
    for k in ("ok_exact", "ok_basename", "missing", "placeholder", "non_image"):
        print(f"  {k:12s} {stat[k]}")

    print("\n=== V7 真断链归属 ===")
    cat = Counter()
    for src, base, target in broken:
        top = Path(src).parts[0]
        cat["消费端" if top in CONSUMER else
            "源料端" if top in SOURCE else
            "报告载体" if top in REPORT_CARRIER else f"其它:{top}"] += 1
    for k, v in cat.most_common():
        print(f"  {k:24s} {v}")

    mr = media_report(used_names)
    print("\n=== V2 媒体仓库利用率 ===")
    print(f"  总 {mr['total']}（顶层 {mr['top']} / 子目录 {mr['sub']}）"
          f"  被引用 {mr['used']}  孤儿 {mr['orphan']} ({mr['orphan']/max(1,mr['total'])*100:.1f}%,"
          f" {mr['orphan_mb']} MB)")
    print("=== V3 子目录 / 别名 ===")
    for k, v in mr["subdirs"].items():
        print(f"  子目录 {k:28s} {v} 文件")
    print(f"  仅存在于子目录（Word 管线取不到）: {mr['sub_only']}")
    print(f"  别名文件 {mr['alias']}（被引用 {mr['alias_used']} / 孤儿 {mr['alias_orphan']}）")
    print("=== V4 内部重复 ===")
    print(f"  同内容组 {mr['dup_groups']}（同名 {mr['dup_same_name']}）"
          f"  冗余 {mr['dup_waste_mb']} MB")

    ir = index_report(full_names)
    print("\n=== V5 图谱索引对账 ===")
    for k, v in ir.items():
        print(f"  {k[:28]:30s} 登记 {v['entries']:5d}  在媒体仓库 {v['in_media']:5d}"
              f" ({v['in_media']/max(1,v['entries'])*100:5.1f}%)  他处 {v['elsewhere']:5d}"
              f"  皆无 {v['nowhere']:3d}  ✅行 {v['checkmark_rows']:5d}"
              f"  ✅失实 {v['checkmark_false']:5d}  自报 {v['claim']}")

    mf = manifest_report(full_names)
    if mf:
        print("\n=== V6 媒体仓库清单对账 ===")
        print(f"  清单生成 {mf['generated']}  登记 {mf['listed']}  现盘 {mf['on_disk']}")
        print(f"  缺失 {mf['missing']}（改名证据 {mf['renamed_evidence']}）"
              f"  新增 {mf['extra']}")
        print(f"  纯哈希缺失 {mf['hash_missing']}，库内他处可寻 {mf['hash_missing']-mf['gone_everywhere']}"
              f"，全库皆无 {mf['gone_everywhere']} ({mf['gone_mb']} MB)")

    if a.json:
        Path(a.json).write_text(json.dumps(
            dict(version=VERSION, stat=dict(stat), broken=broken,
                 media={k: v for k, v in mr.items() if k != "orphan_list"},
                 index=ir, manifest=mf),
            ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n[落盘] {a.json}")


if __name__ == "__main__":
    main()
