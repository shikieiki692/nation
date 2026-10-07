# -*- coding: utf-8 -*-
# 2026-10-07 由 .workbuddy/scripts/testpaper_v2.py 迁入 11-模板/scripts/
# 原因：.workbuddy/ 被 gitignore，清理工作区即丢失该管线。
# 本轮改动：接入 KP 维度（parse_fm 用 fm_parse 解析数组形态的 knowledge_points；
#   select 支持 --kp 贪心覆盖；卷头写入「目标考点」）。原文件保留在 .workbuddy/scripts/。
"""三篇阶段测试卷生成 v2：单次遍历 + 内存索引（结构化学/有机化学/元素与分析）"""
import io, os, re, sys, yaml, random, collections

VAULT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
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
    if not fm:
        return None
    # 2026-10-07：KP 用 fm_parse 解析——数组有六种书写形态，原正则只认标量会全漏
    try:
        import fm_parse as _fp
        fm["kps"] = _fp.get_wikilinks_field(m.group(1), "knowledge_points")
    except Exception:
        kp = re.search(r"(?ms)^knowledge_points[ \t]*:(.*?)(?=\n[ \t]*[A-Za-z_]+[ \t]*:|\Z)", m.group(1))
        seg = kp.group(1) if kp else ""
        fm["kps"] = re.findall(r"\[\[([^\]\|]+)\]\]", seg)
    return fm

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
            "kps": fm.get("kps") or [],          # 2026-10-07 新增
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

def select(subject, records, seed=42, target_kps=None):
    """target_kps：目标考点列表。每个目标 KP 先保底抽 1 题（贪心覆盖），
    剩余名额仍按原「子模块配额 × 难度梯度」逻辑补齐——不改变原选题行为。"""
    rng = random.Random(seed)
    pool = pick_pool(records, subject)
    target_kps = list(target_kps or [])
    kp_taken = {}
    if target_kps:
        # 每档（d3/d4/d5）内先按 KP 覆盖，再走原配额
        by_kp = collections.defaultdict(list)
        for p in pool:
            if not p["status_ok"] or p["file"] in getattr(select, "_used", set()):
                continue
            for k in p["kps"]:
                if k in target_kps:
                    by_kp[k].append(p)
        for k in target_kps:
            cands = [p for p in (by_kp.get(k) or [])
                     if p["file"] not in {x["file"] for x in kp_taken.values()}]
            if not cands:
                continue
            # 同 KP 内优先取低难度（保底可用），difficulty 升序 + 稳定 tie-break
            cands = sorted(cands, key=lambda p: (p["difficulty"], rng.random()))
            pick = cands[0]
            pick.setdefault("kp_cover", []).append(k)
            kp_taken[k] = pick
        # 把保底题从各组池里摘掉（避免重复抽）
        if kp_taken:
            taken_files = {p["file"] for p in kp_taken.values()}
            pool = [p for p in pool if p["file"] not in taken_files]
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
    # 2026-10-07：把 KP 保底题并入结果（放在最前，便于卷头展示「目标考点覆盖」）
    if target_kps:
        covered = list(kp_taken.values())
        for p in covered:
            results.setdefault(p["group"], []).insert(0, p)
        chosen = covered + [p for p in chosen if p["file"] not in
                            {x["file"] for x in covered}][:max(0, 50 - len(covered))]
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
    ap = None
    argv = sys.argv[1:]
    if "--kp" in argv:
        i = argv.index("--kp")
        ap = [x for x in argv[i + 1:] if not x.startswith("-")]
        argv = argv[:i]
    print("目标考点：%s" % ("、".join(ap) if ap else "（未指定，走原配额逻辑）"))
    for subject in ["结构化学", "有机化学", "元素与分析"]:
        results, chosen = select(subject, records, target_kps=ap)
        fn = write_paper(subject, results, chosen)
        nb = backfill(subject, chosen, index)
        dif = collections.Counter(p["difficulty"] for p in chosen)
        print(f"{subject}: {fn} ｜ {len(chosen)} 题 ｜ d分布 {dict(sorted(dif.items()))} ｜ used_in 回填 {nb}")
