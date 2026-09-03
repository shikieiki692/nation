# -*- coding: utf-8 -*-
"""KP 链接健康巡检 —— 一次跑出全库链接健康表。

用法:
    python -X utf8 11-模板/scripts/kp_link_patrol.py            # 巡检并打印摘要
    python -X utf8 11-模板/scripts/kp_link_patrol.py --report   # 同时落 Markdown 报告

巡检项:
    A  带 .md 后缀的断链（[[xxx.md]]，去后缀即命中）
    B  knowledge_points 等字段里的纯文本标签（非断链，仅统计）
    C  指向弃用页的引用（应改指 superseded_by）
    D  真孤儿（全库无对应笔记）
    E  source_notes / prerequisite 悬空
    F  弃用页清单与被引用次数
    G  js-yaml 4 解析失败（需 Node，缺失则跳过）

重要口径（勿改）:
    KP 解析必须分 basename_map（文件名优先）/ alias_map（title/alias 兜底）两张表。
    合成一张 setdefault 会让弃用页的 alias 抢占活跃页文件名，
    把有效链接误报成「指向弃用页」，且结果随 os.walk 顺序漂移。
"""
import os, re, sys, yaml, subprocess, datetime
from collections import Counter, defaultdict

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KP_DIR = os.path.join(VAULT, "03-知识点")
QB_DIRS = [os.path.join(VAULT, "04-题库"), os.path.join(VAULT, "05-真题库")]
QB_LINK_FIELDS = ["knowledge_points", "depends_on", "cross_references", "related", "superseded_by"]
DEP_STATUS = ("deprecated", "已废弃", "已合并", "重定向")
LINK_RE = re.compile(r"\[\[([^\]\n]+?)\]\]")
REPORT = "--report" in sys.argv


def load_fm(path):
    try:
        t = open(path, encoding="utf-8", newline="").read()
    except Exception:
        return None
    if not t.startswith("---"):
        return {}
    e = t.find("\n---", 3)
    if e == -1:
        return {}
    try:
        d = yaml.safe_load(t[3:e])
    except Exception:
        return {"__parse_error__": True}
    return d if isinstance(d, dict) else {}


def as_list(v):
    if v is None: return []
    if isinstance(v, list): return v
    return [v]


def strip_link(s):
    """兼容 '[[X|显示#锚]]' 与 'X|显示#锚'"""
    s = s.strip()
    if s.startswith("[[") and s.endswith("]]"):
        s = s[2:-2]
    return s.split("|")[0].split("#")[0].strip()


# ── 1. KP 宇宙（两张表）───────────────────────────────────────────
basename_map, alias_map, meta, dep_pages = {}, {}, {}, {}
for r, d, fs in os.walk(KP_DIR):
    for fn in fs:
        if not fn.endswith(".md"): continue
        p = os.path.join(r, fn)
        fm = load_fm(p)
        if not fm or "__parse_error__" in fm: continue
        meta[p] = fm
        basename_map.setdefault(fn[:-3].lower(), p)
        title = fm.get("title")
        if title: alias_map.setdefault(str(title).lower(), p)
        for a in as_list(fm.get("aliases")):
            if isinstance(a, str): alias_map.setdefault(a.lower(), p)
        if fm.get("status") in DEP_STATUS or fm.get("deprecated"):
            dep_pages[p] = fm


def resolve_kp(lt):
    k = strip_link(lt).lower()
    if k in basename_map: return basename_map[k]
    if "/" in k:
        leaf = k.rsplit("/", 1)[1]
        if leaf in basename_map: return basename_map[leaf]
        if leaf in alias_map:    return alias_map[leaf]
    if k in alias_map: return alias_map[k]
    return None


# ── 2. 全库笔记名（判断"指向非 KP 笔记"是否合法）──────────────────
vault_bn, vault_alias = set(), set()
for r, d, fs in os.walk(VAULT):
    if "/." in r.replace("\\", "/"):
        d[:] = []
        continue
    for fn in fs:
        if not fn.endswith(".md"): continue
        vault_bn.add(fn[:-3].lower())
        fm = load_fm(os.path.join(r, fn))
        if isinstance(fm, dict) and "__parse_error__" not in fm:
            for a in as_list(fm.get("aliases")):
                if isinstance(a, str): vault_alias.add(a.lower())


def resolve_any(lt):
    k = strip_link(lt).lower()
    if k in vault_bn: return True
    if "/" in k and k.rsplit("/", 1)[1] in vault_bn: return True
    return k in vault_alias


# ── 3. 扫描题库链接字段 ───────────────────────────────────────────
A, C, D, B, DEP_HIT = [], [], [], [], Counter()
for qdir in QB_DIRS:
    for r, d, fs in os.walk(qdir):
        for fn in fs:
            if not fn.endswith(".md"): continue
            p = os.path.join(r, fn)
            fm = load_fm(p)
            if not fm or "__parse_error__" in fm: continue
            rel = os.path.relpath(p, VAULT)
            for field in QB_LINK_FIELDS:
                if field not in fm: continue
                for item in as_list(fm[field]):
                    s = str(item)
                    if "[[" in s:
                        for m in LINK_RE.findall(s):
                            lt = strip_link(m)
                            if not lt: continue
                            tgt = resolve_kp(lt)
                            if tgt:
                                if tgt in dep_pages:
                                    C.append((rel, field, lt, os.path.basename(tgt)[:-3]))
                                    DEP_HIT[os.path.basename(tgt)[:-3]] += 1
                                continue
                            if resolve_any(lt): continue
                            if lt.lower().endswith(".md"):
                                A.append((rel, field, lt))
                            else:
                                D.append((rel, field, lt))
                    elif s.strip():
                        if resolve_kp(s.strip()): continue
                        B.append((rel, field, s.strip()))

# ── 4. 全库 source_notes / prerequisite 悬空 ──────────────────────
E = []
for r, d, fs in os.walk(VAULT):
    if "/." in r.replace("\\", "/"):
        d[:] = []
        continue
    for fn in fs:
        if not fn.endswith(".md"): continue
        p = os.path.join(r, fn)
        fm = load_fm(p)
        if not isinstance(fm, dict) or "__parse_error__" in fm: continue
        for field in ("source_notes", "prerequisite", "prerequisites"):
            if field not in fm: continue
            for item in as_list(fm[field]):
                for m in LINK_RE.findall(str(item)):
                    lt = strip_link(m)
                    if lt and not resolve_any(lt) and not resolve_kp(lt):
                        E.append((os.path.relpath(p, VAULT), field, lt))

# ── 5. js-yaml 闸门 ───────────────────────────────────────────────
jsy = None
try:
    node = r"C:/Users/蕾赛/.workbuddy/binaries/node/versions/22.22.2-2/node.exe"
    nm = r"C:/Users/蕾赛/.workbuddy/binaries/node/workspace/node_modules"
    js = os.path.join(VAULT, "11-模板", "scripts", "jsyaml_verify.js")
    if os.path.isfile(node) and os.path.isfile(js):
        env = dict(os.environ, NODE_PATH=nm)
        out = subprocess.run([node, js, "--dir", "."], cwd=VAULT,
                             capture_output=True, text=True, timeout=900, env=env)
        m = re.search(r"受检 (\d+) / 通过 \d+ / 无frontmatter \d+ / 失败 (\d+)", out.stdout)
        if m: jsy = (int(m.group(1)), int(m.group(2)))
except Exception:
    pass

# ── 6. 输出 ───────────────────────────────────────────────────────
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
A_u = Counter(x[2] for x in A); C_u = Counter(x[2] for x in C)
D_u = Counter(x[2] for x in D); E_u = Counter(x[2] for x in E)

lines = []
lines.append("# KP 链接健康巡检")
lines.append("")
lines.append("巡检时间：%s　|　活跃 KP %d / 弃用页 %d" %
             (now, len(meta) - len(dep_pages), len(dep_pages)))
lines.append("")
lines.append("| 项 | 内容 | 出现次数 | 去重 | 状态 |")
lines.append("|---|---|---|---|---|")
rows = [
    ("A", "带 `.md` 的断链", len(A), len(A_u), "应清" if A else "干净"),
    ("B", "纯文本标签（非断链，仅统计）", len(B), len(set(x[2] for x in B)), "可接受"),
    ("C", "指向弃用页", len(C), len(C_u), "应清" if C else "干净"),
    ("D", "真孤儿", len(D), len(D_u), "应清" if D else "干净"),
    ("E", "source_notes/prereq 悬空", len(E), len(E_u), "低危"),
]
for k, name, n, u, st in rows:
    flag = "⚠️" if st == "应清" else ("·" if st == "低危" else "✅")
    lines.append("| %s | %s | %d | %d | %s %s |" % (k, name, n, u, flag, st))
if jsy:
    lines.append("| G | js-yaml 4 解析失败 | — | — | %s %d/%d |" %
                 ("✅" if jsy[1] == 0 else "⚠️", jsy[1], jsy[0]))
lines.append("")

for tag, title, rows_, cnt in [
    ("A", "A 带 .md 的断链", A, A_u), ("C", "C 指向弃用页", C, C_u),
    ("D", "D 真孤儿", D, D_u), ("E", "E 悬空链", E, E_u)]:
    if not rows_: continue
    lines.append("## %s（去重 %d）" % (title, len(cnt)))
    lines.append("")
    lines.append("| token | 次数 | 样例文件 |")
    lines.append("|---|---|---|")
    sample = {}
    for row in rows_:          # 兼容 3 元组(A/D/E) 与 4 元组(C，含目标弃用页名)
        sample.setdefault(row[2], row[0])
    for tok, n in cnt.most_common(30):
        lines.append("| %s | %d | %s |" % (tok, n, os.path.basename(sample.get(tok, ""))[:46]))
    lines.append("")

if DEP_HIT:
    lines.append("## F 弃用页被引用 Top（%d 个弃用页被引用）" % len(DEP_HIT))
    lines.append("")
    lines.append("| 弃用页 | 被引用次数 | superseded_by |")
    lines.append("|---|---|---|")
    for bn, n in DEP_HIT.most_common(20):
        sup = None
        for p, fm in dep_pages.items():
            if os.path.basename(p)[:-3] == bn:
                sup = fm.get("superseded_by") or fm.get("redirect_to") or "**缺失**"
                break
        lines.append("| %s | %d | %s |" % (bn, n, sup))
    lines.append("")

miss = [os.path.basename(p)[:-3] for p, fm in dep_pages.items()
        if not (fm.get("superseded_by") or fm.get("redirect_to"))]
if miss:
    lines.append("> ⚠️ 缺 superseded_by 的弃用页：%s" % ", ".join(miss))
    lines.append("")

print("=" * 56)
print("KP 链接健康巡检 %s" % now)
print("  A 带.md断链 %d（去重 %d）" % (len(A), len(A_u)))
print("  B 纯文本标签 %d" % len(B))
print("  C 指向弃用页 %d（去重 %d）" % (len(C), len(C_u)))
print("  D 真孤儿 %d（去重 %d）" % (len(D), len(D_u)))
print("  E 悬空链 %d（去重 %d）" % (len(E), len(E_u)))
if jsy:
    print("  G js-yaml 失败 %d / 受检 %d" % (jsy[1], jsy[0]))
if miss:
    print("  !! 缺 superseded_by 的弃用页:", miss)

if REPORT:
    d = os.path.join(VAULT, "09-审计报告")
    os.makedirs(d, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d")
    out = os.path.join(d, "KP链接健康巡检_%s.md" % ts)
    open(out, "w", encoding="utf-8", newline="").write("\n".join(lines))
    print("\n报告已写出:", os.path.relpath(out, VAULT))

sys.exit(1 if (A or C or D) else 0)
