# -*- coding: utf-8 -*-
"""第一轮·竞赛教材版分章练习：选题 + 成卷（教师版/学生版）。

    python gen_r1.py            # dry-run
    python gen_r1.py --write    # 落盘
"""
import os, re, io, sys, json, collections

ROOT = r"C:\Obsidion\妙妙屋"
CENSUS = os.path.join(ROOT, ".workbuddy/tmp/qb_census.json")
OUTDIR = os.path.join(ROOT, "04-课件", "习题集", "第一轮·竞赛教材版")
MEDIA = os.path.join(ROOT, "媒体仓库")
WRITE = "--write" in sys.argv
PER_SET, QUOTA = 25, {2: 2, 3: 15, 4: 8}   # 2026-09-17 三次调整：基础 3→2（未用基础题仅 139，
                                           # 要同时供 12 套综合套卷用，故专题卷让出 1 道/套给套卷）

# 已发给学生的结构化学第一轮卷 → 其题在回收时**最后考虑**（用户 2026-09-17 指示：
# 「允许回收，但避开结构化学第一轮已发的」）。其余已用题可正常回收。
RELEASED = ("结构化学专项卷", "结构化学阶段测试卷")

T = {"S1": "结构·1-原子结构", "S2": "结构·2-元素周期律", "S3": "结构·3-分子结构",
     "S4": "结构·4-晶体结构", "S5": "结构·5-配位化学", "S6": "结构·6-有机分子结构初探",
     "P1": "原理·1-化学计量与气体", "P2": "原理·2-溶液与相平衡", "P3": "原理·3-热力学初步",
     "P4": "原理·4-化学动力学", "P5": "原理·5-化学平衡", "P6": "原理·6-酸碱理论",
     "P7": "原理·7-沉淀溶解平衡", "P8": "原理·8-氧化还原与电化学", "P9": "原理·9-方程式与离子反应"}
ORDER = list(T.keys())

ZXG = {"原子": "S1", "分子": "S3", "晶体": "S4", "配位": "S5", "热力学": "P3",
       "动力学": "P4", "电化学": "P8", "基础": "P1"}
F1 = {"1": "P1", "2": "P9", "3": "P9", "4": "P3", "5": "S1", "6": "S2", "7": "S4",
      "8": "S3", "9": "S3", "10": "S4"}
F2 = {"1": "P4", "2": "P6", "3": "P7", "4": "P8", "5": "P8", "6": "S5"}
NL = {"1": "P1", "2": "P9", "3": "P9", "4": "P3", "5": "S1", "6": "S2", "7": "S4",
      "8": "S3", "9": "S4"}
NL2 = {"1": "P9", "2": "S1", "3": "S4", "4": "S5", "5": "P3", "6": "P4", "7": "P6"}
SH = {"水中平衡": "P6", "原子结构": "S1", "元素周期表与元素周期律": "S2", "共价键理论": "S3",
      "离子键与离子晶体": "S4", "金属键与金属晶体": "S4", "其他类型晶体": "S4",
      "晶体学基础": "S4", "配位化合物基础": "S5", "化学热力学基础": "P3",
      "化学反应能量变化": "P3", "化学平衡": "P5", "溶液和胶体": "P2", "电化学": "P8",
      "离子反应": "P9", "有机化学准备知识": "S6", "分子结构和性质": "S3",
      "化学动力学基础": "P4", "气体": "P1", "氧化还原反应": "P8"}
JC = {"原子结构": "S1", "量子力学": "S1", "共价键": "S3", "多原子分子": "S3",
      "对称性": "S4", "晶体结构": "S4", "金属晶体": "S4", "离子化合物": "S4",
      "配位化学": "S5"}
WJ = {"01": "P1", "02": "P3", "03": "P4", "04": "P5", "05": "S1", "06": "S3",
      "07": "S4", "08": "P6", "09": "P7", "10": "P8", "11": "S5"}
JS = {"原子结构": "S1", "分子结构": "S3", "晶体结构": "S4", "配合物": "S5",
      "反应方程式": "P9", "热力学和动力学初步": "P3", "溶液与化学分析": "P6"}
HZ = {"分子结构": "S3", "晶体结构": "S4", "配合物": "S5", "原子结构": "S1",
      "元素周期律": "S2", "化学平衡": "P5", "热力学": "P3", "动力学": "P4",
      "电化学": "P8", "酸碱": "P6", "沉淀": "P7", "化学计量": "P1", "反应方程式": "P9"}
ZJJ = {"群论": "S4", "配位立体化学": "S5", "配位化学": "S5", "对称性": "S4"}
SUB = {"原子结构": "S1", "元素周期表与周期性": "S2", "分子结构": "S3", "共价键理论": "S3",
       "晶体结构": "S4", "化学动力学": "P4", "化学平衡": "P5", "热力学与热化学": "P3",
       "电化学": "P8", "化学热力学基础": "P3", "化学动力学基础": "P4"}

# ── 通用主题兜底：submodule 关键词 → 15 主题键（2026-09-17 增补）────────────────
# 适用 真题（646）／北斗学友／二分册能力测试逐题／05-真题库／自编 等
# **无 source 专用分支**的源。**按序取首个命中**（长词在前，避免「沉淀溶解平衡」被「化学平衡」吞掉）。
# 不在本表的 submodule（元素化学／有机*／滴定分析／容量分析…）→ 返回 None，
# 即**按设计排除**：它们属「元素与分析／有机」模块，不属于第一轮（结构化学＋化学原理）范围。
ZT = [
    ("沉淀溶解平衡", "P7"), ("溶度积", "P7"), ("沉淀", "P7"),
    ("酸碱", "P6"), ("溶液中的平衡", "P6"),
    ("化学计量", "P1"), ("化学基础与计量", "P1"), ("气体", "P1"),
    ("溶液与相图", "P2"), ("相平衡", "P2"), ("相图", "P2"), ("胶体", "P2"),
    ("热力学", "P3"), ("热化学", "P3"), ("熵", "P3"),
    ("动力学", "P4"), ("反应速率", "P4"), ("反应级数", "P4"),
    ("化学平衡", "P5"), ("平衡常数", "P5"),
    ("电化学", "P8"), ("氧化还原", "P8"),
    ("方程式书写", "P9"), ("反应方程式", "P9"), ("离子反应", "P9"), ("离子方程式", "P9"),
    ("原子结构", "S1"), ("量子", "S1"),
    ("元素周期", "S2"), ("周期性", "S2"),
    ("分子结构与化学键", "S3"), ("分子结构", "S3"), ("共价键", "S3"),
    ("结构基础与波谱", "S3"), ("杂化", "S3"), ("VSEPR", "S3"),
    ("晶体结构", "S4"), ("晶体", "S4"), ("晶胞", "S4"),
    ("配位", "S5"), ("配合物", "S5"),
]


def sub_fallback(sub):
    s = (sub or "").strip().strip('"\'')
    if not s or s == "(空)":
        return None
    for kw, key in ZT:
        if kw in s:
            return key
    return None


# ── 05-真题库（真题讲评层）专用：该层**没有 `submodule` 字段**，但文件名自带学科+主题
#    （`真题-结构-Bragg方程-002`／`真题-物化-相平衡-001`）。按**最长键优先**匹配文件名。
#    不含任何键的（元素／分析／有机／自由基／过渡金属…）→ None，即域外排除。
F05 = [("Born-Haber", "P3"), ("晶体场", "S5"), ("配合物异构", "S5"), ("18电子规则", "S5"),
       ("Jahn-Teller", "S5"), ("反位效应", "S5"), ("化学动力学", "P4"), ("晶体结构", "S4"),
       ("氧化还原", "P8"), ("相平衡", "P2"), ("动力学", "P4"), ("热力学", "P3"),
       ("电化学", "P8"), ("酸碱", "P6"), ("配合物", "S5"), ("平衡", "P5"), ("结构", "S4")]


def fallback_05(basename):
    for kw, key in F05:
        if kw in basename:
            return key
    return None
MULTI = {("教材习题/高中化学竞赛教程第二分册", "1"): ["P4", "P5"],
         ("教材习题/高中化学竞赛教程第二分册", "2"): ["P6", "P2"],
         ("教材习题/化学能力测试", "2"): ["S1", "S3"],
         ("教材习题/化学能力测试", "7"): ["P6", "P7"],
         ("教材习题/无机化学例题与习题", "05"): ["S1", "S2"]}

FM = re.compile(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)
KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*)$")
ANS_STRONG = re.compile(r"^#{1,4}\s*(参考)?(答案|解答|解析)[^\n]*$", re.M)
ZUTI = re.compile(r"^\d+\.\d+-\d+\.\d+-")
IMG = re.compile(r"!\[\[([^\]]+)\]\]")
BLACK = ("普通化学原理", "高考")
# 选择题答案形态（`**答案：D**` / `答案:AB` / `BD` …）—— 2026-09-17 增补：
# 省预赛 240 题全为选择题，答案天然只有 1–2 个字母，此前被「答案≥15 字」整批拒收。
CHOICE_ANS = re.compile(r"^[^A-D]{0,8}[A-D]{1,5}[^A-D]{0,4}$")


def is_choice_ans(a):
    x = re.sub(r"[*\s。．.、（）()【】\[\]]", "", a or "")
    return bool(CHOICE_ANS.match(x)) and 0 < len(x) <= 12
# ⚠️ 2026-09-17 用户规则变更：**非竞赛教材（大学教材课后习题）只出现在「课后习题集」，
#   不进专项卷**。故本表只留竞赛导向来源；大学教材（结构化学基础/无机化学例题与习题/
#   中级无机化学/Weller/Clayden/无机化学第5版）由 prio() 直接排除（=99）。
WHITE = ("赵鑫光", "上海中学", "竞赛教程", "初赛讲义", "汇智", "ABOC", "Zchem")
# 非竞赛教材（大学教材课后习题）—— 一律不进专项卷
UNIV = ("结构化学基础", "无机化学例题与习题", "中级无机化学", "Weller", "Clayden", "无机化学第5版")
LEVMAP = {"竞赛": 0, "拓展": 1, "巩固": 2, "基础": 3}


def after(b, marker):
    i = b.find(marker)
    if i < 0:
        return None
    return (b[i + len(marker):].lstrip("-").split("-")[0]) or None


def route(r):
    p, d = r["_path"], r["_sub"]
    b = os.path.basename(p)[:-3]
    if d == "教材习题/赵鑫光":
        return ZXG.get(after(b, "赵鑫光") or "") or sub_fallback(r.get("submodule"))
    if d in ("教材习题/高中化学竞赛教程第一分册", "教材习题/高中化学竞赛教程第二分册"):
        m = re.search(r"-L(\d+)", b)
        if m:
            k = (d, m.group(1))
            hit = MULTI.get(k) or (F1 if "第一分册" in d else F2).get(m.group(1))
            if hit:
                return hit
        return sub_fallback(r.get("submodule"))
    if d in ("教材习题/一分册能力测试", "教材习题/化学能力测试"):
        m = re.search(r"-(Ch\d+)[AB]-", b)
        if m:
            k = (d, m.group(1)[2:])
            hit = MULTI.get(k) or (NL if "一分册" in d else NL2).get(m.group(1)[2:])
            if hit:
                return hit
        return sub_fallback(r.get("submodule"))
    if d == "教材习题/上海中学竞赛课程":
        return SH.get(after(b, "上海中学") or "") or sub_fallback(r.get("submodule"))
    if d == "教材习题/结构化学基础":
        return JC.get(after(b, "结构化学基础") or "") or sub_fallback(r.get("submodule"))
    if d == "教材习题/中级无机化学":
        return ZJJ.get(after(b, "中级无机化学") or "") or sub_fallback(r.get("submodule"))
    if d == "教材习题/无机化学例题与习题":
        m = re.search(r"(Ch\d\d)", p)
        if m:
            k = (d, m.group(1)[2:])
            hit = MULTI.get(k) or WJ.get(m.group(1)[2:])
            if hit:
                return hit
        return sub_fallback(r.get("submodule"))
    if d == "教材习题/化学竞赛初赛讲义":
        m = re.search(r"初赛讲义-([^-]+)-", b)
        hit = JS.get(m.group(1)) if m else None
        return hit or sub_fallback(r.get("submodule"))
    if d == "教材习题/汇智竞赛题目":
        return HZ.get(after(b, "汇智") or "") or sub_fallback(r.get("submodule"))
    if d == "教材习题/北斗学友":
        return sub_fallback(r.get("submodule"))
    if r["_path"].startswith("05-真题库/"):
        return fallback_05(os.path.basename(r["_path"]))
    # 真题（04-题库/真题/**，含初赛·决赛·省预赛）、05-真题库、自编章节题、二分册逐题 等：
    # 走 submodule 关键词兜底（2026-09-17 增补）
    return sub_fallback(r.get("submodule")) or SUB.get(r.get("submodule", ""))


def load(path):
    t = io.open(path, encoding="utf-8").read()
    m = FM.match(t)
    if not m:
        return None
    fm, cur = {}, None
    for raw in m.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        km = KEY.match(raw)
        if km:
            fm[km.group(1)] = km.group(2).strip()
            cur = km.group(1)
        elif raw.lstrip().startswith("-") and cur:
            fm[cur] = (fm.get(cur, "") + " " + raw.lstrip()[1:].strip()).strip()
    body = t[m.end():]
    ans, bq = "", body
    dd = re.search(r"<details>([\s\S]*?)</details>", body)
    if dd:
        ans = re.sub(r"<summary>[\s\S]*?</summary>", "", dd.group(1))
        bq = body[:dd.start()] + body[dd.end():]
    else:
        am = ANS_STRONG.search(body)
        if am:
            ans, bq = body[am.end():], body[:am.start()]
        else:
            am2 = re.search(r"^\*\*答案\*\*[：:]", body, re.M)
            if am2:
                ans, bq = body[am2.end():], body[:am2.start()]

    def clean(s, drop_h1):
        out = []
        for ln in s.splitlines():
            st = ln.strip()
            if re.match(r"^>\s*\*\*(来源|难度|教学层级|小问关联|关联小问|知识点映射)\*\*", st):
                continue
            # 源题自带的**未加粗**来源行（如 `> 来源：07-资料提炼/提炼-第36届初赛试题解析（第一场） | mineru/…`）
            # —— 2026-09-17 实测会整行漏进题面，学生版因此出现来源行（违反成品规则④）
            if re.match(r"^>\s*\**\s*(来源|选自|出处|原题|题源)\s*\**\s*[：:]", st):
                continue
            if re.match(r"^>\s*(⚠|🔁|💡)", st):
                continue
            if re.match(r"^>\s*\[!", st):
                continue
            if re.match(r"^>\s*(\*\*)?编辑|^>\s*\*\*忠实重录|^>\s*\*\*校勘", st):
                continue
            # 题库旧的 dataview「同大题小问」标记块（`### 🔗 同大题小问`）——
            # 04-题库/新题入库SOP 已明令不写该块；对 Word 无意义且含装饰 emoji（渲染不稳）→ 整行剔除。
            if "🔗" in st:
                continue
            if re.match(r"^#{1,6}\s*$", st):
                continue
            out.append(ln)
        s = "\n".join(out)
        # 清掉**图注型** HTML 折叠块（`<summary>natural_image|chemical|line chart</summary>`
        # 后面跟一段英文图形描述）—— 不是答案，属 OCR 图形标注噪声（2026-09-17 实测 16 处）。
        # 答案型折叠块（`📖 查看答案与解析`）在此之前已被 load() 单独抽出，不影响答案。
        s = re.sub(r"<details>[\s\S]*?</details>", "", s)
        # 剥离 HTML 注释（含跨行）：题库校勘注里常含 `$$` / `\frac` 等**字样**，
        # 会打乱 Word 预检的数学模式配对计数 —— 2026-09-17 实测「第一轮综合卷06 教师版」
        # 被误报 8 个 ERROR 而**阻断整批转换**（+ 学生版 1 个）。注释在 Obsidian 与 Word 中
        # 均不渲染 → 成品卷直接剥离。
        s = re.sub(r"<!--[\s\S]*?-->", "", s)
        # ── Word 预检兼容修复（2026-09-17）────────────────────────────
        # ① 源题正文常把平衡常数/分压商写成**裸下标**（`K_p`/`Q_p`/`K_sp`/`K_HL`），
        #    下游 Word 预检判 ERROR 并**阻断该文件的整批转换**（实测 5 文件 10 处）。
        #    只在**非数学段**包裹，避免破坏已有的 $...$ / $$...$$。
        segs = re.split(r"(\$\$[\s\S]*?\$\$|\$[^$\n]*\$)", s)
        for _i in range(0, len(segs), 2):
            segs[_i] = re.sub(
                r"(?<![\w$\\])((?:K|Q|C)_(?:p|v|sp|HL|c|a|b|w|x|\d))(?![A-Za-z0-9_{])",
                lambda m: "$" + m.group(1) + "$", segs[_i])
        s = "".join(segs)
        # ② OCR 偶把 `$…$` 的美元符吞掉，留下裸公式行 `[ \frac… ]`（实测 1 处）→ 补回 $$ 块；
        #    仅当行内确实含 LaTeX 宏时才动，避免误伤普通方括号文本。
        s = re.sub(r"(?m)^\[ ((?=[^\]]*\\[A-Za-z]).+?) \][ \t]*$",
                   lambda m: "$$ %s $$" % m.group(1), s)
        # ③ HTML 实体还原（`&lt;` → `<` 等），否则会原样印进 Word。
        s = (s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&"))
        # ④ texmath 不支持 `\smash{…}` → 去掉命令本身，保留 `{…}` 分组（渲染等价）。
        #    实测「原理·4 化学动力学」两个版本的 `$…\smash{…}…$` 整段原样漏进 Word。
        s = s.replace("\\smash", "")
        # ⑤ 相邻行内公式紧贴（`$…$$…$`）会被 markdown 判成 display 定界符 → 配对错乱，
        #    其后整段 LaTeX 明文漏进 Word（实测同文件 10 余处）。在两式之间补一个空格。
        #    ⚠️ 前瞻必须**限定 ASCII**：Python 的 `\w` 默认匹配中日韩汉字，
        #    会把 display 块闭合处的 `$$\mathrm{CO}$$由` 误拆（实测「原理·9 教师版」17 处误报）。
        s = re.sub(r"(?<=\})\$\$(?=[\\A-Za-z])", "$ $", s)
        # ⑥ 行内公式**闭合** `$` 后紧跟数字 → pandoc 不认其为闭合，其后整段被判成公式
        #    （实测「原理·5」`代入求 $\rho$2. 质量储氢密度…` 一处）。按出现顺序配对
        #    （第 1、3、5…个为开，第 2、4、6…个为闭），只在**闭** `$` 且后跟数字时补空格。
        def _sp_after_close(line):
            marks = [m.start() for m in re.finditer(r"(?<!\$)\$(?!\$)", line)]
            if len(marks) < 2:
                return line
            ins = [p for p in marks[1::2] if p + 1 < len(line) and line[p + 1].isdigit()]
            for p in reversed(ins):
                line = line[:p + 1] + " " + line[p + 1:]
            return line
        s = "\n".join(_sp_after_close(_ln) for _ln in s.split("\n"))
        # ⑧ 列表行前必须留空行（pandoc 规则）：`下列说法正确的是\n- A. …\n- B. …` 无空行时
        #    会被判成**同一段落**，`-` 退化为字面量、四个选项连成一行（实测两系列普遍）。
        s = re.sub(r"(?m)^([^\s|>#\-].*)\n(?=[-*] )", r"\1\n\n", s)
        # ⑦ 代码围栏内的 `$…$` 不会被解析成公式（pandoc 按代码块原样输出）——
        #    实测「原理·4 教师版 · Step 3 设计抑制剂」整块（12 个公式）被 ``` 包住，
        #    docx 里公式连同 `$` 一起明文印出。**仅当围栏内含 `$`** 时剥掉围栏行
        #    （内容保留为正常段落），避免误伤真正的等宽段/ASCII 图。
        _ls = s.split("\n")
        _out, _in_fence, _buf = [], False, []
        for _ln in _ls:
            _st = _ln.strip()
            if _st.startswith("```"):
                if not _in_fence:
                    _in_fence, _buf = True, []
                    continue
                _in_fence = False
                if any("$" in _x for _x in _buf):
                    _out.extend(_buf)
                else:
                    _out.append("```")
                    _out.extend(_buf)
                    _out.append("```")
                _buf = []
                continue
            if _in_fence:
                _buf.append(_ln)
            else:
                _out.append(_ln)
        if _in_fence:                      # 围栏未闭合 → 原样放回
            _out.append("```")
            _out.extend(_buf)
        s = "\n".join(_out)
        s = s.strip()
        if drop_h1:
            s = re.sub(r"^(#[^\n]*\n+)+", "", s).strip()
        return s

    def unwiki(x):
        x = re.sub(r"(?<!!)\[\[([^\]|]+)\|([^\]]+)\]\]", lambda m: m.group(2), x)
        x = re.sub(r"(?<!!)\[\[([^\]]+)\]\]", lambda m: m.group(1), x)
        return x

    q = clean(bq, True)
    q = re.sub(r"^#{1,6}\s*(参考)?(答案|解答|解析)[^\n]*$\n?", "", q, flags=re.M).strip()
    q = re.sub(r"^\*\*(参考)?(答案|解答|解析)\*\*[：:]?\s*$\n?", "", q, flags=re.M).strip()
    q = re.sub(r"^#{1,6}\s", "**·** ", q, flags=re.M)
    a = clean(ans, False)
    a = re.sub(r"^#{1,6}\s*(参考)?(答案|解答|解析)[^\n]*$", "", a, flags=re.M).strip()
    a = re.sub(r"^#{1,6}\s", "**·** ", a, flags=re.M)
    return fm, unwiki(q).strip(), unwiki(a).strip()


def band(v):
    m = re.search(r"\d+", str(v or ""))
    d = int(m.group()) if m else 3
    return 2 if d <= 2 else (3 if d == 3 else 4)


def prio(r):
    """题源优先序（2026-09-17 按**用户质量排序**重排）；返回 99 = 不进卷。

    用户原话排序：**真题 ＞ 竞赛导向题集 ＞ 竞赛教程 ＞ 竞赛教材·讲义 ＞ 大学教材课后习题**。
      0 真题（初赛·决赛·省预赛）
      1 竞赛导向题集（一分册·二分册·化学能力测试、北斗学友、汇智竞赛题目）
      2 竞赛教程（高中化学竞赛教程第一·二分册）
      3 竞赛教材·讲义（赵鑫光、化学竞赛初赛讲义、ABOC）
      4 自编章节题／教学改编／教材例题
     99 排除：非竞赛教材（大学教材课后习题）＋《普通化学原理》＋高考题
    ⚠️ 旧口径（v1）把「竞赛教材」排在 0、「真题」排在 3，与本排序相反 ——
       实测导致汇智（136 题，可路由 136／合格 127）**0 选中**、真题仅 20 可路由进池。
    """
    s = re.sub(r'^["\']|["\']$', "", r.get("source", ""))
    sc = r.get("source_category", "")
    sn = r.get("source_norm", "").strip('"\'')
    if any(x in s for x in BLACK):
        return 99
    if sc == "教材课后习题" or any(x in s for x in UNIV):
        return 99
    if sc.startswith("竞赛导向·真题"):
        return 0
    if sc == "竞赛导向·竞赛教辅":
        return 1
    if "竞赛教程" in sn:
        return 2
    if sc == "竞赛导向·竞赛教材":
        return 3
    return 4


TIERNAME = {0: "真题", 1: "竞赛题集", 2: "竞赛教程", 3: "竞赛教材", 4: "自编改编"}

TODAY = "2026-09-17"

# ── 来源显示的**书目级简称**（2026-09-17：用户要求「来源简洁一点」）──────────
# 由 `source_norm`（仅 10 个取值）派生，不再带章节/题号，也不带 ⭐ 与【题源层】标签。
SRCDISP = {
    "赵鑫光《高中化学竞赛基本理论学习笔记》": "赵鑫光竞赛笔记",
    "上海中学竞赛课程": "上海中学竞赛课程",
    "高中化学竞赛教程第一分册": "高中化学竞赛教程·第一分册",
    "高中化学竞赛教程第二分册": "高中化学竞赛教程·第二分册",
    "化学竞赛初赛讲义": "化学竞赛初赛讲义",
    "一分册能力测试": "一分册能力测试",
    "二分册能力测试": "二分册能力测试",
    "化学能力测试": "化学能力测试",
    "北斗学友竞赛模拟卷": "北斗学友竞赛模拟卷",
    "汇智竞赛题目": "汇智竞赛题目",
}


def shortsrc(r):
    """把 source_norm 变成一句话能读完的书目简称。"""
    sn = r.get("source_norm", "").strip('"\'')
    if sn in SRCDISP:
        return SRCDISP[sn]
    if sn.startswith("省预赛"):
        return "真题·" + sn.replace("省预赛·", "省预赛 ")
    if sn.startswith("第") and ("初赛" in sn or "决赛" in sn):
        return "真题·" + sn
    if sn.startswith("教学改编"):
        return "教学改编题"
    return re.sub(r"[\"'《》]", "", sn) or "题库"


DISCIPLINE = ("> **题源**：竞赛导向题源（真题 ＋ 一分册·二分册·化学能力测试 ＋ 北斗学友 ＋ "
              "汇智竞赛题目 ＋ 高中化学竞赛教程一·二分册 ＋ 赵鑫光竞赛笔记 ＋ 化学竞赛初赛讲义）。"
              "非竞赛教材（大学教材课后习题）不在本卷内，它们只出现在「课后习题集」。")


CREATE = None

def _media_index():
    s = set()
    for dp, dn, fn in os.walk(MEDIA):
        for f in fn:
            s.add(f)
    return s


MEDIA_IDX = _media_index()


def norm_images(s):
    """图引用归一为**纯哈希名**（库规 ⑥）。

    源题里有一部分写成 `![[06-外部资料导入/真题/images/<hash>.jpg]]`（带路径前缀）；
    只要 basename 在 `媒体仓库/` 存在，就改写为 `![[<hash>.jpg]]`，保证 Obsidian 与
    pandoc→docx 两条渲染路径都稳定命中。
    """
    def rep(m):
        ref = m.group(1).strip()
        if "/" not in ref:
            return m.group(0)
        base = os.path.basename(ref)
        return "![[" + base + "]]" if base in MEDIA_IDX else m.group(0)

    out = re.sub(r"!\[\[([^\]|\n]+)\]\]", rep, s)
    return re.sub(r"!\[\[([^\]|\n]+)\|[^\]\n]*\]\]", rep, out)


def resolve_img(im):
    """图片可解析性（三重口径：仓库相对路径 / 媒体仓库 / 媒体仓库 basename）。"""
    if os.path.exists(im):
        return True
    if os.path.exists(os.path.join(MEDIA, im)):
        return True
    return os.path.basename(im) in MEDIA_IDX


def imgs_ok(q, a):
    """出卷口径：**所有图引用都必须落在「媒体仓库」或仓库根**

    2026-09-17 实测：全库合格池 1,926 题里只有 **35 题** 的图存在但他处
    （`04-题库/真题/**/attachments`、`06-外部资料导入/**/*_images`、根 `media/`），
    且**无一真缺**。为保 Word/pandoc 管线，这类题在选材阶段即拒收（代价 1.8%）。
    """
    for i in IMG.findall(q) + IMG.findall(a):
        i = i.strip()
        if os.path.exists(i) or os.path.exists(os.path.join(MEDIA, i)):
            continue
        return False
    return True


def reuse_tier(r):
    """回收优先级：0 未用 ｜ 1 已用（可回收）｜ 2 已发给学生的结构化学第一轮卷（最后考虑）。"""
    u = r.get("used_in", "")
    if u in ("", "[]"):
        return 0
    return 2 if any(k in u for k in RELEASED) else 1


def main():
    recs = json.load(open(CENSUS, encoding="utf-8"))
    buckets = collections.defaultdict(list)
    stat = collections.Counter()
    for r in recs:
        if r.get("status") == "deprecated":
            continue
        b = os.path.basename(r["_path"])
        if ZUTI.match(b) or r.get("type") == "题组":
            stat["题组跳过"] += 1
            continue
        pp = prio(r)
        if pp >= 99:
            stat["普化/高考跳过"] += 1
            continue
        tk = route(r)
        if not tk:
            stat["无法路由"] += 1
            continue
        for k in ([tk] if isinstance(tk, str) else tk):
            buckets[k].append((pp, r))
    print(f"路由成功 {sum(len(v) for v in buckets.values())} | " +
          "  ".join(f"{k}:{v}" for k, v in stat.items()))

    picked, taken = {}, set()
    for key in ORDER:
        cand = [(pp, r) for pp, r in buckets.get(key, []) if r["_path"] not in taken]
        cand.sort(key=lambda x: (reuse_tier(x[1]), x[0],
                                 LEVMAP.get(x[1].get("teaching_level", ""), 9), x[1]["_path"]))
        ok, rej = [], collections.Counter()
        for pp, r in cand:
            got = load(os.path.join(ROOT, r["_path"].replace("/", os.sep)))
            if not got:
                rej["无frontmatter"] += 1
                continue
            fm, q, a = got
            if len(q) < 40:
                rej["题干过短"] += 1
                continue
            if len(a) < 15 and not is_choice_ans(a):
                rej["答案过短"] += 1
                continue
            if len(q) > 4000:
                rej["题干过长"] += 1
                continue
            if not imgs_ok(q, a):
                rej["图片不在媒体仓库"] += 1
                continue
            ok.append({"pp": pp, "r": r, "q": norm_images(q), "ans": norm_images(a),
                       "band": band(r.get("difficulty"))})
        sel = []
        for bd, n in QUOTA.items():
            sel += [c for c in ok if c["band"] == bd and c not in sel][:n]
        if len(sel) < PER_SET:
            # 兜底补齐：按难度从低到高补（2026-09-17 修，避免配额缺口被高难题随机填满）
            _rest = [c for c in ok if c not in sel]
            _rest.sort(key=lambda c: (c["band"], reuse_tier(c["r"]), c["pp"]))
            sel += _rest[:PER_SET - len(sel)]
        sel = sel[:PER_SET]
        sel.sort(key=lambda c: (c["band"], c["pp"]))
        for c in sel:
            taken.add(c["r"]["_path"])
        picked[key] = sel
        nu = sum(1 for c in sel if c["r"].get("used_in", "") in ("", "[]"))
        nr = sum(1 for c in sel if reuse_tier(c["r"]) == 2)
        print(f"【{T[key]}】路由 {len(buckets.get(key, []))} → 合格 {len(ok)} → 选 {len(sel)}"
              f"（未用 {nu}／回收 {len(sel)-nu}，其中结构已发 {nr}）" +
              ("  [拒收] " + " ".join(f"{k}×{v}" for k, v in rej.most_common(3)) if rej else ""))

    if not WRITE:
        return

    os.makedirs(OUTDIR, exist_ok=True)
    manifest, missing = [], []
    for key in ORDER:
        sel = picked[key]
        if not sel:
            continue
        name = T[key]
        mod = "结构化学" if name.startswith("结构") else "化学原理"
        short = name.split("-", 1)[1]
        bd = collections.Counter(c["band"] for c in sel)
        imgs = sorted({i for c in sel for i in IMG.findall(c["q"]) + IMG.findall(c["ans"])})
        for im in imgs:
            if not resolve_img(im):
                missing.append((name, im))
        for edition, with_ans in (("教师版", True), ("学生版", False)):
            L = ["---",
                 'title: "第一轮' + mod + "·" + short + " 练习（" + edition + "）\"",
                 "type: 题组", "role: 习题集", "round: 第一轮",
                 "subject_module: " + mod, "pack: 章节练习",
                 "question_count: " + str(len(sel)),
                 "difficulty_range: " + str(min(c["band"] for c in sel)) + "-" + str(max(c["band"] for c in sel)),
                 "source_category: 竞赛导向·竞赛教材", "status: 已填充",
                 "created: 2026-09-16", "updated: " + TODAY,
                 "tags: [化竞, 第一轮, 竞赛教材版, " + mod + ", " + short + "]", "---", "",
                 "# 第一轮" + mod + " · " + short + "｜练习", ""]
            if with_ans:
                # 教师版：题源说明 + 难度总览（**去 ⭐ 装饰**；来源行改成书目级简称）
                L += [DISCIPLINE,
                      "> **难度分布**：基础（≤2）" + str(bd.get(2, 0)) + " 题 + 进阶（=3）" + str(bd.get(3, 0))
                      + " 题 + 挑战（≥4）" + str(bd.get(4, 0)) + " 题，共 " + str(len(sel)) + " 题。",
                      "> **学生版**同题号同序，可直接印发。", "",
                      "## 难度总览", "", "| 难度 | 题号 | 题数 |", "|:---|:---|:---:|"]
                for lab, b_ in (("基础", 2), ("进阶", 3), ("挑战", 4)):
                    idx = [i + 1 for i, c in enumerate(sel) if c["band"] == b_]
                    if idx:
                        L.append("| " + lab + " | " + str(idx[0]) + "–" + str(idx[-1]) + " | " + str(len(idx)) + " |")
            else:
                # 学生版：**无来源行、无难度标记、无题源说明**（库内成品规则④）
                L += ["> 共 " + str(len(sel)) + " 题。建议先独立完成，再核对答案。"]
            L += ["", "---", "", "## 题目", ""]
            for i, c in enumerate(sel, 1):
                L += ["### 第" + str(i) + "题", ""]
                if with_ans:
                    L.append("> 来源：" + shortsrc(c["r"]))
                    used = c["r"].get("used_in", "")
                    if used not in ("", "[]"):
                        L.append("> 曾用于：" + used.replace('"', '').replace("[", "").replace("]", ""))
                    L.append("")
                L += [c["q"].strip(), ""]
                if with_ans:
                    L += ["**参考答案**：", "", c["ans"].strip(), ""]
                L += ["---", ""]
            io.open(os.path.join(OUTDIR, "第一轮" + name + "（" + edition + "）.md"),
                    "w", encoding="utf-8", newline="\n").write("\n".join(L))
        manifest.append({"key": key, "name": name, "n": len(sel),
                         "unused": sum(1 for c in sel if c["r"].get("used_in", "") in ("", "[]")),
                         "released": nr,
                         "bands": dict(bd),
                         "srcs": sorted({re.sub(r'^["\']|["\']$', "", c["r"].get("source", "")) for c in sel}),
                         "paths": [c["r"]["_path"] for c in sel]})
    io.open(os.path.join(OUTDIR, "_选题清单.json"), "w", encoding="utf-8").write(
        json.dumps(manifest, ensure_ascii=False, indent=1))
    n_img = sum(len(IMG.findall(c["q"])) + len(IMG.findall(c["ans"]))
                for v in picked.values() for c in v)
    print("\n[write] " + str(len(manifest)) + " 章 × 2 版 → " + OUTDIR)
    print("[图片] 引用 " + str(n_img) + " 处；未在媒体仓库 " + str(len(missing)) + " 处")
    for n, im in missing[:10]:
        print("   ", n, im)


main()
