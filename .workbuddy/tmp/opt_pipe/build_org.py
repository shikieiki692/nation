# -*- coding: utf-8 -*-
"""初赛模拟卷 X（非有机）——机构模拟题 2025~2026 版组卷器。

与 build_multi.py（教材题源）的差异：
- 源 = 04-题库/2026机构初赛模拟题（13 机构），限定 2025~2026（第39/40届 + 显式2025/2026）
- 机构卡**无 used_in** ⇒ 系列去重只靠 vol_plan（不做 used_in 回填）
- 答案区是「题面↔答案逐小问交错」⇒ 新增 strip_q_echo() 剥离题面回显
- 券末清单用**格式 C**（卷内题号|题名|题卡|来源|模块|难度|分值），题卡列**纯短名**
用法：python build_org.py [--check|--apply]
"""
import re, sys, os, glob, collections, json, difflib
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))   # .workbuddy/tmp（mv_extract/build_multi 所在）
import mv_extract as X
import build_multi as B          # 复用 renumber/strip_src_no/student_clean/vote_prefix/score_of/normalize_dd/esc 等
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "..", "11-模板", "scripts"))
try:
    import layout_figs as LF     # 多图组并排成表格（讲义/试卷通用）
except Exception:
    LF = None

ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)
BASE = '04-题库/2026机构初赛模拟题'
QB = '04-题库'
OUTdocx = os.path.join('00-首页', '题组Word', '初赛模拟卷')
SRCS = ['化英社', '清北营', 'chemy', '伽马', '壹尖培优', '汇智', 'XeChem', '质心GChO', '质心UChO', '方圆', '一式', '北京夏令营', '2ChO']
VOL = 'X'
JIE = re.compile(r'第\s*(\d+)\s*届')
PLACEHOLDER = re.compile(r'⛔|源池(无|仅|未见)|未录入|未定位|待人工核'
                         r'|文字化需人工转录|已随卡|源卷答案|答案出处[：:]'
                         r'|文字层自动提取|未逐字校对|答案（源 ?PDF')
# 题面泄露闸：源卡「题面区」若含答案/讲稿内容（化英社 HYS-02 参考答案稿、伽马讲稿批次），
# 直接弃卡——这类泄露无法可靠清洗（题面↔解答逐小问交错）。
# 假结构式闸：OCR 把**结构式/竖排标签**塞进 `\begin{array}` 转成 ASCII 骨架
# （如 `\text{O} \\ | \\ \text{NH}`、`X \\ | \\ Cu^{II} \\ | \\ ...`）⇒ 渲染必乱且无法用正则还原。
# 判据要点：**骨架符号 `|` `/` 出现在行首或行尾**（LaTeX 命令以 `\` 开头，故不会误伤 `\downarrow`/`\mu` 等）。
ARR_FAKE = re.compile(r'\\begin\{array\}(?:\{[^}]*\})?(.*?)\\end\{array\}', re.S)


def has_fake_struct(a):
    for body in ARR_FAKE.findall(a):
        for l in [x.strip() for x in re.split(r'(?<!\\)\\\\', body) if x.strip()]:
            if re.fullmatch(r'[|/]+', l):
                return True
            if re.match(r'^[|/]', l) and len(l) < 60:
                return True
            if re.search(r'[|/]$', l) and len(l) < 60 and re.search(r'[\u4e00-\u9fffA-Za-z]', l):
                return True
    return False


LEAK = re.compile(
    r'```txt|（\s*\d+\s*分|\(\s*\d+\s*分|共\s*\d+\s*分|各\s*\d+\s*分|得\s*\d+\s*分|'
    r'解答\s*[:：]|答案\s*[:：]|回归计算得|代入数据得|'
    r'送大分|高中数学|不是重要考点|这一块需要|给出的答案全错|理清楚|'
    r'注意此题|请注意本题|希望我的|这题[^\n]{0,8}没救|黄金好|大声|记住这个|送分')
# 批次级排除：源为「讲稿」（授课脚本，题面混入讲解/口播）
BATCH_BAD = re.compile(r'讲稿')
QUOTA = [('元素与分析', '第一部分　元素化学与分析化学', 7),
         ('结构化学', '第二部分　结构化学', 5),
         ('化学原理', '第三部分　化学原理', 4)]
VOL_PREF = ['化英社', '清北营', 'chemy', '伽马', '壹尖培优', '汇智', 'XeChem']

# ── 图片判噪（规则化，可复现）────────────────────────────────────────────
# 背景：机构源 PDF 的**水印**（清北营「清」、化英社「教育」等）被建卡管线
# 单独抽成图片，混进题面/答案。人工哈希清单是「某次选题的快照」，选型一变即失效
# ⇒ 改为**按图内容规则判定**（实测校准：卷X 80+25 图）。
try:
    from PIL import Image as _PILImage
except Exception:                      # pragma: no cover
    _PILImage = None

IMG_IDX = {}
for _p in glob.glob(os.path.join(BASE, '*', 'images', '*')):
    IMG_IDX.setdefault(os.path.basename(_p), _p)

NOISE_DARK = 0.005     # 近黑像素占比 < 此值 ⇒ 纯浅灰水印（真图 ≥0.008）
NOISE_MIN_KB = 2.0     # 体积 < 此值 ⇒ 空图/损坏


def _dark_ratio(path):
    """近黑像素（<110/255）占比。真图有黑色线条 ⇒ 显著>0；纯浅灰水印 ⇒ ≈0。"""
    if _PILImage is None or not path or not os.path.exists(path):
        return None
    try:
        im = _PILImage.open(path).convert('L')
    except Exception:
        return None
    w, h = im.size
    small = im.resize((min(w, 200), min(h, 200)))
    px = list(small.getdata())
    n = len(px)
    return (sum(1 for v in px if v < 110) / n) if n else None


def noise_of(path):
    """返回判噪理由或 None。"""
    if not path or not os.path.exists(path):
        return None
    if os.path.getsize(path) / 1024 < NOISE_MIN_KB:
        return 'broken<%.1fKB' % NOISE_MIN_KB
    d = _dark_ratio(path)
    if d is not None and d < NOISE_DARK:
        return 'watermark(dark=%.3f)' % d
    return None


def in_2526(norm, sf):
    jie = [int(j) for j in JIE.findall(norm)]
    if any(j in (39, 40) for j in jie):
        return True
    t = norm + " " + os.path.basename(sf)
    return ("2025" in t or "2026" in t)


def strip_q_echo(q, a):
    """剥离答案区里的**题面回显**。

    源为「题面↔答案逐小问交错」，且回显文字与题面**常不完全一致**
    （实测「D 在-50°C就会分解」vs 题面「D 在 50°C 就会分解」）⇒ 必须**模糊匹配**。
    三层：① 字符间容空白的整段精确删 ② 段落级精确/包含 ③ 段落级 difflib 相似度 ≥0.82。
    """
    def nz(s):
        return re.sub(r'[#\s{}]', '', s)
    qsegs = [nz(p) for p in re.split(r'\n{2,}', q)]
    qsegs = [s for s in qsegs if len(s) >= 12]
    # ① 字符间容空白（治「黏连」回显）
    for seg in sorted(qsegs, key=len, reverse=True):
        try:
            a = re.compile(r'[ \t{}]*'.join(map(re.escape, seg))).sub('', a)
        except re.error:
            pass
    # ②③ 段落级
    keep = []
    for p in re.split(r'\n{2,}', a):
        pn = nz(p)
        if len(pn) >= 12:
            if any(pn in s or s in pn for s in qsegs):
                continue
            if len(pn) >= 40:
                best, br = None, 0.0
                for s in qsegs:
                    if abs(len(s) - len(pn)) > 0.5 * len(pn):
                        continue
                    r = difflib.SequenceMatcher(None, pn, s).ratio()
                    if r > br:
                        br, best = r, s
                if br >= 0.82:
                    continue
        keep.append(p)
    return re.sub(r'\n{3,}', '\n\n', '\n\n'.join(keep)).strip('\n')


def strip_src_heading(s):
    """剥开头的源卡标题 `### 第 N 题 题名（X分，占 Y%）`（⚠️ 题号有中文数字变体「第 四 题」）。"""
    lines = s.split('\n')
    i = 0
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    if i < len(lines) and re.match(r'^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题', lines[i].strip()):
        i += 1
        while i < len(lines) and lines[i].strip() == '':
            i += 1
        s = '\n'.join(lines[i:])
    return s


def flatten_subq_headings(s):
    """「小问写成 H2/H3 标题」（`## 1-2 …`）→ 纯文本（**内容保留**，仅去 `#`）。

    技能 §六.3 的坑：直接删标题会**整条丢小问**。
    """
    return re.sub(r'(?m)^#{2,4}\s*(\d{1,2}\s*-\s*\d{1,2}(?:\s*-\s*\d+)?\s*[^\n]*)$', r'\1', s)


def drop_empty_headings(s):
    return re.sub(r'(?m)^#{1,6}[ \t]*$', '', s)


def renumber2(text, new_no, prefix):
    """重编号（兼容源卡把小题写成 `6- 2- 1` 的**间距变体**，原 renumber 只认 `6-2-1`）。"""
    if prefix is None:
        return text
    p = str(prefix)
    # 加粗三级/二级
    text = re.sub(r'\*\*\s*' + p + r'\s*[-.．]\s*(\d{1,2})\s*[-.．]\s*(\d{1,2})\s*\*\*',
                  lambda m: '**%d-%s-%s**' % (new_no, m.group(1), m.group(2)), text)
    text = re.sub(r'\*\*\s*' + p + r'\s*[-.．]\s*(\d{1,2})\s*\*\*',
                  lambda m: '**%d-%s**' % (new_no, m.group(1)), text)
    # 裸三级（先做，含间距变体）
    text = re.sub(r'(?<![\w\d.])' + p + r'\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})(?![\w\d.])',
                  lambda m: '%d-%s-%s' % (new_no, m.group(1), m.group(2)), text)
    # 裸二级
    text = re.sub(r'(?<![\w\d.])' + p + r'\s*-\s*(\d{1,2})(?![\w\d.]|-)',
                  lambda m: '%d-%s' % (new_no, m.group(1)), text)
    return text


def flatten_layout_tables(s):
    """「每行都是单格（colspan 占满）」的 HTML 表 → 逐行段落。

    这类表是**版面容器**（如 chemy/化英社答案把整段答案塞在 `<td colspan="3">` 里），
    不是数据表；转成 pipe table 会因列数多把长文字挤成窄列（实测挤成 1/3 宽）。
    ⚠️ 必须**先于** strip_q_echo 与 html_table_to_md 执行。
    """
    def rep(m):
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', m.group(0), re.S)
        cells = [re.findall(r'<t[dh][^>]*>.*?</t[dh]>', r, re.S) for r in rows]
        if not cells or any(len(c) != 1 for c in cells):
            return m.group(0)          # 有真多格行 ⇒ 数据表，交给 html_table_to_md
        out = []
        for c in cells:
            txt = re.sub(r'</?t[dh][^>]*>', '', c[0]).replace('<br>', '\n').replace('<br/>', '\n')
            txt = txt.strip()
            if txt:
                out.append(txt)
        return '\n\n' + '\n\n'.join(out) + '\n\n'
    return re.sub(r'<table>.*?</table>', rep, s, flags=re.S)


def _cell_clean(c):
    c = re.sub(r'<br\s*/?>', ' ', c)
    c = re.sub(r'<[^>]+>', '', c)
    c = c.replace('|', r'\|').strip()
    c = re.sub(r'\s+', ' ', c)
    return c


def html_table_to_md(s):
    """源卡的**行内 HTML `<table>`** → markdown 管道表。

    pandoc 不会把源 `<table>`（单行或多行）转成 docx 表格，只会把标签剥掉、
    每个单元格的文字竖排成行（实测「逻辑门真值表」渲成 28 行单个 0/1）。
    ⇒ 先转成原生 pipe table 再走 pandoc。

    🔴 三个坑（2026-10-06 用户报「表格是乱的」后修）：
    ① **rowspan 必须占位**，否则后续行的单元格**整体左移**（实测 7-6 的 A–E 错到 T 列下）；
    ② **colspan 展开后要丢「全空列」**——源常把 4 列语义表用 `colspan=3` 硬拉到 8 列，
       不丢空列 ⇒ Word 里出现大量空列（实测「立方晶系系统消光规律」表）；
    ③ **全跨度说明行**（`<td colspan=8>读图得到…</td>`）是新旧两张表的**分界** ⇒ 应作段落切段，
       否则两张语义无关的表被拼成一张。
    """
    TR = re.compile(r'<tr[^>]*>(.*?)</tr>', re.S)
    TC = re.compile(r'<t[dh]([^>]*)>(.*?)</t[dh]>', re.S)

    def emit(grid):
        grid = [r for r in grid if any(c for c in r)]
        if not grid:
            return ''
        ncol = max(len(r) for r in grid)
        grid = [r + [''] * (ncol - len(r)) for r in grid]
        keep = [j for j in range(ncol) if any(r[j] for r in grid)]   # ② 丢全空列
        grid = [[r[j] for j in keep] for r in grid]
        n = len(grid[0])
        # 🔴 首行首格是「小问号」⇒ 该行是**数据**（如 `| 14-6 | T | F | F | F | T |`），
        #    直接当表头会把它渲染成粗体表头、且语义颠倒。若次行是**短标签行**
        #    （且次行首格不是小问号），则交换两行 ⇒ 表头变成 `| A | B | C | D | E |`。
        if (len(grid) >= 2 and grid[0] and re.fullmatch(r'\d+(?:-\d+)+', grid[0][0].strip())
                and grid[1] and not re.fullmatch(r'\d+(?:-\d+)+', grid[1][0].strip())
                and all(len(c) <= 8 for c in grid[1] if c) and any(grid[1])):
            grid[0], grid[1] = grid[1], grid[0]
        # 单行表：源里大量 `<tr><td>4-1</td><td>…</td></tr>`（小问标签 + 该问答案），
        # 转成表格只会剩**一行表头**（粗体、无表体）⇒ 降级为「**标签** 内容」段落。
        if len(grid) == 1:
            ne = [c for c in grid[0] if c]
            first = (grid[0][0] if grid[0] else '').strip()
            if len(ne) <= 1:
                return ('\n\n**%s**\n\n' % first) if (first and len(first) <= 16) else '\n\n'
            if re.fullmatch(r'\d+(?:-\d+)+', first):
                rest = [c for c in grid[0][1:] if c]
                if not rest:
                    return '\n\n**%s**\n\n' % first
                if len(rest) == 1 and ('[[' in rest[0]):
                    return '\n\n**%s**\n\n%s\n\n' % (first, rest[0])
                return '\n\n**%s** %s\n\n' % (first, ' '.join(rest))
        out = ['| ' + ' | '.join(grid[0]) + ' |',
               '|' + '|'.join([':--:'] * n) + '|']
        for r in grid[1:]:
            out.append('| ' + ' | '.join(r) + ' |')
        return '\n\n' + '\n'.join(out) + '\n\n'

    def rep(m):
        tbl = m.group(0)
        grid, pending = [], {}
        for rm in TR.finditer(tbl):
            row, col = [], [0]

            def fillp():
                while col[0] in pending:
                    row.append('')
                    pending[col[0]] -= 1
                    if pending[col[0]] <= 0:
                        del pending[col[0]]
                    col[0] += 1

            fillp()
            for cm in TC.finditer(rm.group(1)):
                attrs, inner = cm.group(1), cm.group(2)
                csm = re.search(r'colspan\s*=\s*"?(\d+)"?', attrs)
                rsm = re.search(r'rowspan\s*=\s*"?(\d+)"?', attrs)
                cs = int(csm.group(1)) if csm else 1
                rs = int(rsm.group(1)) if rsm else 1
                row.append(_cell_clean(inner))
                row.extend([''] * (cs - 1))
                if rs > 1:                                    # ① rowspan 占位
                    for k in range(cs):
                        pending[col[0] + k] = rs - 1
                col[0] += cs
                fillp()
            grid.append(row)
        if not grid:
            return tbl
        ncol = max(len(r) for r in grid)
        grid = [r + [''] * (ncol - len(r)) for r in grid]
        # ③ 全跨度说明行 ⇒ 切段
        segs, cur = [], []
        for r in grid:
            ne = [c for c in r if c]
            if len(ne) == 1 and (len(r) - 1) >= max(1, ncol - 2):
                if cur:
                    segs.append(cur); cur = []
                segs.append([r])
            else:
                cur.append(r)
        if cur:
            segs.append(cur)
        parts = []
        for sg in segs:
            if len(sg) == 1 and len([c for c in sg[0] if c]) == 1:
                parts.append('\n\n%s\n\n' % [c for c in sg[0] if c][0])
            else:
                parts.append(emit(sg))
        return ''.join(parts)
    return re.sub(r'<table\b[^>]*>.*?</table>', rep, s, flags=re.S)


# 源卡 OCR 把 PDF 的**水印文字**也抓进来，成了 `> 清北营教育` 这类引用行
# （清北营卡实测 8 行）——纯噪音，会让答案里冒出一串无意义引用块。
WM_TEXT = re.compile(r'^(清北营教育|清北教育|清北营|化英社|北斗学友|致学教育|教育|ZCHEM|ZChem)\s*$')


def drop_wm_text(s):
    out = []
    for l in s.split('\n'):
        t = l.strip()
        if t.startswith('>'):
            body = t.lstrip('>').strip().strip('*_ ').strip()
            if WM_TEXT.match(body):
                continue
        out.append(l)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out))


def fix_tex(s):
    """texmath / tex_math_dollars 的渲染修复。

    ① `\\sf`（sans-serif）texmath 不支持 ⇒ 删。
    ② **行内公式两端禁空格**：`$ 2\\text{Na}_2…$` 这种「`$` 后紧跟空格」pandoc 不认 ⇒ 印字面 `$`。
       （实测答案表单元格里 1 处）
    ③ **`\\begin{array}` 的对齐符 `&`**：OMML 没有「对齐点」概念 ⇒ texmath 把 `&` 当字面字符，
       卷面上印出 `&6Ta+8KOH…`（实测题1 答案 3 处）。⇒ 降级为空格（内容与 `\\\\` 分行都保留，
       只是不再对齐；实测 `gathered/aligned` 会**丢掉分行**，不可用）。
    """
    s = re.sub(r'\\sf\b\s*', '', s)

    def _dearray(m):
        return (r'\begin{array}' + (m.group(1) or '')
                + m.group(2).replace('&', ' ') + r'\end{array}')
    s = re.sub(r'\\begin\{array\}(\{[^}]*\})?(.*?)\\end\{array\}', _dearray, s, flags=re.S)

    def _pad(m):
        return '$' + m.group(1).strip() + '$'
    return '\n'.join(re.sub(r'\$([^$\n]{1,400}?)\$', _pad, l) for l in s.split('\n'))


SEP_ROW = re.compile(r'^\|[:\- |]+\|$')
SUBQ_ID = re.compile(r'\d+(?:-\d+)+')


def fix_orphan_tables(s):
    """把「只有表头+分隔符、没有表体」的单行管道表降级为段落。

    这类表在源卡里是 `<tr><td>4-1</td><td>…</td></tr>`（小问标签 + 该问内容），
    docx 里渲染成**只有一个粗体表头行的表格**——用户报的「表格格式有问题」。
    ⚠️ 抽取器（mv_extract）也会自己把 `<table>` 转成管道表，故必须在 **md 层**
    再兜一道，不能只在 HTML 分支处理。
    """
    lines = s.split('\n')
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if (l.strip().startswith('|') and i + 1 < len(lines)
                and SEP_ROW.match(lines[i + 1].strip())):
            nxt = lines[i + 2].strip() if i + 2 < len(lines) else ''
            if not nxt.startswith('|'):
                cells = [c.strip() for c in re.split(r'(?<!\\)\|', l.strip().strip('|'))]
                ne = [c for c in cells if c]
                first = cells[0] if cells else ''
                if len(ne) <= 1:
                    out += (['**%s**' % first, ''] if first and len(first) <= 16 else [''])
                    i += 2
                    continue
                if cells and SUBQ_ID.fullmatch(first):
                    rest = [c for c in cells[1:] if c]
                    if len(rest) == 1 and '[[' in rest[0]:
                        out += ['**%s**' % first, '', rest[0], '']
                    else:
                        out += ['**%s** %s' % (first, ' '.join(rest)) if rest
                                else '**%s**' % first, '']
                    i += 2
                    continue
        out.append(l)
        i += 1
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out))


def clean_q(q):
    q = strip_src_heading(q)
    q = flatten_layout_tables(q)
    q = drop_empty_headings(q)
    q = flatten_subq_headings(q)
    q = strip_artifacts(q)
    q = fix_orphan_tables(q)
    q = fix_tex(q)
    return re.sub(r'\n{3,}', '\n\n', q).strip('\n')


def strip_artifacts(s):
    """清掉源卡 OCR 伪影（实测四类，均来自 PDF 版面元素被误抓）：

    ① 代码栅栏 ``` / ```txt —— 源把某个「方框区域」当成代码块，docx 里渲染成
       灰底等宽框（内容其实是正常答案文字）⇒ **只删栅栏行，保留内容**。
    ② 图片与文字**黏在同一行**（`3-6(共6分)![[a]]![[b]]`）⇒ 拆成独立段落，
       否则并排/缩放逻辑失效。
    ③ 图片行后紧跟的游离 `X`（源 PDF 的勾选框/记号）⇒ 删。
    """
    lines = s.split('\n')
    out = []
    for l in lines:
        if re.fullmatch(r'\s*```\w*\s*', l):       # ① 代码栅栏
            continue
        if not l.strip().startswith('|'):          # ② 行内图 → 独立段
            l = re.sub(r'[ \t]*(!\[\[[^\]]*\]\])[ \t]*', r'\n\1\n', l)
        for part in l.split('\n'):                 # ③ 图后游离 X（可能黏在图同一行尾）
            if re.fullmatch(r'\s*X\s*', part):
                prev = next((x for x in reversed(out) if x.strip()), '')
                if '[[' in prev:
                    continue
            out.append(part)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out))


def clean_a(a, q):
    a = strip_src_heading(a)
    a = flatten_layout_tables(a)
    a = strip_q_echo(q, a)
    a = drop_empty_headings(a)
    a = flatten_subq_headings(a)
    a = drop_wm_text(a)
    a = strip_artifacts(a)
    a = fix_orphan_tables(a)
    a = fix_tex(a)
    return re.sub(r'\n{3,}', '\n\n', a).strip('\n')


def conv_imgs(s):
    """机构卡图引用 `![](images/H.jpg)` / `<img src="images/H.jpg">` → `![[H.jpg]]`
    （系列口径＝纯哈希 wikilink，docx 管线据此解析）。"""
    s = re.sub(r'!\[[^\]]*\]\(\s*images/([^)\s]+)\s*\)', r'![[\1]]', s)
    s = re.sub(r'<img\s+[^>]*src="images/([^"]+)"[^>]*/?>', r'![[\1]]', s)
    return s



def desc_of(c):
    """题名：优先源卡 `### 第 N 题 题名（…）`；否则从**题面首句**摘（源 title/文件名
    常是建卡时截断的，如 `碳族元素需要得到或失去四个电`，不可直接用）。"""
    t = re.sub(r'^[\s.．·、,，;；:：\-]+', '', (c.get('title') or '').strip())
    if 4 <= len(t) <= 26 and not re.search(r'[，。；]', t):
        return t
    # 兜底 A：题面首句（到第一个句末标点；过长则在逗号处断，再退到空格/定长）
    q = re.sub(r'^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题[^\n]*\n',
               '', c.get('question', ''), flags=re.M)
    first = re.split(r'[。！？\n]', q.strip(), 1)[0].strip()
    first = re.sub(r'\$[^$\n]*\$', ' ', first)          # 去行内公式（题7 的 `$\mathrm{Cr}$`）
    first = re.sub(r'^[\s.．·、,，;；:：\-（(「『“"《]+', '', first)
    first = re.sub(r'\s+', ' ', first)
    if len(first) >= 6:
        seg = re.split(r'[，,；;]', first)[0].strip()
        # 掐掉「…具有/是指/可以…」这类谓语尾巴（题6：多核金(I)硫化物团簇**具有**丰富的…）
        seg = re.split(r'(?:具有|是指|是一类|可以|能够|可将|为一种|用于|用来)', seg)[0].strip() or seg
        if len(seg) > 20:
            head = re.split(r'\s+', seg)[0].strip()      # 中文题名常以空格分「主体 说明」
            seg = head if 6 <= len(head) <= 20 else seg[:14]
        seg = re.sub(r'[（(][^）)]*[）)]', '', seg).strip()   # 去括号注释（题7 的「（ :FAP）」残渣）
        return seg.rstrip('，,、 （(')
    # 兜底 B：文件名尾段
    nm = os.path.basename(c['path'])[:-3]
    s = re.sub(r'^题-[A-Za-z0-9]+-\d+-\d+-', '', nm)
    s = re.sub(r'^题-[A-Za-z0-9-]*?-\d+-', '', s)
    return s.strip('-_ ') or '综合推断题'


def build_pool():
    pool = collections.defaultdict(list)
    for rel in SRCS:
        for p in sorted(glob.glob(os.path.join(BASE, rel, '**', '题-*.md'), recursive=True)):
            t = open(p, encoding='utf-8').read()
            def g(k):
                m = re.search(r'^' + k + r':\s*(.*)$', t, re.M)
                return m.group(1).strip() if m else ''
            mod, stage, diff = g('subject_module'), g('exam_stage'), int(g('difficulty') or 0)
            src = g('source'); norm = g('source_norm'); sf = g('source_file')
            if not in_2526(norm, sf):
                continue
            if BATCH_BAD.search(norm):     # 「讲稿」批次＝授课脚本，题面混讲解
                continue
            if mod not in ('元素与分析', '结构化学', '化学原理') or stage == '省预赛':
                continue
            if diff < 4 or [x for x in B.RISK if x in t]:
                continue
            h1m = re.search(r'^#\s+(.+)$', t, re.M)
            h1 = h1m.group(1) if h1m else ''
            tn = re.sub(r'<!--.*?-->', '', t, flags=re.S)
            if B.is_cn_prelim(tn):
                continue
            if B.ORG_CHAP.search(src) or B.ORG_CHAP.search(h1):
                continue
            try:
                c = X.extract(p)
            except Exception:
                continue
            rawq, rawa = c['question'], c['answer']
            if PLACEHOLDER.search(rawa) or PLACEHOLDER.search(rawq):
                continue
            # ASCII 结构骨架闸：⚠️ **题面与答案都要查**（只查答案会漏掉题目区的图）
            if has_fake_struct(rawa) or has_fake_struct(rawq):
                continue
            # 「公式未转录」闸：题面含公式（$ ≥10）但答案**一个 $ 都没有**、且答案很长
            # ⇒ 源卡把公式当成乱码文本录入了（实测 HYS-01-07：`aFE (1-a)FEr^2=k2(1 OHCOO θOH)eRT`）。
            # 全库「答案 $==0」有 480 卡，其中多数是正常的纯文字答案，故必须叠加「题面含公式」条件。
            if len(rawa) >= 400 and rawa.count('$') == 0 and rawq.count('$') >= 10:
                continue
            # 题名：从源卡标题 `### 第 N 题 题名（…）` 取（清洗前抓，清洗会剥掉该行）
            # 源标题两种写法：`第 N 题 题名（分数）` 与 `第 N 题（分数）题名`；
            # 题号可能是中文数字（`第 四 题`），故一并支持。
            tm = re.search(
                r'^#{2,4}\s*第\s*[0-9一二三四五六七八九十]+\s*题\s*[.．、]?\s*'
                r'(?:[（(][^）)\n]*[）)])?\s*([^\n（(]{2,26}?)\s*(?:[（(]|$)',
                rawq, re.M)
            c['title'] = tm.group(1).strip() if tm else ''
            if c['title'] and LEAK.search(c['title']):   # 题名即讲稿口播 ⇒ 弃卡
                continue
            if len(re.sub(r'\s+', '', rawq)) < 60 or len(re.sub(r'\s+', '', rawa)) < 25:
                continue
            q0 = conv_imgs(clean_q(rawq))
            a0 = clean_a(conv_imgs(rawa), q0)
            q, a = html_table_to_md(q0), html_table_to_md(a0)
            if LEAK.search(q):        # 题面泄露（源卡缺陷）⇒ 弃卡
                continue
            qn = re.sub(r'\s+', '', q); an = re.sub(r'\s+', '', a)
            if len(an) < 25 or len(qn) < 60:
                continue
            if len(B.ORGRE.findall(q + ' ' + a)) >= 3:
                continue
            if len(re.findall(r'^\*\*\s*\d{1,2}\s*[.．]\s*\*\*', q + '\n' + a, re.M)) >= 8:
                continue
            c['question'], c['answer'] = q, a
            c['qlen'] = len(qn); c['src_dir'] = rel
            c['intl'] = B.is_intl(tn)
            c['imgs'] = re.findall(r'!\[\[([^\]\|]+)\]\]', q + a)
            # 去重指纹：剥掉 `### 第 N 题（…）` 表头（同题在不同批次里题号不同）
            q_fp = re.sub(r'^#{3,4}\s*第\s*\d+\s*题[^\n]*\n', '', q, count=1, flags=re.M)
            c['fp'] = re.sub(r'\s+', '', q_fp)[:120]
            pool[mod].append(c)
    return pool


def pick_vol(pool, used, max_per_src=4):
    picks = []
    per_src = collections.Counter()
    fps = set()
    for mod, _, need in QUOTA:
        by_src = collections.defaultdict(list)
        for c in sorted(pool[mod], key=lambda x: (-x['difficulty'], -x['qlen'])):
            if c['path'] in used:
                continue
            by_src[c['src_dir']].append(c)
        order = VOL_PREF + [s for s in SRCS if s not in VOL_PREF]
        got, r = [], 0
        while len(got) < need and r < 20:
            prog = False
            for s in order:
                if len(got) >= need:
                    break
                if per_src[s] >= max_per_src:
                    continue
                lst = by_src.get(s, [])
                if r < len(lst):
                    c = lst[r]
                    # 跨批次重复题（机构回收旧题）：同题只取一次
                    if c['fp'] in fps:
                        continue
                    got.append(c); used.add(c['path']); per_src[s] += 1
                    fps.add(c['fp']); prog = True
            if not prog:
                break
            r += 1
        picks.append((mod, got))
    return picks


def assign_scores(flat, target=150):
    """按题面长度比例赋分（机构题分值大，源分值=整卷口径不可直用），归一到 target。"""
    lens = [c['qlen'] for _, c, _ in flat]
    tot = sum(lens) or 1
    raw = [max(6, min(13, round(target * l / tot))) for l in lens]
    diff = target - sum(raw)
    i = 0
    while diff != 0 and i < len(raw) * 20:
        j = i % len(raw)
        if diff > 0 and raw[j] < 13:
            raw[j] += 1; diff -= 1
        elif diff < 0 and raw[j] > 6:
            raw[j] -= 1; diff += 1
        i += 1
    return {c['path']: s for (_, c, _), s in zip(flat, raw)}



def drop_noise_imgs(txt, noise):
    """剔除噪音图（水印/二维码/涂鸦/OCR 碎片）——人工目检哈希清单。

    全域替换（不只剥独立成行的）——噪音图也可能落在**表格单元格**里。
    """
    if not noise:
        return txt
    pat = re.compile(r'!\[\[(' + '|'.join(re.escape(h) for h in noise) + r')(?:\\?\|\d+)?\]\][ \t]*\n?')
    txt = pat.sub('', txt)
    txt = re.sub(r'(?m)^[ \t]*\|([ \t]*\|)+[ \t]*$', '', txt)   # 整行空表格行（全空单元格）
    return re.sub(r'\n{3,}', '\n\n', txt)


def load_noise():
    try:
        with open(os.path.join(HERE, 'noise_hashes.json'), encoding='utf-8') as f:
            return set(json.load(f)['union'])
    except Exception as e:
        print('  ⚠ load_noise 失败:', e)
        return set()


def write_vol(picks, flat, SC):
    total = sum(SC[c['path']] for _, c, _ in flat)
    orgs = sorted({c['src_dir'] for _, c, _ in flat})
    seg_start, seg_score, idx = {}, {}, 1
    for mod, got in picks:
        seg_start[mod] = (idx, idx + len(got) - 1); idx += len(got)
    for mod, got in picks:
        seg_score[mod] = sum(SC[c['path']] for c in got)
    n4 = sum(1 for _, c, _ in flat if c['difficulty'] == 4)
    n5 = sum(1 for _, c, _ in flat if c['difficulty'] == 5)
    modshort = {'元素与分析': '元素与分析', '结构化学': '结构化学', '化学原理': '化学原理'}

    ans, stu = [], []
    for tag, out in (('答案版', ans), ('学生版', stu)):
        is_ans = (tag == '答案版')
        out += ['---', 'title: 初赛模拟卷%s（非有机·%s）' % (VOL, tag), 'type: 题组',
                'role: 竞赛模拟训练卷', 'created: 2026-10-06', 'updated: 2026-10-06',
                'tags: [化竞, 模拟卷, 初赛, 非有机, 多源, 机构模拟题]',
                'source: ' + ('题库多家机构合编' if not is_ans else
                              B.esc('题库多家机构合编（含 ' + '、'.join(orgs) + '）')),
                'source_category: 竞赛导向·竞赛教辅', 'exam_stage: 初赛',
                'question_count: %d' % len(flat), '满分: %d' % total, '---', '',
                '# 初赛模拟卷 %s（非有机 · %s）' % (VOL, tag), '']
        segtxt = '、'.join('%s（第 %d–%d 题，%d 分）' % (lbl, seg_start[m][0], seg_start[m][1], seg_score[m])
                          for m, lbl, _ in QUOTA)
        prev = ', '.join('[[04-题库/初赛模拟卷%s（非有机·答案版）|卷 %s]]' % (x, x) for x in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'])
        if is_ans:
            out += ['> **组卷口径**：16 题跨 **%d 个来源机构**抽取（%s），全部取自各机构 '
                    '**2025~2026 年最新批次**（第39/40届 ＋ 2026 年班次）；均满足 `difficulty≥⭐⭐⭐⭐`、'
                    '`fidelity=原书逐字`；**已剔除全部有机化学题与国内初赛真题**，与 %s 用题零重复。'
                    % (len(orgs), '、'.join(orgs), prev),
                    '> **范围**：' + segtxt + '，**满分 %d 分，建议用时 180 分钟**；'
                    '难度 ⭐⭐⭐⭐ ×%d、⭐⭐⭐⭐⭐ ×%d。' % (total, n4, n5),
                    '> 题卡溯源见卷末选题清单。']
        else:
            out += ['> **考试说明**：本卷共 16 题，满分 %d 分，建议用时 180 分钟。' % total,
                    '> **范围**：' + segtxt + '。',
                    '> 请将答案写在答题纸上，写出必要的推理与计算过程。']
        out += ['', '---', '']

        for mod, lbl, _ in QUOTA:
            got = dict(picks)[mod]
            out += ['## %s（第 %d–%d 题，共 %d 分）' % (lbl, seg_start[mod][0], seg_start[mod][1], seg_score[mod]), '']
            for i, c in enumerate(got, seg_start[mod][0]):
                sc = SC[c['path']]
                pre = B.vote_prefix(c)
                q = renumber2(B.strip_src_no(c['question'], pre), i, pre)
                a = renumber2(B.strip_src_no(c['answer'], pre), i, pre)
                out += ['### 第 %d 题（%d 分）%s' % (i, sc, desc_of(c) if is_ans else ''), '']
                if is_ans:
                    out += ['> 来源：%s｜难度 %s' % (c['source'] or c['src_dir'], c['stars'] or '—'), '']
                out += [q if is_ans else B.student_clean(q), '']
                if is_ans:
                    out += ['#### 答案', '', a, '']
                out += ['---', '']
        if is_ans:
            out += ['## 附：选题清单（题卡溯源）', '',
                    '| 卷内题号 | 题名 | 题卡 | 来源 | 模块 | 难度 | 分值 |',
                    '|:---:|---|---|---|---|:---:|:---:|']
            n = 0
            for mod, got in picks:
                for c in got:
                    n += 1
                    stem = os.path.basename(c['path'])[:-3]
                    out.append('| %d | %s | [[%s]] | %s | %s | %s | %d |' % (
                        n, desc_of(c), stem, c['src_dir'], modshort[mod], c['stars'] or '—', SC[c['path']]))
            out += ['', '合计 %d 分；难度 ⭐⭐⭐⭐ ×%d、⭐⭐⭐⭐⭐ ×%d；有机化学 0 题、真题 0 题；跨 %d 个来源机构。'
                    % (total, n4, n5, len(orgs)),
                    '> 难度星级取自题卡 `difficulty` 字段。**本库 `exam_stage` 字段不可信**，故本卷不按考段标注。', '']
        out.append('')

    # ── 判噪：规则判定（可复现）∪ 人工补充清单（仅对本次引用的图生效）──
    refs = set(re.findall(r'!\[\[([0-9a-fA-F]{64}\.[A-Za-z0-9]+)', '\n'.join(ans + stu)))
    rule_noise = {}
    for h in sorted(refs):
        why = noise_of(IMG_IDX.get(h))
        if why:
            rule_noise[h] = why
    manual = load_noise() & refs
    NOISE = set(rule_noise) | manual
    print('  ── 判噪 %d 图（规则 %d + 人工清单 %d）' % (len(NOISE), len(rule_noise), len(manual)))
    for h in sorted(rule_noise):
        p = IMG_IDX.get(h)
        inst = os.path.relpath(p, BASE).split(os.sep)[0] if p else '?'
        print('     %-24s %-22s %s' % ('[' + inst + ']', rule_noise[h], h[:16]))
    for tag, out in (('答案版', ans), ('学生版', stu)):
        txt = B.normalize_dd('\n'.join(out))
        n0 = len(re.findall(r'!\[\[', txt))
        txt = drop_noise_imgs(txt, NOISE)
        n1 = len(re.findall(r'!\[\[', txt))
        nb = nf = 0
        if LF:
            txt, nb, nf = LF.process(txt)
        p = os.path.join(QB, '初赛模拟卷%s（非有机·%s）.md' % (VOL, tag))
        open(p, 'w', encoding='utf-8', newline='\n').write(txt)
        print('  → %s：噪声剔 %d 图，并排 %d 组/%d 图' % (tag, n0 - n1, nb, nf))
    print('  → 卷 %s 已写出（%d 题 / %d 分 / %d 机构）' % (VOL, len(flat), total, len(orgs)))
    return flat


def main():
    mode = 'apply' if '--apply' in sys.argv else 'check'
    pool = build_pool()
    for m in pool:
        print('  pool[%s] = %d' % (m, len(pool[m])))
    used = set()
    picks = pick_vol(pool, used, max_per_src=4)
    flat = [(mod, c, i) for mod, got in picks for i, c in enumerate(got, 1)]
    SC = assign_scores(flat, target=150)
    total = sum(SC[c['path']] for _, c, _ in flat)
    orgs = sorted({c['src_dir'] for _, c, _ in flat})
    print('=' * 96)
    print('卷 %s  %d 题  满分 %d  机构 %d = %s' % (VOL, len(flat), total, len(orgs), '、'.join(orgs)))
    for mod, c, i in flat:
        hits = B.ORGRE.findall(c['question'] + ' ' + c['answer'])
        print('  %2d d%d q%-5d %2d分 前缀%-4s 图%-2d 有机%d [%-6s] %s'
              % (i, c['difficulty'], c['qlen'], SC[c['path']], B.vote_prefix(c),
                 len(c['imgs']), len(hits), c['src_dir'], desc_of(c)[:30]))
    if mode == 'apply':
        write_vol(picks, flat, SC)
        json.dump([[mod, [dict(path=c['path'].replace(os.sep, '/'), src_dir=c['src_dir'],
                               score=SC[c['path']]) for c in got]] for mod, got in picks],
                  open(os.path.join(HERE, 'vol_plan_X.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('  [plan] 已固化 vol_plan_X.json')


if __name__ == '__main__':
    main()
