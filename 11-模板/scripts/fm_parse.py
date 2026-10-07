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
_ANS_HEAD = re.compile(
    r"(?m)^(#{1,6})[ \t]*(?:参考解答|参考答案与解析|参考答案|答案与解析|答案解析|"
    r"解析要点|详解|解答|答案|解析)[ \t]*$"
)
# 加粗标记型：**答案：** / **参考答案：**
_ANS_MARK = re.compile(r"(?m)^[ \t]*(?:>[ \t]*)?\*\*[ \t]*(?:参考)?答案(?:[ \t]*[:：]|[ \t]*\*\*)")
# 外链型：答案区只写「答案见 [[…]] 的参考答案区」
_EXT_REF = re.compile(r"(?:本题)?答案(?:见|在)[^\n]{0,20}?\[\[")
# 折叠块
_DET = re.compile(r"(?s)<details[^>]*>(.*?)</details>")
_ANY_HEAD = re.compile(r"(?m)^#{1,6}[ \t]*(.+?)[ \t]*$")


def find_answer_section(body, allow_details=True):
    """定位答案区。返回 (start, end, kind)；找不到返回 None。

    kind ∈ {标准, 异形标题, 加粗标记, details}
    「参考答案/答案与解析/答案解析/参考解答」算标准（与旧口径一致），
    其余（答案/解答/解析要点/详解/解析）算异形标题。
    """
    std = re.compile(r"(?m)^#{1,6}[ \t]*(?:参考解答|参考答案与解析|参考答案|答案与解析|答案解析)[ \t]*$")
    m = std.search(body)
    if m:
        nxt = _ANY_HEAD.search(body, m.end())
        return m.start(), (nxt.start() if nxt else len(body)), "标准"
    m = _ANS_HEAD.search(body)
    if m:
        nxt = _ANY_HEAD.search(body, m.end())
        return m.start(), (nxt.start() if nxt else len(body)), "异形标题"
    # ⚠️ details 必须排在加粗标记**之前**：库里多数折叠块里有 `**答案：**`，
    #    先匹配加粗标记会把整块答案截成一行。
    if allow_details:
        m = _DET.search(body)
        if m:
            return m.start(), m.end(), "details"
    m = _ANS_MARK.search(body)
    if m:
        nxt = _ANY_HEAD.search(body, m.end())
        return m.start(), (nxt.start() if nxt else len(body)), "加粗标记"
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
