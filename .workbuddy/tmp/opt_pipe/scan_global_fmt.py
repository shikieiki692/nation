# -*- coding: utf-8 -*-
"""全局源卡 fmt 预演：扫描 `04-题库/2026机构初赛模拟题/**/题-*.md`，
用 volpost.fmt_text 逐卡试算，汇总「哪些规则会触发 / 命中多少」——只读，不写盘。"""
import os, sys, glob, collections

HERE = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe"
sys.path.insert(0, HERE)
import volpost  # noqa

R = r"C:\Obsidion\妙妙屋"
Q = os.path.join(R, "04-题库/2026机构初赛模拟题")

rules = collections.Counter()
files_changed = 0
per_file = []
eol_files = 0

for fp in sorted(glob.glob(os.path.join(Q, "**", "题-*.md"), recursive=True)):
    raw = open(fp, encoding="utf-8-sig").read()
    if "\r\n" in raw:
        eol_files += 1
        raw = raw.replace("\r\n", "\n")
    new, n, chg = volpost.fmt_text(raw)
    if new == raw:
        continue
    files_changed += 1
    cnt = collections.Counter(c[0] for c in chg)
    for k, v in cnt.items():
        rules[k] += v
    per_file.append((os.path.relpath(fp, R).replace("\\", "/"), n, dict(cnt)))

print("受影响卡：%d 张（另 CRLF 文件 %d 个）" % (files_changed, eol_files))
print("\n=== 规则命中汇总 ===")
for k, v in rules.most_common():
    print("   %-16s %d" % (k, v))
print("\n=== 前 25 张卡 ===")
for rel, n, cnt in per_file[:25]:
    print("   %-46s %3d %s" % (os.path.basename(rel)[:44], n, cnt))
