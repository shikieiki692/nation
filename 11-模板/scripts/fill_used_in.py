#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fill_used_in.py — 组卷后 used_in 回填（通用工具）。

用法:
    python fill_used_in.py --exam "04-课件/习题集/某测试卷.md" [--apply]
    python fill_used_in.py --exam 卷.md --exam 卷2.md --apply   # 多卷

行为:
  1) 从卷文件提取题源 token：wikilink 全名 [[题-...]] ＋ 纯文本小问级 token（题-028-1-1-名字）
  2) 定位题库文件：精确 basename → 名字后缀匹配 → 数字链前缀收缩（均须唯一命中）
  3) 按文件聚合 token 后一次写入（防重复扩列表）：
     - 无 used_in          → 新增 used_in: "[[<卷全路径>]]"
     - 已含同值（字面比较）→ 跳过
     - 异值               → 值集合合并去重，1 值写单值式、多值写列表式
  4) 写前快照到 .workbuddy/backups/usedin-fill-<date>/；产出 jsyaml 清单（Windows 原生路径）

铁律: open(newline="") 读写；插入行行尾随原文件 CRLF/LF 风格；FM 边界按首个 --- 对定位。
默认 dry-run，--apply 才写盘。
"""
import argparse, os, re, shutil
from datetime import date
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")

def build_index():
    idx = []
    for sub in ("04-题库",):
        for root, _d, files in os.walk(VAULT / sub):
            for f in files:
                if f.endswith(".md") and f[:-3].startswith("题-"):
                    idx.append((f[:-3], str(Path(root) / f)))
    return idx

def extract_tokens(text):
    toks = set(re.findall(r"\[\[(题-[^\]|#]+)", text))
    toks |= set(m.rstrip("，。；、") for m in re.findall(
        r"题-\d{2,4}(?:-\d)+[^\s|，。；、）)#\]]*", text))
    return toks

def resolve(tok, idx):
    if tok.startswith("题-"):
        exact = [p for b, p in idx if b == tok]
        if len(exact) == 1:
            return exact[0], "exact"
        m = re.match(r"题-(\d+)-", tok)
        num, rest = (m.group(1), tok[m.end():]) if m else (None, tok)
        while num and re.match(r"\d+-", rest):
            rest = rest[rest.index("-") + 1:]
        if num:
            c = [p for b, p in idx if b.startswith(f"题-{num}-") and b.endswith(f"-{rest}") and rest]
            if len(c) == 1:
                return c[0], "name-suffix"
            segs, chain = tok.split("-"), ["题", num]
            for s in segs[2:]:
                if s.isdigit():
                    chain.append(s)
                else:
                    break
            for L in range(len(chain), 2, -1):
                pref = "-".join(chain[:L]) + "-"
                c = [p for b, p in idx if b.startswith(pref)]
                if len(c) == 1:
                    return c[0], f"prefix[{pref}]"
                if len(c) > 1:
                    return None, f"prefix-ambiguous:{pref}"
    return None, "no-hit"

def parse_used_in(line):
    return re.findall(r"\[\[([^\]]+)\]\]", line)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exam", action="append", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run-list", action="store_true", help="输出将改动的文件清单到 stdout")
    args = ap.parse_args()

    idx = build_index()
    print(f"题库索引: {len(idx)} 文件")
    plan, failed = {}, []   # qpath -> [target, [tokens]]
    for exam in args.exam:
        exam_path = VAULT / exam
        raw = open(exam_path, encoding="utf-8", newline="").read()
        target = exam[:-3] if exam.endswith(".md") else exam
        for tok in sorted(extract_tokens(raw)):
            hit, how = resolve(tok, idx)
            if hit:
                plan.setdefault(hit, [target, []])[1].append(tok)
            else:
                failed.append((exam, tok, how))

    changed, skipped, backup_dir = [], [], VAULT / ".workbuddy" / "backups" / f"usedin-fill-{date.today():%Y-%m-%d}"
    for qpath, (target, toks) in sorted(plan.items()):
        qraw = open(qpath, encoding="utf-8", newline="").read()
        lines = qraw.split("\n")
        if lines[0].strip() != "---":
            failed.append(("?", qpath, "NO_FM")); continue
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is None:
            failed.append(("?", qpath, "NO_FM_END")); continue
        old_i = next((i for i in range(1, end) if lines[i].startswith("used_in")), None)
        cr = "\r" if "\r\n" in qraw else ""
        if old_i is None:
            vals = []
            action = "新增"
        else:
            vals = parse_used_in(lines[old_i])
            if target in vals:
                skipped.append(qpath); continue
            action = f"合并({len(vals)}+1)"
        vals = list(dict.fromkeys(vals + [target]))
        newline = (f'used_in: "[[{vals[0]}]]"' + cr) if len(vals) == 1 else (
            "used_in: [" + ", ".join(f'"[[{v}]]"' for v in vals) + "]" + cr)
        if args.apply:
            dst = backup_dir / qpath
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                shutil.copy2(qpath, dst)
            if old_i is None:
                lines.insert(end, newline)
            else:
                lines[old_i] = newline
            open(qpath, "w", encoding="utf-8", newline="").write("\n".join(lines))
        changed.append((qpath, action, len(toks)))

    print(f"{'[APPLY] ' if args.apply else '[DRY-RUN] '}计划改动: {len(changed)} ｜ 同值跳过: {len(skipped)} ｜ 失败: {len(failed)}")
    for p, a, n in changed:
        print(f"  [{a} x{n}token] {p}")
    for e, t, how in failed:
        print(f"  [失败] {e} :: {t} -> {how}")
    if args.apply and changed:
        lst = backup_dir.parent / f"usedin-fill-{date.today():%Y-%m-%d}.txt"
        lst.write_text("\n".join(str(VAULT / p) for p, _a, _n in changed) + "\n", encoding="utf-8")
        print(f"jsyaml 清单: {lst}")

if __name__ == "__main__":
    main()
