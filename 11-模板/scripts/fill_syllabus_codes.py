# -*- coding: utf-8 -*-
"""
习题书待补 syllabus_codes 批量补码（2026-09-01）

背景：质量审计 30 题命中『考纲无关』但实为 syllabus_codes 缺失（内容属考纲范围）。
码表来源：02-考纲条目 frontmatter `syllabus_code`（基础要求 1-56）。
映射规则（按路径/主题人工裁决，宁窄勿滥）：
  分析化学（容量/滴定）            -> 18 容量分析
  无机例题与习题 Ch13-17,19,22     -> 13 元素化学
  Weller Ch19（纳米金）            -> 13 元素化学
  Weller Ch20（基谱项/T-S 图）     -> 12 配合物
  ZOC-022（金属有机试剂）          -> 51 金属有机
  ZOC-023（烯醇互变异构+NMR证据）  -> 25 互变异构体 + 30 有机波谱分析
  ZOC-046 / ZOC-050（Wittig/HWE）  -> 48 膦化合物
  XES-040（Michael 加成）          -> 46 羰基α位反应

用法：python fill_syllabus_codes.py [--write]
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = r"C:\Obsidion\妙妙屋"
LIST_MD = os.path.join(BASE, r"07-资料提炼\习题书-待补syllabus元数据清单.md")
WRITE = "--write" in sys.argv


def parse_targets():
    """从清单 md 提取 30 个相对路径"""
    targets = []
    for line in io.open(LIST_MD, encoding="utf-8"):
        m = re.match(r"^- \[[^\]]+\] (.+?\.md)", line.strip())
        if m:
            targets.append(m.group(1).replace("（难度", "").strip())
    return targets


def resolve(rel):
    p = os.path.join(BASE, "04-题库", rel)
    return p if os.path.exists(p) else None


def map_codes(rel):
    """返回 (codes, 依据说明)；无法判定返回 None"""
    if "分析化学/容量分析与酸碱滴定" in rel or "分析化学/氧化还原与沉淀滴定" in rel:
        return ["18"], "容量分析（酸碱/氧化还原/沉淀滴定）"
    if "无机化学例题与习题/Ch13-" in rel or "无机化学例题与习题/Ch14-" in rel or \
       "无机化学例题与习题/Ch15-" in rel or "无机化学例题与习题/Ch16-" in rel or \
       "无机化学例题与习题/Ch17-" in rel or "无机化学例题与习题/Ch19-" in rel or \
       "无机化学例题与习题/Ch22-" in rel:
        return ["13"], "元素化学（主族/副族元素性质）"
    if "Weller/Ch19/" in rel:
        return ["13"], "元素化学（金）"
    if "Weller/Ch20/" in rel:
        return ["12"], "配合物（配位场理论/基谱项）"
    if "题-ZOC-022-" in rel:
        return ["51"], "金属有机"
    if "题-ZOC-023-" in rel:
        return ["25", "30"], "互变异构体 + 有机波谱分析"
    if "题-ZOC-046-" in rel or "题-ZOC-050-" in rel:
        return ["48"], "膦化合物（Wittig/HWE 烯基化）"
    if "题-XES-040-" in rel:
        return ["46"], "羰基α位反应（Michael 加成）"
    return None


def has_codes(text):
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        return True  # 无 frontmatter，跳过不动
    return re.search(r"(?m)^syllabus_codes:", fm.group(1)) is not None


def insert_field(text, codes):
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    body = text[fm.end():]
    y = fm.group(1)
    val = "[" + ", ".join(codes) + "]"
    line = f"syllabus_codes: {val}"
    # 插到 tags: 行之前（稳定锚点）；无 tags 则追加到 frontmatter 末尾
    if re.search(r"(?m)^tags:", y):
        y2 = re.sub(r"(?m)^(tags:.*)$", line + "\n\\1", y, count=1)
    else:
        y2 = y.rstrip("\n") + "\n" + line + "\n"
    return "---\n" + y2 + "\n---\n" + body


def main():
    targets = parse_targets()
    print(f"清单目标 {len(targets)} 条")
    ok = skip = fail = 0
    for rel in targets:
        p = resolve(rel)
        if not p:
            print(f"  ✗ 文件不存在: {rel}")
            fail += 1
            continue
        text = io.open(p, encoding="utf-8").read()
        if has_codes(text):
            print(f"  = 已有 syllabus_codes，跳过: {rel}")
            skip += 1
            continue
        mc = map_codes(rel)
        if not mc:
            print(f"  ? 无映射规则: {rel}")
            fail += 1
            continue
        codes, why = mc
        if not WRITE:
            print(f"  [dry-run] {rel} -> {codes}（{why}）")
            ok += 1
            continue
        new = insert_field(text, codes)
        io.open(p, "w", encoding="utf-8", newline="").write(new)
        print(f"  ✅ {rel} -> {codes}（{why}）")
        ok += 1
    print(f"\n补码 {ok}，跳过 {skip}，失败 {fail}（{'实写' if WRITE else 'dry-run'}）")


if __name__ == "__main__":
    main()
