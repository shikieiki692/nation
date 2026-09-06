#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从 git 历史恢复"工作区缺失但曾入库"的图片
------------------------------------------
背景：一批视频课笔记（学而思 / Zchem / 质心）导入 vault 时，md 进来了、
      图片 `*_笔记_images/` 没落盘。全库扫描确认 basename 不存在，
      但 git 历史里这些 blob 还在（图片入库后被误删 / 目录迁移时漏拷）。

做法：
  1. 用 `git rev-list --objects --all` 建 basename -> blob sha 索引
  2. 对照 audit_missing_images_v2.py 产出的缺失清单
  3. 按引用形态决定落盘位置：
     - 带目录的引用  `xx_images/hash.jpg`  -> 恢复到 <md所在目录>/xx_images/hash.jpg（原位）
     - 裸 basename   `hash.jpg`            -> 恢复到 媒体仓库/hash.jpg，引用改写 ![[hash.jpg]]
  4. 用 `git cat-file --batch` 流式取 blob（避免 9000 次进程调用）

用法：
  python recover_images_from_git.py            # dry-run
  python recover_images_from_git.py --apply    # 真正写入
"""
import os, re, sys, json, subprocess, collections

VAULT = r"C:\Obsidion\妙妙屋"
OBJLIST = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\allobj.txt"
MISSING = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\missing_img_v2.json"
MEDIA = os.path.join(VAULT, "媒体仓库")
IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp", ".tif", ".tiff"}
GITQUOTE = ["-c", "core.quotepath=false"]

APPLY = "--apply" in sys.argv


def git(*args):
    return subprocess.run(["git"] + GITQUOTE + list(args), cwd=VAULT,
                          capture_output=True)


def build_sha_index():
    """basename -> blob sha（取最后一次出现的）"""
    idx = {}
    n = 0
    with open(OBJLIST, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.rstrip("\n").split(" ", 1)
            if len(parts) != 2:
                continue
            sha, path = parts
            if os.path.splitext(path)[1].lower() not in IMG_EXT:
                continue
            idx[os.path.basename(path)] = sha
            n += 1
    return idx, n


def main():
    if not os.path.isfile(OBJLIST):
        sys.exit("缺少 %s，先跑：git -c core.quotepath=false rev-list --objects --all > %s"
                 % (OBJLIST, OBJLIST))

    sha_idx, n_obj = build_sha_index()
    print("[git] 历史中图片对象 %d 个，去重 basename %d 个" % (n_obj, len(sha_idx)))

    d = json.load(open(MISSING, encoding="utf-8"))
    unresolved = d["unresolved"]
    print("[清单] 未解析引用 %d 处" % len(unresolved))

    # ---- 规划落盘位置 ----
    plan = []          # (sha, 目标绝对路径, rec)
    no_blob = []       # git 里也没有
    rewrite = []       # 需要改写引用的 (file, old, new)

    for rec in unresolved:
        # R3/R4 库内已有同名文件（只是路径写错），走 fix_broken_img_refs.py 的
        # "改路径"路线，不从 git 恢复——避免覆盖掉库内可能已被修改过的版本
        if rec["cls"] in ("R3", "R4"):
            continue

        base = rec["basename"]
        sha = sha_idx.get(base)
        if not sha:
            no_blob.append(rec)
            continue

        md_rel = rec["file"]
        md_abs = os.path.join(VAULT, md_rel)
        md_dir = os.path.dirname(md_abs)
        raw = rec["raw"].replace("\\", "/")

        if "/" in raw:
            # 带目录的引用 -> 原位恢复（相对 md 所在目录）
            dst = os.path.normpath(os.path.join(md_dir, raw))
            new_ref = None
        else:
            # 裸 basename -> 进媒体仓库，引用改写为 wiki 语法
            dst = os.path.join(MEDIA, base)
            new_ref = "![[%s]]" % base

        plan.append((sha, dst, rec))
        if new_ref:
            rewrite.append((md_rel, rec["kind"], raw, new_ref))

    # 去重（同一 dst 可能来自多条引用）
    uniq = {}
    for sha, dst, rec in plan:
        uniq.setdefault(dst, (sha, rec))
    print("\n[规划] 可恢复 %d 处引用 -> %d 个唯一图片文件" % (len(plan), len(uniq)))
    print("[规划] git 历史中也没有：%d 处" % len(no_blob))
    print("[规划] 需改写引用（裸 basename 进媒体仓库）：%d 处" % len(rewrite))

    # 按 cls 细分
    cc = collections.Counter(r["cls"] for _, _, r in plan)
    print("[规划] 按分类：%s" % dict(cc))

    if not APPLY:
        print("\n*** dry-run，未写入任何文件。加 --apply 执行 ***")
        return

    # ---- 提取 blob ----
    os.makedirs(MEDIA, exist_ok=True)
    want = [(dst, sha) for dst, (sha, rec) in uniq.items()]
    shas = [s for _, s in want]
    print("\n[提取] 批量取 %d 个 blob ..." % len(shas))

    # 注意：不能用 PIPE 双向通信——9000 个 blob 的输出会撑满管道缓冲区，
    # git 阻塞在写 stdout、我阻塞在写 stdin，直接死锁（实测被 SIGTERM 杀掉）。
    # 改成 stdin/stdout 全走文件。
    tmpdir = os.path.join(VAULT, ".workbuddy", "tmp")
    os.makedirs(tmpdir, exist_ok=True)
    sha_f = os.path.join(tmpdir, "shas.txt")
    bin_f = os.path.join(tmpdir, "blobs.bin")
    with open(sha_f, "w", encoding="utf-8") as f:
        f.write("\n".join(shas) + "\n")

    with open(sha_f, "r", encoding="utf-8") as fin, open(bin_f, "wb") as fout:
        subprocess.run(["git"] + GITQUOTE + ["cat-file", "--batch"],
                       cwd=VAULT, stdin=fin, stdout=fout, check=True)
    print("[提取] git cat-file 完成，%.1f MB" % (os.path.getsize(bin_f) / 1048576))

    written = skipped = failed = 0
    conflicts = []
    total_bytes = 0
    fp = open(bin_f, "rb")
    for dst, sha in want:
        header = fp.readline().decode("utf-8", "replace").strip()
        hparts = header.split()
        if len(hparts) != 3:
            failed += 1
            continue
        size = int(hparts[2])
        data = fp.read(size)
        fp.read(1)  # trailing newline

        if os.path.isfile(dst):
            if os.path.getsize(dst) == size:
                skipped += 1
            else:
                conflicts.append((dst, size, os.path.getsize(dst)))
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as f:
            f.write(data)
        written += 1
        total_bytes += len(data)
        if written % 2000 == 0:
            print("   ...%d" % written)
    fp.close()
    os.remove(bin_f)
    os.remove(sha_f)

    print("[提取] 写入 %d，已存在跳过 %d，失败 %d，共 %.2f MB"
          % (written, skipped, failed, total_bytes / 1048576))
    if conflicts:
        print("[冲突] %d 个同名但大小不同（未覆盖）：" % len(conflicts))
        for dst, ns, os_ in conflicts[:10]:
            print("   %s  git=%d  现有=%d" % (dst, ns, os_))

    # ---- 改写裸 basename 引用 ----
    if rewrite:
        byfile = collections.defaultdict(list)
        for md_rel, kind, old, new in rewrite:
            byfile[md_rel].append((kind, old, new))
        n_re = 0
        for md_rel, items in byfile.items():
            md_abs = os.path.join(VAULT, md_rel)
            text = open(md_abs, encoding="utf-8").read()
            orig = text
            for kind, old, new in items:
                if kind == "md":
                    text = text.replace("![](%s)" % old, new)
                else:
                    text = text.replace("![[%s]]" % old, new)
            if text != orig:
                open(md_abs, "w", encoding="utf-8").write(text)
                n_re += 1
        print("[改写] 更新 %d 个 md，%d 处引用" % (n_re, len(rewrite)))

    # ---- 记录仍未解决 ----
    if no_blob:
        out = os.path.join(VAULT, ".workbuddy", "tmp", "still_missing.json")
        json.dump(no_blob, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("[残留] git 中也找不到的 %d 处 -> %s" % (len(no_blob), out))


if __name__ == "__main__":
    main()
