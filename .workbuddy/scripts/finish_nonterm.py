# -*- coding: utf-8 -*-
"""收尾：回填空KP + 正文非术语红链转纯文本 + 模板related去重"""
import io, re

# 1) 回填空 knowledge_points
p1 = r"C:\Obsidion\妙妙屋\07-资料提炼\习题提炼\习题-结构化学基础-综合习题解析.md"
kps = ["一维势箱","分子轨道理论","键级","光谱项","原子结构","电离能","杂化轨道",
       "对映异构","配位化合物","18电子规则","EAN规则","系统消光","原子坐标参数",
       "分子晶体","NiAs型结构","六方密堆积","钙钛矿"]
s = io.open(p1, encoding="utf-8", newline="").read()
old = "knowledge_points:\n"
assert old in s, "未找到空 knowledge_points"
new = "knowledge_points:\n" + "".join(f'  - "[[{k}]]"\n' for k in kps)
s = s.replace(old, new, 1)
io.open(p1, "w", encoding="utf-8", newline="").write(s)
print("已回填 KP:", len(kps), "个 ->", p1)

# 2) 正文非术语红链转纯文本
edits = [
    (r"C:\Obsidion\妙妙屋\04-题库\教材习题\Clayden\题-459-Clayden-Ch28-P5-反应失败分析.md",
     "| [[推断题]] |", "| 推断题 |"),
    (r"C:\Obsidion\妙妙屋\07-资料提炼\书籍提炼\提炼-Clayden-PhaseD-习题拆题清单.md",
     " [[推断题]] |", " 推断题 |"),
    (r"C:\Obsidion\妙妙屋\07-资料提炼\书籍提炼\提炼-Clayden-第24章-区域选择性.md",
     "└── [[化竞机理题]]（预测主产物）", "└── 化竞机理题（预测主产物）"),
]
for path, old, new in edits:
    s = io.open(path, encoding="utf-8", newline="").read()
    n = s.count(old)
    assert n >= 1, "未命中: %s: %r" % (path, old)
    s = s.replace(old, new)
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print("正文转纯文本 %d 处: %s" % (n, path))

# 3) 模板 related 去重（保序）
p3 = r"C:\Obsidion\妙妙屋\11-模板\学生讲义模板（v1.2 填充式）.md"
s = io.open(p3, encoding="utf-8", newline="").read()
m = re.match(r"^(---\r?\n)(.*?)(\r?\n---)", s, re.S)
fm = m.group(2)
lines = fm.splitlines()
seen, out, dup = set(), [], []
for ln in lines:
    mm = re.match(r'^\s*-\s*"\[\[(.+?)\]\]"\s*$', ln)
    key = mm.group(1) if mm else ln
    if mm and key in seen:
        dup.append(ln); continue
    if mm: seen.add(key)
    out.append(ln)
if dup:
    eol = "\r\n" if "\r\n" in s else "\n"
    s2 = m.group(1) + eol.join(out) + m.group(3) + s[m.end():]
    io.open(p3, "w", encoding="utf-8", newline="").write(s2)
    print("模板去重 %d 条:" % len(dup))
    for d in dup: print("   -", d.strip())
else:
    print("模板无重复")
