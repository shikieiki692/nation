# -*- coding: utf-8 -*-
"""续填 S1 清单 CSV 的「本会话目检定论」列（26 张全部定性；只改末列，不动其它列）。"""
import csv
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
CSV = os.path.join(R, "09-审计报告", "2026-10-09-机构域题面图位置缺陷清单.csv")

# 末列定性文本（按卡路径末段匹配）
VERDICT = {
    # ── 真 S1（题面引用图，图确在答案区；已逐张 Read 目检）──
    "题-XeC-07-04": "真S1·已目检(图1/图2＝电化学折线图；题面「如图1/图2所示」)",
    "题-CM-123-07": "真S1·已目检(Halpern 1982 催化循环机理图；题面「机理如下图所示」)",
    "题-CM-165-02": "真S1·已目检(ArF 定义式＋C₅ArF₅ 化合物；题面「下图所示化合物」)",
    "题-CM-17-07": "真S1·已目检(PtLCl₂ 配合物结构；题面「下图所示配合物」)",
    "题-CM-65-06": "真S1·已目检(富瓦烯双环结构；题面「结构如右图」)",
    "题-HYS-02-01": "真S1·已目检(源答案页扫描件含 ZrCp″₂(CO)₂ 结构；题面「下左图的化合物」)",
    "题-HYS-03-05": "真S1·已目检(Cu-S 二维层俯视图＋晶胞框；题面「俯视图与晶胞示意图」)",
    # ── 题面图缺失·未标注（图不在卡内任何位置）──
    "题-CM-106-01": "题面图缺失(1-5「烟花」图全卡无且未标注)⇒待回源补图",
    "题-HZ-02-05": "题面图缺失(奎宁结构图全卡无且未标注)⇒待回源补图",
    "题-GChO-42-04": "题面图缺失(元素转化关系图全卡无且未标注)⇒待回源补图",
    "题-HYS-01-01": "题面图缺失(配体结构 OCR 成文字串「Mes-N N Mes」，题面区无图)⇒待回源补图",
    # ── 题面图缺失·已自带「⛔ 待补图」标注（= 已知源缺图，非位置缺陷）──
    "题-CM-127-02": "已标注待补图·确认源缺图(机理示意图；卡内已标 ⛔待补图)",
    "题-YJ-05-02": "已标注待补图·确认源缺图(投影图；卡内已标 ⛔待补图)",
    "题-QBY-08-06": "已标注待补图·确认源缺图(实验结果图；卡内已标 ⛔待补图)",
    "题-UChO-01-05": "已标注待补图·确认源缺图(绝热容器图；卡内已标 ⛔待补图)",
    # ── 假阳性（题面无「引用已有图」语义，全为作答要求/描述）──
    "题-2ChO-01-04": "假阳性(题面仅「画出 X 的结构」作答要求)",
    "题-2ChO-02-07": "假阳性(「在一张图中画出…」作答要求；答案图走 HTML img)",
    "题-XeC-15-04": "假阳性(全为「画出…结构」作答要求)",
    "题-HZ-02-01": "假阳性(「31P NMR 谱图」为实验描述，非引用图)",
    "题-HZ-02-04": "假阳性(题面无图引用；答案区结构用数组式描述)",
    "题-HZ-38-02": "假阳性(全为「画出…结构」作答要求)",
    "题-HYS-03-01": "假阳性(全为「画出…结构」作答要求)",
    "题-GChO-42-06": "假阳性(「画出…投影图」作答要求)",
    "题-GChO-73-06": "假阳性(「c 轴投影图中」为条件描述)",
    "题-GChO-82-06": "假阳性(「93X NMR 谱」为实验描述)",
    "题-UChO-02-03": "假阳性(「画出…投影图」作答要求)",
}


def key_of(path):
    return os.path.basename(path)[:-3] if path.endswith(".md") else os.path.basename(path)


def main():
    with open(CSV, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    hdr, data = rows[0], rows[1:]
    assert hdr[-1] == "本会话目检定论", hdr
    n = 0
    for r in data:
        base = os.path.basename(r[0])[:-3]
        for k, v in VERDICT.items():
            if base.startswith(k):
                r[-1] = v
                n += 1
                break
    print("已填 %d 行（数据行共 %d）" % (n, len(data)))
    miss = [r[0] for r in data if not r[-1]]
    if miss:
        print("⚠️ 仍未定性：", miss)
    with open(CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(hdr)
        w.writerows(data)
    print("写盘完成:", CSV)


if __name__ == "__main__":
    main()
