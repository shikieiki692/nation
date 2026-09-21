"""扫活跃讲义源 md，按 ``` 围栏切块，输出逐块处置清单（CSV）。

用途：把「等宽段治理」的定位基准从 docx 反推改为**源 md 精确到行号**。

活跃口径 = 与 11-模板/scripts/build-all-handout-docx.py 的默认批量范围一致：
  04-课件/学生讲义/**/*.md
  排除：路径含 `_归档`、首层目录以 `_` 开头、stem == README、stem 前缀 `讲义升级模式-`
  保留：stem 含 `超级充实` / `基础版` / `复习` / `-新课`

产出：
  .workbuddy/tmp/verbatim_worklist.csv
  stdout  汇总 + 与 docx 侧 SourceCode 段数的对账
"""
import collections
import csv
import re
from pathlib import Path

ROOT = Path(r"C:\Obsidion\妙妙屋")
SRC = ROOT / "04-课件" / "学生讲义"
OUTCSV = ROOT / ".workbuddy" / "tmp" / "verbatim_worklist.csv"

EXCLUDED_STEMS = {"README"}
EXCLUDED_PREFIXES = ("讲义升级模式-",)
MARKERS = ("超级充实", "基础版", "复习", "-新课")

# ── 与 docx 侧一致的三分类判据 ──
STRUCT = re.compile(r"[├└│─┌┐└┘]|━|\|")
FLOW = re.compile(r"→|—\w*[→>]|⟶")

# ── 分型判据 ──
RE_BOX = re.compile(r"[├└┌┐]")
RE_LINE = re.compile(r"[─━]|│")
RE_GEOM = re.compile(r"\\|/|—{2,}|={2,}")
RE_STEP = re.compile(r"(?m)^\s*(?:Step\s*\d|[①②③④⑤⑥⑦⑧⑨⑩]|\d+\s*[.、)])")
RE_ARROW = re.compile(r"→|⟶|—\w*[→>]")
RE_ALIGN = re.compile(r"\S {2,}\S")
RE_ACTIVE = re.compile(r"[\[\]`*_]|\\\*|<|>")

# 围栏开启行（含 ```text 这类信息串，也含引用块内的 `> ``` `）
OPEN_RE = re.compile(r"^((?:\s{0,3}>\s?)*\s{0,3})(`{3,}|~{3,})\s*(\S*)\s*$")


def active_md():
    """候选人集合 = 与 build 脚本的 candidates 一致（**不加** HANDOUT_MARKERS 过滤）。

    注意：HANDOUT_MARKERS（超级充实/基础版/复习/-新课）只在**批量默认**路径生效；
    `--path` 可在 candidates 内任意指定文件。实测 81 份产物里含大量无 marker 的 stem
    （如 `自由基反应`、`醛酮羧酸`），它们是显式 --path 构建的 → 必须纳入 candidates。
    """
    res = []
    for p in sorted(SRC.rglob("*.md")):
        rel = p.relative_to(SRC)
        if "_归档" in rel.parts or rel.parts[0].startswith("_"):
            continue
        if p.stem in EXCLUDED_STEMS or p.stem.startswith(EXCLUDED_PREFIXES):
            continue
        res.append(p)
    return res


def is_std(p: Path) -> bool:
    return any(m in p.stem for m in MARKERS)


def comment_mask(lines):
    """True = 该行**起始时**处于 HTML 注释内。

    管线 Stage-1 会剥掉 HTML 注释（教师区），注释里的围栏块不会进 docx，
    对账时必须一并排除。
    """
    mask = [False] * len(lines)
    inside = False
    for i, l in enumerate(lines):
        if inside:
            mask[i] = True
        j = 0
        while True:
            if not inside:
                k = l.find("<!--", j)
                if k < 0:
                    break
                e = l.find("-->", k + 4)
                if e < 0:
                    inside = True
                    break
                j = e + 3
            else:
                e = l.find("-->", j)
                if e < 0:
                    break
                inside = False
                j = e + 3
    return mask


def scan_blocks(lines, mask):
    """返回 [(open_line, close_line, lang, body_lines, in_quote)]，行号 1-based。

    mask[i] 为 True 的行（HTML 注释内）不作为围栏开启行。
    """
    out = []
    i, n = 0, len(lines)
    open_re = OPEN_RE
    while i < n:
        m = open_re.match(lines[i])
        if not m or mask[i]:
            i += 1
            continue
        fence = m.group(2)
        close_re = re.compile(
            r"^(?:\s{0,3}>\s?)*\s{0,3}" + re.escape(fence[0]) + "{%d,}\\s*$" % len(fence)
        )
        body, j = [], i + 1
        while j < n and not close_re.match(lines[j]):
            body.append(lines[j])
            j += 1
        out.append((i + 1, (j + 1 if j < n else n), m.group(3), body, ">" in m.group(1)))
        i = j + 1 if j < n else n
    return out


def norm_body(body):
    return [re.sub(r"^(?:\s{0,3}>\s?)+\s?", "", l) for l in body]


def suggest(body):
    txt = "\n".join(body)
    nl = len([l for l in body if l.strip()])
    if RE_BOX.search(txt):
        return "判断树", "转嵌套列表"
    if RE_LINE.search(txt):
        return "结构图/连线", "评估转图片，否则留等宽"
    if nl >= 3 and RE_GEOM.search(txt):
        return "几何/结构式", "转图片（查图谱库优先）"
    if RE_STEP.search(txt):
        return "流程步骤", "转有序/嵌套列表（列表前空一行）"
    if RE_ARROW.search(txt) and nl <= 3:
        return "反应式", "提正文（保留 Unicode 箭头）"
    if nl >= 2 and len([l for l in body if RE_ALIGN.search(l)]) >= 2:
        return "数据/对齐表", "转 md 表格或正文"
    return "文字型", "提正文/公式"


rows = []
files = active_md()
tot_blocks = 0
odd_fence = []       # 围栏行数为奇数 = 有未闭合围栏
for p in files:
    raw = p.read_text(encoding="utf-8")
    lines = raw.split("\n")
    rel = p.relative_to(SRC).as_posix()
    mask = comment_mask(lines)
    n_fence = sum(1 for i, l in enumerate(lines)
                  if OPEN_RE.match(l) and not mask[i])
    if n_fence % 2:
        odd_fence.append((rel, n_fence))
    for idx, (ol, cl, lang, body, inq) in enumerate(scan_blocks(lines, mask), 1):
        tot_blocks += 1
        nb = norm_body(body)
        txt = "\n".join(nb)
        kind = ("结构图" if STRUCT.search(txt)
                else ("流程排序" if FLOW.search(txt) else "纯文本"))
        ftype, action = suggest(nb)
        lead = ""
        k = ol - 2
        while k >= 0:
            s = lines[k].strip()
            if s and not s.startswith("```"):
                lead = s[:80]
                break
            k -= 1
        nz = [l.strip() for l in nb if l.strip()]
        rows.append({
            "文件": rel,
            "标准讲义": "是" if is_std(p) else "",
            "块序": idx,
            "起行": ol,
            "止行": cl,
            "语言": lang or "(裸)",
            "引用块": "是" if inq else "",
            "有效行": len(nz),
            "判据类别": kind,
            "建议分型": ftype,
            "建议处置": action,
            "含$": "是" if "$" in txt else "",
            "活性字符": "".join(sorted(set(RE_ACTIVE.findall(txt))))[:12],
            "引导语": lead,
            "首行": (nz[0][:70] if nz else ""),
            "次行": (nz[1][:70] if len(nz) > 1 else ""),
        })

with open(OUTCSV, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print("活跃源 md：", len(files), "份")
print("围栏块总数：", tot_blocks)
print()
print("── 三分类（应与 docx 侧对齐）──")
for k, n in collections.Counter(r["判据类别"] for r in rows).most_common():
    print(f"   {k}: {n}")
print()
print("── 建议分型 ──")
for k, n in collections.Counter(r["建议分型"] for r in rows).most_common():
    print(f"   {k}: {n}")
print()
print("── 语言标注分布 ──")
for k, n in collections.Counter(r["语言"] for r in rows).most_common():
    print(f"   {k}: {n}")
print()
print("── 含 $ 的块 ──")
md = [r for r in rows if r["含$"]]
print("   共", len(md), "块；文件：", sorted({r["文件"] for r in md}))
print()
print("── 按文件（块数 top15）──")
for k, n in collections.Counter(r["文件"] for r in rows).most_common(15):
    print(f"   {n:3d}  {k}")

print()
print("── 对账：源 md 围栏块  vs  docx 侧 SourceCode 段 ──")
import json  # noqa: E402

base = ROOT / ".workbuddy" / "tmp" / "verbatim_baseline.json"
docx_cnt = collections.Counter()
if base.exists():
    for r in json.loads(base.read_text(encoding="utf-8")):
        if r["group"] == "块":
            docx_cnt[Path(r["file"]).stem] += 1
md_cnt = collections.Counter(Path(r["文件"]).stem for r in rows)
print(f"  源 md 围栏块 {sum(md_cnt.values())}   docx SourceCode 段 {sum(docx_cnt.values())}")
allk = sorted(set(md_cnt) | set(docx_cnt))
mismatch = [(k, md_cnt.get(k, 0), docx_cnt.get(k, 0)) for k in allk
            if md_cnt.get(k, 0) != docx_cnt.get(k, 0)]
print(f"  数不符 / 单侧缺失：{len(mismatch)} 个 stem")
for k, a, b in mismatch[:30]:
    print(f"    {k}: md={a} docx={b}")

print()
print("── 数据质量：未闭合围栏（围栏行数为奇数 → pandoc 不识别为代码块）──")
if odd_fence:
    for r, n in odd_fence:
        print(f"   ! {r}  围栏行数={n}")
else:
    print("   无")

print()
print("清单已写入：", OUTCSV)
