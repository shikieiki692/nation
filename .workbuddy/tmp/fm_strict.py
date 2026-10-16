# -*- coding: utf-8 -*-
"""ruamel 严格 FM 解析（重复键视为 FAIL）。用法：python fm_strict.py <path...>"""
import io
import os
import sys
from ruamel.yaml import YAML


def check(p):
    y = YAML(typ="safe")
    y.allow_duplicate_keys = False
    t = open(p, encoding="utf-8-sig", newline="").read()
    if not t.startswith("---"):
        return "NO_FM"
    e = t.find("\n---", 3)
    if e == -1:
        return "NO_FM_END"
    try:
        d = y.load(t[3:e])
        return "OK" if isinstance(d, dict) else "NOT_DICT"
    except Exception as ex:
        return "FAIL: %s" % str(ex).splitlines()[0]


def main():
    bad = 0
    for p in sys.argv[1:]:
        r = check(p)
        if r != "OK":
            bad += 1
        print("  [%s] %s" % (r, os.path.relpath(p, r"C:/Obsidion/妙妙屋")))
    print("\nFAIL=%d / 受检 %d" % (bad, len(sys.argv) - 1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
