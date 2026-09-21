# -*- coding: utf-8 -*-
"""生成 A/C/D 待批清单报告（题源定位 + 建议写法）。只读扫描 + 写报告。"""
import os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"c:\Obsidion\妙妙屋")

BOOK = "04-课件/习题集/习题书-教师版"
QB = "04-题库"
OUT = "09-审计报告/习题书裸下标-ACD待批清单-2026-09-14.md"

SUB_UNI = "₀-₉₊₋₌₍₎ₐₑₒₓₔₕₖₗₘₙₚₛₜⁿ"
SUP_UNI = "⁰-⁹⁺⁻⁼⁽⁾ⁿ"
BODY = r"A-Za-z0-9()+\-−·/_%"
FIRSTCH = r"0-9A-Za-z()+\-−·θφλμνσπσΣΔΩ°½¼¾′″" + SUB_UNI + SUP_UNI
PAT = re.compile(r"(?<![\\$A-Za-z0-9])([A-Za-z][A-Za-z0-9]{0,14})([_^])(["
                 + FIRSTCH + r"][" + BODY + SUB_UNI + SUP_UNI + r"]{0,10})")
MEDIA_EXT = re.compile(r'\.(?:jpe?g|png|gif|webp|svg|bmp|tiff?|pdf|md|docx?|xlsx?|zip)(?:$|[|\])\s])', re.I)


def mask(line):
    out = list(line); i, n = 0, len(line)
    def blank(a, b):
        for k in range(a, min(b, n)):
            out[k] = ' '
    while i < n:
        ch = line[i]
        if ch == '`':
            j = line.find('`', i + 1)
            if j == -1:
                break
            blank(i, j + 1); i = j + 1; continue
        if line.startswith('$$', i) and not (i > 0 and line[i - 1] == '\\'):
            j = line.find('$$', i + 2)
            if j == -1:
                blank(i, n); break
            blank(i, j + 2); i = j + 2; continue
        if ch == '$' and not (i > 0 and line[i - 1] == '\\'):
            j = line.find('$', i + 1)
            if j == -1:
                i += 1; continue
            blank(i, j + 1); i = j + 1; continue
        if line.startswith('![[', i) or line.startswith('[[', i):
            j = line.find(']]', i)
            if j == -1:
                break
            blank(i, j + 2); i = j + 2; continue
        i += 1
    return ''.join(out)


def is_pathish(raw, a, b):
    word_re = re.compile(r'[A-Za-z0-9_\-./\\]+')
    wa, wb = a, b
    while wa > 0 and word_re.match(raw[wa - 1]):
        wa -= 1
    while wb < len(raw) and word_re.match(raw[wb]):
        wb += 1
    if MEDIA_EXT.search(raw[wa:wb]):
        return True
    def w(ch):
        return ch.isascii() and (ch.isalnum() or ch == '_')
    if (a > 0 and w(raw[a - 1])) or (b < len(raw) and w(raw[b])):
        return True
    return False


def cls(base, mark, sub):
    if mark == '^':
        return 'D'
    if re.search(r"[" + SUB_UNI + SUP_UNI + r"]", sub):
        return 'A'
    if re.fullmatch(r'[A-Za-z]', sub):
        return 'B'
    return 'C'


hits = []
files = []
for dp, dn, fn in os.walk(BOOK):
    if '_归档' in dp or '_archive' in dp or os.path.basename(dp).startswith('_'):
        continue
    for f in fn:
        if f.endswith('.md') and not f.startswith('README'):
            files.append(os.path.join(dp, f))
files.sort()

for p in files:
    lines = open(p, encoding="utf-8", errors="replace").read().split("\n")
    in_fence = in_fm = in_disp = False; fm_done = False
    for idx, raw in enumerate(lines, 1):
        s = raw.strip()
        if not fm_done:
            if idx == 1 and s == '---':
                in_fm = True; continue
            if in_fm:
                if s == '---':
                    in_fm = False; fm_done = True
                continue
        if s.startswith('```') or s.startswith('~~~'):
            in_fence = not in_fence; continue
        if in_fence: continue
        c_dd = s.count('$$')
        if c_dd:
            if c_dd % 2 == 1:
                in_disp = not in_disp; continue
            if in_disp:
                continue
        if in_disp: continue
        if s.startswith('<!--') or s.endswith('-->'): continue
        m = mask(raw)
        for mo in PAT.finditer(m):
            if is_pathish(raw, mo.start(), mo.end()):
                continue
            c = cls(mo.group(1), mo.group(2), mo.group(3))
            hits.append((c, p, idx, mo.group(0), mo.group(1), mo.group(2), mo.group(3), raw))

print("命中 %d 处 / %s" % (len(hits), dict(collections.Counter(h[0] for h in hits))))

# 题源索引（去空白）
IDX = []
for dp, dn, fn in os.walk(QB):
    if '_归档' in dp or '_archive' in dp or '元文件' in dp:
        continue
    for f in fn:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(dp, f)
        try:
            t = open(fp, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        IDX.append((fp, re.sub(r"\s+", "", t)))


def locate(raw, tok):
    """回溯题源：用逐级缩短的窗口做「去空白」匹配（长窗口会被行首改动打断）。"""
    pos = raw.find(tok)
    best = None
    for w in (24, 18, 14, 10, 7, 5):
        frag = re.sub(r"\s+", "", raw[max(0, pos - w): pos + len(tok) + w])
        if len(frag) < len(tok):
            continue
        found = [ip for ip, it in IDX if frag in it]
        if len(found) == 1:
            return found[0].replace("\\", "/")
        if found and best is None:
            best = found
    if best:
        return "%s  (等多候选 %d)" % (best[0].replace("\\", "/"), len(best))
    return None


def shape_of(raw):
    s = raw.strip()
    if s.startswith('#'):
        return "小标题（源自题源 title/文件名）"
    if re.match(r'^>\s*\*\*小问关联\*\*', s):
        return "小问关联块（wikilink 引用题源文件名）"
    if s.startswith('|') and s.endswith('|'):
        return "题源内的关联/速查表行"
    return "其它派生文本"


# 建议写法表（人工核对，key=唯一 token）
SUG = {
    # A：`_` + 已部分 Unicode 化的化学式 —— 须按基团拆
    "p_SO₂": (r"$p_{\mathrm{SO_2}}$", "高"),
    "p_H₂O": (r"$p_{\mathrm{H_2O}}$", "高"),
    "p_NH₃": (r"$p_{\mathrm{NH_3}}$", "高"),
    "p_O₂": (r"$p_{\mathrm{O_2}}$", "高"),
    "p_O₂/p": (r"$p_{\mathrm{O_2}}/p$", "中"),
    "p_CO₂": (r"$p_{\mathrm{CO_2}}$", "高"),
    "p_H₂": (r"$p_{\mathrm{H_2}}$", "高"),
    "p_N₂": (r"$p_{\mathrm{N_2}}$", "高"),
    "p_Cl₂/Torr": (r"$p_{\mathrm{Cl_2}}/\mathrm{Torr}$", "中"),
    "c_O₂": (r"$c_{\mathrm{O_2}}$", "高"),
    "c_O₂·": (r"$c_{\mathrm{O_2}}$·", "中"),
    "c_KOH/mol·dm⁻": (r"$c_{\mathrm{KOH}}/\mathrm{mol\cdot dm^{-3}}$", "中"),
    "e_g⁰": (r"$e_g^0$", "高"),
    "Y_ySₓ₋₂": (r"$Y_yS_{x-2y}$", "中"),
    # B：多字母基底
    "N_A": (r"$N_{\mathrm{A}}$", "高"),
    "Dq_t": (r"$Dq_t$", "中"),
    "RT_b": (r"$RT_b$", "中"),
    "UCl_b": (r"$\mathrm{UCl}_b$", "中"),
    "xUCl_a": (r"$x_{\mathrm{UCl}_a}$", "低"),
    "Ad_E": (r"$Ad_E$", "低"),
    # C：化学式 / 多字符
    "S_N2": (r"$S_{\mathrm{N}}2$", "高"),
    "S_N1": (r"$S_{\mathrm{N}}1$", "高"),
    "S_N2X": (r"$S_{\mathrm{N}}2$X", "低"),
    "J_PH": (r"$J_{\mathrm{PH}}$", "高"),
    "J_PH)": (r"$J_{\mathrm{PH}}$)", "高"),
    "J_CF": (r"$J_{\mathrm{CF}}$", "高"),
    "J_HH": (r"$J_{\mathrm{HH}}$", "高"),
    "J_HF": (r"$J_{\mathrm{HF}}$", "高"),
    "J_cis": (r"$J_{\mathrm{cis}}$", "高"),
    "J_trans": (r"$J_{\mathrm{trans}}$", "高"),
    "J_axial/axial": (r"$J_{\mathrm{axial/axial}}$", "中"),
    "k_obs": (r"$k_{\mathrm{obs}}$", "高"),
    "kc_NO": (r"$k_{c,\mathrm{NO}}$", "低"),
    "d_xy": (r"$d_{xy}$", "高"),
    "p_total": (r"$p_{\mathrm{total}}$", "高"),
    "p_total/2": (r"$p_{\mathrm{total}}/2$", "高"),
    "P_total/atm": (r"$P_{\mathrm{total}}/\mathrm{atm}$", "中"),
    "p_max": (r"$p_{\mathrm{max}}$", "高"),
    "p_max(1−e": (r"$p_{\mathrm{max}}(1-e^{\cdots})$", "低"),
    "p_CO/p": (r"$p_{\mathrm{CO}}/p$", "中"),
    "p_HCl/Torr": (r"$p_{\mathrm{HCl}}/\mathrm{Torr}$", "中"),
    "r_CO": (r"$r_{\mathrm{CO}}$", "高"),
    "r_CO/(": (r"$r_{\mathrm{CO}}/($", "低"),
    "t_break": (r"$t_{\mathrm{break}}$", "高"),
    "c_O−M": (r"$c_{\mathrm{O-M}}$", "低"),
    "c_NO·": (r"$c_{\mathrm{NO}}$·", "低"),
    "c_NO−M": (r"$c_{\mathrm{NO-M}}$", "低"),
    "A_xN_y": (r"$A_xN_y$", "高"),
    "M_av": (r"$M_{\mathrm{av}}$", "中"),
    "UCl_a)": (r"$\mathrm{UCl}_a$)", "中"),
    # D：上标
    "H^A": (r"$H^{\mathrm{A}}$", "高"),
    "H^B": (r"$H^{\mathrm{B}}$", "高"),
    "H^C": (r"$H^{\mathrm{C}}$", "高"),
    "H^D": (r"$H^{\mathrm{D}}$", "高"),
    "e^(−E/kT)": (r"$e^{-E/kT}$", "高"),
    "e^(−": (r"$e^{-(\cdots)}$", "低"),
    "N^N": (r"$N^{\mathrm{N}}$", "低"),
    "SO4^2-": (r"$\mathrm{SO_4^{2-}}$", "高"),
    "VO4^3-": (r"$\mathrm{VO_4^{3-}}$", "高"),
    "S^+": (r"$S^{+}$", "中"),
    "np^(n−1)": (r"$np^{n-1}$", "中"),
    "ns^n": (r"$ns^n$", "中"),
    "sp^2": (r"$sp^2$", "高"),
}

by = collections.defaultdict(list)
for h in hits:
    by[(h[0], h[3])].append(h)

out = []
out.append("# 习题书·正文裸下标「A / C / D 类」待批清单（2026-09-14）")
out.append("")
out.append("> 这批是 **A/B 类扫描（只查 `_{…}`/`^{…}`）查不到** 的形态：正文里裸写 `_`/`^`，")
out.append("> Word 中会字面显示下划线/尖号。B 类（单字母基底）已完成；本清单是剩余的 **需判断项**。")
out.append("")
out.append("**扫描口径**：遮蔽 frontmatter / 代码围栏 / code span / 行内与块级 `$…$` / `[[…]]` / HTML 注释；")
out.append("排除媒体文件名（路径护卫）。扫描对象：`04-课件/习题集/习题书-教师版`（学生版同源）。")
out.append("")
out.append("| 类 | 含义 | 处数 | 唯一 token |")
out.append("|---|---|---|---|")
for k, label in (('A', '`_` + 部分 Unicode 化化学式（半途转换）'),
                 ('B', '多字母基底（非单字母）'),
                 ('C', '化学式 / 多字符下标'),
                 ('D', 'ASCII 上标')):
    n = sum(1 for h in hits if h[0] == k)
    u = len(set(h[3] for h in hits if h[0] == k))
    out.append("| **%s** | %s | %d | %d |" % (k, label, n, u))
out.append("")
out.append("## 一、建议写法（按类）")
out.append("")
out.append("「置信度」= 是否可从上下文唯一确定；**低**者必须人工看原题。")
out.append("")
for k in ('A', 'B', 'C', 'D'):
    rows = sorted([(t, v) for (kk, t), v in by.items() if kk == k], key=lambda x: -len(x[1]))
    if not rows:
        continue
    out.append("### %s 类（%d 处 / %d 个 token）" % (k, sum(len(v) for _, v in rows), len(rows)))
    out.append("")
    out.append("| token | 处数 | 建议写法 | 置信度 |")
    out.append("|---|---|---|---|")
    for t, v in rows:
        sug, conf = SUG.get(t, ("—", "待定"))
        out.append("| `%s` | %d | `%s` | %s |" % (t, len(v), sug, conf))
    out.append("")
out.append("## 二、逐处明细（含题源定位）")
out.append("")
for k in ('A', 'B', 'C', 'D'):
    rows = sorted([(t, v) for (kk, t), v in by.items() if kk == k], key=lambda x: -len(x[1]))
    if not rows:
        continue
    out.append("### %s 类" % k)
    out.append("")
    for t, v in rows:
        sug, conf = SUG.get(t, ("—", "待定"))
        out.append("**`%s`** ×%d（%s）→ `%s`" % (t, len(v), conf, sug))
        out.append("")
        for c, p, idx, tok, base, mark, sub, raw in v:
            src = locate(raw, tok)
            pos = raw.find(tok)
            ctx = raw[max(0, pos - 40): pos + len(tok) + 40].strip()
            if src:
                out.append("- %s **L%d** ｜ …%s…" % (src, idx, ctx))
            else:
                out.append("- ⚠️ 未定位（%s）**L%d** ｜ …%s…" % (shape_of(raw), idx, ctx))
        out.append("")
out.append("## 三、特殊形态：题源文件名 / title 中的裸上标")
out.append("")
out.append("全库扫 `04-题库` + `04-课件/习题集` 的**文件名**与 **title 字段**，只命中 1 处：")
out.append("")
out.append("| 文件 | 内容 | 影响 |")
out.append("|---|---|---|")
out.append("| `04-题库/真题/第34届初赛/无机和结构化学/题-034-2-1-SO4^2-参与的释能反应方程式.md` "
           "| 文件名与 `title:` 均含 `SO4^2-` | 习题书 H2 标题印成 `## 2.62 SO4^2-参与的释能反应方程式（第34届初赛）`；"
           "另被多份 `小问关联` 以 `[[题-034-2-1-SO4^2-…]]` 引用 |")
out.append("")
out.append("**修法需拍板**：改 `title:` 字段即可让 Word 标题变干净（`$\\mathrm{SO_4^{2-}}$`），")
out.append("但**文件名**若一并改，会牵动全库 `[[题-034-2-1-SO4^2-…]]` 引用（题库 + exam 中间产物），")
out.append("需按「批量改名迁移」流程处理（先 `git ls-files` 查入库状态、再做引用扫描）。建议**只改 title**，文件名另议。")
out.append("")
out.append("## 四、执行约定")
out.append("")
out.append("1. **改在题源**（`04-题库/`），再重建习题书 md + 重导 docx（师/生两版 + 打印版）。")
out.append("2. 逐文件断言：行数不变、净 `$` 数偶、控制字符 0。")
out.append("3. 改动性质应为**最小**（插入 `$…$` 或替换下标写法），改动前后去 `$` 文本应可比对。")
out.append("4. 「低」置信度项**不得机械替换**，须对照原书/答案区。")
out.append("")

open(OUT, "w", encoding="utf-8").write("\n".join(out))
print("报告已写:", OUT, "(%d 行)" % len(out))
