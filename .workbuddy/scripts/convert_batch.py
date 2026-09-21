"""阶段3 批量转换：判断树 -> 嵌套列表；压平的流程步骤 -> 有序列表。

设计要点
- 只做这两类**可规则化**的转换；几何图/反应式/数据表一律跳过（留给人工或后续阶段）。
- 严格准入门槛：任何一行不符合模式就整块放弃（宁可漏，不可错）。
- 自测：用已手工转换过的「元素推断 L326-336 判断树」原文反推，必须复现出同样的列表。
- 应用时自下而上替换，逐文件断言 行数/CRLF 变化量，dry-run 为默认。

用法
  python convert_batch.py --selftest        # 校验解析器
  python convert_batch.py                   # 全库 dry-run，打印每块转换预览
  python convert_batch.py --apply           # 全库落盘
  python convert_batch.py --apply --only <子串>   # 只处理路径含该子串的文件
"""
import collections
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(r"C:\Obsidion\妙妙屋")
SRC = ROOT / "04-课件" / "学生讲义"
EXCLUDED_STEMS = {"README"}
EXCLUDED_PREFIXES = ("讲义升级模式-",)

TREE_CHARS = "├└┌┐└┘│─━┗┛┏┓╙╜╕╛"
ELBOW = "├└┌┐┗┛┏┓╙╜╕╛"          # 拐角符：有它才是真节点，只有 │ 竖线则是折行续写
RE_TREE = re.compile("[" + TREE_CHARS + "]")
RE_PREFIX = re.compile("^[" + TREE_CHARS + "\\s]*")
OPEN_RE = re.compile(r"^((?:\s{0,3}>\s?)*\s{0,3})(`{3,}|~{3,})\s*(\S*)\s*$")

# 纯序号前缀（可安全剥离，顺序由列表编号承担）
RE_ORDINAL = re.compile(
    r"^(?:Step\s*\d+\s*[:：.]?\s*"
    r"|步骤\s*\d+\s*[:：.]?\s*"
    r"|第\s*[一二三四五六七八九十\d]+\s*步\s*[:：.]?\s*"
    r"|\d+\s*[.、)]\s*"
    r"|[\u2460-\u2469]\s*)")
# 一行内压平的多个序号（用于拆分）
RE_INLINE_ORD = re.compile(r"(?=[\u2460-\u2469]\s)|(?<!\d)(?=\d+\s*[.、)])")

# ── 活性字符守卫：从"字符类一刀切"改为"精确模式" ────────────────────────
# 旧版 `[$`*\[\]\\<|]` 过严：化学里 `[配合物]`、`π*`、`-->`、`|` 都是普通文本，
# 一刀切把大量可转块挡在门外。改为只在**真正会被 markdown 解析**时才放弃。
RE_BAN_CODE = re.compile(r"`")                          # 行内代码
RE_BAN_MATH = re.compile(r"\$")                         # 数学（出块会改变 $ 奇偶口径）
RE_BAN_STRONG = re.compile(r"\*\*|__")                  # 加粗
RE_BAN_LINK = re.compile(r"!?\[\[|\[[^\]]*\]\s*[(\[]")  # wikilink / md 链接 / 图片
RE_BAN_HTML = re.compile(r"<[!a-zA-Z?/]|</")            # 残留 HTML 标签
RE_BAN_TBLSEP = re.compile(r"^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$")   # 表格分隔行
RE_BAN_SLASH = re.compile(r"\\")                        # 反斜杠（LaTeX 转义）
RE_BAN_STAR = re.compile(r"\*[^*\n]*\*")                # 成对的单星号 → 强调


def unsafe(txt: str):
    """返回放弃原因，或 None（安全）。txt 为整块文本（多行用 \\n 连接）。"""
    if RE_BAN_CODE.search(txt):
        return "含反引号"
    if RE_BAN_MATH.search(txt):
        return "含 $（出块会改变奇偶口径）"
    if RE_BAN_SLASH.search(txt):
        return "含反斜杠"
    if RE_BAN_STRONG.search(txt):
        return "含 **/__"
    if RE_BAN_STAR.search(txt):
        return "含成对单星号（会被解析为强调）"
    if RE_BAN_LINK.search(txt):
        return "含链接语法"
    if RE_BAN_HTML.search(txt):
        return "含 HTML 标签"
    for ln in txt.split("\n"):
        if RE_BAN_TBLSEP.match(ln) and "|" in txt:
            return "含表格分隔行且含竖线（会被解析为表格）"
    if RE_UNDERSCORE_BAD.search(txt):
        return "下划线出现在词边界（会被解析为强调）"
    return None


BANNED = RE_BAN_CODE       # 兼容旧调用点；真正的判定统一走 unsafe()
RE_ALIGN = re.compile(r"\S {2,}\S")        # 列对齐 = 有对齐意图
RE_BLOCKSTART = re.compile(r"^([-*+]\s|#{1,6}\s|>|\||\d+[.)]\s)")
RE_HR = re.compile(r"^[-=*]{3,}$")
# 下划线只在其"词内"时才是字面量（pandoc：词内 `_` 不触发强调）；出现在词边界会变成强调定界符
RE_UNDERSCORE_BAD = re.compile(r"(?<!\w)_|_(?!\w)")


LF = "\n"          # 字面换行常量（避免在 shell 内联里被转义吃掉）


def strip_cr(s: str) -> str:
    return s[:-1] if s.endswith("\r") else s


def active_md():
    out = []
    for p in sorted(SRC.rglob("*.md")):
        rel = p.relative_to(SRC)
        if "_归档" in rel.parts or rel.parts[0].startswith("_"):
            continue
        if p.stem in EXCLUDED_STEMS or p.stem.startswith(EXCLUDED_PREFIXES):
            continue
        out.append(p)
    return out


def comment_mask(lines):
    mask, inside = [False] * len(lines), False
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
    out, i, n = [], 0, len(lines)
    while i < n:
        m = OPEN_RE.match(lines[i])
        if not m or mask[i]:
            i += 1
            continue
        fence = m.group(2)
        close_re = re.compile(r"^(?:\s{0,3}>\s?)*\s{0,3}"
                              + re.escape(fence[0]) + r"{%d,}\s*$" % len(fence))
        body, j = [], i + 1
        while j < n and not close_re.match(lines[j]):
            body.append(lines[j])
            j += 1
        out.append((i + 1, (j + 1 if j < n else n), [strip_cr(x) for x in body]))
        i = j + 1 if j < n else n
    return out


# ─────────────────────── 转换器 ───────────────────────

def try_tree(nz):
    """判断树 -> 嵌套列表。返回 (new_lines, None) 或 (None, 原因)。"""
    if len(nz) < 3:
        return None, "行数<3"
    tree_lines = [l for l in nz if RE_TREE.search(l)]
    if len(tree_lines) < 2:
        return None, "树形符行<2"
    if len(tree_lines) / len(nz) < 0.6:
        return None, "树形符占比不足"
    _why = unsafe(LF.join(RE_PREFIX.sub("", l) for l in nz))
    if _why:
        return None, _why
    if any(RE_ALIGN.search(RE_PREFIX.sub("", l)) for l in nz):
        return None, "含列对齐空格"
    if any(l.lstrip().startswith(">") for l in nz):
        return None, "行首为引用符"

    def treepos(l):
        """行首前缀中**最后**一个树形符的列号；无则 None。

        关键：`│   └── x` 的层级由 `└` 决定，而不是行首那个 `│` ——
        取行首符会把嵌套整片压平（实测加成反应块塌成一层）。
        """
        m = RE_PREFIX.match(l)
        pref = m.group(0)
        idxs = [i for i, ch in enumerate(pref) if ch in TREE_CHARS]
        return (idxs[-1], l[m.end():].strip()) if idxs else (None, l.strip())

    def is_cont(l):
        """折行续写判定：有树形前缀、有文字，但前缀里**没有拐角符**。

        真节点形如 `│   ├── 文本`（前缀含 ├/└ 等拐角）；
        续写形如 `│   │       口诀："…"`（前缀只有 │ 竖线，文字属于上一节点）。
        注意不能判"最后一个树形符后是否接 ─" —— `─` 本身也在 TREE_CHARS 里，
        那样取到的末位是横线，会把所有正常节点误判成续写。
        续写会被当成独立节点且层级错乱 → 整块放弃交人工。
        """
        m = RE_PREFIX.match(l)
        pref = m.group(0)
        if not l[m.end():].strip():
            return False                      # 纯 `│` 间隔行
        if not any(ch in TREE_CHARS for ch in pref):
            return False                      # 无树形前缀
        return not any(ch in ELBOW for ch in pref)

    if any(is_cont(l) for l in nz):
        return None, "含折行续写（树形符后无 ─）"

    roots, items = [], []
    for l in nz:
        pos, text = treepos(l)
        if pos is None:
            if l != l.lstrip():
                return None, "存在缩进但无树形符的续行"
            if text:
                roots.append(text)
        elif text:                      # 纯 `│` 等"空树形符行"是间隔符，跳过而非报错
            items.append((pos, text))
    if not items:
        return None, "无有效树形分支"

    cols = sorted({p for p, _ in items})
    depth_of = {c: i for i, c in enumerate(cols)}
    base = 1 if roots else 0

    seq = []
    for l in nz:
        pos, text = treepos(l)
        if not text:
            continue
        seq.append(("root", text) if pos is None
                   else ("tree", depth_of[pos] + base, text))

    # 校验：每个 tree 层级的父级必须存在
    if roots and seq[0][0] != "root":
        return None, "首行为树行但存在根"
    out = []
    for it in seq:
        if it[0] == "root":
            out.append("- " + it[1])
        else:
            _, d, t = it
            out.append("  " * d + "- " + t)
    return out, None


def try_steps(nz):
    """压平的流程步骤 -> 有序列表。返回 (new_lines, None) 或 (None, 原因)。"""
    lines = [l.strip() for l in nz]
    _why = unsafe(LF.join(lines))
    if _why:
        return None, _why
    if any(RE_TREE.search(l) for l in lines):
        return None, "含树形符（应走 tree）"

    if len(lines) == 1 and len(re.split(r"(?=\d+\s*[.、)])", lines[0])) >= 3:
        lines = [p.strip() for p in re.split(r"(?=\d+\s*[.、)])", lines[0]) if p.strip()]

    texts = []
    for l in lines:
        if not RE_ORDINAL.match(l):
            return None, "有行未以序号开头"
        t = RE_ORDINAL.sub("", l).strip()
        if not t:
            return None, "序号后无文字"
        texts.append(t)
    if len(texts) < 2:
        return None, "步骤<2"

    out = []
    for i, t in enumerate(texts, 1):
        out.append("%d. %s" % (i, t))
    return out, None


def try_inline(nz):
    """去掉围栏 -> 普通段落（多行时每行各成一段，行间补空行）。

    只处理"无缩进、无列对齐、无活性字符"的块。**真结构式/对齐示意一律跳过**：
    形如 `Br` 折行、`H—OH` 竖排、`4000 3000 2000` 坐标轴之类的块都有缩进或列对齐，
    会被下面两条守卫拦下（matter：这类应该转图片或保留等宽，绝不能当正文）。
    """
    n = len(nz)
    if n > 8:
        return None, "行数过多"
    if n >= 2 and any(x != x.lstrip() for x in nz):
        return None, "多行块含缩进行（疑为对齐示意）"
    # 列对齐：只有"行尾单处注记对齐"才容忍（塌成单空格后仍可读）；
    # 一行里出现 ≥2 处 2+ 空格 = 多列布局（表格/坐标轴/多栏注记），放弃。
    if n >= 2:
        for x in nz:
            if len(RE_ALIGN.findall(x.strip())) > 1:
                return None, "多列对齐（疑为对齐示意图）"
    lines = [re.sub(r" {2,}", " ", x.strip()) for x in nz]
    if any(not l for l in lines):
        return None, "空行异常"
    _why = unsafe(LF.join(lines))
    if _why:
        return None, _why
    if any(RE_UNDERSCORE_BAD.search(l) for l in lines):
        return None, "含词边界下划线（会被解析成强调）"
    if any(RE_TREE.search(l) for l in lines):
        return None, "含树形符"
    for l in lines:
        if RE_BLOCKSTART.match(l) or RE_HR.match(l):
            return None, "行首会被解析为块级结构"
    out = []
    for i, l in enumerate(lines):
        if i:
            out.append("")
        out.append(l)
    return out, None


def try_table(nz):
    """「标签 + 数值」两列对齐块 → 真 md 表格。

    准入很严：≥3 行、**每行恰好一处 2+ 空格**、无缩进、无树形符、无活性字符、
    且**不含箭头**（含箭头说明是"条件→结论"式流程，用段落/列表更贴原意，不该做成两列表）。
    """
    if len(nz) < 3:
        return None, "行数<3"
    if any(x != x.lstrip() for x in nz):
        return None, "含缩进行"
    _why = unsafe("\n".join(nz))
    if _why:
        return None, _why
    if RE_TREE.search("\n".join(nz)):
        return None, "含树形符"
    if re.search(r"→|⟶", "\n".join(nz)):
        return None, "含箭头（应按流程处理）"
    cells = []
    for x in nz:
        parts = re.split(r" {2,}", x.strip())
        if len(parts) != 2:
            return None, "不是干净的 2 列"
        a, b = parts[0].strip(), parts[1].strip()
        if not a or not b:
            return None, "空单元格"
        if RE_BLOCKSTART.match(a) or RE_HR.match(a):
            return None, "首列行首会被解析为块级结构"
        cells.append((a, b))
    out = ["| 项 | 值 |", "|:--|:--|"]
    out += ["| %s | %s |" % (a, b) for a, b in cells]
    return out, None


def try_hfork(nz):
    """横向分叉：`┌─ 子 / 父──┼─ 子 / └─ 子` → 父 + 3 个子项。

    形态很固定：三行，`┌`/`┼`/`└` 三符**列号相同**，父标签写在中间 `┼` 行分支符之前。
    其它形状（如 `┌──┴──┐` 双分叉）一律不匹配 → 交给人工。
    """
    if len(nz) != 3:
        return None, "行数≠3"
    cols = []
    for l, ch in zip(nz, "┌┼└"):
        i = l.find(ch)
        if i < 0:
            return None, "缺 %s" % ch
        cols.append(i)
    if len(set(cols)) != 1:
        return None, "分支符未对齐"
    col = cols[0]
    parent = nz[1][:col].strip().rstrip("─").strip()
    if not parent:
        return None, "缺父节点标签"
    kids = []
    for l in nz:
        k = re.sub(r" {2,}", " ", l[col + 1:].strip().lstrip("─").strip())
        if not k:
            return None, "分支后无文字"
        _w = unsafe(k)
        if _w:
            return None, _w
        if RE_BLOCKSTART.match(k) or RE_HR.match(k):
            return None, "分支行首会被解析为块级结构"
        kids.append(k)
    out = ["- " + parent] + ["  - " + k for k in kids]
    return out, None


def try_step_tree(nz):
    """「序号主项 + 缩进子项」→ 嵌套列表；也覆盖"纯 ↓ 连接符"的竖向流程。

    典型：`① 引发：…` 下面缩进挂几条反应式；或 `材料/题干线索 / ↓ / 物理性质：… / ↓ / …`。
    """
    if len(nz) < 3:
        return None, "行数<3"
    txt = "\n".join(l.strip() for l in nz)
    if RE_TREE.search(txt):
        return None, "含树形符"
    _why = unsafe(txt)
    if _why:
        return None, _why
    if RE_UNDERSCORE_BAD.search(txt):
        return None, "含词边界下划线"
    roots = [l for l in nz if l == l.lstrip()]
    subs = [l for l in nz if l != l.lstrip()]
    if not roots or not subs:
        return None, "不是 主项+子项 结构"

    if not all(RE_ORDINAL.match(l.strip()) for l in roots):
        # 竖向 ↓ 流程：子项全是纯 ↓ 连接符 → 根做有序列表，丢掉 ↓；
        # 根自带 ①②③ 等序号时一并剥掉，避免与列表编号重复。
        if all(l.strip().strip("↓").strip() == "" for l in subs) and len(roots) >= 3:
            items = []
            for l in roots:
                t = RE_ORDINAL.sub("", l.strip()).strip()
                if not t:
                    return None, "根序号后无文字"
                items.append(t)
            return ["%d. %s" % (i, t) for i, t in enumerate(items, 1)], None
        return None, "主项不是序号行"

    out, cnt = [], 0
    for l in nz:
        if l == l.lstrip():
            cnt += 1
            t = RE_ORDINAL.sub("", l.strip()).strip()
            if not t:
                return None, "序号后无文字"
            out.append("%d. %s" % (cnt, t))
        else:
            t = l.strip()
            if not t:
                continue
            if RE_BLOCKSTART.match(t) or RE_HR.match(t):
                return None, "子项行首会被解析为块级结构"
            if RE_ALIGN.search(t):
                return None, "子项含列对齐"
            out.append("  - " + t)
    if cnt < 2:
        return None, "序号主项<2"
    return out, None


def try_indent_tree(nz):
    """「根 + 缩进子项」→ 两级嵌套列表（无树形符的那种，如 Frost 图要点）。"""
    if len(nz) < 3:
        return None, "行数<3"
    if nz[0] != nz[0].lstrip():
        return None, "首行缩进（不是根）"
    if any(l == l.lstrip() for l in nz[1:]):
        return None, "根之后仍有非缩进行"
    txt = "\n".join(l.strip() for l in nz)
    if RE_TREE.search(txt):
        return None, "含树形符"
    _why = unsafe(txt)
    if _why:
        return None, _why
    if RE_UNDERSCORE_BAD.search(txt):
        return None, "含词边界下划线"
    if any(RE_ALIGN.search(l.strip()) for l in nz[1:]):
        return None, "子项含列对齐"
    if any(RE_BLOCKSTART.match(l.strip()) or RE_HR.match(l.strip()) for l in nz[1:]):
        return None, "子项行首会被解析为块级结构"
    # 折行守卫①：子项里若有行以逗号/顿号/分号结尾 → 是跨行折行的同一句话，不是独立子项
    if any(l.strip().endswith(("，", ",", "、", "；", ";")) for l in nz[1:-1]):
        return None, "子项为跨行折行（非独立条目）"
    # 折行守卫②：整组子项就是"一个被折行的括号补充说明" → 也不是子项
    subs = [l.strip() for l in nz[1:]]
    if len(subs) >= 2 and subs[0][:1] in "（(" and subs[-1][-1:] in "）)":
        return None, "子项是折行的括号补充说明"
    out = ["- " + nz[0].strip()]
    out += ["  - " + l.strip() for l in nz[1:]]
    return out, None


# ─────────────────────── 自测 ───────────────────────

PILOT_TREE_OLD = [
    "题目现象 → 识别最强信号",
    "   ├─ 唯一性信号 → 直接锁定",
    "   ├─ 组合信号 → 列 2-4 个候选",
    "   └─ 单一信号 → 提取第二信号",
    "候选 → 用否定信息排除 → 剩余 ≤2？",
    "   ├─ 否 → 提取第三信号交叉验证 → 回到候选",
    "   └─ 是 → 反向验证：所有条件都能解释？",
    "            ├─ 否 → 回溯，重新识别信号（止损）",
    "            └─ 是 → 定价态 + 写关键方程式 → 完成",
]
PILOT_TREE_NEW = [
    "- 题目现象 → 识别最强信号",
    "  - 唯一性信号 → 直接锁定",
    "  - 组合信号 → 列 2-4 个候选",
    "  - 单一信号 → 提取第二信号",
    "- 候选 → 用否定信息排除 → 剩余 ≤2？",
    "  - 否 → 提取第三信号交叉验证 → 回到候选",
    "  - 是 → 反向验证：所有条件都能解释？",
    "    - 否 → 回溯，重新识别信号（止损）",
    "    - 是 → 定价态 + 写关键方程式 → 完成",
]


def selftest():
    got, why = try_tree(PILOT_TREE_OLD)
    ok = got == PILOT_TREE_NEW
    print("判断树自测：", "通过" if ok else "失败（%s）" % why)
    if not ok and got:
        for a, b in zip(got, PILOT_TREE_NEW):
            print("   ", "OK " if a == b else "DIFF", repr(a), "|", repr(b))
    steps = ["第一步 圈古文操作词：「煅」→高温加热；",
             "第二步 定位关键物质：雄黄=As₄S₄；",
             "第三步 按操作写方程式：把古文操作链翻译为现代化学反应"]
    g2, w2 = try_steps(steps)
    print("步骤自测：", "通过" if g2 == ["1. 圈古文操作词：「煅」→高温加热；",
                                       "2. 定位关键物质：雄黄=As₄S₄；",
                                       "3. 按操作写方程式：把古文操作链翻译为现代化学反应"] else "失败（%s）" % w2)
    if g2:
        for x in g2:
            print("    ", x)
    return 0 if ok else 1


# ─────────────────────── 主流程 ───────────────────────

def main(argv):
    if "--selftest" in argv:
        return selftest()

    only = None
    if "--only" in argv:
        only = argv[argv.index("--only") + 1]
    apply = "--apply" in argv

    plan, skipped = [], collections.Counter()
    kinds = collections.Counter()
    for p in active_md():
        rel = p.relative_to(SRC).as_posix()
        if only and only not in rel:
            continue
        lines = p.read_text(encoding="utf-8").split("\n")
        mask = comment_mask(lines)
        for ol, cl, body in scan_blocks(lines, mask):
            nz = [strip_cr(x) for x in body if strip_cr(x).strip()]
            if not nz:
                continue
            new, why = try_tree(nz)
            kind = "判断树"
            if new is None:
                new, why = try_steps(nz)
                kind = "流程步骤"
            if new is None:
                new, why = try_hfork(nz)
                kind = "横向分叉"
            if new is None:
                new, why = try_step_tree(nz)
                kind = "步骤+子项"
            if new is None:
                new, why = try_indent_tree(nz)
                kind = "根+缩进树"
            if new is None:
                new, why = try_table(nz)
                kind = "两列表格"
            if new is None:
                new, why = try_inline(nz)
                kind = "去围栏出块"
            if new is None:
                skipped[why] += 1
                continue
            plan.append({"file": rel, "open": ol, "close": cl,
                         "old": nz, "new": new, "kind": kind})
            kinds[kind] += 1

    print("可转换块：%d  （判断树 %d / 横向分叉 %d / 流程步骤 %d / 步骤+子项 %d / 根+缩进树 %d / 两列表格 %d / 去围栏出块 %d）"
          % (len(plan), kinds["判断树"], kinds["横向分叉"], kinds["流程步骤"],
             kinds["步骤+子项"], kinds["根+缩进树"], kinds["两列表格"], kinds["去围栏出块"]))
    print("跳过块：", dict(skipped))
    print()

    by_file = collections.defaultdict(list)
    for b in plan:
        by_file[b["file"]].append(b)
    print("涉及文件 %d 个：" % len(by_file))
    for f, blocks in sorted(by_file.items(), key=lambda x: -len(x[1])):
        print("  %2d 块  %s" % (len(blocks), f))
    print()

    # 预览
    for f, blocks in sorted(by_file.items()):
        for b in sorted(blocks, key=lambda x: x["open"]):
            print("── %s  L%d-%d  [%s]" % (f, b["open"], b["close"], b["kind"]))
            for x in b["old"]:
                print("   - " + x[:88])
            for x in b["new"]:
                print("   + " + x[:88])
            print()

    if not apply:
        print("[dry-run] 未落盘。加 --apply 执行。")
        return 0

    # 落盘：逐文件自下而上
    changed = []
    for f, blocks in by_file.items():
        p = SRC / f
        raw = p.read_text(encoding="utf-8", newline="")
        lines = raw.split("\n")
        n0, c0 = len(lines) - 1, raw.count("\r\n")
        want, want_crlf = 0, 0
        for b in sorted(blocks, key=lambda x: -x["open"]):
            i, j = b["open"] - 1, b["close"] - 1
            assert OPEN_RE.match(lines[i]), "%s L%d 不是围栏开启行" % (f, b["open"])
            assert OPEN_RE.match(lines[j]), "%s L%d 不是围栏关闭行" % (f, b["close"])
            got = [strip_cr(x) for x in lines[i + 1:j] if strip_cr(x).strip()]
            assert got == b["old"], "%s L%d 内容不符" % (f, b["open"])
            # 行尾跟随该块自身（有的文件是纯 LF，不能一律补 \r）
            eol = "\r" if lines[i].endswith("\r") else ""
            removed_crlf = sum(1 for x in lines[i:j + 1] if x.endswith("\r"))
            added_crlf = len(b["new"]) if eol else 0
            lanes = len(b["new"]) - (j - i + 1)
            lines[i:j + 1] = [x + eol for x in b["new"]]
            want += lanes
            want_crlf += added_crlf - removed_crlf
        new_raw = "\n".join(lines)
        n1, c1 = len(lines) - 1, new_raw.count("\r\n")
        assert n1 == n0 + want, "%s 行数异常 %d->%d(期望%+d)" % (f, n0, n1, want)
        assert c1 == c0 + want_crlf, "%s CRLF 异常 %d->%d(期望%+d)" % (f, c0, c1, want_crlf)
        p.write_text(new_raw, encoding="utf-8", newline="")
        assert p.read_text(encoding="utf-8", newline="") == new_raw, "%s 回读失败" % f
        changed.append((f, len(blocks), want))

    print("[applied] 文件 %d 个，块 %d 个" % (len(changed), sum(c[1] for c in changed)))
    for f, n, w in sorted(changed):
        print("   %2d 块  行数%+d  %s" % (n, w, f))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
