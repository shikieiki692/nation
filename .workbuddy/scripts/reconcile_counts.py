# -*- coding: utf-8 -*-
"""三模块实时对账：题目总数 + teaching_level 分布（并行导入期间的移动靶账本）。"""
import os, re, collections

cnt = collections.Counter()
tot = 0
for root in ("04-题库", "05-真题库"):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            t = open(p, encoding="utf-8", newline="").read(3000)
            if not t.startswith("---"):
                continue
            m = re.search(r"^type:\s*(.+?)\s*$", t, re.M)
            ty = m.group(1).strip('"') if m else ""
            if ty not in ("题目", "真题"):
                continue
            tot += 1
            m2 = re.search(r"^teaching_level:\s*(.+?)\s*$", t, re.M)
            lv = m2.group(1).strip('"') if m2 else "(空)"
            cnt[lv] += 1

print("题目总数:", tot, "（昨日基线 4,182）")
for lv, n in cnt.most_common():
    print(f"  {lv}: {n}")
print("三模块: 习题集(基础+巩固)=", cnt["基础"] + cnt["巩固"],
      "｜ 习题书(拓展)=", cnt["拓展"],
      "｜ 测试题(竞赛)=", cnt["竞赛"])
