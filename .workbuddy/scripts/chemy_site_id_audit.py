# -*- coding: utf-8 -*-
r"""Chemy 站点 id 校核器（常驻）—— 卡内站点 id 是否「全站最优匹配」。

用法（无需第三方库）：
    python chemy_site_id_audit.py --all                # 全量校核
    python chemy_site_id_audit.py --all --strict       # 非白名单异常 ⇒ 退出码 1
    python chemy_site_id_audit.py --all --report       # 落 CSV 明细
    python chemy_site_id_audit.py --all --top 20       # 多列前 N 名（调试）

数据源（**只读参照**，gitignore）：`.workbuddy/tmp/chemy_site/questions.json`（站点 1,933 题）。
卡来源：`04-题库/2026机构初赛模拟题/chemy/` 正文 `> 来源：Chemy- 项目（…）\`chemy⟨届⟩-⟨套⟩-⟨题⟩\``。

═══ 判据（**主判据＝全站 rank-1**）═══
· **必须全站排名**：套内 rank-1 **抓不到套级偏移**（实测 `CM-162-09` 声称 `38-11-3`、
  真属 `38-10-9`，套内排名完全看不见）。
· **纯 n-gram 计数会被「长题」刷分** ⇒ 得分只作**筛查**；真值看三样证据：
  ① 卡首段与站点正文**逐字吻合**；② 特征串**全站唯一命中**；③ 卡标题 ≡ 站点 `title`。
  工具对每个非 rank-1 项输出**证据行**（卡首段 vs 声称/最优题 body）供目检。
· **双方分数都低（<0.5）时不可据以改号**——站点侧正文稀薄/以图为主即可致低分（实测 D 类 3 张）。

白名单：`.workbuddy/scripts/siteid_keep.json`  `{"<卡文件名>": "原因"}`
"""
import io, json, os, re, sys, time, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
CARD_DIR = "04-题库/2026机构初赛模拟题/chemy"
QJSON = ".workbuddy/tmp/chemy_site/questions.json"
KEEP = ".workbuddy/scripts/siteid_keep.json"
N = 6

TAG = re.compile(r"<[^>]+>")
LATEX = re.compile(r"\\[a-zA-Z]+\*?|\$|\{|\}|_|\^|\\[\[\]()]")
SRC = re.compile(r"来源：Chemy- 项目（[^）]*）\s*`([^`]+)`")
H1 = re.compile(r"^#\s+(.+)$", re.M)


def norm(s):
    return re.sub(r"[^\u3400-\u9fffA-Za-z0-9]+", "", LATEX.sub(" ", TAG.sub(" ", s))).lower()


def grams(s):
    return {s[i:i + N] for i in range(len(s) - N + 1)}


def card_stem(t):
    i = t.find("## 题目")
    if i < 0:
        return ""
    j = t.find("## 参考答案", i)
    return t[i:j if j > 0 else len(t)]


def probe(stem):
    """提「卡首段」特征串：跳过标题/图/表/公式行（站点 body 无标题行 ⇒ 否则永远匹配不上）。"""
    for ln in stem.split("\n"):
        p = ln.strip()
        if not p or p[0] in "#!|$":
            continue
        if p.startswith(">") or p.startswith("<"):
            continue
        q = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]+", "", p)
        if len(q) >= 12:
            return q[:18]
    return ""


def main():
    argv = sys.argv[1:]
    ALL = "--all" in argv
    STRICT = "--strict" in argv
    REPORT = "--report" in argv
    TOP = 1
    if "--top" in argv:
        TOP = int(argv[argv.index("--top") + 1])
    if not ALL:
        print(__doc__)
        print("!! 需 --all"); return 2
    if not os.path.isfile(QJSON):
        print("!! 缺站点数据（只读参照，gitignore，需先抓取）：", QJSON); return 2
    keep = {}
    if os.path.isfile(KEEP):
        keep = json.load(io.open(KEEP, encoding="utf-8"))

    t0 = time.time()
    Q = json.load(io.open(QJSON, encoding="utf-8"))
    SITE = {x["id"]: x for x in Q}
    INV, LEN = collections.defaultdict(set), {}
    for x in Q:
        g = grams(norm(x.get("body", "") + " " + x.get("answer", "")))
        LEN[x["id"]] = len(g)
        for t in g:
            INV[t].add(x["id"])
    print("站点 %d 条 ｜ 词项 %d ｜ 索引 %.1fs" % (len(Q), len(INV), time.time() - t0))

    rows, no_id, missing = [], 0, []
    for fn in sorted(os.listdir(CARD_DIR)):
        if not fn.startswith("题-") or not fn.endswith(".md"):
            continue
        t = io.open(os.path.join(CARD_DIR, fn), encoding="utf-8-sig").read()
        m = SRC.search(t)
        if not m:
            no_id += 1
            continue
        sid = m.group(1).strip()
        stem = card_stem(t)
        g = grams(norm(stem))
        if sid not in SITE:
            missing.append((fn, sid)); continue
        if not g:
            missing.append((fn, sid + "(空题面)")); continue
        cnt = collections.Counter()
        for tk in g:
            for cid in INV.get(tk, ()):
                cnt[cid] += 1
        sc = lambda cid: cnt.get(cid, 0) / len(g)
        ranked = sorted(cnt.items(), key=lambda kv: (-kv[1] / len(g), kv[0]))
        best = ranked[0][0] if ranked else None
        rank = 1 + sum(1 for c in cnt if sc(c) > sc(sid) + 1e-9)
        rows.append({"卡文件": fn, "站点id": sid, "声称分": round(sc(sid), 3),
                     "全站最优": best, "最优分": round(sc(best), 3) if best else 0.0,
                     "排名": rank, "题面gram": len(g), "首段": probe(stem),
                     "site_title": SITE[sid].get("title", ""), "top": ranked[:TOP]})

    ok = [r for r in rows if r["排名"] == 1]
    bad = [r for r in rows if r["排名"] != 1]
    bad_nw = [r for r in bad if r["卡文件"] not in keep]
    print("=" * 86)
    print("受检 %d 张（带来源行）｜ **全站 rank-1: %d** ｜ 非 rank-1: %d（其中白名单 %d，**待核 %d**）"
          % (len(rows), len(ok), len(bad), len(bad) - len(bad_nw), len(bad_nw)))
    print("无站点 id 来源行: %d（B 类等，正常）｜ id 不在站点: %d" % (no_id, len(missing)))
    print("-" * 86)
    for r in bad_nw:
        print("  ⚠️ %-44s 声称 %-14s %.3f ｜ 最优 %-14s %.3f ｜ #%d"
              % (r["卡文件"][:42], r["站点id"], r["声称分"], r["全站最优"], r["最优分"], r["排名"]))
        if r["首段"]:
            st = SITE.get(r["全站最优"], {})
            print("       首段 %r ｜ 声称题 body 含: %s ｜ 最优题 body 含: %s"
                  % (r["首段"], r["首段"] in norm(SITE[r["站点id"]].get("body", "")),
                     r["首段"] in norm(st.get("body", ""))))
    for fn, sid in missing[:10]:
        print("  ❓ id 不在站点: %-40s %s" % (fn[:38], sid))
    if REPORT:
        out = ".workbuddy/tmp/chemy_site_id_audit.csv"
        import csv
        with io.open(out, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["卡文件", "站点id", "声称分", "全站最优", "最优分", "排名", "题面gram", "首段", "site_title"], extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print("明细 CSV →", out)
    print("-" * 86)
    print("VERDICT: %s" % ("PASS" if not bad_nw else "WARN（逐项目检：卡首段/唯一命中/标题三判据）"))
    return 1 if (STRICT and bad_nw) else 0


if __name__ == "__main__":
    sys.exit(main())
