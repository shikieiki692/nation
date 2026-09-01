# -*- coding: utf-8 -*-
"""
真题子题断链折叠 v7（保守 + 机器验证）

原理：本库真题采用「一题一文件」的题组制，文件名取首个小问描述。
生成器写关联小问时把子题号带了进去（[[题-037-1-2-xxx]]），
但真实文件只有 [[题-037-1-xxx]]，于是产生断链。

已机器验证（父文件内实际小问数 == 链接请求子题数，逐项吻合）：
  036b-1:5/1-1..1-5  036b-2:2/2-1..2-2  036b-3:2  036b-4:3  036b-5:2
  036b-6:3  036b-7-1:6/7-1-1..7-3  036b-8:5  036b-9:4  036b-10:6
  037-8:7/8-7-1~8-7-6   030-6:(295K+315K 同文件)   033-3:(3-2 算 K2 在文件内)
  033-8-1:(Fischer ×11)  038-1:(3 小问,含炼金提纯与 AuCl3 热力学)
  039-1:(1.4.1 彩金 / 1.4.2 硒砂 均在文件内)

安全设计：
  - 只改正文，跳过 frontmatter（frontmatter 断链归另一类，用户已说先不动）
  - 排除 09-审计报告（v2 翻车点）
  - 折叠目标必须真实存在，不存在则跳过留红链
  - 保留原链接显示文本作为别名，避免渲染文本突变
"""
import sys, os, re, json, argparse

VAULT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(VAULT, "11-模板", "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

import validate_kb as V  # noqa: E402

# ── 全库可解析链接目标索引 ──
INDEX = {}
for f in V.iter_link_resolution_files(V.VAULT_ROOT):
    INDEX.setdefault(f.stem, []).append(f.relative_to(V.VAULT_ROOT).as_posix())

with open(os.path.join(VAULT, ".workbuddy", "scripts", "broken_links_v5.json"),
          encoding="utf-8") as fh:
    data = json.load(fh)
targets = data["targets"]

# 畸形前缀修正：题-38届初赛/... → 真题真实目录
MALFORMED = re.compile(r"^题-(\d+)届(初赛|决赛)/")
EXAM_DIR = {}


def build_exam_dir_index():
    base = os.path.join(VAULT, "04-题库", "真题")
    for d in os.listdir(base):
        p = os.path.join(base, d)
        if os.path.isdir(p):
            m = re.match(r"^第(\d+)届(初赛|决赛)", d)
            if m:
                EXAM_DIR[(m.group(1), m.group(2))] = d


build_exam_dir_index()

# 题号形态：题-036b-7-2-1-描述  /  04-题库/真题/.../题-039-1-4-描述
STEM = re.compile(r"^(题-\d+\w*)((?:-\d+)*)(-(.+))?$")


def resolve(t: str):
    """返回 (新链接目标, 说明) 或 (None, 跳过原因)"""
    # 1. 畸形前缀
    m = MALFORMED.match(t)
    rest = t
    prefix = ""
    if m:
        key = (m.group(1), m.group(2))
        if key in EXAM_DIR:
            prefix = "04-题库/真题/" + EXAM_DIR[key] + "/"
        rest = t[m.end():]

    # 2. 拆路径前缀
    if "/" in rest:
        pfx, base = rest.rsplit("/", 1)
        prefix = prefix or (pfx + "/")
    else:
        base = rest

    sm = STEM.match(base)
    if not sm:
        return None, "非题号形态"
    head, nums, _desc = sm.group(1), sm.group(2), sm.group(4)

    # 3. 逐级去掉尾部子号，按【题号前缀】找真实存在的题组文件
    #    注意：题组文件名取首个小问描述，与子题描述不同，故只能按前缀匹配。
    segs = [s for s in nums.split("-") if s]
    if not segs:
        return None, "无子号"
    for drop in range(1, len(segs) + 1):
        keep = segs[:len(segs) - drop]
        cand_head = head + ("-" + "-".join(keep) if keep else "")
        hits = [r for name, rs in INDEX.items()
                if name == cand_head or name.startswith(cand_head + "-")
                for r in rs]
        if not hits:
            continue
        # 路径优先
        chosen = None
        if prefix:
            same = [r for r in hits if r.startswith(prefix)]
            if len(same) == 1:
                chosen = same[0]
        if chosen is None:
            uniq = sorted(set(hits))
            if len(uniq) == 1:
                chosen = uniq[0]
            else:
                return None, f"前缀 {cand_head} 多义: {uniq}"
        chosen = chosen[:-3] if chosen.endswith(".md") else chosen
        return chosen, f"折叠子号 ({'-'.join(segs)} → {'-'.join(keep) or '大题'})"
    return None, "折叠后无对应文件"


# ── 手工特例（已逐条核实上下文）──
MANUAL = {
    "SN2Ar": ("SNAr", "07-资料提炼 第28届解析中「SN2Ar、硝基活化效应」= 芳香亲核取代 → SNAr"),
}

plan = {}
skipped = {}
for t, d in targets.items():
    if t in MANUAL:
        plan[t] = (MANUAL[t][0], MANUAL[t][1])
        continue
    new, why = resolve(t)
    if new:
        plan[t] = (new, why)
    else:
        skipped[t] = why

print(f"可折叠 {len(plan)} 条 / 跳过 {len(skipped)} 条\n")
for t, (new, why) in sorted(plan.items()):
    print(f"  ✔ {t}")
    print(f"     → {new}   [{why}]")
print("\n跳过（保留红链）：")
for t, why in sorted(skipped.items()):
    print(f"  · {t}  [{why}]")

if "--apply" not in sys.argv:
    print("\n[dry-run] 加 --apply 才写入")
    sys.exit(0)

# ── 应用 ──
FMBOUND = re.compile(r"^---\s*$", re.M)
changed = {}
for t, (new, _why) in plan.items():
    pat = re.compile(r"\[\[" + re.escape(t) + r"(\\?\|[^\]]*)?\]\]")
    for src in targets[t]["src"]:
        rel = src
        if rel.startswith("09-审计报告"):
            continue
        p = os.path.join(VAULT, rel.replace("/", os.sep))
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8", newline="") as fh:
            raw = fh.read()
        # 只改正文：仅当首行 --- 且头部含 YAML 键时才认定为 frontmatter
        # （正文里的 --- 水平分隔线不参与，避免越界改到正文开头）
        split = 0
        if raw.startswith("---"):
            m2 = FMBOUND.search(raw, 3)
            if m2 and re.search(r"^[\w\-]+:", raw[:m2.start()], re.M):
                split = m2.end()
        head, body = raw[:split], raw[split:]

        def rep(mo):
            alias = mo.group(1)
            if alias:
                return "[[" + new + alias + "]]"
            # 原链接无别名时，补一个「短别名」= 原目标末段（去掉路径），
            # 避免把整条路径当显示文本（Dalton分压定律踩过）
            short = t.rsplit("/", 1)[-1]
            return "[[" + new + "|" + short + "]]"

        nb, n = pat.subn(rep, body)
        if n:
            body = nb
            with open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(head + body)
            changed.setdefault(rel, []).append((t, new, n))

print(f"\n已改 {len(changed)} 个文件：")
tot = 0
for rel, items in sorted(changed.items()):
    s = sum(i[2] for i in items)
    tot += s
    print(f"  {rel}  ({s} 处)")
print(f"合计替换 {tot} 处")
json.dump(changed, open(os.path.join(VAULT, ".workbuddy", "scripts",
                                     "fix_exam_v7_applied.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=1)
