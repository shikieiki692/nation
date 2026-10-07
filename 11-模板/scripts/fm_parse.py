#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全库 frontmatter 字段解析器（**唯一正确口径**）。

🔴 这一天在同一个坑上栽了六次，全部源于「YAML 数组有多种书写形态」：
   ① 同数组  knowledge_points: ["[[A]]", "[[B]]"]          —— tags/aliases 都有
   ② 跨行数组  aliases: [别名1, 别名2,\n  别名3]                —— Clapeyron方程页
   ③ 块列表    knowledge_points:\n  - "[[A]]"
   ④ 空值      aliases:      （换行后无内容）
   ⑤ 值内含逗号  aliases: ["Clausius-Clapeyron 方程", 蒸气压]
   ⑥ 字段取值不能对整段 frontmatter 抓 wikilink（source_file/cross_references 会被误算）

**唯一规则：判「键是否存在」只看键名；取值必须限定在该字段的边界内；
数组要支持跨行与块列表两种形态。**
"""
import re

FM = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", re.S)


def split_fm(text):
    """返回 (frontmatter 文本, 正文)；无 frontmatter 时 ('', text)"""
    m = FM.match(text.replace("\r\n", "\n"))
    return (m.group(1), text[m.end():]) if m else ("", text)


def has_key(fm, key):
    """判键是否存在——**只认键名**，不管值写成哪种形态"""
    return bool(re.search(r"(?m)^%s[ \t]*:" % re.escape(key), fm))


def get_list_field(fm, key):
    r"""取数组/块列表字段的值（list[str]）。

    🔴 实现要点：**不能用非贪婪的\[|\[.*?\]** 去截数组内容——库内 KP 字段全是
    形如 knowledge_points: ["[[A]]", "[[B]]"] 的写法，非贪婪会匹配到 **wikilink 自带的
    第一个 ]**，把 ["[[A]]","[[B]]"] 截成 ["[[A"]。故这里**手工配平方括号**扫描。
    """
    km = re.search(r"(?m)^%s[ \t]*:" % re.escape(key), fm)
    if not km:
        return []
    i = km.end()
    rest = fm[i:]
    # 跳过空格
    j = 0
    while j < len(rest) and rest[j] in " \t":
        j += 1
    if j < len(rest) and rest[j] == "[":
        depth = 0
        for k in range(j, len(rest)):
            if rest[k] == "[":
                depth += 1
            elif rest[k] == "]":
                depth -= 1
                if depth == 0:
                    raw = rest[j + 1:k].replace("\n", " ")
                    out = []
                    for x in raw.split(","):
                        x = x.strip().strip("'").strip('"').strip()
                        if x and x not in ("(空)", "~", "null"):
                            out.append(x)
                    return out
        return []
    # 块列表：key: 换行 - item。⚠️ rest 已去掉 `key:` 前缀，故直接匹配行首缩进 + `-`
    bm = re.match(r"[ \t]*\n((?:[ \t]*-[ \t]*.*(?:\n|$))*)", rest)
    if bm:
        out = []
        for x in re.findall(r"(?m)^[ \t]*-[ \t]*(.+?)[ \t]*$", bm.group(1)):
            x = x.strip().strip("'").strip('"').strip()
            if x and x not in ("(空)", "~", "null"):
                out.append(x)
        return out
    # 标量：key: value（2026-10-07 补）。
    # ⚠️ 此前一直返回 []，被误当成「空值」的正确行为 —— 实则标量**有值**，
    #    会让 `knowledge_points: "[[X]]"` 这类卡被判成无 KP。
    rest2 = rest.lstrip(" \t")
    if rest2 and not rest2.startswith(("[", "|", ">", "#", "\n", "-")):
        first = rest2.split("\n")[0].strip()
        first = first.strip("'").strip('"').strip()
        if first and first not in ("(空)", "~", "null"):
            return [first]
    return []


def get_wikilinks_field(fm, key):
    """取某字段里的 [[...]]（**只限该字段**，不做整段匹配）"""
    return re.findall(r"\[\[([^\]\|]+)\]\]", "\n".join(get_list_field(fm, key)))


def kp_index(kb_dir):
    """建立知识点索引：{'names': set, 'alias': {别名: {页名…}}}，三种数组形态都支持"""
    import os
    names, alias = set(), {}
    for b, d, fs in os.walk(kb_dir):
        for f in fs:
            if not f.endswith(".md"):
                continue
            nm = os.path.splitext(f)[0]
            names.add(nm)
            fm, _ = split_fm(open(os.path.join(b, f), encoding="utf-8-sig", errors="replace").read())
            for a in get_list_field(fm, "aliases"):
                alias.setdefault(a, set()).add(nm)
    return names, alias

# ══════════════════════════════════════════════════════════════════
# 答案区识别（2026-10-07 并入）
# ──────────────────────────────────────────────────────────────────
# 在役题目卡的答案区有**四种书写形态**，早期各体检脚本只认 `## 参考答案`，
# 导致 **465 张**卡被误判为「无答案区」（异形标题 304 答案 / 115 解析要点·解答 / …），
# 另有 355 张把答案放进 `<details>`、577 张为「答案见卷册」的外链型。
#
# ⚠️ 外链型**不是缺陷**：卡内原话「派生文件不复制卷内 OCR 答案
#   （源答案文本存在跨题粘连等缺陷，复制会引入错误）」——是有意的设计决定。
#
# ⚠️ 两条实测得来的判据（别再拍脑袋改）：
#   ① 「有实体答案」不能用字数阈值：'答案是 B' 只有 4 字，库内还有 '有;无;有'
#      这种短序列答案 ⇒ 判据是「去结构符后非空 且 非外链指引」。
#   ② details 必须排在「**答案：**」标记之前：多数折叠块内部就有该标记，
#      先匹配标记会把整块答案截成一行。

# ── 答案区标题的异形写法 ──
# ⚠️ 顺序有意义：先匹配更具体的（答案与解析 在 答案 之前，否则「答案」会先命中）
# 2026-10-07 加「后缀词」形态：## 参考答案要点 / ## 答案与解析（详解）等。
# ⚠️ 后缀词表是**有限白名单**，不放开成 `参考答案.*`——
#    否则「参考答案见 [[卷-01]] 的参考答案区」这类指针句也会被当标题（外链型判不出来）。
_ANS_SUFFIX = r"(?:要点|详解|汇总|对照|与解析|与解答|说明|详解与解析)?"
_ANS_HEAD = re.compile(
    r"(?m)^(#{1,6})[ \t]*(?:参考解答|参考答案与解析|参考答案|答案与解析|答案解析|"
    r"解析要点|详解|解答|答案|解析)" + _ANS_SUFFIX + r"[ \t]*(?:[（(][^）)\n]{0,12}[）)])?[ \t]*[:：]?[ \t]*$"
)
# 加粗标记型：**答案：** / **参考答案：**
_ANS_MARK = re.compile(r"(?m)^[ \t]*(?:>[ \t]*)?\*\*[ \t]*(?:参考)?答案(?:[ \t]*[:：]|[ \t]*\*\*)")
# 外链型：答案区只写「答案见 [[…]] 的参考答案区」
# 外链型：答案区只写指针而非答案。
# ⚠️ 2026-10-07 放宽：原式只认「答案见/答案在」，但库里有「> 见 [[卷-01]] 的参考答案区」
#    这类**省略主语**的写法（段边界修复后暴露：这类段被判成有实体答案）。
#    判据收紧为：短段 ＋ 含 wikilink ＋ 含「见/参见/详见/答案」任一 ⇒ 视为外链指针。
_EXT_REF = re.compile(r"(?:答案(?:见|在)|见|参见|详见)[^\n]{0,24}?\[\[")
# 折叠块
_DET = re.compile(r"(?s)<details[^>]*>(.*?)</details>")
# Obsidian callout 整块：`> [!warning] 标题` + 后续连续的 `>` 行（2026-10-07 加，
# 用于剔除「只有核查标注、没有实质答案」的自我满足式误判）
_CALLOUT_BLOCK = re.compile(
    r"(?m)^[ \t]*>[ \t]*\[!\w+\][^\n]*(?:\n[ \t]*>[^\n]*)*\n?")
_ANY_HEAD = re.compile(r"(?m)^(#{1,6})[ \t]*(.+?)[ \t]*$")
# 「整行只有答案类标题」的形态（用于识别连续包裹标题）
_ANS_TITLE_ONLY = re.compile(
    r"(?m)^#{1,6}[ \t]*(?:参考解答|参考答案与解析|参考答案|答案与解析|答案解析|"
    r"解析要点|详解|解答|答案|解析)" + _ANS_SUFFIX + r"[ \t]*$")
# 🔴 第五种形态（2026-10-07）：答案区里用**一级标题**写小问
#    （`## 参考答案` → `#1-1 (2分)` / `#1-2` / `#(浓度转化过程 2 分)`）。
#    判据：井号后**紧跟数字或中文括号**（不要求空格）⇒ 视为答案小问标题而非区界。
_SUBQ_HEAD = re.compile(r"(?m)^#{1,6}[ \t]*(?=[0-9（(【\[])")


def find_answer_section(body, allow_details=True):
    """定位答案区。返回 (start, end, kind)；找不到返回 None。

    kind ∈ {标准, 异形标题, 加粗标记, details}
    「参考答案/答案与解析/答案解析/参考解答」算标准（与旧口径一致），
    其余（答案/解答/解析要点/详解/解析）算异形标题。

    🔴 2026-10-07 修（真实缺陷，A 层标注时踩到）：
    段边界原先用「下一个**任意**标题」作结束，但答案区里**紧跟子标题**是常态
    （`## 参考答案` → `### (1) …`），于是段长被截成 0 ⇒ `has_entity=False`
    ⇒ 21 张**有答案**的卡被误判为「答案区空」。
    正解：**同级别或更高级**的标题才算区界；`###`/`####` 是答案区的子结构，要**并入**。
    """
    def _end_after(m):
        """找答案区结束位置：下一个 level <= 本级的标题；没有则到文末。

        ⚠️ 必须从 **m.end()** 起扫，不能从 m.start()——否则会匹配到**标题自己**
        并立刻返回自身位置（实测把 `## 参考答案\\n\\n#### 答\\n\\n答案…` 截成空段）。
        ⚠️ 2026-10-07 再修：库里有**连续答案类标题**（`## 答案与解析` 紧跟 `## 参考答案`，
           两者同级且中间无内容）⇒ 按原规则会截成空段，误判「答案区空」。
           正解：**跳过后续连续的答案类标题**，直到遇到「非答案类」标题或正文。
        """
        m0 = re.match(r"(?m)^(#{1,6})[ \t]*", body[m.start():m.end() + 1])
        level = len(m0.group(1)) if m0 else 2
        pos = m.end()
        while True:
            nxt = None
            for h in _ANY_HEAD.finditer(body, pos):
                if len(h.group(1)) <= level:
                    nxt = h
                    break
            if nxt is None:
                return len(body)
            # 该标题若是「答案类」，说明是连续包裹标题 ⇒ 跳过，继续往后找
            if _ANS_TITLE_ONLY.match(nxt.group(0)):
                pos = nxt.end()
                continue
            # 🔴 2026-10-07 第五种形态：答案区里用**一级标题**写小问
            #    （`## 参考答案` → `#1-1 (2分)`、`#1-2`、`#(浓度转化过程 2 分)`）。
            #    这类「`#` ＋ 题号数字/括号」的标题是**答案的子结构**，不是区界。
            #    判据：井号后紧跟数字或中文括号 ⇒ 视为答案小问标题。
            if _SUBQ_HEAD.match(nxt.group(0)):
                pos = nxt.end()
                continue
            return nxt.start()

    std = re.compile(r"(?m)^(#{1,6})[ \t]*(?:参考解答|参考答案与解析|参考答案|答案与解析|答案解析)"
                     + _ANS_SUFFIX + r"[ \t]*(?:[（(][^）)\n]{0,12}[）)])?[ \t]*$")
    # 🔴 第六形态（2026-10-07，final_stats 时发现 47 张卡命中）：
    #    **同页重复的答案标题**——这些卡的正文被整段复制了两遍，
    #    于是 `## 参考答案` 出现 2–6 次；`search` 只取**第一个**，
    #    其后紧跟的同名标题立刻成为区界 ⇒ 截成空段 ⇒ 误判「答案区空」。
    #    正解：取**最后一个「后面确实有内容」的**那个标题。
    allm = list(std.finditer(body))
    if allm:
        if len(allm) > 1:
            for mm in reversed(allm):
                s0, e0 = mm.start(), _end_after(mm)
                seg0 = re.sub(r"(?m)^#{1,6}[ \t]*.*$", "", body[s0:e0])
                if re.sub(r"[\s>*`]", "", seg0):
                    return s0, e0, "标准"
        m = allm[0]
        return m.start(), _end_after(m), "标准"
    m = _ANS_HEAD.search(body)
    if m:
        return m.start(), _end_after(m), "异形标题"
    # ⚠️ details 必须排在加粗标记**之前**：库里多数折叠块里有 `**答案：**`，
    #    先匹配加粗标记会把整块答案截成一行。
    if allow_details:
        m = _DET.search(body)
        if m:
            return m.start(), m.end(), "details"
    m = _ANS_MARK.search(body)
    if m:
        return m.start(), _end_after(m), "加粗标记"
    return None


def classify_answer(body):
    """分类答案形态。返回 dict：
    {found, kind, has_entity, ext_ref, chars}
      · found       —— 能否定位到答案区
      · has_entity  —— 是否有**实体答案**（外链型与空壳都算 False）
      · ext_ref     —— 是否外链型（答案在卷册，卡内有意不复制）
    """
    loc = find_answer_section(body)
    if not loc:
        return {"found": False, "kind": None, "has_entity": False, "ext_ref": False, "chars": 0}
    s, e, kind = loc
    seg = body[s:e]
    txt = _DET.sub(lambda m: m.group(1), seg) if kind == "details" else seg
    # 🔴 第七形态（2026-10-07，final_stats 时发现 207 张受影响）：
    #    答案区**只有 callout 标注块**（`> [!warning] 源确缺答案…` / `> [!warning] 待人工核…`）。
    #    这些标注是**我们自己的核查记录，不是答案**；原判据把它当成实体答案
    #    ⇒ **「自我满足式误判」**：标注让卡片看起来有答案，可用率虚高 207 张。
    #    正解：**先把 callout 整块剥掉**，再判是否还有实质内容。
    txt = _CALLOUT_BLOCK.sub("", txt)
    txt = re.sub(r"(?m)^[ \t]*(?:>[ \t]*)?#{1,6}[ \t]*.*$", "", txt)      # 去标题行
    plain = re.sub(r"[\s>*#`\[\]（）()｜|]", "", txt)
    ext = bool(_EXT_REF.search(txt))
    # 外链型：答案区只是指针。
    # ⚠️ 阈值不能用「字数 >= 12」——「答案是 B」只有 4 字，库内还有「有;无;有」这种
    #    短序列答案（记忆里早已记着「短答案≠无答案」）。判据改为：非空且非外链指引即算实体。
    has_entity = (not ext) and len(plain) >= 1
    return {"found": True, "kind": kind, "has_entity": has_entity,
            "ext_ref": ext, "chars": len(plain)}


def answer_text(body, limit=None, ext_note="（答案见卷册，未复制——源答案存在跨题粘连缺陷，见原文件）"):
    """取答案正文；外链型返回明确标注而非指针原文。"""
    loc = find_answer_section(body)
    if not loc:
        return ""
    s, e, kind = loc
    seg = body[s:e]
    if kind == "details":
        inner = " ".join(_DET.findall(seg))
    else:
        inner = "\n".join(ln for ln in seg.split("\n") if not re.match(r"^\s*-{3,}\s*$", ln))
    inner = re.sub(r"\s+", " ", inner).strip()
    info = classify_answer(body)
    if info["ext_ref"] and not info["has_entity"]:
        return ext_note
    return inner[:limit] if limit else inner
