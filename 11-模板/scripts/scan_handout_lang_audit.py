#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生讲义语言体检扫描器 —— 《11-模板/讲义语言规范》配套机检工具。

检测项（对应规范条款）：
  pseudo_callout   伪 callout（`> **标题**：` 独立引用块）          规范 §2.1
  callout          正式 callout 计数与密度                          规范 §2.3
  warning_prefix   `⚠` 加粗前缀行                                   规范 §2.2
  fragments        单句碎片段（<N 字孤立普通段落，豁免图注/公式/表）  规范 §4.3
  negative_words   负面词命中（含白名单豁免判定）                    规范 §3
  motto_dupe       引号长句（口诀）逐字重复                          规范 §5.3
  quickref_names   收尾节命名识别                                    规范 §6.1
  dup_pairs        跨区域疑似重复对（规范化 8-gram 相似）             规范 §1

用法：
  python -X utf8 scan_handout_lang_audit.py --path <md路径> [--path <md2> ...]
      [--out-dir <报告目录>] [--json] [--frag-len 25] [--dup-n 8] [--dup-th 0.35]
输出：控制台摘要 + MD 报告（--out-dir 缺省与首文件同目录）；--json 另出 JSON。
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

# ---------------- 负面词表（规范 §3.1 首版） ----------------
NEGATIVE_WORDS = {
    "塞进": "填入/排布至",
    "划算": "能量上更有利",
    "走人": "离去",
    "不给力": "离去能力弱/亲核性弱",
    "抢答": "过早下结论",
    "翻盘": "按语境改写（如「熵项贡献超过焓项」）",
    "踢走": "排出（「通俗理解」栏带引号可豁免）",
    "纠结": "竞争激烈/判定依赖试剂（口诀内按规范 §5.3 处理）",
}
# 白名单豁免：词 -> 豁免上下文正则（命中则不计负面，单列 whitelist_hits）
WHITELIST_PATTERNS = {
    "纠结": [r"“[^”]*纠结[^”]*”", r"「[^」]*纠结[^」]*」"],
}

# 术语异形词（规范 §8.1 词表）：禁用形 -> 规范词
TERM_VARIANTS = {
    "阿佛加德罗": "阿伏伽德罗",
    "阿伏加德罗": "阿伏伽德罗",
    "稀烃": "烯烃",
}

# Weasel 词（规范 §9.2）：匿名权威/跳步遮蔽/预设断言初筛词表
WEASEL_WORDS = {
    "研究表明": "写实名出处（如「由 Hess 定律可知」）或删",
    "众所周知": "删或写实名出处",
    "人们认为": "删或实名",
    "显然": "省步须可一步补全，否则补步；合法用「可得/即得」",
    "显然易见": "同上",
    "不难发现": "同上",
}

# 句式杂糅特征词对（规范 §7.1，CY/T 266 条目 1-11）
HYBRID_SYNTAX_RE = re.compile(
    r"原因是.{0,24}造成|目的是.{0,16}为目的|围绕.{0,16}为中心|关键在于.{0,16}的问题|由于.{0,20}的结果"
)

# 数值范围连字符（规范 §7.3，GB/T 15835）：应为「～」；豁免化学式位次连字符
UNIT_RANGE_RE = re.compile(r"\d\s*[-—]\s*\d+\s*(mL|L|mol|kJ|kJ/mol|K|°C|eV|pm|nm|g)\b")

# 收尾节命名归一目标（规范 §6.1）
QUICKREF_TARGET = "本讲速查"
SUMMARY_TARGET = "本讲小结"
QUICKREF_VARIANTS = ("本节总结", "核心速查卡", "速查卡", "知识速查")

CALLOUT_RE = re.compile(r"^>\s*\[!(tip|warning|info|note|abstract|example|quote|summary)\]", re.I)
PSEUDO_RE = re.compile(r"^>\s*\*\*([^*]{2,40})\*\*\s*[：:]")

# S0 豁免白名单（推广批校准固化，2026-09-23）：下列标题的 `> **…**：` 是**结构位**
# 而非病灶位（frontmatter 元信息块 / 题目区结构 / 来源登记 / 收尾结构）——
# 试点三份改造后残留的 15/11/9 个与第一轮校准样本（数学工具第1讲 8 个全豁免）
# 均由此类构成。命中不计 pseudo_callout，单列 structural_exempt 保留可审计性。
PSEUDO_STRUCTURAL_EXEMPT = {
    # 元信息 / frontmatter 块
    "对应专题", "建议使用方式", "前置要求", "深度边界", "课时", "版本说明",
    "本讲定位", "对应考纲", "对应备课大纲", "下节衔接", "本讲解决的问题",
    "关联讲义", "考纲对应", "适用", "轮次导航", "考纲覆盖", "编排说明",
    "立项依据", "本章定位", "使用边界", "复习提示", "学习目标", "目录",
    "符号约定", "题源", "来源", "出处", "图片说明", "图源", "使用建议",
    # 题目区结构
    "题目", "答案", "解析", "纠正", "练习题", "例题", "思考题", "变式",
    "考点", "竞赛考点", "竞赛链接", "真题提醒", "题干", "设问",
    # 收尾结构
    "方法总结", "本章小结", "习题与思考", "本节总结",
}
PSEUDO_STRUCTURAL_EXEMPT_RE = re.compile(
    r"^(误区\s*[一二三四五六七八九十\d]+|第\s*[一二三四五六七八九十\d]+\s*(问|步|类|部分)|解\s*\d*|辨析\s*\d+|情境\s*\d+)$"
)
WARN_PREFIX_RE = re.compile(r"⚠")
IMG_EMBED_RE = re.compile(r"!\[\[|!\[")
FIGCAPTION_RE = re.compile(r"^\*[^*]+\*\s*$")          # *图 N …* 斜体图注
TABLE_ROW_RE = re.compile(r"^\s*\|")
HEADING_RE = re.compile(r"^#{1,6}\s")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.、)])\s")
MATH_MARK_RE = re.compile(r"\$|\\[a-zA-Z]+|^\\\[")


def strip_math(text: str) -> str:
    """去掉 LaTeX 命令与 math 定界符，供碎片段长度与重复规范化用。"""
    t = re.sub(r"\$\$?[^$]*\$\$?", "F", text)      # display/inline math → 占位
    t = re.sub(r"\\[a-zA-Z]+", "F", t)
    t = t.replace("$", "")
    return t


def visible_len(text: str) -> int:
    """粗略可见长度：去 markdown 标记与数学占位后的字符数。"""
    t = strip_math(text)
    t = re.sub(r"[*_`>#|\[\]()]", "", t)
    t = re.sub(r"\s", "", t)
    return len(t)


_DUP_STRIP_RE = re.compile(r"[\W_]+", re.UNICODE)   # 删全部非字母数字汉字（中文 dup 规范化最稳，无转义陷阱）


def normalize_for_dup(sentence: str) -> str:
    """重复判定用规范化：去 LaTeX、标记、空白与全部标点。"""
    t = strip_math(sentence)
    t = re.sub(r"\[!\w+\]", "", t)
    t = re.sub(r"[*_`#>|]", "", t)
    return _DUP_STRIP_RE.sub("", t)


def split_sentences(lines_with_no: list[tuple[int, str]]):
    """把 (行号, 文本) 序列按句号类标点切句，返回 [(行号, 规范化串, 原句)]。"""
    out = []
    buf_line, buf_chars = None, []
    for ln, text in lines_with_no:
        for ch in text:
            buf_chars.append(ch)
            if ch in "。！？；;!?":
                sent = "".join(buf_chars).strip()
                buf_chars = []
                norm = normalize_for_dup(sent)
                if len(norm) >= 12:
                    out.append((buf_line if buf_line is not None else ln, norm, sent.strip()))
        if buf_chars and not "".join(buf_chars).isspace():
            pass  # 跨行句子保留缓冲，行号取首行
        if buf_line is None and buf_chars:
            buf_line = ln
        if not buf_chars:
            buf_line = None
    if buf_chars:
        sent = "".join(buf_chars).strip()
        norm = normalize_for_dup(sent)
        if len(norm) >= 12 and buf_line is not None:
            out.append((buf_line, norm, sent.strip()))
    return out


def find_dup_pairs(sentences, n: int = 8, th: float = 0.35, max_report: int = 40):
    """规范化句子的字符 n-gram 倒排 → 候选对 → 相似度过滤。"""
    grams: dict[str, list[int]] = {}
    gram_sets: list[set[str]] = []
    for idx, (_, norm, _) in enumerate(sentences):
        gs = {norm[i:i + n] for i in range(0, max(1, len(norm) - n + 1))}
        gram_sets.append(gs)
        for g in gs:
            grams.setdefault(g, []).append(idx)
    pair_count: Counter = Counter()
    for g, idxs in grams.items():
        if len(idxs) > 60:      # 高频 gram（如常见术语）不做候选来源
            continue
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                pair_count[(idxs[a], idxs[b])] += 1
    reported = []
    seen = set()
    for (a, b), shared in pair_count.most_common():
        if shared < 2:
            continue
        union = len(gram_sets[a] | gram_sets[b])
        sim = shared / union if union else 0.0
        if sim >= th and (a, b) not in seen:
            seen.add((a, b))
            la, na, sa = sentences[a]
            lb, nb, sb = sentences[b]
            # 自报告排除：完全同句且同行邻近的平凡重复也算（有行号定位即可）
            reported.append({
                "line_a": la, "line_b": lb, "sim": round(sim, 2),
                "text_a": sa[:80], "text_b": sb[:80],
            })
        if len(reported) >= max_report:
            break
    reported.sort(key=lambda r: -r["sim"])
    return reported


def scan_file(path: Path, frag_len: int, dup_n: int, dup_th: float) -> dict:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    res = {
        "file": str(path), "total_lines": len(lines),
        "pseudo_callout": [], "callout": [], "warning_prefix": [],
        "structural_exempt": [],
        "fragments": [], "negative_words": [], "whitelist_hits": [],
        "motto_dupe": [], "quickref_names": [], "dup_pairs": [],
        "term_variants": [], "weasel_words": [], "hybrid_syntax": [], "unit_range": [],
    }
    # ---- 区块状态机：图注/公式块/引用块/速查节识别 ----
    in_math = False
    in_answer = False
    for i, line in enumerate(lines, 1):
        s = line.strip()
        # $$ 状态机：按行内 $$ 出现次数的奇偶翻转（兼容 单行完整块/跨行块/行尾缀文字 等全部形态）
        cnt = s.count("$$")
        m0 = in_math
        if cnt % 2 == 1:
            in_math = not in_math
        if m0 or in_math or (cnt >= 2):
            continue  # 本行含公式块内容，跳过其余检测
        if HEADING_RE.match(s):
            # 答案区起点（进入后不再计碎片段/伪callout——答案区有自己的纪律但形态不同）
            if re.search(r"参考答案|^#+\s*.*答案", s) and "练习" in raw[max(0, raw.find(s) - 200):raw.find(s)]:
                in_answer = True
            for kw in (QUICKREF_TARGET, SUMMARY_TARGET):
                if kw in s:
                    res["quickref_names"].append({"line": i, "heading": s.strip("# ").strip(), "matched": kw})
            for v in QUICKREF_VARIANTS:
                if v in s:
                    res["quickref_names"].append({"line": i, "heading": s.strip("# ").strip(), "matched": f"变体:{v}"})
        if CALLOUT_RE.match(s):
            m = CALLOUT_RE.match(s)
            res["callout"].append({"line": i, "type": m.group(1).lower()})
            continue
        if PSEUDO_RE.match(s) and not in_answer:
            title = PSEUDO_RE.match(s).group(1)
            if title.strip() in PSEUDO_STRUCTURAL_EXEMPT or PSEUDO_STRUCTURAL_EXEMPT_RE.match(title.strip()):
                res["structural_exempt"].append({"line": i, "title": title})
            else:
                res["pseudo_callout"].append({"line": i, "title": title})
        if WARN_PREFIX_RE.search(s) and not FIGCAPTION_RE.match(s):
            res["warning_prefix"].append({"line": i, "text": s[:60]})
        # 负面词
        for w in NEGATIVE_WORDS:
            if w in s:
                wl = any(re.search(p, s) for p in WHITELIST_PATTERNS.get(w, []))
                entry = {"line": i, "word": w, "suggest": NEGATIVE_WORDS[w], "text": s[:60]}
                (res["whitelist_hits"] if wl else res["negative_words"]).append(entry)
        # 术语异形词（§8）
        for w, std in TERM_VARIANTS.items():
            if w in s:
                res["term_variants"].append({"line": i, "word": w, "suggest": std, "text": s[:60]})
        # Weasel 词（§9.2）
        for w, sug in WEASEL_WORDS.items():
            if w in s:
                res["weasel_words"].append({"line": i, "word": w, "suggest": sug, "text": s[:60]})
        # 句式杂糅（§7.1）
        m = HYBRID_SYNTAX_RE.search(s)
        if m:
            res["hybrid_syntax"].append({"line": i, "pattern": m.group(0)[:24], "text": s[:60]})
        # 数值范围连字符（§7.3）
        m = UNIT_RANGE_RE.search(s)
        if m:
            res["unit_range"].append({"line": i, "match": m.group(0), "text": s[:60]})
    # ---- 单句碎片段（普通段落，前后空行，豁免图注/公式/表/列表/标题/引用） ----
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith(">") or TABLE_ROW_RE.match(s) or HEADING_RE.match(s) \
                or LIST_RE.match(s) or FIGCAPTION_RE.match(s) or IMG_EMBED_RE.search(s) \
                or MATH_MARK_RE.search(s) or s.startswith("<!--") or s.startswith("---"):
            continue
        prev_blank = i == 1 or not lines[i - 2].strip()
        next_blank = i == len(lines) or not lines[i].strip()
        if prev_blank and next_blank and visible_len(s) < frag_len and not s.endswith(("：", ":")):
            res["fragments"].append({"line": i, "text": s[:50], "len": visible_len(s)})
    # ---- 口诀/引号长句逐字重复 ----
    quoted = re.findall(r"[“\"]([^”\"]{12,})[”\"]", raw)
    for text, cnt in Counter(quoted).items():
        if cnt >= 2:
            res["motto_dupe"].append({"count": cnt, "text": text[:60]})
    # ---- 跨区域重复对 ----
    body_lines = [(i, l) for i, l in enumerate(lines, 1) if l.strip()]
    sentences = split_sentences(body_lines)
    res["dup_pairs"] = find_dup_pairs(sentences, n=dup_n, th=dup_th)
    # ---- 密度 ----
    res["callout_density_per_100"] = round(len(res["callout"]) * 100 / max(1, len(lines)), 2)
    res["callout_limit"] = min(12, math.ceil(len(lines) / 100))
    return res


def md_report(reports: list[dict]) -> str:
    out = ["# 学生讲义语言体检报告（scan_handout_lang_audit）\n"]
    out.append("> 配套规范：[[11-模板/讲义语言规范]]。本报告为机检基线/复核数据，删除裁决需人工确认。\n")
    for r in reports:
        out.append(f"\n## {Path(r['file']).name}（{r['total_lines']} 行）\n")
        out.append("| 指标 | 值 | 阈值/说明 |")
        out.append("|:--|--:|:--|")
        out.append(f"| 伪callout | {len(r['pseudo_callout'])} | 目标 0（§2.1 三分法处置） |")
        out.append(f"| 结构性豁免 | {len(r.get('structural_exempt', []))} | S0 白名单，登记即可 |")
        out.append(f"| 正式callout | {len(r['callout'])}（{r['callout_density_per_100']}/百行） | ≤{r['callout_limit']} 个且 ≤1.0/百行 |")
        out.append(f"| ⚠前缀行 | {len(r['warning_prefix'])} | 目标 0 |")
        out.append(f"| 单句碎片段 | {len(r['fragments'])} | ≤3 |")
        out.append(f"| 负面词命中 | {len(r['negative_words'])} | 白名单外 0 |")
        out.append(f"| 白名单豁免命中 | {len(r['whitelist_hits'])} | 登记即可 |")
        out.append(f"| 术语异形词 | {len(r['term_variants'])} | 按 §8 词表替换，0 |")
        out.append(f"| Weasel 词 | {len(r['weasel_words'])} | 人工复核后 0 |")
        out.append(f"| 句式杂糅特征 | {len(r['hybrid_syntax'])} | 人工复核后 0 |")
        out.append(f"| 数值范围连字符 | {len(r['unit_range'])} | 改「～」，0 |")
        out.append(f"| 口诀逐字重复 | {len(r['motto_dupe'])} | 0 |")
        out.append(f"| 疑似重复对 | {len(r['dup_pairs'])} | 人工裁决后残留 0 |")
        out.append(f"| 收尾节命名 | {len(r['quickref_names'])} 处 | 「本讲速查」+「本讲小结」 |")
        for key, cap in (("pseudo_callout", 60), ("fragments", 40), ("negative_words", 30),
                         ("warning_prefix", 20), ("motto_dupe", 10), ("dup_pairs", 25),
                         ("whitelist_hits", 10), ("quickref_names", 12),
                         ("term_variants", 20), ("weasel_words", 20),
                         ("hybrid_syntax", 15), ("unit_range", 15),
                         ("structural_exempt", 60)):
            items = r[key]
            if not items:
                continue
            out.append(f"\n### {key}（{len(items)}）\n")
            for it in items[:cap]:
                if key == "pseudo_callout":
                    out.append(f"- L{it['line']} `> **{it['title']}**：`")
                elif key == "structural_exempt":
                    out.append(f"- L{it['line']} `> **{it['title']}**：`")
                elif key == "dup_pairs":
                    out.append(f"- sim={it['sim']} L{it['line_a']}↔L{it['line_b']}：`{it['text_a']}` ↔ `{it['text_b']}`")
                elif key == "motto_dupe":
                    out.append(f"- ×{it['count']} `{it['text']}`")
                elif key in ("negative_words", "term_variants", "weasel_words"):
                    out.append(f"- L{it['line']} 【{it['word']}→{it['suggest']}】`{it['text']}`")
                elif key == "hybrid_syntax":
                    out.append(f"- L{it['line']} 杂糅型`{it['pattern']}``{it['text']}`")
                elif key == "unit_range":
                    out.append(f"- L{it['line']} `{it['match']}` `{it['text']}`")
                elif key == "fragments":
                    out.append(f"- L{it['line']} ({it['len']}字) `{it['text']}`")
                else:
                    out.append(f"- L{it['line']} `{it.get('text', it.get('heading', ''))}`")
            if len(items) > cap:
                out.append(f"- …（其余 {len(items) - cap} 条见 JSON）")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="学生讲义语言体检（配套《讲义语言规范》）")
    ap.add_argument("--path", action="append", required=True, help="讲义 md 路径，可多次")
    ap.add_argument("--out-dir", default=None, help="报告输出目录（缺省与首个文件同目录）")
    ap.add_argument("--json", action="store_true", help="同时输出 JSON")
    ap.add_argument("--frag-len", type=int, default=25, help="碎片段长度阈值（默认25字）")
    ap.add_argument("--dup-n", type=int, default=8, help="重复检测 n-gram 长度")
    ap.add_argument("--dup-th", type=float, default=0.35, help="重复相似度阈值")
    args = ap.parse_args()

    reports = []
    for p in args.path:
        path = Path(p)
        if not path.exists():
            print(f"[SKIP] 不存在: {path}", file=sys.stderr)
            continue
        reports.append(scan_file(path, args.frag_len, args.dup_n, args.dup_th))
    if not reports:
        print("无可扫描文件", file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir) if args.out_dir else Path(reports[0]["file"]).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = "语言体检-" + "-".join(re.findall(r"([\u4e00-\u9fff5]+讲|附录)", Path(reports[0]["file"]).stem))[:40] or "语言体检"
    md_path = out_dir / f"语言体检报告-{Path(reports[0]['file']).stem}.md"
    md_path.write_text(md_report(reports), encoding="utf-8")
    if args.json:
        (out_dir / f"语言体检报告-{Path(reports[0]['file']).stem}.json").write_text(
            json.dumps(reports, ensure_ascii=False, indent=1), encoding="utf-8")

    # 控制台摘要
    print(f"{'文件':<36} 伪cal 正式 ⚠ 碎片 负面 重复对 收尾名")
    for r in reports:
        print(f"{Path(r['file']).stem[:34]:<36} {len(r['pseudo_callout']):>4} {len(r['callout']):>4} "
              f"{len(r['warning_prefix']):>3} {len(r['fragments']):>4} {len(r['negative_words']):>4} "
              f"{len(r['dup_pairs']):>5} {len(r['quickref_names']):>4}")
    print(f"\n报告: {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
