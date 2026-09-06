# -*- coding: utf-8 -*-
"""
2026-08-31 题库逐题质量扫描（只读，不写题库文件）
目标：四类问题全量机械检测
  ① OCR 识别错误（选项字母/符号/数字/大小写混淆）
  ② 题干或答案缺失、错漏、顺序颠倒
  ③ 答案选项内容不一致/重复
  ④ 格式、标点、空格不一致
另输出优化建议线索（答案分布、选项同前缀、跨文件重复题干）。
用法：python scan_question_quality.py
"""
import re, json, sys
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import audit_question_bank as A

VAULT = A.VAULT
OUT_MD = VAULT / "09-审计报告" / "2026-08-31-逐题质量扫描.md"
OUT_JSON = VAULT / "09-审计报告" / "缓存-逐题质量扫描.json"

QUESTION_TYPES = {"题目", "真题", "例题"}
SKIP_DIR_PARTS = {".obsidian", ".git", "node_modules", "__pycache__", ".chem_media"}

# ---------- 正则 ----------
# 选项前缀：行首或空格后的 A. A、 A) A） (A) （A） A: A：
# 注意：不含顿号 `、`（中文列举“A、B”不是选项）；不含全角句点（单独检测）
OPT_PREFIX_RE = re.compile(r"(?<![A-Za-z])[A-D]\s*[.)）:：]")
# 选项标点种类提取
OPT_SEP_RE = re.compile(r"(?<![A-Za-z])[A-D]\s*([.、)）:：])")
# 全角点当分隔：A．xxx
OPT_FW_DOT_RE = re.compile(r"(?<![A-Za-z])[A-D]．")
# 答案字母：答案[:：]（...）A
ANS_LETTER_RE = re.compile(r"(?:答案|答|参考答案|【答案】|参考答案：)\s*[:：]?\s*[（(]?\s*([A-E]{1,6})\s*[）)]?")
# 元素符号全小写（双字母，中文化学语境高置信 OCR 错）；排除单位词与英文常用词
LOWER_EL_SET = {
    "co", "na", "cl", "fe", "cu", "ca", "al", "ne", "ar", "kr", "xe",
    "li", "be", "ti", "mn", "ni", "zn", "ga", "ge", "as", "se", "br", "rb", "sr",
    "zr", "nb", "mo", "tc", "ru", "rh", "pd", "ag", "cd", "in", "sn", "sb", "te",
    "cs", "ba", "la", "ce", "pr", "nd", "sm", "eu", "gd", "tb", "dy", "ho", "er",
    "tm", "yb", "lu", "hf", "ta", "re", "os", "ir", "pt", "au", "hg", "tl", "pb",
    "bi", "po", "at", "ra", "ac", "th", "pa",
}
# 排除英文高频词（Clayden 原题英文句）：be in as at he no so me we si is
LOWER_EL_SET -= {"be", "in", "as", "at", "he", "no", "so", "me", "we", "si", "is"}
UNIT_WORDS = {"mg", "pm", "nm", "cm", "mm", "dm", "kg", "ml", "mol", "mol", "m", "l", "t", "v"}
LOWER_EL_RE = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(sorted(LOWER_EL_SET)) + r")(?![A-Za-z0-9])")
# 摄氏度 OCR：25oC / 25 0C；排除库仑单位 C/mol、C/g 等
DEG_OCR_RE = re.compile(r"(?<=\d)\s*[oO0]\s*C(?![a-zA-Z])")
# pH 大小写：PH= / PH值 / ph=
PH_RE = re.compile(r"\bPH\s*[=＝]|\bPH\s*值|\bph\s*[=＝]")
# 全角字母数字
FW_CHAR_RE = re.compile(r"[Ａ-Ｚａ-ｚ０-９]")
# 全角百分号
FW_PCT_RE = re.compile(r"％")
# 行尾空白
TRAIL_WS_RE = re.compile(r"[ \t]+$")
# 重复标点：中文重复或 3+ 个英文问号/感叹号；排除 LaTeX 省略号点阵 ......(1)
DUP_PUNC_RE = re.compile(r"[。，、；：？！]{2,}|[!?]{3,}")
# 全角空格
FW_SPACE_RE = re.compile(r"\u3000")
# 连续半角空格（在 math 被占位替换后的文本上检测）
DBL_SPACE_RE = re.compile(r" {2,}")
# 中文夹半角标点（中文后紧跟半角,;:!? 再跟中文）
CN_SEMI_RE = re.compile(r"[\u4e00-\u9fff][,;:!?][\u4e00-\u9fff]")
# 乱码特征（在 strip_math 后的文本上检测；□■○△▲ 为晶体结构题合法图形记号，不算乱码）
GARBLE_RE = re.compile(r"�|\\u[0-9a-fA-F]{4}|\\\\begin\{")
# 题干直接泄漏答案：题干中出现 答案：A 之类
STEM_ANS_LEAK_RE = re.compile(r"(?:答案|参考答案)\s*[:：]\s*[（(]?\s*[A-E]")
# 占位符（排除合法"原书未提供解答"标注）
PLACEHOLDER_RE = re.compile(r"待补|待填|TODO|TBD|占位|待完善|空缺|待查|需人工")

# ---------- 文本工具 ----------
def strip_math(s):
    return re.sub(r"\$[^$\n]*\$", " ", s)

def norm_text(s):
    """规范化：去空白 + 全半角标点归一 + 去中文标点；保留 math、`-`、括号（避免选项重复误报）"""
    s = s.replace(" ", "").replace("\u3000", "")
    s = s.replace("（", "(").replace("）", ")").replace("，", ",").replace("。", ".")
    s = s.replace("；", ";").replace("：", ":").replace("！", "!").replace("？", "?").replace("．", ".")
    s = re.sub(r"[、·—…“”‘’「」『』《》<>]", "", s)
    return s

def natural_key(rel: str):
    """自然排序：把路径中的数字段按数值排序"""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", rel)]

# ---------- 主扫描 ----------
def scan():
    files = []
    for root in ("04-题库", "05-真题库"):
        base = VAULT / root
        for p in sorted(base.rglob("*.md")):
            rel = p.relative_to(VAULT).as_posix()
            if any(sp in rel for sp in SKIP_DIR_PARTS):
                continue
            files.append(p)
    files.sort(key=lambda p: natural_key(p.relative_to(VAULT).as_posix()))

    issues = []          # {cat, sub, rel, stem, detail, suggest}
    ans_dist = defaultdict(lambda: defaultdict(int))  # sub库 -> 字母 -> 计数
    option_info = []     # {rel, stem, nopt, ans, opts}
    seen_stems = defaultdict(list)  # norm题干 -> [rel]

    for p in files:
        rel = p.relative_to(VAULT).as_posix()
        try:
            raw = p.read_text(encoding="utf-8")
        except Exception:
            continue
        fm, body = A.strip_fm(raw)
        if not body.strip():
            continue
        ftype = str(fm.get("type", "")).strip()
        if ftype not in QUESTION_TYPES:
            continue
        stem = p.stem

        # 分区块：题干段 / 答案段（标题后允许附加说明，如“参考答案（提炼版）”）
        m = re.search(r"^##\s*(题目|问题|题目与答案)[^\n]*$", body, re.M)
        m2 = re.search(r"^##\s*(参考答案|参考解答|答案|解答|解析|题目与答案)[^\n]*$", body, re.M)
        # 合集文件判定：正文含 ≥2 个 `## 数字.数字` 小节 或 ≥2 个 `**答案：` 标记
        is_collection = (len(re.findall(r"^##\s*\d+\.\d+\s*$", body, re.M)) >= 2
                         or len(re.findall(r"\*\*答案\s*[:：]", body)) >= 2)
        if m and (not m2 or m.end() <= m2.start()):
            stem_sec = body[m.end(): m2.start() if m2 else len(body)]
            ans_sec = body[m2.end():] if m2 else ""
        else:
            # 无独立题目标题，或 m/m2 重叠（如"## 题目与答案"）：题干段 = 标题前全部
            stem_sec = body[: m2.start()] if m2 else body
            ans_sec = body[m2.end():] if m2 else ""

        # ---- 选项检测（在题干段内）----
        opt_starts = [(mm.start(), mm.group(0)) for mm in OPT_PREFIX_RE.finditer(stem_sec)]
        # 过滤：出现在 math 里的（$...$ 内部）不算
        math_ranges = [(mm.start(), mm.end()) for mm in re.finditer(r"\$[^$\n]*\$", stem_sec)]
        def in_math(pos):
            return any(a <= pos < b for a, b in math_ranges)
        opt_starts = [(i, g) for i, g in opt_starts if not in_math(i)]

        # 取最长连续递增字母段作为选项（排除题干正文零散 A./B. 叙述；优先 A 开头段）
        if len(opt_starts) >= 2:
            def find_seg(si):
                seg = [opt_starts[si]]
                cur = ord(opt_starts[si][1][0])
                for k in range(si + 1, len(opt_starts)):
                    nxt = ord(opt_starts[k][1][0])
                    if nxt == cur + 1:
                        seg.append(opt_starts[k])
                        cur = nxt
                    else:
                        break
                return seg
            best = []
            for si in range(len(opt_starts)):
                seg = find_seg(si)
                if len(seg) >= 2 and (len(seg) > len(best) or (len(seg) == len(best) and seg[0][1].startswith("A"))):
                    best = seg
            opt_starts = best
        else:
            opt_starts = []

        # 提取选项内容：按选项前缀切分（同一行内多个 A. B. C. D. 也支持）
        opts = []
        if opt_starts:
            for idx, (pos, g) in enumerate(opt_starts):
                end = opt_starts[idx + 1][0] if idx + 1 < len(opt_starts) else len(stem_sec)
                content = stem_sec[pos + len(g): end]
                letter = g[0]
                opts.append((letter, content.strip()))
        if opts:
            letters = [l for l, _ in opts]
            seq = "".join(letters)
            if len(set(letters)) >= 2:
                optinfo = {"rel": rel, "letters": seq, "opts": opts}
                option_info.append(optinfo)

                # A1 标点混用
                sep_chars = {OPT_SEP_RE.match(g).group(1) for g in [g for _, g in opt_starts] if OPT_SEP_RE.match(g)}
                if len(sep_chars) > 1:
                    issues.append({"cat": "选项", "sub": "标点混用", "rel": rel, "stem": stem,
                                   "detail": f"选项分隔标点不一致：{'/'.join(sorted(sep_chars))}",
                                   "suggest": "统一为 `A. ` 半角点+空格"})
                # A2 字母序列异常
                if seq not in ("ABCD", "ABCDE", "ABC", "AB", "ABCDEF", "ABCDF", "ABCE", "ABDE", "ACD", "ABD", "ABC"):
                    if len(set(letters)) != len(letters):
                        issues.append({"cat": "选项", "sub": "字母重复", "rel": rel, "stem": stem,
                                       "detail": f"选项字母重复：{seq}", "suggest": "核对选项字母，去重/改正"})
                    elif len(set(letters)) >= 2:
                        issues.append({"cat": "选项", "sub": "字母跳号/缺失", "rel": rel, "stem": stem,
                                       "detail": f"选项字母序列异常：{seq}", "suggest": "核对选项是否缺项/跳号（A→B→C→D 连续）"})
                # A4 选项内容重复
                contents = [norm_text(c) for _, c in opts]
                dup_found = False
                for i in range(len(contents)):
                    for j in range(i + 1, len(contents)):
                        if contents[i] and contents[i] == contents[j]:
                            issues.append({"cat": "选项", "sub": "选项重复", "rel": rel, "stem": stem,
                                           "detail": f"选项 {letters[i]} 与 {letters[j]} 内容相同：{opts[i][1][:40]}",
                                           "suggest": "核对 OCR，两个选项不应相同"})
                            dup_found = True
                            break
                    if dup_found:
                        break
                # A3 选项过少
                uniq_letters = set(letters)
                if len(uniq_letters) == 2 and "A" in uniq_letters and "B" in uniq_letters:
                    issues.append({"cat": "选项", "sub": "选项过少", "rel": rel, "stem": stem,
                                   "detail": "仅 2 个选项（A/B），确认是否为判断题误标选择题",
                                   "suggest": "判断题改为“正确/错误”表述，或补齐选项"})

        # ---- 答案检测 ----
        ans_letters = ""
        am = ANS_LETTER_RE.search(ans_sec)
        if am:
            ans_letters = am.group(1)
            # 答案字母越界 / 多字母
            if opts:
                uniq_letters = set(letters)
                bad = [c for c in ans_letters if c not in uniq_letters and c not in "E"]
                if bad:
                    issues.append({"cat": "答案", "sub": "答案越界", "rel": rel, "stem": stem,
                                   "detail": f"答案字母 {ans_letters} 超出选项范围 {seq}",
                                   "suggest": "核对答案与选项字母"})
                if len(ans_letters) > 1:
                    issues.append({"cat": "答案", "sub": "答案多字母", "rel": rel, "stem": stem,
                                   "detail": f"答案含多字母：{ans_letters}（若为多选请确认）",
                                   "suggest": "单题应为单选；多选需注明“多选”"})
            # 答案分布统计
            for c in ans_letters:
                if c in "ABCDE":
                    d = rel.split("/")[1] if len(rel.split("/")) > 1 else rel
                    ans_dist[d][c] += 1

        # ---- B. OCR 特征 ----
        full = stem_sec + "\n" + ans_sec
        plain = strip_math(full)
        math_mask = re.sub(r"\$[^$\n]*\$", "M", full)  # math 整体占位（用于空格检测）
        for mm in DEG_OCR_RE.finditer(plain):
            ctx = plain[max(0, mm.start() - 8): mm.end() + 6]
            if re.search(r"C\s*[/／]", ctx):  # C/mol 库仑单位
                continue
            issues.append({"cat": "OCR", "sub": "摄氏度误识", "rel": rel, "stem": stem,
                           "detail": f"疑似 °C 被 OCR 为：…{ctx}…", "suggest": "改为 `°C`（或 `℃`）"})
        for mm in PH_RE.finditer(plain):
            ctx = plain[max(0, mm.start() - 4): mm.end() + 4]
            issues.append({"cat": "OCR", "sub": "pH大小写", "rel": rel, "stem": stem,
                           "detail": f"疑似 pH 大小写错误：…{ctx}…", "suggest": "统一为 `pH`（PH3 膦除外）"})
        fw = FW_CHAR_RE.findall(full)
        if fw:
            issues.append({"cat": "OCR", "sub": "全角字符", "rel": rel, "stem": stem,
                           "detail": f"全角字母/数字：{' '.join(fw[:6])}", "suggest": "改为半角（选项字母必须半角）"})
        if FW_PCT_RE.search(plain):
            issues.append({"cat": "OCR", "sub": "全角百分号", "rel": rel, "stem": stem,
                           "detail": "出现全角 `％`", "suggest": "改为半角 `%`"})
        fwdot = OPT_FW_DOT_RE.search(stem_sec)
        if fwdot:
            issues.append({"cat": "OCR", "sub": "全角句点选项", "rel": rel, "stem": stem,
                           "detail": f"选项用全角点 `{fwdot.group(0)}`", "suggest": "改为 `A. ` 半角点"})
        low_el = []
        for m_el in LOWER_EL_RE.finditer(plain):
            w = m_el.group(1)
            pre = plain[max(0, m_el.start() - 4): m_el.start()]
            post = plain[m_el.end(): m_el.end() + 1]
            if w in UNIT_WORDS and re.search(r"\d", pre):  # 单位（如 5 pm / 12 mg）
                continue
            if re.search(r"\d\s*$", pre):  # 数字紧跟（低置信）
                continue
            if not re.search(r"[\u4e00-\u9fff]", pre[-1:] + post):  # 前后无中文 → 英文句，跳过
                continue
            low_el.append(w)
        if low_el:
            issues.append({"cat": "OCR", "sub": "元素符号小写", "rel": rel, "stem": stem,
                           "detail": f"疑似元素符号被 OCR 成小写：{' '.join(sorted(set(low_el))[:6])}",
                           "suggest": "核对元素符号大小写（如 Co/Na/Cl）"})

        # ---- C. 题干/答案完整性 ----
        stem_text = re.sub(r"^[0-9]+\.\s*", "", stem_sec.strip())
        stem_plain = norm_text(stem_text)
        if len(stem_plain) < 8 and not opts and not is_collection:
            issues.append({"cat": "题干答案", "sub": "题干过短", "rel": rel, "stem": stem,
                           "detail": f"题干文本极短（{len(stem_plain)} 字）：{stem_sec.strip()[:40]}",
                           "suggest": "核对是否题干缺失/只留题号"})
        if not m and not m2:
            pass  # 无分隔符的题（罕见），跳过
        elif not m2 and not re.search(r"^\s*>?\s*\*\*答案|\*\*答案\s*[:：]|^答案\s*[:：]", body, re.M):
            issues.append({"cat": "题干答案", "sub": "无答案块", "rel": rel, "stem": stem,
                           "detail": "缺 `## 参考答案/解答/答案` 区块（亦无 `**答案**` 标记）",
                           "suggest": "补答案区块"})
        if PLACEHOLDER_RE.search(ans_sec[:200]) and len(ans_sec) < 300:
            issues.append({"cat": "题干答案", "sub": "答案占位", "rel": rel, "stem": stem,
                           "detail": f"答案区疑似占位：{ans_sec.strip()[:60]}",
                           "suggest": "按 OCR 原文补全"})
        if STEM_ANS_LEAK_RE.search(stem_text) and not is_collection:
            issues.append({"cat": "题干答案", "sub": "题干含答案", "rel": rel, "stem": stem,
                           "detail": "题干出现“答案：X”形式（疑似答案泄漏进题干）",
                           "suggest": "核对题干是否把答案写进题干，移至参考答案区"})
        if GARBLE_RE.search(plain):
            issues.append({"cat": "题干答案", "sub": "乱码特征", "rel": rel, "stem": stem,
                           "detail": "出现乱码特征字符", "suggest": "修复乱码"})

        # ---- D. 格式 ----
        for mm in TRAIL_WS_RE.finditer(raw):
            line = raw[: mm.start()].rsplit("\n", 1)[-1]
            issues.append({"cat": "格式", "sub": "行尾空白", "rel": rel, "stem": stem,
                           "detail": f"行尾空白：`{line[-30:]}`", "suggest": "删除行尾空格"})
            break  # 每文件报一次即可
        for mm in DUP_PUNC_RE.finditer(plain):
            ctx = plain[max(0, mm.start() - 8): mm.end() + 8]
            issues.append({"cat": "格式", "sub": "重复标点", "rel": rel, "stem": stem,
                           "detail": f"重复标点：…{ctx}…", "suggest": "删去重复标点"})
            break
        if FW_SPACE_RE.search(raw):
            issues.append({"cat": "格式", "sub": "全角空格", "rel": rel, "stem": stem,
                           "detail": "含全角空格 `　`", "suggest": "替换为半角空格"})
        if FW_SPACE_RE.search(raw):
            issues.append({"cat": "格式", "sub": "全角空格", "rel": rel, "stem": stem,
                           "detail": "含全角空格 `　`", "suggest": "替换为半角空格"})
        if CN_SEMI_RE.search(plain):
            issues.append({"cat": "格式", "sub": "中文夹半角标点", "rel": rel, "stem": stem,
                           "detail": "中文字符间夹半角标点", "suggest": "统一为全角中文标点"})

        # ---- 重复题干（跨文件，仅记录非空题干）----
        if len(stem_plain) >= 12:
            seen_stems[stem_plain].append(rel)

    # 重复题干组
    dup_groups = {s: v for s, v in seen_stems.items() if len(v) >= 2}

    # 排序 issues：按 rel 自然序
    issues.sort(key=lambda x: natural_key(x["rel"]))

    result = {
        "issues": issues,
        "dup_stem_groups": dup_groups,
        "ans_dist": {k: dict(v) for k, v in ans_dist.items()},
    }
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- MD 报告 ----
    by_cat = defaultdict(list)
    for x in issues:
        by_cat[x["cat"]].append(x)
    lines = ["# 2026-08-31 题库逐题质量扫描报告（机械扫描）", "",
             f"> 扫描范围：04-题库 + 05-真题库（type=题目/真题/例题，共 {len(files)} 个 md）",
             f"> 生成时间：2026-08-31；方法：正则全量扫描（只读），需人工抽样核验后采纳", ""]
    for cat in ("OCR", "选项", "答案", "题干答案", "格式"):
        sub_items = by_cat.get(cat, [])
        lines.append(f"## {cat}类问题（{len(sub_items)}）")
        if not sub_items:
            lines.append("_无_")
        for x in sub_items:
            lines.append(f"- **{x['rel']}**｜{x['sub']}：{x['detail']}")
            lines.append(f"  - 建议：{x['suggest']}")
        lines.append("")
    # 重复题干
    lines.append(f"## 跨文件重复题干（{len(dup_groups)} 组，供查重参考）")
    for s, v in sorted(dup_groups.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"- 题干摘要 `{s[:40]}`… 出现于 {len(v)} 处：{'、'.join(v[:6])}")
    lines.append("")
    # 答案分布
    lines.append("## 答案分布（每子库，供检查选项顺序合理性）")
    for k, v in sorted(ans_dist.items()):
        total = sum(v.values())
        ratio = " ".join(f"{c}:{v.get(c, 0)}" for c in "ABCDE")
        lines.append(f"- **{k}**（{total}）{ratio}")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    # 控制台摘要
    print(f"受检文件: {len(files)}")
    for cat in ("OCR", "选项", "答案", "题干答案", "格式"):
        print(f"  {cat}: {len(by_cat.get(cat, []))}")
    print(f"  重复题干组: {len(dup_groups)}")
    print("→", OUT_MD)

if __name__ == "__main__":
    scan()
