# -*- coding: utf-8 -*-
"""只读｜扫「00-首页/活跃任务/」正文 wikilink 断链（沿用 10-15 判据）。
判据：① 先剥 ```…```／~~~…~~~／`…`（J1）；② 路径型 token 做末段 basename 兜底；
      ③ 目标可为 md 笔记 或 任何实际存在的文件（目录/脚本/图片/课件）。
"""
import os
import re
import sys

VAULT = r"C:/Obsidion/妙妙屋"
TARGETS = [os.path.join(VAULT, "00-首页", "活跃任务")]
LINK_RE = re.compile(r"\[\[([^\]\n]+?)\]\]")
FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
INLINE_RE = re.compile(r"`[^`\n]*`")


def strip_code(t):
    t = FENCE_RE.sub("", t)
    t = INLINE_RE.sub("", t)
    return t


def strip_link(s):
    s = s.strip()
    if s.startswith("[[") and s.endswith("]]"):
        s = s[2:-2]
    return s.split("|")[0].split("#")[0].strip()


# 全库：文件名（不含扩展名）+ 全路径存在性
stem = {}
allrel = set()
for r, d, fs in os.walk(VAULT):
    if "/." in r.replace("\\", "/"):
        d[:] = []
        continue
    for fn in fs:
        rel = os.path.relpath(os.path.join(r, fn), VAULT).replace("\\", "/")
        allrel.add(rel.lower())
        allrel.add(rel.rsplit("/", 1)[-1].lower())
        if fn.endswith(".md"):
            stem.setdefault(fn[:-3].lower(), rel)


def resolves(lt):
    k = strip_link(lt).lower()
    if k in stem:
        return True
    if k in allrel:
        return True
    if "/" in k:
        leaf = k.rsplit("/", 1)[1]
        if leaf in stem or leaf in allrel:
            return True
    return False


hits = []
for base in TARGETS:
    for r, d, fs in os.walk(base):
        for fn in fs:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(r, fn)
            t = strip_code(open(p, encoding="utf-8-sig", newline="").read())
            for m in LINK_RE.findall(t):
                lt = strip_link(m)
                if not lt:
                    continue
                if not resolves(lt):
                    hits.append((os.path.relpath(p, VAULT).replace("\\", "/"), lt))

print("=== 00-首页/活跃任务/ 正文断链：%d 处 / 去重 %d ===" % (len(hits), len(set(x[1] for x in hits))))
for rel, lt in sorted(hits):
    print("  %-70s | %s" % (rel, lt))
