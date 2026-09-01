#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
修复「路径写错但文件还在」的图片引用（audit_missing_images_v2 的 R3/R4）
------------------------------------------------------------------------
R3：basename 全库唯一命中（例：引用 35届初赛试题解析_images/x.jpg，
    实际文件在 mineru\02-真题解析\35届初赛试题解析_images\x.jpg）
R4：basename 全库多处命中（这些是 64 位哈希名，各副本内容逐字节一致，任选其一）

统一处置（对齐 00-首页/规则-配图来源优先级.md）：
    把图复制进 媒体仓库/，引用改写为 ![[basename]] —— vault 的标准写法。
    源文件一律保留，不删。

用法：
    python fix_broken_img_refs.py           # dry-run
    python fix_broken_img_refs.py --apply
"""
import os, sys, json, shutil, collections, re

VAULT = r"C:\Obsidion\妙妙屋"
MEDIA = os.path.join(VAULT, "媒体仓库")
MISSING = os.path.join(VAULT, ".workbuddy", "tmp", "missing_img_v2.json")

APPLY = "--apply" in sys.argv


def main():
    d = json.load(open(MISSING, encoding="utf-8"))
    targets = [x for x in d["unresolved"] if x["cls"] in ("R3", "R4")]
    print("[清单] R3/R4 共 %d 处" % len(targets))

    copied = skipped = nostd = 0
    conflicts = []
    rewrite = collections.defaultdict(list)   # md -> [(kind, old, new)]
    total_bytes = 0

    for rec in targets:
        if not rec["candidates"]:
            nostd += 1
            continue
        src_rel = rec["candidates"][0]              # 内容一致，取第一个即可
        src = os.path.join(VAULT, src_rel)
        if not os.path.isfile(src):
            nostd += 1
            continue

        base = rec["basename"]
        dst = os.path.join(MEDIA, base)
        new_ref = "![[%s]]" % base

        if os.path.isfile(dst):
            if os.path.getsize(dst) == os.path.getsize(src):
                skipped += 1
            else:
                conflicts.append((base, os.path.getsize(dst), os.path.getsize(src)))
                continue
        else:
            if APPLY:
                os.makedirs(MEDIA, exist_ok=True)
                shutil.copy2(src, dst)
            copied += 1
            total_bytes += os.path.getsize(src)

        rewrite[rec["file"]].append((rec["kind"], rec["raw"], new_ref))

    print("[规划] 复制到媒体仓库 %d（已存在跳过 %d），改写 %d 个 md"
          % (copied, skipped, len(rewrite)))
    print("[规划] 体积 %.2f MB" % (total_bytes / 1048576))
    if conflicts:
        print("[冲突] %d 个同名但大小不同，已跳过：" % len(conflicts))
        for b, a, c in conflicts[:8]:
            print("   %s 媒体仓库=%d 源=%d" % (b, a, c))
    if nostd:
        print("[跳过] %d 处候选文件不存在" % nostd)

    if not APPLY:
        print("\n*** dry-run，未写入。加 --apply 执行 ***")
        return

    n_ref = 0
    for md_rel, items in rewrite.items():
        md_abs = os.path.join(VAULT, md_rel)
        text = open(md_abs, encoding="utf-8").read()
        orig = text
        for kind, old, _new in items:
            base = os.path.basename(old)
            if kind == "wiki":
                # wiki 语法：! [[old]] -> ! [[base]]
                pat = re.compile(r"!\[\[(" + re.escape(old) + r")\]\]")
            else:
                # md 语法：! [任意](old) -> ! [[base|任意]]
                # 保留原图注作为新 wiki 语法的别名，alt 含 ] 或 | 时丢弃
                pat = re.compile(r"!\[([^\]]*)\]\(" + re.escape(old) + r"\)")
            def _repl(m):
                if kind == "wiki":
                    return "![[%s]]" % base
                alt = m.group(1)
                if alt and "]" not in alt and "|" not in alt:
                    return "![[%s|%s]]" % (base, alt)
                return "![[%s]]" % base
            text = pat.sub(_repl, text)
            n_ref += 1
        if text != orig:
            open(md_abs, "w", encoding="utf-8").write(text)
    print("[改写] 更新 %d 个 md，%d 处引用" % (len(rewrite), n_ref))


if __name__ == "__main__":
    main()
