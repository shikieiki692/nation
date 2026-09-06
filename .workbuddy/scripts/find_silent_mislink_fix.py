"""为 11 个「静默吸题」的概念词寻找正确的知识点文件：
   在 03-知识点/04-专题与题型 里按 文件名/title/aliases 找候选，排除题目类。
"""
import os, sys, re, json

VAULT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(VAULT, "11-模板", "scripts"))
import validate_kb as V

TERMS = ["羟醛缩合", "配合物颜色", "克劳修斯-克拉佩龙方程", "酰氯", "双缩脲反应",
         "固体电解质", "氮化物结构", "硼氢化氧化", "亲电性", "内酰胺", "不饱和度"]

# 建立 03-知识点 / 04-专题与题型 的 name+title+aliases 索引
SCAN = [os.path.join(VAULT, d) for d in ["03-知识点", "04-专题与题型"]]
entries = []  # (kind, value, relpath)
FM = re.compile(r"^---\s*\n(.*?)\n---", re.S)


def fmget(fm, key):
    m = re.search(rf"^{key}:\s*(.+?)\s*$", fm, re.M)
    return m.group(1).strip() if m else None


for root in SCAN:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, VAULT).replace("\\", "/")
            raw = open(p, encoding="utf-8", errors="ignore").read()
            m = FM.match(raw)
            if not m:
                continue
            fm = m.group(1)
            ty = fmget(fm, "type") or ""
            if ty in V.QB_TYPES:
                continue  # 排除题目类
            entries.append(("name", f[:-3], rel, ty))
            t = fmget(fm, "title")
            if t:
                entries.append(("title", t.strip("\"'"), rel, ty))
            am = re.search(r"^aliases:\s*\n((?:[ \t]+-.*\n)+)", fm, re.M)
            if am:
                for line in am.group(1).splitlines():
                    a = line.strip().lstrip("- ").strip().strip("\"'")
                    if a:
                        entries.append(("alias", a, rel, ty))
            am2 = fmget(fm, "aliases")
            if am2 and am2.startswith("["):
                for a in am2.strip("[]").split(","):
                    a = a.strip().strip("\"'")
                    if a:
                        entries.append(("alias", a, rel, ty))

print(f"索引条目（非题目类，03-知识点 + 04-专题与题型）：{len(entries)}\n")

for t in TERMS:
    low = t.lower()
    hits = []
    for kind, val, rel, ty in entries:
        v = val.lower()
        if v == low or low in v or v in low:
            hits.append((kind, val, rel, ty))
    # 去重按 rel
    seen, uniq = set(), []
    for h in hits:
        if h[2] not in seen:
            seen.add(h[2])
            uniq.append(h)
    exact = [h for h in uniq if h[1].lower() == low]
    print(f"### [[{t}]]")
    cur = V.find_wikilink_target(t, V.VAULT_ROOT)
    print(f"    当前解析 → {cur.relative_to(V.VAULT_ROOT).as_posix() if cur else '—'}")
    if exact:
        print(f"    ✅ 精确同名（可直接改指）：")
        for k, v, r, ty in exact:
            print(f"        {r}  (type={ty}, 匹配方式={k})")
    if uniq:
        print(f"    候选 {len(uniq)} 个：")
        for k, v, r, ty in uniq[:8]:
            print(f"        [{k}] {v}  →  {r}  (type={ty})")
        if len(uniq) > 8:
            print(f"        … 另 {len(uniq)-8} 个")
    else:
        print("    （无候选 → 只能靠移除题目文件 alias 才能变红链）")
    print()
