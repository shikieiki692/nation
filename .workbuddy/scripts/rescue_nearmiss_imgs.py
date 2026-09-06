#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
抢救「形似但名字对不上」的残留缺图引用（still_missing.json）

思路：残留引用分三类
  A 标准 64 位哈希，库内确实没有  -> 真丢失，放弃
  B 十六进制但长度非 64（63/65 居多）-> 差一位，可尝试在同目录找编辑距离1的实文件
  C 非哈希名（占位/语义名）        -> 尝试同目录前缀匹配，否则放弃

用法：
  python rescue_nearmiss_imgs.py            # 预览
  python rescue_nearmiss_imgs.py --apply    # 写回 md
"""
import os, re, sys, json, collections

VAULT = r"C:\Obsidion\妙妙屋"
STILL = os.path.join(VAULT, ".workbuddy", "tmp", "still_missing.json")
APPLY = "--apply" in sys.argv

HEXRE = re.compile(r"^[0-9a-f]+$", re.I)
EXTS = (".jpg", ".jpeg", ".png", ".svg", ".gif", ".webp")


def load_dir_index():
    """dir -> set(basename)，只索引 06-外部资料导入/clayden 有机化学/mineru/media 等图片仓"""
    idx = collections.defaultdict(set)
    roots = []
    for name in ["06-外部资料导入", "07-资料提炼", "clayden 有机化学", "mineru",
                 "media", "媒体仓库", "高中化学竞赛笔记", "结构化学习题与解析",
                 "结构化学基础", "各省预赛题目", "高考化学", "00-附件", "10-附件",
                 "04-题库", "03-知识点", "06-学生侧材料", "08-可视化资源"]:
        p = os.path.join(VAULT, name)
        if os.path.isdir(p):
            roots.append(p)
    for root in roots:
        for r, dirs, files in os.walk(root):
            if ".git" in r:
                continue
            fl = [f for f in files if f.lower().endswith(EXTS)]
            if fl:
                idx[r] = set(fl)
    return idx


def edit1_candidates(name, pool):
    """返回 pool 中与 name 编辑距离 1（含插入/删除 1 字符）的候选"""
    out = []
    for p in pool:
        if p == name:
            continue
        if abs(len(p) - len(name)) > 1:
            continue
        if len(p) == len(name):
            diff = sum(1 for a, b in zip(p, name) if a != b)
            if diff == 1:
                out.append(p)
        else:
            lo, hi = (p, name) if len(p) < len(name) else (name, p)
            i = j = 0
            skipped = False
            ok = True
            while i < len(lo) and j < len(hi):
                if lo[i] == hi[j]:
                    i += 1
                    j += 1
                elif not skipped:
                    skipped = True
                    j += 1
                else:
                    ok = False
                    break
            if ok:
                out.append(p)
    return out


def main():
    data = json.load(open(STILL, encoding="utf-8"))
    print("残留引用 %d 处" % len(data))

    idx = load_dir_index()
    print("图片目录索引 %d 个" % len(idx))

    # basename -> 全部所在目录（用于裸 basename 引用的兜底）
    base2dirs = collections.defaultdict(set)
    for d, s in idx.items():
        for b in s:
            base2dirs[b].add(d)

    plan = []          # (file, raw, kind, new_basename, strategy)
    giveup_a = []
    giveup_c = []

    for rec in data:
        raw = rec["raw"].replace("\\", "/")
        base = rec["basename"]
        stem, ext = os.path.splitext(base)
        # 引用里带的目录（相对 vault 根）
        if "/" in raw:
            dpart = raw.rsplit("/", 1)[0]
        else:
            dpart = None

        pool = None
        if dpart:
            # 同目录优先：raw 里的目录可能相对 vault 根，也可能相对 md 所在目录
            cands = [os.path.join(VAULT, dpart)]
            md_dir = os.path.dirname(os.path.join(VAULT, rec["file"]))
            cands.append(os.path.normpath(os.path.join(md_dir, dpart)))
            for c in cands:
                if c in idx:
                    pool = idx[c]
                    break
        if pool is None:
            # 裸 basename：汇全库同名目录（一般是 _images）
            pool = set()
            for d, s in idx.items():
                if os.path.basename(d).endswith("_images"):
                    pool |= s

        hit = None
        strat = None
        if HEXRE.match(stem):
            if len(stem) == 64:
                giveup_a.append(rec)
                continue
            c1 = edit1_candidates(base, pool)
            if len(c1) == 1:
                hit, strat = c1[0], "edit1"
            elif len(c1) > 1:
                hit, strat = c1[0], "edit1-multi"
        else:
            # 非哈希名：前缀匹配
            pre = stem[:16]
            pre_c = [p for p in pool if p.startswith(pre)]
            if len(pre_c) == 1:
                hit, strat = pre_c[0], "prefix"
            else:
                giveup_c.append(rec)
                continue

        if hit:
            plan.append((rec["file"], raw, rec["kind"], hit, strat))

    print()
    print("=== 可抢救 ===")
    c = collections.Counter(x[4] for x in plan)
    for k, v in c.most_common():
        print("  %-14s %5d" % (k, v))
    print("  合计          %5d" % len(plan))
    print()
    print("=== 放弃 ===")
    print("  A 标准64位但库内无 : %d" % len(giveup_a))
    print("  C 非哈希名无唯一候: %d" % len(giveup_c))

    print()
    print("=== 可抢救样例 ===")
    for row in plan[:15]:
        print("  [%s] %s" % (row[4], os.path.basename(row[1])[:70]))
        print("        -> %s" % row[3][:70])

    json.dump(plan, open(os.path.join(VAULT, ".workbuddy", "tmp", "nearmiss_plan.json"),
                         "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    if not APPLY:
        print()
        print("(dry-run, 加 --apply 写回)")
        return

    # 写回
    rewrite = collections.defaultdict(list)
    for f, raw, kind, newbase, strat in plan:
        rewrite[f].append((raw, newbase, kind))

    n_file = n_ref = 0
    for f, items in rewrite.items():
        p = os.path.join(VAULT, f)
        if not os.path.isfile(p):
            continue
        # newline="" 关闭通用换行转换：读时不把 CRLF 折叠成 LF，
        # 写时也不把 LF 展开成 CRLF。否则整文件行尾被改写，
        # git diff 会炸出几万行噪音。
        t = open(p, encoding="utf-8", newline="").read()
        orig = t
        for raw, newbase, kind in items:
            if kind == "wiki":
                t = t.replace("![[%s]]" % raw, "![[%s]]" % newbase)
                t = t.replace("![[%s|" % raw, "![[%s|" % newbase)
            else:
                t = t.replace("](%s)" % raw, "](%s)" % newbase)
            n_ref += 1
        if t != orig:
            open(p, "w", encoding="utf-8", newline="").write(t)
            n_file += 1
    print()
    print("[写回] %d 个 md，%d 处引用" % (n_file, n_ref))


if __name__ == "__main__":
    main()
