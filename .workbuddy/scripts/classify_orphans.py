#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
把孤儿图按「可安全清理等级」分类，输出回收清单（只读，不删任何东西）

等级
  S 立即删   : 渲染产物 / PPTX 解压残留 / node_modules / work_old 备份
  A 可删     : 孤儿图中体积 >= 阈值 或 位于明确"未启用"目录（如（已压缩））
  B 待确认   : 孤儿图，但属于来源仓（可能是还没引用到的素材）
  C 不建议删 : 孤儿图但在 媒体仓库（Obsidian 主用仓，删了可能影响未来引用）
"""
import os, re, json, collections

VAULT = r"C:\Obsidion\妙妙屋"
SRC = os.path.join(VAULT, ".workbuddy", "tmp", "image_usage.json")
OUT = os.path.join(VAULT, ".workbuddy", "tmp", "orphan_classified.json")

# S 级：纯产物，可重建
S_PAT = re.compile(r"(_render|_render_preview|/ppt/media/|node_modules|"
                   r"work_old_\d+|/_qa_render|/thumbs?/)", re.I)
# 明确未启用的素材目录
A_DIR_PAT = re.compile(r"（已压缩）|（教师用）|_archive|备份", re.I)


def hsize(n):
    if n >= 1 << 30:
        return "%.2f GB" % (n / (1 << 30))
    if n >= 1 << 20:
        return "%.2f MB" % (n / (1 << 20))
    return "%.1f KB" % (n / 1024)


def main():
    d = json.load(open(SRC, encoding="utf-8"))
    orph = d["orphan"]
    print("孤儿图 %d 张 / %s" % (len(orph), hsize(sum(x["size"] for x in orph))))

    buckets = collections.defaultdict(list)
    for x in orph:
        p = x["path"].replace("\\", "/")
        if S_PAT.search(p):
            buckets["S"].append(x)
        elif A_DIR_PAT.search(p):
            buckets["A"].append(x)
        elif p.startswith("媒体仓库/"):
            buckets["C"].append(x)
        else:
            buckets["B"].append(x)

    print()
    print("%-3s %-8s %8s %10s   %s" % ("级", "说明", "张数", "体积", "典型路径"))
    desc = {"S": "产物可重建", "A": "未启用素材", "B": "来源仓待查", "C": "媒体仓库"}
    total = 0
    for k in ["S", "A", "B", "C"]:
        v = buckets.get(k, [])
        s = sum(x["size"] for x in v)
        total += s if k in ("S", "A") else 0
        sample = v[0]["path"] if v else ""
        print("%-3s %-8s %8d %10s   %s"
              % (k, desc[k], len(v), hsize(s), sample[:60]))

    print()
    print("S+A 可直接回收：%s" % hsize(total))

    # S 级按目录聚合
    print()
    print("=== S 级按目录 top12 ===")
    sd = collections.defaultdict(lambda: [0, 0])
    for x in buckets.get("S", []):
        p = x["path"].replace("\\", "/")
        key = "/".join(p.split("/")[:3])
        sd[key][0] += 1
        sd[key][1] += x["size"]
    for k, (n, s) in sorted(sd.items(), key=lambda kv: -kv[1][1])[:12]:
        print("  %6d 张 %10s  %s" % (n, hsize(s), k))

    # B 级按顶层目录
    print()
    print("=== B 级（来源仓孤儿）按顶层目录 top12 ===")
    bd = collections.defaultdict(lambda: [0, 0])
    for x in buckets.get("B", []):
        p = x["path"].replace("\\", "/")
        key = p.split("/")[0]
        bd[key][0] += 1
        bd[key][1] += x["size"]
    for k, (n, s) in sorted(bd.items(), key=lambda kv: -kv[1][1])[:12]:
        print("  %6d 张 %10s  %s" % (n, hsize(s), k))

    # 大文件清单（>=500KB）
    big = sorted([x for x in orph if x["size"] >= 500 * 1024],
                 key=lambda x: -x["size"])
    print()
    print("=== 单张 >=500KB 的孤儿 top15 ===")
    for x in big[:15]:
        print("  %9s  %s" % (hsize(x["size"]), x["path"][:80]))
    print("  (>=500KB 共 %d 张 / %s)" % (len(big), hsize(sum(x["size"] for x in big))))

    json.dump({k: v for k, v in buckets.items()},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    print()
    print("分类清单 ->", OUT)


if __name__ == "__main__":
    main()
