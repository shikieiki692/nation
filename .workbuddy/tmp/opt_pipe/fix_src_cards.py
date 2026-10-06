# -*- coding: utf-8 -*-
"""fix_src_cards.py —— 机构题源卡（04-题库/2026机构初赛模拟题）结构性伪影修复。

处理 7 类（全部确定性、不涉及内容判断）：
  1 表格改造：A 单格行/容器表 → 段落；C 全「小问号|答案」行 → 段落；其余保留 HTML 表
     并丢掉「题面重述」单格行（<td>N-M 题干…</td>）
  2 图黏连文字：`3-6(共6分)![[a]]![[b]]` → 图各占一行
  3 图后游离 X（源 PDF 勾选框被 OCR 成 X）
  4 水印文字引用行（`> 清北营教育`）
  5 代码栅栏 ``` / ```txt（只删栅栏，保留内容）
  6 行内公式两端空格 `$ x $` → `$x$`
  7 `\\sf`（texmath 不支持）

强断言（不满足即中止、不写盘）：
  · 卡数不变          · frontmatter 字节不变
  · 图片引用多重集不变（本脚本不动图引用）
  · `## 题目`/`## 参考答案`/`## 知识点映射` 仍存在且顺序不变
  · 每卡 `$` 计数奇偶性不变

用法：python fix_src_cards.py            # dry-run（只报统计 + 抽样 diff）
      python fix_src_cards.py --apply    # 写盘
"""
import io, os, re, glob, sys, collections, difflib
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(ROOT, "04-题库", "2026机构初赛模拟题")

FM = re.compile(r'\A(?:---\r?\n.*?\r?\n---[ \t]*\r?\n)', re.S)
TABLE = re.compile(r'<table\b[^>]*>.*?</table>', re.S)
ROW = re.compile(r'<tr\b[^>]*>(.*?)</tr>', re.S)
CELL = re.compile(r'<t[dh]\b[^>]*>(.*?)</t[dh]>', re.S)
SUBQ = re.compile(r'\d+(?:-\d+)+')
SUBLAB = re.compile(r'^\s*(\d+(?:-\d+)+)\s*(?:[（(]?\s*共?\s*\d+\s*分\s*[）)]?)?\s*$')
IMGTAG = re.compile(r'(!\[\[[^\]]*\]\]|!\[[^\]]*\]\([^)]*\)|<img\b[^>]*>)')
IMGREF = re.compile(r'images/([0-9a-fA-F]{64}\.[A-Za-z0-9]+)|!\[\[([0-9a-fA-F]{64}\.[A-Za-z0-9]+)')
WM = re.compile(r'^\s*>\s*(清北营教育|清北教育|清北营|化英社|北斗学友|致学教育|教育|ZCHEM|ZChem|致学)\s*$')
FENCE = re.compile(r'^\s*```\w*\s*$')
MATHSP = re.compile(r'(?<!\$)\$([^$\n]{1,400}?)\$(?!\$)')
SF = re.compile(r'\\sf\b\s*')
H2 = ["## 题目", "## 参考答案", "## 知识点映射"]

ST = collections.Counter()


def plain(c):
    return re.sub(r'<[^>]+>', '', c).strip()


def has_content(c):
    """单元格是否「有内容」：有文字 **或** 含图（⚠️ 只含 `<img>` 的单元格先前被当空行丢掉）。"""
    return bool(plain(c)) or bool(re.search(r'<img\b|!\[', c))


# ── 1 表格 ──────────────────────────────────────────────────────────
def fix_tables(s):
    def rep(m):
        tb = m.group(0)
        rows = []
        for rm in ROW.finditer(tb):
            raw = rm.group(1)
            cells = CELL.findall(raw)
            # ⚠️ colspan="1"/rowspan="1" 是**无意义**写法，不算结构单元格
            #    （源里回显行常带 colspan="1"，曾因此逃过「单格行」判定）
            struct = sum(1 for n in re.findall(r'(?:col|row)span\s*=\s*"?(\d+)"?', raw)
                         if int(n) >= 2)
            rows.append(dict(raw=rm.group(0), cells=cells,
                             plains=[plain(c) for c in cells],
                             keepcell=[has_content(c) for c in cells],
                             nstruct=struct))
        if not rows:
            return tb
        live = [r for r in rows if any(r["keepcell"])]
        if not live:
            ST["表格-整表空"] += 1
            return ""

        def nonempty(r):
            return [c for c, k in zip(r["cells"], r["keepcell"]) if k]

        # ① 表内「标签行」的小问号集合（含父级前缀，如 2-4-1 ⇒ 2-4 / 2）
        label_ids = set()
        for r in live:
            ne = nonempty(r)
            if len(ne) == 2 and r["nstruct"] == 0:
                mm = SUBLAB.match(plain(ne[0]))
                if mm:
                    label_ids.add(mm.group(1))
        ids = set(label_ids)
        for i in label_ids:
            parts = i.split("-")
            for k in range(1, len(parts)):
                ids.add("-".join(parts[:k]))

        # ② 丢「题面重述」行：**单格**且文本以本表某小问号开头、后接题干正文
        #    （源里这类行写成 `<td colspan="2">4-3-2 题干…</td>`，是版面占位，非答案）
        kept, echo = [], 0
        for r in live:
            ne = nonempty(r)
            if len(ne) == 1 and not re.search(r'<img\b|!\[', ne[0]):
                p = re.sub(r'\s+', ' ', plain(ne[0])).strip()
                mm = re.match(r'^(\d+(?:-\d+)+)\s*', p)
                if mm and mm.group(1) in ids and len(p) > len(mm.group(0)) + 8:
                    echo += 1
                    continue
            kept.append(r)
        if not kept:
            ST["表格-全为回显"] += 1
            return ""

        # ③ 分类
        label_rows, single_rows, data_rows = [], [], []
        for r in kept:
            ne = nonempty(r)
            if len(ne) == 1:
                (single_rows if r["nstruct"] == 0 else data_rows).append(r)
            elif len(ne) == 2 and r["nstruct"] == 0 and SUBLAB.match(plain(ne[0])):
                label_rows.append(r)
            else:
                data_rows.append(r)

        # A. 无数据行 ⇒ 整表降级为段落
        if not data_rows:
            out = []
            for r in label_rows:
                ne = nonempty(r)
                out.append("**%s** %s" % (plain(ne[0]), ne[1].strip()))
            for r in single_rows:
                ne = nonempty(r)[0]
                p = plain(ne)
                mm = re.match(r'^(\d+(?:-\d+)+)\s+(.*)$', p, re.S)
                if mm:
                    # ⚠️ 必须基于**原始单元格**（含 <img>）重建，用 plain 会丢图
                    rest = re.sub(r'^\s*' + re.escape(mm.group(1)) + r'\s*', '', ne, count=1)
                    out.append("**%s** %s" % (mm.group(1), rest.strip()))
                else:
                    out.append(ne.strip())
            ST["表格-A降级为段落"] += 1
            return "\n\n" + "\n\n".join(out) + "\n\n"

        # B. 有数据行 ⇒ 保留 HTML 表（仅按 ② 丢掉回显行）
        if echo:
            ST["表格-B丢回显行"] += 1
            return "<table>" + "".join(r["raw"] for r in kept) + "</table>"
        return tb

    return TABLE.sub(rep, s)


# ── 2 图黏连 ────────────────────────────────────────────────────────
def fix_glued(s):
    out = []
    for l in s.split("\n"):
        if "<table" in l or l.strip().startswith("|"):
            out.append(l)
            continue
        if IMGTAG.search(l) and IMGTAG.sub("", l).strip():
            l = IMGTAG.sub(lambda m: "\n" + m.group(1) + "\n", l)
            l = re.sub(r'\n{2,}', '\n\n', l)
            ST["图黏连拆行"] += 1
        out.append(l)
    return "\n".join(out)


# ── 3 图后游离 X ────────────────────────────────────────────────────
def fix_stray_x(s):
    lines = s.split("\n")
    out = []
    for l in lines:
        if re.fullmatch(r'\s*X\s*', l):
            prev = next((x for x in reversed(out) if x.strip()), "")
            if IMGTAG.search(prev):
                ST["图后游离X"] += 1
                continue
        out.append(l)
    return "\n".join(out)


# ── 4 水印文字引用行 ────────────────────────────────────────────────
def fix_wm_lines(s):
    out = []
    for l in s.split("\n"):
        if WM.match(l):
            ST["水印引用行"] += 1
            continue
        out.append(l)
    return "\n".join(out)


# ── 5 代码栅栏 ──────────────────────────────────────────────────────
def fix_fences(s):
    out = []
    for l in s.split("\n"):
        if FENCE.match(l):
            ST["代码栅栏"] += 1
            continue
        out.append(l)
    return "\n".join(out)


# ── 6 行内公式两端空格 ──────────────────────────────────────────────
def fix_math(sp):
    def rep(m):
        c = m.group(1).strip()
        return "$%s$" % c if c else m.group(0)
    return MATHSP.sub(rep, sp)


# ── 7 \sf ──────────────────────────────────────────────────────────
def fix_sf(s):
    return SF.sub("", s)


def transform(body):
    """逐步变换；**任何一步若改变图片引用多重集就整步回退**（图绝不丢/不增）。"""
    base = sorted(IMGREF.findall(body))
    b = body
    for fn in (fix_tables, fix_glued, fix_stray_x, fix_wm_lines, fix_fences, fix_math, fix_sf):
        nb = fn(b)
        if nb != b and sorted(IMGREF.findall(nb)) != base:
            ST["回退步-" + fn.__name__] += 1
            continue
        b = nb
    return b


def main():
    apply = "--apply" in sys.argv
    show = "--show" in sys.argv
    cards = sorted(glob.glob(os.path.join(BASE, "*", "题-*.md")))
    changed, errs, shown = 0, [], 0
    samples = []
    for p in cards:
        raw = io.open(p, encoding="utf-8").read()
        m = FM.match(raw)
        fm, body = (m.group(0), raw[m.end():]) if m else ("", raw)
        new = transform(body)
        # 断言
        if m is None:
            errs.append((p, "无 frontmatter"))
            continue
        if new == body:
            continue
        old_refs = sorted(IMGREF.findall(body))
        new_refs = sorted(IMGREF.findall(new))
        if old_refs != new_refs:
            errs.append((p, "图引用变动 %d→%d" % (len(old_refs), len(new_refs))))
            continue
        if sum(1 for _ in re.finditer(r'(?<!\$)\$(?!\$)', body)) % 2 != \
           sum(1 for _ in re.finditer(r'(?<!\$)\$(?!\$)', new)) % 2:
            errs.append((p, "$ 配对性变了"))
            continue
        poss = [new.find(h) for h in H2 if h in new]
        if len(poss) != 3 or poss != sorted(poss):
            errs.append((p, "二级标题缺失/失序"))
            continue
        changed += 1
        if len(samples) < 40:
            samples.append((p, body, new))
        if apply:
            io.open(p, "w", encoding="utf-8", newline="\n").write(fm + new)

    print("扫描卡 %d ；需改 %d ；断言失败 %d" % (len(cards), changed, len(errs)))
    for p, e in errs[:20]:
        print("   ⛔", os.path.relpath(p, BASE), e)
    print("=" * 70)
    for k in sorted(ST):
        print("   %-20s %d" % (k, ST[k]))
    if show:
        print("=" * 70)
        for p, a, b in samples[:14]:
            print("\n### %s" % os.path.relpath(p, BASE))
            d = [l for l in difflib.unified_diff(a.split("\n"), b.split("\n"),
                                                 lineterm="", n=0)][:26]
            for l in d:
                print("   " + l[:150])
    print("模式：", "APPLY（已写盘）" if apply else "dry-run")
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())
