# -*- coding: utf-8 -*-
"""
孤儿图风险分层分析（在 image_usage_stats.py --deep 之后运行）

在「md 引用」这一维之外，再补三个判据，把孤儿图分成可安全删除 / 必须保留 / 需人工判断：

  T0 假孤儿：孤儿图其实被 docx/pptx/xlsx/canvas/json/html/ipynb/py 等非 md 文件引用
             → 必须保留（除非确认那些容器本身废弃）
  T1 零损失：孤儿图的内容哈希 == 某个「被引用图」的内容哈希
             → 删掉它，同样的图还在库里（以另一个名字被引用着），零信息损失
  T2 冗余份：真孤儿，但同内容还有其他孤儿副本
             → 可删冗余副本、保留 1 份（信息不丢）
  T3 唯一份：真孤儿且内容全库唯一
             → 删了就真没了，需人工按目录判断

用法：
  python .workbuddy/scripts/analyze_orphan_risk.py
输出：
  .workbuddy/tmp/orphan_risk.json
"""
import os, re, json, sys, zipfile, collections, subprocess

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.join(VAULT, ".workbuddy", "tmp")


def git_tracked_tops():
    """返回「顶层目录 -> 是否有 git 跟踪」。
    媒体仓库等被 gitignore 的目录删了没法 git 回滚，保留副本时应优先避开。"""
    try:
        r = subprocess.run(["git", "-c", "core.quotepath=false", "ls-files", "-z"],
                           cwd=VAULT, capture_output=True)
        files = [x for x in r.stdout.decode("utf-8", errors="ignore").split("\0") if x]
    except Exception:
        return collections.defaultdict(lambda: True)
    tops = collections.Counter(f.split("/")[0] for f in files)
    return tops


def keeper_score(path, tracked_tops):
    """越大越优先保留：(git 有跟踪, 体积, 路径短)"""
    top = path.split(os.sep)[0]
    tracked = 1 if tracked_tops.get(top, 0) > 0 else 0
    try:
        sz = os.path.getsize(os.path.join(VAULT, path))
    except OSError:
        sz = 0
    return (tracked, sz, -len(path))
IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp", ".tif", ".tiff", ".ico"}
SKIP_DIRS = {".git", ".workbuddy", "node_modules", ".obsidian", "__pycache__",
             ".trash", "_归档", "_archive", "备份"}

# 非 md 容器里「像图片文件名」的 token
RE_IMGTOKEN = re.compile(r"[\w\-\u4e00-\u9fff\.\(\)（）]+\.(?:jpe?g|png|gif|svg|webp|bmp|tif|tiff)", re.I)
# 容器后缀（zip 系需要解压扫描）
ZIP_EXT = {".docx", ".pptx", ".xlsx", ".odt", ".odp", ".ods", ".zip", ".jar", ".vsix", ".crx", ".whl"}
# 纯文本后缀（直接读）
TEXT_EXT = {".md", ".txt", ".json", ".html", ".htm", ".xml", ".canvas", ".base",
            ".ipynb", ".py", ".js", ".ts", ".css", ".csv", ".yaml", ".yml",
            ".tex", ".bib", ".rst", ".ini", ".cfg", ".toml", ".sh", ".bat"}

# ---------------------------------------------------------------------------
# 噪源过滤：下面这些文件会「提到」图片名，但属于登记/日志/临时产物，不算真引用。
# 不剔除的话 T0 会被严重高估（实测：媒体仓库清单.json 一家就命中 14,043 次）。
# ---------------------------------------------------------------------------
NOISE_PATH_PAT = re.compile(
    r"(^|[\\/])("
    r"10-索引与统计|"        # 图谱雷达/媒体仓库清单：图片「目录」而非「使用处」
    r"\.claudian|"           # AI 会话日志
    r"\.workbuddy|"
    r"09-审计报告|"          # 审计报告正文里会抄写图片名当证据
    r"构建中间产物|"         # 构建临时目录
    r"\.trash"
    r")([\\/]|$)"
)
NOISE_NAME_PAT = re.compile(
    r"^(媒体仓库清单|全库核心图谱总索引|dependency-map|溯源映射|checkpoint)"
    r"|_filelist|_index|图谱总索引|\.meta\.json$", re.I
)


def is_noise(rel):
    return bool(NOISE_PATH_PAT.search(rel)) or bool(NOISE_NAME_PAT.search(os.path.basename(rel)))


def walk_images():
    """全库图片：relpath -> size"""
    out = {}
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if os.path.splitext(f)[1].lower() in IMG_EXT:
                p = os.path.relpath(os.path.join(root, f), VAULT)
                try:
                    out[p] = os.path.getsize(os.path.join(root, f))
                except OSError:
                    pass
    return out


def scan_container_refs():
    """扫描所有非 md 文件（docx/pptx/canvas/...），抽出里面出现的图片 basename。
    噪源（目录/日志/临时产物）单独记到 noise 里，不计入真引用。"""
    found = collections.defaultdict(set)   # basename -> {真引用方}
    noise = collections.defaultdict(set)   # basename -> {噪源}
    n_zip = n_txt = n_skip = 0
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in IMG_EXT or ext == ".md":
                continue
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, VAULT)
            bucket = noise if is_noise(rel) else found
            try:
                if bucket is noise:
                    n_skip += 1
                if ext in ZIP_EXT and zipfile.is_zipfile(fp):
                    n_zip += 1
                    with zipfile.ZipFile(fp) as z:
                        for name in z.namelist():
                            b = os.path.basename(name)
                            if os.path.splitext(b)[1].lower() in IMG_EXT:
                                bucket[b.lower()].add(rel)
                        for name in z.namelist():
                            if not name.lower().endswith((".xml", ".rels", ".txt", ".json")):
                                continue
                            try:
                                data = z.read(name).decode("utf-8", "ignore")
                            except Exception:
                                continue
                            for m in RE_IMGTOKEN.finditer(data):
                                bucket[os.path.basename(m.group(0)).lower()].add(rel)
                elif ext in TEXT_EXT:
                    n_txt += 1
                    with open(fp, encoding="utf-8", errors="ignore") as fh:
                        data = fh.read()
                    for m in RE_IMGTOKEN.finditer(data):
                        bucket[os.path.basename(m.group(0)).lower()].add(rel)
            except Exception:
                pass
    print("  扫描容器：zip %d 个，文本 %d 个（噪源 %d 个已剔除）" % (n_zip, n_txt, n_skip))
    return found, noise


def main():
    usage = json.load(open(os.path.join(TMP, "image_usage.json"), encoding="utf-8"))
    orphan = {o["path"]: o["size"] for o in usage["orphan"]}
    dup = usage.get("dup_groups", {})
    print("孤儿 %d 张 / %.2f MB；重复组 %d 个" % (
        len(orphan), sum(orphan.values()) / 1048576, len(dup)))

    print("[1/3] 重建全库图片索引...")
    tracked_tops = git_tracked_tops()
    untracked = [t for t in ("媒体仓库", "无机化学下册", "中级无机化学", "10-附件")
                 if tracked_tops.get(t, 0) == 0]
    if untracked:
        print("  ⚠ 无 git 跟踪的顶层目录：%s（删了只能靠回收站）" % "、".join(untracked))
    allimg = walk_images()
    referenced = {p: s for p, s in allimg.items() if p not in orphan}
    print("  全库图片 %d，被引用 %d，孤儿 %d" % (len(allimg), len(referenced), len(orphan)))

    print("[2/3] 扫描非 md 容器引用（docx/pptx/canvas/...）...")
    cref, cnoise = scan_container_refs()

    # ---- T0 假孤儿（真引用，必须保留）----
    t0 = {}
    for p, s in orphan.items():
        b = os.path.basename(p).lower()
        if b in cref:
            t0[p] = {"size": s, "ref_by": sorted(cref[b])[:3]}
    # ---- T0n 仅被噪源提到（目录/日志/临时产物），不算在用 ----
    t0n = {}
    for p, s in orphan.items():
        b = os.path.basename(p).lower()
        if p not in t0 and b in cnoise:
            t0n[p] = {"size": s, "noise_by": sorted(cnoise[b])[:3]}
    print("  T0  假孤儿（被 docx/pptx/canvas 等真引用，必须保留）：%d 张 / %.2f MB" % (
        len(t0), sum(v["size"] for v in t0.values()) / 1048576))
    print("  T0n 仅被目录/日志提到（非真引用）：%d 张 / %.2f MB" % (
        len(t0n), sum(v["size"] for v in t0n.values()) / 1048576))

    rest = {p: s for p, s in orphan.items() if p not in t0}

    # ---- T1 零损失：孤儿内容 == 某个被引用图的内容 ----
    # dup[hash] = [[path, size], ...]
    t1, t2, t3 = {}, {}, {}
    seen_in_dup = set()
    for h, members in dup.items():
        paths = [m[0] for m in members]
        ref_m = [m for m in members if m[0] in referenced]
        orph_m = [m for m in members if m[0] in rest]
        for m in orph_m:
            seen_in_dup.add(m[0])
            if ref_m:
                t1[m[0]] = {"size": m[1], "hash": h,
                            "twin": ref_m[0][0]}
            else:
                # 全是孤儿：保留 1 份。优先保留在「有 git 跟踪」的目录里，
                # 其次体积大、路径短——避免幸存副本落在 gitignore 的媒体仓库。
                keep = max(orph_m, key=lambda x: keeper_score(x[0], tracked_tops))[0]
                if m[0] != keep:
                    t2[m[0]] = {"size": m[1], "hash": h, "keep": keep}
    # T3 = 真孤儿且不在任何重复组（内容全库唯一）
    for p, s in rest.items():
        if p not in seen_in_dup:
            t3[p] = {"size": s}

    for tag, d in (("T1 零损失删", t1), ("T2 冗余副本删", t2), ("T3 唯一份·待判", t3)):
        print("  %s：%d 张 / %.2f MB" % (tag, len(d), sum(v["size"] for v in d.values()) / 1048576))

    print("[3/3] T3 按顶层目录归类...")
    bydir = collections.defaultdict(lambda: [0, 0])
    for p, v in t3.items():
        top = p.split(os.sep)[0] if os.sep in p else "(根目录)"
        bydir[top][0] += 1
        bydir[top][1] += v["size"]
    for k, (n, s) in sorted(bydir.items(), key=lambda x: -x[1][1]):
        print("    %8.2f MB  %6d 张  %s" % (s / 1048576, n, k))

    out = {
        "all_images": len(allimg), "referenced": len(referenced), "orphan": len(orphan),
        "T0_false": t0, "T0n_noise_only": t0n,
        "T1_zeroloss": t1, "T2_redundant": t2, "T3_unique": t3,
        "T3_by_dir": {k: {"n": v[0], "size": v[1]} for k, v in bydir.items()},
    }
    dst = os.path.join(TMP, "orphan_risk.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False)
    print("\n-> " + dst)


if __name__ == "__main__":
    main()
