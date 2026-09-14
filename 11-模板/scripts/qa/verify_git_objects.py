#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""git 对象库「可信判据」复核。

背景：本仓库 fsck 不可信 —— 畸形 pack 的 .idx 空登记会让 fsck 漏报缺失，
唯一可信判据是 `git cat-file -e`（09-13 已定论）。promisor 未取消时还会制造"假绿"。

本脚本做两件事：
  A. 全覆盖交叉验证：把 `git rev-list --objects --all` 的全部可达对象喂给
     `git cat-file --batch-check`，统计 missing（batch-check 对不存在的对象会输出
     `<sha> missing`，这是全覆盖判定，比抽样强）。
  B. 分层抽样逐对象校验：按 commit/tree/blob 分层抽样（默认 800，>=500），
     对每个抽样 SHA 单独跑 `git cat-file -e`（逐对象子进程，与 A 交叉验证）。

用法:
    python -X utf8 11-模板/scripts/qa/verify_git_objects.py [--sample 800] [--seed 20260915]

退出码: 0 = 全部可读（不可读=0）；1 = 存在不可读对象（需走三源恢复）；2 = 脚本自身出错。
"""
import argparse
import collections
import random
import subprocess
import sys


def run(args, **kw):
    return subprocess.run(
        args, capture_output=True, text=True,
        encoding="utf-8", errors="replace", **kw
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=800, help="分层抽样总数（>=500）")
    ap.add_argument("--seed", type=int, default=20260915, help="随机种子（可复现）")
    args = ap.parse_args()

    seed = args.seed
    print("=" * 68)
    print("git 对象库可信判据复核（判据 = git cat-file -e）")
    print("=" * 68)

    # 0) 前置：promisor / gc / lock
    problems = []
    for k in ("remote.origin.promisor", "remote.origin.partialclonefilter"):
        v = run(["git", "config", "--get", k]).stdout.strip()
        print(f"[config] {k} = {v if v else '(未设置, 正常)'}")
        if v:
            problems.append(f"{k} 未取消 → 会制造假绿")
    if problems:
        for p in problems:
            print(f"  !! {p}", file=sys.stderr)
        print("[ABORT] 请先取消 promisor 再复核。", file=sys.stderr)
        return 2

    # 1) 可达对象全集
    r = run(["git", "rev-list", "--objects", "--all"])
    if r.returncode != 0:
        print("[ERROR] git rev-list 失败:\n" + r.stderr, file=sys.stderr)
        return 2
    shas = [ln.split()[0] for ln in r.stdout.splitlines() if ln.strip()]
    print(f"[rev-list] 可达对象 = {len(shas)}")

    # 2) 全覆盖 batch-check
    inp = "\n".join(shas) + "\n"
    r = run(["git", "cat-file", "--batch-check", "--buffer"], input=inp)
    if r.returncode != 0:
        print("[ERROR] cat-file --batch-check 失败:\n" + r.stderr, file=sys.stderr)
        return 2
    types = collections.Counter()
    by_type = collections.defaultdict(list)
    missing_full = []
    for ln in r.stdout.splitlines():
        parts = ln.split()
        if not parts:
            continue
        if len(parts) >= 2 and parts[1] == "missing":
            missing_full.append(parts[0])
            continue
        if len(parts) >= 3:
            sha, typ = parts[0], parts[1]
            types[typ] += 1
            by_type[typ].append(sha)
    print(f"[batch-check] 类型分布 = {dict(types)}")
    print(f"[batch-check] 不可读(missing) = {len(missing_full)}  (全覆盖)")
    if missing_full:
        print("  前 20 个:", missing_full[:20])

    # 3) 分层抽样（commit/tree/blob 各占一定比例）
    alloc = [("commit", 0.25), ("tree", 0.25), ("blob", 0.50)]
    random.seed(seed)
    sampled = {}   # sha -> type
    plan = {}
    for typ, frac in alloc:
        pop = by_type.get(typ, [])
        n = min(len(pop), max(1, round(args.sample * frac))) if pop else 0
        plan[typ] = n
        for sha in random.sample(pop, n):
            sampled[sha] = typ
    total_n = sum(plan.values())
    print(f"[抽样] seed={seed} 计划 = {plan}  合计 = {total_n}")

    # 4) 逐个 cat-file -e
    bad = []
    for i, (sha, typ) in enumerate(sampled.items(), 1):
        rc = subprocess.run(
            ["git", "cat-file", "-e", sha],
            capture_output=True
        ).returncode
        if rc != 0:
            bad.append((sha, typ, rc))
        if i % 200 == 0:
            print(f"  ... 已验 {i}/{total_n}")

    print("-" * 68)
    print(f"[抽样逐对象 cat-file -e] 已验 = {total_n}, 不可读 = {len(bad)}")
    if bad:
        for sha, typ, rc in bad[:20]:
            print(f"  BAD: {sha} ({typ}) rc={rc}")

    unreadable = len(missing_full) + len(bad)
    print("-" * 68)
    print(f"[结论] 全覆盖 missing={len(missing_full)} + 抽样不可读={len(bad)} "
          f"→ 总不可读 = {unreadable}")
    print("[结论] " + ("✅ 通过（不可读 = 0）" if unreadable == 0
                       else "❌ 未通过 → 走三源恢复"))
    print("=" * 68)
    return 0 if unreadable == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
