#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
补弱卷生成器（失分复盘 → 定向补弱，grill 定稿 2026-09-02）。

降档链式抽题：测试题档(竞赛) → 习题书档(拓展) → 习题集档(基础/巩固)，
KP 精确命中（knowledge_points 与 03-知识点/ 精确对应），默认排除已用题与承接题。

用法：
  python gen_weak_drill.py --kp 化学平衡 --module 化学原理                # dry-run
  python gen_weak_drill.py --kp 化学平衡 --module 化学原理 --write        # 自动命名落盘
  python gen_weak_drill.py --kp 晶胞 --kp 配位化合物 --size 15 --seed 7
  python gen_weak_drill.py --list-kps 晶体                               # 找 KP 名

行为：
  · type 白名单 {题目, 真题}；status 白名单 {已填充, 已补全答案}
  · knowledge_points 解析为健壮版：同名键重复出现时取最后一次（YAML 后值覆盖语义，
    兼容 104 条真题的重复键缺陷）；inline / 标量 / block 三种写法；去 [[ ]] 后精确比对
  · 降档链：每档内 difficulty 升序、seed 稳定 tie-break，取满剩余名额后降到下一档
  · 默认同来源不限流（KP 专项天然集中）；--src-limit N 启用 srcKey 归一限流
  · --write 落盘到 06-学生侧材料/练习卷/（试卷 frontmatter 对齐阶段测试卷样本，
    卷尾「参考答案」给每题 ≤120 字摘要 + 跳转），并自动跑 validate_kb --changed 闸门
  · 出卷后回填闭环：python .workbuddy/scripts/mark_used.py --paper "<补弱卷>.md"
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
Q_DIRS = ("04-题库", "05-真题库")
KP_DIR = VAULT / "03-知识点"
OUT_DIR = VAULT / "06-学生侧材料" / "练习卷"
VALIDATE = VAULT / "11-模板" / "scripts" / "validate_kb.py"
PY = r"C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe"

OK_STATUS = {"已填充", "已补全答案"}
Q_TYPES = {"题目", "真题"}
# 降档链：教学档 → 档名（与三模块视图对应）
TIERS = [("竞赛", "测试题档"), ("拓展", "习题书档"), ("巩固", "习题集档"), ("基础", "习题集档")]

WIKI = re.compile(r"\[\[([^\]\|#]+)")
NUM = re.compile(r"\d+")
ANS_H = re.compile(r"(?m)^#{1,6}\s*(?:参考答案|答案与解析|答案)\s*$")
HEAD = re.compile(r"(?m)^#{1,6}\s")


# ────────────────────────── 基础工具 ──────────────────────────

def read_raw(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def strip_wiki(v: str) -> str:
    """'[[化学平衡]]' → '化学平衡'；锚点/别名一并去掉。"""
    v = v.strip().strip('"').strip("'").strip()
    m = WIKI.match(v)
    if m:
        return m.group(1).strip()
    return v.split("#")[0].split("|")[0].strip()


def fm_lines(text: str) -> list[str] | None:
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return None


def fm_scalar(fl: list[str], field: str) -> str:
    """取字段标量值；同名键重复时取最后一次（YAML 后值覆盖语义）。"""
    pat = re.compile(rf"^{re.escape(field)}\s*:\s*(.*)$")
    val = ""
    for ln in fl:
        m = pat.match(ln)
        if m:
            val = m.group(1).strip()
    return val.strip('"').strip("'")


def fm_list(fl: list[str], field: str) -> list[str]:
    """取字段列表：inline [a, b] / 标量 / block(- item) 三种写法，重复键取最后一次。"""
    pat = re.compile(rf"^{re.escape(field)}\s*:\s*(.*)$")
    last_idx = None
    for i, ln in enumerate(fl):
        if pat.match(ln):
            last_idx = i
    if last_idx is None:
        return []
    v = pat.match(fl[last_idx]).group(1).strip()
    if v.startswith("["):
        inner = v[1:].rstrip().rstrip("]")
        return [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
    if v:
        return [v.strip('"').strip("'")]
    out = []
    for ln in fl[last_idx + 1:]:
        m = re.match(r"^\s+-\s*(.+?)\s*$", ln)
        if m:
            out.append(m.group(1).strip('"').strip("'"))
        elif ln.strip() and not ln.startswith((" ", "\t", "-")):
            break  # 下一字段开始
    return out


def diff_num(d: str) -> int | None:
    """difficulty 取首个整数（区间 '3-5' 取下界），与工作台 diffNum 口径一致。"""
    m = NUM.search(str(d or ""))
    return int(m.group(0)) if m else None


def used_tags(fl: list[str]) -> list[str]:
    """used_in 已用卷名（wikilink 归一）；空列表 = 未用过。"""
    raw = fm_scalar(fl, "used_in")
    if not raw:
        return []
    if raw.startswith("["):
        inner = raw[1:].rstrip().rstrip("]")
        return [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
    return [strip_wiki(raw)] if strip_wiki(raw) else []


# 与 check_workbench_js.py / 组卷工作台 srcKey() 完全一致（--src-limit 用）
SRC_RULES = [
    (re.compile(r"[（(]忠实转录[)）]"), ""),
    (re.compile(r"[·•]\s*第\s*\d+\s*[讲章][\s\S]*$"), ""),
    (re.compile(r"第\s*[\d一二三四五六七八九十]+\s*[章节讲篇][\s\S]*$"), ""),
    (re.compile(r"[·•]\s*第\s*[\d一二三四五六七八九十]+\s*[分册卷][\s\S]*$"), ""),
    (re.compile(r"-\s*\d{1,2}\s*$"), ""),
    (re.compile(r"[\s·•、,，\-—]+$"), ""),
]


def src_key(s: str) -> str:
    k = str(s or "").strip()
    for pat, rep in SRC_RULES:
        k = pat.sub(rep, k)
    return k.strip() or "(未知来源)"


def kp_files(name: str) -> list[Path]:
    """KP 精确命中前提：03-知识点/ 下（含模块子目录）存在同名 .md。"""
    return [p for p in KP_DIR.rglob(f"{name}.md") if p.name == f"{name}.md"]


# ────────────────────────── 题目扫描 ──────────────────────────

def scan_pool() -> list[dict]:
    """扫全库题目 → [{path, rel, name, tier, diff, src, module, qt, used, dep}]。"""
    pool = []
    for d in Q_DIRS:
        for p in (VAULT / d).rglob("*.md"):
            try:
                fl = fm_lines(read_raw(p))
            except OSError:
                continue
            if fl is None or fm_scalar(fl, "type") not in Q_TYPES:
                continue
            st = fm_scalar(fl, "status")
            if st not in OK_STATUS:
                continue
            lvl = fm_scalar(fl, "teaching_level")
            tier = next((name for l, name in TIERS if l == lvl), None)
            if tier is None:
                continue
            d_ = diff_num(fm_scalar(fl, "difficulty"))
            if d_ is None:
                continue
            pool.append({
                "path": p,
                "rel": p.relative_to(VAULT).as_posix(),
                "name": p.stem,
                "tier": tier,
                "level": lvl,
                "diff": d_,
                "src": fm_scalar(fl, "source"),
                "module": fm_scalar(fl, "subject_module"),
                "qt": [x for x in fm_list(fl, "question_type") if x],
                "kps": [strip_wiki(x) for x in fm_list(fl, "knowledge_points") if strip_wiki(x)],
                "used": used_tags(fl),
                "dep": bool(fm_scalar(fl, "depends_on")),
            })
    # basename 全库唯一性（试卷 wikilink 写短名的前提）
    seen: dict[str, int] = {}
    for q in pool:
        seen[q["name"]] = seen.get(q["name"], 0) + 1
    for q in pool:
        q["uniq"] = seen[q["name"]] == 1
    return pool


def ans_summary(path: Path, limit: int = 120) -> str:
    """抽题目文件参考答案节文本（≤limit 字符）；纯图答案原样保留不编造。"""
    try:
        text = read_raw(path)
    except OSError:
        return ""
    fl = fm_lines(text)
    body = text if fl is None else text.split("\n", len(fl) + 2)[-1]
    m = ANS_H.search(body)
    if not m:
        return ""
    nxt = HEAD.search(body, m.end())
    seg = body[m.end(): nxt.start() if nxt else len(body)]
    seg = "\n".join(ln for ln in seg.split("\n") if not re.match(r"^\s*-{3,}\s*$", ln))
    seg = re.sub(r"\s+", " ", seg).strip()
    if len(seg) > limit:
        seg = seg[:limit].rstrip() + "……"
    return seg


# ────────────────────────── 选题 ──────────────────────────

def tiebreak(seed: int, rel: str) -> str:
    return hashlib.md5(f"{seed}:{rel}".encode("utf-8")).hexdigest()


def pick_chain(cands: list[dict], size: int, seed: int, src_limit: int,
               kps: set[str]) -> tuple[list[dict], dict]:
    """降档链式抽题。返回 (入选, 每档统计)。档内难度升序 + seed 稳定 tie-break；
    多 KP 时每档优先抽尚未入卷的 KP（贪心覆盖），保证每个失分 KP 都练到。"""
    order = {name: i for i, (_, name) in enumerate(TIERS)}
    stats = {}
    chosen: list[dict] = []
    used_src: dict[str, int] = {}
    remaining = set(kps)
    for tier in dict.fromkeys(name for _, name in TIERS):
        bucket = [q for q in cands if q["tier"] == tier]
        want = size - len(chosen)
        bucket.sort(key=lambda q: (q["diff"], tiebreak(seed, q["rel"])))
        got: list[dict] = []
        got_ids: set[str] = set()

        def take(only_new_kp: bool) -> None:
            for q in bucket:
                if len(got) >= want:
                    return
                if q["rel"] in got_ids:
                    continue
                k = src_key(q["src"])
                if src_limit > 0 and used_src.get(k, 0) >= src_limit:
                    continue
                if only_new_kp and remaining and not (set(q["kps"]) & kps & remaining):
                    continue
                got.append(q)
                got_ids.add(q["rel"])
                used_src[k] = used_src.get(k, 0) + 1

        take(True)   # 先覆盖还没入卷的 KP
        take(False)  # 再补满名额
        for q in got:
            remaining -= set(q["kps"]) & kps
        stats[tier] = {"cand": len(bucket), "got": len(got), "quota": want}
        chosen.extend(got)
        if len(chosen) >= size:
            break
    chosen.sort(key=lambda q: (q["diff"], tiebreak(seed, q["rel"])))
    return chosen, stats


# ────────────────────────── 报告与出卷 ──────────────────────────

def wiki_of(q: dict) -> str:
    return f"[[{q['name']}]]" if q["uniq"] else f"[[{q['rel'][:-3]}]]"


def report(args, kps: list[str], pool: list[dict], cands: list[dict],
           chosen: list[dict], stats: dict) -> None:
    print(f"\n═══ 补弱卷 dry-run（{'--write ' + args.write if args.write else '未落盘'}）═══")
    print(f"目标：{args.size} 题 ｜ KP：{' / '.join(kps)}"
          f" ｜ 模块：{' / '.join(args.module) or '不限'} ｜ 种子：{args.seed}")
    print(f"池子全量 {len(pool)} ｜ KP 精确命中候选 {len(cands)}")
    print("─" * 62)
    print("降档链：")
    for name in dict.fromkeys(n for _, n in TIERS):
        s = stats.get(name, {"cand": 0, "got": 0, "quota": 0})
        flag = " ⚠️ 候选不足" if s["got"] < s["quota"] else ""
        print(f"  {name}：候选 {s['cand']:4d} ｜ 名额 {s['quota']:3d} ｜ 实得 {s['got']:3d}{flag}")
    print("─" * 62)
    for i, q in enumerate(chosen, 1):
        qt = "/".join(q["qt"]) or "—"
        print(f"  {i:2d}. {wiki_of(q)}  d{q['diff']}  {q['level']}  {qt}  "
              f"{q['module'] or '—'}  {q['src'][:26]}")
    # KP 覆盖
    print("─" * 62)
    for kp in kps:
        hit = [q for q in cands if kp in q["kps"]]
        got = [q for q in chosen if kp in q["kps"]]
        print(f"  KP「{kp}」：命中 {len(hit)} ｜ 入卷 {len(got)}")
    # 来源分布（归一后）：补弱卷默认不限流，集中是特性，但要让用户看得见
    from collections import Counter
    srcs = Counter(src_key(q["src"]) for q in chosen)
    top = " ｜ ".join(f"{k[:22]}×{v}" for k, v in srcs.most_common(3))
    print(f"  来源分布（前 3）：{top}"
          + ("" if args.src_limit > 0 else "（默认不限流，可用 --src-limit 3 收紧）"))
    excl_used = sum(1 for q in pool if q["used"])
    print(f"  （全库已用题 {excl_used} 条，均已排除"
          f"{'' if not args.include_used else ' —— 本次 --include-used 未排除'}）")


def build_paper(args, kps: list[str], chosen: list[dict], stats: dict) -> tuple[str, str]:
    today = args.date
    kp_slug = "-".join(re.sub(r"[\\/:*?\"<>|\s]+", "", k) for k in kps)[:40]
    title = f"补弱卷-{kp_slug}-{today}"
    diffs = [q["diff"] for q in chosen]
    tier_n = {}
    for q in chosen:
        tier_n[q["tier"]] = tier_n.get(q["tier"], 0) + 1
    tier_line = " / ".join(f"{n}×{c}" for n, c in tier_n.items())
    mod_line = " / ".join(args.module) if args.module else "不限"
    lines = [
        "---",
        f'title: "{title}"',
        "type: 系统",
        "role: 试卷",
        f"updated: {today}",
        "tags: [系统, 试卷, 补弱卷]",
        f"question_count: {len(chosen)}",
        f"difficulty_range: {min(diffs)}-{max(diffs)}" if diffs else "difficulty_range: -",
        "---",
        "",
        f"# {title}",
        "",
        f"> **题量**: {len(chosen)} 题 ｜ **建议时长**: 90 分钟 ｜ **总分**: 100 分",
        f"> **降档链**: 测试题(竞赛) → 习题书(拓展) → 习题集(基础/巩固) ｜ 实得: {tier_line}",
        f"> **失分复盘**: 失分模块={mod_line} ｜ 失分 KP={' / '.join(kps)}",
        f"> **选题种子**: {args.seed}（同参数可复现） ｜ 生成: gen_weak_drill.py ｜ 已排除已用题与承接题",
        "",
        "## 试题",
        "",
    ]
    for i, q in enumerate(chosen, 1):
        qt = "/".join(q["qt"])
        meta = f"难度 {q['diff']} ｜ {q['tier']}"
        if qt:
            meta += f" ｜ {qt}"
        lines.append(f"{i}. {wiki_of(q)}　（{meta}）")
    lines += ["", "## 参考答案", "",
              "> 完整答案与解析见各题目笔记（点击题号跳转）。", ""]
    for i, q in enumerate(chosen, 1):
        seg = ans_summary(q["path"])
        lines.append(f"{i}. {wiki_of(q)}" + (f" —— {seg}" if seg else " ——（见原文件）"))
    lines.append("")
    return title, "\n".join(lines)


# ────────────────────────── main ──────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="补弱卷生成器（降档链式）")
    ap.add_argument("--kp", action="append", default=[], help="失分 KP（可多次）")
    ap.add_argument("--module", action="append", default=[], help="失分模块 subject_module（可多次）")
    ap.add_argument("--size", type=int, default=15, help="目标题数（默认 15，grill 定稿）")
    ap.add_argument("--seed", type=int, default=42, help="随机种子（默认 42）")
    ap.add_argument("--src-limit", type=int, default=0, help="同来源限流 N（0=不限，默认）")
    ap.add_argument("--include-used", action="store_true", help="不排除已用题（默认排除）")
    ap.add_argument("--list-kps", metavar="子串", help="列出含子串的 KP 及频次后退出")
    ap.add_argument("--write", nargs="?", const="auto", default=None,
                    help="落盘（无值=自动命名到 06-学生侧材料/练习卷/）")
    ap.add_argument("--date", default=None, help=argparse.SUPPRESS)
    args = ap.parse_args()
    if not args.date:
        import datetime
        args.date = datetime.date.today().isoformat()

    # ── --list-kps 辅助模式 ──
    if args.list_kps:
        from collections import Counter
        cnt: Counter = Counter()
        for q in scan_pool():
            for k in q["kps"]:
                if args.list_kps in k:
                    cnt[k] += 1
        print(f"含「{args.list_kps}」的 KP（按频次）：")
        for k, v in cnt.most_common(30):
            exists = "✓" if kp_files(k) else "✗ 无KP文件"
            print(f"  {v:5d}  {k}  {exists}")
        return

    if not args.kp:
        ap.error("需要 --kp（或用 --list-kps 查找 KP 名）")

    # ── KP 校验：精确命中要求 KP 能解析到 03-知识点/ ──
    kps = [strip_wiki(k) for k in args.kp]
    bad = [k for k in kps if not kp_files(k)]
    if bad:
        print(f"❌ 以下 KP 在 03-知识点/（含模块子目录）下没有同名文件：{' / '.join(bad)}")
        near = set()
        for q in scan_pool():
            for k in q["kps"]:
                if any(b in k or k in b for b in bad):
                    near.add(k)
        if near:
            print("   近似候选（题库实际在用的 KP 名）：")
            for k in sorted(near)[:15]:
                print(f"     - {k}")
        sys.exit(1)
    kp_set = set(kps)

    pool = scan_pool()
    cands = []
    for q in pool:
        if not (kp_set & set(q["kps"])):
            continue
        if args.module and q["module"] not in args.module:
            continue
        if q["used"] and not args.include_used:
            continue
        if q["dep"]:
            continue  # 承接题必须连前驱出卷，补弱卷直接排除（全库仅 4 条）
        cands.append(q)

    chosen, stats = pick_chain(cands, args.size, args.seed, args.src_limit, kp_set)
    report(args, kps, pool, cands, chosen, stats)

    if not chosen:
        print("\n没有可选题，退出。")
        sys.exit(1)
    if len(chosen) < args.size:
        print(f"\n⚠️ 只凑到 {len(chosen)}/{args.size} 题（候选池不足）。"
              f"可加 --include-used 或放宽 --module 再试。")

    # ── 落盘 ──
    if args.write is None:
        print("\n这是 DRY-RUN。确认后加 --write 落盘，再跑 mark_used.py 回填 used_in。")
        return
    if args.write == "auto":
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        kp_slug = "-".join(re.sub(r"[\\/:*?\"<>|\s]+", "", k) for k in kps)[:40]
        out = OUT_DIR / f"补弱卷-{kp_slug}-{args.date}.md"
    else:
        out = VAULT / args.write.replace("\\", "/")
    title, md = build_paper(args, kps, chosen, stats)
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write(md)
    rel = out.relative_to(VAULT).as_posix()
    print(f"\n✅ 已生成 {rel}（{len(chosen)} 题）")

    # ── 入库闸门：validate_kb --changed 硬性通过（SOP §5.2）──
    r = subprocess.run([PY, "-X", "utf8", str(VALIDATE), "--changed", rel],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=str(VAULT))
    tail = "\n".join((r.stdout or "").strip().splitlines()[-6:])
    print(f"── validate_kb --changed（退出码 {r.returncode}）──\n{tail}")
    if r.returncode != 0:
        print("❌ 闸门未过：请检查上面的报错，或删除该文件后反馈。")
        sys.exit(2)
    print("\n出卷闭环下一步（回填 used_in，先 dry-run 确认）：")
    print(f'  python .workbuddy/scripts/mark_used.py --paper "{rel}"')
    print(f'  python .workbuddy/scripts/mark_used.py --paper "{rel}" --write   # 确认无误后')


if __name__ == "__main__":
    main()
