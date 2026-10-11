# -*- coding: utf-8 -*-
"""qa_fm_gate_files.py —— 通用版 FM 严格解析闸门（js-yaml4 等价语义），路径由 argv 给。

用法：python qa_fm_gate_files.py <md 路径…>
判据：① ruamel safe 严格解析（重复键/非法转义 ⇒ 抛错）；② 块列表项必须 '- '；
      ③ 值含裸 ': ' 或以 * [ { 开头须加引号；④ CRLF/行内数组兼容。
"""
import io
import os
import re
import sys

from ruamel.yaml import YAML

yaml = YAML(typ="safe")
yaml.allow_duplicate_keys = False


def front_of(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return None


def check(p):
    raw = io.open(p, encoding="utf-8-sig", newline="").read()
    fm = front_of(raw)
    notes = []
    if fm is None:
        notes.append("无 FM 块")
    else:
        try:
            doc = yaml.load(fm)
            if not isinstance(doc, dict):
                notes.append("FM 非映射")
        except Exception as e:
            notes.append("PARSE=%s: %s" % (type(e).__name__, e))
        for m in re.finditer(r"^([A-Za-z_]+):\s*$", fm, re.M):
            after = fm[m.end():].lstrip("\n")
            if after.startswith("[[") or after.startswith("{"):
                notes.append("块列表 %s 值裸 [[/{" % m.group(1))
        for line in fm.split("\n"):
            mm = re.match(r"^([A-Za-z_]+):\s+(.*)$", line)
            if not mm:
                continue
            k, v = mm.group(1), mm.group(2).strip()
            if not v or v[0] in "\"'|>[&!":
                continue
            if ": " in v:
                notes.append("值含裸 ': ' ← %s" % k)
            if v[0] in "*[{" and not v.startswith("[["):
                notes.append("值以 %s 开头未加引号 ← %s" % (v[0], k))
    return notes


def main():
    paths = sys.argv[1:]
    bad = 0
    for p in paths:
        if not os.path.exists(p):
            print("[MISS] %s" % p)
            bad += 1
            continue
        notes = check(p)
        if notes:
            bad += 1
        print("[%s] %-46s %s" % ("FAIL" if notes else "OK  ", os.path.basename(p)[:46], "; ".join(notes)))
    print("\n受检 %d ｜ 异常 %d" % (len(paths), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
