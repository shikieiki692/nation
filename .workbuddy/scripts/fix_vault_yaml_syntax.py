# -*- coding: utf-8 -*-
r"""全库剩余 48 个 js-yaml 解析失败文件的分类修复（11 种处理器）。

清单来源：.workbuddy/tmp/_jsyaml_all_fail.txt（jsyaml_scan_all.js v2 全库扫描）。
R1 任务卡(16)：source_notes/related_notes/evidence 逗号连写 wikilink → 合法 inline list
R2 课件(2)：last_audit 值含裸 `: ` → 双引号包裹
R3 WARNING(8)：title 值含 `: ` 与 `\` → 单引号包裹
R4 习题提炼(13)：target_kp: [[ 多一个 [ → 删之
R5(1)：`- [Re₂Cl₈]...` 条目被当 flow → 双引号包裹
R6(1)：third_round_target 值含裸 `: ` → 双引号包裹
R7(2)：knowledge_points 行内 [5+2]环加成 → 加引号
R8(1)：tags: [[2+2]环加成,... → 首项加引号
R9(1)：FM 内全角引号 “” → ASCII "
R10(2)：`- 2026-06-25: **...` 值以 * 开头(被当 alias) → 双引号包裹
R11(1)：aliases: - x 单行连写 → 拆两行

用法：python -X utf8 fix_vault_yaml_syntax.py [--write]
读写 newline=""，行元素禁含 \n，行尾 tr_of 取实际行；写前 zip 快照。
"""
import os, sys, re, zipfile, datetime

VAULT = r"C:\Obsidion\妙妙屋"
TMP = os.path.join(VAULT, ".workbuddy", "tmp")

FILES = []
for l in open(os.path.join(TMP, "_jsyaml_all_fail.txt"), encoding="utf-8"):
    l = l.strip()
    if l:
        FILES.append(l.split("\t")[0])
assert len(FILES) == 48, f"清单应 48 个，实得 {len(FILES)}"

FIELD_RE = re.compile(r"^(source_notes|related_notes|evidence): (\[\[.+)$")
WIKI_RE = re.compile(r"\[\[([^\]]+)\]\]")


def tr_of(line):
    return "\r" if line.endswith("\r") else ""


def read_text(p):
    return open(p, encoding="utf-8", newline="").read()


def fix_r1(lines, fm_end, log):
    """任务卡：wikilink 逗号连写字段 → 合法形态。

    纯 wikilink 段 → 逐项加引号；含残留文本的段（如 "[[X]] §1.1" 章节引用）
    → 整段加双引号，零文本丢失（断言无 " 无 \\ 且以 [[ 开头）。
    """
    for i, ln in enumerate(lines):
        if i >= fm_end:
            break
        core = ln.rstrip("\r")
        m = FIELD_RE.match(core)
        if not m:
            continue
        rest = m.group(2)
        segs = []
        for p in (s.strip() for s in rest.split(",")):
            links = WIKI_RE.findall(p)
            residual = WIKI_RE.sub("", p).strip()
            assert links or residual, f"空段: {p!r}"
            assert '"' not in p and "\\" not in p, f"段含引号或反斜杠: {p!r}"
            if residual:
                assert p.startswith("[["), f"残留段不以 wikilink 开头: {p!r}"
                segs.append('"' + p + '"')
            else:
                segs.extend('"[[' + l + ']]"' for l in links)
        assert segs, f"未产出任何项: {rest!r}"
        val = segs[0] if len(segs) == 1 else "[" + ", ".join(segs) + "]"
        lines[i] = m.group(1) + ": " + val + tr_of(ln)
        log.append(f"R1: {m.group(1)} → {val[:60]}{'…' if len(val) > 60 else ''}")


def quote_double(core, prefix):
    """值部分加双引号（断言值内无 " 与 \\）。"""
    val = core[len(prefix):]
    assert '"' not in val and "\\" not in val, f"值含 \" 或 \\，双引号不安全: {val!r}"
    return prefix + '"' + val + '"'


def quote_single(core, prefix):
    """值部分加单引号（断言值内无 '）。"""
    val = core[len(prefix):]
    assert "'" not in val, f"值含 '，单引号不安全: {val!r}"
    return prefix + "'" + val + "'"


def do_fix(rel):
    p = os.path.join(VAULT, rel)
    lines = read_text(p).split("\n")
    end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    assert end > 0 and lines[0].strip() == "---", f"{rel}: frontmatter 异常"
    fm_end = end
    base = os.path.basename(rel)
    log = []

    if "WARNING__META" in rel:
        for i in range(1, fm_end):
            core = lines[i].rstrip("\r")
            if core.startswith("title: ") and ": " in core[len("title: "):]:
                lines[i] = quote_single(core, "title: ") + tr_of(lines[i])
                log.append("R3: title 单引号包裹")
    elif rel.startswith("00-首页") and base.startswith("任务卡-"):
        fix_r1(lines, fm_end, log)
    elif base.startswith("习题-普化原理-"):
        for i in range(1, fm_end):
            core = lines[i].rstrip("\r")
            if core.startswith("target_kp: [["):
                lines[i] = core.replace("target_kp: [[", "target_kp: [", 1) + tr_of(lines[i])
                assert core.count("[") == core.count("]") + 1, core
                log.append("R4: target_kp 删多余 [")
    elif base in ("晶体学与晶体结构-第一轮基础版（普化原理）.md",
                  "配位化合物基础-第一轮基础版（普化原理）.md"):
        for i in range(1, fm_end):
            core = lines[i].rstrip("\r")
            if core.startswith("last_audit: ") and ": " in core[len("last_audit: "):]:
                lines[i] = quote_double(core, "last_audit: ") + tr_of(lines[i])
                log.append("R2: last_audit 双引号包裹")
    elif "届初赛试题解析" in base and ("第36届" in base or "第38届" in base):
        # 裸化学名 token（flow list 里被当嵌套 sequence）→ 加引号；(?<!") 防止重复包裹
        R7_TOKENS = ("[5+2]环加成", "[2,3]-σ迁移")
        for i in range(1, fm_end):
            core = lines[i].rstrip("\r")
            if not core.startswith("knowledge_points: ["):
                continue
            n = 0
            for tok in R7_TOKENS:
                core, k = re.subn(r'(?<!")' + re.escape(tok), '"' + tok + '"', core)
                n += k
            if n:
                lines[i] = core + tr_of(lines[i])
                log.append(f"R7: 裸化学名 token 加引号 ×{n}")
    elif base.startswith("题-ZOC-027-"):
        for i in range(1, fm_end):
            core = lines[i].rstrip("\r")
            if core.startswith("tags: [[2+2]环加成, "):
                lines[i] = core.replace("tags: [[2+2]环加成, ", 'tags: ["[2+2]环加成", ', 1) + tr_of(lines[i])
                log.append("R8: tags 首项加引号")
    elif base.startswith("题-025决-8-"):
        for i in range(1, fm_end):
            core = lines[i].rstrip("\r")
            m = re.match(r"^aliases: - (.+)$", core)
            if m:
                nl = tr_of(lines[i])
                lines[i:i + 1] = ["aliases:" + nl, "  - " + m.group(1) + nl]
                log.append("R11: aliases 拆两行")
    elif base.startswith("提炼-无机化学第五版-第21章"):
        for i in range(1, fm_end):
            core = lines[i].rstrip("\r")
            if core.startswith("  - [Re₂Cl₈]"):
                assert '"' not in core
                lines[i] = core[:4] + '"' + core[4:] + '"' + tr_of(lines[i])
                log.append("R5: Re₂Cl₈ 条目加引号")
    elif base.startswith("提炼-结构化学基础-第2章"):
        for i in range(1, fm_end):
            core = lines[i].rstrip("\r")
            if core.startswith("third_round_target: ") and ": " in core[len("third_round_target: "):]:
                lines[i] = quote_double(core, "third_round_target: ") + tr_of(lines[i])
                log.append("R6: third_round_target 双引号包裹")
    elif base == "任务卡-validate_kb与published断链目录治理.md":
        n = 0
        for i in range(1, fm_end):
            ln = lines[i]
            if "“" in ln or "”" in ln:
                lines[i] = ln.replace("“", '"').replace("”", '"')
                n += 1
        assert n >= 5, f"全角引号行数异常: {n}"
        log.append(f"R9: 全角引号→ASCII（{n} 行）")
    elif base in ("任务卡-超级充实版模式推广.md", "任务卡-结构部分超级充实讲义收官.md"):
        for i in range(1, fm_end):
            core = lines[i].rstrip("\r")
            m = re.match(r"^(\s+- \d{4}-\d{2}-\d{2}: )(\*\*.+)$", core)
            if m:
                assert '"' not in m.group(2)
                lines[i] = m.group(1) + '"' + m.group(2) + '"' + tr_of(lines[i])
                log.append("R10: * 开头值加引号")
    else:
        raise SystemExit(f"{rel}: 无匹配处理器")

    if not log:
        return None, []
    assert not any("\n" in ln for ln in lines), f"{rel}: 行元素混入 \\n"
    return "\n".join(lines), log


WRITE = "--write" in sys.argv
if WRITE:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = os.path.join(VAULT, ".workbuddy", "backups", f"fix_vault_yaml_{ts}.zip")
    zf = zipfile.ZipFile(bak, "w", zipfile.ZIP_DEFLATED)

done = 0
for rel in FILES:
    new_t, log = do_fix(rel)
    done += 1
    print(f"== {rel}")
    for msg in log:
        print(f"   {msg}")
    if WRITE and new_t is not None:
        zf.write(os.path.join(VAULT, rel), rel.replace("\\", "/"))
        open(os.path.join(VAULT, rel), "w", encoding="utf-8", newline="").write(new_t)

if WRITE:
    zf.close()
    print(f"\n快照 → {bak}")
print(f"\n处理 {done} 个文件。模式：{'实写' if WRITE else 'dry-run'}")
