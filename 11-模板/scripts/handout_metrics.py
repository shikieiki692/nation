# -*- coding: utf-8 -*-
"""讲义/源口径统一度量器 v2（替换 vault_deep_audit.py 的失真判据）

修订要点（2026-09-24 独立审查实证）：
1. sources 分类不再看字符串里有没有 "07-资料提炼"，而是 **把 wikilink 解析到真实文件再按路径判定**。
   旧判据把 [[提炼-结构化学基础-第2章]] 这类短链当成「原文」，导致「原文 11.8%」虚高（实测真原文 1/127）。
2. 练习题节不再只认 `^## ...练习题`，改为多级标题 + 多种命名（练习/习题/三级练习/真题挑战/真题演练/
   习题与思考/本章练习/自我检验），旧判据把 15 份有完整练习区的讲义判成「缺」。
3. 自带自证：打印扫描文件数、FM 命中数、sources 解析率、练习题命中明细，扫 0 行视为静默失效。

用法：
  python handout_metrics.py                      # 打印控制台明细
  python handout_metrics.py --csv <out.csv>      # 同时导出逐份 CSV
  python handout_metrics.py --self-check         # 只跑自证断言
"""
import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # …/妙妙屋
LECT_ROOT = ROOT / "04-课件" / "学生讲义"

SKIP_DIRS = {".git", ".workbuddy", "node_modules", ".obsidian", ".claude",
             ".claudian", ".trash", "__pycache__", ".venv", "venv"}

HAN = re.compile(r"[\u4e00-\u9fff]")
COMMENT = re.compile(r"<!--.*?-->", re.S)
FM = re.compile(r"^---\n(.*?)\n---\n", re.S)
SRC_BLOCK = re.compile(r"^sources:[ \t]*\n((?:[ \t]*-[ \t]*.*\n|[ \t]*\n)*)", re.M)
SRC_ITEM = re.compile(r"^\s*-\s*[\"']?\[\[([^\]\"|\n]+)", re.M)

# 旧版 HASEX（保留以便对照）
OLD_HASEX = re.compile(r"^##\s*[一二三四五六七八九十]*[、.]?\s*练习题", re.M)
# 新版：多级标题 + 多命名
EX_HEAD = re.compile(
    r"^(#{1,6})\s*[§0-9一二三四五六七八九十（）()]*\s*[、.]?\s*"
    r"(练习题|习题|练习|课后练习|三级练习|本章练习|真题挑战|真题演练|真题精练|自我检验|自测)", re.M)
EX_ITEM = re.compile(r"^\*\*\s*(\d+)\s*[\.．、]", re.M)

# 警示/提醒类板块（↘ 用户要求：重心放内容本身，不得堆叠无用「易错点/注意点」）
ALERT_HEAD = re.compile(
    r"^#{1,6}\s*.*(易错点|易错提醒|易错警示|易混点|常见错误|注意事项|提醒|误区|避坑|坑点|陷阱|陷阱题)", re.M)
ALERT_CALLOUT = re.compile(r"^>\s*\[!(warning|danger|caution)\]", re.M)
#警示类 callout 内部再分：真·「易错/注意/误区」类 vs 安全/口径等合规用途
ALERT_WORD = re.compile(r"(易错|注意|误区|陷阱|坑|提醒|常见错误|混淆)")
# 伪标签白名单：模板固有栏目（实测 4855 命中里绝大多数是这些，不可当缺陷报）
WHITE_LABELS = {
    "解析", "答案", "题干", "题目", "思路", "解答", "口诀", "定义", "结论", "示例", "例题",
    "练习", "习题", "小结", "本节小结", "速查", "推断信号", "真题", "来源", "出处", "步骤",
    "分析", "计算", "判断", "应用", "拓展", "补充", "附录", "参考", "备注", "要点", "重点",
    "难点", "目标", "要求", "说明", "反例", "例", "性质", "规律", "特点", "条件", "适用",
    "范围", "单位", "符号", "命名", "结构", "机理", "现象", "数据", "公式", "推导", "实验",
    "安全", "使用建议", "教学提示", "难度", "轮次", "考纲对应",
}
CALLOUT_ANY = re.compile(r"^>\s*\[!\w+\]", re.M)
PSEUDO_LABEL = re.compile(r"\*\*[^*\n]{2,10}\*\*[：:]")
META_LINE = re.compile(
    r"^>\s*\*\*(关联知识点|为什么先讲|关联真题|主线|深度边界|学习建议|建议使用方式|使用说明)", re.M)
ANALOGY_HINT = re.compile(r"(生活中|生活里|打个比方|打个比喻|就好像|就像.{0,12}(一样|那样)|想象一下|好比|类似于.{0,8}关系|像.{0,6}(家长|父母|孩子|将军|士兵|老板|员工|邻居|朋友))")

# S/A 级源池（按《教材选用与内容编排规范》§1.1b 两源池口径）
S_PREFIX = (
    "mineru/03-教材书籍/",
    "clayden 有机化学/",
    "中级无机化学/",
    "无机化学 习题集/",
    "Mathematics for Physical Chemistry/",
    "人教版初中化学教材/",
    "bdwp资源/",
    "结构化学习题与解析/",
    "06-外部资料导入/上海中学竞赛教程/",
    "06-外部资料导入/化学竞赛初赛讲义/",
    "06-外部资料导入/结构化学基础/",
    "06-外部资料导入/无机化学下册/",
    "06-外部资料导入/人教版教材/",
    "06-外部资料导入/一化 高中化学/",
    "06-外部资料导入/书籍/",
    "06-外部资料导入/习题普通化学/",
    "06-外部资料导入/25-32届真题解析/",
    "高中化学竞赛笔记/",
)
B_NOTE_KEY = ("Zchem", "质心", "学而思", "有机反应合成与机理")


def build_index():
    """全库 md 索引：相对路径集合 + basename 映射。返回 (allrel, basemap, scanned)"""
    allrel, basemap = set(), {}
    scanned = 0
    for dp, dns, fns in os.walk(ROOT):
        rel_dp = os.path.relpath(dp, ROOT)
        parts = [] if rel_dp == "." else rel_dp.split(os.sep)
        if any(p in SKIP_DIRS for p in parts):
            dns[:] = []
            continue
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if not fn.lower().endswith(".md"):
                continue
            rel = fn if rel_dp == "." else (rel_dp + "/" + fn).replace("\\", "/")
            allrel.add(rel)
            basemap.setdefault(fn[:-3], []).append(rel)
            scanned += 1
    return allrel, basemap, scanned


def resolve(entry, allrel, basemap):
    e = entry.strip().split("#")[0].split("|")[0].strip()
    if not e:
        return None
    if "/" in e:
        cand = e if e.lower().endswith(".md") else e + ".md"
        return cand if cand in allrel else None
    hits = basemap.get(e, [])
    return hits[0] if hits else None


def classify(rel):
    if rel is None:
        return "断链"
    for p in S_PREFIX:
        if rel.startswith(p):
            if any(k in rel for k in B_NOTE_KEY):
                return "B笔记"
            return "原文源池"
    if any(k in rel for k in B_NOTE_KEY):
        return "B笔记"
    if rel.startswith("07-资料提炼/"):
        return "提炼页"
    if rel.startswith(("04-题库/", "05-真题库/")):
        return "题库/真题卡"
    if rel.startswith("03-知识点/"):
        return "知识点页"
    if rel.startswith(("04-课件/", "13-教案/", "12-教学洞察/", "00-首页/", "11-模板/", "04-专题与题型/")):
        return "内部产物"
    return "其他"


def _alert_callouts(text):
    """warning/danger/caution callout 中，首行含「易错/注意/误区/陷阱」等词的条数"""
    n = 0
    for m in ALERT_CALLOUT.finditer(text):
        seg = text[m.end():m.end() + 120]
        if ALERT_WORD.search(seg):
            n += 1
    return n


META_KW = re.compile(
    r"(关联|对应|定位|建议|要求|边界|衔接|覆盖|说明|版本|主线|反思|易错|注意|类比|策略|"
    r"提示|本讲|本节|小节|考纲|备课|专题页|深度|层级|记忆|信号|口诀|题源|来源)")


def _custom_labels(text):
    """**标签**：` 形态中「疑似元信息/装饰性标签」数。
    口径：不在模板固有栏目白名单内 **且** 命中元信息关键词。
    ⚠️ 这是**候选线索**而非缺陷计数——长尾一次性标签须人工判定，不得据此判缺陷。"""
    n = 0
    for m in PSEUDO_LABEL.finditer(text):
        inner = m.group(0)[2:-3].strip()
        if inner not in WHITE_LABELS and META_KW.search(inner):
            n += 1
    return n


def exercise_stats(text):
    """返回 (命中标题列表, 练习题条目估算数)"""
    heads, n = [], 0
    for m in EX_HEAD.finditer(text):
        level, name = len(m.group(1)), m.group(2)
        heads.append(f"H{level}:{name}")
        # 从该标题行往后取到下一个同级或更高级标题
        start = m.end()
        rest = text[start:]
        stop = re.search(r"^#{1,%d}\s+\S" % level, rest, re.M)
        seg = rest[:stop.start()] if stop else rest
        n += len(EX_ITEM.findall(seg))
    return heads, n


def metrics_of(path, allrel, basemap):
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
    han = len(HAN.findall(text))
    fm_m = FM.match(text)
    fm = fm_m.group(1) if fm_m else ""
    body = text[fm_m.end():] if fm_m else text
    visible = COMMENT.sub("", body)

    src_m = SRC_BLOCK.search(fm)
    entries = SRC_ITEM.findall(src_m.group(1)) if src_m else []
    cats = []
    for e in entries:
        cats.append(classify(resolve(e, allrel, basemap)))
    heads, ex_n = exercise_stats(text)

    return {
        "file": path.name,
        "lines": lines,
        "han": han,
        "hanK": han // 1000,
        "src_n": len(entries),
        "src_true_orig": sum(1 for c in cats if c == "原文源池"),
        "src_refined": sum(1 for c in cats if c == "提炼页"),
        "src_bank": sum(1 for c in cats if c == "题库/真题卡"),
        "src_kp": sum(1 for c in cats if c == "知识点页"),
        "src_note": sum(1 for c in cats if c == "B笔记"),
        "src_internal": sum(1 for c in cats if c == "内部产物"),
        "src_other": sum(1 for c in cats if c == "其他"),
        "src_broken": sum(1 for c in cats if c == "断链"),
        "kp_inline": visible.count("关联知识点"),
        "warn": visible.count("\u26a0"),
        "ex_heads": ";".join(heads[:4]),
        "ex_n": ex_n,
        "old_hasex": bool(OLD_HASEX.search(text)),
        "alert_head": len(ALERT_HEAD.findall(text)),
        "alert_callout": _alert_callouts(text),
        "alert_callout_all": len(ALERT_CALLOUT.findall(text)),
        "pseudo_total": len(PSEUDO_LABEL.findall(text)),
        "pseudo_custom": _custom_labels(text),
        "callout": len(CALLOUT_ANY.findall(text)),
        "pseudo_label": len(PSEUDO_LABEL.findall(text)),
        "meta_line": len(META_LINE.findall(text)),
        "analogy_hint": len(ANALOGY_HINT.findall(text)),
        "has_sources_field": bool(src_m and entries),
        "categories": cats,
        "entries": entries,
    }


def collect(include_readme=False):
    allrel, basemap, scanned = build_index()
    rows = []
    for p in sorted(LECT_ROOT.rglob("*.md")):
        relv = str(p.relative_to(ROOT)).replace("\\", "/")
        parts = relv.split("/")
        mod = parts[-2] if len(parts) >= 2 else ""
        if not re.match(r"^[1-6]-", mod):
            continue
        if not include_readme and p.name.startswith("README"):
            continue
        d = metrics_of(p, allrel, basemap)
        d["module"] = mod
        rows.append(d)
    return rows, scanned


def self_check(rows, scanned):
    print("== 自证 ==")
    print(f"  扫描全库 md 文件数     : {scanned}")
    print(f"  纳入统计的现役讲义      : {len(rows)}（六栏目、已排除 README 类）")
    entries = [e for r in rows for e in r["entries"]]
    print(f"  sources 条目总数        : {len(entries)}")
    broken = sum(r["src_broken"] for r in rows)
    print(f"  解析失败的条目          : {broken}")
    cat_sum = {k: sum(r[k] for r in rows) for k in
               ("src_true_orig", "src_refined", "src_bank", "src_kp", "src_note",
                "src_internal", "src_other")}
    print(f"  二手档位(提炼页+B笔记)  : {cat_sum['src_refined'] + cat_sum['src_note']}")
    print(f"  分类合计(不含断链)      : {sum(cat_sum.values())}  {cat_sum}")
    print(f"  行合计/汉字合计         : {sum(r['lines'] for r in rows)} 行 / {sum(r['han'] for r in rows)//1000}K")
    print(f"  练习节命中数(新口径)    : {sum(1 for r in rows if r['ex_heads'])} / {len(rows)}")
    print(f"  练习节命中数(旧口径)    : {sum(1 for r in rows if r['old_hasex'])} / {len(rows)}")
    assert scanned > 10000, "全库索引扫得太少，疑似静默失效"
    assert len(rows) > 0, "未扫到讲义"
    assert sum(cat_sum.values()) + broken == len(entries), "sources 分类不守恒"
    return True


FIELDS = ["module", "file", "lines", "hanK", "src_n", "src_true_orig", "src_refined",
          "src_bank", "src_kp", "src_note", "src_internal", "src_other", "src_broken",
          "kp_inline", "warn", "ex_heads", "ex_n", "old_hasex",
          "alert_head", "alert_callout", "alert_callout_all", "callout",
          "pseudo_total", "pseudo_custom", "meta_line", "analogy_hint"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="导出逐份 CSV 路径")
    ap.add_argument("--json", help="导出 JSON 路径")
    ap.add_argument("--include-readme", action="store_true")
    ap.add_argument("--self-check", action="store_true", help="只跑自证断言")
    args = ap.parse_args()

    rows, scanned = collect(args.include_readme)
    self_check(rows, scanned)
    if args.self_check:
        print("自证通过。")
        return

    print()
    print(f"{'栏目':14s} {'文件':46s} {'行':>5s} {'汉字K':>6s} {'src':>4s} {'原文':>4s} {'提炼':>4s} {'关联':>4s} {'warn':>4s} {'练习':>4s} {'旧判有':>6s} {'警示块':>6s}")
    for r in sorted(rows, key=lambda x: (x["module"], x["file"])):
        print(f"{r['module']:14s} {r['file'][:44]:46s} {r['lines']:5d} {r['hanK']:6d} "
              f"{r['src_n']:4d} {r['src_true_orig']:4d} {r['src_refined']:4d} "
              f"{r['kp_inline']:4d} {r['warn']:4d} {r['ex_n']:4d} "
              f"{str(r['old_hasex']):>6s} {r['alert_head']+r['alert_callout']:6d}")

    print()
    print("== 汇总 ==")
    print(f"  有 sources / 无 sources : {sum(1 for r in rows if r['src_n']>0)} / {sum(1 for r in rows if r['src_n']==0)}")
    print(f"  含 ≥1 条真原文(S/A 池)   : {sum(1 for r in rows if r['src_true_orig']>0)}")
    print(f"  练习节：新口径有 / 旧口径有 : {sum(1 for r in rows if r['ex_heads'])} / {sum(1 for r in rows if r['old_hasex'])}")
    print(f"  警示类小标题             : {sum(r['alert_head'] for r in rows)}")
    print(f"  警示类 callout（含易错/注意等词）: {sum(r['alert_callout'] for r in rows)}"
          f" （warning/danger/caution 全量 {sum(r['alert_callout_all'] for r in rows)}）")
    print(f"  `**标签**：` 命中总量     : {sum(r['pseudo_total'] for r in rows)}"
          f"  其中非模板栏目（自创伪标签）: {sum(r['pseudo_custom'] for r in rows)}")
    print(f"  元信息行（关联知识点等）  : {sum(r['meta_line'] for r in rows)}")
    print(f"  类比体疑似句（待人工核） : {sum(r['analogy_hint'] for r in rows)}")

    if args.csv:
        out = Path(args.csv)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
            w.writeheader()
            for r in sorted(rows, key=lambda x: (x["module"], x["file"])):
                w.writerow(r)
        print(f"\nCSV 已写出：{out}")
    if args.json:
        out = Path(args.json)
        out.write_text(json.dumps([{k: v for k, v in r.items()
                                    if k not in ("categories", "entries")} for r in rows],
                                  ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"JSON 已写出：{out}")


if __name__ == "__main__":
    main()
