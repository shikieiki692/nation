import io, os, sys
from collections import Counter
from importlib import import_module

_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stdout = _stdout

"""只读巡检：复现 build_module_book 的分类结果，列出落到兜底章节/可疑分类的源文件。"""

_here = os.path.dirname(os.path.abspath(__file__))
_root = _here
while not os.path.isdir(os.path.join(_root, "04-题库")):
    _next = os.path.dirname(_root)
    if _next == _root:
        raise SystemExit("未找到 vault 根目录（04-题库）")
    _root = _next
os.chdir(_root)
if _here not in sys.path:
    sys.path.insert(0, _here)

bm = import_module("build_module_book")

MODULE_SPECS = [
    ("结构化学", bm.STRUCTURE_MAP, (99, "综合"), None),
    ("元素与分析", bm.YSFX_MAP, (99, "综合"), None),
    ("化学原理", bm.CHEM_MAP, (6, "综合"), None),
    ("有机化学", bm.ORGANIC_MAP, (6, "综合"), bm.ORGANIC_EXCLUDE),
]


def build_report(module, chapter_map, fallback, exclude_subs=None):
    all_pool = bm.gather_questions(module)
    exclude_subs = set(exclude_subs or [])
    pool = [q for q in all_pool if q["submodule"] not in exclude_subs]
    print(f"\n===== {module} 源库活跃题量 ===== {len(all_pool)}")
    if exclude_subs:
        exc = Counter(q["submodule"] for q in all_pool if q["submodule"] in exclude_subs)
        detail = "、".join(f"{k}×{v}" for k, v in exc.most_common())
        print(f"生成器设计排除（不进书）：{detail}")
    groups = {}
    for item in pool:
        res = bm.classify_by_keywords(item, chapter_map, module)
        if res is None:
            res = fallback
        groups.setdefault(res, []).append(item)
    fb_items = groups.get(fallback, [])
    print(f"\n===== {module} 章节分布 =====")
    for key, items in sorted(groups.items()):
        print(f"  第{key[0]}章 {key[1]}: {len(items)} 题")
    print(f"\n===== {module} 兜底章节 ===== 共 {len(fb_items)} 题")
    for item in sorted(fb_items, key=lambda x: x["path"]):
        sub = item["submodule"] or "(空)"
        print(f"  {item['path']}  [sub={sub}]")
    print(f"===== {module} 兜底 submodule 统计 =====")
    for k, v in Counter(x["submodule"] or "(空)" for x in fb_items).most_common():
        print(f"  {k}: {v}")


def elements_ch1_decision(item):
    """给元素篇第1章条目一个可执行建议，收窄旧版的纯路径弱误报。"""
    path = item["path"]
    if path.startswith("化学原理/Ch02-气体/02-27"):
        return "参考：留元素篇第1章（气体基础计量）；未来若建气体章再迁移"
    if path.startswith("化学原理/Ch08-酸碱平衡/08-34"):
        return "建议改篇：酸碱平衡 → 化学原理第5章溶液与酸碱平衡"
    if path.startswith("化学原理/Ch09-沉淀溶解平衡/09-26"):
        return "建议改篇：沉淀溶解平衡 → 化学原理第5章溶液与酸碱平衡"
    if path.startswith("化学原理/Ch09-沉淀溶解平衡/09-27"):
        return "建议改篇：沉淀溶解平衡 → 化学原理第5章溶液与酸碱平衡"
    if "上海中学竞赛课程" in path and "溶液和胶体" in path:
        return "暂留：溶液/胶体基础；若未来新增化学原理溶液章再迁移"
    if "赵鑫光" in path and "基础-例9" in path:
        return "暂留：溶液依数性基础；同时归 Q-A 真无答案桶优先补"
    if "赵鑫光" in path and "基础-习13" in path:
        return "已迁移：蒸气压/分子缔合基础计量 → 元素篇第1章"
    if "第29届初赛" in path:
        return "建议改章：方程式/元素推断 → 元素篇第2章或第5章（非第1章）"
    if "第30届初赛" in path:
        return "建议改篇：分压/Kp → 化学原理第2章化学平衡（submodule 改 化学平衡）"
    if "第31届初赛" in path:
        if "3-1-铋" in path:
            return "建议改章：铋推断/热重 → 元素篇第5章元素推断"
        return "建议改章：主族元素方程式 → 元素篇第2章离子反应或第3章主族"
    if "第39届初赛" in path:
        if "4-1-碘量法" in path:
            return "建议改章：碘量法 → 元素篇第6章化学分析"
        if "6-1" in path:
            return "建议改篇：高压储氢/vdW/相图 → 化学原理第2章化学平衡"
        if "1-4" in path:
            return "建议改篇：彩金热力学计算 → 化学原理第1章热力学"
    if "第37届初赛" in path and "7-1-3" in path:
        return "合理保留：物理化学计量与数据处理 → 元素篇第1章（暂不新建物化章）"
    if "第32届初赛" in path:
        return "正常：同位素/核化学 → 元素篇第1章合理"
    if any(x in path for x in (
        "第25届初赛", "第27届初赛", "第28届初赛", "第33届初赛", "第34届初赛",
    )):
        return "正常：化学史/气体/化学计量 → 元素篇第1章合理"
    return "需人工复核"


def show_elements_ch1_suspects():
    """元素篇第1章：只列分类结果+决策建议，弱路径误报收敛到具体操作。"""
    print("\n===== 元素与分析 第1章 清单与决策建议 =====")
    pool = bm.gather_questions("元素与分析")
    rows = []
    for item in sorted(pool, key=lambda x: x["path"]):
        res = bm.classify_by_keywords(item, bm.YSFX_MAP, "元素与分析")
        if res and res[0] == 1:
            rows.append((item["path"], item["module"] or "(空)", item["submodule"] or "(空)",
                         elements_ch1_decision(item)))
    if not rows:
        print("  无")
    for path, mod, sub, dec in rows:
        print(f"  {path}  [module={mod} sub={sub}]")
        print(f"      -> {dec}")
    print("\n决策分布：")
    for k, v in Counter(x[3] for x in rows).most_common():
        print(f"  {k}: {v}")


def chem_unclassified_decision(item):
    """化学原理第6章综合里的题逐个给归属建议。"""
    path = item["path"]
    if "赵鑫光" in path and "习13" in path:
        return "Q-A 真无答案；内容=蒸气压，暂留综合，未来建议并入第2章化学平衡或新建蒸气压节"
    if "第30届初赛" in path:
        return "建议改 submodule=化学平衡 → 第2章化学平衡（与 6-1 同系列）"
    if "036b-7-3" in path:
        return "可选：核反应/氦-3 → 结构化学第1章原子结构（含核化学）或元素篇第1章，需定篇"
    if "038-4-3" in path:
        return "可选：胶束/分子间作用力 → 结构化学第2章分子结构或元素篇第1章，需定篇"
    if "038-8-5" in path:
        return "建议按内容：聚脲氢键/有机材料 → 有机化学第1章结构基础或第12章高分子"
    if "039-2-4" in path:
        return "综合题可留第6章；若拆分，主块建议归第4章氧化还原与电化学"
    return "需人工复核"


def show_chem_unclassified():
    """化学原理：列出真正落到第6章综合的题，替代旧版漏检。"""
    print("\n===== 化学原理 第6章（综合/未分类）清单与决策建议 =====")
    pool = bm.gather_questions("化学原理")
    rows = []
    for item in sorted(pool, key=lambda x: x["path"]):
        res = bm.classify_by_keywords(item, bm.CHEM_MAP, "化学原理")
        if res and res[0] == 6:
            rows.append((item["path"], item["submodule"] or "(空)", chem_unclassified_decision(item)))
    if not rows:
        print("  无")
    for path, sub, dec in rows:
        print(f"  {path}  [sub={sub}]")
        print(f"      -> {dec}")
    print(f"共 {len(rows)} 题")


if __name__ == "__main__":
    for module, chapter_map, fallback, exclude_subs in MODULE_SPECS:
        build_report(module, chapter_map, fallback, exclude_subs)
    show_chem_unclassified()
    show_elements_ch1_suspects()
