#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""validate_handout.py — 讲义线第三道闸门（基建战 A4）
依据《11-模板/讲义练习区格式规范.md v1.0》校验 04-课件/学生讲义/ 下的 md。

用法：
  python validate_handout.py --changed <文件…>   # 与 validate_kb.py 同接口
  python validate_handout.py --all               # 全量扫描学生讲义目录

分级：ERROR（阻断，exit 1）/ WARNING（登记不阻断）/ INFO。
铁律：扫描文件数为 0 时直接 FAIL（防静默失效）；输出受检文件数。
"""
import os, re, sys, json, argparse

# 从脚本位置逐级向上找 vault（含 04-课件 的目录），防移位后层级变化
_here = os.path.dirname(os.path.abspath(__file__))
VAULT = _here
for _ in range(6):
    if os.path.isdir(os.path.join(VAULT, "04-课件", "学生讲义")):
        break
    VAULT = os.path.dirname(VAULT)
else:
    VAULT = os.path.dirname(os.path.dirname(os.path.dirname(_here)))
ROOT = os.path.join(VAULT, "04-课件", "学生讲义")

REQUIRED_FM = ["title", "type", "chapter", "serve_rounds", "stage",
               "difficulty_level", "has_images"]  # exercise_count 单独按「有练习题」条件查（规范 §五）
EX_HEAD_WHITELIST = ("综合串联题",)  # 节名变体白名单
# 装饰性 emoji（排除 ✓✗≈ 等文本功能符号；⭐ 单列铁律项）
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF\u2B00-\u2BFF\u2728\u274C\u2757\U0001F900-\U0001F9FF]")
# 合法题目/答案行：**N.** 题干 或 **N. [标签] 题名**
PAT_ITEM = re.compile(r"^\*\*(\d{1,2})\.\*\*[ \t]*", re.A)
PAT_ITEM_T = re.compile(r"^\*\*(\d{1,2})\.[ \t]+\[.*\][ \t]*\S.*\*\*[ \t]*", re.A)  # **26. [届次] 题名**
PAT_BARE = re.compile(r"^(\d{1,2})\.[ \t]+", re.A)

# 考纲注册表（教学价值战 B1）：`02-考纲条目/` FM syllabus_code 的固化快照
SYL_PATH = os.path.join(os.path.dirname(_here), "data", "syllabus_registry.json")

def load_syllabus_labels():
    """返回注册表 label 集合（§NN 名 / 决赛NN 名）；缺失时返回 None（降级跳过码校验）"""
    try:
        reg = json.load(open(SYL_PATH, encoding="utf-8"))
    except Exception:
        return None
    labels = set()
    for r in reg:
        code = str(r["code"])
        title = r["title"]
        if r["stage"] == "决赛":
            m_ = re.search(r"决赛(\d+)", title)
            name = re.sub(r"^决赛\d+-", "", title)
            labels.add(f"决赛{int(m_.group(1)):02d} {name}")
        elif code.isdigit():
            name = re.sub(r"^\d+-", "", title)
            labels.add(f"§{int(code):02d} {name}")
    return labels


SYLLABUS_LABELS = load_syllabus_labels()


def fm_of(text):
    m = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n", text, re.S)
    return m.group(1) if m else None


def fm_get(fm, key):
    m = re.search(rf"(?m)^\s*{key}:\s*(.+?)[ \t]*\r?$", fm)
    return m.group(1).strip() if m else None


def zones_of(lines):
    """返回 [(start, end, kind)]，kind ∈ ex/ans/None；### 内嵌答案并入 ex 的 ans 子区起点。"""
    zs, cur, cs = [], None, None
    for i, L in enumerate(lines):
        m = re.match(r"^##[ \t]+(.+?)[ \t]*\r?\n?$", L)
        if m:
            if cur is not None:
                zs.append((cs, i, cur))
            name = m.group(1)
            is_ex = ("练习" in name or any(w in name for w in EX_HEAD_WHITELIST)) and "答案" not in name
            cur = "ex" if is_ex else ("ans" if "答案" in name else None)
            cs = i
    if cur is not None:
        zs.append((cs, len(lines), cur))
    return zs


def check(rel):
    """返回 (errors, warnings, infos) 三列表[str]"""
    E, W, I = [], [], []
    p = os.path.join(ROOT, rel)
    with open(p, encoding="utf-8", errors="replace") as f:
        text = f.read()
    lines = text.splitlines(keepends=True)
    fm = fm_of(text)
    if fm is None:
        E.append("无 frontmatter")
        return E, W, I
    is_index = os.path.basename(rel).startswith("README")
    if is_index:
        # 索引/说明页形态自由：只要求有 FM，不做必填字段与配平检查
        return E, W, I
    for k in REQUIRED_FM:
        if fm_get(fm, k) is None:
            if k == "chapter":
                # chapter=讲次路由字段，缺值需对照课程计划人工定，降 WARNING 登记待补
                W.append("FM 缺 chapter（待人工对照课程计划补值）")
            else:
                E.append(f"FM 缺 {k}")

    zs = zones_of(lines)
    zone_kind = [None] * len(lines)
    for s, e, k in zs:
        for i in range(s, e):
            zone_kind[i] = k
    # 内嵌答案子区（ex 内 ###…答案… 标题之后）
    emb_start = None
    for i, L in enumerate(lines):
        if zone_kind[i] == "ex" and re.match(r"^#{3,4}[ \t]+[^\n]*答案", L):
            emb_start = i
            break

    # 1 编号格式：题目区（ex 非内嵌答案部分）+ 答案区（ans 或 ex 内嵌）
    q_nums, a_nums = [], []
    for i, L in enumerate(lines):
        zk = zone_kind[i]
        if zk is None:
            continue
        body = L.rstrip("\r\n")
        in_q = (zk == "ex") and not (emb_start is not None and i >= emb_start)
        in_a = (zk == "ans") or ((zk == "ex") and emb_start is not None and i >= emb_start)
        if PAT_ITEM.match(body) or PAT_ITEM_T.match(body):
            n = int(re.match(r"^\*\*(\d{1,2})\.", body).group(1))
            (q_nums if in_q else a_nums).append(n)
        elif PAT_BARE.match(body) and (in_q or in_a):
            # 裸编号行可能是题内小问/步骤/要点列表（规范定义「不是题目」），降级 WARNING 人工复核
            W.append(f"L{i+1} 裸编号行（若为题目请加粗）：{body[:40]}…")
    # 2 题号连续
    if q_nums:
        s_ = sorted(set(q_nums))
        miss = [x for x in range(1, max(s_) + 1) if x not in s_]
        if miss:
            E.append(f"题号不连续，缺 {miss}")
    # 3 配平
    if q_nums and a_nums and len(set(q_nums)) != len(set(a_nums)):
        E.append(f"练习 {len(set(q_nums))} 题 ≠ 答案 {len(set(a_nums))} 条")
    if q_nums and not a_nums:
        W.append(f"有 {len(set(q_nums))} 题无答案区（登记待补清单）")
    # 4 FM 题数口径（纯练习数）
    fm_ex = fm_get(fm, "exercise_count")
    if q_nums:
        try:
            if fm_ex is None:
                E.append("有练习题但 FM 缺 exercise_count")
            elif int(fm_ex) != len(set(q_nums)):
                E.append(f"exercise_count={fm_ex} ≠ 正文纯练习数 {len(set(q_nums))}")
        except ValueError:
            E.append(f"exercise_count 非整数：{fm_ex}")
    # 5 图片配平
    imgs = re.findall(r"!\[\[([^\]]+)\]\]", text)
    has_img = (fm_get(fm, "has_images") or "").lower()
    fm_ic = fm_get(fm, "image_count")
    if has_img == "true" and not imgs:
        E.append("has_images=true 但正文无图")
    if has_img == "false" and imgs:
        E.append(f"has_images=false 但正文有 {len(imgs)} 图")
    if fm_ic and fm_ic.isdigit() and int(fm_ic) != len(imgs):
        E.append(f"image_count={fm_ic} ≠ 实际 {len(imgs)} 图")
    # 6 emoji（全正文）
    for i, L in enumerate(lines):
        if EMOJI.search(L):
            W.append(f"L{i+1} 含装饰性 emoji：{L.strip()[:30]}")
            break  # 每文件只报首处
    # 7 ⭐ 残留（铁律：在役清零）
    if "⭐" in text:
        E.append("⭐ 难度标记残留")
    # 8 学习目标考纲对齐（教学价值战 B1）：LO 节须含「> 对齐考纲：」且码在注册表
    m_lo = re.search(r"^##[ \t]+学习目标.*?[ \t]*\r?$", text, re.M)
    if m_lo:
        seg = text[m_lo.end():]
        nxt = re.search(r"^##[ \t]+", seg, re.M)
        seg = seg[:nxt.start()] if nxt else seg
        bq = re.search(r"^>[ \t]*对齐考纲：(.+?)[ \t]*\r?$", seg, re.M)
        if not bq:
            W.append("LO 节缺「> 对齐考纲：」blockquote（未锚定考纲）")
        elif SYLLABUS_LABELS is not None:
            codes = [c.strip() for c in re.split(r"[·;；]", bq.group(1)) if c.strip()]
            bad = [c for c in codes if c not in SYLLABUS_LABELS]
            if bad:
                E.append(f"LO 锚点码不在注册表: {bad}")
            else:
                I.append(f"LO对齐{len(codes)}码")
        else:
            I.append("LO对齐(注册表缺失,码未校验)")
    I.append(f"练习节×{sum(1 for _,_,k in zs if k=='ex')} 答案节×{sum(1 for _,_,k in zs if k=='ans')} 题{len(set(q_nums))}/答{len(set(a_nums))} 图{len(imgs)}")
    return E, W, I


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--changed", nargs="*", default=[])
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    if args.all:
        rels = []
        for dp, dn, fns in os.walk(ROOT):
            if "_归档" in dp:
                dn[:] = []
                continue
            for fn in fns:
                if fn.endswith(".md"):
                    rels.append(os.path.relpath(os.path.join(dp, fn), ROOT).replace("\\", "/"))
    else:
        rels = [os.path.relpath(x, ROOT).replace("\\", "/") for x in args.changed
                if os.path.abspath(x).startswith(os.path.abspath(ROOT)) and x.endswith(".md")]

    print(f"🔍 validate_handout 开始（受检 {len(rels)} 文件）...")
    if not rels:
        print("🔴 FAIL：受检文件数为 0（防静默失效）")
        sys.exit(1)

    nE = nW = 0
    for rel in sorted(rels):
        E, W, I = check(rel)
        nE += len(E); nW += len(W)
        tag = "✅" if not E else "🔴"
        print(f"  {tag} {rel}  {'; '.join(I)}")
        for x in E:
            print(f"      🔴 {x}")
        for x in W:
            print(f"      🟡 {x}")
    print(f"\n📊 结果: 受检 {len(rels)} | 🔴 Error {nE} | 🟡 Warning {nW}")
    sys.exit(1 if nE else 0)


if __name__ == "__main__":
    main()
