# -*- coding: utf-8 -*-
"""逐文件对账：HEAD 版 vs 当前版 的 frontmatter 红链数"""
import sys, re, subprocess
sys.path.insert(0, r"C:\Obsidion\妙妙屋\11-模板\scripts")
from pathlib import Path
import validate_kb as vk

ROOT = vk.VAULT_ROOT
FILES = [
 "04-题库/教材习题/Clayden/题-459-Clayden-Ch28-P5-反应失败分析.md",
 "04-题库/教材习题/无机化学例题与习题/Ch13-硼族元素/习题/Ch13-选择题.md",
 "04-题库/教材习题/无机化学例题与习题/Ch14-碳族元素/习题/Ch14-简答题.md",
 "04-题库/教材习题/无机化学例题与习题/Ch14-碳族元素/习题/Ch14-选择题.md",
 "04-题库/教材习题/无机化学例题与习题/Ch18-氢和稀有气体/例题/例18.3-Xe化合物推断与反应方程式.md",
 "04-题库/教材习题/无机化学例题与习题/Ch20-钛副族和钒副族/习题/20.1-20.10-选择题.md",
 "04-题库/教材习题/无机化学例题与习题/Ch21-铬副族和锰副族/习题/21.1-21.12-选择题.md",
 "04-题库/教材习题/赵鑫光/题-赵鑫光-晶体-习18.md",
 "04-题库/教材习题/赵鑫光/题-赵鑫光-晶体-习32.md",
 "07-资料提炼/习题提炼/习题-结构化学基础-综合习题解析.md",
 "07-资料提炼/书籍提炼/提炼-Clayden-PhaseD-习题拆题清单.md",
 "07-资料提炼/书籍提炼/提炼-Clayden-第24章-区域选择性.md",
 "07-资料提炼/书籍提炼/提炼-Clayden-第25章-烯醇盐的烷基化.md",
 "07-资料提炼/书籍提炼/提炼-Clayden-第2章-有机结构.md",
 "07-资料提炼/书籍提炼/提炼-Clayden-第37章-自由基反应.md",
 "07-资料提炼/书籍提炼/提炼-Clayden-第41章-不对称合成.md",
 "07-资料提炼/书籍提炼/提炼-Clayden-第7章-离域与共轭.md",
 "07-资料提炼/网课资料/Zchem 基础有机化学/资料提炼-Zchem基础有机化学-批次Z-G-综合复习与例题.md",
 "11-模板/学生讲义模板（v1.2 填充式）.md",
]

def count(text):
    fm, _ = vk.parse_frontmatter(text)
    if not isinstance(fm, dict):
        return -1, []
    n, bad = 0, []
    for field in vk.QB_LINK_FIELDS:
        vals = fm.get(field)
        if isinstance(vals, str):
            vals = [vals]
        if not isinstance(vals, list):
            continue
        for v in vals:
            if not isinstance(v, str):
                continue
            for tgt in re.findall(r"(?<!\!)\[\[([^\]|#]+)", v):
                tgt = tgt.strip()
                if not tgt or vk.is_placeholder_target(tgt):
                    continue
                if Path(tgt).suffix.lower() in {".png",".jpg",".jpeg",".gif",".webp",".svg"}:
                    continue
                if vk.find_wikilink_target(tgt, ROOT) is None:
                    n += 1
                    bad.append(f"{field}:{tgt}")
    return n, bad

tot_head = tot_now = 0
for rel in FILES:
    p = ROOT / rel
    head = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=str(ROOT),
                          capture_output=True).stdout.decode("utf-8", "replace")
    now = p.read_text(encoding="utf-8")
    ch, chbad = count(head)
    cn, cnbad = count(now)
    tot_head += max(ch, 0); tot_now += max(cn, 0)
    mark = "  <-- 差异" if ch != cn else ""
    print(f"[HEAD {ch:>2} | NOW {cn:>2}] {rel}{mark}")
    if ch != cn:
        print(f"    HEAD红链: {chbad}")
        print(f"    NOW 红链: {cnbad}")
print(f"\n合计 HEAD {tot_head} -> NOW {tot_now} (Δ {tot_now-tot_head})")
