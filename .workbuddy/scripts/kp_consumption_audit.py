# -*- coding: utf-8 -*-
"""统计 30 项 KP 待完善任务涉及的 KP 被讲义/备课消费的引用度。
只读，不写任何文件。"""
import glob
import os
import re

ROOT = r"C:\Obsidion\妙妙屋"

KPS = [
    "元素周期律", "原子半径", "方程式书写", "物料守恒", "电解池",
    "Feltham-Enemark记号", "水的特殊性", "硼酸盐", "磷及其化合物",
    "缺电子化合物", "间隙化合物", "1,2-迁移与重排", "Brook重排",
    "Grossman规则", "α效应", "不对称合成", "亲核体与亲电体", "共振论",
    "共轭效应", "影响亲核性的因素", "有机化学基础", "生物碱",
    "立体选择性", "糖苷", "非对映选择性", "元素推断",
]

# 消费端目录
CONSUMERS = {
    "学生讲义": os.path.join(ROOT, "04-课件", "学生讲义"),
    "备课大纲": os.path.join(ROOT, "04-课件", "备课大纲"),
    "专题页": os.path.join(ROOT, "04-专题与题型"),
    "题库": os.path.join(ROOT, "04-题库"),
}

# 预读消费端所有 md
def load_md(base):
    out = []
    if not os.path.isdir(base):
        return out
    for fp in glob.glob(os.path.join(base, "**", "*.md"), recursive=True):
        try:
            with open(fp, encoding="utf-8") as f:
                out.append((fp, f.read()))
        except Exception:
            pass
    return out

consumer_text = {}
for name, base in CONSUMERS.items():
    consumer_text[name] = load_md(base)
    print("[加载] %s: %d 文件" % (name, len(consumer_text[name])))

print()
print("| KP | 学生讲义 | 备课大纲 | 专题页 | 题库 | 合计 |")
print("|:--|--:|--:|--:|--:|--:|")

rows = []
for kp in KPS:
    # 链接形式 [[kp]] 或 [[路径/kp]] 或 [[kp|别名]]
    pat = re.compile(r"\[\[(?:[^\[\]|]*/)?%s(?:\|[^\[\]]*)?\]\]" % re.escape(kp))
    counts = {}
    for name in CONSUMERS:
        c = 0
        for fp, txt in consumer_text[name]:
            c += len(pat.findall(txt))
        counts[name] = c
    total = sum(counts.values())
    rows.append((total, kp, counts))

rows.sort(reverse=True)
for total, kp, counts in rows:
    print("| %s | %d | %d | %d | %d | **%d** |" % (
        kp, counts["学生讲义"], counts["备课大纲"], counts["专题页"], counts["题库"], total))

print()
zero = [r for r in rows if r[0] == 0]
low = [r for r in rows if 1 <= r[0] <= 5]
high = [r for r in rows if r[0] > 5]
print("=== 汇总 ===")
print("零引用 KP：%d 个 -> %s" % (len(zero), ", ".join(r[1] for r in zero)))
print("低引用 (1-5)：%d 个" % len(low))
print("中高引用 (>5)：%d 个 -> %s" % (len(high), ", ".join("%s(%d)" % (r[1], r[0]) for r in high)))
