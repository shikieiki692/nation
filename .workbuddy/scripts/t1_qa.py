# -*- coding: utf-8 -*-
"""T1 质检：docx vs md 题量/图数/答案泄漏（按段落抽文本）"""
import io, re, sys, zipfile
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

VAULT = Path(r"C:/Obsidion/妙妙屋")
SRC = VAULT / "04-课件" / "习题集"
STU = VAULT / ".workbuddy" / "tmp" / "student_build"
OUT = VAULT / ".workbuddy" / "tmp" / "_t1_out"

names = ["第一轮化学原理-化学动力学习题集","第一轮化学原理-化学平衡习题集","第一轮化学原理-气体与溶液习题集",
         "第一轮化学原理-沉淀溶解平衡习题集","第一轮化学原理-溶液与相图习题集","第一轮化学原理-热力学习题集",
         "第一轮化学原理-电化学习题集","第一轮化学原理-酸碱理论习题集",
         "第一轮结构化学-元素周期表与周期律练习题组","第一轮结构化学-分子结构练习题组",
         "第一轮结构化学-原子结构练习题组","第一轮结构化学-晶体结构练习题组","第一轮结构化学-配位化合物练习题组"]

QPAT = re.compile(r'^\s*#{2,3}\s*(第\s*\d+\s*题|教-\d+题|赵-\d+题|汇-\d+题)', re.M)

def paragraphs(p):
    with zipfile.ZipFile(p) as z:
        doc = z.read("word/document.xml").decode("utf-8", "replace")
        imgs = [n for n in z.namelist() if n.startswith("word/media/")]
    # 每个 <w:p> 拼成一段
    paras = []
    for pm in re.finditer(r"<w:p[ >].*?</w:p>|<w:p/>", doc, re.S):
        seg = pm.group(0)
        txt = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", seg))
        paras.append(txt)
    return paras, imgs

def count_q(paras):
    # 题头 = 段落以「第N题」/「教-N题」等 开头
    n = 0
    for s in paras:
        if re.match(r"^\s*(第\s*\d+\s*题|教-\d+题|赵-\d+题|汇-\d+题)", s):
            n += 1
    return n

print(f"{'文件':<40}{'md题':>5}{'师题':>5}{'生题':>5}{'md图':>5}{'师图':>5}{'生图':>5}{'生泄漏':>7}")
issues = []
for n in names:
    mt = (SRC/(n+".md")).read_text(encoding="utf-8")
    st = (STU/(n+".md")).read_text(encoding="utf-8")
    mq = len(QPAT.findall(mt)); sq = len(QPAT.findall(st))
    mi = mt.count("![[")
    tparas, timgs = paragraphs(OUT/(n+".docx"))
    sparasm, simgs = paragraphs(OUT/("学生版-"+n+".docx"))
    tq = count_q(tparas); sq2 = count_q(sparasm)
    sfull = "\n".join(sparasm)
    leak = len(re.findall(r"参考答案|\*\*答案[:：]|^答案[:：]", sfull, re.M))
    flag = ""
    if sq != sq2: flag += f" 生题{sq2}≠{sq}!"
    if mi != len(timgs): flag += f" 师图{len(timgs)}≠{mi}!"
    if leak: flag += f" 生泄漏{leak}!"
    if flag: issues.append((n, flag))
    print(f"{n:<40}{mq:>5}{tq:>5}{sq2:>5}{mi:>5}{len(timgs):>5}{len(simgs):>5}{leak:>7}{flag}")
print("-"*100)
print(f"异常文件 {len(issues)} 个")
for n, f in issues: print("  ", n, f)
