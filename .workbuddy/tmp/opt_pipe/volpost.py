# -*- coding: utf-8 -*-
"""volpost.py —— 机构模拟卷「卷级后处理」通用工具（RMW · 幂等 · 可复核）。

【为什么有它】此前每出一卷都要重抄一份 `fix_xiii_fmt.py / fix_xiii_fmt2.py /
restructure_ans_XIII.py / fix_titles_XIII.py`（9 个硬编码脚本）—— 规则完全一致，
只有卷号不同。本工具把**规则库 + 驱动**一次固化，`--vol <任意卷>` 即可复用。

用法（在 `build_org --apply` 之后、出 docx 之前）：
  python volpost.py --vol XII --diag                 # 只读：卷卡 + 卷 md 的缺陷形态扫描
  python volpost.py --vol XII --fmt   [--apply]      # 源卡格式规范化（不改正文语义）
  python volpost.py --vol XII --ans   [--apply]      # 卷 md 答案区结构优化（题号对齐/去重述）
  python volpost.py --vol XII --titles cfg.json [--apply]   # 卷 md 题名人工修正（配置驱动）
  python volpost.py --vol XII --all   [--apply]      # 顺序执行 fmt → ans

纪律：① 任何写盘前先 `shutil.copy2` 备份到 `volpost_bak_<vol>_<step>/`；
      ② 写盘前对同一输入重算一次，逐字节复核；③ CRLF 文件跳过并报警；
      ④ 幂等 —— 重跑第二次应报「0 处」。
"""
import argparse
import difflib
import io
import json
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")

R = r"C:\Obsidion\妙妙屋"
OP = os.path.join(R, ".workbuddy/tmp/opt_pipe")
CARD_FILE = None          # `--cards <清单>` 时由 main 设置


# ─────────────────────────── 路径解析 ───────────────────────────
def plan_cards(vol):
    """读 `vol_plan_<vol>.json` → 卷内卡相对路径列表。

    ★ 若设了全局 `CARD_FILE`（`--cards <清单>`），优先按该清单（每行一个相对路径）。
      用途：计划锁被覆盖/失效时，仍能对**指定卡**做后处理（不依赖池与计划）。
    """
    if CARD_FILE and os.path.isfile(CARD_FILE):
        return [l.strip() for l in io.open(CARD_FILE, encoding="utf-8") if l.strip()]
    p = os.path.join(OP, "vol_plan_%s.json" % vol)
    d = json.load(io.open(p, encoding="utf-8"))
    return [c["path"] for _m, lst in d for c in lst]


def md_path(vol):
    return os.path.join(R, "04-题库", "初赛模拟卷%s（非有机·答案版）.md" % vol)


def read(p):
    return io.open(p, encoding="utf-8-sig", newline="").read()


def write(p, t):
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)


# ─────────────────────────── 规则库（fmt）───────────────────────────
# 全部在**源卡**上跑；只做「错形 → 规范形」的等价替换，不动正文语义。
RULES = [
    # 标准态上标：\theta / \Theta / \circ 三种错形 → \ominus（前面不是数字，排除角度 30^{\circ}）
    ("std", re.compile(r"(?<![0-9])\s*\^\s*\{?\s*\\(?:theta|Theta|circ)\s*\}?"), r"^{\\ominus}"),
    # 无 `^` 的裸写法：`H_{m} \circ` ⇒ `H_{m}^{\ominus}`（仅当前面是 `}`）
    ("std2", re.compile(r"(?<=\})[ \t]*\\(?:theta|Theta|circ)\b"), r"^{\\ominus}"),
    # 饱和蒸气压标记：bullet / 裸星号 → \ast
    ("pstar_b", re.compile(r"p\s*_\s*\{?([AB])\}?\s*\^\s*\{?\s*\\bullet\s*\}?"), r"p_{\1}^{\\ast}"),
    ("pstar_s", re.compile(r"p\s*_\s*\{?([AB])\}?\s*\^\s*\*"), r"p_{\1}^{\\ast}"),
    # 单位
    ("u_kjmol_math", re.compile(r"/\\mathrm\{kJ\}/\\mathrm\{mol\}"), r"/\\mathrm{kJ}\\cdot\\mathrm{mol}^{-1}"),    ("u_kjmol_text", re.compile(r"\\text\{\s*kJ\s*/\s*mol\s*\}"), r"\\mathrm{kJ\\cdot mol^{-1}}"),
    ("u_kjmol_rm", re.compile(r"\\mathrm\{kJ\s*/\s*mol\}"), r"\\mathrm{kJ\\cdot mol^{-1}}"),
    ("u_jmolK", re.compile(r"\\mathrm\{J\s*/\s*\(\s*mol\s*K\s*\)\}"), r"\\mathrm{J\\cdot mol^{-1}\\cdot K^{-1}}"),
    ("u_kJ_mol", re.compile(r"\\mathrm\{kJ\}\s*\\mathrm\{mol\}"), r"\\mathrm{kJ\\cdot mol}"),
    # 表格标题单位（粗体/纯文本混排）
    ("u_paren_kjmol", re.compile(r"\(\s*kJ\s*/\s*mol\s*\)"), r"($\\mathrm{kJ\\cdot mol^{-1}}$)"),
    ("u_paren_jmolK", re.compile(r"\(\s*J\s*/\s*mol\s*[·・]\s*K\s*\)"), r"($\\mathrm{J\\cdot mol^{-1}\\cdot K^{-1}}$)"),
    # OCR 丢失：\mathrm{n} 实为 \ln
    ("lnfix", re.compile(r"\\mathrm\{n\}\s*(?=\\frac)"), r"\\ln "),
    # 下标用句点
    ("Vdotm", re.compile(r"\{\s*([pV])\s*\.\s*\\mathrm\{m\}\s*\}"), lambda m: "{%s,\\mathrm{m}}" % m.group(1)),
    ("pdotm", re.compile(r"\{\\mathrm\{\s*([pV])\s*\.\s*m\s*\}\}"), lambda m: "{\\mathrm{%s,m}}" % m.group(1)),
    # 评分标记：LaTeX 撇号形态 → 中文（分值可含小数点，如 0.5 分）
    ("sc1", re.compile(r"\(\s*([\d.]+)\s*\^?\s*\{\s*\\prime\s*\}\s*\)"), lambda m: "（%s 分）" % m.group(1)),
    ("sc2", re.compile(r"(?<![\^])([\d.]+)\s*\^\s*\{\s*\\prime\s*\}"), lambda m: "（%s 分）" % m.group(1)),
    ("sc3", re.compile(r"\(\s*([\d.]+)\s*'\s*\)"), lambda m: "（%s 分）" % m.group(1)),
    # ★ `$$` 必须独占一行（SOP 铁律二）：行首有内容、行尾为 `$$` ⇒ 拆为「内容 + 空行 + $$」。
    #   同行的 `$$` 不被识别为块级数学定界符，会让整段数学当字面文本（实测「字面 $」计数飙升）。
    ("split_ss", re.compile(r"(?m)^([^\n$][^\n]*?)[ \t]*\$\$[ \t]*$"), r"\1\n\n$$"),
]
# 在两区（题面 / 答案）都要跑的通用规则
ALWAYS = {"split_ss"}
# 🔴 评分标记规则**只在答案区**跑：`build_org.LEAK` 判据把「（N 分」视作**答案特征**，
#    若在题面区生成该形态 ⇒ 卡被判「题面泄露」⇒ **掉出池**（实测致 `题-GChO-03-02` 掉池、
#    plan-lock 失效、整卷重选）。此坑为格式工具与判据的交互缺陷，2026-10-08 实测。
SC_NAMES = {"sc1", "sc2", "sc3"}

# 评分标记括号/空格风格统一（单独实现：**只计真正变化的**，保证幂等）。
# 仅命中「括号内恰为 [共]N.N分」的形态 —— 不碰公式括号 (1)/(a)/\left(…\right)。
SC_RE = re.compile(r"[（(]\s*(共)?\s*([\d.]+)\s*分\s*[）)]")


def sc_norm(t, chg):
    n = 0

    def rep(m):
        nonlocal n
        prefix = (m.group(1) + " ") if m.group(1) else ""
        new = "（%s%s 分）" % (prefix, m.group(2))
        if new == m.group(0):
            return new                       # 已规范 ⇒ 不动、不计
        n += 1
        chg.append(("sc_norm", m.group(0), new))
        return new

    return SC_RE.sub(rep, t), n


# `\text{ \mathrm{X}}` 嵌套 ⇒ 去 `\text` 外壳。
# 🔴 texmath 不支持该嵌套 ⇒ **整个 `$…$` 被判为字面**（docx 里出现字面 `$`）。
TEXT_RM = re.compile(r"\\text\{\s*(\\mathrm\{.+?\})\s*\}")


def unwrap_text(t, chg):
    """去 `\text{ \mathrm{…}}` 的 `\text` 外壳（须在「裸 kJ/mol」替换**之后**跑）。"""
    n = 0

    def rep(m):
        nonlocal n
        n += 1
        chg.append(("unwrap_text", m.group(0), m.group(1)))
        return m.group(1)

    return TEXT_RM.sub(rep, t), n


def in_math(t, pos):
    """判断 pos 是否处于数学环境中。

    ⚠️ 必须先判**块级 `$$`**（`$$` 计数为奇数 ⇒ 在块内），再判行内 `$`。
       只数 `$` 会把 `$$…$$` 内的位置误判为「非数学」（`$$` 恰好 2 个 ⇒ 偶数），
       从而在块内插入 `$…$` ⇒ 破坏数学块（2026-10-08 实测：致 13 处**字面 `$`**）。
    """
    before = t[:pos]
    if before.count("$$") % 2 == 1:
        return True
    return before.replace("$$", "").count("$") % 2 == 1


# `$$` 块内被误插 `$` 的形态（`\mathrm{$\mathrm{…}$}`）⇒ 去内层 `$`。
NEST = re.compile(r"\\mathrm\{\s*\$([^$]*)\$\s*\}")


def fix_math_nesting(t, chg):
    """修复数学块内的多余 `$`（历史坏数据 + 兜底清理）。"""
    n = 0

    def rep(m):
        nonlocal n
        n += 1
        chg.append(("fix_nested_usd", m.group(0), m.group(1)))
        return m.group(1)

    t = NEST.sub(rep, t)

    def rep2(m):
        nonlocal n
        inner = m.group(1)
        if "$" in inner:
            n += inner.count("$")
            chg.append(("fix_block_usd", "$$●$$" if False else "$" * inner.count("$"), ""))
            inner = inner.replace("$", "")
        return "$$" + inner + "$$"

    return re.sub(r"\$\$(.*?)\$\$", rep2, t, flags=re.S), n


def fmt_text(t):
    """返回 (新文本, 处数, [(规则,旧,新)…])。

    ★ 分区：`## 参考答案` 之前为**题面区**，之后为**答案区**；
      评分标记类规则（`sc*`）**只在答案区**跑（见 `SC_NAMES` 注释的掉池坑）。
    """
    n, chg = 0, []
    m = re.search(r"(?m)^## 参考答案[ \t]*$", t)
    cut = m.end() if m else -1

    def apply_rules(seg, only_sc):
        nonlocal n
        for name, rx, rep in RULES:
            if name not in ALWAYS and (name in SC_NAMES) != only_sc:
                continue

            def _sub(mm, _rep=rep, _name=name):
                new = _rep(mm) if callable(_rep) else mm.expand(_rep)
                chg.append((_name, mm.group(0), new))
                return new
            seg, k = rx.subn(_sub, seg)
            n += k
        if only_sc:                       # sc_norm 同为评分规则 ⇒ 仅答案区
            seg, k = sc_norm(seg, chg)
            n += k
        return seg

    if cut > 0:
        head, tail = t[:cut], t[cut:]
        head, tail = apply_rules(head, False), apply_rules(tail, True)
        t = head + tail
    else:
        t = apply_rules(t, False)         # 无答案区（异常卡）：只做非评分规则
    # 残留裸写 kJ/mol：按是否在数学模式内分别处理（题面/答案均安全）
    out, last, k2 = [], 0, 0
    for mm in re.finditer(r"kJ\s*/\s*mol", t):
        out.append(t[last:mm.start()])
        out.append(r"\mathrm{kJ\cdot mol^{-1}}" if in_math(t, mm.start())
                   else r"$\mathrm{kJ\cdot mol^{-1}}$")
        chg.append(("u_kjmol_bare", mm.group(0), out[-1]))
        last = mm.end()
        k2 += 1
    out.append(t[last:])
    t2 = "".join(out)
    t2, k3 = fix_math_nesting(t2, chg)     # ★ 收尾：修复数学块内多余 `$`
    t2, k4 = unwrap_text(t2, chg)          # ★ 收尾：去 `\text{ \mathrm{…}}` 嵌套
    return t2, n + k2 + k3 + k4, chg


# ─────────────────────── 诊断（九类缺陷形态）───────────────────────
DIAG = [
    ("1 标态错形(LaTeX)", re.compile(r"\^\s*\{?\s*\\(?:theta|Theta|circ)\s*\}?|(?<=\})[ \t]*\\(?:theta|Theta|circ)\b")),
    ("2 单位连除", re.compile(r"/\\mathrm\{kJ\}/\\mathrm\{mol\}|kJ\s*/\s*mol|J\s*/\s*mol\s*[·・]?\s*K|\\mathrm\{J\s*/\s*\(")),
    ("3 评分标记裸写", re.compile(r"(?<![0-9（(])(\d+)\s*分(?![子])")),
    ("4 评分标记LaTeX撇", re.compile(r"\(\s*\d+\s*\^?\s*\{\s*\\prime\s*\}")),
    ("5 OCR残迹(dot/上0/断下标)", re.compile(r"\\dot\s*\{|\^\s*\{\s*0\s*\}(?![0-9.])|\{\s*\\ominus\s*\}\s*[a-zA-Z]\s*\(")),
    ("6 小问粘连(N-x紧跟数字)", re.compile(r"(?m)^\s*\d+-\d+\d+")),
    ("7 答案区源题号行", re.compile(r"(?m)^第\s*[0-9]+\s*题")),
    ("8 \\mathrm{n}应为ln", re.compile(r"\\mathrm\{n\}\s*(?=\\frac)")),
    ("9 bullet星号", re.compile(r"\^\s*\{?\s*\\bullet\s*\}?")),
]


def diag(vol):
    cards = plan_cards(vol)
    md = md_path(vol)
    print("=" * 96)
    print("【卷 %s】源卡 %d 张 —— 缺陷形态扫描（只读）" % (vol, len(cards)))
    print("=" * 96)
    for i, rel in enumerate(cards, 1):
        t = read(os.path.join(R, rel))
        a = re.search(r"^## 参考答案\s*\n(.*?)(?=^## 知识点映射|\Z)", t, re.S | re.M)
        seg = a.group(1) if a else ""
        hits = []
        for name, rx in DIAG:
            n_all, n_ans = len(rx.findall(t)), len(rx.findall(seg))
            if n_all:
                sample = rx.search(seg or t)
                ctx = t[max(0, sample.start() - 30):sample.end() + 16].replace("\n", "⏎")
                hits.append((name, n_all, n_ans, ctx))
        if hits:
            print("\n第%2d题 ← %s" % (i, os.path.basename(rel)[:56]))
            for name, na, nans, ctx in hits:
                print("   %-26s 全文%3d 答案区%3d  …%s…" % (name, na, nans, ctx[:96]))
    # 卷 md
    if os.path.isfile(md):
        t = read(md)
        print("\n" + "-" * 96)
        print("【卷 md】%s" % os.path.basename(md))
        for name, rx in DIAG:
            ms = list(rx.finditer(t))
            if ms:
                print("   %-26s %3d 处  例：%s" % (
                    name, len(ms), t[max(0, ms[0].start() - 26):ms[0].end() + 14].replace("\n", "⏎")[:90]))
        print("   引块「— 解析 —」= %d ；结构化解析「> **考点**」= %d"
              % (t.count("> —— 解析 ——"), t.count("> **考点**：")))
    else:
        print("\n（卷 md 不存在：%s）" % md)


def subq(vol):
    """卷 md 级：逐题列「题面小问号 / 答案小问号」，并报缺号（首问非 `N-1` 即缺）。"""
    md = md_path(vol)
    if not os.path.isfile(md):
        print("\n（卷 md 不存在，跳过小问核对）")
        return
    txt = read(md).replace("\r\n", "\n")
    blocks = list(re.finditer(r"(?m)^### 第 (\d+) 题[^\n]*\n", txt))
    print("\n" + "-" * 96)
    print("【卷 %s】小问编号核对（题面 vs 答案）" % vol)
    for k, b in enumerate(blocks):
        volno = int(b.group(1))
        s = b.end()
        e = blocks[k + 1].start() if k + 1 < len(blocks) else len(txt)
        body = txt[s:e]
        am = re.search(r"(?m)^#### 答案\s*\n", body)
        qpart = body[:am.start()] if am else body
        apart = body[am.end():] if am else ""
        qn = re.findall(r"(?m)^\s*(\d+-\d+(?:-\d+)*)", qpart)
        an = re.findall(r"(?m)^\s*(\d+-\d+(?:-\d+)*)", apart)
        head = qn[0] if qn else "-"
        warn = "" if (qn and qn[0] == "%d-1" % volno) else "  ⚠ 首问非 %d-1" % volno
        bad = sorted({x.split("-")[0] for x in an if x.split("-")[0] != str(volno)})
        warn2 = ("  ⚠ 答案区含源题号 %s" % bad) if bad else ""
        print("第%2d题  题面 %s%s" % (volno, qn[:14], warn))
        print("        答案 %s%s" % (an[:14], warn2))
        # 游离编号：题面/答案区中出现的、前缀 ≠ 卷内题号的 `N-x`（组卷重编号漏识别）
        free = []
        for m in re.finditer(r"(?<![\d\-])(\d+)-(\d+(?:-\d+)*)", qpart + "\n" + apart):
            if m.group(1) != str(volno):
                a = max(0, m.start() - 26)
                free.append((qpart + "\n" + apart)[a:m.end() + 10].replace("\n", "⏎"))
        if free:
            print("        ⚠ 游离编号 %d 处：" % len(free))
            for x in free[:6]:
                print("            …%s…" % x)


# ─────────────────────────── fmt 步骤 ───────────────────────────
def fmt_step(vol, apply_):
    cards = plan_cards(vol)
    bak = os.path.join(OP, "volpost_bak_%s_fmt" % vol)
    if apply_:
        os.makedirs(bak, exist_ok=True)
    tot = chg_files = eol_fixed = 0
    for rel in cards:
        fp = os.path.join(R, rel)
        raw = read(fp)
        # 工作区可能是 CRLF（建卡脚本遗留），而 `.gitattributes` 定 `*.md eol=lf`
        # ⇒ 规范化后写回 LF；因 git 比较的是规范化内容，diff 只显真实改动。
        eol_here = "\r\n" in raw
        if eol_here:
            raw = raw.replace("\r\n", "\n")
        new, n, chg = fmt_text(raw)
        if n == 0 and not eol_here:
            continue
        if fmt_text(raw)[0] != new:
            print("   [复核不通过]", os.path.basename(rel))
            continue
        if eol_here:
            eol_fixed += 1
            print("   [EOL 归一 CRLF→LF]", os.path.basename(rel))
        chg_files += 1
        tot += n
        print("   %-46s %3d 处  %d→%d" % (os.path.basename(rel)[:44], n, len(raw), len(new)))
        for name, o, nw in chg[:2]:
            print("        [%s] %r → %r" % (name, o[:34], nw[:34]))
        if apply_:
            shutil.copy2(fp, os.path.join(bak, rel.replace("/", "__")))
            write(fp, new)
    print("%s fmt：%d 卡 / %d 处" % ("(dry)" if not apply_ else "已写盘", chg_files, tot))


# `$$` 块内出现「小问号开头」的行（如 `7-4 \Delta H_L = …`）⇒ 在它前面断块。
# 必要性：源卡把几个小问的结果写在同一个 `$$` 块内，块内容超版心 ⇒ **右侧被裁**；
# 断块后每块独立居中显示，不再超宽。保护：含 `\begin{`（array/aligned）的块不拆。
QN_IN_BLOCK = re.compile(r"^\s*\d+-\d+(?=[\\\s]|$)")


def split_inner_qno(t):
    n = 0

    def rep(m):
        nonlocal n
        inner = m.group(1)
        if "\\begin{" in inner:
            return m.group(0)
        lines = inner.split("\n")
        if not any(QN_IN_BLOCK.match(l) for l in lines):
            return m.group(0)
        groups, cur = [], []
        for l in lines:
            if QN_IN_BLOCK.match(l) and cur:
                groups.append(cur)
                cur = [l]
            else:
                cur.append(l)
        if cur:
            groups.append(cur)
        if len(groups) <= 1:
            return m.group(0)
        n += len(groups) - 1
        return "\n\n".join("$$\n" + "\n".join(g).strip("\n") + "\n$$" for g in groups)

    return re.sub(r"\$\$(.*?)\$\$", rep, t, flags=re.S), n


def md_fix(t):
    """卷 md 层的最小修复：拆「行尾 `$$`」 + 修数学块内多余 `$`。

    必要性：组卷器会压缩空行 ⇒ 源卡里「`10-3-1` ⏎ `$$`」会被并成「`10-3-1$$`」，
    而同行 `$$` 不是块级定界符 ⇒ 整段数学当字面文本（SOP 铁律二）。
    """
    n, chg = 0, []
    for name, rx, rep in RULES:
        if name != "split_ss":
            continue
        t, k = rx.subn(rep, t)
        n += k
    t, k = fix_math_nesting(t, chg)
    t, k2 = unwrap_text(t, chg)
    t, k3 = split_inner_qno(t)             # 块内小问号 ⇒ 断块（防超宽被裁）
    return t, n + k + k2 + k3


# ─────────────────────────── ans 步骤 ───────────────────────────
CLEAN = re.compile(r"\$[^$\n]*\$|\\[a-zA-Z]+|\s+|[\[\]{}()（）,，。.、；;:：'\"`*_^~|<>/\\-]")


def norm(s):
    return CLEAN.sub("", s)


def ans_step(vol, apply_):
    md = md_path(vol)
    bak = os.path.join(OP, "volpost_bak_%s_ans" % vol)
    txt = read(md).replace("\r\n", "\n")
    blocks = list(re.finditer(r"(?m)^### 第 (\d+) 题[^\n]*\n", txt))
    if not blocks:
        print("未找到题块"); return
    out, stats, rep_cnt = [], 0, 0
    prev_end = 0
    for k, b in enumerate(blocks):
        volno = int(b.group(1))
        s = b.end()
        e = blocks[k + 1].start() if k + 1 < len(blocks) else len(txt)
        body = txt[s:e]
        am = re.search(r"(?m)^#### 答案\s*\n(.*?)(?=^> \*\*解析|^> —— 解析 ——|^---\s*$|\Z)", body, re.S)
        if not am:
            continue
        qpart, apart = body[:am.start()], am.group(1)
        qsub = {}
        for m in re.finditer(r"(?m)^\s*(\d+-\d+(?:-\d+)*)\s*[．.、]?\s*(.{6,140})$", qpart):
            qsub[m.group(1)] = norm(m.group(2))
        rows = list(re.finditer(r"(?m)^\s*(\d+)-(\d+(?:-\d+)*)\s*([^\n]*)$", apart))
        if not rows:
            out.append(txt[prev_end:e]); prev_end = e; continue
        srcpre = rows[0].group(1)
        new_ap, n_rep = apart, 0
        for m in reversed(rows):
            rest, tail = m.group(2), m.group(3)
            old_num, new_num = "%s-%s" % (srcpre, rest), "%d-%s" % (volno, rest)
            cand = [qsub[x] for x in (old_num, new_num) if x in qsub] or list(qsub.values())
            tn = norm(tail)
            sim = max((difflib.SequenceMatcher(None, tn, c).ratio() for c in cand), default=0)
            if tn and sim >= 0.70:
                rep, n_rep = "**%s**" % new_num, n_rep + 1
            else:
                rep = new_num + tail
            new_ap = new_ap[:m.start()] + rep + new_ap[m.end():]
        if new_ap != apart:
            stats += n_rep
            rep_cnt += 1
            body = body[:am.start(1)] + new_ap + body[am.end(1):]
        out.append(txt[prev_end:s]); out.append(body); prev_end = e
    out.append(txt[prev_end:])
    txt2 = "".join(out)
    txt2, k_md = md_fix(txt2)          # ★ 卷 md 层修复：拆行尾 `$$`、清块内多余 `$`
    if txt2 == txt:
        print("(无变化)")
        return
    if apply_:
        os.makedirs(bak, exist_ok=True)
        shutil.copy2(md, os.path.join(bak, os.path.basename(md)))
        write(md, txt2)
    print("%s ans：%d 题变动；重述转标签 %d 处；卷 md 修复 %d 处；文件 %d→%d 字"
          % ("(dry)" if not apply_ else "已写盘", rep_cnt, stats, k_md, len(txt), len(txt2)))


# ─────────────────────────── titles 步骤 ───────────────────────────
def titles_step(vol, cfg_path, apply_):
    md = md_path(vol)
    cfg = json.load(io.open(cfg_path, encoding="utf-8")) if cfg_path else {}
    txt = read(md)
    bak = os.path.join(OP, "volpost_bak_%s_titles" % vol)
    n, old = 0, txt
    for q, (a, b) in cfg.items():
        # 标题行：`### 第 N 题（…分）<题名>`
        pat = re.compile(r"(?m)^(### 第 %s 题（[^）]*）)" % q)  # noqa: N806
        m = pat.search(txt)
        if m and txt[m.end():].startswith(a):
            txt = txt[:m.end()] + b + txt[m.end() + len(a):]
            n += 1
        # 清单行：`| N | <题名> |`
        cell = "| %s | %s |" % (q, a)
        if cell in txt:
            txt = txt.replace(cell, "| %s | %s |" % (q, b))
            n += 1
    if n and apply_:
        os.makedirs(bak, exist_ok=True)
        shutil.copy2(md, os.path.join(bak, os.path.basename(md)))
        write(md, txt)
    print("%s titles：%d 处" % ("(dry)" if not apply_ else "已写盘", n))


# ─────────────────────────── patch 步骤 ───────────────────────────
def patch_step(vol, cfg_path, apply_):
    """配置驱动的**精确串替换**（回源补漏行 / 断粘连），格式：
    {"<卡相对路径>": [[旧串, 新串], …]}   —— 命中数 0 会显式报警（防静默失效）。"""
    cfg = json.load(io.open(cfg_path, encoding="utf-8"))
    bak = os.path.join(OP, "volpost_bak_%s_patch" % vol)
    tot = miss = 0
    for rel, rules in cfg.items():
        fp = os.path.join(R, rel)
        raw = read(fp)
        eol = "\r\n" in raw
        t = raw.replace("\r\n", "\n") if eol else raw
        n = 0
        for old, new in rules:
            # ★ 幂等保护：插入型规则（新串含旧串）——若**替换后的完整串已存在**则跳过，
            #    否则二次运行会重复插入（本工具首版踩此坑；不能用「插入片是否在文中」判，
            #    插入片常是 `\n\n` 这种到处都有的空白）。
            if old in new:
                if new in t:
                    print("   [已存在·跳过]", os.path.basename(rel)[:40], repr(old[:26]))
                    continue
            elif new in t and old not in t:
                print("   [已应用·跳过]", os.path.basename(rel)[:40], repr(old[:26]))
                continue
            c = t.count(old)
            if c == 0:
                miss += 1
                print("   [未命中 ⚠]", os.path.basename(rel)[:40], repr(old[:34]))
                continue
            t = t.replace(old, new)
            n += c
        if n == 0 and not eol:
            continue
        if apply_:
            os.makedirs(bak, exist_ok=True)
            shutil.copy2(fp, os.path.join(bak, rel.replace("/", "__")))
            write(fp, t)
        tot += n
        print("   %-46s %d 处%s" % (os.path.basename(rel)[:44], n, "  [EOL→LF]" if eol else ""))
    print("%s patch：%d 处；未命中 %d" % ("(dry)" if not apply_ else "已写盘", tot, miss))


# ─────────────────────────── main ───────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vol", required=True)
    ap.add_argument("--diag", action="store_true")
    ap.add_argument("--subq", action="store_true")
    ap.add_argument("--fmt", action="store_true")
    ap.add_argument("--ans", action="store_true")
    ap.add_argument("--titles")
    ap.add_argument("--patch")
    ap.add_argument("--cards")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    global CARD_FILE
    CARD_FILE = a.cards
    if not (a.diag or a.subq or a.fmt or a.ans or a.titles or a.patch or a.all):
        a.diag = True
    if a.diag:
        diag(a.vol)
    if a.diag or a.subq:
        subq(a.vol)
    if a.fmt or a.all:
        print("\n### fmt（源卡）"); fmt_step(a.vol, a.apply)
    if a.ans or a.all:
        print("\n### ans（卷 md）"); ans_step(a.vol, a.apply)
    if a.titles:
        print("\n### titles（卷 md）"); titles_step(a.vol, a.titles, a.apply)
    if a.patch:
        print("\n### patch（源卡，配置驱动）"); patch_step(a.vol, a.patch, a.apply)


if __name__ == "__main__":
    main()
