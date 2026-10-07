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
    ns = {"__file__": os.path.join(HERE, name + ".py"), "re": re, "os": os, "sys": sys}
    picked = []
    for node in tree.body:
        nm = getattr(node, "name", None)
        if isinstance(node, ast.Try):
            picked.append(node)                      # _kps_of 定义在 try/except 里
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