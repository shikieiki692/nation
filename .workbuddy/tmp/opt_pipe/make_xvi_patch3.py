# -*- coding: utf-8 -*-
"""卷 XVI · patch3：YJ-05-04 答案区小问标签 `**4-1-1共5分**` → `**4-1-1**（5 分）`。

原因：`renumber2` 的裸号匹配带 `(?![\w\d.])`，而「共」在 Python3 属 `\w`
⇒ `4-1-1共5分` 不被重编号 ⇒ 卷 md 里题面已变为 13-1-1、答案区仍为 4-1-1（不一致）。
改成「**（N 分）**」形态后加粗模式 `**4-1-1**` 可被命中 ⇒ 答案区随题面一起重编号。
"""
import io, json, os

CARD = r"04-题库/2026机构初赛模拟题/壹尖培优/题-YJ-05-04-在整个冷战期间苏联705型核.md"

PAIRS = [
    ("**4-1-1共5分**", "**4-1-1**（5 分）"),
    ("**4-1-2共3分**", "**4-1-2**（3 分）"),
    ("**4-2-1共2分**", "**4-2-1**（2 分）"),
    ("**4-2-2共9分**", "**4-2-2**（9 分）"),
    ("**4-2-3共3分**", "**4-2-3**（3 分）"),
    ("**4-3共8分**", "**4-3**（8 分）"),
]

txt = io.open(CARD, encoding="utf-8-sig").read()
cfg = {}
for a, b in PAIRS:
    assert txt.count(a) == 1, (a, txt.count(a))
    cfg.setdefault(CARD, []).append([a, b])

json.dump(cfg, io.open(r".workbuddy/tmp/opt_pipe/xvi_patch3.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("patch3 生成：%d 处" % sum(len(v) for v in cfg.values()))

# 题名修复配置
titles = {"11": ["**5-1** 在气相的硫单质中", "硫单质的结构、基序与液态硫聚合平衡"]}
json.dump(titles, io.open(r".workbuddy/tmp/opt_pipe/xvi_titles.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("titles 生成：%d 处" % len(titles))
