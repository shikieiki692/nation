# -*- coding: utf-8 -*-
"""诊断：题-HZ-01-06 为何不在真实池（build_pool）中。"""
import importlib.util
import os
import sys

VAULT = r"C:\Obsidion\妙妙屋"
OPT = os.path.join(VAULT, ".workbuddy", "tmp", "opt_pipe")
sys.path.insert(0, OPT)
os.chdir(VAULT)

spec = importlib.util.spec_from_file_location("BORG", os.path.join(OPT, "build_org.py"))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

TARGET = "题-HZ-01-06-CuI由于具有灵活多变的配位.md"

print("== 闸门命中清单 ==")
for name in ("ECHO_HITS", "OVERFLOW_HITS", "GARB2_HITS", "HANDWRITTEN_HITS"):
    lst = getattr(M, name, None)
    if lst is None:
        print(f"  {name}: <无>")
        continue
    hits = [x for x in lst if TARGET in str(x)]
    print(f"  {name}: 共 {len(lst)} ｜含目标 {len(hits)} → {hits}")

pool = M.build_pool()
paths = set()
for mod, lst in pool.items():
    for c in lst:
        paths.add(c['path'].replace('\\', '/'))
hit = [p for p in paths if TARGET in p]
print("\n== 真实池 ==")
print("  池规模:", {k: len(v) for k, v in pool.items()})
print("  目标在池:", hit)
