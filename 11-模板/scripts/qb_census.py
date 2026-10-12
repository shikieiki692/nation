# -*- coding: utf-8 -*-
"""题库字段普查：按 subject_module / source_category / 来源 / teaching_level / used_in 聚合。只读。

⚠️ 2026-10-12 修复（关键）：原 `parse_fm` 有 `if line[0] in " \t-": continue`
   —— **跳过所有续行**，于是 YAML **块列表/多行数组**（`knowledge_points:` + `- "[[金]]"`）
   一律被读成**空字符串**。后果：`qb_census.json` 的列表字段（KP/syllabus/question_type/
   used_in/…)系统性失真，实测 KP 非空被低报为 43%（真值 94.8%）；
   且 `gen_r1.reuse_tier()` 依赖 `used_in` 字符串 ⇒ **把已用题全判成「未用」**。
   现改为「续行并入上一个键」（保持**字符串**类型，与既有消费者兼容）。
   ⚠️ 结构化访问请用 `11-模板/scripts/fm_parse.py::get_list_field`（唯一口径）。
"""
import os, re, json, collections, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SCOPES = [os.path.join(ROOT, "04-题库"), os.path.join(ROOT, "05-真题库")]
SKIP_DIRS = {"元文件"}

FM = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.S)
KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):[ \t]*(.*)$")


def parse_fm(text):
    m = FM.match(text)
    if not m:
        return None
    d = {}
    cur = None
    for line in m.group(1).splitlines():
        if not line.strip():
            cur = None                      # 空行 ⇒ 结束当前块
            continue
        if line[0] in " \t-":               # 续行：块列表 / 跨行数组
            if cur is not None:
                s = line.strip()
                if s.startswith("- "):
                    s = s[2:]
                elif s.startswith("-"):
                    s = s[1:].strip()
                d[cur] = (d[cur] + " " + s).strip() if d.get(cur) else s
            continue
        km = KEY.match(line)
        if km:
            cur = km.group(1)
            d[cur] = km.group(2).strip()
        else:
            cur = None
    return d


recs = []
for scope in SCOPES:
    for dp, dns, fns in os.walk(scope):
        if any(s in dp.split(os.sep) for s in SKIP_DIRS):
            continue
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dp, fn)
            try:
                with open(p, encoding="utf-8", errors="replace") as f:
                    txt = f.read(20000)
            except Exception:
                continue
            fm = parse_fm(txt)
            if not fm:
                continue
            t = fm.get("type", "")
            if t not in ("题目", "真题"):
                continue
            fm["_path"] = os.path.relpath(p, ROOT).replace("\\", "/")
            fm["_bucket"] = os.path.relpath(p, ROOT).replace("\\", "/").split("/")[1]
            fm["_sub"] = "/".join(os.path.relpath(p, ROOT).replace("\\", "/").split("/")[1:3])
            recs.append(fm)


def cnt(key):
    return collections.Counter(r.get(key, "(缺)") for r in recs)


def show(title, c, limit=40):
    print(f"\n### {title}  [总 {sum(c.values())}]")
    for k, v in c.most_common(limit):
        print(f"  {v:5d}  {k}")


print(f"题目/真题 文件总数: {len(recs)}")
show("按一级目录", cnt("_bucket"))
show("subject_module × teaching_level", collections.Counter(
    (r.get("subject_module", "?"), r.get("teaching_level", "?")) for r in recs), 40)
show("source_category", cnt("source_category"))
show("source_grade", cnt("source_grade"))
show("pack", cnt("pack"))
show("exam_stage", cnt("exam_stage"))

used = sum(1 for r in recs if r.get("used_in") and r["used_in"] not in ("", "[]"))
print(f"\nused_in 非空: {used} / {len(recs)}")
kp = sum(1 for r in recs if r.get("knowledge_points") and r["knowledge_points"] not in ("", "[]"))
print(f"knowledge_points 非空: {kp} / {len(recs)}")

srcs = collections.Counter(re.sub(r'^["\']|["\']$', "", r.get("source", "(缺)"))[:46] for r in recs)
show("来源 TOP60", srcs, 60)

print("\n### 教材习题 子目录 × teaching_level")
sub = collections.defaultdict(collections.Counter)
for r in recs:
    parts = r["_path"].split("/")
    if len(parts) > 2 and parts[1] == "教材习题":
        sub[parts[2]][r.get("teaching_level", "?")] += 1
for k in sorted(sub, key=lambda x: -sum(sub[x].values())):
    c = sub[k]
    print(f"  {sum(c.values()):5d}  {k:34s} 基础{c.get('基础',0)} 巩固{c.get('巩固',0)} 拓展{c.get('拓展',0)} 竞赛{c.get('竞赛',0)}")

print("\n### 未用题（组卷池）")
un = [r for r in recs if not (r.get("used_in") and r["used_in"] not in ("", "[]"))]
print(f"未用题总数: {len(un)}")
c = collections.Counter((r.get("source_category", "?"), r.get("teaching_level", "?")) for r in un)
for k, v in sorted(c.items(), key=lambda x: -x[1])[:40]:
    print(f"  {v:5d}  {k[0]} | {k[1]}")

json.dump(recs, open(os.path.join(ROOT, ".workbuddy/tmp/qb_census.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("\n[dump] .workbuddy/tmp/qb_census.json")
