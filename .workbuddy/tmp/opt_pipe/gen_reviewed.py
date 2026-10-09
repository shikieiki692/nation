# -*- coding: utf-8 -*-
"""生成 noise_reviewed.json：**已逐张目检确认为装饰性/无效**、允许被剔除的图。

与 `noise_keep.json`（强制保留）互为对偶：
  · keep    = 判噪假阳性（真内容被剔）⇒ 必须保留
  · reviewed= 人工复核后确认「本就是水印/涂鸦/坏裁图」⇒ 允许剔除（qa_vol_deliver 不再报）
"""
import json, os
R = r"C:\Obsidion\妙妙屋"
P = os.path.join(R, ".workbuddy", "tmp", "opt_pipe", "noise_reviewed.json")
ITEMS = {
    "3dd7a6fc14155c538659c1bcebaf22edd74f63a85374f940d08f762ece7f2cab": "CHEM 哥特体文字 logo",
    "15f705caa38b1d00a77e1d29305157ca4f7a9ef2b913f384433dc55bb328891a": "「育」单字水印",
    "6420235fcfdd95fc39d47aa88ec5ab56255ed31dd51eac607a15f0c4cefdfd58": "「育」单字水印",
    "1a271a40156d678202a34c22b1872e7161a20a59fa88944134606dc27b89e80e": "音符涂鸦",
    "53188f49d9ee93ba5433d0a3ab129614308a6ea746c573429698fc203d3fdbe4": "火柴人涂鸦",
    "de97ea9b9a2eaf8d753736d25e75f3a6ccebfa68e4b532f27a519d9a2b92335b": "火柴人涂鸦（CH₃）",
    "ef8b376c52efb9c442a3fdeae6e4b7dc411e5f139a7139fd0e4c447a687c6b4c": "音符涂鸦",
    "d3518e56383bdc3af12e54888ba4980b042360f0441516ea2f7acfaaf3788773": "火柴人涂鸦",
    "ec25ca675cadba613f3e9bb7323033f6b1d2a1ed584608aadd04f7ba24cf4dff": "坏裁图（仅 图例碎片）",
    "e67ecd53a4b9a42648382a057e18c92a9ad3f8383b388bde32fff881b14c1b65": "火柴人涂鸦",
}
json.dump(ITEMS, open(P, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("noise_reviewed.json：%d 条" % len(ITEMS))
