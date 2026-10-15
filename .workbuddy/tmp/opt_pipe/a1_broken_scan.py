# -*- coding: utf-8 -*-
"""A1：扫 00-首页/活跃任务/ 的 wiki 断链（先剥代码块与行内代码）。

判据（J1）：不剥离代码块 ⇒ 「规范说明文档」的示例文本贡献大量假阳性（174→掉 93）。
只读，不落盘改动。
"""
import os, re, io

VAULT = r"C:\Obsidion\妙妙屋"
TARGET = os.path.join(VAULT, "00-首页", "活跃任务")
LINK_RE = re.compile(r"\[\[([^\]\n]+?)\]\]")

# 全库 md 文件名（去后缀）用于解析判定
names = set()
for r, d, fs in os.walk(VAULT):
    d[:] = [x for x in d if not x.startswith(".") and x != "node_modules"]
    for fn in fs:
        if fn.endswith(".md"):
            names.add(fn[:-3])
            names.add(os.path.splitext(fn)[0])
# 全库相对路径（去后缀）也允许命中
rel_names = set()
for r, d, fs in os.walk(VAULT):
    d[:] = [x for x in d if not x.startswith(".") and x != "node_modules"]
    for fn in fs:
        if fn.endswith(".md"):
            rel_names.add(os.path.relpath(os.path.join(r, fn), VAULT)[:-3].replace("\\", "/"))


def strip_code(text):
    # 1) 围栏代码块
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    text = re.sub(r"~~~.*?~~~", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    # 2) 行内代码
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def strip_link(s):
    s = s.strip()
    if s.startswith("[[") and s.endswith("]]"):
        s = s[2:-2]
    s = s.split("|")[0].split("#")[0].strip()
    return s


rows = []
for r, d, fs in os.walk(TARGET):
    d[:] = [x for x in d if not x.startswith(".")]
    for fn in sorted(fs):
        if not fn.endswith(".md"):
            continue
        p = os.path.join(r, fn)
        raw = open(p, encoding="utf-8-sig", newline="").read()
        txt = strip_code(raw.replace("\r\n", "\n"))
        rel = os.path.relpath(p, VAULT).replace("\\", "/")
        for i, line in enumerate(txt.split("\n"), 1):
            for m in LINK_RE.findall(line):
                t = strip_link(m)
                if not t:
                    continue
                base = t[:-3] if t.endswith(".md") else t
                base = base.replace("\\", "/")
                # ① 全相对路径命中 ② 路径末段（basename）命中——文件迁移子目录后仍应算命中
                tail = base.rsplit("/", 1)[-1]
                if base in rel_names or tail in names:
                    continue
                rows.append((rel, i, t, line.strip()[:110]))

print("断链总条数 =", len(rows))
uniq = {}
for rel, i, t, line in rows:
    uniq.setdefault(t, []).append((rel, i, line))
print("去重目标 =", len(uniq))
print()
for t, occ in sorted(uniq.items(), key=lambda kv: -len(kv[1])):
    print("### %s  （%d 处）" % (t, len(occ)))
    for rel, i, line in occ:
        print("    %s:%d" % (rel, i))
        print("        | %s" % line)
    print()
