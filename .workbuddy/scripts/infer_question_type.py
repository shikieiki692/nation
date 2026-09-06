#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B2b：question_type 归一化 + 分层推断。

背景：question_type 覆盖率只有 4.7%（4,071 题里仅 190 题有值），且已有值有 24 种
自由写法。实测纯正则启发式的**高置信只有 6%**，所以本脚本不追求全覆盖：

  T1 格式信号   选择 / 填空       —— 零误判，写
  T2 窄内容信号 机理/推断/方程式书写/作图/计算 —— 需抽样核精度，写
  T3 弱兜底     简答             —— 不写（"没识别出题型"的委婉说法，不是真标签）
  无信号        ——                —— 不写

核心设计：**输出触发证据而不只是标签**。每个推断都附带命中片段，
这样判断精度靠看证据，而不是看统计数字猜。

用法：
  python infer_question_type.py                       # dry-run：统计 + 每档抽样
  python infer_question_type.py --samples 60          # 每档抽 60 条
  python infer_question_type.py --dump evidence.txt   # 抽样证据落盘细看
  python infer_question_type.py --write               # 实写（确认精度后再跑）
  python infer_question_type.py --tiers T1            # 只写指定档（可 T1 / T1,T2）
"""
from __future__ import annotations

import argparse
import random
import re
import sys
from collections import Counter
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
sys.path.insert(0, str(VAULT / "11-模板" / "scripts"))
import validate_kb as V  # noqa: E402

TARGET_DIRS = ["04-题库", "05-真题库"]

# ── 词汇表 ───────────────────────────────────────────────────────
# 10 种原子题型 + 2 个标记值
# 2026-09-02 B6 新增「合成」：缺口档实测 91 题含「合成」（85 条是真指令，
# 集中在 ABOC），原 9 种题型没有这一类，有机合成题全部无类型、组卷无法筛。
ATOMIC = ["选择", "填空", "简答", "计算", "推断", "作图", "机理", "方程式书写", "推导", "合成"]
MARKERS = ["例题", "综合"]          # 例题=角色标记；综合=未细分待人工拆
VOCAB = set(ATOMIC) | set(MARKERS)

# 现有 24 种写法 → 归一化列表。None = 无法拆分，保持原样并进 backlog。
NORM = {
    "选择题": ["选择"],
    "简答题": ["简答"],
    "计算题": ["计算"],
    "计算": ["计算"],
    "推断题": ["推断"],
    "推断": ["推断"],
    "机理题": ["机理"],
    "方程式书写题": ["方程式书写"],
    "填空题": ["填空"],
    "例题": ["例题"],
    "简答+画图": ["简答", "作图"],
    "简答+计算": ["简答", "计算"],
    "推断+画图": ["推断", "作图"],
    "推断与简答": ["推断", "简答"],
    "计算+推断": ["计算", "推断"],
    "计算与简答": ["计算", "简答"],
    "计算+推导": ["计算", "推导"],
    "计算与推导": ["计算", "推导"],
    "推导与计算": ["计算", "推导"],
    "简答与推导": ["简答", "推导"],
    "综合计算与简答": ["计算", "简答"],
    "综合计算与画图": ["计算", "作图"],
    "综合题": None,
}

# ── 推断规则 ─────────────────────────────────────────────────────
# 每条规则 = (题型, 档位, 正则)。档位决定写不写。
# 正则刻意写窄：宁可漏，不可错。早期宽正则让「画图」虚高到 16%，
# 因为「画出某某结构」其实是推断题的一部分。

# 选项标记：形如 A. / A、/ （A） / A）
# 排除误判「化合物 A、B、C、D」这种推断题的字母代号，靠 detect_choice 的
# 「相邻选项之间至少 2 个字符内容」把关 —— 字母代号紧贴在一起，没有选项内容。
#
# 2026-09-02 修正：原写法是 (?<![\w.。（(])，负向断言把前面是 `(` 的情况也排除了，
# 于是 `(A) 2; (B) 4; (C) 8; (D) 16` 这种**最常见**的选项排版 100% 检不出。
# 实测全库 394 → 482（+88），零丢失，抽样 25 条全部是真选择题。
# 现在的负向断言只保留「前面是字母/数字/句点」，避免把 `H2A)` 之类化学式当选项。
OPT_ANY = re.compile(r"(?<![A-Za-z0-9.。])([ABCD])\s*[)）.、．]")

# 计算档：动词 + 宾语双条件。
# 只写「求 X 的浓度」这种指令式，不写「由晶格匹配计算结果，……」这种名词用法。
# 「求」加负向断言，排除 要求/需求/请求/追求/寻求/求证。
CALC_OBJ = (
    r"(?:平衡常数|解离常数|电离常数|稳定常数|速率常数|平衡转化率|转化率|产率|收率|纯度|"
    r"质量分数|摩尔分数|体积分数|物质的量|摩尔质量|相对分子质量|分子式|化学式|分子量|"
    r"浓度|溶解度|溶度积|密度|晶胞参数|配位数|晶胞的体积|"
    r"电动势|电极电势|电势|电位|电压|"
    r"焓变|熵变|自由能|活化能|键能|晶格能|热效应|热量|反应热|"
    r"pH|pOH|pK|K_\{?[a-zA-Z]|k_\{?[a-zA-Z]|"
    r"半衰期|速率|反应级数|百分[含数]|质量|体积|压强|压力|温度|电量|电流效率|"
    r"键级|磁矩|偶极矩|介电常数|电离能|电子亲和能|电负性|原子半径|离子半径)"
)
# 2026-09-02 B6 补动词：「多少 / 是多少 / 估计」此前完全没覆盖，而教材习题里
# 「至少要取多少克 KClO₃」「估计总共用了多少千克氮气」是极常见的问法。
CALC_VERB = (r"(?:计算|试求|求算|推算|估算|估计|算(?:出|得)?|"
             r"(?<![要需请追寻力求探证])求(?:出|得)?|多少|是多少)")
# 2026-09-02 B6 补宾语：教材习题的问法超出原词表很多。反例：
#   「试求管中气体的分子数」——原词表有「物质的量」没有「分子数」
#   「求氮气与氢气的分压」——原词表有「压力」但「分压」二字不挨着，匹配不上
#   「计算水的总硬度」「推算 H⁻ 的半径」「计算…的键长/波长」——原词表全缺
CALC_OBJ_EXTRA = (
    # 热化学：原词表只有「焓变」，而教材习题高频问的是「生成焓/燃烧热/生成热」。
    # 反例 05-05「由以下两个反应热求 NO 的生成焓」、05-27「金刚石的标准摩尔生成焓为多少」。
    r"生成焓|生成热|生成自由能|燃烧热|溶解热|水合热|升华热|汽化热|熔化热|中和热|"
    # LaTeX / Unicode 形式的热力学量。反例 05-18「求下列反应的 $\Delta H^{\ominus},
    # \Delta G^{\ominus}$ 和 $\Delta S^{\ominus}$」——原正则只认中文「焓变/熵变」。
    r"\\Delta\s*[HGSEUF]|Δ[HGSEUF]|"
    r"分子数|原子数|电子数|质子数|中子数|离子数|粒子数|"
    r"分压|总压|蒸气压|渗透压|"
    r"硬度|解离度|电离度|回收率|"
    r"物质的量之比|摩尔比|质量比|体积比|比值|比例|"
    r"式量|摩尔体积|气体体积|"
    r"克数|用量|投料量|产量|"
    r"含量|品位|滴定度|酸度|碱度|缓冲容量|"
    r"沸点|熔点|凝固点|"
    r"能级|能量|波长|频率|波数|"
    r"键长|键角|半径|晶胞参数值|"
    r"电量|电荷量|电流|"
    r"级数|速率值"
)
CALC_OBJ = (
    r"(?:平衡常数|解离常数|电离常数|稳定常数|速率常数|平衡转化率|转化率|产率|收率|纯度|"
    r"质量分数|摩尔分数|体积分数|物质的量|摩尔质量|相对分子质量|分子式|化学式|分子量|"
    r"浓度|溶解度|溶度积|密度|晶胞参数|配位数|晶胞的体积|"
    r"电动势|电极电势|电势|电位|电压|"
    r"焓变|熵变|自由能|活化能|键能|晶格能|热效应|热量|反应热|"
    r"pH|pOH|pK|K_\{?[a-zA-Z]|k_\{?[a-zA-Z]|"
    r"半衰期|速率|反应级数|百分[含数]|质量|体积|压强|压力|温度|电量|电流效率|"
    r"键级|磁矩|偶极矩|介电常数|电离能|电子亲和能|电负性|原子半径|离子半径|"
    rf"{CALC_OBJ_EXTRA})"
)
# 2026-09-02 B6：窗口 24 → 60。反例「计算0.10 mol/L硼酸甘露醇溶液用0.10 mol/L
# NaOH滴定时的计量点pH」——动词与宾语隔了 40+ 字符，24 的窗口根本够不着。
#
# 另加**宾语在前**的反向分支。中文问句常把疑问词放句尾：
#   「金刚石的标准摩尔生成焓**为多少**？」「三价铁离子浓度**为何值**时…」
# 原先只认「动词 + 宾语」，这两类一律漏判，然后被 T3S 的「为何」捡去误标成简答。
# 反向分支的宾语表排除「配位数」。反例 题-元钛-01「金红石型 TiO₂ 晶胞中 Ti 与 O 的
# **配位数**各为多少」——那是读已知结构，不是计算题。
CALC_OBJ_REV = CALC_OBJ.replace("|配位数", "")
CALC_RE = re.compile(
    rf"(?:{CALC_VERB}[^。！？；\n]{{0,60}}?{CALC_OBJ})"
    rf"|(?:{CALC_OBJ_REV}[^。！？；\n]{{0,10}}?(?:为|是|等于)?(?:多少|为何值|几[克个摩]))"
)

RULES: list[tuple[str, str, re.Pattern]] = [
    # T2 窄内容信号
    ("机理", "T2", re.compile(r"反应机理|反应历程|历程如下|写出.{0,6}机理|机理[，。、：]|用.{0,4}机理解释")),
    # 2026-09-02 B6 放宽：原正则要求「推断」后面紧跟 其/出/该/结构，
    # 于是「推断 A、C 的可能组成」「推断 X 并写出相应反应」这类元素推断题 100% 漏判。
    # 题干里出现「推断」几乎必然是推断题；与机理/方程式书写并存时是多标签，不冲突。
    #
    # 不要加「判断」类分支：中文分词陷阱 —— 「判断**下列**说法是否正确」的字符序列
    # 包含子串「判断下列」，会被误判成推断题（实测 题-络重-05 中招）。
    # 而「判断下列说法」其实是判断题/简答题，根本不是推断。
    #
    # 「推断」作名词时要排除。实测三个反例：
    #   ABOC-267/290「全合成**推断题目**的分析方法」——标题里的名词，实为合成分析题
    #   Clayden-497「请评论这**一推断**的有效性」——评论题，不是推断题
    ("推断", "T2", re.compile(r"推断(?!\s*(?:题目|的|有效性|结果|结论|过程|方法|依据))|未知物")),
    # 2026-09-02 B6 新增「合成」题型。刻意排除名词用法「合成氨/合成气/合成橡胶」：
    # 这些后面跟的是具体物质名，不会接 路线/方法/方案，也凑不出「以X为原料合成Y」。
    ("合成", "T2", re.compile(
        r"(?:设计|提出|给出|写出).{0,12}合成(?:路线|方法|方案|步骤)"
        r"|以.{0,24}为原料合成|由.{0,20}为原料.{0,6}合成"
        r"|合成路线|试合成|如何合成|怎样合成|合成下列")),
    ("方程式书写", "T2", re.compile(r"完成并配平|配平下列|写出.{0,10}(?:化学|离子|电极|热化学)反应?方程式|写出.{0,6}反应式")),
    ("作图", "T2", re.compile(r"画出.{0,12}(?:结构|构型|轨道|能级|相图|曲线|图像|示意|图)|[画作绘]制.{0,10}(?:图|曲线)|试画|作出.{0,8}图")),
    ("计算", "T2", CALC_RE),
    # T3S 强解释信号：整题**没有**任何 T1/T2 命中时才写（2026-09-02 用户决策）。
    # 与 T3 的区别在于动词是否明确指向"论述型回答"——「说明理由」是，「说明」不是。
    # 「为何」必须排除「为何值」（浓度为何值 = 计算题，不是问原因）。
    # 反例 09-07「试问当三价铁离子浓度为何值时，恰好有 Fe(OH)₃ 沉淀析出」。
    ("简答", "T3S", re.compile(r"为什么|为何(?!值)|解释|简述|说明理由|(?:说明|解释)理由|加以说明|比较|讨论|鉴别")),
    # T3 弱兜底：只用于统计，不写。这些词在化学题干里常作插入语，
    # 单独命中不足以认定题型（「如图所示，说明…」「如何操作」）。
    ("简答", "T3", re.compile(r"说明|怎样|如何|指出|描述|分析")),
]

# 答案区边界：本库写法五花八门，除 ## 答案 / **答案：** / <details> 外，
# 还有 OCR 逐字重录题直接跟「解：」「解答：」——不切会把答案内容当题干去推断。
ANS_CUT = re.compile(
    r"(?m)^(?:"
    r"##+\s*(?:参考答案|答案|解析|解答|详解|【答案】|【解析】|【解答】)"
    r"|>?\s*\*\*答案[：:]\*\*"
    r"|>?\s*\*\*(?:解析|解答|详解)[：:]?\*\*"
    r"|[解答][：:]"
    r"|【解】|【解答】|【解析】"
    r"|<details>"
    r")"
)
MAX_STEM = 3000

# 竞争动作动词：题干里若同时出现这些动词，说明是**混合题**
# （「解释…并写出方程式」「说明…并计算…」），单标一个题型会盖掉另一半。
# 2026-09-02 B6 新增。反例：题-元钛-03「写出…平衡方程式，说明加酸/加碱的移动方向」
# 只标「简答」就把方程式书写那一半吞掉了。
# 「求」加了负向断言排除 要求/需求/请求/追求/寻求/求证，与 CALC_VERB 同一套处理。
COMPETE_RE = re.compile(
    r"写出|画出|绘制|作出|试画|配平|完成并|计算|试求|求算|推算|估算|合成|制备|分离|设计"
    r"|(?<![要需请追寻力探证])求"
)

# ── 题干净化 ───────────────────────────────────────────────────
# 文件名/标题里经常带「机理」「计算」「单选」等词（题-XXX-反应机理），
# 混进题干会被当成内容信号 —— 这是机理档误判的头号来源。
SECTION_Q = re.compile(r"(?m)^##+\s*(?:题目|问题|原题|题干)\s*$")
# B6.5（2026-09-02）：答案前置布局里，答案块之后的编号小节标题（## 5.11 / ## 18.1 …）
NUM_SEC = re.compile(r"(?m)^##+\s*\d")
H1_LINE = re.compile(r"(?m)^#\s+.*$")
META_QUOTE = re.compile(
    r"(?m)^>\s*\[?!?\w*\]?\s*\*{0,2}(?:来源|难度|教学层级|题目类型|分值|知识点|标签|小问关联|答案)\*{0,2}\s*[：:]"
)


def clean_stem(text: str) -> str:
    """取干净的题干：去 frontmatter → 切答案区 → 去标题与元信息引用行。"""
    fs, fe, lines = split_fm(text)
    body = "\n".join(lines[fe + 1:]) if fs is not None else text
    m = ANS_CUT.search(body)
    if m:
        # B6.5（2026-09-02）：答案前置布局——《无机化学例题与习题》选择题合集把
        # 「## 参考答案」放在题目前面，题干全在答案块之后的编号小节（## 5.11 …）里。
        # 旧逻辑切到答案区之前 → stem 只剩标题 → 假"无信号"。
        # 三条件同时满足才改取编号小节起的内容：答案区出现极早 / 答案区后有编号小节 /
        # 答案区前只有标题（≤200 字）。否则维持原切法（普通"题干→答案"布局零影响）。
        m_num = NUM_SEC.search(body, m.end())
        if (
            m.start() <= 300
            and m_num is not None
            and len(body[: m.start()].strip()) <= 200
        ):
            body = body[m_num.start():]
        else:
            body = body[: m.start()]
    # 有 ## 题目 / ## 问题 小节的，只取其后的内容
    ms = list(SECTION_Q.finditer(body))
    if ms:
        body = body[ms[0].end():]
    else:
        # 没有小节标记的，剥掉首个 # 标题行（通常就是「# 题-XXX-机理」）
        h1 = H1_LINE.search(body)
        if h1 and h1.start() < 400:
            body = body[: h1.start()] + body[h1.end():]
    # 剥掉开头连续的引用块元信息（> 来源：… / > [!info] …）
    out, started = [], False
    for ln in body.split("\n"):
        if not started and (not ln.strip() or META_QUOTE.match(ln)):
            continue
        started = True
        out.append(ln)
    body = "\n".join(out)
    return body[:MAX_STEM]


# ── frontmatter 文本级定位（复用 B1）──────────────────────────────
def split_fm(text: str):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None, lines
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return 0, i, lines
    return None, None, lines


def find_key_line(lines: list[str], fm_end: int, field: str):
    pat = re.compile(rf"^{re.escape(field)}\s*:")
    for idx in range(1, fm_end):
        if pat.match(lines[idx]):
            return idx
    return None


def read_raw(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_raw(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def line_term(line: str) -> str:
    return "\r" if line.endswith("\r") else ""


def term_at(lines: list[str], idx: int) -> str:
    if idx < len(lines):
        return line_term(lines[idx])
    return line_term(lines[-1]) if lines else ""


def yq(s: str) -> str:
    if s == "":
        return '""'
    if re.search(r'[\[\]:#{}&*!|>%@`",\n]', s) or s != s.strip():
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def render_inline(field: str, items: list[str]) -> str:
    return f"{field}: [{', '.join(yq(i) for i in items)}]"


# ── 题干提取与推断 ───────────────────────────────────────────────
def stem_of(text: str) -> str:
    """去掉 frontmatter，切到答案区之前。（兼容旧名，内部走 clean_stem）"""
    return clean_stem(text)


def detect_choice(stem: str):
    """
    选择题检测。
    - 支持「逐行」和「行内」两种排版（浙江预赛是 `- A. x　B. y　C. z　D. w` 挤在一行）
    - 要求 A→B→C→D 顺序连续出现 ≥3 个
    - 相邻两个选项之间必须间隔 ≥2 字符，用来排除推断题里
      「化合物 A、B、C、D」这种字母代号（它们紧贴在一起，没有实际选项内容）
    """
    ms = list(OPT_ANY.finditer(stem))
    want = "ABCD"
    i = 0
    chain: list = []
    for m in ms:
        ch = m.group(1)
        if ch == want[i]:
            if chain and m.start() - chain[-1].end() < 2:
                # 与上一条选项之间没有内容 —— 是字母代号，不是选项，重开
                chain, i = [], 0
                if ch == "A":
                    chain, i = [m], 1
                continue
            chain.append(m)
            i += 1
            if i == 4:
                break
        elif ch == "A":
            chain, i = [m], 1
        else:
            chain, i = [], 0
    if len(chain) >= 3:
        seg = stem[chain[0].start(): chain[-1].end() + 20]
        return seg.replace("\n", " ")[:40]
    return None


# ── 多小问检测 ───────────────────────────────────────────────────
# 真题大题一题多问（7-1 / 7-2 / 7-3 / (1)(2)(3)），单一题型标签必然失真，
# 这类文件不写推断结果，留给人工或后续拆分。
SUBQ_LINE = re.compile(r"(?m)^\s*[\(（【]?\s*(\d{1,2})\s*[\)）】]?\s*[.、．]")
# 复合编号：7-1、5-1-1、10.1、1.1.1。前置必须是行首或分隔标记，
# 避免把「0.10 mol/L」这类浓度数值误当编号。
SUBQ_TOKEN = re.compile(
    r"(?m)(?:^|(?<=[\s>\*\-\(（、；;：:｜|]))(\d{1,2}(?:[.\-]\d{1,2}){1,2})(?![\w.\-])"
)
SUBQ_INLINE = re.compile(r"[\(（]\s*(\d{1,2})\s*[\)）]")


def _has_run(vals) -> bool:
    """值集合里是否含 ≥3 个连续整数。
    小问编号几乎总是 1,2,3 连续；而「0.10 / 0.20 / 0.30 mol/L」这类
    浓度数值不会连续 —— 靠这一条把它们排除掉。"""
    ns = sorted({int(v) for v in vals if v.isdigit()})
    if len(ns) < 3:
        return False
    run = 1
    for i in range(1, len(ns)):
        run = run + 1 if ns[i] == ns[i - 1] + 1 else 1
        if run >= 3:
            return True
    return False


def is_multi(stem: str) -> bool:
    if _has_run(SUBQ_LINE.findall(stem)):
        return True
    if _has_run(SUBQ_INLINE.findall(stem)):
        return True
    groups: dict[str, set] = {}
    for tok in SUBQ_TOKEN.findall(stem):
        parts = re.split(r"[.\-]", tok)
        if len(parts) == 2:
            groups.setdefault(parts[0], set()).add(parts[1])
        else:                       # a-b-c / a.b.c：以 a-b 为组，c 为小问号
            groups.setdefault(f"{parts[0]}-{parts[1]}", set()).add(parts[2])
    return any(_has_run(v) for v in groups.values())


def split_subq(stem: str) -> list[str]:
    """按小问编号把题干切成若干段。切不出来返回空表。"""
    marks: set[int] = set()
    for pat in (SUBQ_LINE, SUBQ_INLINE, SUBQ_TOKEN):
        for m in pat.finditer(stem):
            marks.add(m.start())
    pos = sorted(marks)
    if len(pos) < 3:
        return []
    # 总起句在编号之前（「计算下列溶液的 pH：(1)…(2)…」），切段后每段只剩
    # 化学式、没有动词，会全部落空。把总起句拼进每一段。
    prefix = stem[: pos[0]]
    if len(prefix) > 300:
        # 2026-09-02 B6：原写法直接置空，长题干的多问题每一段就只剩化学式、
        # 没有指令动词 —— 实测 287 条「切段后全段落空」就是这么来的。
        # 指令动词通常紧邻第一个小问编号之前，保留末尾 200 字就能带出来。
        prefix = prefix[-200:]
    segs = []
    for i, s in enumerate(pos):
        e = pos[i + 1] if i + 1 < len(pos) else len(stem)
        if e - s >= 4:              # 2026-09-02：8 → 4，「(2) 计算 pH」这种短问原先被滤掉
            segs.append(prefix + stem[s:e])
    return segs


def infer_multi(stem: str):
    """
    多小问题干的特殊处理：按小问切段后逐段推断。

    像「计算下列溶液的 pH：(1)… (2)… (3)…」这种**同质多问题**，整题就是计
    算题，不该因为小问数 ≥3 就放弃。判定条件（宁可漏不可错）：
      · 至少切出 3 段
      · 每一段都命中 T1/T2/T3S（任一段落空或落到 T3「没识别出题型」就整体放弃）
      · 各段题型的并集 ≤2（段间不一致说明是真综合题，留给人工）
    """
    segs = split_subq(stem)
    if len(segs) < 3:
        return None, [], []
    res = []
    for s in segs:
        t, ty, _ = infer(s)
        if t is None or t == "T3":
            return None, [], []
        res.append((t, ty, s))
    union: set[str] = set()
    for _, ty, _ in res:
        union |= set(ty)
    if not union or len(union) > 2:
        return None, [], []
    best = "T3S"
    for cand in ("T2", "T1"):
        if any(r[0] == cand for r in res):
            best = cand
            break
    types = [x for x in ATOMIC if x in union]
    evs = [r[2].strip().replace("\n", " ")[:44] for r in res[:3]]
    return best, types, evs


def detect_blank(stem: str):
    m = re.search(r"_{3,}|（[ \u3000]{2,}）|\([ \t]{2,}\)", stem)
    return m.group(0).strip()[:40] if m else None


def infer(stem: str):
    """
    返回 (档位, 题型列表, 证据列表)。

    T1（选择/填空）与 T2（计算/推断/作图/机理/方程式书写）是**两个维度**：
    前者是作答形式，后者是内容题型，并不互斥。
      「画出A的结构简式____」  → [填空, 作图]
      「配平下列方程式 (1)____」 → [填空, 方程式书写]
      「选择题：求pH」          → [选择, 计算]
    两个维度都写，组卷时无论按形式筛还是按内容筛都能命中。
    T3（简答）是「没识别出题型」的委婉说法，只统计不写。
    """
    hits: list[tuple[str, str, str]] = []   # (tier, type, evidence)

    ev = detect_choice(stem)
    if ev:
        hits.append(("T1", "选择", ev))
    ev = detect_blank(stem)
    if ev:
        hits.append(("T1", "填空", ev))

    for typ, tier, pat in RULES:
        m = pat.search(stem)
        if m:
            s = max(0, m.start() - 12)
            hits.append((tier, typ, stem[s: m.end() + 12].replace("\n", " ")[:60]))

    if not hits:
        return None, [], []

    keep = [h for h in hits if h[0] in ("T1", "T2")]
    if not keep:
        # 只有兜底信号。**全部**命中强信号才算 T3S（可写）；
        # 混入任何 T3 弱信号就降回 T3（不写）—— 弱信号说明题型不确定。
        types, evs = [], []
        for _, typ, e in hits:
            if typ not in types:
                types.append(typ)
                evs.append(e)
        tier = "T3S" if all(h[0] == "T3S" for h in hits) else "T3"
        # 竞争动词闸门：题干里还有别的动作动词 → 是混合题，单标「简答」会失真，不写。
        if tier == "T3S" and COMPETE_RE.search(stem):
            tier = "T3"
        return tier, types, evs

    types, evs = [], []
    for _, typ, e in keep:
        if typ not in types:
            types.append(typ)
            evs.append(e)
    best = "T1" if any(h[0] == "T1" for h in keep) else "T2"
    return best, types, evs


# ── 主流程 ───────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="实写（默认 dry-run）")
    # 2026-09-02 B6：默认档位加入 T3S（强解释信号，仅整题无 T1/T2 命中时才写）。
    # T3（说明/怎样/如何 等弱信号）默认仍不写。
    ap.add_argument("--tiers", default="T1,T2,T3S", help="允许写入的档位，逗号分隔")
    ap.add_argument("--samples", type=int, default=25, help="每档抽样条数")
    ap.add_argument("--per-label", type=int, default=0,
                    help=">0 时**按题型标签**分组抽样，用于逐标签核精度（档位抽样看不出单个标签的误判）")
    ap.add_argument("--dump", default="", help="抽样证据落盘路径")
    ap.add_argument("--pending-out", default="",
                    help="dry-run 时把**将会被写入**的文件清单落盘，用于先打快照再实写、事后逐字节校验")
    ap.add_argument("--seed", type=int, default=20260902)
    args = ap.parse_args()
    allow = set(t.strip() for t in args.tiers.split(","))

    files: list[Path] = []
    for d in TARGET_DIRS:
        files.extend(sorted((VAULT / d).rglob("*.md")))
    files = [p for p in files if p.name not in V.EXCLUDE_FILE_NAMES]

    stats: Counter = Counter()
    samples: dict[str, list] = {"T1": [], "T2": [], "T3S": [], "T3": [], "多问": [], "无": []}
    lab_samples: dict[str, list] = {}      # 按题型标签分组（--per-label）
    pending: list[str] = []                # 待写文件清单（--pending-out）
    backlog_norm: list = []
    rng = random.Random(args.seed)

    print(f"扫描 {len(files)} 个文件…")

    for p in files:
        try:
            text = read_raw(p)
            fs, fe, lines = split_fm(text)
            if fs is None:
                stats["无frontmatter跳过"] += 1
                continue
            fm_text = "\n".join(lines[fs + 1:fe])
            import yaml
            try:
                fm = yaml.safe_load(fm_text) or {}
            except Exception:
                stats["YAML解析失败"] += 1
                continue
            if not isinstance(fm, dict):
                continue
            # 只处理真正的题目文件。本目录里混着 索引 / README / 真题整卷 /
            # 图片索引 等非题目文件，不加这道闸会把 question_type 写进它们。
            # 05-真题库 的题目 type 写作「真题」，一并放行。
            if str(fm.get("type", "")).strip() not in ("题目", "真题"):
                stats["非题目跳过"] += 1
                continue

            rel = p.relative_to(VAULT).as_posix()
            cur = fm.get("question_type")

            # ── 归一化已有值（确定性）──
            if cur is not None:
                raw = cur if isinstance(cur, list) else [cur]
                raw_s = [str(x).strip() for x in raw if str(x).strip()]
                out: list[str] = []
                unknown: list[str] = []
                for r in raw_s:
                    if r in VOCAB:
                        out.append(r)
                    elif r in NORM:
                        if NORM[r] is None:
                            unknown.append(r)
                        else:
                            out.extend(NORM[r])
                    else:
                        unknown.append(r)
                if unknown:
                    stats["归一化-无法拆分保持原样"] += 1
                    backlog_norm.append((rel, raw_s))
                    continue
                # 去重保序
                seen, dedup = set(), []
                for x in out:
                    if x not in seen:
                        seen.add(x)
                        dedup.append(x)
                if dedup == raw_s:
                    stats["归一化-已是规范写法"] += 1
                    continue
                stats["归一化-待改写"] += 1
                pending.append(rel)
                if args.write:
                    i = find_key_line(lines, fe, "question_type")
                    if i is None:
                        stats["归一化-定位失败"] += 1
                    else:
                        lines[i] = render_inline("question_type", dedup) + term_at(lines, i + 1)
                        write_raw(p, "\n".join(lines))
                        stats["归一化-已写入"] += 1
                continue

            # ── 缺失 → 推断 ──
            stats["缺question_type"] += 1
            stem = stem_of(text)
            tier, types, evs = infer(stem)
            if tier is None:
                stats["推断-无信号"] += 1
                key = "无"
            elif tier != "T1" and is_multi(stem):
                # 一题多问：先试「同质多问」（各小问题型一致），否则放弃
                m_tier, m_types, m_evs = infer_multi(stem)
                if m_types:
                    tier, types, evs = m_tier, m_types, m_evs
                    stats["推断-多问同质"] += 1
                    stats[f"推断-多问同质-{'+'.join(types)}"] += 1
                    key = tier
                    if tier in allow:
                        stats["推断-符合写入条件"] += 1
                        pending.append(rel)
                        if args.write:
                            i = find_key_line(lines, fe, "difficulty")
                            idx = (i + 1) if i is not None else fe
                            lines.insert(idx, render_inline("question_type", types) + term_at(lines, idx))
                            write_raw(p, "\n".join(lines))
                            stats["推断-已写入"] += 1
                else:
                    stats["推断-多小问跳过"] += 1
                    key = "多问"
            else:
                stats[f"推断-{tier}"] += 1
                stats[f"推断-{tier}-{'+'.join(types)}"] += 1
                key = tier
                if tier in allow:
                    stats["推断-符合写入条件"] += 1
                    pending.append(rel)
                    if args.write:
                        i = find_key_line(lines, fe, "difficulty")
                        idx = (i + 1) if i is not None else fe
                        lines.insert(idx, render_inline("question_type", types) + term_at(lines, idx))
                        write_raw(p, "\n".join(lines))
                        stats["推断-已写入"] += 1

            if len(samples[key]) < args.samples and (rng.random() < 0.35 or len(samples[key]) < 5):
                samples[key].append((rel, types, evs, stem[:150].replace("\n", " ")))
            # 只抽**会被写入**的条目（tier in allow）——把 T3 不写档的样本混进来
            # 会让精度判断失真：看着一堆 🟡，其实那一半根本不会落盘。
            if args.per_label and types and tier in allow and key == tier:
                lkey = "+".join(types)
                bucket = lab_samples.setdefault(lkey, [])
                if len(bucket) < args.per_label:
                    bucket.append((rel, tier, evs, stem[:150].replace("\n", " ")))
        except Exception as e:
            stats["异常跳过"] += 1
            if stats["异常跳过"] <= 5:
                print(f"  !! {p.relative_to(VAULT).as_posix()}: {type(e).__name__}: {e}")

    print("\n═══ 统计 ═══")
    for k, v in sorted(stats.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {k:34s} {v}")

    dump_lines: list[str] = []
    for key in ["T1", "T2", "T3S", "多问", "T3", "无"]:
        if not samples[key]:
            continue
        hdr = f"\n═══ 抽样：{key}（{len(samples[key])} 条）═══"
        print(hdr)
        dump_lines.append(hdr)
        for rel, types, evs, snip in samples[key]:
            mark = "写" if key in allow else "不写"
            line1 = f"  [{mark}] {rel}"
            line2 = f"        标签={types}  证据={evs}"
            line3 = f"        题干: {snip}"
            print(line1)
            print(line2)
            print(line3)
            dump_lines += [line1, line2, line3]

    if lab_samples:
        print("\n═══ 按题型标签抽样（逐标签核精度用）═══")
        for lkey in sorted(lab_samples, key=lambda k: -len(lab_samples[k])):
            rows = lab_samples[lkey]
            hdr4 = f"\n--- 标签 [{lkey}]  样本 {len(rows)} 条 ---"
            print(hdr4)
            dump_lines.append(hdr4)
            for rel, tier, evs, snip in rows:
                line = (f"  [{tier}] {rel}\n        证据={evs}\n        题干: {snip}")
                print(line)
                dump_lines.append(line)

    if backlog_norm:
        print(f"\n═══ 归一化 backlog（无法拆分，保持原样）{len(backlog_norm)} 条 ═══")
        for rel, raw in backlog_norm[:10]:
            print(f"  {rel}  原值={raw}")
        if len(backlog_norm) > 10:
            print(f"  …共 {len(backlog_norm)} 条")

    if args.pending_out and not args.write:
        Path(args.pending_out).write_text("\n".join(sorted(set(pending))),
                                          encoding="utf-8", newline="")
        print(f"\n待写清单已写入：{args.pending_out}（{len(set(pending))} 个文件）")

    if args.dump:
        Path(args.dump).write_text("\n".join(dump_lines), encoding="utf-8", newline="")
        print(f"\n抽样证据已写入：{args.dump}")

    print("\n" + ("已实写。" if args.write else "这是 DRY-RUN，加 --write 才会落盘。"))


if __name__ == "__main__":
    main()
