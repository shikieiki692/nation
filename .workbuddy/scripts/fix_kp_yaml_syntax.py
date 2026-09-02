# -*- coding: utf-8 -*-
"""03-知识点 60 个 js-yaml 解析失败文件的分类修复（A/B/D/E 四类）。

A 类(41)：frontmatter 双引号 wikilink 内 \\ → /
B 类(9)：frontmatter 内误入的 ![[...]] 嵌入行 → 图存在则挪正文 h1 后，缺失则删除；
         共轭体系电子计数 额外删 "### 已配图" 行、嵌入行插正文引用块后
D 类(5)：key_images: [] 空壳挂回缩进条目（3 个）；相图与相平衡 删 2 行冗余图题；
         原子轨道与波函数 2 条 wikilink 挪 sources（正斜杠、去 .md）
E 类(5)：tags/sources 断行精确行对替换（flow 内 [x,y] 加引号、]related 拆行）

用法：python -X utf8 fix_kp_yaml_syntax.py [--write]
默认 dry-run；--write 实写并先打 zip 快照到 .workbuddy/backups/。
读写一律 newline=""，行尾原样保留；新插行按邻居风格补 \\r。
"""
import os, sys, zipfile, datetime

VAULT = r"C:\Obsidion\妙妙屋"
TMP = os.path.join(VAULT, ".workbuddy", "tmp")
MEDIA = os.path.join(VAULT, "媒体仓库")

def load_list(fn):
    p = os.path.join(TMP, fn)
    out = []
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if l:
            out.append(l)
    return out

A_FILES = load_list("_jsyaml_fail_A.txt")
B_FILES = load_list("_jsyaml_fail_Btag.txt")
D_FILES = load_list("_jsyaml_fail_D.txt")
E_FILES = load_list("_jsyaml_fail_.txt")
assert len(A_FILES) == 41 and len(B_FILES) == 9 and len(D_FILES) == 5 and len(E_FILES) == 5, \
    f"清单数量异常 A={len(A_FILES)} B={len(B_FILES)} D={len(D_FILES)} E={len(E_FILES)}"

D_EMPTY_KI = {"分光光度法.md", "沉淀滴定.md", "小分子活化.md"}
D_XIANGTU = "相图与相平衡.md"
D_YUANZI = "原子轨道与波函数.md"
B_SPECIAL = "共轭体系电子计数.md"

E_EDITS = {
    "2+2环加成.md": [
        (["tags: [化竞, 有机化学, [2+2]",
          "环加成, 环丁烷, 光化学, 周环反应, 烯酮]related:"],
         ['tags: [化竞, 有机化学, "[2+2]环加成", 环丁烷, 光化学, 周环反应, 烯酮]',
          "related:"]),
    ],
    "Claisen重排.md": [
        (["tags: [化竞, 有机化学, Claisen重排, [3,3]",
          "-σ迁移, 周环反应, 协同反应, 烯丙基醚, 热重排]related: [Cope重排, 周环反应, 芳香亲电取代, Diels-Alder反应, 烯烃, 酚]"],
         ['tags: [化竞, 有机化学, Claisen重排, "[3,3]-σ迁移", 周环反应, 协同反应, 烯丙基醚, 热重排]',
          "related: [Cope重排, 周环反应, 芳香亲电取代, Diels-Alder反应, 烯烃, 酚]"]),
    ],
    "Fischer吲哚合成.md": [
        (["tags: [化竞, 有机化学, Fischer吲哚合成, 吲哚合成, 苯肼, [3,3]",
          "-σ迁移, 芳香化]related: [Paal-Knorr合成, 吡咯, Larock吲哚合成, Bartoli吲哚合成, 杂环合成]"],
         ['tags: [化竞, 有机化学, Fischer吲哚合成, 吲哚合成, 苯肼, "[3,3]-σ迁移", 芳香化]',
          "related: [Paal-Knorr合成, 吡咯, Larock吲哚合成, Bartoli吲哚合成, 杂环合成]"]),
    ],
    "σ迁移反应.md": [
        (["tags: [化竞, 有机化学, σ迁移反应, 西格玛迁移, [1,n]",
          "-迁移, [3,3]-迁移, Cope重排, Claisen重排, 周环反应]related: [Diels-Alder反应, 电环化反应, 前线轨道理论, Cope重排, Claisen重排]"],
         ['tags: [化竞, 有机化学, σ迁移反应, 西格玛迁移, "[1,n]-迁移", "[3,3]-迁移", Cope重排, Claisen重排, 周环反应]',
          "related: [Diels-Alder反应, 电环化反应, 前线轨道理论, Cope重排, Claisen重排]"]),
    ],
    "质子转移可行性.md": [
        (['  - "ABOC §2.1',
          '  - §2.4 行 1544-1600"'],
         ['  - "ABOC §2.1"',
          '  - "§2.4 行 1544-1600"']),
    ],
}

D_YUANZI_NEW_SOURCES = [
    "sources:",
    '  - "[[07-资料提炼/书籍提炼/提炼-Atkins物理化学-主题7-8-9-量子理论与结构]]"',
    '  - "[[07-资料提炼/书籍提炼/提炼-普化原理-第11章-原子结构]]"',
]
D_YUANZI_DROP = [
    '  - "[[07-资料提炼\\书籍提炼\\提炼-Atkins物理化学-主题7-8-9-量子理论与结构.md]]"',
    '  - "[[07-资料提炼\\书籍提炼\\提炼-普化原理-第11章-原子结构.md]]"',
]

# ── 媒体仓库文件名索引（B 类存在性判断）──
print("索引媒体仓库文件名 ...")
media_names = set()
for root, dirs, fs in os.walk(MEDIA):
    for f in fs:
        media_names.add(f)
print(f"  共 {len(media_names)} 个文件名\n")


def read_text(p):
    return open(p, encoding="utf-8", newline="").read()


def write_text(p, t):
    open(p, "w", encoding="utf-8", newline="").write(t)


def fm_bounds(lines):
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return (0, i)
    return None


def fix_inline_links(s):
    """双引号 wikilink 内 \\ → /（仅 \"[[ ... ]]\" 段内）。"""
    out, j, in_link = [], 0, False
    while j < len(s):
        if not in_link and s.startswith('"[[', j):
            in_link = True
            out.append('"[[')
            j += 3
        elif in_link:
            if s.startswith(']]"', j):
                in_link = False
                out.append(']]"')
                j += 3
            else:
                out.append("/" if s[j] == "\\" else s[j])
                j += 1
        else:
            out.append(s[j])
            j += 1
    return "".join(out)


def tr_of(line):
    """行分隔符的字面 CR 部分：CRLF 行返回 '\\r'（LF 由 join 提供，元素内禁止含 \\n）。"""
    return "\r" if line.endswith("\r") else ""


def apply_edits(lines, edits, label):
    """精确连续行块替换（等长），逐行保留原行尾。"""
    for old, new in edits:
        assert len(old) == len(new)
        for i in range(len(lines) - len(old) + 1):
            if all(lines[i + k].rstrip("\r") == old[k] for k in range(len(old))):
                for k in range(len(old)):
                    lines[i + k] = new[k] + tr_of(lines[i + k])  # 行尾取实际行，非模板
                break
        else:
            raise SystemExit(f"[{label}] EDIT NOT FOUND: {old!r}")


changes = {}  # rel -> [描述]


def do_fix(rel):
    p = os.path.join(VAULT, rel)
    t = read_text(p)
    lines = t.split("\n")
    fb = fm_bounds(lines)
    if fb is None:
        raise SystemExit(f"{rel}: 无 frontmatter？")
    fm_end = fb[1]
    name = os.path.basename(rel)
    log = []

    # ── A 类：双引号 wikilink 反斜杠 ──
    if rel in A_FILES:
        n = 0
        for i in range(1, fm_end):
            ln = lines[i]
            if '"[[' in ln:
                tr = tr_of(ln)
                new = fix_inline_links(ln.rstrip("\r") if tr else ln) + tr
                if new != ln:
                    lines[i] = new
                    n += 1
        log.append(f"A: 修正 {n} 行反斜杠 wikilink")

    # ── B 类：frontmatter 内 ![[...]] 行 ──
    if rel in B_FILES:
        embed_lines = []
        keep = []
        for i, ln in enumerate(lines):
            s = ln.strip()
            if i < fm_end and s.startswith("![["):
                embed_lines.append(ln.rstrip("\r"))
                continue
            if i < fm_end and name == B_SPECIAL and s.startswith("###"):
                log.append(f"B: 删 FM 内标题行 {s!r}")
                continue
            keep.append(ln)
        lines = keep
        fb2 = fm_bounds(lines)
        fm_end = fb2[1]
        for ln in embed_lines:
            base = ln.strip()
            base = base[3:].split("]]")[0]  # 去掉 ![[ 与 ]] 后缀注释
            base = base.split("/")[-1]
            if base in media_names:
                if name == B_SPECIAL:
                    pos = None
                    for i in range(fm_end + 1, len(lines)):
                        if lines[i].startswith("> "):
                            pos = i
                    if pos is None:
                        raise SystemExit(f"{rel}: 找不到引用块插入点")
                else:
                    pos = None
                    for i in range(fm_end + 1, len(lines)):
                        if lines[i].startswith("# "):
                            pos = i
                            break
                    if pos is None:
                        pos = fm_end
                tr = tr_of(lines[pos])
                e = ln.rstrip("\r") + tr
                block = [tr, e]  # 空行 + 嵌入行（元素不含 \n）
                if pos + 1 < len(lines) and lines[pos + 1].strip() != "":
                    block.append(tr)  # 插入点后无空行则补一行
                lines[pos + 1:pos + 1] = block
                log.append(f"B: 嵌入挪正文（{base} 存在）")
            else:
                log.append(f"B: 嵌入删除（{base} 媒体仓库缺失）")

    # ── D 类 ──
    if rel in D_FILES:
        if name in D_EMPTY_KI:
            for i, ln in enumerate(lines):
                if ln.rstrip("\r") == "key_images: []" and i + 1 < len(lines) \
                        and lines[i + 1].strip().startswith("- "):
                    lines[i] = "key_images:" + tr_of(ln)
                    log.append("D: key_images [] 空壳挂回缩进条目")
                    break
            else:
                raise SystemExit(f"{rel}: 未找到 key_images: [] + 缩进条目")
        elif name == D_XIANGTU:
            drop = {'  - "水的相图"', '  - "二氧化碳的相图"'}
            kept = [ln for ln in lines if ln.rstrip("\r") not in drop]
            nd = len(lines) - len(kept)
            assert nd == 2, f"{rel}: 预期删 2 行实删 {nd}"
            lines = kept
            log.append("D: 删 2 行冗余图题（正文已有等价图注）")
        elif name == D_YUANZI:
            for i, ln in enumerate(lines):
                if ln.rstrip("\r") == "sources: []":
                    tr = tr_of(ln)
                    repl = [s + tr for s in D_YUANZI_NEW_SOURCES]
                    lines[i:i + 1] = repl
                    break
            else:
                raise SystemExit(f"{rel}: 未找到 sources: []")
            dropset = {s for s in D_YUANZI_DROP}
            kept = [ln for ln in lines if ln.rstrip("\r") not in dropset]
            nd = len(lines) - len(kept)
            assert nd == 2, f"{rel}: 预期删 2 条目实删 {nd}"
            lines = kept
            log.append("D: 2 条 wikilink 挪 sources（正斜杠去 .md），删 key_images 后原条目")

    # ── E 类 ──
    if name in E_EDITS:
        apply_edits(lines, E_EDITS[name], rel)
        log.append("E: 精确行对替换 " + "；".join(str(len(a)) + "行块" for a, _ in E_EDITS[name]))

    if not log:
        return None
    assert not any("\n" in ln for ln in lines), f"{rel}: 行元素混入 \\n（会产生多余空行）"
    changes[rel] = log
    return "\n".join(lines)


WRITE = "--write" in sys.argv
if WRITE:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = os.path.join(VAULT, ".workbuddy", "backups", f"fix_kp_yaml_{ts}.zip")
    os.makedirs(os.path.dirname(bak), exist_ok=True)
    zf = zipfile.ZipFile(bak, "w", zipfile.ZIP_DEFLATED)
for rel in A_FILES + B_FILES + D_FILES + E_FILES:
    new_t = do_fix(rel)
    if new_t is None:
        print(f"-- {rel}: 无变更（异常，应四类之一）")
        continue
    p = os.path.join(VAULT, rel)
    for msg in changes[rel]:
        print(f"   {msg}")
    if WRITE:
        zf.write(p, rel)  # 快照写前状态
        write_text(p, new_t)

if WRITE:
    zf.close()
    print(f"快照 → {bak}")
print(f"\n共 {len(changes)} 个文件有变更。模式：{'实写' if WRITE else 'dry-run'}")
if not WRITE:
    print("确认无误后加 --write 实写。")
