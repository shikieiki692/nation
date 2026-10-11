# -*- coding: utf-8 -*-
"""回填 vol_meta_<卷>.json（各卷建计划时的池开关）＋登记卷 XVI 的补丁与重建清单。

背景：`build_org.py` 自 2026-10-11 起把「建计划的池开关」固化进 vol_meta_<卷>.json 并硬校验；
      既有各卷（X~XV）的计划是在 --all-years 下建的（见 make_plan_*.py 注释「与标准动作一致」），
      但当时未落盘 ⇒ 本脚本按实回填，避免新校验把正常卷误挡。
"""
import json
import os

HERE = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe"
PLANS = ["X", "XI", "XI.new", "XII", "XIII", "XIp", "XIV", "XV", "XVI"]

for v in PLANS:
    if v.endswith(".new"):          # 冗余计划文件（卷 XI 的旧版）不打 sidecar
        continue
    pp = os.path.join(HERE, "vol_plan_%s.json" % v)
    if not os.path.exists(pp):
        print("[skip] 无计划:", v)
        continue
    plan = json.load(open(pp, encoding="utf-8"))
    n = sum(len(l) for _m, l in plan)
    mp = os.path.join(HERE, "vol_meta_%s.json" % v)
    meta = {}
    if os.path.exists(mp):
        meta = json.load(open(mp, encoding="utf-8"))
    meta.setdefault("flags", ["--all-years"])
    meta.setdefault("vol", v)
    meta["n"] = n
    meta.setdefault("backfilled", "2026-10-11")
    json.dump(meta, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[OK] vol_meta_{v}.json  n={n}  flags={meta['flags']}"
          + ("  post_patches=%d" % len(meta.get("post_patches") or []) if meta.get("post_patches") else ""))

# ── 卷 XVI 专属登记：卷级补丁 + 重建待核清单 ────────────────────────────
mp = os.path.join(HERE, "vol_meta_XVI.json")
meta = json.load(open(mp, encoding="utf-8"))
meta["post_patches"] = [
    {"script": "xvi_tbl_color_fix.py",
     "why": "修「21 列颜色汉字波长表」的 pandoc 网格错误（20 根 gridCol×600tw 溢出版心 9752tw "
            "⇒ LO 压缩致波长 950 折成 95/0）；重建 docx 后**必须**重跑，漏跑所有闸门都不报",
     "added": "2026-10-11"}
]
meta["rebuild_flags"] = [
    {"card": "题-HZ-01-06-CuI由于具有灵活多变的配位",
     "where": "答案区 6-1-2",
     "note": "源答案句在 OCR md 中整句丢失（只剩 $$NaHSO_3$$/$$(CN)_2$$ 两块漂移公式）⇒ "
             "2026-10-11 据残留重建为散文句；已回源目检（汇智《长沙化学刷初赛模拟1》答案册 p7）"
             "逐字核对为「更温和的反应条件和 NaHSO₃ 的添加避免了 (CN)₂ 的释放」",
     "status": "已回源核对"}
]
json.dump(meta, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"[OK] vol_meta_XVI.json 追加 post_patches={len(meta['post_patches'])} "
      f"rebuild_flags={len(meta['rebuild_flags'])}")
