# -*- coding: utf-8 -*-
"""诊断：讲义里「理解要点 / 易错提醒 / 深入思考 / 拓展」类板块的**内容质量**。

⚠️ 判据局限（本库实测，务必先读）：
  · T1「<100 字」**不可作判据** —— 本库 34% 命中，但其中多数是**有效口诀**
    （如「酸性强≠热稳定性强」仅 56 字、「2.303 陷阱」是精华）。
  · T2「无化学实义」有**已知假阳性**（Unicode 上下标 ⁺⁻、纯标注型 callout），命中数只能当**上限**。
  · **C 薄壳 / D 错位 / E 空泛三类机检全部漏检**，只能人工读。
  ⇒ 机检只缩圈，终审必须通读（与 `讲义语言规范.md` §十 同一条纪律）。
复跑前置：目标为 `04-课件/学生讲义` 等目录，无需外部数据；输出落 <目录>/.workbuddy 之外时自带 --out。

判据设计（三条，分别对应三类"无效堆叠"）：
  T1 长度：正文 < 100 字 → 可疑"薄"（不是判据，只是缩圈线索）
  T2 无化学实义：正文里找不到 ① 化学式/元素符号 ② 带单位数值 ③ 对比词（而/但/区别/反常）
     ⇒ 大概率是"定义复述/常识提醒/考纲说明"这类复述性文字
  T3 复述指认：正文与「教材定义式」高度重合（关键词：是……的近似 / 定义为 / 属于 / 表示为）

输出：总体分布 + 按文件排行 + T2 全量清单（供人工抽样核对）
用法: diag_filler.py [目录1 目录2 …]
"""
import re, sys
from pathlib import Path
from collections import Counter, defaultdict

V = Path(r"C:\Obsidion\妙妙屋")
ROOTS = [V / a for a in (sys.argv[1:] or ["04-课件/学生讲义"])]
OUT = V / ".workbuddy/tmp/img_audit"      # 复用草稿区，避免新增目录

# callout 型（形如 `> [!warning] 易错提醒`）与 标题型（`## 附：易错清单`）两类
CALLOUT = re.compile(r"^>\s*\[!(\w+)\][-+]?\s*(.*)$")
HEADSEC = re.compile(r"^(#{1,6})\s*(.*?(?:易错|理解要点|深入思考|误区|认知冲突|易混|小贴士|拓展|延伸阅读|记忆口诀|延伸|小结).*)$")
ANYHEAD = re.compile(r"^(#{1,6})\s")
CHEM = re.compile(
    r"[A-Z][a-z]?[0-9₀-₉⁰-⁹]|\$[^$]+\$|\\ce|\\mathrm|→|⟶|⇌|△|Δ"
    r"|[₀-₉⁰-⁹]|[α-ωΑ-Ω]|°|↑|↓|≡|≈|±|pK|pH|E_|Δ[GHS]")
UNIT = re.compile(r"\d+(\.\d+)?\s*(kJ|KJ|kJ/mol|J|K|Pa|kPa|MPa|mol|L|mL|cm|nm|pm|°C|℃|%|eV|V|A|Hz|cm-1|cm⁻¹)")
CMP = re.compile(r"而|但|区别|反常|不同|相反|不等|≠|例外|恰恰|误|错")
REWORD = re.compile(r"是.{0,12}的(近似|模型|推广|特例)|定义为|指的是|属于|表示为|即.{0,6}的")

rows = []
for ROOT in ROOTS:
    for p in sorted(ROOT.rglob("*.md")):
        if "_归档" in p.parts:
            continue
        lines = p.read_text(encoding="utf-8", errors="replace").split("\n")
        i = 0
        while i < len(lines):
            ln = lines[i]
            mc = CALLOUT.match(ln)
            mh = None if mc else HEADSEC.match(ln)
            if not mc and not mh:
                i += 1
                continue
            if mc:
                kind, title = "callout", (mc.group(2) or mc.group(1)).strip()
                # 收正文：连续同一 callout 的行（含空 >）
                body, j = [], i + 1
                while j < len(lines) and (lines[j].startswith(">") or lines[j].strip() == ""):
                    if lines[j].strip() == "" and not (j + 1 < len(lines) and lines[j + 1].startswith(">")):
                        break
                    body.append(re.sub(r"^>\s?", "", lines[j]))
                    j += 1
                i = j
            else:
                lv, title = len(mh.group(1)), mh.group(2).strip()
                body, j = [], i + 1
                while j < len(lines):
                    m2 = ANYHEAD.match(lines[j])
                    if m2 and len(m2.group(1)) <= lv:
                        break
                    body.append(lines[j]); j += 1
                i = j
            txt = " ".join(x.strip() for x in body if x.strip())
            n = len(txt)
            if n == 0:          # 空壳 callout（如「练一练」标签）不进统计
                continue
            rows.append(dict(
                file=str(p.relative_to(V)), line=0, kind=kind, title=title, n=n, txt=txt,
                t2=(not (CHEM.search(txt) or UNIT.search(txt) or CMP.search(txt))),
                t3=bool(REWORD.search(txt)),
                thin=(n < 100)))

print(f"扫描目录 {[r.name for r in ROOTS]}　命中板块 {len(rows)} 处")
print("  类型分布:", dict(Counter(r["kind"] for r in rows)))
print("  标题频次 top12:")
for k, v in Counter(r["title"] for r in rows).most_common(12):
    print(f"    {v:4d}  {k[:52]}")
thin = [r for r in rows if r["thin"]]
t2 = [r for r in rows if r["t2"]]
t3 = [r for r in rows if r["t3"]]
print(f"\n  T1 薄(<100 字)        : {len(thin)}　（{len(thin)/max(1,len(rows))*100:.0f}%）")
print(f"  T2 无化学实义         : {len(t2)}　（{len(t2)/max(1,len(rows))*100:.0f}%）")
print(f"  T3 复述式措辞         : {len(t3)}　（{len(t3)/max(1,len(rows))*100:.0f}%）")
print(f"  T1∩T2（嫌疑最大）     : {len([r for r in rows if r['thin'] and r['t2']])}")

print("\n=== T2 清单（无化学式/无数值/无对比词）前 30 条 ===")
byfile = defaultdict(list)
for r in t2:
    byfile[r["file"]].append(r)
for f, rs in sorted(byfile.items(), key=lambda kv: -len(kv[1]))[:14]:
    print(f"\n  {f}　（{len(rs)} 处）")
    for r in rs[:4]:
        print(f"     [{r['title'][:20]}] {r['n']}字  {r['txt'][:100]}")

OUT.mkdir(parents=True, exist_ok=True)
import json
(OUT / "filler_diag.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"\n→ {OUT.relative_to(V) / 'filler_diag.json'}")
