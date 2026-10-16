# -*- coding: utf-8 -*-
r"""登记 O2 第五轮修补进 vol_meta_O2.json::md_patches。"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
O = r"C:/Obsidion/妙妙屋/.workbuddy/tmp/opt_pipe"

ADD = [
    {
        "script": "add_analysis.py (--data anO2_data1.py,anO2_data2.py)",
        "why": "四段式结构化解析 ×10（考点／思路／步骤／易错），插在各题答案区之后、块尾 `---` 之前。"
               "本卷口味：答案多以**结构图**呈现 ⇒ 解析以「机理路径 ＋ 考点 ＋ 易错」为主体，不复述具体结构。",
        "apply": "python .workbuddy/tmp/opt_pipe/add_analysis.py --vol O2 "
                 "--md \"04-题库/初赛模拟卷O2（有机·答案版）.md\" "
                 "--data .workbuddy/tmp/opt_pipe/anO2_data1.py,.workbuddy/tmp/opt_pipe/anO2_data2.py",
        "added": "2026-10-16",
    },
    {
        "script": "o2_q7_residue_fix.py",
        "why": "第 7 题答案区删除 **31 行残缺引用块**（`> 源：`…`> 参考结构：`；内容与下方清理后答案重复、"
               "且含 `> 示。`／`> 移程度大于B。`／`> 方式。` 等碎片行；全卷仅此 1 处、卷 O1 为 0 处 ⇒ 系 `--ans` 时代残渣）。"
               "其中**唯一独有信息 `杂化为sp3 杂化`（7-6 答案）已保留**；另修 2 处："
               "`**7-4** ABCE` 与 `D 中错误…` **粘连**⇒插分隔、`7-6` 行补 `**7-6**` 标。",
        "apply": "python .workbuddy/tmp/opt_pipe/o2_q7_residue_fix.py",
        "added": "2026-10-16",
    },
    {
        "script": "o2_q4_glue_fix.py",
        "why": "第 4 题**标签粘连**（源号与年份被 OCR 粘连，同卷 X `md_patches` 的「类 B 连字符源号」缺陷）："
               "`4-1-12021 年` → `4-1-1 2021 年`、`4-32023 年` → `4-3 2023 年`（卷两版＋源卡 GM-10-08 同改）。",
        "apply": "python .workbuddy/tmp/opt_pipe/o2_q4_glue_fix.py",
        "added": "2026-10-16",
    },
]


def main():
    p = os.path.join(O, "vol_meta_O2.json")
    d = json.load(io.open(p, encoding="utf-8"))
    mp = d.setdefault("md_patches", [])
    have = {x.get("script") for x in mp}
    add = [x for x in ADD if x["script"] not in have]
    mp.extend(add)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=1))
    print("vol_meta_O2.json md_patches: +%d → 共 %d 项" % (len(add), len(mp)))
    for x in mp:
        print("   -", x["script"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
