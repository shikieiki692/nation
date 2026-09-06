# -*- coding: utf-8 -*-
"""习题书分类准确性审计（只读，不改源库、不重建成书）。

方法：在内存中重放 build_module_book 的 gather → gap过滤 → 大题合并 → classify 管线，
再回读每个源文件的完整 frontmatter（module / submodule / knowledge_points），
用"源文件字段证据"与"成书章归属"做交叉验证。

重点核查（用户 2026-09-01 需求）：
  A. 晶体类题误入「分子结构与化学键」章（硬焦点）；
  B. 反向：化学键类题误入「晶体结构」章；
  C. 通用：frontmatter module 可唯一映射到某章、但成书章不同的题（全四篇）。

输出：09-审计报告/<日期>-习题书分类审计.md + 控制台摘要。
运行：系统 Python 3.12（需 PyYAML），必须在 vault 根目录执行。
  C:\\Users\\蕾赛\\AppData\\Local\\Programs\\Python\\Python312\\python.exe 11-模板/scripts/audit_book_classification.py
"""
import io
import json
import re
import sys
import collections
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, "11-模板/scripts")
import build_module_book as B  # noqa: E402
import yaml  # noqa: E402

VAULT = Path(__file__).resolve().parents[2]
REPORT_DIR = VAULT / "09-审计报告"
OUT_REPORT = REPORT_DIR / f"{B.TODAY}-习题书分类审计.md"

MODULES = [
    ("化学原理", B.CHEM_MAP, None),
    ("有机化学", B.ORGANIC_MAP, B.ORGANIC_EXCLUDE),
    ("元素与分析", B.YSFX_MAP, None),
    ("结构化学", B.STRUCTURE_MAP, None),
]

# 晶体 / 化学键证据正则（用户裁决规则：晶体关键词命中即判晶体，即使化学键词同时出现）
# 注意“晶体(?!场)”：晶体场理论属配位化学，不算晶体证据
CRYSTAL_RE = re.compile(
    r"晶体(?!场)|晶胞|晶格|点阵|堆积|晶面|布拉维|钙钛矿|沸石|分子筛|金刚石|富勒烯|冰晶石|密堆积")
BOND_RE = re.compile(
    r"化学键|共价键|杂化|vsepr|lewis|分子轨道|价键理论|价键|离子键|等电子体|离域|键级|键长|键角|键能")

CHAPTER_LOOKUP = {}  # module -> {chapter_name: (num, name)}
for _m, _map, _exc in MODULES:
    CHAPTER_LOOKUP[_m] = {name: (num, name) for num, name, _ in _map}

# 泛化 module 字段值（学科级/来源级标签，非章级证据），不参与 C 类判定
GENERIC_FMOD = {
    "结构化学", "化学原理", "有机化学", "元素与分析", "无机和结构化学", "无机化学",
    "化学", "元素化学", "分析化学", "溶液化学", "容量分析", "沉淀溶解平衡",
    "离子反应", "化学基础知识", "化学键理论", "综合", "04-题库",
}
# 设计性例外：电化学平衡题按管线设计有意路由至氧化还原与电化学章（防误入热力学）
INTENTIONAL = {("化学原理", "氧化还原与电化学", "热力学"),
               ("化学原理", "氧化还原与电化学", "化学热力学")}


def load_full_fm(rel_path):
    """回读源文件完整 frontmatter（build 的 gather 只取了部分字段）。"""
    p = VAULT / "04-题库" / rel_path
    try:
        s = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}


def kp_names(fm):
    """knowledge_points（wikilink 或纯文本列表）→ 条目名列表。"""
    kp = fm.get("knowledge_points") or []
    if isinstance(kp, str):
        kp = [kp]
    out = []
    for k in kp:
        k = str(k)
        found = re.findall(r"\[\[([^\]|#]+)", k)
        if found:
            out.extend(x.strip() for x in found)
        elif k.strip():
            out.append(k.strip())
    return [x for x in out if x]


def fuzzy_module_to_chapter(module, fmod):
    """frontmatter module 字段 → (num, name)；唯一命中才返回。"""
    if not fmod:
        return None, None
    hits = set()
    for name, (num, _n) in CHAPTER_LOOKUP[module].items():
        if fmod == name or fmod in name or name in fmod:
            hits.add(name)
    if len(hits) == 1:
        return CHAPTER_LOOKUP[module][hits.pop()], None
    if len(hits) > 1:
        return None, "歧义:" + "/".join(sorted(hits))
    return None, None


def evidence_hits(text_l, chapter_map):
    """文本在哪些章的关键词表命中 → {章名: 命中词列表}。"""
    hits = {}
    for num, name, kws in chapter_map:
        got = [kw for kw in kws if kw.lower() in text_l]
        if got:
            hits[name] = got
    return hits


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    flags = []          # 全部疑点
    stats = collections.Counter()
    fmod_dist = collections.defaultdict(collections.Counter)

    for module, cmap, exclude in MODULES:
        pool = [q for q in B.gather_questions(module)
                if q.get("submodule") not in set(exclude or [])]
        pool = [q for q in pool if not B.is_gap_item(q)]
        if B.MERGE_DA:
            pool = B.merge_da_items(pool)

        for item in pool:
            res = B.classify_by_keywords(item, cmap, module)
            if res is None:
                continue  # 待分类题不入书，不在本次范围
            book_num, book_name = res
            fm = load_full_fm(item["path"])
            fmod = str(fm.get("module", "") or "").strip()
            fsub = item["submodule"] or ""
            kps = kp_names(fm)
            title = item.get("title", "") or ""
            fmod_dist[module][fmod or "(空)"] += 1

            sub_l = fsub.lower()
            title_l = title.lower()
            file_l = item["file"].lower()
            kp_l = " ".join(kps).lower()
            fmod_l = fmod.lower()

            # ---- 焦点 A：成书=分子结构与化学键，但晶体证据命中（只看强证据字段）----
            if module == "结构化学" and book_name == "分子结构与化学键":
                cr_hits = []
                if CRYSTAL_RE.search(sub_l):
                    cr_hits.append("submodule")
                if fmod and CRYSTAL_RE.search(fmod_l):
                    cr_hits.append("frontmatter.module")
                if CRYSTAL_RE.search(file_l) or CRYSTAL_RE.search(item["path"].lower()):
                    cr_hits.append("file/path")
                if cr_hits:
                    flags.append({
                        "kind": "A-晶体误入化学键", "module": module,
                        "book": f"{book_num}.{book_name}", "sug": "3.晶体结构",
                        "path": item["path"], "submodule": fsub, "fmod": fmod,
                        "kp": "; ".join(kps)[:80], "evidence": "+".join(cr_hits),
                        "strength": "高" if "submodule" in cr_hits or "frontmatter.module" in cr_hits else "中",
                    })
                    stats["A"] += 1

            # ---- 焦点 B：成书=晶体结构，但仅化学键证据、无晶体证据 ----
            if module == "结构化学" and book_name == "晶体结构":
                has_crystal = bool(CRYSTAL_RE.search(sub_l) or CRYSTAL_RE.search(kp_l)
                                   or CRYSTAL_RE.search(fmod_l) or CRYSTAL_RE.search(title_l))
                bond_hits = []
                if BOND_RE.search(sub_l):
                    bond_hits.append("submodule")
                if BOND_RE.search(kp_l):
                    bond_hits.append("knowledge_points")
                if not has_crystal and bond_hits:
                    flags.append({
                        "kind": "B-化学键误入晶体", "module": module,
                        "book": f"{book_num}.{book_name}", "sug": "2.分子结构与化学键",
                        "path": item["path"], "submodule": fsub, "fmod": fmod,
                        "kp": "; ".join(kps)[:80], "evidence": "+".join(bond_hits),
                        "strength": "低（建议人工复核）",
                    })
                    stats["B"] += 1

            # ---- 通用 C：frontmatter module 唯一映射到某章但成书章不同 ----
            # 需 kp 佐证：建议章的关键词须命中 knowledge_points（防泛化字段噪声）
            # 中级无机化学文件走专用的文件名判定分支，其 module 字段不参与 C 类判定
            if fsub == "中级无机化学" or fmod in GENERIC_FMOD:
                target, amb = None, None
            else:
                target, amb = fuzzy_module_to_chapter(module, fmod)
            if target and (target[1] != book_name):
                kp_ok = any(kw.lower() in kp_l
                            for _n, _nm, kws in cmap if _nm == target[1] for kw in kws)
                if not kp_ok:
                    stats["kp-veto"] += 1
                    continue
                if (module, book_name, target[1]) in INTENTIONAL:
                    stats["intentional"] += 1
                    continue
                # 路径覆盖表已知例外跳过
                if item["path"] in B.PATH_SUBJECT_MODULE_OVERRIDES:
                    continue
                flags.append({
                    "kind": "C-module字段与成书章不符", "module": module,
                    "book": f"{book_num}.{book_name}", "sug": f"{target[0]}.{target[1]}",
                    "path": item["path"], "submodule": fsub, "fmod": fmod,
                    "kp": "; ".join(kps)[:80], "evidence": f"frontmatter.module={fmod}",
                    "strength": "中",
                })
                stats["C"] += 1

    # ---- 控制台摘要 ----
    print("=" * 60)
    print(f"分类审计完成：疑点 {len(flags)} 条  "
          f"(A 晶体误入化学键: {stats['A']} | B 化学键误入晶体: {stats['B']} | "
          f"C module字段不符: {stats['C']})")
    byk = collections.Counter(f["kind"] for f in flags)
    for k, n in byk.most_common():
        print(f"  {k}: {n}")

    # ---- 报告 ----
    L = []
    L.append("---")
    L.append('title: "习题书分类审计报告"')
    L.append("type: 审计报告")
    L.append(f"updated: {B.TODAY}")
    L.append("question_count: " + str(len(flags)))
    L.append("---")
    L.append("")
    L.append(f"# 习题书分类审计报告（{B.TODAY}）")
    L.append("")
    L.append("> 方法：内存重放 gather→合并→classify 管线，回读源文件 frontmatter "
             "（module/submodule/knowledge_points）三方证据交叉验证成书章归属。")
    L.append(f"> 结论：疑点 **{len(flags)}** 条 —— A 晶体误入化学键 {stats['A']} 条、"
             f"B 化学键误入晶体 {stats['B']} 条、C module字段不符 {stats['C']} 条。")
    L.append("")

    for kind in ["A-晶体误入化学键", "B-化学键误入晶体", "C-module字段与成书章不符"]:
        rows = [f for f in flags if f["kind"] == kind]
        if not rows:
            continue
        # 按证据字段聚合统计迁移量
        mig = collections.Counter((r["book"], r["sug"]) for r in rows)
        L.append(f"## {kind}（{len(rows)} 条）")
        L.append("")
        L.append("**迁移汇总**（现章 → 建议章）：")
        L.append("")
        for (b, s), n in sorted(mig.items()):
            L.append(f"- {b} → {s}：{n} 题")
        L.append("")
        L.append("| 模块 | 成书章 | 建议 | 源文件 | submodule | module字段 | knowledge_points | 证据 | 置信 |")
        L.append("|:--|:--|:--|:--|:--|:--|:--|:--|:--|")
        for r in rows:
            L.append(f"| {r['module']} | {r['book']} | {r['sug']} | {r['path']} "
                     f"| {r['submodule'] or '—'} | {r['fmod'] or '—'} "
                     f"| {r['kp'] or '—'} | {r['evidence']} | {r['strength']} |")
        L.append("")

    # 附：各篇 frontmatter module 字段分布（帮助判断字段可靠性）
    L.append("## 附：各篇源文件 frontmatter `module` 字段分布 TOP20")
    L.append("")
    for module, _c, _e in MODULES:
        top = fmod_dist[module].most_common(20)
        L.append(f"### {module}")
        L.append("")
        L.append("```")
        for v, n in top:
            L.append(f"{n:>5}  {v}")
        L.append("```")
        L.append("")

    OUT_REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"报告已写入: {OUT_REPORT}")


if __name__ == "__main__":
    main()
