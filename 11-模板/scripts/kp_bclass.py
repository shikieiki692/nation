# -*- coding: utf-8 -*-
"""①-b 纯文本标签二次分类。

knowledge_points 等字段里「不带 [[]] 的纯文本项」并不都是问题：
绝大多数是一次性描述（具体反应对、制备工艺、分离方案、性质规律），
它们描述的是"这道题做了什么"而非可复用知识点，留作纯文本是正确归宿
——既全文可检索，又不会在图谱里造出单例孤儿节点。

本脚本按规则把它们分门别类，把「真概念缺口」从噪音里筛出来。

用法:
    python -X utf8 11-模板/scripts/kp_bclass.py            # 打印分类概览
    python -X utf8 11-模板/scripts/kp_bclass.py --write    # 落 09-审计报告

判据（勿丢）：一个 token 该不该成为 KP，看它有没有第二道题会用到。
    「FeCl3与KI」只属于这一道配平题；「配体效应」会出现在所有均相催化的题里。
"""
import os, re, sys
from collections import Counter, defaultdict

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(VAULT, "11-模板", "scripts"))

# 复用巡检的解析口径（basename_map 优先 / alias_map 兜底），避免两套标准
_o = sys.exit
sys.exit = lambda *a, **k: None      # 巡检末尾 sys.exit(1) 是正常信号
import kp_link_patrol as P           # noqa: E402
sys.exit = _o

# ── 分类规则：顺序敏感，先特殊后一般 ──────────────────────────────
RULES = [
    ("B2 制备与工艺",
     re.compile(r"制备|合成|制法|制锑|制铋|提纯|生产")),
    ("B3 分离·鉴别·除杂",
     re.compile(r"鉴别|分离|除杂|鉴定|检验")),
    ("B1 具体反应对",
     re.compile(r"与.*(反应|盐酸|硫酸|硝酸|氢碘酸|溴水|碘水|氨水|NaOH|KOH|KI|KSCN|碳酸钠|空气)|"
                r"^(Cl2|Fe|Co|Ni|Mn|Pd|Ru|Sn)\d?.*与|被空气氧化|氧化为|氧化还原|"
                r"还原Fe|氧化Cl|氧化CN|氧化Mn|与铜盐|"
                r"(氧化|还原|反应)$|系列反应|氢化物反应|转化反应")),
    ("B4 热分解·性质规律",
     re.compile(r"分解|酸性|还原性|氧化性|水解|歧化|原理|现象|性质|影响|处理|清洗|催化")),
]

# 非化学概念：不该做化学 KP，单独标注避免误判为缺口
NOT_CONCEPT = {"动量"}

VERDICT = {
    "B1 具体反应对": ("本就不是概念，是一次性反应描述", "保持纯文本"),
    "B2 制备与工艺": ("工艺路线，非单一知识点", "保持纯文本"),
    "B3 分离·鉴别·除杂": ("方案类描述，依题而异", "保持纯文本"),
    "B4 热分解·性质规律": ("规律类，多已由父页覆盖", "保持纯文本 / 少数回指父页"),
    "B5 非化学概念": ("物理/数学基础量，不该做化学 KP", "保持纯文本"),
    "B6 其他/待定": ("需人工判断", "逐条看"),
}
ORDER = ["B1 具体反应对", "B2 制备与工艺", "B3 分离·鉴别·除杂",
         "B4 热分解·性质规律", "B5 非化学概念", "B6 其他/待定"]


def classify(tok):
    if tok in NOT_CONCEPT:
        return "B5 非化学概念"
    for name, rx in RULES:
        if rx.search(tok):
            return name
    return "B6 其他/待定"


def build():
    cnt = Counter(x[2] for x in P.B)
    files = defaultdict(set)
    for rel, _field, tok in P.B:
        files[tok].add(rel)

    groups = defaultdict(list)
    for tok, n in cnt.most_common():
        groups[classify(tok)].append((tok, n))

    out = ["# ①-b 纯文本标签 · 二次分类", "",
           "巡检口径：`knowledge_points` 等字段中**不带 `[[]]` 的纯文本项**，且无法解析到任何 KP。",
           "共 **%d 条**。" % len(P.B), "",
           "## 分类总览", "",
           "| 类别 | 条数 | 判定 | 处置 |", "|---|---:|---|---|"]
    for k in ORDER:
        v = groups.get(k, [])
        if not v:
            continue
        d, act = VERDICT[k]
        out.append("| %s | %d | %s | %s |" % (k, len(v), d, act))
    out.append("")

    for k in ORDER:
        v = groups.get(k, [])
        if not v:
            continue
        d, act = VERDICT[k]
        out += ["## %s（%d 条）" % (k, len(v)), "",
                "> %s → **%s**" % (d, act), "",
                "| token | 来源文件 |", "|---|---|"]
        for tok, _n in sorted(v):
            out.append("| %s | %s |" % (tok, os.path.basename(sorted(files[tok])[0])[:52]))
        out.append("")

    out += ["## 结论", "",
            "**待定项为 0 即代表：这批纯文本里没有需要新建 KP 的真概念缺口。**",
            "它们描述的是「这道题做了什么」，不是可复用的知识点。", "",
            "> 判据：一个 token 该不该成为 KP，看它**有没有第二道题会用到**。",
            "> 「FeCl3与KI」只属于这一道配平题；「配体效应」会出现在所有均相催化的题里。", ""]
    return out, groups


if __name__ == "__main__":
    lines, groups = build()
    for k in ORDER:
        v = groups.get(k, [])
        if v:
            print("  %-20s %d" % (k, len(v)))
    print("  合计", len(P.B))
    todo = sorted(groups.get("B6 其他/待定", []))
    if todo:
        print("\n=== 待人工判断 ===")
        for tok, _n in todo:
            print("  ", tok)
    if "--write" in sys.argv:
        import datetime
        d = os.path.join(VAULT, "09-审计报告")
        os.makedirs(d, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y-%m-%d")
        dst = os.path.join(d, "①b-纯文本标签二次分类_%s.md" % ts)
        open(dst, "w", encoding="utf-8", newline="").write("\n".join(lines))
        print("\n报告已写出:", os.path.relpath(dst, VAULT))
