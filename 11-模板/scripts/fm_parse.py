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
    """取数组/块列表字段的值（list[str]）。

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


