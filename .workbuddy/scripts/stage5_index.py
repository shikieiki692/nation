# -*- coding: utf-8 -*-
"""批次12：把 8 张新重画图登记到 10-索引与统计 的三个索引（追加行，不动导航与计数）。"""
import os, io

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IDX = os.path.join(ROOT, "10-索引与统计")

H = {
    "cyc": "54a58a59cbde9af9f01928c0134de1268dfa39b2b7363f4e4520e91cf2f5650d",
    "nbs": "76649ba4f852d34eb875af7d1d0cf7d73fea9102f88599f7516dcf1d73d6eafd",
    "d6":  "7e6642f0118c9e10be90ae3e451f5fa94987e8f95dfc70afa90103026707f461",
    "d5":  "462bb0d51f4637d925499fad2c2e01f24b48b239d705bc64144785b551d67ed4",
    "rs":  "a2d6bdc07e33b4da24573b7e934189b92ac4cc162469bf460d189ca4a54fc323",
    "pin": "be2115bb0b3b1b81cc04061d3f68a981b317b442271b193de9a354cbd882f304",
    "pe":  "1ebeef39f78c99406c4792989e0a6b0f3b764c00c32fa0da020d624c8818f554",
    "sh":  "ae508fe64a1548d947765b5955839b39182b089ea6e015a84f090c250f58a795",
}
SRC = "讲义用图补录（本库重画·批次12）"
TAG = "【视觉核验·本库重画批次12】"

ROWS_01 = [
    ("cyc", "cyclohexane_skeletal_hexagon.png",
     "%s环己烷键线式：正六边形骨架，6 个顶点 = 6 个 CH₂" % TAG, "有机化学/结构表示/键线式"),
    ("nbs", "cyclohexene_nbs_allylic_bromination.png",
     "%s环己烯经 NBS/AIBN/CCl₄ 加热光照烯丙位溴代生成 3-溴环己烯（双键保留）" % TAG,
     "有机化学/自由基取代/烯丙位溴代"),
    ("rs", "sn2_walden_inversion_r_bromobutane_to_s_butanol.png",
     "%s(R)-2-溴丁烷经 OH⁻ 背面进攻生成 (S)-2-丁醇，Walden 构型翻转" % TAG,
     "有机化学/亲核取代/立体化学"),
    ("pin", "pinacol_asymmetric_substrate_2phenyl3methylbutane_diol.png",
     "%s不对称 Pinacol 重排底物 2-苯基-3-甲基-2,3-丁二醇结构式" % TAG,
     "有机化学/分子重排/频哪醇重排"),
    ("pe", "two_step_reaction_potential_energy_profile.png",
     "%s两步反应势能剖面：反应物→‡₁→中间体（能量极小值）→‡₂→产物" % TAG,
     "有机化学/物理有机/势能面"),
    ("sh", "neopentyl_cation_12_methyl_shift_curved_arrow.png",
     "%s新戊基正离子 1,2-甲基迁移生成叔戊基正离子（含弯箭头机理）" % TAG,
     "有机化学/分子重排/1,2-迁移"),
]
ROWS_02 = [
    ("d6", "octahedral_low_spin_d6_t2g6_eg0.png",
     "%s八面体场低自旋 d⁶ 排布：t₂g⁶ eg⁰（Ru²⁺，EDTA 体系）" % TAG,
     "配位化学/晶体场/d 电子构型"),
    ("d5", "octahedral_low_spin_d5_t2g5_eg0.png",
     "%s八面体场低自旋 d⁵ 排布：t₂g⁵ eg⁰（Ru³⁺，EDTA 体系）" % TAG,
     "配位化学/晶体场/d 电子构型"),
]
KP = {"d6": "结构化学", "d5": "结构化学"}


def append(fname, rows, style):
    p = os.path.join(IDX, fname)
    raw = io.open(p, encoding="utf-8", newline="").read()
    EOL = "\r" if raw.split("\n")[0].endswith("\r") else ""
    if not raw.endswith("\n"):
        raw += EOL
    out = []
    for key, slug, desc, cat in rows:
        h = H[key] + ".png"
        if style == "subject":
            out.append("| %s | %s | %s | %s | %s | 🟢已视觉核验 |"
                       % (h, slug, desc, cat, SRC))
        else:
            kp = cat.split("/")[0]
            out.append("| %s | %s | %s | %s | 媒体仓库/ | ✅在媒体仓库 |"
                       % (h, slug, desc, kp))
    raw = raw + EOL.join(out) + EOL
    io.open(p, "w", encoding="utf-8", newline="").write(raw)
    print("  %s  +%d 行 (EOL=%s)" % (fname, len(rows), "CRLF" if EOL else "LF"))


print("登记索引：")
append("01-有机化学图谱总索引.md", ROWS_01, "subject")
append("02-结构与无机化学图谱总索引.md", ROWS_02, "subject")
append("全库核心图谱总索引.md", ROWS_01 + ROWS_02, "core")
