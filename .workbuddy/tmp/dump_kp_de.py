# -*- coding: utf-8 -*-
"""只读：完整打印 kp_link_patrol 的 D（真孤儿）与 E（悬空链）明细，含全部文件。"""
import os, re, sys, yaml
from collections import Counter

VAULT = r"C:/Obsidion/妙妙屋"
KP_DIR = os.path.join(VAULT, "03-知识点")
QB_DIRS = [os.path.join(VAULT, "04-题库"), os.path.join(VAULT, "05-真题库")]
QB_LINK_FIELDS = ["knowledge_points", "depends_on", "cross_references", "related", "superseded_by"]
DEP_STATUS = ("deprecated", "已废弃", "已合并", "重定向")
LINK_RE = re.compile(r"\[\[([^\]\n]+?)\]\]")


def load_fm(path):
    try:
        t = open(path, encoding="utf-8", newline="").read()
    except Exception:
        return None
    if not t.startswith("---"):
        return {}
    e = t.find("\n---", 3)
    if e == -1:
        return {}
    try:
        d = yaml.safe_load(t[3:e])
    except Exception:
        return {"__parse_error__": True}
    return d if isinstance(d, dict) else {}


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def strip_link(s):
    s = s.strip()
    if s.startswith("[[") and s.endswith("]]"):
        s = s[2:-2]
    return s.split("|")[0].split("#")[0].strip()


basename_map, alias_map = {}, {}
for r, d, fs in os.walk(KP_DIR):
    for fn in fs:
        if not fn.endswith(".md"):
            continue
        fm = load_fm(os.path.join(r, fn))
        if not fm or "__parse_error__" in fm:
            continue
        basename_map.setdefault(fn[:-3].lower(), os.path.join(r, fn))
        if fm.get("title"):
            alias_map.setdefault(str(fm["title"]).lower(), os.path.join(r, fn))
        for a in as_list(fm.get("aliases")):
            if isinstance(a, str):
                alias_map.setdefault(a.lower(), os.path.join(r, fn))


def resolve_kp(lt):
    k = strip_link(lt).lower()
    if k in basename_map:
        return basename_map[k]
    if "/" in k:
        leaf = k.rsplit("/", 1)[1]
        if leaf in basename_map:
            return basename_map[leaf]
        if leaf in alias_map:
            return alias_map[leaf]
    return alias_map.get(k)


vault_bn, vault_alias = set(), set()
for r, d, fs in os.walk(VAULT):
    if "/." in r.replace("\\", "/"):
        d[:] = []
        continue
    for fn in fs:
        if not fn.endswith(".md"):
            continue
        vault_bn.add(fn[:-3].lower())
        fm = load_fm(os.path.join(r, fn))
        if isinstance(fm, dict) and "__parse_error__" not in fm:
            for a in as_list(fm.get("aliases")):
                if isinstance(a, str):
                    vault_alias.add(a.lower())


def resolve_any(lt):
    k = strip_link(lt).lower()
    if k in vault_bn:
        return True
    if "/" in k and k.rsplit("/", 1)[1] in vault_bn:
        return True
    return k in vault_alias


D, E = [], []
for qdir in QB_DIRS:
    for r, d, fs in os.walk(qdir):
        for fn in fs:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(r, fn)
            fm = load_fm(p)
            if not fm or "__parse_error__" in fm:
                continue
            rel = os.path.relpath(p, VAULT).replace("\\", "/")
            for field in QB_LINK_FIELDS:
                if field not in fm:
                    continue
                for item in as_list(fm[field]):
                    s = str(item)
                    if "[[" not in s:
                        continue
                    for m in LINK_RE.findall(s):
                        lt = strip_link(m)
                        if not lt:
                            continue
                        if resolve_kp(lt) or resolve_any(lt):
                            continue
                        if lt.lower().endswith(".md"):
                            continue
                        D.append((rel, field, lt))

for r, d, fs in os.walk(VAULT):
    if "/." in r.replace("\\", "/"):
        d[:] = []
        continue
    for fn in fs:
        if not fn.endswith(".md"):
            continue
        p = os.path.join(r, fn)
        fm = load_fm(p)
        if not isinstance(fm, dict) or "__parse_error__" in fm:
            continue
        for field in ("source_notes", "prerequisite", "prerequisites"):
            if field not in fm:
                continue
            for item in as_list(fm[field]):
                for m in LINK_RE.findall(str(item)):
                    lt = strip_link(m)
                    if lt and not resolve_any(lt) and not resolve_kp(lt):
                        E.append((os.path.relpath(p, VAULT).replace("\\", "/"), field, lt))

print("=== D 真孤儿 %d（去重 %d）===" % (len(D), len(set(x[2] for x in D))))
for rel, field, lt in sorted(D):
    print("  %-90s | %-20s | %s" % (rel, field, lt))
print()
print("=== E 悬空链 %d（去重 %d）===" % (len(E), len(set(x[2] for x in E))))
for rel, field, lt in sorted(E):
    print("  %-90s | %-14s | %s" % (rel, field, lt))
