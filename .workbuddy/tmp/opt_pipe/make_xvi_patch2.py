# -*- coding: utf-8 -*-
"""卷 XVI patch #2：清理卡内「文档性」杂质（重排说明/核验截图/杂标题/实验报告 H2）。"""
import json
import io

R = r"C:\Obsidion\妙妙屋"

def rd(p):
    return io.open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")

cfg = {}

# 1) CM-17-05：删题面重排说明、源答案标题行、节选说明、杂标题、源题面页截图段
t = rd(r"04-题库/2026机构初赛模拟题/chemy/题-CM-17-05-51在气相的硫单质中存在着等.md")
rules = []
# a) 题面区：重排说明引用块（含其后空行）
a1 = "> ⚠️ **源 OCR（MinerU）将第 5/6/7 题内容混排错序、题面标题丢失**。本卡正文据**源 PDF 题面页**与**源答案文件**（顺序完好）重排；配图取自答案文件，并与源 PDF 页一并附上供逐字核验。\n\n"
assert t.count(a1) == 1
rules.append([a1, ""])
# b) 题面区：重复的源标题行
a2 = "### 第 5 题 探索硫单质：气态、液态与固态（36 分，占总分的 16%）\n\n"
assert t.count(a2) == 1
rules.append([a2, ""])
# c) 答案区：节选说明行
a3 = "> 以下为**源答案文件**第 5 题节选（含题面复述与评分细则）。\n\n"
assert t.count(a3) == 1
rules.append([a3, ""])
# d) 答案区：杂标题
a4 = "## 两种邻位交叉构象\n\n"
assert t.count(a4) == 1
rules.append([a4, ""])
# e) 答案区尾部：源题面页截图段（标题+2 PNG）
i = t.find("## 源 PDF 题面页")
assert i > 0
j = t.find("## 知识点映射")
seg = t[i:j]
assert "源题面页-CM17-p4.png" in seg and "源题面页-CM17-p5.png" in seg
rules.append([seg, ""])
cfg["04-题库/2026机构初赛模拟题/chemy/题-CM-17-05-51在气相的硫单质中存在着等.md"] = rules

# 2) YJ-05-04：题面区 6 个实验报告 H2 → 加粗行
t2 = rd(r"04-题库/2026机构初赛模拟题/壹尖培优/题-YJ-05-04-在整个冷战期间苏联705型核.md")
rules2 = []
for h in ["铅铋合金中铋和铅的连续络合滴定", "试剂及仪器",
          "1. 配制 $0.02 \\mathrm{~mol} \\cdot \\mathrm{L}^{-1}$ EDTA 溶液",
          "2. 配制 $0.02 \\, mol \\cdot L^{-1}$ 锌标准溶液",
          "3. 标定 EDTA 溶液",
          "4. 铅铋合金的测定"]:
    old = "## " + h + "\n"
    assert t2.count(old) == 1, (h, t2.count(old))
    rules2.append([old, "**" + h + "**\n"])
cfg["04-题库/2026机构初赛模拟题/壹尖培优/题-YJ-05-04-在整个冷战期间苏联705型核.md"] = rules2

out = r".workbuddy/tmp/opt_pipe/xvi_patch2.json"
io.open(out, "w", encoding="utf-8").write(json.dumps(cfg, ensure_ascii=False, indent=1))
print("written", out, "cards:", len(cfg), "rules:", sum(len(v) for v in cfg.values()))
