"""
生成模块习题集 — 从 04-题库 按 subject_module + pack 筛选，按子模块分组输出
用法: python gen_module_set.py <模块名> <输出文件名>
示例: python gen_module_set.py 有机化学 模块习题集-有机化学.md
"""
import os, re, sys, io, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = "04-题库"
TODAY = "2026-08-25"

if len(sys.argv) < 3:
    print("用法: python gen_module_set.py <模块名> <输出文件名>")
    sys.exit(1)

MODULE = sys.argv[1]
OUTPUT = sys.argv[2] if not sys.argv[2].startswith("04-") else sys.argv[2]
OUTPUT_PATH = os.path.join(BASE, OUTPUT)

# 子模块归类规则
def classify(sub, kp_text, path):
    text = (sub + " " + kp_text + " " + path).lower()
    if MODULE == "有机化学":
        if any(k in text for k in ("机理", "人名", "推断", "波谱")): return "机理推断与波谱"
        if any(k in text for k in ("合成", "路线", "催化")): return "有机合成"
        if any(k in text for k in ("结构", "构型", "构象", "立体", "异构", "手性", "旋光")): return "结构与立体化学"
        if any(k in text for k in ("方程式", "产物", "完成")): return "反应方程式与产物"
        return "综合"
    elif MODULE == "结构化学":
        if any(k in text for k in ("原子", "量子", "核外", "波函数", "电离", "光谱")): return "原子结构"
        if any(k in text for k in ("分子", "化学键", "杂化", "分子轨道", "价键", "VSEPR", "键级")): return "分子结构与化学键"
        if any(k in text for k in ("晶体", "晶胞", "晶格", "点阵", "堆积", "布拉维")): return "晶体结构"
        if any(k in text for k in ("配合物", "配位", "晶体场", "分裂能", "配位数")): return "配位化学"
        return "综合"
    elif MODULE == "元素与分析":
        if any(k in text for k in ("滴定", "容量", "EDTA", "指示剂", "误差", "定量")): return "容量分析"
        if any(k in text for k in ("制备", "鉴别", "分离")): return "制备与鉴别"
        if any(k in text for k in ("推断", "元素", "周期")): return "元素推断"
        if any(k in text for k in ("方程式", "配平")): return "方程式书写"
        return "综合"
    else:
        if any(k in text for k in ("气体", "相变", "溶液", "渗透")): return "气体与溶液"
        if any(k in text for k in ("热力学", "焓", "熵", "Gibbs")): return "热力学"
        if any(k in text for k in ("速率", "动力学", "活化能")): return "化学动力学"
        if any(k in text for k in ("平衡常数", "勒夏特列", "转化率")): return "化学平衡"
        if any(k in text for k in ("氧化还原", "电极", "电化学", "Nernst")): return "氧化还原与电化学"
        return "综合"

# 收集
pool = []
for root, dirs, fs in os.walk(BASE):
    if "高考" in root: continue
    for fn in fs:
        if not fn.endswith(".md"): continue
        s = open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
        fm = re.match(r"^---\n(.*?)\n---\n", s, re.S)
        if not fm: continue
        y = fm.group(1)
        if not re.search(r"(?m)^type: 题目", y): continue
        if not re.search(rf"(?m)^pack: 模块习题集", y): continue
        if not re.search(rf"(?m)^subject_module: {MODULE}$", y): continue
        if "used_in" in y: continue
        diff = (re.search(r"(?m)^difficulty: (.*)", y) or [None, "3"])[1].strip()
        fid = (re.search(r"(?m)^fidelity: (.*)", y) or [None, ""])[1].strip()
        kp = (re.search(r"(?m)^knowledge_points: \[(.*?)\]", y) or [None, ""])[1]
        kps = [k.strip() for k in re.findall(r"\[\[([^\]|]+)", kp)][:3]
        sub = (re.search(r"(?m)^submodule: (.*)", y) or [None, ""])[1].strip().strip('"')
        src = (re.search(r"(?m)^source: (.*)", y) or [None, ""])[1].strip().strip('"')[:35]
        grp = classify(sub, " ".join(kps), fn)
        try: d = int(diff)
        except: d = 3
        pool.append((grp, d, fn[:-3], fid, src, kps))

pool.sort(key=lambda x: (x[0], -x[1], x[2]))

# 分组
groups = collections.OrderedDict()
for g, d, fn, fid, src, kps in pool:
    groups.setdefault(g, []).append((d, fn, fid, src, kps))

# 输出
lines = []
lines.append("---")
lines.append(f'title: "模块习题集-{MODULE}"')
lines.append("type: 系统")
lines.append("role: 模块习题集")
lines.append(f"updated: {TODAY}")
lines.append(f"tags: [系统, 题库, 模块习题集, {MODULE}]")
lines.append("---")
lines.append("")
lines.append(f"# 模块习题集 · {MODULE}")
lines.append("")
dc = collections.Counter(x[1] for x in pool)
lines.append(f"> **题量**: {len(pool)} 题")
lines.append(f"> **难度**: " + " / ".join(f"d{k}={v}" for k, v in sorted(dc.items())))
lines.append(f"> **用途**: {MODULE}模块阶段测试")
lines.append(f"> **选题方法**: 按子模块选 50-70 题，难度梯度 2:5:3；出卷后在源文件加 `used_in` 标记")
lines.append(f"> **重新生成**: `python 11-模板/scripts/gen_module_set.py {MODULE} {OUTPUT}`")
lines.append("")
lines.append("---")
lines.append("")

for grp in groups:
    items = groups[grp]
    items.sort(key=lambda x: (-x[0], x[2]))
    lines.append(f"## {grp}（{len(items)} 题）")
    lines.append("")
    for d, fn, fid, src, kps in items:
        if "逐字" in fid: tag = "🟢"
        elif "自编" in fid: tag = "🔵"
        else: tag = "🟡"
        kp_str = " ".join(f"[[{k}]]" for k in kps) if kps else ""
        lines.append(f"- {tag} **d{d}** [[{fn}]] | {kp_str}")
    lines.append("")

open(OUTPUT_PATH, "w", encoding="utf-8", newline="").write("\n".join(lines))
dc = collections.Counter(x[1] for x in pool)
print(f"已生成 {OUTPUT_PATH}: {len(pool)} 题, {len(groups)} 个子模块")
print(f"难度: {dict(sorted(dc.items()))}")
