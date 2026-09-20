# -*- coding: utf-8 -*-
"""第一轮·综合套卷：把专题池**打散重组**为 12 套 × 30 题（横跨结构化学＋化学原理）。

    python gen_r1_mixed.py            # dry-run
    python gen_r1_mixed.py --write    # 落盘

配比（每套 30 题）：
  学科：结构化学 15 ＋ 化学原理 15
  题源层 × 难度（联合配额，保证「混合」不偏科）：
    真题      基础1 进阶4 挑战1 = 6
    竞赛题集  基础3 进阶7 挑战2 = 12
    竞赛教程  基础1 进阶4 挑战1 = 6
    竞赛教材  基础1 进阶1 挑战4 = 6
  → 难度合计 基础6 / 进阶16 / 挑战8；题源合计 真6/集12/程6/教6
格式：去 ⭐ 与【题源层】标签，来源用书目级简称；学生版无来源行/难度标记（成品规则④）。
"""
import io
import os
import re
import sys
import json
import collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"C:\Obsidion\妙妙屋"
WRITE = "--write" in sys.argv
OUTDIR = os.path.join(ROOT, "04-课件", "习题集", "三·竞赛导向层（载体Ⅱ·Ⅲ）", "第一轮·综合套卷")

src = io.open(".workbuddy/scripts/gen_r1.py", encoding="utf-8").read().replace("\nmain()\n", "\n")
G = {"__name__": "gen_r1_lib"}
exec(compile(src, "gen_r1.py", "exec"), G)
route, prio, load = G["route"], G["prio"], G["load"]
band, is_choice, reuse_tier = G["band"], G["is_choice_ans"], G["reuse_tier"]
norm_images, resolve_img, shortsrc = G["norm_images"], G["resolve_img"], G["shortsrc"]
imgs_ok = G["imgs_ok"]
clean_used = G["clean_used"]    # 2026-09-18：与竞赛教材版共用「曾用于」清理（剥库内路径/去重）
_strip_mineru_div = G["_strip_mineru_div"]   # 2026-09-20：剥 MinerU OCR 的 div 包裹（致公式不渲染）
gate_v2 = G["gate_v2"]          # 2026-09-18：与竞赛教材版共用「卷面质量闸门 v2」
T, ORDER, TIERNAME = G["T"], G["ORDER"], G["TIERNAME"]
DISCIPLINE, TODAY, IMG, ZUTI = G["DISCIPLINE"], G["TODAY"], G["IMG"], G["ZUTI"]

N_PAPER = 12
STRUCT_Q = {"S1": 2, "S2": 1, "S3": 4, "S4": 4, "S5": 4}                    # = 15
CHEM_Q = {"P1": 2, "P2": 1, "P3": 3, "P4": 2, "P5": 1, "P6": 2, "P7": 1, "P8": 1, "P9": 2}  # = 15
# 2026-09-17 简化：**只保留两条规则** —— 学科（结构 15＋原理 15）与难度（基础6/进阶16/挑战8）。
# 题源层不再设配额，只按用户质量序（真题→题集→教程→讲义→自编）自然取；真不足时按序降级。
BAND_T = {2: 6, 3: 16, 4: 8}
# 平行卷要可比：给「真题」设一个**每卷上限**（1 个数，不是网格）。不加的话卷01 会吃 22 道真题、
# 卷09 一道没有 —— 难度与来源都不可比。6/30 = 20%。
MAX_ZHENTI = 6
assert sum(STRUCT_Q.values()) == 15 and sum(CHEM_Q.values()) == 15
assert sum(BAND_T.values()) == 30

# ── 建池 ──────────────────────────────────────────────────────────────
recs = json.load(io.open(".workbuddy/tmp/qb_census.json", encoding="utf-8"))
avail = collections.defaultdict(list)     # (topic, tier, band) -> [cand]
for r in recs:
    if r.get("status") == "deprecated" or r.get("type") == "题组":
        continue
    if ZUTI.match(os.path.basename(r["_path"])):
        continue
    if prio(r) >= 99:
        continue
    # 2026-09-18 第二轮补：与「竞赛教材版」共用同一份 `EXCLUDE_PATHS` 真缺陷黑名单。
    #   本脚本此前**漏了这道过滤** → 上轮 4 题有 2 道（汇智-晶体结构-5/51）已进现役套卷，
    #   构成真实交付物缺陷。判定层与 `prio(r) >= 99` 同层（都在 `route()` 之前）。
    if r["_path"].replace(os.sep, "/") in G["EXCLUDE_PATHS"]:
        continue
    tk = route(r)
    if not tk:
        continue
    got = load(os.path.join(ROOT, r["_path"].replace("/", os.sep)))
    if not got:
        continue
    fm, q, a = got
    # 2026-09-18：旧口径 `len(q) < 40`（纯长度门槛）→ 升级为**结构质量门槛 v2**
    #   （与「第一轮·竞赛教材版」共用 `gate_v2`）：拒 H1 派生描述短语、纯指针、
    #   极短指示词+清单缺失、答案过短、题干过长。起因＝用户反馈套卷含无关信息。
    _rej = collections.Counter()
    if not gate_v2(r, fm, q, a, _rej):
        continue
    if (fm.get("answer_status") or "").strip() in ("源书无解", "待补"):
        continue
    if not imgs_ok(q, a):          # 图必须在媒体仓库或仓库根（保 Word 管线）
        continue
    for k in ([tk] if isinstance(tk, str) else tk):
        avail[(k, prio(r), band(r.get("difficulty")))].append(
            {"pp": prio(r), "tier": prio(r), "band": band(r.get("difficulty")),
             "r": r, "q": norm_images(q, r.get("_path")), "ans": norm_images(a, r.get("_path")), "topic": k})
for key in avail:
    avail[key].sort(key=lambda c: (reuse_tier(c["r"]), c["r"]["_path"]))

pool_sz = collections.Counter()
for (k, t, b), v in avail.items():
    pool_sz[k] += len(v)
print("可组池 %d 题；逐专题 %s" % (sum(pool_sz.values()),
      " ".join("%s:%d" % (k, pool_sz[k]) for k in ORDER)))


used_paths = set()
# 与「第一轮·竞赛教材版」专题卷**互斥**：专题卷先出，套卷只从剩下的题里选，
# 避免同一道题同时出现在跟课卷与综合套卷（学生重复做题）。
_zj = os.path.join(ROOT, "04-课件", "习题集", "三·竞赛导向层（载体Ⅱ·Ⅲ）", "第一轮·竞赛教材版", "_选题清单.json")
if os.path.exists(_zj):
    for m in json.load(io.open(_zj, encoding="utf-8")):
        used_paths.update(m["paths"])
    print("已避开专题卷已用题 %d 道" % len(used_paths))


def take(topic, tier, bd):
    lst = avail.get((topic, tier, bd))
    if not lst:
        return None
    # ⚠️ 同一道题可能被 route() 映射到多个主题（MULTI），故必须按 path 全局去重
    while lst and lst[0]["r"]["_path"] in used_paths:
        lst.pop(0)
    if not lst:
        return None
    c = lst.pop(0)
    return c


def take_band(topic, bd, zhenti_left=None):
    """按用户质量序（真题→题集→教程→讲义→自编）取该专题该难度的一题。

    `zhenti_left`：本卷还剩几道真题额度；为 0 时跳过 tier 0（平行卷可比）。
    """
    tiers = (0, 1, 2, 3, 4) if (zhenti_left is None or zhenti_left > 0) else (1, 2, 3, 4)
    for t in tiers:
        c = take(topic, t, bd)
        if c:
            return c
    return None


def take_any(topic, zhenti_left=None):
    for b in (2, 3, 4):
        c = take_band(topic, b, zhenti_left)
        if c:
            return c
    return None


papers, log = [], []
for pi in range(1, N_PAPER + 1):
    quota = dict(CHEM_Q)
    quota.update(STRUCT_Q)
    assert sum(quota.values()) == 30, sum(quota.values())
    sel, fallback = [], 0
    zt_left = MAX_ZHENTI
    # Pass 1：按难度目标填（跨专题，谁池子大先取谁）
    for bd, need in BAND_T.items():
        while need > 0:
            cands = [k for k in quota if quota[k] > 0 and any(avail.get((k, t, bd)) for t in (0, 1, 2, 3, 4))]
            if not cands:
                break
            k = max(cands, key=lambda x: (sum(len(avail.get((x, t, bd), [])) for t in (0, 1, 2, 3, 4)),
                                          quota[x], -ORDER.index(x)))
            c = take_band(k, bd, zt_left)
            if c is None:
                break
            if c["tier"] == 0:
                zt_left -= 1
            quota[k] -= 1
            sel.append(c)
            need -= 1
    # Pass 2：余下配额用任意难度补
    while len(sel) < 30 and any(v > 0 for v in quota.values()):
        cands = [k for k in quota if quota[k] > 0]
        k = max(cands, key=lambda x: (pool_sz[x], quota[x], -ORDER.index(x)))
        c = take_any(k, zt_left)
        if c is None:
            quota[k] = 0
            continue
        if c["tier"] == 0:
            zt_left -= 1
        quota[k] -= 1
        sel.append(c)
        fallback += 1
    # 按**难度阶梯**排（易→难），学科与题源层只作次级序 → 总览表的「基础 1–6 / 进阶 7–22 / 挑战 23–30」才是连续区间
    sel.sort(key=lambda c: (c["band"], 0 if c["topic"].startswith("S") else 1,
                            c["tier"], ORDER.index(c["topic"])))
    dupe = [c for c in sel if c["r"]["_path"] in used_paths]
    assert not dupe, "跨卷重复 %d 条" % len(dupe)
    used_paths |= {c["r"]["_path"] for c in sel}
    papers.append(sel)
    ti = collections.Counter(c["tier"] for c in sel)
    ba = collections.Counter(c["band"] for c in sel)
    tp = collections.Counter(c["topic"] for c in sel)
    log.append((pi, len(sel), dict(ti), dict(ba), dict(tp), fallback))

print()
print("=== 12 套构成（tier: 0真 1集 2程 3教）===")
for pi, n, ti, ba, tp, fb in log:
    print("  综合卷%02d  %2d 题  真%d/集%d/程%d/教%d  基础%d/进阶%d/挑战%d  结构%d+原理%d  兜底%d" % (
        pi, n, ti.get(0, 0), ti.get(1, 0), ti.get(2, 0), ti.get(3, 0),
        ba.get(2, 0), ba.get(3, 0), ba.get(4, 0),
        sum(v for k, v in tp.items() if k.startswith("S")),
        sum(v for k, v in tp.items() if k.startswith("P")), fb))

if not WRITE:
    print("\n（dry-run）")
    sys.exit(0)

# ── 写出 ──────────────────────────────────────────────────────────────
os.makedirs(OUTDIR, exist_ok=True)
manifest, missing = [], []
for pi, sel in enumerate(papers, 1):
    bd = collections.Counter(c["band"] for c in sel)
    ti = collections.Counter(c["tier"] for c in sel)
    imgs = sorted({i for c in sel for i in IMG.findall(c["q"]) + IMG.findall(c["ans"])})
    for im in imgs:
        if not resolve_img(im):
            missing.append(("综合卷%02d" % pi, im))
    for edition, with_ans in (("教师版", True), ("学生版", False)):
        L = ["---",
             'title: "第一轮综合练习 第%02d卷（%s）"' % (pi, edition),
             "type: 题组", "role: 习题集", "round: 第一轮",
             "pack: 综合模拟卷",
             "question_count: " + str(len(sel)),
             "difficulty_range: " + str(min(c["band"] for c in sel)) + "-" + str(max(c["band"] for c in sel)),
             "source_category: 竞赛导向·竞赛教材", "status: 已填充",
             "created: " + TODAY, "updated: " + TODAY,
             "tags: [化竞, 第一轮, 综合套卷, " + str(pi) + "]", "---", "",
             "# 第一轮综合练习 · 第%02d卷" % pi, ""]
        if with_ans:
            L += [DISCIPLINE,
                  "> **构成**：共 " + str(len(sel)) + " 题（结构化学 " +
                  str(sum(1 for c in sel if c["topic"].startswith("S"))) + " ＋ 化学原理 " +
                  str(sum(1 for c in sel if c["topic"].startswith("P"))) + "）；" +
                  "基础 " + str(bd.get(2, 0)) + " ＋ 进阶 " + str(bd.get(3, 0)) +
                  " ＋ 挑战 " + str(bd.get(4, 0)) + "。",
                  "> **学生版**同题号同序，可直接印发。", "",
                  "## 难度总览", "", "| 难度 | 题号 | 题数 |", "|:---|:---|:---:|"]
            for lab, b_ in (("基础", 2), ("进阶", 3), ("挑战", 4)):
                idx = [i + 1 for i, c in enumerate(sel) if c["band"] == b_]
                if idx:
                    L.append("| " + lab + " | " + str(idx[0]) + "–" + str(idx[-1]) + " | " + str(len(idx)) + " |")
        else:
            L += ["> 共 " + str(len(sel)) + " 题。建议先独立完成，再核对答案。"]
        L += ["", "---", "", "## 题目", ""]
        for i, c in enumerate(sel, 1):
            L += ["### 第" + str(i) + "题", ""]
            if with_ans:
                L.append("> 来源：" + shortsrc(c["r"]))
                # 2026-09-18：删除「> 曾用于：…」行（用户拍板「整行全删」）。
                # 理由同 gen_r1.py：台账信息，对做题无价值，且含自引用本卷。
                L.append("")
            L += [c["q"].strip(), ""]
            if with_ans:
                L += ["**参考答案**：", "", c["ans"].strip(), ""]
            L += ["---", ""]
        io.open(os.path.join(OUTDIR, "第一轮综合卷%02d（%s）.md" % (pi, edition)),
                "w", encoding="utf-8", newline="\n").write(
                    _strip_mineru_div("\n".join(L)))
    manifest.append({"no": pi, "n": len(sel),
                     "tiers": dict(ti), "bands": dict(bd),
                     "topics": dict(collections.Counter(c["topic"] for c in sel)),
                     "srcs": sorted({c["r"].get("source_norm", "").strip('"\'') for c in sel}),
                     "paths": [c["r"]["_path"] for c in sel]})
io.open(os.path.join(OUTDIR, "_选题清单.json"), "w", encoding="utf-8").write(
    json.dumps(manifest, ensure_ascii=False, indent=1))

# ── 总索引 ────────────────────────────────────────────────────────────
tn = sum(m["n"] for m in manifest)
tb = collections.Counter()
tt = collections.Counter()
for m in manifest:
    tb.update({int(k): v for k, v in m["bands"].items()})
    tt.update(m["tiers"])
idx = ["---", 'title: "第一轮综合套卷 总索引"', "type: 索引", "role: 习题集索引",
       "round: 第一轮", "status: 已填充", "created: " + TODAY, "updated: " + TODAY,
       "question_count: " + str(tn), "tags: [化竞, 第一轮, 综合套卷, 索引]", "---", "",
       "# 第一轮综合套卷 · 总索引", "",
       "> **共 %d 套、%d 题**（结构化学 %d ＋ 化学原理 %d）；每套**教师版**（题面＋参考答案）与"
       "**学生版**（纯题面）各一份，题号同序。" % (
           len(manifest), tn,
           sum(m["topics"].get(k, 0) for m in manifest for k in ("S1", "S2", "S3", "S4", "S5", "S6")),
           sum(m["topics"].get(k, 0) for m in manifest for k in "P1 P2 P3 P4 P5 P6 P7 P8 P9".split())),
       "> **用途**：结构化学第一轮＋化学原理第一轮学完后的**综合练习**（跟课用专项卷，见 "
       "`04-课件/习题集/三·竞赛导向层（载体Ⅱ·Ⅲ）/第一轮·竞赛教材版/`；两系列**互不重复用题**）。", "",
       DISCIPLINE,
       "> **每套构成**：结构化学 15 ＋ 化学原理 15；难度 基础 6 ＋ 进阶 16 ＋ 挑战 8。", "",
       "| 卷 | 题数 | 基础/进阶/挑战 | 真题 | 竞赛题集 | 竞赛教程 | 竞赛教材 | 教师版 | 学生版 |",
       "|:--|--:|:--|--:|--:|--:|--:|:--|:--|"]
for m in manifest:
    b = m["bands"]
    t = m["tiers"]
    # 兼容 int / str 两种键（内存构造用 int、JSON 回读用 str；2026-09-17 实测曾整列输出 0）
    _g = lambda d, k: d.get(k, d.get(int(k), 0))
    idx.append("| 第%02d卷 | %d | %d/%d/%d | %d | %d | %d | %d | [[第一轮综合卷%02d（教师版）]] | [[第一轮综合卷%02d（学生版）]] |"
               % (m["no"], m["n"], _g(b, "2"), _g(b, "3"), _g(b, "4"),
                  _g(t, "0"), _g(t, "1"), _g(t, "2"), _g(t, "3"), m["no"], m["no"]))
idx += ["", "**合计**：基础 %d ＋ 进阶 %d ＋ 挑战 %d ＝ %d 题；真题 %d ／ 竞赛题集 %d ／ 竞赛教程 %d ／ 竞赛教材 %d。"
        % (tb.get(2, 0), tb.get(3, 0), tb.get(4, 0), tn,
           tt.get("0", 0), tt.get("1", 0), tt.get("2", 0), tt.get("3", 0)), ""]
io.open(os.path.join(OUTDIR, "_总索引.md"), "w", encoding="utf-8", newline="\n").write("\n".join(idx))
print("\n[write] %d 套 × 2 版 → %s" % (len(manifest), OUTDIR))
print("合计 %d 题（去重后）｜缺图 %d 处" % (sum(m["n"] for m in manifest), len(missing)))
for a, b in missing[:8]:
    print("   ", a, b)
