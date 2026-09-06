# -*- coding: utf-8 -*-
"""恢复 化学原理阶段测试卷 的 50 处 used_in（从卷内链接反查）"""
import io, os, re

ROOT = r"C:\Obsidion\妙妙屋\04-题库"
paper = io.open(os.path.join(ROOT, "化学原理阶段测试卷.md"), encoding="utf-8").read()
links = re.findall(r"^### \[\[([^\]]+)\]\]", paper, re.M)
print("原理卷链接数:", len(links))

ok = miss = skip = 0
for name in links:
    name = name.strip()
    target = None
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {"_归档", "_archive_v2",
                       "浙江卷2021", "浙江卷2022", "浙江卷2023"}]
        if name + ".md" in filenames:
            target = os.path.join(dirpath, name + ".md")
            break
    if not target:
        print("!! 未找到:", name); miss += 1; continue
    s = io.open(target, encoding="utf-8", newline="").read()
    if "used_in:" in s:
        skip += 1; continue
    eol = "\r\n" if "\r\n" in s else "\n"
    lines = s.split(eol)
    for i, ln in enumerate(lines):
        if ln.startswith("status:"):
            lines.insert(i + 1, 'used_in: "[[化学原理阶段测试卷]]"')
            break
    else:
        print("!! 无 status 行:", name); miss += 1; continue
    io.open(target, "w", encoding="utf-8", newline="").write(eol.join(lines))
    ok += 1
print(f"恢复 {ok} / 跳过(已有) {skip} / 失败 {miss}")
