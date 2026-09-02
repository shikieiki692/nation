# -*- coding: utf-8 -*-
"""三篇阶段测试卷生成 v2：单次遍历 + 内存索引（结构化学/有机化学/元素与分析）"""
import io, os, re, yaml, random, collections

VAULT = r"C:\Obsidion\妙妙屋"
ROOT = os.path.join(VAULT, "04-题库")
EXCLUDE_DIRS = {"_归档", "_archive_v2", "浙江卷2021", "浙江卷2022", "浙江卷2023"}
QUOTA = {
    "结构化学":   {"d3": 8,  "d4": 34, "d5": 8},
    "有机化学":   {"d3": 8,  "d4": 34, "d5": 8},
    "元素与分析": {"d3": 10, "d4": 36, "d5": 4},
}
MERGE = {
    "配位化合物": "配位化学", "配位化合物基础": "配位化学",
    "共价键理论": "分子结构与化学键",
    "离子键与离子晶体": "离子晶体与离子键", "其他类型晶体": "晶体结构",
    "金属键与金属晶体": "晶体结构", "晶体结构基础": "晶体结构",
    "非对映选择性": "立体化学", "立体选择性": "立体化学",
    "环加成反应": "周环反应", "元素推断": "推断技术",
}

def parse_fm(path):
    """正则直取标量字段（比 yaml 快一个量级），够用且零依赖"""
    try:
        text = io.open(path, encoding="utf-8").read()
    except Exception:
        return None
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None
    fm = {}
    for ln in m.group(1).splitlines():
        mm = re.match(r"^(pack|subject_module|status|submodule|used_in):\s*(.+?)\s*(?:#.*)?$", ln)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip("'\"")
        mm2 = re.match(r"^difficulty:\s*(\d+)", ln)
        if mm2:
            fm["difficulty"] = int(mm2.group(1))
    return fm if fm else None

def single_pass():
    """一次遍历：返回 (index{basename:path}, records[])"""
    index, records = {}, []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dirpath, f)
            index.setdefault(f[:-3], p)
            fm = parse_fm(p)
            if not fm:
                continue
            records.append((f[:-3], fm))
    return index, records

def normalize(sub):
    return MERGE.get(sub, sub)

def pick_pool(records, subject):
    pool = []
    for name, fm in records:
        if fm.get("pack") != "模块习题集" or fm.get("subject_module") != subject:
            continue
        status = str(fm.get("status", "")).strip()
        if "deprecated" in status or status == "暂缓" or fm.get("used_in"):
            continue
        try:
            d = int(fm.get("difficulty"))
        except Exception:
            continue
        if not (1 <= d <= 5):
            continue
        pool.append({
            "file": name,
            "group": normalize(str(fm.get("submodule", "")).strip() or "综合"),
            "difficulty": d,
            "status_ok": status.startswith("已"),
        })
    return pool

def allocate_quota(groups, total=50, lo=3, hi=16):
    """大组数受 K×lo ≤ total 约束，超额组折叠进 综合；返回 (quota, big)"""
    big = {g: v for g, v in groups.items() if len(v) >= 4}
    small = {g: v for g, v in groups.items() if len(v) < 4}
    K = max(1, total // lo - 1)
    ordered = sorted(big, key=lambda g: -len(big[g]))
    keep = ordered[:K]
    folded = [g for g in ordered if g not in keep]
    if folded:
        merged = list(groups.get("综合", []))
        for g in folded:
            merged += groups[g]
        groups["综合"] = merged
    if small:
        groups["综合"] = list(groups.get("综合", [])) + [p for v in small.values() for p in v]
    big = {g: groups[g] for g in keep if len(groups.get(g, [])) >= 4}
    if len(groups.get("综合", [])) >= 4:
        big["综合"] = groups["综合"]
    w = {g: len(v) ** 0.5 for g, v in big.items()}
    tw = sum(w.values())
    raw = {g: total * w[g] / tw for g in big}
    quota = {g: max(lo, min(hi, int(raw[g]))) for g in big}
    diff = total - sum(quota.values())
    order = sorted(big, key=lambda g: raw[g] - int(raw[g]), reverse=True)
    i = 0
    while diff != 0 and i < 500:
        g = order[i % len(order)]
        if diff > 0 and quota[g] < hi:
            quota[g] += 1; diff -= 1
        elif diff < 0 and quota[g] > lo:
            quota[g] -= 1; diff += 1
        i += 1
    return quota, big

def pick_from(items, want_d, n, rng, used):
    cand = [p for p in items if p["file"] not in used]
    exact = [p for p in cand if p["difficulty"] == want_d and p["status_ok"]]
    rng.shuffle(exact)
    take = exact[:n]
    if len(take) < n:
        rest = sorted([p for p in cand if p not in take and p["status_ok"]],
                      key=lambda p: (abs(p["difficulty"] - want_d), rng.random()))
        take += rest[:n - len(take)]
    if len(take) < n:
        rest = sorted([p for p in cand if p not in take],
                      key=lambda p: (abs(p["difficulty"] - want_d), rng.random()))
        take += rest[:n - len(take)]
    for p in take:
        used.add(p["file"])
    return take

def select(subject, records, seed=42):
    rng = random.Random(seed)
    pool = pick_pool(records, subject)
    groups = collections.defaultdict(list)
    for p in pool:
        groups[p["group"]].append(p)
    quota, big = allocate_quota(groups)
    used = set()
    results = collections.OrderedDict()
    for g in sorted(quota, key=lambda g: -len(big[g])):
        items = groups.get(g, [])
        take = []
        grad = QUOTA[subject]
        for dk, dn in grad.items():
            want = int(dk[1])
            take += pick_from(items, want, round(quota[g] * dn / 50), rng, used)
        results[g] = take[:quota[g]]
    chosen = [p for v in results.values() for p in v]
    # 补齐到 50（组配额被截断时）
    if len(chosen) < 50:
        rest = sorted([p for p in pool if p["file"] not in used and p["status_ok"]],
                      key=lambda p: (p["difficulty"], rng.random()))
        for p in rest[:50 - len(chosen)]:
            used.add(p["file"])
            results.setdefault(p["group"], []).append(p)
            chosen.append(p)
    return results, chosen[:50]

def write_paper(subject, results, chosen):
    dif = collections.Counter(p["difficulty"] for p in chosen)
    grad = QUOTA[subject]
    fn = os.path.join(ROOT, f"{subject}阶段测试卷.md")
    lines = [
        "---",
        f'title: "{subject}阶段测试卷"',
        "type: 系统",
        "role: 试卷",
        "updated: 2026-09-02",
        f"tags: [系统, 题库, 试卷, {subject}, 阶段测试]",
        f"question_count: {len(chosen)}",
        "difficulty_range: 3-5",
        "---", "",
        f"# {subject}阶段测试卷", "",
        f"> **题量**: {len(chosen)} 题 ｜ **建议时长**: 150 分钟 ｜ **总分**: 100 分",
        f"> **难度梯度**: 目标 d3 热身({grad['d3']}) → d4 主体({grad['d4']}) → d5 拔高({grad['d5']})｜实际 d3×{dif.get(3,0)} / d4×{dif.get(4,0)} / d5×{dif.get(5,0)}",
        f"> **覆盖子模块**: {' / '.join(f'{g}({len(v)})' for g, v in results.items() if v)}",
        "> **生成日期**: 2026-09-02 ｜ **选题来源**: 模块习题集题池（used_in 排除已用题，答案状态优先）", "", "---", "",
    ]
    for g, items in results.items():
        if not items:
            continue
        lines.append(f"## {g}（{len(items)} 题）")
        lines.append("")
        for p in items:
            lines.append(f"### [[{p['file']}]]")
            lines.append("")
    lines += ["---", "",
              "*组卷：2026-09-02 阶段测试卷专项（结构/有机/元素与分析三篇同期生成，随机种子 42）；所选题目已回填 used_in。*"]
    io.open(fn, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    return fn

def backfill(subject, chosen, index):
    n = 0
    tag = f'used_in: "[[{subject}阶段测试卷]]"'
    for p in chosen:
        path = index.get(p["file"])
        if not path:
            print("  !! 索引缺失:", p["file"]); continue
        s = io.open(path, encoding="utf-8", newline="").read()
        if "used_in:" in s:
            continue
        eol = "\r\n" if "\r\n" in s else "\n"
        lines = s.split(eol)
        end = next((i for i, l in enumerate(lines) if l.strip() == "---" and i > 0), None)
        if end is None:
            print("  !! 无 frontmatter 结束:", p["file"]); continue
        lines.insert(end, tag)
        io.open(path, "w", encoding="utf-8", newline="").write(eol.join(lines))
        n += 1
    return n

if __name__ == "__main__":
    print("单次遍历扫描 04-题库 …")
    index, records = single_pass()
    print("索引:", len(index), "| 解析:", len(records))
    for subject in ["结构化学", "有机化学", "元素与分析"]:
        results, chosen = select(subject, records)
        fn = write_paper(subject, results, chosen)
        nb = backfill(subject, chosen, index)
        dif = collections.Counter(p["difficulty"] for p in chosen)
        print(f"{subject}: {fn} ｜ {len(chosen)} 题 ｜ d分布 {dict(sorted(dif.items()))} ｜ used_in 回填 {nb}")
