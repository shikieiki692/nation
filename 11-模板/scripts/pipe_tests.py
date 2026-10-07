#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""管线回归测试基座（2026-10-07 建）。

存在的理由：今天在「脚本能跑但判据没测」上栽了 11 次（FM 数组形态、字段边界、
索引范围、语义判据……）。**脚本能跑 ≠ 判据正确**。本文件把各管线用到的
判据全部固化成可复跑的断言，改管线后先跑这里。

用法：
    python 11-模板/scripts/pipe_tests.py            # 全部
    python 11-模板/scripts/pipe_tests.py fm         # 只跑名字含 fm 的
退出码 0 = 全通过；1 = 有失败。
"""
import os
import re
import sys
import json
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import fm_parse as fp  # noqa: E402

CASES = []          # (组名, 用例名, 断言函数)


def case(group):
    def deco(fn):
        CASES.append((group, fn.__name__, fn))
        return fn
    return deco


# ══════════════════════════════════════════════════════════════
# 1. fm_parse：FM 数组的六种书写形态 + 字段边界
# ══════════════════════════════════════════════════════════════
@case("fm_parse")
def fm_三种取值形态():
    """同行数组 / 块列表 / 跨行数组 / 标量 / 空值 —— 每种都要能取对"""
    assert fp.get_list_field('k: ["[[A]]", "[[B]]"]', "k") == ["[[A]]", "[[B]]"]
    assert fp.get_list_field('k:\n  - "[[A]]"\n  - "[[B]]"', "k") == ["[[A]]", "[[B]]"]
    assert fp.get_list_field('k: ["[[A]]",\n  "[[B]]"]', "k") == ["[[A]]", "[[B]]"]
    assert fp.get_list_field('k: "[[A]]"', "k") == ["[[A]]"]      # 标量有值
    assert fp.get_list_field('k: 蒸气压', "k") == ["蒸气压"]
    assert fp.get_list_field('k: []', "k") == []
    assert fp.get_list_field('k:', "k") == []
    assert fp.get_list_field('k: [(空)]', "k") == []


@case("fm_parse")
def fm_块列表不吞后续字段():
    """块列表后接别的字段，不能把下一字段的项也吃进来"""
    txt = 'k:\n  - "[[A]]"\nsource: x\n  - "[[B]]"'
    assert fp.get_list_field(txt, "k") == ["[[A]]"]


@case("fm_parse")
def fm_wikilink不被截断():
    """回归：非贪婪 \\[.*?\\] 会截到 wikilink 自带的第一个 ] —— 这是今天踩过的坑"""
    got = fp.get_list_field('k: ["[[很长的考点名]]", "[[另一个]]"]', "k")
    assert got == ["[[很长的考点名]]", "[[另一个]]"], got
    assert fp.get_wikilinks_field('k: ["[[A]]", "[[B]]"]', "k") == ["A", "B"]


@case("fm_parse")
def fm_键存在性只认键名():
    """判「键在不在」与值怎么写无关（同行/跨行/块列表/标量都算在）"""
    for txt in ['knowledge_points: ["[[A]]"]',
                'knowledge_points: ["[[A]]",\n  "[[B]]"]',
                'knowledge_points:\n  - "[[A]]"',
                'knowledge_points: "[[A]]"']:
        assert fp.has_key(txt, "knowledge_points"), txt
    assert not fp.has_key('knowledge_points_x: ["[[A]]"]', "knowledge_points")


@case("fm_parse")
def fm_取值限定字段边界():
    """回归：不能对整段 frontmatter 抓 wikilink（source_file/cross_references 会被误算）"""
    txt = ('source_file: "[[04-题库/某卷]]"\n'
           'cross_references: ["[[另一张卡]]"]\n'
           'knowledge_points: ["[[真考点]]"]')
    assert fp.get_wikilinks_field(txt, "knowledge_points") == ["真考点"]


@case("fm_parse")
def fm_split还原正文():
    txt = '---\ntitle: t\n---\n\n# 正文\n内容\n'
    fmx, body = fp.split_fm(txt)
    assert "title: t" in fmx and "# 正文" in body
    # 无 frontmatter 时不炸
    fmx2, body2 = fp.split_fm("# 只有正文\n")
    assert fmx2 == "" and "只有正文" in body2


# ══════════════════════════════════════════════════════════════
# 2. 答案区识别（异形标题 / details / 外链型）—— 2026-10-07 并入 fm_parse
# ══════════════════════════════════════════════════════════════
@case("答案区")
def 答案区识别四形态():
    CASES = [
        ("## 参考答案\n答案是 B", "标准", True, False),
        ("## 答案\nB", "异形标题", True, False),
        ("## 解答\n因为……", "异形标题", True, False),
        ("## 解析要点\n关键在于氧化性更强。", "异形标题", True, False),
        ("## 答案与解析\nB", "标准", True, False),
        ("**答案：** B", "加粗标记", True, False),
        ("<details><summary>查看答案</summary>\n**答案：C**\n</details>", "details", True, False),
        ("## 参考答案\n> 本题答案见 [[卷-01]] 的 `## 参考答案` 区。\n> 卷内锚表标识题号：1。",
         "标准", False, True),
        ("## 题目\n只有题面", None, False, False),
    ]
    for body, kind, ent, ext in CASES:
        info = fp.classify_answer(body)
        assert info["kind"] == kind, "kind：%s（期望 %s）" % (info["kind"], kind)
        assert info["has_entity"] == ent, "has_entity：%s（期望 %s）｜%s" % (info["has_entity"], ent, body[:30])
        assert info["ext_ref"] == ext, "ext_ref：%s（期望 %s）" % (info["ext_ref"], ext)


@case("答案区")
def 答案区短答案不算缺():
    """回归：不能用字数阈值判「有实体答案」——'答案是 B' 只有 4 字。
    记忆里早已记着「短答案≠无答案」（如 '有;无;有' / 单结论分子式）。"""
    for body in ("## 参考答案\nB", "## 参考答案\n有;无;有", "## 答案\nCuSO4"):
        info = fp.classify_answer(body)
        assert info["has_entity"], "短答案被误判为无实体：%r" % body


@case("答案区")
def 答案区details优先于加粗标记():
    """回归：多数折叠块内部就有 `**答案：**`，先匹配标记会把整块答案截成一行。"""
    body = "<details><summary>查看答案与解析</summary>\n**8-1** 化学式：MX。\n\n**8-2** 配位数：4。\n</details>"
    s, e, kind = fp.find_answer_section(body)
    assert kind == "details", kind
    got = fp.answer_text(body)
    assert "配位数" in got, got
    assert len(got) > 40, "details 内容被截短：%s" % got[:60]


@case("答案区")
def 外链型答案不被当成实体答案():
    """577 张外链型卡：答案区只写指针，摘要须标注而非截原文。"""
    body = "## 参考答案\n> 本题答案见 [[卷-01-第1章-A卷-化学反应速率与化学平衡]] 的 `## 参考答案` 区。\n> 卷内锚表标识题号：1。"
    txt = fp.answer_text(body)
    assert "[[" not in txt, txt
    assert "答案见卷册" in txt, txt


@case("答案区")
def 答案区段边界只认同级或更高级标题():
    """🔴 回归（2026-10-07 真实缺陷，A 层标注时踩到）：

    段边界原先用「下一个**任意**标题」作结束，但答案区里**紧跟子标题**是常态
    （`## 参考答案` → `### (1) …`），于是段长被截成 0 ⇒ `has_entity=False`
    ⇒ **21 张本来有答案的卡被误判为「答案区空」**，差点被错标「源确缺」。

    正解：区界是「level ≤ 本级」的标题；`###`/`####` 是答案区的子结构，要并入。
    """
    CASES = [
        ("## 参考答案\n\n### (1) 子问\n\nEndo 产物为主。\n", True),
        ("## 参考答案\n\n#### 答\n\n分子量 128 g/mol。\n", True),
        ("## 解答\n\n### 第一问\n\n因为稳定性顺序…\n", True),
        # 下面三个必须仍判 False / 原行为不变
        ("## 参考答案\n\n## 知识点映射\n\n- x\n", False),        # 真空答案区
        ("## 参考答案\n> 见 [[卷-01]] 的参考答案区。\n", False),        # 外链型
    ]
    for body, want in CASES:
        info = fp.classify_answer(body)
        assert info["has_entity"] == want, "has_entity=%s（期望 %s）｜%r" % (info["has_entity"], want, body[:40])
    # 区界长度：答案区必须真的取到内容
    s, e, k = fp.find_answer_section("## 参考答案\n\n### (1) 子问\n\nEndo 产物为主。\n")
    assert e - s > 20, "答案区段长 %d 仍被截断" % (e - s)


@case("答案区")
def 只有标注块不算有答案():
    """🔴 回归（2026-10-07 第七形态，final_stats 时发现 207 张受影响）：

    答案区**只有 callout 标注块**（`> [!warning] 源确缺答案…` / `> [!warning] 待人工核…`）。
    这些标注是**我们自己的核查记录，不是答案**；原判据把它当实体答案
    ⇒ **「自我满足式误判」**：标注让卡片看起来有答案，**可用率虚高 207 张**。

    修法：`classify_answer` 先把 callout 整块剥掉，再判是否还有实质内容。
    ⚠️ 「标注块 ＋ 真答案」必须仍判 True（不能过度剥离）。
    """
    only_warn = ("## 参考答案\n\n> [!warning] 源确缺答案\n> 本卡答案区为空，库内无任何可回源线索。\n"
                 "> 组卷时按无答案处理。\n")
    assert not fp.classify_answer(only_warn)["has_entity"], "只有标注块却被判有实体答案"
    warn_plus = ("## 参考答案\n\n> [!warning] 已核查\n\n答案 B，因为半径越大。\n")
    assert fp.classify_answer(warn_plus)["has_entity"], "标注块＋真答案被误判为无答案"


@case("答案区")
def 答案区支持重复标题形态():
    """🔴 回归（2026-10-07 第六形态，final_stats 时发现 47 张卡命中）：

    这些卡的正文被**整段复制了两遍**（`## 题目` 出现 2 次，整段逐字相同），
    于是 `## 参考答案` 出现 2–6 次。`search` 只取**第一个**，
    其后紧跟的同名标题立刻成为区界 ⇒ 截成空段 ⇒ 误判「答案区空」。

    实测受害：`题-CM-46-01-11在空气中向氯化亚铜中加入`（3 次）、
    `题-35决理-2-6-溶剂效应`（6 次）、`题-35决理-1-9`（6 次）。

    修法：取**最后一个「后面确实有内容」的**那个标题。
    """
    cases = [
        ("## 参考答案\n\n## 答案：\n\n## 参考答案\n\n答案 B。\n\n## 考点抽象\n\nx\n", True, "取最后一个有内容的"),
        ("## 参考答案\n\n因为半径越大。\n", True, "单标题不能退化"),
        ("## 参考答案\n> 本题答案见 [[卷-01]] 的参考答案区。\n", False, "外链型不能退化"),
        ("## 参考答案\n\n## 知识点映射\n\n- x\n", False, "真空答案区不能退化"),
        ("## 参考答案\n\n#1-1 (2分)\n\n答案 B。\n\n## 考点抽象\n\nx\n", True, "第五形态不能退化"),
        ("## 参考答案\n\n## 参考答案\n\n## 知识点映射\n\n- x\n", False, "两标题皆空取第一个"),
        ("## 答案与解析\n\n## 参考答案\n\n答案 B。\n", True, "连续答案标题不能退化"),
    ]
    for body, want, why in cases:
        got = fp.classify_answer(body)["has_entity"]
        assert got == want, "%s：has_entity=%s（期望 %s）" % (why, got, want)


@case("答案区")
def 答案区支持一级标题小问形态():
    """🔴 回归（2026-10-07 第五种形态，37 决补录时踩到）：

    库内决赛卡（`题-37决理-2-1-DNA 纳米结构`）的答案区用**一级标题**写小问：
    `## 参考答案` → `#1-1 (2分)` / `#1-2 （小计5分）` / `#(浓度转化过程 2 分)`。
    按「level ≤ 本级」规则会被截成 **9 字符空段** ⇒ 判「答案区空」。

    修法：井号后**紧跟数字或中文括号**的标题视为答案小问标题，不是区界。
    """
    body = ("## 参考答案\n\n#1-1 (2分)\n\n答案 B。\n\n#1-2 （小计5分）\n\n答案 C。\n\n"
            "## 考点抽象\n\n后面是别的节。\n")
    info = fp.classify_answer(body)
    assert info["has_entity"], "一级标题小问形态未被识别"
    s, e, k = fp.find_answer_section(body)
    seg = body[s:e]
    assert "考点抽象" not in seg, "区界错误：把 `## 考点抽象` 之后的都算进答案区"
    assert len(seg) > 30, "答案区段长 %d 仍被截断" % (e - s)
    # 其他四种形态不能退化
    for b2, want, why in [
        ("## 参考答案\n> 本题答案见 [[卷-01]] 的参考答案区。\n", False, "外链型"),
        ("## 参考答案\n\n## 知识点映射\n\n- x\n", False, "真空答案区"),
        ("## 答案与解析\n\n## 参考答案\n\n答案 B。\n", True, "连续答案标题"),
        ("## 参考答案\n\n因为半径越大。\n", True, "标准形态"),
    ]:
        got = fp.classify_answer(b2)["has_entity"]
        assert got == want, "%s：has_entity=%s（期望 %s）" % (why, got, want)


@case("答案区")
def 答案区标题支持后缀词形态():
    """🔴 回归（2026-10-07 反向验证发现，第 3 种形态）：

    `## 参考答案要点`（真题卡 `真题-有机-NAI环化对映选择性-001`）判成「无答案区」。
    修法：加**有限白名单**后缀词（要点/详解/汇总/对照/与解析/与解答/说明）
    ＋尾随括号。

    ⚠️ 后缀词表刻意**不放开成 `参考答案.*`**——否则
    「参考答案见 [[卷-01]] 的参考答案区」这类**指针句**也会被当标题，
    外链型就判不出来了。下方「外链不能退化」用例就是守这条线。
    """
    CASES = [
        ("## 参考答案要点\n\n- 9.3.1 缩醛手性碳构型保留\n", True, "后缀词"),
        ("## 答案与解析（详解）\n\n因为半径越大。\n", True, "后缀词+括号"),
        ("## 答案汇总\n\n答案 B。\n", True, "汇总"),
        ("## 参考答案\n\n因为半径越大。\n", True, "常规不能退化"),
        ("## 参考答案要点\n\n## 知识点映射\n\n- x\n", False, "真空答案区"),
        ("## 参考答案\n> 本题答案见 [[卷-01]] 的参考答案区。\n", False, "外链不能退化"),
    ]
    for body, want, why in CASES:
        info = fp.classify_answer(body)
        assert info["has_entity"] == want, "%s：has_entity=%s（期望 %s）" % (why, info["has_entity"], want)


@case("答案区")
def 库内异形答案卡能被新口径识别():
    """真实数据回归：抽 40 张原判「无答案区」的卡，新口径须能定位到答案区。"""
    import glob
    hit = 0
    for p in glob.glob(os.path.join(ROOT, "04-题库", "**", "*.md"), recursive=True):
        t = open(p, encoding="utf-8-sig", errors="replace").read()
        fmx, body = fp.split_fm(t)
        if re.search(r"(?m)^type[ \t]*:", fmx) is None or "status: deprecated" in fmx:
            continue
        if "## 参考答案" in body:
            continue                       # 只看原本被判「无标准答案区」的
        if fp.classify_answer(body)["found"]:
            hit += 1
        if hit >= 40:
            break
    assert hit >= 40, "只识别到 %d 张" % hit


# ══════════════════════════════════════════════════════════════
# 3. 库内真实数据（不依赖硬编码样本）
# ══════════════════════════════════════════════════════════════
@case("库内")
def 库内知识点索引可用():
    names, alias = fp.kp_index(os.path.join(ROOT, "03-知识点"))
    assert len(names) > 900, len(names)
    assert len(alias) > 3000, len(alias)
    for must in ("溶度积", "电离能", "配合物"):
        assert must in names, must


@case("库内")
def 库内题卡KP覆盖率():
    """在役**题目卡**（type: 题目 / 真题）应 100% 有 knowledge_points（fm_parse 口径）。

    ⚠️ 断言只对题目卡生效——索引/系统/题组/答案册等非题目卡本来就没有 KP，
    混进来会把覆盖率算成 97.67% 的假缺口（2026-10-07 实测踩过）。
    """
    import glob
    n = has = 0
    miss = []
    for p in glob.glob(os.path.join(ROOT, "04-题库", "**", "*.md"), recursive=True) + \
             glob.glob(os.path.join(ROOT, "05-真题库", "**", "*.md"), recursive=True):
        t = open(p, encoding="utf-8-sig", errors="replace").read()
        fmx, _ = fp.split_fm(t)
        if "status: deprecated" in fmx:
            continue
        tm = re.search(r"(?m)^type[ \t]*:[ \t]*(.+)$", fmx)
        if not tm or tm.group(1).strip() not in ("题目", "真题"):
            continue
        n += 1
        if fp.has_key(fmx, "knowledge_points"):
            has += 1
        else:
            miss.append(os.path.relpath(p, ROOT))
    assert n > 10000, n
    assert has == n, "有 %d 张题目卡无 KP：%s" % (len(miss), miss[:5])


@case("库内")
def 库内管线脚本都在入库目录():
    """管线脚本必须在 11-模板/scripts/（.workbuddy/ 被 gitignore 会丢）"""
    must = ["fm_parse.py", "gen_weak_drill.py", "special_papers.py", "qa_simvol_papers.py"]
    for f in must:
        assert os.path.exists(os.path.join(HERE, f)), f


@case("库内")
def 管线脚本无硬编码绝对路径():
    """2026-10-07 修：三条迁入脚本原本写死 vault 绝对路径"""
    for f in ("gen_weak_drill.py", "special_papers.py", "qa_simvol_papers.py"):
        t = open(os.path.join(HERE, f), encoding="utf-8", errors="replace").read()
        assert "__file__" in t, "%s 缺 __file__ 自动定位" % f
        assert "Obsidion" not in t, "%s 仍含硬编码路径" % f


# ══════════════════════════════════════════════════════════════
# 3. gen_weak_drill：KP 形态解析 + 外链型答案标注
# ══════════════════════════════════════════════════════════════
def _load(name):
    """加载管线模块并恢复 stdout。

    注意：`gen_module_set.py` / `gen_weak_drill.py` 在 import 时会
    ① 把 sys.stdout 换成 TextIOWrapper（原 wrapper 被 GC ⇒ 关闭）
    ② 缺参数时 sys.exit(1)
    所以这里必须备份并**重新绑定 stdout**，否则测试进程自身的 print 会炸。
    """
    old = sys.stdout
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    finally:
        sys.stdout = old
    return m


def _load_partial(name, symbols):
    """只执行源码中指定的顶层定义（用于有 CLI 副作用的脚本）。

    `gen_module_set.py` 的主逻辑在模块级执行（无 __main__ 保护），
    直接 import 会触发 sys.exit 并破坏 stdout；改用 ast 精确提取所需定义后独立编译执行。
    """
    import ast
    src = open(os.path.join(HERE, name + ".py"), encoding="utf-8", errors="replace").read()
    tree = ast.parse(src)
    import io, random, collections, types
    ns = {"__file__": os.path.join(HERE, name + ".py"), "re": re, "os": os, "sys": sys,
          "io": io, "random": random, "collections": collections}
    picked = []
    for node in tree.body:
        nm = getattr(node, "name", None)
        if isinstance(node, ast.Try):
            picked.append(node)                      # _kps_of 定义在 try/except 里
        elif isinstance(node, ast.Assign):           # 顶层常量（MERGE / QUOTA …）
            tgt = node.targets[0]
            if isinstance(tgt, ast.Name) and tgt.id in symbols:
                picked.append(node)
        elif nm in symbols:
            picked.append(node)
    if not picked:
        raise AssertionError("源码里找不到 %s" % symbols)
    exec(compile(ast.Module(body=picked, type_ignores=[]), name + "<extract>", "exec"), ns)
    return ns


@case("gen_weak_drill")
def gwd_fm_list覆盖四形态():
    g = _load("gen_weak_drill")
    f = g.fm_list
    a = f(['k: ["[[A]]", "[[B]]"]'], "k")
    b = f(['k: ["[[A]]",', '  "[[B]]"]'], "k")
    c = f(['k:', '  - "[[A]]"', '  - "[[B]]"'], "k")
    d = f(['k: "[[A]]"'], "k")
    assert a == ["[[A]]", "[[B]]"], "同行数组 → %s" % a
    assert b == ["[[A]]", "[[B]]"], "跨行数组 → %s" % b
    assert c == ["[[A]]", "[[B]]"], "块列表 → %s" % c
    assert d == ["[[A]]"], "标量 → %s" % d


@case("gen_weak_drill")
def gwd_重复键取最后一次():
    """该脚本刻意保留 YAML 后值覆盖语义（库内有 104 条真题重复键）"""
    g = _load("gen_weak_drill")
    got = g.fm_list(['k: ["[[旧]]"]', 'k: ["[[新]]"]'], "k")
    assert got == ["[[新]]"], got


@case("gen_weak_drill")
def gwd_外链型答案不被当成答案():
    """577 张外链型卡：答案区只写指引，摘要须明确标注而非截指引原文"""
    g = _load("gen_weak_drill")
    p = os.path.join(ROOT, "04-题库", "教材习题", "二分册能力测试", "逐题",
                     "题-卷01-01-HI平衡KpKcKx关系与Kp计算.md")
    if not os.path.exists(p):
        return  # 数据不在则跳过
    seg = g.ans_summary(g.Path(p))
    assert "答案见卷册" in seg, seg
    assert "[[" not in seg, "不应把 wikilink 指引原样当答案输出：%s" % seg


# ══════════════════════════════════════════════════════════════
# 4. gen_module_set：KP 解析（回归：曾 1635/1919 张只取到 1 项）
# ══════════════════════════════════════════════════════════════
@case("gen_module_set")
def gms_kps覆盖三形态():
    ns = _load_partial("gen_module_set", ["_kps_of"])
    f = ns["_kps_of"]
    assert f('knowledge_points: ["[[A]]", "[[B]]"]') == ["A", "B"]
    assert f('knowledge_points:\n  - "[[A]]"\n  - "[[B]]"') == ["A", "B"]
    assert f('knowledge_points: ["[[A]]",\n  "[[B]]"]') == ["A", "B"]


@case("gen_module_set")
def gms_kps不越界取后三():
    ns = _load_partial("gen_module_set", ["_kps_of"])
    fm = 'knowledge_points: ["[[A]]", "[[B]]", "[[C]]", "[[D]]"]'
    assert ns["_kps_of"](fm) == ["A", "B", "C"]


@case("gen_module_set")
def gms_块列表形态原本会漏项():
    """回归证据：修复前用 `\\[(.*?)\\]`，块列表形态返回 []（KP 全丢）"""
    import re as _re
    fm = 'knowledge_points:\n  - "[[A]]"\n  - "[[B]]"'
    old = _re.search(r"(?ms)^knowledge_points[ \t]*:[\s]*\[(.*?)\]", fm)
    old_got = [] if not old else _re.findall(r"\[\[([^\]|]+)", old.group(1))
    assert old_got == [], "前提变了：旧正则居然能解析块列表"
    ns = _load_partial("gen_module_set", ["_kps_of"])
    assert ns["_kps_of"](fm) == ["A", "B"]


# ══════════════════════════════════════════════════════════════
# 4. testpaper_v2：KP 接入（2026-10-07）
# ══════════════════════════════════════════════════════════════
@case("testpaper_v2")
def tp2_有main保护():
    """🔴 回归：2026-10-07 误跑本脚本，**实际改写了库**——
    重写 3 个阶段测试卷 ＋ 给 150 张卡回填 `used_in`。
    根因是它是「生成类脚本」且无 dry-run。⇒ 必须有 `__main__` 保护，
    且测试**只测解析层**、绝不 import 后直接调用 main。"""
    src = open(os.path.join(HERE, "testpaper_v2.py"), encoding="utf-8", errors="replace").read()
    assert 'if __name__ == "__main__":' in src, "缺 __main__ 保护，import 即产生副作用"
    # 生成与回填入口必须在 __main__ 之内
    body = src.split('if __name__ == "__main__":', 1)[1]
    assert "write_paper(" in body, "write_paper 不在 main 内"
    assert "backfill(" in body, "backfill 不在 main 内"
    # 模块顶层不得出现写盘调用
    import re as _re2
    top = src.split('if __name__ == "__main__":', 1)[0]
    # 只看真正的调用行（排除 def 定义行）
    calls = [_re2.sub(r"^\s+", "", ln) for ln in top.split("\n")
             if not ln.lstrip().startswith("def ")]
    calls = "\n".join(calls)
    assert "write_paper(" not in calls, "顶层调用了 write_paper（import 即写盘）"
    assert "backfill(" not in calls, "顶层调用了 backfill（import 即改 FM）"


@case("testpaper_v2")
def tp2_路径自动定位():
    src = open(os.path.join(HERE, "testpaper_v2.py"), encoding="utf-8", errors="replace").read()
    assert "__file__" in src, "缺 __file__ 自动定位"
    assert "Obsidion" not in src, "仍含硬编码 vault 路径"


@case("testpaper_v2")
def tp2_KP解析走fm_parse():
    """KP 是数组形态（原 parse_fm 的正则只认标量会全漏），须走 fm_parse。"""
    ns = _load_partial("testpaper_v2", ["parse_fm"])
    pf = ns["parse_fm"]
    import tempfile
    cases = [
        ('knowledge_points: ["[[晶胞]]", "[[化学平衡]]"]', ["晶胞", "化学平衡"]),
        ('knowledge_points:\n  - "[[晶胞]]"', ["晶胞"]),
        ('knowledge_points: "[[晶胞]]"', ["晶胞"]),
    ]
    for kp, want in cases:
        txt = '---\ntitle: t\npack: 模块习题集\nsubject_module: 结构化学\ndifficulty: 4\n' + kp + '\n---\n\n## 题目\nx\n'
        fd, p = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        open(p, "w", encoding="utf-8").write(txt)
        try:
            fm = pf(p)
            assert fm is not None, "parse_fm 返回 None：%r" % kp
            assert fm.get("kps") == want, "%r → %s（期望 %s）" % (kp, fm.get("kps"), want)
        finally:
            os.unlink(p)


@case("testpaper_v2")
def tp2_KP贪心覆盖():
    """select(target_kps=[...])：每个目标 KP 先保底 1 题，且不与原配额重复抽。"""
    ns = _load_partial("testpaper_v2", ["select", "pick_pool", "normalize", "allocate_quota", "pick_from", "MERGE", "QUOTA"])
    sel = ns["select"]

    def rec(name, kps, subj="结构化学", diff=4, group="晶体结构"):
        fm = {"pack": "模块习题集", "subject_module": subj, "status": "已填充",
              "submodule": group, "difficulty": diff}
        if kps is not None:
            fm["kps"] = kps
        return (name, fm)

    # ⚠️ 数据量要够：allocate_quota 按「子模块组」分配配额，组太少会除零。
    #    真实池有十几个子模块组，这里造 6 组 × 8 题。
    groups = ["晶体结构", "分子结构", "配位化学", "立体化学", "分析化学", "元素化学"]
    records = []
    for gi, g in enumerate(groups):
        for j in range(8):
            kps = [["晶胞", "化学平衡"]][0] if (gi == 0 and j < 2) else \
                  ["分子对称性"] if gi == 1 else ["能级"] if gi == 2 else \
                  ["立体选择性"] if gi == 3 else ["滴定分析"] if gi == 4 else ["元素性质"]
            records.append(rec("%s-%02d" % (g, j), kps, group=g))
    records.append(rec("无KP题", None, group="元素化学"))
    _, chosen = sel("结构化学", records, seed=42, target_kps=["晶胞", "化学平衡"])
    files = {p["file"] for p in chosen}
    assert "晶体结构-00" in files, "晶胞保底题未入卷：%s" % sorted(files)[:8]
    assert len(chosen) == len({p["file"] for p in chosen}), "出现重复题"


# ══════════════════════════════════════════════════════════════
def run(filter_=None):
    passed, failed = 0, []
    for group, name, fn in CASES:
        if filter_ and filter_ not in group and filter_ not in name:
            continue
        try:
            fn()
            print("  ✔ [%s] %s" % (group, name))
            passed += 1
        except AssertionError as e:
            print("  ✘ [%s] %s —— %s" % (group, name, str(e)[:110]))
            failed.append((group, name))
        except Exception as e:
            print("  💥 [%s] %s —— %s: %s" % (group, name, type(e).__name__, str(e)[:90]))
            failed.append((group, name))
    print()
    print("通过 %d / %d" % (passed, passed + len(failed)))
    if failed:
        print("失败：" + "、".join("%s/%s" % f for f in failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else None))