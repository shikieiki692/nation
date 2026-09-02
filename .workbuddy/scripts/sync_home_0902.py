# -*- coding: utf-8 -*-
"""09-02 下午：首页入口文档同步（省预赛整合 + 三篇测试卷 + 高考待办核实）"""
import io, os, re

ROOT = r"C:\Obsidion\妙妙屋"

def load(path):
    return io.open(os.path.join(ROOT, path), encoding="utf-8", newline="").read()

def save(path, s):
    io.open(os.path.join(ROOT, path), "w", encoding="utf-8", newline="").write(s)

def sub(path, pairs, optional=False):
    s = load(path)
    for old, new in pairs:
        if old not in s:
            if optional:
                print("  (skip)", path, "|", old[:40])
                continue
            raise AssertionError(f"{path}: 未找到 {old[:60]!r}")
        s = s.replace(old, new, 1)
    save(path, s)
    print("OK", path)

# ============ 1. 状态摘要 ============
p = "00-首页/状态摘要.md"
s = load(p)
eol = "\r\n" if "\r\n" in s else "\n"
# 顶部新增置顶进展
s0 = load(p)
eol = "\r\n" if "\r\n" in s0 else "\n"
anchor = "# 状态摘要 · AI 启动必读" + eol
top_note = (
"> **🟢 省预赛整合 + 阶段测试卷收官（09-02，最新）**：**题库 3,946 → 4,186**（Warning 纹丝不动 1,641 / 0 error）。"
"① **省预赛图依赖题全部闭环**：江苏 24 图、福建 10 图逐张看图核验嵌入 13 个题目文件；浙江三卷查实主卷早已内嵌整页图 129 处，手册 80 题状态全关闭，题 4 悬案裁决（三氯异氰尿酸 C₃N₃O₃Cl₃，A/B 双解属原卷瑕疵）；"
"② **浙江三卷 240 道选择题按新题入库SOP拆题入库**：3 个并行代理逐题分类（KP 白名单硬约束），`04-题库/真题/省预赛/浙江卷2021|2022|2023/` 各 80 单题文件，0 断链 0 缺图；"
"③ **结构/有机/元素与分析三篇阶段测试卷生成**（各 50 题，d3→d5 梯度 + 跨子模块配额 + used_in 回填 150 处，0 死链 0 重复）；"
"④ **高考化学 1,482 文件题目化核实为过时待办**（该赛道 L1/L2/L3 早已完成，自有整卷+锚点规范即其题目化形态）。工作详情见 [[00-首页/工作日志/2026-09-02]]。"
)
assert anchor in s
s = s.replace(anchor, anchor + eol + top_note + eol, 1)
# 关键状态标题日期
s = s.replace("## 📊 当前关键状态（2026-09-01 · 使用期+深化期 · 维护+精品化 · 链接治理收官）",
              "## 📊 当前关键状态（2026-09-02 · 使用期+深化期 · 维护+精品化 · 省预赛入库收官）", 1)
# 健康基线行
s = s.replace(
 "| 健康基线 | validate_kb full **0 error / 1,641 warning**（2026-09-01 深夜终检实测）：",
 "| 健康基线 | validate_kb full **0 error / 1,641 warning**（2026-09-02 终检实测，受检 6,410 文件）：", 1)
# 新增阶段测试卷行（插在题库规模行后）
m = re.search(r"^\| 题库规模 \|.+$", s, re.M)
row = "| 阶段测试卷 | 四篇全齐：化学原理（历史）+ **09-02 新增**结构化学/有机化学/元素与分析各 50 题（模块习题集题池、d3→d5 梯度、used_in 回填 150 处）；化学原理卷 4 条重复链接留待专项维护 |"
s = s[:m.end()] + eol + row + s[m.end():]
s = re.sub(r"^updated: 2026-09-01$", "updated: 2026-09-02", s, count=1, flags=re.M)
save(p, s); print("OK", p)

# ============ 2. 工作日志总索引 ============
p = "00-首页/工作日志.md"
s = load(p)
eol = "\r\n" if "\r\n" in s else "\n"
anchor = "| 2026-09-01 | [[00-首页/工作日志/2026-09-01]] |"
idx = s.find(anchor)
assert idx > 0
# 找该行行尾
line_end = s.find(eol, idx)
row = ("| 2026-09-02 | [[00-首页/工作日志/2026-09-02]] | 省预赛整合日：江苏/福建图依赖题看图核验补图、浙江三卷悬案裁决+手册80题闭环、"
       "**浙江240题按SOP拆题入库（题库 3,946→4,186）**、结构/有机/元素与分析三篇阶段测试卷生成、高考化学待办核实为过时；Warning 保持 1,641（0 error） |")
s = s[:line_end] + eol + row + s[line_end:]
s = re.sub(r"^updated: 2026-09-01$", "updated: 2026-09-02", s, count=1, flags=re.M)
save(p, s); print("OK", p)

# ============ 3. 待办交接清单 ============
p = "00-首页/活跃任务/待办交接清单.md"
s = load(p)
eol = "\r\n" if "\r\n" in s else "\n"
s = s.replace("| 受检文件 | 6,167（validate_kb --full 终检） |",
              "| 受检文件 | 6,410（validate_kb --full 09-02 终检；较 09-01 +240 浙江拆题 +3 测试卷） |", 1)
s = s.replace("> ⚠️ **09-01 深夜终检全量实测（validate_kb --full）**：受检 **6,167 文件 / Error 0 / Warning 1,641**。",
              "> ⚠️ **09-02 终检全量实测（validate_kb --full，省预赛 240 拆题 + 三篇测试卷后）**：受检 **6,410 文件 / Error 0 / Warning 1,641**（warning 纹丝不动 = 新增 243 文件 0 断链 0 缺图）。09-01 终检（6,167 文件）构成：", 1)
# 最近已完成：顶部插入 09-02 条目
anchor = "## ✅ 最近已完成（勿重做）"
add = (anchor + eol + eol +
"- **省预赛整合 + 三篇测试卷（09-02）**：① 江苏 24 图 / 福建 10 图看图核验嵌入 13 题；浙江三卷整页图已全覆盖（手册 80 题状态关闭），题 4 裁决=三氯异氰尿酸（A/B 双解）；"
"② 浙江 240 题按 SOP 拆题入库（`浙江卷2021|2022|2023/` 各 80 文件，KP 白名单硬约束零断链，3 并行代理分类），题库 **3,946→4,186**；"
"③ 结构/有机/元素与分析阶段测试卷 ×50 题（used_in 150 处回填）；④ 高考化学「题目化」核实为过时待办（L1/L2/L3 早已完成）；⑤ 体系总纲 pack 矩阵同步（预赛专项 20→260）。"
"提交：8204a280 / 38be4340 / aa629df1 / 4dd54872。详见 [[00-首页/工作日志/2026-09-02]]。")
assert anchor in s
s = s.replace(anchor, add, 1)
s = re.sub(r"^updated: 2026-09-0\d$", "updated: 2026-09-02", s, count=1, flags=re.M)
save(p, s); print("OK", p)

# ============ 4. 任务卡 ============
p = "00-首页/活跃任务/任务卡-validate_kb每周运行.md"
s = load(p)
eol = "\r\n" if "\r\n" in s else "\n"
s = s.replace("| 受检文件 | 6407 |", "| 受检文件 | 6410 |", 1)
s = s.replace("- **2026-09-02 full（浙江拆题后）**：6407 文件 · **0 error / 1641 warning**（warning 纹丝不动 = 240 新题 0 断链 0 缺图）。报告 [[09-审计报告/auto-validation/2026-09-02-validation]]",
              "- **2026-09-02 full（三篇测试卷后，最新）**：6410 文件 · **0 error / 1641 warning**（省预赛 240 拆题 + 3 新卷 + 150 used_in 回填，warning 全程纹丝不动）。报告 [[09-审计报告/auto-validation/2026-09-02-validation]]\n- **2026-09-02 full（浙江拆题后）**：6407 文件 · **0 error / 1641 warning**（warning 纹丝不动 = 240 新题 0 断链 0 缺图）。报告 [[09-审计报告/auto-validation/2026-09-02-validation]]", 1)
s = re.sub(r"^updated: 2026-09-0\d$", "updated: 2026-09-02", s, count=1, flags=re.M)
save(p, s); print("OK", p)

# ============ 5. 活跃任务 ============
p = "00-首页/活跃任务.md"
s = load(p)
eol = "\r\n" if "\r\n" in s else "\n"
anchor = "> ✅ **当前判断（2026-09-01 链接治理专场）**："
add = ("> ✅ **当前判断（2026-09-02 省预赛整合）**：\n"
"> - **省预赛整合收官（09-02）**：**题库 3,946 → 4,186**。① 江苏/福建图依赖题看图核验补图（34 图嵌入 13 题）；浙江三卷整页图已全覆盖、手册 80 题闭环 + 题 4 悬案裁决（三氯异氰尿酸）；"
"② **浙江 240 题按新题入库SOP拆题入库**（3 并行代理分类、KP 白名单零断链）；③ 三篇阶段测试卷落地（各 50 题 + used_in 150 处）；④ 高考化学待办核实为过时；体系总纲 pack 矩阵同步（预赛专项 260）。详见 [[00-首页/工作日志/2026-09-02]]。\n")
assert anchor in s
s = s.replace(anchor, add + anchor, 1)
s = re.sub(r"^updated: 2026-09-0\d$", "updated: 2026-09-02", s, count=1, flags=re.M)
save(p, s); print("OK", p)

print("ALL DONE")
