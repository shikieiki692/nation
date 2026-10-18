# -*- coding: utf-8 -*-
"""F 判据 v5：三分法（缺陷 / 教材图号引用 / 噪声），并区分题面区与答案区。

v4 → v5 变更：
  1. 答案区分隔新增 `**解**：`/`**解：`/`^解：`（例题卡把解答写在 `## 参考答案` 之前）；
  2. EXT（引用书图号，如《结构化学基础》图4.3.7(b)）不再计入缺陷，单列「教材图号引用」；
  3. 非题卡（元文件／清单／任务页／答案子目录）单列「噪声」；
  4. H1 标题行不计入扫描（标题＝题面首句截断），但若正文无命中则标「仅标题」供人判。
"""
import io, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
OUT = os.path.join(ROOT, ".workbuddy", "tmp", "_fig_v5.txt")

REF = re.compile(r"(下图|右图|左图|上[图左]|如[上左下右]图|如下[上左下右]*图|见[上左下右]图|见图|如图)")
NUM = re.compile(r"(?<![画绘])图\s*\d")
EXT = re.compile(r"[《【\[（(][^》】\]）)]{0,30}[》】\]）)]\s*图\s*\d|图\s*\d+\.\d+")
EMB = re.compile(r"!\[\[")
MD = re.compile(r"!\[[^\]]*\]\(images/")
ANS = [r"^## 参考答案", r"^## 答案与解析", r"^## 答案", r"^## 解答", r"^## 解析",
       r"^\*\*参考答案\*\*", r"^\*\*解答\*\*", r"^\*\*答案[:：]", r"^\*\*解[:：]", r"^\*\*解\*\*", r"^解[:：]"]
SKIP = {"images", ".git", "_归档", "_archive"}


def split_fm(t):
    if t.startswith("---"):
        i = t.find("\n---", 3)
        if i > 0:
            return t[: i + 4], t[i + 4:]
    return "", t


def split_front(body):
    best = len(body)
    for pat in ANS:
        m = re.search(pat, body, re.M)
        if m and 0 <= m.start() < best:
            best = m.start()
    return body[:best], body[best:]


def is_noise(rel, base):
    if base in ("README.md", "索引.md"):
        return "索引/README"
    if "/元文件/" in rel or "任务.md" in base or "清单.md" in base:
        return "任务页/清单"
    if "/答案/" in rel or base.endswith("-答案.md"):
        return "答案子目录"
    return ""


def scan_line(ln):
    return bool(REF.search(ln)) or bool(NUM.search(ln))


def mask_ext(ln):
    """把「书图号」区间抹掉，避免 `图4.3.7(b)` 里的「图4」被误当 REF 引用。"""
    return EXT.sub("《图号》", ln)


def scan_ref(ln):
    """去掉书图号后，是否仍存在题面内提图（真缺陷判据）。"""
    m = mask_ext(ln)
    return bool(REF.search(m)) or bool(NUM.search(m))


rows = []
for dp, dn, fn in os.walk(os.path.join(ROOT, "04-题库")):
    dn[:] = [d for d in dn if d not in SKIP]
    for f in fn:
        if not f.endswith(".md") or f.startswith("初赛模拟卷"):
            continue
        p = os.path.join(dp, f)
        try:
            t = io.open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
        except Exception:
            continue
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        fm, body = split_fm(t)
        front, an = split_front(body)
        # 题面区无任何图嵌入
        if EMB.search(front) or MD.search(front):
            continue
        # 跳过 H1 标题行
        body_lines = [l for l in front.split("\n") if not l.startswith("# ")]
        hit_ln = [l for l in body_lines if scan_ref(l)]
        hit_ext = [l for l in body_lines if EXT.search(l) and not scan_ref(l)]
        only_title = (not hit_ln) and any(scan_ref(l) for l in front.split("\n") if l.startswith("# "))
        if not hit_ln and not hit_ext and not only_title:
            continue
        # 分类
        if hit_ln:
            nz = is_noise(rel, f)
            cat = ("噪声·" + nz) if nz else ("结构畸形合集" if "Weller/Ch21" in rel else "缺陷·题面提图无图")
        elif only_title:
            cat = "仅标题命中（人判）"
        else:
            cat = "教材图号引用（非缺陷）"
        marked = ("题面缺图" in t) or ("组卷隔离" in t) or ("缺图" in t)
        snip = (hit_ln[0].strip() if hit_ln else "(仅标题)")[:150]
        rows.append((rel, cat, "True" if marked else "False", snip))


cnt = collections.Counter(r[1] for r in rows)
print("命中 %d 条" % len(rows))
for k, v in cnt.most_common():
    print("   %-24s %d" % (k, v))
un = [r for r in rows if r[2] == "False"]
print("\n未自标 %d 条" % len(un))
cu = collections.Counter(r[1] for r in un)
for k, v in cu.most_common():
    print("   %-24s %d" % (k, v))
with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    for rel, cat, mk, snip in sorted(rows):
        fh.write("%s\t%s\t%s\t%s\n" % (rel, cat, mk, snip))
print("\n明细 →", OUT)
