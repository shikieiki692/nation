# -*- coding: utf-8 -*-
"""
阶段2 删除清单构建 + 删除前严格校验

只纳入「信息零损失」的两类：
  T1 孤儿图的内容 == 某个被 md 引用的图的内容  -> 删它，同样的图还在库里
  T2 真孤儿，但同内容还有其他孤儿副本        -> 只删冗余份，每组保留 1 份

校验项（任一不过关就剔除，不进清单）：
  1. 内容保留方（twin / keep）在磁盘上真实存在
  2. 内容保留方不在本次删除名单里（防止两个副本互删、全组清空）
  3. 待删文件本身存在
  4. 待删文件不是被非 md 容器真引用的 T0（双保险）

用法：
  python .workbuddy/scripts/build_stage2_manifest.py [--execute]
不加 --execute 只生成清单并打印校验报告。
"""
import os, sys, json, collections

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.join(VAULT, ".workbuddy", "tmp")


def main(execute=False):
    risk = json.load(open(os.path.join(TMP, "orphan_risk.json"), encoding="utf-8"))
    t1 = risk["T1_zeroloss"]
    t2 = risk["T2_redundant"]
    t0 = set(risk["T0_false"].keys())

    # ---- 先收集全部待删路径，再统一校验（避免边删边判）----
    cand = {}   # path -> (tag, keeper)
    for p, v in t1.items():
        cand[p] = ("T1", v["twin"])
    for p, v in t2.items():
        cand[p] = ("T2", v["keep"])

    del_set = set(cand.keys())
    ok, bad = {}, collections.Counter()

    for p, (tag, keeper) in cand.items():
        fp = os.path.join(VAULT, p)
        kp = os.path.join(VAULT, keeper)
        if p in t0:
            bad["命中 T0 真引用，跳过"] += 1
            continue
        if not os.path.isfile(fp):
            bad["待删文件不存在"] += 1
            continue
        if not os.path.isfile(kp):
            bad["内容保留方不存在"] += 1
            continue
        if keeper in del_set:
            bad["保留方也被列入删除"] += 1
            continue
        ok[p] = (tag, keeper, os.path.getsize(fp))

    n1 = sum(1 for v in ok.values() if v[0] == "T1")
    n2 = sum(1 for v in ok.values() if v[0] == "T2")
    s1 = sum(v[2] for v in ok.values() if v[0] == "T1")
    s2 = sum(v[2] for v in ok.values() if v[0] == "T2")

    print("=" * 70)
    print("候选 T1 %d + T2 %d = %d" % (len(t1), len(t2), len(cand)))
    print("校验剔除：")
    for k, v in bad.items():
        print("    %-24s %d" % (k, v))
    print("-" * 70)
    print("通过校验：T1 %d 张 / %.2f MB" % (n1, s1 / 1048576))
    print("         T2 %d 张 / %.2f MB" % (n2, s2 / 1048576))
    print("      合计 %d 张 / %.2f MB" % (len(ok), (s1 + s2) / 1048576))

    # 按顶层目录
    by = collections.defaultdict(lambda: [0, 0])
    for p, v in ok.items():
        t = p.split(os.sep)[0] if os.sep in p else "(根)"
        by[t][0] += 1
        by[t][1] += v[2]
    print("-" * 70)
    print("按顶层目录 top12：")
    for k, (n, s) in sorted(by.items(), key=lambda x: -x[1][1])[:12]:
        print("    %8.2f MB  %5d 张  %s" % (s / 1048576, n, k))

    out = os.path.join(TMP, "cleanup_stage2.txt")
    with open(out, "w", encoding="utf-8") as f:
        for p in sorted(ok):
            f.write(os.path.join(VAULT, p) + "\n")
    print("\n清单 -> %s（%d 行）" % (out, len(ok)))

    if execute:
        print("\n[执行] 调用 trash_files.py 送回收站...")
        import subprocess
        r = subprocess.run([sys.executable, os.path.join(VAULT, ".workbuddy", "scripts", "trash_files.py"),
                            out], cwd=VAULT, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        print(r.stdout[-4000:])
        if r.stderr:
            print("STDERR:", r.stderr[-2000:])
    else:
        print("\n（未加 --execute，仅生成清单）")


if __name__ == "__main__":
    main(execute="--execute" in sys.argv)
