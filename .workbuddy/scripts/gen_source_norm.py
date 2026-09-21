# -*- coding: utf-8 -*-
"""新增 source_norm 字段：按【路径】推导归一化来源名，供组卷「同源限流 ≤N」真正生效。

为什么按路径而不是按 source 字符串：source 存的是「来源+题号」（如 `…第1题`、
`Clayden … Chapter 6 Problem 1`），同书被拆成几百个值（2,187 个去重值 / 2,024 个只出现 1 次）。
路径是权威的：文件本就按来源目录归档，且能把 `元文件/教材习题/无机化学例题与习题`
与 `教材习题/无机化学例题与习题` 这类「同书两处」自动合并。

用法：python gen_source_norm.py            # dry-run
      python gen_source_norm.py --write    # 实写
安全：newline="" 保行尾；断言「删掉插入行后逐字还原原文」；已有 source_norm 则跳过。
"""
import io
import os
import re
import sys
import time
from collections import Counter

WRITE = "--write" in sys.argv
ROOT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(ROOT, "04-题库")
TYPES = {"题目", "真题", "题组", "题目集"}
RX_ZHENTI = re.compile(r"^真题/第(\d+)届(初赛|决赛)")

# 长前缀须排在短前缀之前
RULES = [
    # ── 真题：按届/省，保粒度（综合模拟卷要求真题占比 ≥60%，若真题算单一源则限流会锁死）──
    ("真题/省预赛/江苏卷", "省预赛·江苏"),
    ("真题/省预赛/福建卷", "省预赛·福建"),
    ("真题/省预赛/浙江卷2021", "省预赛·浙江2021"),
    ("真题/省预赛/浙江卷2022", "省预赛·浙江2022"),
    ("真题/省预赛/浙江卷2023", "省预赛·浙江2023"),
    ("真题/省预赛", "省预赛·其他"),
    ("真题/第36届初赛第二场", "第36届初赛第二场"),
    # ── 教材习题：逐源正名 ──
    ("教材习题/化学竞赛初赛讲义", "化学竞赛初赛讲义"),
    ("教材习题/赵鑫光", "赵鑫光《高中化学竞赛基本理论学习笔记》"),
    ("教材习题/Clayden", "Clayden 有机化学"),
    ("教材习题/高中化学竞赛教程第一分册", "高中化学竞赛教程第一分册"),
    ("教材习题/高中化学竞赛教程第二分册", "高中化学竞赛教程第二分册"),
    ("教材习题/结构化学基础", "结构化学基础（周公度·第5版）"),
    ("教材习题/一分册能力测试", "一分册能力测试"),
    ("教材习题/二分册能力测试", "二分册能力测试"),
    ("教材习题/无机化学例题与习题", "无机化学例题与习题（徐佳宁·第4版）"),
    ("教材习题/ABOC", "ABOC 有机化学"),
    ("教材习题/上海中学竞赛课程", "上海中学竞赛课程"),
    ("教材习题/化学能力测试", "化学能力测试"),
    ("教材习题/汇智竞赛题目", "汇智竞赛题目"),
    ("教材习题/无机化学第6版Weller", "无机化学第6版（Weller）"),
    ("教材习题/北斗学友", "北斗学友竞赛模拟卷"),
    ("教材习题/中级无机化学", "中级无机化学"),
    ("教材习题/无机化学第5版", "无机化学第5版"),
    ("教材习题/化竟能力测试", "化竟能力测试（已废弃）"),
    ("教材习题/", "（未归类教材习题）"),
    # ── 元文件：同书合并回教材习题的规范名 ──
    ("元文件/教材习题/无机化学例题与习题", "无机化学例题与习题（徐佳宁·第4版）"),
    ("元文件/教材习题/结构化学基础", "结构化学基础（周公度·第5版）"),
    ("元文件/教材习题/赵鑫光", "赵鑫光《高中化学竞赛基本理论学习笔记》"),
    ("元文件/教材习题/化学竞赛初赛讲义", "化学竞赛初赛讲义"),
    ("元文件/教材习题/上海中学竞赛课程", "上海中学竞赛课程"),
    ("元文件/教材习题/无机化学第6版Weller", "无机化学第6版（Weller）"),
    ("元文件/教材习题/物理化学Atkins", "Atkins 物理化学（第11版）"),
    ("元文件/", "（元文件其他）"),
    # ── 自编/改编 ──
    ("化学原理/", "普通化学原理（第4版）习题解析"),
    ("有机化学/", "自编·有机化学"),
    ("分析化学/", "自编·分析化学"),
    ("元素化学/", "自编·元素化学"),
    ("物理化学/", "自编·物理化学"),
    ("教学改编题/", "教学改编题"),
    ("经典例题/", "经典例题"),
    # ── 其他 ──
    ("05-真题库/", "05-真题库（真题讲评层）"),
]


def norm_of(qrel, rel):
    for pre, val in RULES:
        if qrel.startswith(pre) or rel.startswith(pre):
            return val
    # 真题届次（通用）：「真题/第25届初赛」「真题/第39届决赛」
    for s in (qrel, rel):
        m = RX_ZHENTI.match(s)
        if m:
            return "第%s届%s" % (m.group(1), m.group(2))
    return None


stat = Counter()
vals = Counter()
edits = []
unmatched = []

for base in ("04-题库", "05-真题库"):
    for dp, dn, fn in os.walk(os.path.join(ROOT, base)):
        for f in fn:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            qrel = rel.split("/", 1)[1] if rel.startswith("04-题库/") else rel
            t = io.open(p, encoding="utf-8", newline="").read()
            if not t.startswith("---"):
                continue
            ls = t.split("\n")
            end = None
            for i in range(1, len(ls)):
                if ls[i].strip() == "---":
                    end = i
                    break
            if end is None:
                continue
            fm = "\n".join(ls[1:end])
            d = {}
            for line in fm.split("\n"):
                if ":" in line:
                    k, _, v = line.partition(":")
                    d[k.strip()] = v.strip()
            if d.get("type") not in TYPES:
                continue
            if d.get("source_norm"):
                stat["已有 source_norm"] += 1
                continue
            v = norm_of(qrel, rel)
            if v is None:
                unmatched.append(rel)
                continue
            stat["待写"] += 1
            vals[v] += 1
            edits.append((p, rel, v))

print("[%s]" % ("WRITE" if WRITE else "DRY-RUN"))
for k, c in sorted(stat.items()):
    print("  %-18s %5d" % (k, c))
print("  → 归一化后 distinct 值：%d" % len(vals))
if unmatched:
    print("  ⚠ 未匹配规则 %d 条（前 10）：" % len(unmatched))
    for r in unmatched[:10]:
        print("     " + r)
print()
print("归一化后各来源题量：")
for k, v in vals.most_common():
    print("  %5d  %s" % (v, k))

if WRITE:
    n = 0
    fails = []
    for p, rel, v in edits:
        t = io.open(p, encoding="utf-8", newline="").read()
        ls = t.split("\n")
        end = None
        for i in range(1, len(ls)):
            if ls[i].strip() == "---":
                end = i
                break
        ls.insert(end, 'source_norm: "%s"' % v)
        nt = "\n".join(ls)
        m = nt.split("\n")
        back = [l for i, l in enumerate(m) if i != end]
        assert "\n".join(back) == t, "还原失败 %s" % rel
        ok = False
        last = ""
        for attempt in range(5):          # Windows 下偶发瞬时占用 → 重试
            try:
                with io.open(p, "w", encoding="utf-8", newline="") as fh:
                    fh.write(nt)
                ok = True
                break
            except OSError as e:
                last = "%s" % e
                time.sleep(0.4 * (attempt + 1))
        if ok:
            n += 1
        else:
            fails.append((rel, last))
    print()
    print("实写 %d 个文件" % n)
    if fails:
        print("⚠ 仍失败 %d 个（须重跑本脚本补齐）：" % len(fails))
        for rel, why in fails[:10]:
            print("   %s  %s" % (rel, why[:60]))
    else:
        print("✓ 无写入失败")
