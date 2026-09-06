# -*- coding: utf-8 -*-
"""
生成《全库图片引用体检报告》—— 在 audit_vault_images.py 基础上剔除噪音：
  · 占位示例（<hash>.jpg / xxx.jpg / path 等）
  · 归档与备份目录（_归档/、备份/、_archive 等，非活跃内容）
只保留真缺失，并按"目录整个不存在 / 目录存在但图缺"归因。
"""
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

VAULT = r"C:\Obsidion\妙妙屋"
OUT = os.path.join(
    VAULT, "09-审计报告", f"全库图片引用体检-{datetime.now():%Y-%m-%d}.md"
)
IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
SKIP = {".git", ".obsidian", "node_modules", ".workbuddy"}

# 占位示例特征
PLACEHOLDER = re.compile(
    r"^(<[^>]*>|xxx?\.[a-z]{3,4}|path|path/to/.*|foo\..*|bar\..*|example\..*"
    r"|.*\b(hash|占位|示例)\b.*|(?:\.{1,2}/)*[A-Za-z]*hash[A-Za-z]*\.[a-z]{3,4})$",
    re.I,
)
# 归档 / 备份
ARCHIVE = re.compile(r"(_归档|/_archive|archive|备份[\\/]|/备份|[\\/]old[\\/]|_old)", re.I)

stat = defaultdict(int)
real_missing = defaultdict(list)  # 顶层目录 -> [(文件, 路径)]
no_dir = defaultdict(set)         # 缺失的图片目录 -> 引用它的 md
has_dir = defaultdict(int)        # 目录存在但图缺 -> 缺几张
top_stat = defaultdict(lambda: defaultdict(int))

for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
    for fn in files:
        if not fn.endswith(".md"):
            continue
        fp = os.path.join(root, fn)
        rel_fp = os.path.relpath(fp, VAULT)
        top = rel_fp.split(os.sep)[0]
        try:
            text = open(fp, encoding="utf-8").read()
        except Exception:
            continue

        for m in IMG.finditer(text):
            path = m.group(2).strip().replace("\\", "/").rstrip("/")
            if path.startswith(("http://", "https://", "data:")):
                stat["外链"] += 1
                continue
            stat["引用总数"] += 1

            ap = os.path.normpath(os.path.join(root, path))
            if os.path.isfile(ap):
                stat["1.相对命中"] += 1
                top_stat[top]["ok"] += 1
                continue
            stripped = path
            while stripped.startswith("../"):
                stripped = stripped[3:]
            if os.path.isfile(os.path.normpath(os.path.join(VAULT, path))):
                stat["2.根兜底命中"] += 1
                top_stat[top]["ok"] += 1
            elif os.path.isfile(os.path.normpath(os.path.join(VAULT, stripped))):
                stat["3.剥../可修"] += 1
                top_stat[top]["fixable"] += 1
            elif PLACEHOLDER.match(stripped):
                stat["4.占位示例(噪音)"] += 1
            elif ARCHIVE.search(rel_fp):
                stat["5.归档备份(噪音)"] += 1
            else:
                stat["6.真缺失"] += 1
                top_stat[top]["missing"] += 1
                real_missing[top].append((rel_fp, path))
                d = os.path.dirname(ap)
                if os.path.isdir(d):
                    has_dir[os.path.relpath(d, VAULT)] += 1
                else:
                    no_dir[os.path.relpath(d, VAULT)].add(rel_fp)

# ---------------- 写报告 ----------------
L = []
w = L.append
w("---")
w("title: 全库图片引用体检报告")
w("type: 审计报告")
w(f"created: {datetime.now():%Y-%m-%d}")
w("tags: [审计, 图片, 体检, 资产]")
w("---")
w("")
w("# 全库图片引用体检报告")
w("")
w(f"> 扫描时间：{datetime.now():%Y-%m-%d} ｜ 范围：vault 全库 md ｜ 脚本：`.workbuddy/scripts/gen_vault_img_report.py`")
w("> 起因：`03-知识点/高中化学基础` 图片路径损坏，修复后回扫全库确认是否为同一根因。")
w("")
w("## 一、总览")
w("")
w("| 分类 | 数量 | 说明 |")
w("|------|------|------|")
for k in ["引用总数", "外链", "1.相对命中", "2.根兜底命中", "3.剥../可修",
          "4.占位示例(噪音)", "5.归档备份(噪音)", "6.真缺失"]:
    note = {
        "1.相对命中": "Obsidian 主解析路径，正常",
        "2.根兜底命中": "fallback 到 vault 根，能显示但不规范",
        "3.剥../可修": "**同高中化学基础病灶，可机械修复**",
        "4.占位示例(噪音)": "文档里的 `<hash>.jpg`、`xxx.jpg` 等示意文本",
        "5.归档备份(噪音)": "`_归档/`、`备份/` 下非活跃内容，无需修",
        "6.真缺失": "**图片资产本身缺失，脚本无法修复**",
    }.get(k, "")
    w(f"| {k} | {stat[k]} | {note} |")
w("")
w("**有效引用** = 相对命中 + 根兜底命中；**待处理** = 剥`../`可修 + 真缺失。")
w("")

w("## 二、按顶层目录")
w("")
w("| 顶层目录 | 正常 | 可修(剥`../`) | 真缺失 |")
w("|----------|------|--------------|--------|")
rows = [(c["fixable"] + c["missing"], d, c["ok"], c["fixable"], c["missing"])
        for d, c in top_stat.items()]
for _, d, ok, fx, ms in sorted(rows, reverse=True):
    if fx == 0 and ms == 0:
        continue
    w(f"| `{d}` | {ok} | {fx} | {ms} |")
w("")

w("## 三、真缺失归因")
w("")
w("真缺失分两种性质，处置方式完全不同：")
w("")
w(f"- **A. 图片目录整个不存在**：{len(no_dir)} 个目录 —— 导入时图片资产就没拷进来，")
w("  属数据丢失，**脚本无法修复**，只能回源重新导入。")
w(f"- **B. 目录存在但个别图缺**：{len(has_dir)} 个目录 —— 目录在、文件少，")
w("  可能是导入中断或部分图未落盘。")
w("")

if no_dir:
    w("### A. 图片目录整个不存在（按影响 md 数排序）")
    w("")
    w("| 缺失的图片目录 | 被引用 md 数 |")
    w("|----------------|-------------|")
    for d, fs in sorted(no_dir.items(), key=lambda x: -len(x[1])):
        w(f"| `{d}` | {len(fs)} |")
    w("")

if has_dir:
    w("### B. 目录存在但图缺失")
    w("")
    w("| 图片目录 | 缺失张数 |")
    w("|----------|---------|")
    for d, c in sorted(has_dir.items(), key=lambda x: -x[1]):
        w(f"| `{d}` | {c} |")
    w("")

w("## 四、可机械修复清单（活跃内容）")
w("")
w("与 `03-知识点/高中化学基础` 同一病灶：`../` 多写了一层，剥掉后即可命中。")
w("修复方式参照 `fix_gaozhong_p0.py` 的图片处理段（相对路径统一重算为 vault 根相对路径）。")
w("")
w("**已排除归档与备份目录** —— 那 440 处 100% 落在")
w("`09-审计报告/备份/题库修复-2026-08-31/` 与 `04-课件/习题集/_归档/习题书-旧版-2026-08-30/`，")
w("是历史快照，不属于活跃内容，无需修复（详见下节）。")
w("")
w("| 文件 | 引用路径 |")
w("|------|---------|")
cnt = 0
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
    for fn in files:
        if not fn.endswith(".md"):
            continue
        fp = os.path.join(root, fn)
        rel_fp = os.path.relpath(fp, VAULT)
        if ARCHIVE.search(rel_fp):
            continue
        try:
            text = open(fp, encoding="utf-8").read()
        except Exception:
            continue
        for m in IMG.finditer(text):
            path = m.group(2).strip().replace("\\", "/")
            if path.startswith("http") or PLACEHOLDER.match(path.lstrip("./")):
                continue
            ap = os.path.normpath(os.path.join(root, path))
            if os.path.isfile(ap):
                continue  # 相对命中，正常
            # 根兜底也能命中的属于"能显示但不规范"，不列入可修清单
            if os.path.isfile(os.path.normpath(os.path.join(VAULT, path))):
                continue
            st = path
            while st.startswith("../"):
                st = st[3:]
            if os.path.isfile(os.path.normpath(os.path.join(VAULT, st))):
                cnt += 1
                w(f"| `{rel_fp}` | `{path[:88]}` |")
w("")
if cnt == 0:
    w("**合计 0 处。**")
    w("")
    w("> ✅ **结论：`03-知识点/高中化学基础` 的图片路径问题是孤例，不是库级通病。**")
    w("> 全库活跃内容中再无同类病灶，该目录的修复已覆盖全部此类问题。")
else:
    w(f"合计 {cnt} 处。")
w("")
w("## 五、归档/备份目录里的 440 处（无需处理）")
w("")
w("这 440 处虽与上述病灶同型，但全部位于历史快照内，修了反而会让快照与当时状态不符：")
w("")
w("| 目录 | 处数 |")
w("|------|------|")
arch_stat = defaultdict(int)
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
    for fn in files:
        if not fn.endswith(".md"):
            continue
        fp = os.path.join(root, fn)
        rel_fp = os.path.relpath(fp, VAULT)
        if not ARCHIVE.search(rel_fp):
            continue
        try:
            text = open(fp, encoding="utf-8").read()
        except Exception:
            continue
        for m in IMG.finditer(text):
            path = m.group(2).strip().replace("\\", "/")
            if path.startswith("http") or PLACEHOLDER.match(path.lstrip("./")):
                continue
            if os.path.isfile(os.path.normpath(os.path.join(root, path))):
                continue
            if os.path.isfile(os.path.normpath(os.path.join(VAULT, path))):
                continue
            st = path
            while st.startswith("../"):
                st = st[3:]
            if os.path.isfile(os.path.normpath(os.path.join(VAULT, st))):
                key = "/".join(rel_fp.split(os.sep)[:3])
                arch_stat[key] += 1
for k, v in sorted(arch_stat.items(), key=lambda x: -x[1]):
    w(f"| `{k}` | {v} |")
w(f"| **合计** | **{sum(arch_stat.values())}** |")
w("")

w("## 六、⚠️ 版本控制注意事项（重要）")
w("")
w("`.gitignore` 第 9 行忽略了整个 `媒体仓库/`，但**图片来源仓是入库的**：")
w("")
w("| 目录 | 是否纳入 git | 影响 |")
w("|------|-------------|------|")
w("| `媒体仓库/` | ❌ 被忽略 | 库内约 18,620 张图不在版本控制中 |")
w("| `06-外部资料导入/**_images/` | ✅ 入库 | OCR 来源图有版本备份 |")
w("| `人教版高中化学课本/**_images/` | ✅ 入库 | 教材来源图有版本备份 |")
w("")
w("**推论**：若只从 git 仓库恢复，`![[哈希.jpg]]` 形式的引用会全部断图。")
w("本地环境两份都在，显示正常；但灾备角度，**源图所在的来源仓才是唯一有版本备份的副本**。")
w("")
w("本次高中化学基础的 58 张图**源图已全部保留**（见上一份报告 8.3），")
w("因此两份副本并存，本地与灾备均安全。")
w("")
w("> 是否把 `媒体仓库/` 纳入版本控制属于仓库策略选择（体积约数 GB），")
w("> 本报告只陈述事实，未改动 `.gitignore`。")
w("")
w("---")
w("")
w("*本报告由脚本自动生成，可复现（只读，未修改任何文件）。*")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="") as fh:
    fh.write("\n".join(L))

print("已生成:", OUT)
print()
for k in ["引用总数", "1.相对命中", "2.根兜底命中", "3.剥../可修",
          "4.占位示例(噪音)", "5.归档备份(噪音)", "6.真缺失"]:
    print(f"  {k:<22}{stat[k]:>7}")
print(f"\n  A.目录整个不存在: {len(no_dir)}")
print(f"  B.目录存在但图缺: {len(has_dir)}")
