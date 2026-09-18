# -*- coding: utf-8 -*-
"""重生成 第一轮·竞赛教材版/_总索引.md（数字全部取自 _选题清单.json）。"""
import io
import json
import os
import re
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = os.path.join("04-课件", "习题集", "第一轮·竞赛教材版")
man = json.load(io.open(os.path.join(D, "_选题清单.json"), encoding="utf-8"))

tot = sum(m["n"] for m in man)
unused = sum(m["unused"] for m in man)
srcs = Counter()
for m in man:
    for s in m["srcs"]:
        srcs[re.sub(r"《高中化学竞赛基本理论学习笔记》.*$", "《高中化学竞赛基本理论学习笔记》", s)] += 1


def rows(struct):
    out = []
    for m in man:
        if m["name"].startswith("结构") != struct:
            continue
        short = m["name"].split("-", 1)[1].split("-", 1)[-1] if "·" in m["name"] else m["name"]
        short = short.replace("结构·", "").replace("原理·", "")
        short = m["name"].split("-", 1)[1]
        b = m["bands"]
        dist = "基础%s/进阶%s/挑战%s" % (b.get("2", 0), b.get("3", 0), b.get("4", 0))
        top = "、".join(m["srcs"][:3])[:40]
        out.append("| %s | %d | %s | %d/%d | %s | [[第一轮%s（教师版）]] | [[第一轮%s（学生版）]] |"
                   % (m["name"], m["n"], dist, m["unused"], m["n"] - m["unused"], top, m["name"], m["name"]))
    return out


L = []
L += ["---",
      'title: "第一轮·竞赛教材版分章练习 总索引"',
      "type: 索引", "role: 习题集索引", "round: 第一轮", "status: 已填充",
      "created: 2026-09-16", "updated: 2026-09-17",
      "question_count: %d" % tot,
      "tags: [化竞, 第一轮, 竞赛教材版, 索引]", "---", "",
      "# 第一轮·竞赛教材版分章练习 · 总索引", "",
      "> **共 15 个专题、%d 题**（未出卷 %d / 回收已用 %d），每专题**教师版**（题干 + 参考答案）与**学生版**（纯题干）各一份，题号同序。"
      % (tot, unused, tot - unused),
      "> **题源纪律**：全部取自**竞赛导向**题源——赵鑫光竞赛笔记、上海中学竞赛课程、高中化学竞赛教程一·二分册、化学竞赛能力测试、一分册·二分册能力测试、汇智竞赛题目、北斗学友、化学竞赛初赛讲义、初赛·决赛真题。**不含非竞赛教材（大学教材课后习题：普通化学原理、结构化学基础、无机化学例题与习题、中级无机化学、Weller、Clayden）与高考题**——按 2026-09-17 规则，非竞赛教材只出现在「课后习题集」（`04-课件/习题集/习题书-*`）。",
      "> **选题方式**：按题目所在书目/讲次的**章标签**路由（不依赖已被错标的 `submodule` 字段），再经「题干非空 + 答案完整」双查，按 基础2 : 进阶8 : 挑战5 配额抽取。",
      "> **与既有材料的关系**：本系列是**独立成套**的竞赛教材版；`04-课件/习题集/第一轮化学原理-*习题集`（8 卷 454 题，普化占多数）与 `第一轮结构化学-*练习题组`（5 份 272 题）保持原状，可对照使用或择一替换。", "",
      "> **2026-09-17 扩量**：每套由 12 题扩到 **15 题**（比例沿用 2:6:4 的等比放大 → 基础2/进阶8/挑战5），共 %d 题（原 178）。" % tot, "",
      "## 一、结构化学第一轮（6 专题）", "",
      "| 专题 | 题数 | 难度分布 | 未用/已用 | 主要题源 | 教师版 | 学生版 |",
      "|:---|:---:|:---|:---|:---|:---|:---|"] + rows(True)
L += ["", "## 二、化学原理第一轮（9 专题）", "",
      "| 专题 | 题数 | 难度分布 | 未用/已用 | 主要题源 | 教师版 | 学生版 |",
      "|:---|:---:|:---|:---|:---|:---|:---|"] + rows(False)
L += ["", "## 三、题源构成汇总", "", "| 题源 | 出现题数 |", "|:---|:---:|"]
for k, v in srcs.most_common(20):
    L.append("| %s | %d |" % (k, v))
L += ["", "---", "", "## 四、说明与后续", "",
      "- **图片**：题干/答案中的图片按 `媒体仓库/` 哈希文件名引用（Obsidian 图片双链语法）。",
      "- **已知薄点**：结构·6 有机分子结构初探库内该主题竞赛题本就稀薄（路由命中仅 10 条，已全取）；",
      "  原理·2 溶液与相平衡、原理·5 化学平衡、原理·7 沉淀溶解平衡的**未用池**偏小，仍需回收既有专项卷用过的题（`used_in` 台账留存于源题文件中，卷面不再印出）。",
      "  ⚠️ 同因导致这几套**偏难**：原理·7 挑战 10 题、原理·2 挑战 9 题、原理·5 挑战 8 题（进阶未用见底，配额缺口由挑战补）。若要压难度，需放宽题源或减题量。",
      ""]

with io.open(os.path.join(D, "_总索引.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(L))
print("已写 _总索引.md：%d 专题 / %d 题 / 未用 %d" % (len(man), tot, unused))
