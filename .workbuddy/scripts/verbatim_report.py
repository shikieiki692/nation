"""讲义产物「等宽段」结构化报表（v2）

区分两类根因（旧脚本 scan_verbatim.py 只按 "VerbatimChar" 字符串判段，混在一起）：
  A) 真代码块   —— w:pStyle == "SourceCode"      （来自源 md 的 ``` 围栏）
  B) 行内反引号 —— 段落含 rStyle VerbatimChar，但 pStyle 是正文类（Compact/BodyText/…）

产出：
  .workbuddy/tmp/verbatim_baseline.json   全量明细，供治理后 diff
  stdout                                  汇总报表
"""
import collections
import json
import os
import re
import zipfile


def zipfile_read(path: str) -> str:
    with zipfile.ZipFile(path) as z:
        return z.read("word/document.xml").decode("utf-8")

OUT = r"C:\Obsidion\妙妙屋\06-学生侧材料\讲义"
BASE = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\verbatim_baseline.json"

T = re.compile(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", re.S)
PARA = re.compile(r"<w:p[ >].*?</w:p>", re.S)
PS = re.compile(r'<w:pStyle w:val="([^"]+)"')
BR = re.compile(r"<w:br\s*/>")

# 与旧口径保持一致，便于对账
STRUCT = re.compile(r"[├└│─┌┐└┘]|━|\|")
FLOW = re.compile(r"→|—\w*[→>]|⟶")

NL = "\u21b5"  # ↵ 块内换行标记


def para_text(blk: str) -> str:
    s = BR.sub(NL, blk)
    return "".join(T.findall(s)).strip()


def classify(t: str) -> str:
    if STRUCT.search(t):
        return "结构图"
    if FLOW.search(t):
        return "流程排序"
    return "纯文本"


rows = []
for dp, dns, fns in os.walk(OUT):
    rel0 = os.path.relpath(dp, OUT)
    if rel0.split(os.sep)[0] == "_archive":
        continue
    for fn in sorted(fns):
        if not fn.endswith(".docx") or fn.startswith("~$"):
            continue
        path = os.path.join(dp, fn)
        try:
            xml = zipfile_read(path)
        except Exception:
            continue
        rel = fn if rel0 == "." else os.path.join(rel0, fn)
        for blk in PARA.findall(xml):
            if "VerbatimChar" not in blk:
                continue
            txt = para_text(blk)
            if not txt:
                continue
            m = PS.search(blk)
            pstyle = m.group(1) if m else "(none)"
            rows.append({
                "file": rel.replace("\\", "/"),
                "pstyle": pstyle,
                "group": "块" if pstyle == "SourceCode" else "行内",
                "kind": classify(txt),
                "text": txt,
            })

with open(BASE, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)

# ── 报表 ──
print("=" * 64)
print("等宽段总数：", len(rows))
print("=" * 64)
gc = collections.Counter(r["group"] for r in rows)
for g in ("块", "行内"):
    sub = [r for r in rows if r["group"] == g]
    kc = collections.Counter(r["kind"] for r in sub)
    print(f"[{g}] {gc.get(g,0):4d} 段   结构图 {kc.get('结构图',0):3d} / "
          f"流程排序 {kc.get('流程排序',0):3d} / 纯文本 {kc.get('纯文本',0):3d}")

print()
print("── 交叉表：类别 x 段落样式 ──")
cross = collections.Counter((r["kind"], r["pstyle"]) for r in rows)
for kind in ("结构图", "流程排序", "纯文本"):
    items = sorted(((s, n) for (k, s), n in cross.items() if k == kind),
                   key=lambda x: -x[1])
    tot = sum(n for _, n in items)
    print(f"  {kind}({tot}): " + ", ".join(f"{s}={n}" for s, n in items))

print()
print("── 真代码块（SourceCode）按文件分布 ──")
bc = collections.Counter(r["file"] for r in rows if r["group"] == "块")
print(f"  涉及 {len(bc)} 个文件")
for f, n in bc.most_common(15):
    print(f"    {n:3d}  {f}")

print()
print("── 行内反引号按文件分布 top10 ──")
ic = collections.Counter(r["file"] for r in rows if r["group"] == "行内")
print(f"  涉及 {len(ic)} 个文件")
for f, n in ic.most_common(10):
    print(f"    {n:3d}  {f}")

print()
print("明细已写入：", BASE)
