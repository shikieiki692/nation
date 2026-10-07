# -*- coding: utf-8 -*-
# 2026-10-07 由 .workbuddy/scripts/special_papers.py 迁入 11-模板/scripts/
# 原因：.workbuddy/ 被 gitignore，清理工作区即丢失该管线。
# 原文件保留在 .workbuddy/scripts/（可能有其他会话引用）。
# 职责：一分册/二分册专项卷组卷（单源 25 题，按章分布）
"""一分册/二分册专项卷组卷：单源 25 题，按章分布"""
import io, sys, os, re, collections, json, random
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
random.seed(20260913)

VAULT = str(Path(__file__).resolve().parents[2])
ROOT = os.path.join(VAULT, "04-题库")

def fm_of(text):
    if not text.startswith("---"):
        return None
    ls = text.split("\n")
    for i in range(1, len(ls)):
        if ls[i].strip() == "---":
            return "\n".join(ls[1:i])
    return None

def fget(fm, key):
    m = re.search(rf"^{key}:\s*[\"\']?(.+?)[\"\']?\s*$", fm, re.M)
    return m.group(1).strip() if m else ""

def scan(dirkey, label):
    cands = []
    base = os.path.join(ROOT, "教材习题", dirkey)
    for dp, _, ns in os.walk(base):
        for n in ns:
            if not n.endswith(".md"):
                continue
            p = os.path.join(dp, n)
            rel = os.path.relpath(p, VAULT).replace("\\", "/")
            fm = fm_of(open(p, encoding="utf-8", newline="").read())
            if fm is None or not re.search(r"^type:\s*题目", fm, re.M):
                continue
            if re.search(r"^status:\s*deprecated", fm, re.M) or re.search(r"^used_in:", fm, re.M):
                continue
            try:
                d = int(str(fget(fm, "difficulty")).split("-")[0].split()[0])
            except Exception:
                continue
            if not (2 <= d <= 5) or fget(fm, "status") not in ("已填充", "已补全答案"):
                continue
            m = re.search(r"Ch(\d+)", n)
            chap = f"Ch{m.group(1)}" if m else "?"
            cands.append(dict(file=rel, d=d, mod=fget(fm, "subject_module"), chap=chap))
    dd = collections.Counter(c["d"] for c in cands)
    chaps = collections.Counter(c["chap"] for c in cands)
    mods = collections.Counter(c["mod"] for c in cands)
    print(f"{label}: 池 {len(cands)} | d={dict(sorted(dd.items()))} | 章={dict(sorted(chaps.items()))} | 模块={dict(mods.most_common())}")
    return cands

def pick_balanced(cands, n=25, d_weights=None):
    """按章分布 + 难度梯度抽 n 题；d_weights 覆盖默认"""
    by_chap = collections.defaultdict(list)
    for c in cands:
        by_chap[c["chap"]].append(c)
    chaps = [ch for ch in sorted(by_chap) if ch != "?"]
    per = max(1, n // max(1, len(chaps)))
    picked, cap = [], collections.Counter()
    for ch in chaps:
        pool = sorted(by_chap[ch], key=lambda x: (x["d"], x["file"]))
        random.shuffle(pool)
        take = 0
        for c in pool:
            if take >= per:
                break
            w = (d_weights or {}).get(c["d"], 1)
            if w and cap[c["d"]] < (d_weights or {}).get("cap", 99):
                picked.append(c); cap[c["d"]] += 1; take += 1
    # 补足到 n
    rest = [c for c in cands if c not in picked]
    random.shuffle(rest)
    while len(picked) < n and rest:
        c = rest.pop()
        if c not in picked:
            picked.append(c)
    return picked[:n]

def build_paper(picked, title, cn, focus_note, seed, script):
    MOD_ORDER = ["化学原理", "结构化学", "有机化学", "元素与分析"]
    SCORE = {2: 2, 3: 3, 4: 4, 5: 5}
    lines = ["---", f'title: "{title}"', "type: 系统", "role: 试卷",
             "updated: 2026-09-06", "tags: [系统, 题库, 试卷, 专项]",
             f"question_count: {len(picked)}", "difficulty_range: 2-5",
             "exam_coverage: 单源专项（竞赛教材配套自测）", "---", "",
             f"# {cn}", "",
             f"> **题量**: {len(picked)} 题 ｜ **建议时长**: 150 分钟 ｜ **总分**: {sum(SCORE[c['d']] for c in picked)} 分（d2/d3/d4/d5 = 2/3/4/5 分）",
             f"> **取题口径**: {focus_note}",
             f"> **生成**: 2026-09-06，`.workbuddy/tmp/{script}`（seed={seed}，按章分布）",
             "> **答案**: 每题 wikilink 直达题文件；作答后错题请登记至 [[05-错题与反思]] 并回链知识点", ""]
    total = 0
    for mod in MOD_ORDER:
        items = sorted([c for c in picked if c["mod"] == mod], key=lambda x: x["d"])
        if not items:
            continue
        lines += [f"## {mod}（{len(items)} 题）", ""]
        for c in items:
            name = os.path.splitext(os.path.basename(c["file"]))[0]
            total += SCORE[c["d"]]
            lines += [f"### [[{name}]]（d{c['d']}，{SCORE[c['d']]} 分）", ""]
    lines += ["---", "", f"**合计 {len(picked)} 题，参考总分 {total} 分**"
              "（按 d2/d3/d4/d5=2/3/4/5 计，仅供自评）", ""]
    out = os.path.join(VAULT, "04-题库", f"{title}.md")
    open(out, "w", encoding="utf-8", newline="").write("\n".join(lines))
    print("卷已生成:", out)
    return picked

def backfill(picked, paper):
    n = 0
    for c in picked:
        p = os.path.join(VAULT, c["file"])
        text = open(p, encoding="utf-8", newline="").read()
        if re.search(r"^used_in:", text[:text.index("\n---", 4)] if "\n---" in text else "", re.M):
            continue
        ls = text.split("\n")
        end = next(i for i in range(1, len(ls)) if ls[i].strip() == "---")
        ls.insert(end, f'used_in: "[[{paper}]]"')
        open(p, "w", encoding="utf-8", newline="").write("\n".join(ls))
        n += 1
    print(f"used_in 回填: {n}")

# ── 一分册专项卷 I ──
c1 = scan("高中化学竞赛教程第一分册", "一分册正册")
p1 = pick_balanced(c1, 25)
print(f"  选中 {len(p1)}: d={dict(sorted(collections.Counter(c['d'] for c in p1).items()))}, "
      f"章={dict(sorted(collections.Counter(c['chap'] for c in p1).items()))}")
json.dump(p1, open(".workbuddy/tmp/p1_picked.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ── 二分册专项卷 I（d5 主攻）──
c2 = scan("高中化学竞赛教程第二分册", "二分册")
p2 = pick_balanced(c2, 25, d_weights={2: 0, 3: 0, 4: 1, 5: 1})
print(f"  选中 {len(p2)}: d={dict(sorted(collections.Counter(c['d'] for c in p2).items()))}, "
      f"章={dict(sorted(collections.Counter(c['chap'] for c in p2).items()))}")
json.dump(p2, open(".workbuddy/tmp/p2_picked.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
