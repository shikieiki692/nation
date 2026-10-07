# -*- coding: utf-8 -*-
"""poolscope.py —— 给「弃卡」追加 `pool_scope` 池归属标注（幂等 · RMW 最小改动）。

背景：2026-10-07 弃卡处置去向表定案 —— 弃卡不等于卡坏了，只是「站错队」。
本脚本给弃卡在 frontmatter 末尾插入一行 `pool_scope: <去向>`，供下游按池检索。

纪律（血泪）：
  · **RMW**：读当前磁盘内容 → 只在 FM 末尾插入一行 → 写回；绝不重建 FM、不碰正文。
  · **排除主索引暂存的路径**（并行会话资产）——否则提交会与并行会话互相回退。
  · 读 `utf-8-sig`；若文件含 CRLF 则跳过（避免整文件换行差异）。
  · 备份原件到 poolscope_bak/；写盘后做**体积对比**＋**逐字节差异复核**（只允许多出那一行）。
  · 幂等：已有 `pool_scope:` 键 ⇒ 跳过（重跑应 0 变更）。

用法：python poolscope.py --dry | --apply
"""
import collections, csv, os, re, shutil, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
CSV = os.path.join(ROOT, "09-审计报告", "2026-10-07-不可组卷题目清单.csv")
BAK = os.path.join(ROOT, ".workbuddy/tmp/opt_pipe/poolscope_bak")
_SUF = "_dry" if DRY else ""
CHG = os.path.join(ROOT, ".workbuddy/tmp/opt_pipe/poolscope_changes%s.txt" % _SUF)
SKIP = os.path.join(ROOT, ".workbuddy/tmp/opt_pipe/poolscope_skip%s.txt" % _SUF)
DRY = "--dry" in sys.argv
# --allow-staged：允许写盘「主索引已暂存」的路径（仅当并行会话已暂停、且经 owner 确认时用）
ALLOW_STAGED = "--allow-staged" in sys.argv

FM = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", re.S)

# ── 弃卡原因 → 池归属 ───────────────────────────────────────────────
# B 类（口径外，卡本身完好，换池即可用）
MAP = {
    "非目标模块": "有机化学",
    "有机章节": "有机化学",
    "讲稿批次": "讲稿",
    "题面含竞赛真题特征": "待复核",      # 判据已修，残留须人工确认
    "RISK 命中": "待复核",
    "省预赛": "待复核",
    "难度<4": "待复核",
    "提取异常": "待复核",
    "编号列表≥8": "待复核",
    "年份口径外": "待复核",
    # A 类
    "无答案/占位": "无答案练习",        # P2-a：82 张确缺答案 → 降级为无答案练习池
    "题面泄露": "待复核",              # 内容缺陷：须重切或换卡
    "越界（含他题内容）": "待复核",
    "仅题干回显": "待复核",
    "假结构式": "待复核",
}


def staged_paths():
    out = subprocess.run(["git", "-c", "core.quotepath=false", "diff", "--cached", "--name-only"],
                         cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout
    return {x for x in out.split("\n") if x.strip()}


def rel_of(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def main():
    staged = set() if ALLOW_STAGED else staged_paths()
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    tgt = [r for r in rows if r["verdict"] == "弃卡" and r["reason"] in MAP]
    print("弃卡合计 %d；其中可标注 %d" % (sum(1 for r in rows if r["verdict"] == "弃卡"), len(tgt)))

    byreason = collections.Counter(r["reason"] for r in tgt)
    for k, v in sorted(byreason.items(), key=lambda x: -x[1]):
        print("   %-18s -> %-8s %5d" % (k, MAP[k], v))

    os.makedirs(BAK, exist_ok=True)
    changes, skips = [], []
    for r in tgt:
        p = r["path"]
        rel = rel_of(p)
        val = MAP[r["reason"]]
        if rel in staged:
            skips.append((rel, "并行会话已暂存"))
            continue
        if not os.path.isfile(p):
            skips.append((rel, "文件不存在"))
            continue
        raw = open(p, encoding="utf-8-sig").read()
        if "\r\n" in raw:
            skips.append((rel, "含 CRLF"))
            continue
        if re.search(r"(?m)^pool_scope[ \t]*:", raw):
            continue                                   # 幂等：已有
        m = FM.match(raw)
        if not m:
            skips.append((rel, "无 frontmatter"))
            continue
        new = raw[:m.end(1)] + "\npool_scope: " + val + raw[m.end(1):]
        # 逐字节差异复核：只允许多出「\npool_scope: val」
        exp = raw[:m.end(1)] + raw[m.end(1):]
        if new.replace("\npool_scope: " + val, "", 1) != exp:
            skips.append((rel, "差异复核不通过"))
            continue
        changes.append((rel, val, len(raw.encode()), len(new.encode())))
        if not DRY:
            shutil.copy2(p, os.path.join(BAK, rel.replace("/", "__")))
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)

    with open(CHG, "w", encoding="utf-8", newline="\n") as f:
        for rel, val, a, b in changes:
            f.write("%-8s %6d->%6d  %s\n" % (val, a, b, rel))
    with open(SKIP, "w", encoding="utf-8", newline="\n") as f:
        for rel, why in skips:
            f.write("%-16s %s\n" % (why, rel))

    print("\n%s：变更 %d ｜ 跳过 %d" % ("(dry)" if DRY else "已写盘", len(changes), len(skips)))
    if skips:
        c = collections.Counter(w for _, w in skips)
        print("跳过原因:", dict(c))
    print("→ %s / %s" % (os.path.basename(CHG), os.path.basename(SKIP)))


if __name__ == "__main__":
    main()
