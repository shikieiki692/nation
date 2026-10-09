# -*- coding: utf-8 -*-
"""清理：仓库根目录的 0 字节事故文件 ＋ 本次会话临时产物（只删明确垃圾，带清单与体积核对）。"""
import glob
import json
import os
import shutil
import sys

R = r"C:\Obsidion\妙妙屋"
APPLY = "--apply" in sys.argv

# ① 根目录 0 字节事故文件（重定向/heredoc 误写产物；均 0 字节，无内容损失）
STRAY = ["全库可用率", "承接", "本线于", "[!warning]", "\uf02a\uf02a答案\uf02a\uf02a："]
# ② 根目录 .tmp（仅两个失败推送日志）
TMPDIR = ".tmp"
# ③ 本次会话临时产物
MINE = [
    ".workbuddy/tmp/dpi_ab",
    ".workbuddy/tmp/opt_pipe/render_out/xiv_stu_old",
    ".workbuddy/tmp/opt_pipe/render_out/xiv_stu_new",
    ".workbuddy/tmp/opt_pipe/render_out/xiv_ans_old",
    ".workbuddy/tmp/opt_pipe/render_out/xiv_ans_new",
    ".workbuddy/tmp/opt_pipe/render_out/xip19",
    ".workbuddy/tmp/opt_pipe/render_out/xip24",
    ".workbuddy/tmp/opt_pipe/render_out/xi14",
    ".workbuddy/tmp/opt_pipe/render_out/xia31",
]

manifest = {"stray_files": [], "tmpdir": [], "mine_dirs": []}
freed = 0

print("== ① 根目录 0 字节事故文件 ==")
for n in STRAY:
    p = os.path.join(R, n)
    if os.path.exists(p):
        sz = os.path.getsize(p)
        manifest["stray_files"].append({"name": repr(n), "size": sz})
        print("   %-24s %d 字节  ⇒ 删" % (repr(n), sz))
        if sz != 0:
            print("   ⛔ 非 0 字节，跳过（需人工核）")
            continue
        if APPLY:
            os.remove(p)
    else:
        print("   %-24s （不存在，跳过）" % repr(n))

print("== ② .tmp/ ==")
td = os.path.join(R, TMPDIR)
if os.path.isdir(td):
    for dp, dn, fn in os.walk(td):
        for f in fn:
            fp = os.path.join(dp, f)
            manifest["tmpdir"].append({"path": os.path.relpath(fp, R), "size": os.path.getsize(fp)})
            freed += os.path.getsize(fp)
    print("   文件 %d 个 共 %d 字节" % (len(manifest["tmpdir"]), freed))
    if APPLY:
        shutil.rmtree(td)

print("== ③ 本会话临时产物 ==")
for d in MINE:
    p = os.path.join(R, d)
    if os.path.exists(p):
        sz = 0
        n = 0
        for dp, dn, fn in os.walk(p):
            for f in fn:
                sz += os.path.getsize(os.path.join(dp, f)); n += 1
        manifest["mine_dirs"].append({"path": d, "files": n, "bytes": sz})
        print("   %-58s %3d 文件 %8.2f MB" % (d, n, sz / 1048576))
        if APPLY:
            shutil.rmtree(p)
    else:
        print("   %-58s （不存在）" % d)

if APPLY:
    with open(os.path.join(R, ".workbuddy/tmp/_cleanup_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print("\n已写入清单 .workbuddy/tmp/_cleanup_manifest.json")
else:
    print("\n(dry-run；加 --apply 执行)")
