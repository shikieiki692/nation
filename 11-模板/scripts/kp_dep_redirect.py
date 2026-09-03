# -*- coding: utf-8 -*-
"""把题库里指向【弃用页】的 wikilink 改指其 superseded_by（已归位，原 .workbuddy/tmp/do_r2_c.py）。

   用法: python -X utf8 11-模板/scripts/kp_dep_redirect.py          预演（不写入）
         python -X utf8 11-模板/scripts/kp_dep_redirect.py --apply  写入

   安全策略:
     - 只为「目标 superseded_by 存在且指向活跃页」的弃用页建立映射，否则跳过并报告。
     - 只收「链接实际会解析到该弃用页」的 key：弃用页常把目标页名写进自己的 alias
       （当年为不断链），那些 key 会先命中目标页，不能改。
     - 解析分 basename_map / alias_map 两张表（文件名优先、alias 兜底），不可合成一张。
     - 字面替换，不 YAML 回写；frontmatter 行数不变才落盘。
   已知常态: 并行导入器沿用弃用页名（配位化合物/理想气体状态方程/等电子体原理）会周期性回涨，
             重跑本脚本即可清理；根治需改导入规范用活跃页名（配合物/理想气体/等电子体）。
"""
import os, re, sys, yaml, zipfile, datetime
from collections import Counter, defaultdict

ROOT = "C:/Obsidion/妙妙屋"
KP = os.path.join(ROOT, "03-知识点")
APPLY = "--apply" in sys.argv
QB = [os.path.join(ROOT, "04-题库"), os.path.join(ROOT, "05-真题库")]
FIELDS = ["knowledge_points", "depends_on", "cross_references", "related", "superseded_by"]
DEP_STATUS = ("deprecated", "已废弃", "已合并", "重定向")

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
        dep_map[k.lower()] = (tgt_txt, tgt_path)

print("弃用页映射可用: %d 个 key / 无法映射的弃用页: %d" % (len(dep_map), len(unresolved)))
for n, why in unresolved:
    print("   !! %-24s %s" % (n, why))

# ── 3. 扫描题库，收集待替换 ──
plan = defaultdict(list)     # file -> [(old_link_text, new_link_text)]
cnt = Counter()
skipped = Counter()
for qdir in QB:
    for r, d, fs in os.walk(qdir):
        for fn in fs:
            if not fn.endswith(".md"): continue
            p = os.path.join(r, fn)
            t = read(p)
            if not t.startswith("---"): continue
            e = t.find("\n---", 3)
            if e == -1: continue
            fm_txt = t[3:e]
            for m in re.findall(r"\[\[([^\]\n]+?)\]\]", fm_txt):
                lt = m
                key = strip_link(lt).lower()
                if key not in dep_map: continue
                new_txt, _ = dep_map[key]
                # 保留原链接的显示文本与锚点
                if "|" in lt:
                    disp = lt.split("|", 1)[1]
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
print("Top10:")
for k, v in cnt.most_common(10):
    print("   %-24s x%-3d -> %s" % (k, v, dep_map[strip_link(k).lower()][0]))

if not APPLY:
    with open(".workbuddy/tmp/_r2c_files.txt", "w", encoding="utf-8") as f:
        for p in sorted(plan): f.write(p + "\n")
    print("\n[DRY-RUN] 未写入。文件清单 -> .workbuddy/tmp/_r2c_files.txt")
    sys.exit(0)

# ── 4. 快照 ──
files = sorted(plan)
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
zp = ".workbuddy/tmp/snap_r2c_%s.zip" % ts
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p, os.path.relpath(p, ROOT).replace(os.sep, "/"))
print("\n快照:", zp, "文件数:", len(files))

# ── 5. 执行：只在 frontmatter 区间内做字面替换 ──
done, repl, skip = 0, 0, 0
for p in files:
    t = read(p)
    e = t.find("\n---", 3)
    fm_txt, body = t[3:e], t[e:]
    new_fm = fm_txt
    n = 0
    for old, new in set(plan[p]):
        o, w = "[[%s]]" % old, "[[%s]]" % new
        c = new_fm.count(o)
        if c:
            new_fm = new_fm.replace(o, w); n += c
    if not n:
        skip += 1; continue
    new_t = "---" + new_fm + body
    if new_fm.count("\n") != fm_txt.count("\n") or new_t.count("\n") != t.count("\n"):
        print("!! 行数异常跳过:", p); skip += 1; continue
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(new_t)
    done += 1; repl += n

print("已写入 %d 文件 / 替换 %d 处 / 跳过 %d" % (done, repl, skip))
with open(".workbuddy/tmp/_r2c_files.txt", "w", encoding="utf-8") as f:
    for p in files: f.write(p + "\n")
