# -*- coding: utf-8 -*-
r"""非有机 5 栏目讲义「完整合规复检」——一脚本出全量基线 + 缺陷明细。

用法：
    python -X utf8 11-模板/scripts/qa/audit_nonorganic.py                # 全量
    python -X utf8 11-模板/scripts/qa/audit_nonorganic.py --section 3-物理化学
    python -X utf8 11-模板/scripts/qa/audit_nonorganic.py --csv 09-审计报告/xxx.csv

判据分 7 类（口径 v4 + 2026-09-30 图版式 + docx 工程）：
    A 结构    无 H1 / `## §1`~`§N` 连续 / 无「学习目标」/ 无「目录」/ 有 `## §N 课后习题`
    B 图版式  正文区独立图行 = 0 / 限宽数 = 图数 / 图注编号连续 / 图注在表内（表外 = 缺陷）
    C 标题层级 H4 是否成体系（`#### N.M.K` 有编号为可接受；`#### (1) xxx` / `#### 无编号` 记缺陷）
    D 并段    A 类＝`**加粗小标题**` 紧邻正文行；B 类＝两普通正文行紧邻；标题前缺空行
    E 双轨    学生版存在 / 零答案泄漏 / FM image_count 与实图数一致
    F 溯源    图片物理文件存在（断链 = 0）
    G 内容    `>600 字`正文段 / 四要素速查表有无

⚠️ 全程 utf-8-sig 读（BOM 会让 \A--- 的 FM 正则失配）。
⚠️ 判据 B/C/D 为**候选池**：B 类并段需语义甄别（并列项该拆、同段续行不该拆）。
"""
import argparse
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(r"C:\Obsidion\妙妙屋")
BASE = ROOT / "04-课件/学生讲义"
MEDIA = ROOT / "媒体仓库"
SECTIONS = ["1-化学基础知识", "2-结构化学", "3-物理化学", "4-分析化学", "5-无机化学"]

FM_RE = re.compile(r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*\r?\n", re.S)
IMG = re.compile(r"!\[\[([^\]]+?)\]\]")
BOLD_HEAD = re.compile(r"^\*\*[^*]{2,40}\*\*[：:]?")
LISTY = re.compile(r"^(?:[ \t]*[-*+] |[ \t]*\d+[.、]|[ \t]*（?\d+）|[|>$!#]|---)")
BLOCK = ("|", ">", "$", "!", "#", "---")
ANS_LEAK = re.compile(r"(?m)^\*\*解[ \t]*\d{1,2}\*\*")
ANS_HEAD = re.compile(r"(?m)^#{2,4} *参考答案")


def split_fm(raw):
    m = FM_RE.match(raw)
    fm = m.group(0) if m else ""
    return fm, raw[len(fm):]


def fm_int(fm, key):
    m = re.search(r"(?m)^%s:\s*(\d+)" % key, fm)
    return int(m.group(1)) if m else None


def audit_one(sec, p):
    name = p.name.replace("-超级充实版（自学完整）.md", "")
    raw = p.read_text(encoding="utf-8-sig")
    fm, body = split_fm(raw)
    L = body.split("\n")
    ax = next((i for i, l in enumerate(L) if l.startswith("## §") and "课后习题" in l), len(L))
    r = {"section": sec, "name": name}

    # A 结构
    secs = [int(x) for x in re.findall(r"(?m)^## §(\d+)", body)]
    r["n_sec"] = len(secs)
    r["sec_ok"] = bool(secs) and secs == list(range(1, len(secs) + 1))
    r["h1"] = len(re.findall(r"(?m)^# ", body))
    r["learn"] = len(re.findall(r"(?m)^#+ *学习目标", body))
    r["toc"] = len(re.findall(r"(?m)^## *目录\s*$", body))
    r["ex_head"] = len(re.findall(r"(?m)^## §\d+ *课后习题", body))

    # B 图版式
    hs = re.findall(r"!\[\[([^\]|]+?)\.(jpg|png)", body)
    r["n_img"] = len(IMG.findall(body))
    r["limited"] = len(re.findall(re.escape("\\") + r"\|[0-9]+\]\]", body))
    r["solo"] = sum(1 for i, l in enumerate(L) if i < ax and l.startswith("![["))
    caps = [int(x) for x in re.findall(r"[>|]\s*图 \d+-(\d+)[： 　]", raw)]
    # 无图/无图注的讲义不作「跳号」判定
    r["cap_ok"] = (not caps) or caps == list(range(1, len(caps) + 1))
    r["n_cap"] = len(caps)
    # 图注在表外：只算 `> 图 N-M：`（带冒号的独立行，属正文区插图漏包装）；
    # `| 图 N-M 标签 |` 是例题/习题题面图样式，合法，不计。
    r["cap_outside"] = [i + 1 for i, l in enumerate(L) if i < ax and re.match(r"^> 图 \d+-\d+：", l)]
    r["broken"] = [f"{h}.{e}" for h, e in hs if not (MEDIA / f"{h}.{e}").exists()]

    # C 标题层级
    h4 = [l for l in L if l.startswith("#### ")]
    r["h4"] = len(h4)
    r["h4_bad"] = sum(1 for l in h4 if not re.match(r"^#### +\d+(?:\.\d+)+ ", l))

    # D 并段
    a = b = head_adj = 0
    for i in range(1, len(L)):
        cur, prev = L[i], L[i - 1]
        if cur.startswith("#") and prev.strip():
            head_adj += 1
        if not cur.strip() or not prev.strip():
            continue
        if cur.startswith(BLOCK) or prev.startswith(BLOCK):
            continue
        if BOLD_HEAD.match(cur.strip()) or BOLD_HEAD.match(prev.strip()):
            a += 1
        elif not LISTY.match(cur) and not LISTY.match(prev):
            b += 1
    r["adj_a"], r["adj_b"], r["head_adj"] = a, b, head_adj

    # E 双轨
    sp = BASE / "学生专用版" / sec / (name + "-超级充实版（学生专用版）.md")
    r["has_sp"] = sp.exists()
    r["leak"] = None
    r["sp_img"] = None
    if sp.exists():
        sfm, sbody = split_fm(sp.read_text(encoding="utf-8-sig"))
        r["leak"] = len(ANS_LEAK.findall(sbody)) + len(ANS_HEAD.findall(sbody))
        r["sp_img"] = fm_int(sfm, "image_count")
    r["fm_img"] = fm_int(fm, "image_count")
    r["fk"] = fm_int(fm, "exercise_count")

    # G 内容
    r["b600"] = sum(1 for i in range(ax) if len(L[i].strip()) > 600 and not L[i].startswith("|"))
    r["sp_tab"] = ("物质速查" in body) or ("速查（" in body) or ("信号速查" in body)
    return r


def verdict(r):
    f = []
    if r["h1"]:
        f.append(f"H1×{r['h1']}")
    if not r["sec_ok"]:
        f.append("§N不连续/缺失")
    if r["learn"]:
        f.append("学习目标")
    if r["toc"]:
        f.append("目录节")
    if r["n_sec"] and not r["ex_head"]:
        f.append("无课后习题节")
    if r["solo"]:
        f.append(f"独立图行×{r['solo']}")
    if r["n_img"] and r["limited"] < r["n_img"]:
        f.append(f"限宽{r['limited']}/{r['n_img']}")
    if r["n_cap"] and not r["cap_ok"]:
        f.append("图注跳号")
    if r["cap_outside"]:
        f.append(f"图注在表外×{len(r['cap_outside'])}")
    if r["h4_bad"]:
        f.append(f"非规范H4×{r['h4_bad']}")
    if r["head_adj"]:
        f.append(f"标题缺空行×{r['head_adj']}")
    if r["broken"]:
        f.append(f"断链×{len(r['broken'])}")
    if not r["has_sp"]:
        f.append("缺学生版")
    if r["leak"]:
        f.append(f"答案泄漏×{r['leak']}")
    # 两轨图数：学生版删答案区图属预期，故只报异常（学生版 > 母版）
    if r["sp_img"] is not None and r["fm_img"] is not None and r["sp_img"] > r["fm_img"]:
        f.append("学生版图数>母版")
    if r["fm_img"] is not None and r["fm_img"] != r["n_img"]:
        f.append(f"FM图{r['fm_img']}≠{r['n_img']}")
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", default=None)
    ap.add_argument("--csv", default=None)
    args = ap.parse_args()

    rows, details = [], []
    print(f"{'栏目':<12}{'讲名':<22}{'§':>3}{'图':>4}{'注':>4}{'H4':>4}{'坏H4':>5}{'A并':>4}{'B并':>5}{'头缺':>4}  判定")
    print("-" * 104)
    for sec in SECTIONS:
        if args.section and sec != args.section:
            continue
        for p in sorted((BASE / sec).glob("*超级充实版（自学完整）.md")):
            r = audit_one(sec, p)
            rows.append(r)
            f = verdict(r)
            for x in f:
                details.append((sec, r["name"], x, r))
            mark = "✅" if not f else "🔴 " + " / ".join(f)
            print(f"{sec[:10]:<12}{r['name'][:20]:<22}{r['n_sec']:>3}{r['n_img']:>4}{r['n_cap']:>4}"
                  f"{r['h4']:>4}{r['h4_bad']:>5}{r['adj_a']:>4}{r['adj_b']:>5}{r['head_adj']:>4}  {mark}")
    print("-" * 104)

    ok = sum(1 for r in rows if not verdict(r))
    print(f"结构层达标：{ok}/{len(rows)}")
    print(f"并段候选：A 类 {sum(r['adj_a'] for r in rows)} 处 ｜ B 类 {sum(r['adj_b'] for r in rows)} 处"
          f"（B 类需语义甄别：并列项该拆、同段续行不该拆）")
    print(f"H4 总数 {sum(r['h4'] for r in rows)}，其中非规范（无编号/`(1)`式）{sum(r['h4_bad'] for r in rows)}")
    print(f"断链 {sum(len(r['broken']) for r in rows)} ｜ 图注在表外 {sum(len(r['cap_outside']) for r in rows)} 处"
          f" ｜ 标题缺空行 {sum(r['head_adj'] for r in rows)} 处")

    if details:
        print("\n===== 缺陷明细（A/B/C/D/E/F 类，非并段候选）=====")
        for sec, name, x, r in details:
            extra = ""
            if "图注在表外" in x:
                extra = " 行号 " + ",".join(map(str, r["cap_outside"]))
            if "断链" in x:
                extra = " " + ", ".join(r["broken"][:3])
            print(f"  [{sec}] {name}  →  {x}{extra}")

    if args.csv:
        out = pathlib.Path(args.csv)
        keys = list(rows[0].keys())
        with out.open("w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            for r in rows:
                w.writerow({k: (",".join(map(str, v)) if isinstance(v, list) else v) for k, v in r.items()})
        print(f"\nCSV → {out}")


if __name__ == "__main__":
    sys.exit(main())
