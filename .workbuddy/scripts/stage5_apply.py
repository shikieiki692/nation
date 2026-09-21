# -*- coding: utf-8 -*-
"""阶段5 批次12：把 8 张新图写回源 md，并执行 2 处去重、1 处拆块(+存疑)、1 处删 callout。

铁律：
  * 读写均 open(..., newline="")
  * 新行行尾跟随该文件自身（CRLF/LF），不改动其它行
  * 逐块先断言"围栏位置 + 块内原文"，全部通过才落盘
  * 断言围栏计数 c1 == c0 + want_delta
用法： python stage5_apply.py [--apply]
"""
import os, io, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "04-课件", "学生讲义")
MAP = {r["src"]: r for r in json.load(
    io.open(os.path.join(ROOT, ".workbuddy", "tmp", "stage5_media_map.json"),
            encoding="utf-8"))}
H = {k: v["hash"] for k, v in MAP.items()}

APPLY = "--apply" in sys.argv

# 每个 op: f 文件 / kind / s,e(1-based 闭区间) / sig 块内必须出现的字符串 / af 必须为裸围栏的行号
OPS = [
    # ---- 有机化学基础.md (LF) ----
    dict(f="有机化学/有机化学基础.md", kind="replace", s=167, e=173, af=[167, 173],
         sig=["     /\\"], img="R1_cyclohexane_skeletal.png", tag="R1 环己烷键线式"),
    dict(f="有机化学/有机化学基础.md", kind="textify", s=159, e=165, af=[160, 165],
         tag="D1 删重复块并保留键线式要点",
         sig=["**1-丙醇四种表示方式对照**（键线式是竞赛书写答案的标准形式）："],
         lines=["**键线式是竞赛书写答案的标准形式**。"]),
    # ---- 自由基反应.md (CRLF) ----
    dict(f="有机化学/自由基反应.md", kind="replace", s=531, e=537, af=[531, 537],
         sig=["    ╕          ╕"], img="R2_cyclohexene_nbs_allylic.png",
         tag="R2 环己烯→3-溴环己烯"),
    dict(f="有机化学/自由基反应.md", kind="textify", s=352, e=364, af=[352, 364],
         tag="R3 链增长拆块+存疑",
         sig=["Br· +   环己烯    → HBr + 烯丙基自由基（共振稳定，3 个等价共振式）"],
         lines=[
             "Br· + 环己烯 → HBr + 烯丙基自由基（共振稳定，3 个等价共振式）",
             "",
             "烯丙基自由基 + NBS → 3-溴环己烯 + 琥珀酰亚胺自由基",
             "",
             "（琥珀酰亚胺自由基与 HBr 反应再生 Br₂，循环）",
             "",
             "> [!warning] 存疑待核",
             "> 上文“3 个等价共振式”“单电子分布在 C1/C3/C5”与本文件 §5.5「烯丙基 2 个等价极限式」口径矛盾：",
             "> 环己烯只有一个双键，烯丙基自由基应只有 2 个共振式（单电子在 C1、C3），C5 并非烯丙位。",
             "> 原文表述暂保留待定夺，作答勿沿用该处“3 个共振式”。",
         ]),
    # ---- 结构化学专题课-学生用合集（完整版）.md (CRLF) ----
    dict(f="结构化学/结构化学专题课-学生用合集（完整版）.md", kind="replace",
         s=2238, e=2246, af=[2238, 2246], sig=["↑↓ || ↑  |"],
         img="R5_Ru3+_d5_t2g5_eg0.png", tag="R5 d⁵ 排布"),
    dict(f="结构化学/结构化学专题课-学生用合集（完整版）.md", kind="replace",
         s=2222, e=2230, af=[2222, 2230], sig=["↑↓ || ↑↓ |"],
         img="R4_Ru2+_d6_t2g6_eg0.png", tag="R4 d⁶ 排布"),
    # ---- 亲核取代与消除反应.md (CRLF) ----
    dict(f="有机化学/亲核取代与消除反应.md", kind="replace", s=547, e=554, af=[547, 554],
         sig=["  CH₃          CH₃          CH₃"], img="R6_R_to_S_walden_inversion.png",
         tag="R6 R→S 构型翻转"),
    # ---- 重排反应.md (LF) ----
    dict(f="有机化学/重排反应.md", kind="replace", s=814, e=818, af=[814, 818],
         sig=["   Ph—C(OH)—C(OH)(CH₃)₂"], img="R7_pinacol_asym_substrate.png",
         tag="R7 Pinacol 底物"),
    # ---- 活性中间体与反应机理基础.md (CRLF) ----
    dict(f="有机化学/活性中间体与反应机理基础.md", kind="delete", s=193, e=194, af=[],
         sig=["🖼️ **待补图**：1,2-H/烷基迁移正式机理箭头图"], tag="删 L193 待补图 callout"),
    dict(f="有机化学/活性中间体与反应机理基础.md", kind="replace", s=182, e=191,
         af=[182, 191], sig=["[1,2]-甲基迁移（新戊基 1° → 叔戊基 3°）："],
         img="R9_neopentyl_12_Me_shift.png", tag="R9 1,2-甲基迁移机理"),
    dict(f="有机化学/活性中间体与反应机理基础.md", kind="replace", s=382, e=390,
         af=[382, 390], sig=["能量 ↑"], img="R8_two_step_potential_profile.png",
         tag="R8 两步势能剖面"),
    # ---- 过渡金属催化.md (LF) ----
    dict(f="有机化学/过渡金属催化.md", kind="delete", s=87, e=104, af=[87, 104],
         sig=["                       氧化加成"], tag="D2 删与上方 Suzuki 图重复的通用循环框"),
]


def fence(s):
    return s.rstrip("\r").strip() == "```"


def blank(s):
    return s.strip() == ""


def main():
    byfile = {}
    for o in OPS:
        byfile.setdefault(o["f"], []).append(o)
    total_delta = 0
    for rel, ops in byfile.items():
        p = os.path.join(SRC, rel)
        lines = io.open(p, encoding="utf-8", newline="").read().split("\n")
        crlf = lines[0].endswith("\r") if lines else False
        EOL = "\r" if crlf else ""
        c0 = sum(1 for x in lines if fence(x))
        nocr0 = [i + 1 for i, x in enumerate(lines[:-1]) if not x.endswith("\r")]
        n_nocr0 = len(nocr0)
        print("=" * 88)
        print("%s  EOL=%s  原围栏行=%d  行数=%d  非CR行=%d"
              % (rel, "CRLF" if crlf else "LF", c0, len(lines), n_nocr0))
        want_delta = 0
        for o in sorted(ops, key=lambda z: -z["s"]):
            s, e = o["s"], o["e"]
            for ln in o["af"]:
                assert fence(lines[ln - 1]), "[%s] L%d 非裸围栏: %r" % (o["tag"], ln, lines[ln - 1])
            blk = "\n".join(lines[s - 1:e])
            for sg in o["sig"]:
                assert sg in blk, "[%s] 块内断言失败(缺 %r)" % (o["tag"], sg)
            pre_b = s >= 2 and blank(lines[s - 2])
            post_b = e < len(lines) and blank(lines[e])
            # 围栏行数变化：每个真代码块 = 2 行裸围栏；删 callout 之类无围栏 → 0
            fd = -2 if o["af"] else 0
            if o["kind"] in ("replace", "textify"):
                repl = []
                if not pre_b:
                    repl.append("")
                if o["kind"] == "replace":
                    # 缩进从「围栏行」取——块内 ASCII 自身的缩进是画图用的，不能当 Markdown 缩进
                    fl = lines[s - 1]
                    ind = fl[:len(fl) - len(fl.lstrip())]
                    repl.append(ind + "![[%s.png]]" % H[o["img"]])
                else:
                    repl += list(o["lines"])
                if not post_b:
                    repl.append("")
            elif o["kind"] == "delete":
                repl = [""] if (pre_b == post_b) else []
            else:
                raise SystemExit("unknown kind " + o["kind"])
            want_delta += fd
            print("  [%-28s] L%d-%d → %d 行 | 前空=%-5s 后空=%s"
                  % (o["tag"], s, e, len(repl), pre_b, post_b))
            blk_eol = "\r" if lines[s - 1].endswith("\r") else ""   # 跟随该块自身行尾
            lines[s - 1:e] = [x + blk_eol for x in repl]
        c1 = sum(1 for x in lines if fence(x))
        assert c1 == c0 + want_delta, "%s 围栏 %d ≠ %d" % (rel, c1, c0 + want_delta)
        print("  ✓ 围栏 %d → %d（期望 %+d）" % (c0, c1, want_delta))
        if crlf:
            bad = [i + 1 for i, x in enumerate(lines[:-1]) if not x.endswith("\r")]
            assert len(bad) == n_nocr0, \
                "%s 非 CR 行数 %d ≠ 原 %d（新增 %s）" % (rel, len(bad), n_nocr0, bad[:10])
            if n_nocr0:
                print("  · 历史遗留非 CR 行 %d 行（%s），未被本次改动波及" % (n_nocr0, nocr0[:5]))
        total_delta += want_delta
        if APPLY:
            io.open(p, "w", encoding="utf-8", newline="").write("\n".join(lines))
            print("  → 已写入")
        else:
            print("  (dry-run，未写入)")
    print("=" * 88)
    print("围栏行总变化 %+d ；预期最终 %d 行裸围栏 = %d 个真代码块"
          % (total_delta, 90 + total_delta, (90 + total_delta) // 2))


if __name__ == "__main__":
    main()
