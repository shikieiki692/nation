# -*- coding: utf-8 -*-
"""待目检视觉核验 第二批写入：第 180–588 张（409 张）→ 判定台账 + 回写三份索引状态列。

方法：21 张印相表（4×5 格、300×250 大格、中文字体标注）逐格目检；
      5 张可疑小图 + 1 张含角标图做**原尺寸 ×3 放大复核**（再定案）。
约定（与第一批一致）：
  合格 → 🟢已视觉核验；废片 → 🔴已核验·废片（新状态档）
保障：行级回写前逐条校验「文件名 / 现状态含待目检 / 列数 ≥6」，任一不符即跳过并报出。
"""
import json, sys
from pathlib import Path

V = Path(r"C:\Obsidion\妙妙屋")
O = V / ".workbuddy/tmp/img_audit"
S = V / ".workbuddy/scripts"
WO = json.load(open(O / "pending_wo.json", encoding="utf-8"))
dry = "run" not in sys.argv

# ── 本批（180–588）判废清单：idx_no → 理由（全部经原尺寸放大确认） ──
BAD = {
    182: "QR 码",
    326: "剪贴画（UFO，与化学无关）",
    334: "剪贴画（UFO，同画面第 2 份副本）",
    346: "剪贴画（UFO，同画面第 3 份副本）",
    353: "QR 码",
}
# 主体合格但带缺陷，单独留痕（不判废）
WARN = {
    242: "主体为合格晶体结构（A1/A2/B1 + a/b/c 轴），但右侧嵌一竖排 QR 码（拼版图）",
}
# 明显「图文不符」样例（描述质量线，与图像质量分开记）
DESC_MISMATCH = {
    227: "声称「环己酮→TMS 端醇→二溴代物」/ 实为 Ga≡Ga 三重键化合物",
    229: "声称「喹啉硝化 (HNO3/H2SO4)」/ 实为烯醇 + MeC(OEt)3 酯化",
    232: "声称「苯甲酸结构」/ 实为 CsCl 型晶体（Fe/Cs/Cl）",
    235: "声称「亲核加成机理 (107°角)」/ 实为 [Ga-Ga]²⁻ 阴离子",
    251: "声称「吲哚烷基化机理（金催化）」/ 实为喹啉硝化",
    265: "声称「HFIP 促进的有机反应机理」/ 实为硼簇结构",
    267: "声称「磷脂酰乙醇胺 (PE) 超分子结构」/ 实为晶体球棍结构",
    294: "声称「联苯二酚环化 (H2SO4)」/ 实为 Fe 立方簇",
    367: "声称「NaCl 面心立方晶体结构」/ 实为 C60 富勒烯笼",
    403: "声称「双核钴胺配合物 (Co(I)CO)」/ 实为 A-pH 曲线图",
    432: "声称「KMnO4 氧化 H2O2 / KI 反应方程式」/ 实为 Cu(NH3)n²⁺ 分布分数图",
    447: "声称「物质-能量-信息三角关系」/ 实为氢键结构示意",
    462: "声称「沉淀转化反应方程式」/ 实为分光光度法比色皿原理图",
    469: "声称「Ir(CO)3(CH3) 配合物结构」/ 实为 P4O7 结构",
    531: "声称「两种点缺陷 (Schottky)」/ 实为球堆积照片",
    539: "声称「六方最密堆积 (abab)」/ 实为反应式",
    587: "声称「水的 Pourbaix 图 a/b 线」/ 实为 d 轨道分裂图",
}

LO, HI = 180, 589          # [180, 589)
verdicts, warns = [], []
for i in range(LO, HI):
    e = WO[i]
    rec = dict(idx_no=i, idx=e["idx"], ln=e["ln"], name=e["name"],
               w=e["w"], h=e["h"])
    if i in BAD:
        rec.update(verdict="废片", why=BAD[i])
    else:
        rec.update(verdict="合格", why="")
    if i in DESC_MISMATCH:
        rec["desc_mismatch"] = DESC_MISMATCH[i]
    verdicts.append(rec)
    if i in WARN:
        warns.append(dict(idx_no=i, name=e["name"], note=WARN[i]))

ok = [v for v in verdicts if v["verdict"] == "合格"]
bad = [v for v in verdicts if v["verdict"] == "废片"]
print(f"本批判定（{LO}–{HI-1}，共 {len(verdicts)} 张）：合格 {len(ok)}　废片 {len(bad)}"
      f"（{len(bad)/len(verdicts)*100:.1f}%）")
for v in bad:
    print(f"   ✗ [{v['idx_no']:3d}] {v['name'][:34]} {v['w']}x{v['h']}  {v['why']}")
print(f"   带缺陷但主体合格 {len(warns)}：")
for w in warns:
    print(f"   ⚠️ [{w['idx_no']}] {w['note'][:80]}")
print(f"   记录在案的「图文不符」样例 {sum(1 for v in verdicts if 'desc_mismatch' in v)} 条（描述质量线，不判废）")

# ── 回写索引状态列 ──
IDXF = {
    "01-有机化学": "10-索引与统计/01-有机化学图谱总索引.md",
    "02-结构与无机": "10-索引与统计/02-结构与无机化学图谱总索引.md",
    "03-物化与分析": "10-索引与统计/03-物化与分析化学图谱总索引.md",
}
byfile = {}
for v in verdicts:
    byfile.setdefault(v["idx"], []).append(v)

changed = 0
for tag, vs in byfile.items():
    fp = V / IDXF[tag]
    lines = fp.read_text(encoding="utf-8").split("\n")
    n = 0
    for v in vs:
        ln = v["ln"] - 1
        if ln < 0 or ln >= len(lines):
            print(f"   ⚠️ 行号越界 {tag} L{v['ln']}"); continue
        old = lines[ln]
        if not old.startswith("| "):
            print(f"   ⚠️ 非表格行 {tag} L{v['ln']}: {old[:50]}"); continue
        cells = [x.strip() for x in old.strip().strip("|").split("|")]
        if len(cells) < 6:
            print(f"   ⚠️ 列数异常 {tag} L{v['ln']}"); continue
        if cells[0] != v["name"]:
            print(f"   ⚠️ 名不符 {tag} L{v['ln']}: {cells[0][:24]} != {v['name'][:24]}"); continue
        if "待目检" not in cells[5]:
            print(f"   ⚠️ 状态非待目检 {tag} L{v['ln']}: {cells[5]}"); continue
        cells[5] = "🟢已视觉核验" if v["verdict"] == "合格" else "🔴已核验·废片"
        lines[ln] = "| " + " | ".join(cells) + " |"
        n += 1
    if n and not dry:
        fp.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"  {tag}: 改写 {n} 行{'（干跑未写盘）' if dry else ''}")
    changed += n

# ── 合并台账（前批 180 + 本批 409 = 589） ──
if not dry:
    prev = json.loads((S / "img_pending_verdicts.json").read_text(encoding="utf-8"))
    all_items = prev["all_items"] + verdicts
    bad_all = prev["bad_items"] + bad
    doc = dict(
        scope=f"全部 {len(all_items)} 张（主工单 在库×被引用，589 张）",
        ok=sum(1 for x in all_items if x["verdict"] == "合格"),
        bad=len(bad_all), bad_items=bad_all,
        warn=prev.get("warn", []) + warns,
        all_items=all_items,
        source="逐格目检 21+9 张印相表（4×5 大格 / 中文字体标注）+ 原尺寸放大复核关键样本",
    )
    for p in (O / "pending_verdicts.json", S / "img_pending_verdicts.json"):
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ 台账合并：合格 {doc['ok']}　废片 {doc['bad']}　共 {len(all_items)} 张")
    print("→ 已写", (O / 'pending_verdicts.json').name, "+", (S / 'img_pending_verdicts.json').name)
print("合计改写", changed, f"行{'（干跑）' if dry else ''}")
