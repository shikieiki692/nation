# -*- coding: utf-8 -*-
r"""渲染「Q8 解析加厚样板」预览件（含题面、答案、新旧解析对照与量化）。"""
import importlib.util
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Obsidion\妙妙屋")
OP = ".workbuddy/tmp/opt_pipe/"

spec = importlib.util.spec_from_file_location("probe", OP + "anO2_probe_Q8.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def block_of(d):
    out = ["> —— 解析 ——", ">"]
    out += ["> **考点**：" + d["考点"], ">"]
    out += ["> **思路**：" + d["思路"], ">"]
    for tag, score, txt in d["步骤"]:
        head = "> **%s**" % tag
        head += ("（%s）" % score) if score and score not in ("—", "-", "") else "："
        out += [head + txt, ">"]
    out += ["> **易错**：" + d["易错"], ">"]
    if d.get("举一反三"):
        out += ["> **举一反三**：" + d["举一反三"], ">"]
    if d.get("溯源"):
        out += ["> **溯源**：" + d["溯源"], ">"]
    out += [""]
    return out


new = block_of(m.A8[8])
newtxt = "\n".join(new)
cjk_new = len(re.findall(r"[\u4e00-\u9fff]", newtxt))

V = "04-题库/初赛模拟卷O2（有机·答案版）.md"
L = io.open(V, encoding="utf-8-sig", newline="").read().replace("\r\n", "\n").split("\n")
s = next(i for i, l in enumerate(L) if l.startswith("### 第 8 题"))
e = next(i for i, l in enumerate(L) if l.startswith("### 第 9 题"))
q = L[s:e]
old_i = next((i for i, l in enumerate(q) if l.strip() == "> —— 解析 ——"), None)
old = q[old_i:] if old_i else []
cjk_old = len(re.findall(r"[\u4e00-\u9fff]", "\n".join(old)))
body = q[:old_i] if old_i else q

doc = []
doc.append("---")
doc.append("title: O2 解析加厚样板（第 8 题）")
doc.append("type: 审计")
doc.append("status: 待 owner 验收")
doc.append("tags: [组卷线, O2, 解析加厚, 样板]")
doc.append("created: 2026-10-16")
doc.append("---")
doc.append("")
doc.append("# O2 解析加厚样板 · 第 8 题（构象分析与 A¹,³ 张力）")
doc.append("")
doc.append("> **验收要点**：本件只改「解析」段，题面与答案**一字未动**。口径＝owner 已拍板的"
           "**六维全做**（判据直引／答案图逐张落位／分步数值／得分点拆解／举一反三／教材溯源）"
           "＋ **`[[页名]]` wikilink**（docx 侧实测会剥方括号、只印页名；Obsidian 侧可跳转）。")
doc.append("")
doc.append("| 指标 | 旧稿 | 本样板 |")
doc.append("|:--|--:|--:|")
doc.append("| 解析正文汉字 | %d | **%d** |" % (cjk_old, cjk_new))
doc.append("| 引用知识点页 | 7 个（仅页名，`〈〉` 裸文本） | **%d 处 `[[ ]]` 真链接** |"
           % len(re.findall(r"\[\[", newtxt)))
doc.append("| 知识点页资产直引 | 无 | 4 张定量表 ＋ 3 条关键结论 ＋ 2 张易错点表 ＋ 2 个现成例题 |")
doc.append("| 答案图落位 | **0 张**（且 8-1-1 臆断「答案 (a)」＝**错**） | **10 张逐张落位**（含 `4e091d2d` 内嵌「8-1-1 b（2分）」实证） |")
doc.append("| 得分点拆解 | 无 | 8 个小问逐条 |")
doc.append("| 举一反三 | 无 | 4 条库内题 |")
doc.append("| 教材溯源 | 无 | Clayden 第16章 ＋ 教学洞察页 |")
doc.append("")
doc.append("> ⚠️ **本样板纠正的旧稿错误**：旧稿 8-1-1 写「答案 (a)」——卷内答案图 `4e091d2d`"
           "明确写「**8-1-1 b（2分）**」；848/850 行的 `(a)/(b)` 是**题面回显选项**，不是答案。")
doc.append("")
doc.append("---")
doc.append("")
doc.append("## 一 题面与答案（原文，未改动）")
doc.append("")
doc.extend(body)
doc.append("")
doc.append("---")
doc.append("")
doc.append("## 二 新解析（加厚版 · 六维）")
doc.append("")
doc.extend(new)
doc.append("")
doc.append("---")
doc.append("")
doc.append("## 三 旧解析（对照用，将被替换）")
doc.append("")
doc.extend(old if old else ["（无）"])

out = "09-审计报告/2026-10-16-O2解析加厚样板-Q8.md"
io.open(out, "w", encoding="utf-8", newline="\n").write("\n".join(doc) + "\n")
print("旧稿汉字 %d → 新稿汉字 %d（×%.2f）" % (cjk_old, cjk_new, cjk_new / max(1, cjk_old)))
print("wikilink 处数 =", len(re.findall(r"\[\[", newtxt)))
print("样板 →", out)
