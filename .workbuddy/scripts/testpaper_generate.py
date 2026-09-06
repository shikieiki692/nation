# -*- coding: utf-8 -*-
"""三篇阶段测试卷生成：结构化学/有机化学/元素与分析（模式复刻 化学原理阶段测试卷）"""
import io, os, re, yaml, random, collections

ROOT = r"C:\Obsidion\妙妙屋\04-题库"
OUT_ROOT = r"C:\Obsidion\妙妙屋\04-题库"

def fm_of(path):
    try:
        text = io.open(path, encoding="utf-8").read()
    except Exception:
        return None
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception:
        return None
    return fm if isinstance(fm, dict) else None

def scan(subject):
    pool = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {"_归档", "_archive_v2",
                       "浙江卷2021", "浙江卷2022", "浙江卷2023"}]
        for f in filenames:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dirpath, f)
            fm = fm_of(p)
            if not fm:
                continue
            if fm.get("pack") != "模块习题集" or fm.get("subject_module") != subject:
                continue
            status = str(fm.get("status", "")).strip()
            if "deprecated" in status or status == "暂缓":
                continue
            if fm.get("used_in"):
                continue
            try:
                d = int(fm.get("difficulty"))
            except Exception:
                continue
            if not (1 <= d <= 5):
                continue
            pool.append({
                "file": os.path.splitext(f)[0],
                "submodule": str(fm.get("submodule", "")).strip() or "综合",
                "difficulty": d,
                "status_ok": status.startswith("已"),
            })
    return pool

# 子模块归并（同义折叠）
MERGE = {
    "配位化合物": "配位化学", "配位化合物基础": "配位化学",
    "分子结构与化学键": "分子结构与化学键", "共价键理论": "分子结构与化学键",
    "离子键与离子晶体": "离子晶体与离子键", "其他类型晶体": "晶体结构",
    "金属键与金属晶体": "晶体结构", "晶体结构基础": "晶体结构",
    "结构化学基础": "结构化学基础", "中级无机化学": "中级无机化学",
    "非对映选择性": "立体化学", "立体选择性": "立体化学",
    "环加成反应": "周环反应", "元素推断": "推断技术",
}

def normalize(sub):
    return MERGE.get(sub, sub)

QUOTA = {  # 每卷难度梯度
    "结构化学":   {"d3": 8,  "d4": 34, "d5": 8},
    "有机化学":   {"d3": 8,  "d4": 34, "d5": 8},
    "元素与分析": {"d3": 10, "d4": 36, "d5": 4},
}

def select(subject, seed=42):
    pool = scan(subject)
    rng = random.Random(seed)
    groups = collections.defaultdict(list)
    for p in pool:
        p["group"] = normalize(p["submodule"])
        groups[p["group"]].append(p)
    # 分组配额：sqrt 比例，min 3（组员≥4 才独立成组，否则并入 综合），cap 16
    big = {g: v for g, v in groups.items() if len(v) >= 4}
    small = {g: v for g, v in groups.items() if len(v) < 4}
    TOTAL = 50
    quota = {}
    w = {g: len(v) ** 0.5 for g, v in big.items()}
    tw = sum(w.values())
    raw = {g: 50 * w[g] / tw for g in big}
    for g in big:
        quota[g] = max(3, min(16, int(raw[g])))  # floor（带下限/上限）
    # 最大余数法把总和精确调到 TOTAL
    diff = TOTAL - sum(quota.values())
    order = sorted(big, key=lambda g: raw[g] - int(raw[g]), reverse=True)
    i = 0
    while diff != 0:
        g = order[i % len(order)]
        if diff > 0 and quota[g] < 16:
            quota[g] += 1; diff -= 1
        elif diff < 0 and quota[g] > 3:
            quota[g] -= 1; diff += 1
        i += 1
    # 修正到 50
    flat = [p for g, v in big.items() for p in v] + [p for v in small.values() for p in v]
    # 调平：先按配额取，不足从大组补
    chosen = []
    used_files = set()
    grad = QUOTA[subject]
    def pick_from(items, want_d, n, r):
        cand = [p for p in items if p["file"] not in used_files]
        exact = [p for p in cand if p["difficulty"] == want_d and p["status_ok"]]
        rng.shuffle(exact)
        take = exact[:n]
        if len(take) < n:  # 从相邻难度补
            rest = [p for p in cand if p not in take and p["status_ok"]]
            rest.sort(key=lambda p: abs(p["difficulty"] - want_d))
            take += rest[:n - len(take)]
        if len(take) < n:  # status 不 ideal 的兜底
            rest = [p for p in cand if p not in take]
            rest.sort(key=lambda p: abs(p["difficulty"] - want_d))
            take += rest[:n - len(take)]
        for p in take:
            used_files.add(p["file"])
        return take
    results = collections.OrderedDict()
    # 各组先按梯度取配额
    for g, q in sorted(quota.items(), key=lambda kv: -len(big.get(kv[0], small.get(kv[0], [])))):
        items = groups.get(g, [])
        per = grad
        take = []
        # 组内按梯度分配
        for dk, dn in per.items():
            want = dk[1]
            take += pick_from(items, int(want), max(1, round(q * dn / 50)), rng)
        take = take[:q]
        results[g] = take
        chosen += take
    # 不足 50 则从全池补
    if len(chosen) < 50:
        rest = [p for p in flat if p["file"] not in used_files and p["status_ok"]]
        rest.sort(key=lambda p: (p["difficulty"], rng.random()))
        for p in rest[:50 - len(chosen)]:
            used_files.add(p["file"])
            g = p["group"]
            results.setdefault(g, []).append(p)
            chosen.append(p)
    return results, chosen

def write_paper(subject, results, chosen):
    dif = collections.Counter(p["difficulty"] for p in chosen)
    fn = os.path.join(OUT_ROOT, f"{subject}阶段测试卷.md")
    title = f"{subject}阶段测试卷"
    grad = QUOTA[subject]
    lines = [
        "---",
        f'title: "{title}"',
        "type: 系统",
        "role: 试卷",
        "updated: 2026-09-02",
        f"tags: [系统, 题库, 试卷, {subject}, 阶段测试]",
        f"question_count: {len(chosen)}",
        "difficulty_range: 3-5",
        "---",
        "",
        f"# {title}",
        "",
        f"> **题量**: {len(chosen)} 题 ｜ **建议时长**: 150 分钟 ｜ **总分**: 100 分",
        f"> **难度梯度**: d3 热身({grad['d3']}题) → d4 主体({grad['d4']}题) → d5 拔高({grad['d5']}题)（实际分布 d3×{dif.get(3,0)} / d4×{dif.get(4,0)} / d5×{dif.get(5,0)}）",
        f"> **覆盖子模块**: {' / '.join(f'{g}({len(v)})' for g, v in results.items() if v)}",
        "> **生成日期**: 2026-09-02 ｜ **选题来源**: 模块习题集题池（used_in 排除已用题，答案状态优先）",
        "",
        "---",
        "",
    ]
    for g, items in results.items():
        if not items:
            continue
        lines.append(f"## {g}（{len(items)} 题）")
        lines.append("")
        for p in items:
            lines.append(f"### [[{p['file']}]]")
            lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*组卷：2026-09-02 阶段测试卷专项（结构/有机/元素与分析三篇同期生成）；所选题目已回填 used_in。*")
    eol = "\n"
    io.open(fn, "w", encoding="utf-8", newline="").write(eol.join(lines) + eol)
    return fn, len(chosen)

def build_index():
    idx = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {"_归档", "_archive_v2",
                       "浙江卷2021", "浙江卷2022", "浙江卷2023"}]
        for f in filenames:
            if f.endswith(".md"):
                idx.setdefault(f[:-3], os.path.join(dirpath, f))
    return idx

def backfill_used_in(subject, chosen, index):
    n = 0
    for p in chosen:
        target = index.get(p["file"])
        if not target:
            print("  !! 未找到文件:", p["file"]); continue
        s = io.open(target, encoding="utf-8", newline="").read()
        if "used_in:" in s:
            continue
        eol = "\r\n" if "\r\n" in s else "\n"
        lines = s.split(eol)
        # 插在 status 行后
        for i, ln in enumerate(lines):
            if ln.startswith("status:"):
                lines.insert(i + 1, f'used_in: "[[{subject}阶段测试卷]]"')
                break
        else:
            continue
        io.open(target, "w", encoding="utf-8", newline="").write(eol.join(lines))
        n += 1
    return n

if __name__ == "__main__":
    total = 0
    index = build_index()
    print('索引文件数:', len(index))
    for subject in ["结构化学", "有机化学", "元素与分析"]:
        results, chosen = select(subject)
        fn, n = write_paper(subject, results, chosen)
        nb = backfill_used_in(subject, chosen, index)
        total += n
        print(f"{subject}: 卷 {fn} ({n} 题), used_in 回填 {nb}")
    print("used_in 回填总数:", total)
