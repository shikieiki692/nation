# -*- coding: utf-8 -*-
"""阶段5 批次12：把 8 张新图按内容 sha256 入 媒体仓库，输出映射表。"""
import os, io, json, hashlib, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, ".workbuddy", "tmp", "stage5_img")
MEDIA = os.path.join(ROOT, "媒体仓库")

MAP = [
    ("R1_cyclohexane_skeletal.png", "有机化学/有机化学基础",
     "环己烷键线式（正六边形骨架，6 个顶点=6 个 CH₂）", "01"),
    ("R2_cyclohexene_nbs_allylic.png", "有机化学/自由基反应",
     "环己烯经 NBS/AIBN/CCl₄ 烯丙位溴代生成 3-溴环己烯（双键保留）", "01"),
    ("R4_Ru2+_d6_t2g6_eg0.png", "结构化学/配合物电子构型",
     "八面体场低自旋 d⁶ 排布：t₂g⁶ eg⁰（Ru²⁺，EDTA 体系）", "02"),
    ("R5_Ru3+_d5_t2g5_eg0.png", "结构化学/配合物电子构型",
     "八面体场低自旋 d⁵ 排布：t₂g⁵ eg⁰（Ru³⁺，EDTA 体系）", "02"),
    ("R6_R_to_S_walden_inversion.png", "有机化学/亲核取代与消除反应",
     "(R)-2-溴丁烷经 OH⁻ 背面进攻生成 (S)-2-丁醇（Walden 构型翻转）", "01"),
    ("R7_pinacol_asym_substrate.png", "有机化学/分子重排/频哪醇重排",
     "不对称 Pinacol 重排底物 2-苯基-3-甲基-2,3-丁二醇结构式", "01"),
    ("R8_two_step_potential_profile.png", "有机化学/活性中间体与反应机理",
     "两步反应势能剖面：反应物→‡₁→中间体（能量极小值）→‡₂→产物", "01"),
    ("R9_neopentyl_12_Me_shift.png", "有机化学/分子重排/1,2-迁移",
     "新戊基正离子 1,2-甲基迁移生成叔戊基正离子（含弯箭头机理）", "01"),
]

rows = []
for fn, cat, desc, idx in MAP:
    p = os.path.join(SRC, fn)
    assert os.path.exists(p), p
    b = io.open(p, "rb").read()
    h = hashlib.sha256(b).hexdigest()
    dst_name = h + ".png"
    dst = os.path.join(MEDIA, dst_name)
    if not os.path.exists(dst):
        io.open(dst, "wb").write(b)
        state = "新增"
    else:
        state = "已存在(跳过)"
    rows.append(dict(src=fn, hash=h, media=dst_name, cat=cat,
                     desc=desc, idx=idx, state=state, size=len(b)))
    print("%-38s -> %s.png  %6d B  %s" % (fn, h[:16] + "...", len(b), state))

io.open(os.path.join(ROOT, ".workbuddy", "tmp", "stage5_media_map.json"),
        "w", encoding="utf-8").write(json.dumps(rows, ensure_ascii=False, indent=2))
print("\n映射写入 .workbuddy/tmp/stage5_media_map.json")
