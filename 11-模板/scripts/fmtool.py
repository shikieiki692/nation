# -*- coding: utf-8 -*-
"""FM（YAML frontmatter）稳健解析工具 —— 消除 2026-10-02 第三轮体检的三类假阳性。

🔴 背景（血泪）：本库 md **大量是 CRLF**，且列表字段**行内数组与块列表两种写法并存**。
   因此下列写法都会**静默失败**（不报错、只是匹配不到）：
     ✗ re.match(r'^---\\n(.*?)\\n---', t)        # 硬编码 \\n，遇 CRLF 全库 miss
     ✗ re.search(r'^key:\\s*$', fm)              # 块列表才匹配；行内数组漏
     ✗ re.search(r'^key:\\s*(\\S+)', fm)         # \\S+ 把行尾 \\r 吃进断言
   ⇒ 曾据此误报「72 个考纲页全缺 syllabus_code」「41 张真题卡全缺 KP」「专题层全缺 KP」，
     实际库完全合规。**判覆盖前一律用本模块。**

✅ 正确做法：先归一行尾 → 用 `^key:(.*)$` 抓整行 → 用 `([^\\r\\n]+)` 取值。
"""
import os
import re

__all__ = [
    "read_text", "read_fm", "get_raw", "get_list", "has_field", "is_empty_value",
    "audit_dir", "DEPRECATED_KEYS",
]

# 抗 CRLF：行尾归一后再匹配；也吃 \r\n 混排
_FM_BLOCK = re.compile(r'^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)', re.S)

# deprecated 有两式：`status: deprecated` 与老式 `deprecated: true`
DEPRECATED_KEYS = ("status: deprecated", "deprecated: true")


def read_text(path):
    """读文件并**归一行尾为 LF**、去 BOM。"""
    with open(path, "rb") as fh:
        raw = fh.read()
    return raw.decode("utf-8-sig").replace("\r\n", "\n")


def read_fm(path):
    """返回 frontmatter 文本（不含 --- 分隔符）；无 FM 返回 ''。"""
    m = _FM_BLOCK.match(read_text(path))
    return m.group(1) if m else ""


def get_raw(fm, key, default=None):
    """取字段的**原始值文本**（整行等号右侧），不做类型转换。

    兼容三种写法：
        key: ["[[A]]", "[[B]]"]   ← 行内数组
        key:                      ← 块列表（值在后续缩进行）
        key: 决赛01← 标量（**不含**行尾 \\r）
    """
    m = re.search(r'^' + re.escape(key) + r':[ \t]*([^\n]*)', fm, re.M)
    if not m:
        return default
    return m.group(1).strip()


def split_inline_array(inner):
    """切分行内数组，**尊重引号**：元素内可含逗号。

    🔴 2026-10-02 实测踩坑：`["[[1,2-迁移与重排]]", "[[X]]"]`按逗号裸切
       会把元素撕成 `[[1` 与 `2-迁移与重排]]` ⇒ 误报「KP 不存在」。
       故须先按引号成对，再取每对内的内容。
    """
    out, buf, in_q = [], [], False
    for ch in inner:
        if ch == '"':
            in_q = not in_q
            continue
        if ch == "," and not in_q:
            if buf:
                out.append("".join(buf).strip())
            buf = []
            continue
        buf.append(ch)
    if buf:
        out.append("".join(buf).strip())
    return [x for x in out if x]


def get_list(fm, key):
    """取列表字段（同时吃行内数组与块列表），返回 list[str]；无则返回 []。"""
    v = get_raw(fm, key)
    if v is None:
        # 块列表写法：key 后跟缩进块（**可零缩进**，故只要求 `- `）
        m = re.search(r'^' + re.escape(key) + r':[ \t]*\r?\n((?:[ \t]*-[^\n]*\r?\n?)+)',
                      fm, re.M)
        if not m:
            return []
        return [x.strip().lstrip('-').strip() for x in m.group(1).splitlines() if x.strip()]
    if v.startswith('[') and v.endswith(']'):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [x.strip().strip('"\'') for x in split_inline_array(inner) if x.strip()]
    return [v] if v else []


def has_field(fm, key):
    """键是否存在（⛔ **不等于已覆盖**，判覆盖请用 is_empty_value）。"""
    return re.search(r'^' + re.escape(key) + r':', fm, re.M) is not None


def is_empty_value(fm, key):
    """字段**不存在**或**值为空**（[] / 空 / null）皆算 True。

    🔴 判覆盖时**必须**按「值非空」—— 本库导入管线会把 knowledge_points 预置为
       `[]`，若只判「键是否存在」会得「100% 已覆盖」的假阳性。
    """
    v = get_raw(fm, key)
    if v is None or v in ("", "[]", "{}", "null", "~"):
        return True
    return False


def is_deprecated(fm):
    """目标页是否被废止（**两式并查**：status: deprecated 与 deprecated: true）。"""
    return any(k in fm for k in DEPRECATED_KEYS)


def audit_dir(root, key="knowledge_points", skip_names=("README.md",), skip_excalidraw=True):
    """统计某目录下 md 的某字段覆盖率（按「值非空」判定）。

    返回 dict：total / covered / empty / no_fm / no_key / files_empty(前若干)
    """
    root = os.path.abspath(root)
    stat = {"total": 0, "covered": 0, "no_fm": 0, "no_key": 0, "empty": 0,
            "files_empty": [], "files_nofm": []}
    for dp, dn, fn in os.walk(root):
        for f in sorted(fn):
            if not f.endswith(".md") or f in skip_names:
                continue
            # excalidraw 图页是图不是知识页，统计须排除
            if skip_excalidraw and ".excalidraw.md" in f:
                continue
            p = os.path.join(dp, f)
            stat["total"] += 1
            t = read_text(p)
            m = _FM_BLOCK.match(t)
            if not m:
                stat["no_fm"] += 1
                stat["files_nofm"].append(os.path.relpath(p, root))
                continue
            fm = m.group(1)
            if not has_field(fm, key):
                stat["no_key"] += 1
                stat["files_empty"].append(os.path.relpath(p, root))
                continue
            if is_empty_value(fm, key):
                stat["empty"] += 1
                stat["files_empty"].append(os.path.relpath(p, root))
                continue
            stat["covered"] += 1
    return stat


if __name__ == "__main__":
    import sys
    ROOT = r"C:\Obsidion\妙妙屋"

    checks = [
        ("02-考纲条目", "syllabus_code"),
        ("05-真题库", "knowledge_points"),
        ("04-专题与题型\\题型", "knowledge_points"),
        ("04-专题与题型\\专题", "knowledge_points"),
        ("04-题库\\真题", "syllabus_codes"),
    ]
    print(f"{'目录':<22}{'字段':<20}{'总数':>6}{'已覆盖':>8}{'缺键':>7}{'空值':>7}{'无FM':>7}")
    print("-" * 78)
    for rel, key in checks:
        s = audit_dir(os.path.join(ROOT, rel), key)
        print(f"{rel:<22}{key:<20}{s['total']:>6}{s['covered']:>8}"
              f"{s['no_key']:>7}{s['empty']:>7}{s['no_fm']:>7}")
    print()
    print("判读：'已覆盖' 才是真实覆盖；'缺键'与'空值'都算未覆盖。")
    print("⚠️ 本工具抗 CRLF + 抗行内数组，勿再手写 ^key:\\s*$ 或 \\S+ 取值。")
