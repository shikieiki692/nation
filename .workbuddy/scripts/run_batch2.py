# -*- coding: utf-8 -*-
"""补跑 有机化学 / 元素与分析 两卷（结构卷已生成，避免重抽）"""
import importlib.util, collections, sys

spec = importlib.util.spec_from_file_location("tp", r"C:\Obsidion\妙妙屋\.workbuddy\scripts\testpaper_v2.py")
tp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tp)

print("扫描中…", flush=True)
index, records = tp.single_pass()
print("索引:", len(index), "解析:", len(records), flush=True)

for subject in ["有机化学", "元素与分析"]:
    pool = tp.pick_pool(records, subject)
    print(subject, "池:", len(pool), flush=True)
    results, chosen = tp.select(subject, records)
    fn = tp.write_paper(subject, results, chosen)
    nb = tp.backfill(subject, chosen, index)
    dif = collections.Counter(p["difficulty"] for p in chosen)
    print(subject, "->", len(chosen), "题 | d分布", dict(sorted(dif.items())), "| used_in", nb, flush=True)
