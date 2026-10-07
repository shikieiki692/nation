#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gcho_preflight.py —— 对全部「手写届」做裁图预检：题标记数 vs 卡数、未匹配卡清单。"""
import glob, importlib, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
GC = importlib.import_module("gcho_crop")

ANS = os.path.join(R, "06-外部资料导入/OCR/01-题目/质心合集新/GChO模拟试题合集答案")
manu = sorted(int(re.search(r"GChO(\d+)解析手稿", os.path.basename(f)).group(1))
              for f in glob.glob(os.path.join(ANS, "ZCHEM-GChO*解析手稿.pdf")))
print("手写届 %d 个：%s\n" % (len(manu), manu))
tot_cards = tot_ok = tot_bad = 0
bad_rounds = []
for rnd in manu:
    cards = GC.cards_of(rnd)
    cache = os.path.join(GC.LOC, "GChO%d.json" % rnd)
    if not os.path.exists(cache):
        print("届%-3d ⏳无 OCR 缓存" % rnd); continue
    idx = GC.load_index(rnd, None)
    mks = GC.markers(idx, 150)
    by_q = {q: 1 for q, p, y in mks}
    ok = [c for c in cards if GC.card_qno(c) in by_q]
    bad = [c for c in cards if GC.card_qno(c) not in by_q]
    tot_cards += len(cards); tot_ok += len(ok); tot_bad += len(bad)
    flag = "" if not bad else "  ⚠未匹配 %d" % len(bad)
    print("届%-3d 标记%-3d 卡%-3d → 命中%-3d%s  %s" % (rnd, len(mks), len(cards), len(ok), flag,
                                                     ",".join(str(q) for q, _, _ in mks)))
    if bad:
        bad_rounds.append((rnd, [os.path.basename(c)[:26] for c in bad]))
        for b in bad:
            print("       ✗ %s (题号 %s)" % (os.path.basename(b)[:40], GC.card_qno(b)))
print("\n合计：卡 %d，命中 %d，未匹配 %d" % (tot_cards, tot_ok, tot_bad))
