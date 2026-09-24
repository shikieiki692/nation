"""讲义真缺陷扫描：R1 整段重复 / R2 元信息混入正文 / R3 通用常识 / R4 空泛抒情。

R1 用 25 汉字滑窗 + 包含率 ≥0.72，是**确定性判据**（可靠性最高）；
R2–R4 用词表，**必出实例供目检**（本库 R4 命中「Xe 神奇消失」经核为题目原文 ⇒ 假阳性）。
⚠️ 重复组需按性质分流：本库 84 组中 54 组＝**同讲多版本并存**（真冗余）、
   11 组＝单讲↔合集（装配产物，**不算缺陷**）。

复跑：python -X utf8 .workbuddy/scripts/handout_dup_scan.py
"""
"""原始说明：

R1 跨文件/跨节**整段重复**：25 汉字滑窗 + 包含率 ≥0.72 判同源重复
R2 元叙述混入正文：维护者视角的句子（"本节定位""选题口径""本讲定位""建议使用方式"…）
R3 通用常识式陈述：无化学专指的普适句（"自然界中一切自发过程都趋向…"类）
R4 空泛抒情：审美/感受式评价（"最美""魅力""震撼"…）

⚠️ R2–R4 用词表，必出实例供目检；R1 是确定性判据（滑窗精确匹配），可靠性最高。
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

V = Path(r"C:\Obsidion\妙妙屋")
ROOT = V / "04-课件/学生讲义"
OUT = V / ".workbuddy/tmp/img_audit"
sys.path.insert(0, str(V / ".workbuddy/tmp"))
from diag_density2 import blocks, LINE_CJK  # noqa: E402
from diag_density4 import split_layers, RE_COMMENT  # noqa: E402


def skel(t):
    return "".join(LINE_CJK.findall(t))


# ── 收集 L3 段落 ──
segs = []
for p in sorted(ROOT.rglob("*.md")):
    if "_归档" in p.parts or p.name.startswith("README"):
        continue
    rel = str(p.relative_to(V))
    L = split_layers(p.read_text(encoding="utf-8", errors="replace"))
    for x in L["l3"]:
        s = skel(x)
        if len(s) >= 40:
            segs.append(dict(file=rel, name=p.name, cjk=len(s), sk=s, raw=x.replace("\n", " ")))
print(f"L3 段落 {len(segs)} 段 / {sum(x['cjk'] for x in segs):,} 汉字")

W = 25

# ── R1 重复检测 ──
idx = defaultdict(list)
for i, x in enumerate(segs):
    for j in range(0, max(1, len(x["sk"]) - W + 1), 5):
        idx[x["sk"][j:j + W]].append(i)

groups, seen = [], set()
for i, x in enumerate(segs):
    if i in seen:
        continue
    mates = set()
    for j in range(0, max(1, len(x["sk"]) - W + 1), 5):
        for k in idx[x["sk"][j:j + W]]:
            if k != i:
                mates.add(k)
    strong = []
    for k in mates:
        a, b = x["sk"], segs[k]["sk"]
        short, long_ = (a, b) if len(a) <= len(b) else (b, a)
        # 短段的 shingle 有多少比例出现在长段里
        ws = [short[j:j + W] for j in range(0, max(1, len(short) - W + 1), 3)]
        if not ws:
            continue
        if sum(1 for w in ws if w in long_) / len(ws) >= 0.72:
            strong.append(k)
    if strong:
        grp = sorted({i} | set(strong))
        if grp[0] not in seen:
            groups.append(grp)
            seen |= set(grp)

print(f"\n{'='*80}\n=== R1 跨文件/跨节重复组：{len(groups)} 组 ===")
dupe_cjk = 0
detail = []
for g in sorted(groups, key=lambda x: -sum(segs[i]["cjk"] for i in x[1:])):
    head = segs[g[0]]
    copies = [segs[i] for i in g[1:]]
    extra = sum(c["cjk"] for c in copies)
    dupe_cjk += extra
    detail.append(dict(main=dict(file=head["file"], cjk=head["cjk"], text=head["raw"][:400]),
                       copies=[dict(file=c["file"], cjk=c["cjk"]) for c in copies]))
    if len(detail) <= 14:
        files = {head["file"].split("/")[-1]} | {c["file"].split("/")[-1] for c in copies}
        print(f"  ×{len(g)} 主{head['cjk']}字 副本{extra}字  涉及 {len(files)} 文件: "
              f"{' | '.join(list(files)[:3])}")
        print(f"      {head['raw'][:150]}")

print(f"\n  R1 可精简约 **{dupe_cjk:,} 汉字**（{dupe_cjk/len(segs) and dupe_cjk/sum(x['cjk'] for x in segs)*100:.1f}% of L3）")
(OUT / "dup_groups.json").write_text(json.dumps(detail, ensure_ascii=False, indent=1), encoding="utf-8")

# ── R2 元叙述 ──
META = [r"本讲(的)?定位", r"本节定位", r"选题口径", r"建议使用方式", r"配图规划",
        r"版本说明", r"本版(本)?为", r"主框架教材", r"辅助教材", r"深度边界",
        r"上节衔接", r"下节衔接", r"和第一轮其他讲的分工", r"教材覆盖口径",
        r"课堂主讲主线", r"配图说明", r"已被本页取代", r"已由 §"]
meta_hits = []
for x in segs:
    for pat in META:
        if re.search(pat, x["raw"]):
            meta_hits.append((x["file"], pat, x["raw"][:150]))
            break
print(f"\n{'='*80}\n=== R2 元叙述混入正文：{len(meta_hits)} 段 ===")
from collections import Counter
print("  按文件:", dict(Counter(h[0].split("/")[-1][:26] for h in meta_hits).most_common(8)))
for f, pat, t in meta_hits[:10]:
    print(f"    [{pat}] {f.split('/')[-1][:30]}  {t[:110]}")

# ── R3 通用陈述 / R4 抒情 ──
GEN = [r"自然界中一切自发过程", r"自然界的(普遍|基本)规律", r"万物", r"宇宙",
       r"这体现了化学的", r"体现了自然界的"]
LYR = [r"最美", r"最美妙", r"魅力", r"震撼", r"令人惊叹", r"神奇", r"奥妙", r"华丽", r"优雅"]
gen_h, lyr_h = [], []
for x in segs:
    for pat in GEN:
        if re.search(pat, x["raw"]):
            gen_h.append((x["file"], x["raw"][:170])); break
    for pat in LYR:
        if re.search(pat, x["raw"]):
            lyr_h.append((x["file"], pat, x["raw"][:150])); break
print(f"\n=== R3 通用常识式陈述：{len(gen_h)} 段 ===")
for f, t in gen_h[:8]:
    print(f"    {f.split('/')[-1][:32]}  {t[:120]}")
print(f"\n=== R4 空泛抒情：{len(lyr_h)} 段 ===")
for f, pat, t in lyr_h[:10]:
    print(f"    [{pat}] {f.split('/')[-1][:30]}  {t[:110]}")

json.dump(dict(meta=meta_hits, generic=gen_h, lyric=lyr_h, dup_extra_cjk=dupe_cjk),
          open(OUT / "defect_scan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ {OUT/'dup_groups.json'} | {OUT/'defect_scan.json'}")
