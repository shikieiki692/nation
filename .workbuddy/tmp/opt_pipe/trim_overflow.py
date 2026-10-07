#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trim_overflow.py —— 越界卡尾部清理（源卡结构修复，owner 2026-10-07 授权）。
判据与组卷器「越界闸」**完全一致**（BO.overflow_reason），仅对闸门命中的卡动手。
在答案区/题面区定位**首个**越界处（`第M题` 或 行首 `M-K`，M>本卡题号），自成行起整段截除并加校勘注。
用法：python trim_overflow.py [--apply] [--limit N]
"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
_ARGS = sys.argv[1:]
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
sys.argv = ["x", "--vol", "TRIM"]
import build_org as BO

BASE = os.path.join(R, "04-题库/2026机构初赛模拟题")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/overflow_backup")


def find_cut(seg, own):
    """返回 (字符位置, 原因) 或 (None, None)；位置对齐到行首。"""
    pos, why = None, None
    for mm in BO.QW_RE.finditer(seg):
        n = BO._cn2int(mm.group(1))
        if n and n > own:
            pos, why = mm.start(), "「第%s题」" % mm.group(1); break
    for mm in BO.SUBQ_HEAD_RE.finditer(seg):
        if int(mm.group(1)) > own:
            if pos is None or mm.start() < pos:
                pos, why = mm.start(), "行首小问组「%s-…」" % mm.group(1)
            break
    if pos is None:
        return None, None
    ls = seg.rfind("\n", 0, pos) + 1
    return ls, why


def main():
    apply = "--apply" in _ARGS
    lim = 0
    csv_only = "--csv" in _ARGS
    for i, a in enumerate(_ARGS):
        if a == "--limit" and i + 1 < len(_ARGS):
            lim = int(_ARGS[i + 1])
    allow = None
    if csv_only:                      # 只用闸门已验证命中清单
        import csv as _csv
        allow = {r["path"].replace("/", os.sep) for r in
                 _csv.DictReader(open(os.path.join(R, ".workbuddy/tmp/opt_pipe/overflow_hits.csv"),
                                      encoding="utf-8-sig"))}
        print("闸门清单 %d 条" % len(allow))
    os.makedirs(BK, exist_ok=True)
    hits = []
    for p in sorted(glob.glob(os.path.join(BASE, "**", "题-*.md"), recursive=True)):
        if p.split(os.sep)[-2] == "质心GChO":
            continue
        rel = os.path.relpath(p, R)
        if allow is not None and rel not in allow and rel.replace(os.sep, "/") not in allow:
            continue
        t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
        own = BO.own_qno(t, p)
        if not own:
            continue
        i0 = t.find("## 题目"); j0 = t.find("## 参考答案"); k0 = t.find("## 知识点映射")
        if i0 < 0 or j0 < 0:
            continue
        if k0 < 0:
            k0 = len(t)
        q, a = t[i0:j0], t[j0:k0]
        reason = BO.overflow_reason(q, a, own)
        if not reason:
            continue
        # 用「清洗后」的文本判门槛（与闸门一致），但截除在原文上做
        tag = "题面" if "题面区" in reason else "答案"
        s, e = (i0, j0) if tag == "题面" else (j0, k0)
        cut, why = find_cut(t[s:e], own)
        if cut is None:
            continue
        hits.append((p, tag, own, why, cut, s, e, t))
    print("命中 %d 卡（与闸门一致）" % len(hits))
    n = 0
    for p, tag, own, why, cut, s, e, t in hits:
        if lim and n >= lim:
            break
        seg = t[s:e]
        print("  %-44s %s区 第%d行起（%s）" % (os.path.basename(p)[:44], tag,
                                              seg[:cut].count("\n") + 1, why))
        if apply:
            bkf = os.path.join(BK, os.path.basename(p) + ".orig")
            if not os.path.exists(bkf):
                open(bkf, "w", encoding="utf-8", newline="\n").write(t)
            note = ("> ⛔ 校勘（组卷核验 2026-10-07）：源答案卷错排，%s区尾部混入越界内容"
                    "（%s > 本卡第%d题），已整段截除。" % (tag, why, own))
            newseg = seg[:cut].rstrip() + "\n\n" + note + "\n\n"
            open(p, "w", encoding="utf-8", newline="\n").write(t[:s] + newseg + t[e:])
            n += 1
    print("%s %d 卡" % ("已清理" if apply else "（dry-run）", n))


if __name__ == "__main__":
    main()
