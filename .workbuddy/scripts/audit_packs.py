# -*- coding: utf-8 -*-
"""按 09-13 任务卡判据体检全部 pack：
畸形特征 = 「对象数极少但体积巨大」且其对象 cat-file -e 失败。
同时抽样 cat-file -e 交叉验证（fsck 在本仓库不可信）。"""
import os, sys, glob, subprocess
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"c:\Obsidion\妙妙屋")


def cat_e(sha):
    return subprocess.run(["git", "cat-file", "-e", sha], capture_output=True).returncode == 0


rows = []
for idx in sorted(glob.glob(".git/objects/pack/*.idx")):
    pack = idx[:-4] + ".pack"
    if not os.path.exists(pack):
        rows.append(("NO_PACK", os.path.basename(pack), 0, 0, 0, 0))
        continue
    size = os.path.getsize(pack)
    out = subprocess.run(["git", "show-index"], stdin=open(idx, "rb"),
                         capture_output=True).stdout.decode("utf-8", errors="replace")
    lines = [l for l in out.strip().split("\n") if l.strip()]
    n = len(lines)
    # 抽样 3 个对象做 cat-file -e
    shas = [l.split()[1] for l in lines[:2]] + [l.split()[1] for l in lines[-1:]]
    ok = sum(1 for s in shas if cat_e(s))
    rows.append(("OK", os.path.basename(pack), n, size, ok, len(shas)))

tot_obj = sum(r[2] for r in rows)
print("pack 数 %d，登记对象合计 %d" % (len(rows), tot_obj))
print()
# 按体积排序看头部
rows.sort(key=lambda r: -r[3])
print("%-52s %10s %12s %s" % ("pack", "对象数", "体积MB", "抽样可读"))
for st, name, n, size, ok, tot in rows[:12]:
    print("%-52s %10d %12.2f %d/%d" % (name[:50], n, size / 1048576, ok, tot))
print("...")
print()
# 畸形候选：对象数<=1000 且 体积>50MB  或  抽样有不可读
sus = [r for r in rows if (r[2] <= 1000 and r[3] > 50 * 1048576) or r[4] < r[5]]
print("⚠️ 畸形/异常候选 %d 个：" % len(sus))
for st, name, n, size, ok, tot in sus[:20]:
    print("   %s  objs=%d  %.2fMB  可读 %d/%d" % (name, n, size / 1048576, ok, tot))
# 小 pack 统计
tiny = [r for r in rows if r[2] <= 5 and r[3] < 1024 * 1024]
print()
print("微型 pack（≤5 对象、<1MB）: %d 个，合计 %.2f MB"
      % (len(tiny), sum(r[3] for r in tiny) / 1048576))
