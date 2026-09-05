# -*- coding: utf-8 -*-
"""把指向【弃用页】的 wikilink 改指其 superseded_by（已归位，原 .workbuddy/tmp/do_r2_c.py）。

   用法: python -X utf8 11-模板/scripts/kp_dep_redirect.py                 预演（默认 scope=qb）
         python -X utf8 11-模板/scripts/kp_dep_redirect.py --scope=kb       知识库侧预演
         python -X utf8 11-模板/scripts/kp_dep_redirect.py --scope=kb --apply  写入

   --scope 作用域（2026-09-03 新增；原工具只覆盖题库，导致非题库积压 262 条残留引用）:
     qb  = 04-题库 + 05-真题库，只改 frontmatter（旧行为，周巡检自动化沿用，默认）
     kb  = 03-知识点/04-课件/07-资料提炼/04-专题与题型/00-首页/01-考纲导航/02-考纲条目/
           06-学生侧材料/08-可视化资源/11-模板/12-教学洞察，**全文扫描**
           ⚠ 刻意排除 04-题库/05-真题库（并行导入会话的工作区）
     all = qb + kb

   安全策略:
     - 只为「目标 superseded_by 存在且指向活跃页」的弃用页建立映射，否则跳过并报告。
     - 只收「链接实际会解析到该弃用页」的 key：弃用页常把目标页名写进自己的 alias
       （当年为不断链），那些 key 会先命中目标页，不能改。
     - 解析分 basename_map / alias_map 两张表（文件名优先、alias 兜底），不可合成一张。
     - EXCLUDE 白名单：弃用页 aliases 里混有泛化/下位概念（价键理论、缺陷、白磷…），
       这些 key 虽解析到弃用页，但语义不等价，一律跳过不自动改。
     - 锚点一律丢弃：目标页无同名小节（已逐条核实），保留会变成死锚点。
     - 字面替换，不 YAML 回写；全文行数不变才落盘。
   已知常态: 并行导入器沿用弃用页名（配位化合物/理想气体状态方程/等电子体原理）会周期性回涨，
             重跑本脚本即可清理；根治需改导入规范用活跃页名（配合物/理想气体/等电子体）。
"""
import os, re, sys, yaml, zipfile, datetime
from collections import Counter, defaultdict

ROOT = "C:/Obsidion/妙妙屋"
KP = os.path.join(ROOT, "03-知识点")
APPLY = "--apply" in sys.argv

# ── 作用域 ────────────────────────────────────────────────────────────
QB_DIRS = ["04-题库", "05-真题库"]
KB_DIRS = ["03-知识点", "04-课件", "07-资料提炼", "04-专题与题型", "00-首页",
           "01-考纲导航", "02-考纲条目", "06-学生侧材料", "08-可视化资源",
           "11-模板", "12-教学洞察"]
SCOPES = {
    "qb": (QB_DIRS, False),   # (目录, 是否全文扫描)
    "kb": (KB_DIRS, True),
    "all": (QB_DIRS + KB_DIRS, True),
}
scope = "qb"
for a in sys.argv[1:]:
    if a.startswith("--scope="):
        scope = a.split("=", 1)[1]
if scope not in SCOPES:
    sys.exit("未知 --scope：%s（可选 qb/kb/all）" % scope)
SCAN_DIRS, FULLTEXT = SCOPES[scope]

FIELDS = ["knowledge_points", "depends_on", "cross_references", "related", "superseded_by"]
DEP_STATUS = ("deprecated", "已废弃", "已合并", "重定向")

# ── 语义不等价，跳过不自动改（09-03 人工核定，理由见注释）────────────────
EXCLUDE = {
    "价键理论",        # 通用成键理论，只是被弃用页「配位化合物」收作 alias；全库 15 处未必是配合物语境
    "缺陷",           # 泛指晶体缺陷，不等于非整比化合物
    "白磷", "红磷", "磷酸", "磷酸盐矿物",   # 具体物质，改指到「磷及其化合物」丢精度
    "Wade规则", "硼烷结构", "碳硼烷", "硼族元素化学",  # 下位/独立/上位概念，与「硼」不等价
    "糖",             # 过泛
    "自由基加成", "加成-消除机理",          # 机理名，与目标非全等
    "Sθ",             # 记号，可能泛指其他熵
    "热力学深化", "电荷平衡深化",          # 可能是独立分层页
}

def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()

def load_fm(p):
    t = read(p)
    if not t.startswith("---"): return {}
    e = t.find("\n---", 3)
    if e == -1: return {}
    try: return yaml.safe_load(t[3:e]) or {}
    except Exception: return {}

def strip_link(s):
    """兼容两种输入：'[[X|显示#锚]]' 完整形式 与 'X|显示#锚' 内部形式"""
    s = s.strip()
    if s.startswith("[[") and s.endswith("]]"):
        s = s[2:-2]
    return s.split("|")[0].split("#")[0].strip()

def deq(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'": s = s[1:-1]
    return s

# ── 1. 建立 KP 宇宙 ──
# ★ 关键：模拟 Obsidian 真实解析优先级 —— 文件名(basename) 优先，alias/title 兜底。
#   分两张表，禁止合成一张后用 setdefault 抢位（会导致弃用页与活跃页互抢，结果随遍历顺序漂移）。
basename_map, alias_map, meta = {}, {}, {}
for r, d, fs in os.walk(KP):
    for fn in fs:
        if not fn.endswith(".md"): continue
        p = os.path.join(r, fn)
        fm = load_fm(p)
        if not isinstance(fm, dict): continue
        meta[p] = fm
        basename_map.setdefault(fn[:-3].lower(), p)
        if fm.get("title"): alias_map.setdefault(str(fm["title"]).lower(), p)
        for a in (fm.get("aliases") or []):
            if isinstance(a, str): alias_map.setdefault(a.lower(), p)

def is_dep(fm):
    return fm.get("status") in DEP_STATUS or fm.get("deprecated")

def resolve(lt):
    """模拟 Obsidian：文件名优先，其次 alias/title；支持 a/b 路径取末段"""
    k = strip_link(lt).lower()
    if k in basename_map: return basename_map[k]
    if "/" in k:
        leaf = k.rsplit("/", 1)[1]
        if leaf in basename_map: return basename_map[leaf]
        if leaf in alias_map: return alias_map[leaf]
    if k in alias_map: return alias_map[k]
    return None

# ── 2. 弃用页 → superseded_by 映射表 ──
dep_map = {}      # 弃用页 key(lower) -> (目标链接文本, 目标路径)
unresolved = []
skipped_keys = []
for p, fm in meta.items():
    if not is_dep(fm): continue
    keys = {os.path.basename(p)[:-3]}
    if fm.get("title"): keys.add(str(fm["title"]))
    for a in (fm.get("aliases") or []):
        if isinstance(a, str): keys.add(a)
    sup = fm.get("superseded_by") or fm.get("redirect_to")
    if not sup:
        unresolved.append((os.path.basename(p)[:-3], "无 superseded_by/redirect_to"))
        continue
    tgt_txt = strip_link(str(sup))
    tgt_path = resolve(tgt_txt)
    if not tgt_path:
        unresolved.append((os.path.basename(p)[:-3], "superseded_by 目标不存在: " + tgt_txt))
        continue
    if is_dep(meta.get(tgt_path, {})):
        unresolved.append((os.path.basename(p)[:-3], "superseded_by 目标自身是弃用页: " + tgt_txt))
        continue
    for k in keys:
        # ★ 只收「链接实际会解析到本弃用页」的 key。
        #   弃用页常把目标页名写进自己的 alias（当年为不断链），那些 key 会先命中目标页，不能改。
        if resolve(k) != p:
            continue
        if k in EXCLUDE:
            skipped_keys.append((k, tgt_txt))
            continue
        dep_map[k.lower()] = (tgt_txt, tgt_path)

print("scope = %s（目录 %d 个，%s）" % (scope, len(SCAN_DIRS), "全文扫描" if FULLTEXT else "仅 frontmatter"))
print("弃用页映射可用: %d 个 key / EXCLUDE 跳过: %d / 无法映射的弃用页: %d"
      % (len(dep_map), len(skipped_keys), len(unresolved)))
for n, why in unresolved:
    print("   !! %-24s %s" % (n, why))
if skipped_keys:
    print("   -- EXCLUDE 跳过的 key（语义不等价，不自动改）:")
    for k, t in sorted(skipped_keys):
        print("      %-16s (否则会改指到 %s)" % (k, t))

# ── 3. 扫描，收集待替换 ──
LINK = re.compile(r"\[\[([^\]\n]+?)\]\]")
plan = defaultdict(list)     # file -> [(old_link_text, new_link_text)]
cnt = Counter()
skipped = Counter()
anchor_dropped = Counter()
for top in SCAN_DIRS:
    base = os.path.join(ROOT, top)
    if not os.path.isdir(base): continue
    for r, d, fs in os.walk(base):
        if "node_modules" in r.split(os.sep):
            d[:] = []; continue
        for fn in fs:
            if not fn.endswith(".md"): continue
            p = os.path.join(r, fn)
            t = read(p)
            if t.startswith("---"):
                e = t.find("\n---", 3)
                if e == -1: continue
                zone = t[3:e] if not FULLTEXT else t
            else:
                if not FULLTEXT: continue
                zone = t
            for m in LINK.findall(zone):
                lt = m
                key = strip_link(lt).lower()
                if key not in dep_map: continue
                new_txt, _ = dep_map[key]
                # 保留原链接的显示文本；锚点一律丢弃（目标页无同名小节，保留会成死锚点）
                disp = lt.split("|", 1)[1] if "|" in lt else None
                anchor = "#" in (disp or lt)
                if anchor:
                    anchor_dropped[lt] += 1
                if disp:
                    disp = disp.split("#")[0]          # 去掉显示文本里的锚点残留
                    new_lt = new_txt + "|" + disp
                else:
                    new_lt = new_txt
                if new_lt == lt:
                    skipped["同文本"] += 1
                    continue
                plan[p].append((lt, new_lt))
                cnt[lt] += 1

total = sum(len(v) for v in plan.values())
print("\n待替换: %d 处 / 涉及文件 %d / 去重链接 %d" % (total, len(plan), len(cnt)))
if anchor_dropped:
    print("丢弃锚点 %d 处（目标页无同名小节，保留会成死锚点）:" % sum(anchor_dropped.values()))
    for k, v in anchor_dropped.most_common():
        print("   [[%s]] x%d" % (k, v))
print("Top15:")
for k, v in cnt.most_common(15):
    print("   %-24s x%-3d -> %s" % (k, v, dep_map[strip_link(k).lower()][0]))

if not APPLY:
    with open(".workbuddy/tmp/_r2c_files.txt", "w", encoding="utf-8") as f:
        for p in sorted(plan): f.write(p + "\n")
    print("\n[DRY-RUN] 未写入。文件清单 -> .workbuddy/tmp/_r2c_files.txt")
    sys.exit(0)

# ── 4. 快照 ──
files = sorted(plan)
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
zp = ".workbuddy/tmp/snap_r2c_%s_%s.zip" % (scope, ts)
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p, os.path.relpath(p, ROOT).replace(os.sep, "/"))
print("\n快照:", zp, "文件数:", len(files))

# ── 5. 执行：字面替换（qb 只在 frontmatter 区间，kb/all 全文）──
done, repl, skip = 0, 0, 0
for p in files:
    t = read(p)
    if t.startswith("---"):
        e = t.find("\n---", 3)
        fm_txt, body = t[3:e], t[e:]
    else:
        fm_txt, body = "", t
    if FULLTEXT:
        # 全文替换（frontmatter 与正文一起）
        new_t = t
        n = 0
        for old, new in set(plan[p]):
            o, w = "[[%s]]" % old, "[[%s]]" % new
            c = new_t.count(o)
            if c:
                new_t = new_t.replace(o, w); n += c
    else:
        new_fm = fm_txt
        n = 0
        for old, new in set(plan[p]):
            o, w = "[[%s]]" % old, "[[%s]]" % new
            c = new_fm.count(o)
            if c:
                new_fm = new_fm.replace(o, w); n += c
        new_t = "---" + new_fm + body
    if not n:
        skip += 1; continue
    if new_t.count("\n") != t.count("\n"):
        print("!! 行数异常跳过:", p); skip += 1; continue
    if new_t == t:
        skip += 1; continue
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(new_t)
    done += 1; repl += n

print("已写入 %d 文件 / 替换 %d 处 / 跳过 %d" % (done, repl, skip))
with open(".workbuddy/tmp/_r2c_files.txt", "w", encoding="utf-8") as f:
    for p in files: f.write(p + "\n")
