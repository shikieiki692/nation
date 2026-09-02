# -*- coding: utf-8 -*-
"""浙江选择题入库生成器：读分类 JSON → 生成 type:题目 文件（按新题入库SOP v1.1）"""
import io, json, os, re, sys

ROOT = r"C:\Obsidion\妙妙屋"
SRC = os.path.join(ROOT, ".workbuddy", "scripts")
YEAR = sys.argv[1]
CLS = os.path.join(SRC, f"zj_class_{YEAR}.json")
OUTDIR = os.path.join(ROOT, "04-题库", "真题", "省预赛", f"浙江卷{YEAR}")

data = json.load(io.open(os.path.join(SRC, "zj_split_source.json"), encoding="utf-8"))
cls = json.load(io.open(CLS, encoding="utf-8"))
qs = {q["num"]: q for q in data[str(YEAR)]}

SUBJECTS = {"化学原理", "结构化学", "有机化学", "元素与分析"}
TYPES = {"单选": 60, "多选": 80}
yy = YEAR[2:]
created, skipped = [], []

for num_str, c in cls.items():
    num = int(num_str)
    if num not in qs:
        skipped.append(f"{num}: 题块不存在"); continue
    q = qs[num]
    qtype = q["type"]
    if not ((qtype == "单选" and num <= TYPES["单选"]) or (qtype == "多选" and 61 <= num <= TYPES["多选"])):
        skipped.append(f"{num}: 题型不符 {qtype}"); continue
    sm = c["subject_module"]
    if sm not in SUBJECTS:
        skipped.append(f"{num}: subject_module 非法 {sm}"); continue
    d = int(c["difficulty"])
    if not (1 <= d <= 5):
        skipped.append(f"{num}: difficulty 非法"); continue
    kps = [k for k in c["kps"] if k.strip()]
    if not (1 <= len(kps) <= 3):
        skipped.append(f"{num}: kps 数量非法"); continue
    desc = re.sub(r'[\\/:*?"<>|\s]+', "", c["desc"])[:12]
    if not desc:
        skipped.append(f"{num}: desc 空"); continue
    fn = f"题-浙江{yy}-{qtype}-{num:02d}-{desc}.md"
    title = fn[:-3]
    body = q["body"].strip()
    ans = q["answer"] or "（原卷答案存疑，见主卷答案文件 [待核] 标注）"
    fm = [
        "---",
        f'title: "{title}"',
        "type: 题目",
        f'submodule: {c["submodule"]}',
        "exam_stage: 省预赛",
        f"subject: {sm}",
        f"difficulty: {d}",
        f'teaching_level: {c["teaching_level"]}',
        "fidelity: 原书逐字",
        f'subject_module: {sm}',
        "pack: 预赛专项",
        "status: 已填充",
        f"year: {YEAR}",
        f"province: 浙江",
        f'source: {YEAR}年浙江省预赛试题第{num}题（{qtype}）',
        'source_file: "[[04-题库/真题/省预赛/' + f"{YEAR}-浙江预赛]]\"",
        f'cross_references: ["[[04-题库/真题/省预赛/{YEAR}-浙江预赛]]"]',
        "knowledge_points: []",
        "tags: [化竞, 真题, 省预赛, 浙江, " + f"{YEAR}, {qtype}, {c['submodule']}" + "]",
        "created: 2026-09-02",
        "updated: 2026-09-02",
        f"aliases: [浙江{yy}-{qtype}{num:02d}]",
        "---",
    ]
    content = eol_body = "\n".join(fm) + "\n\n"
    content += f"# {title}\n\n{body}\n\n## 参考答案\n\n<details>\n<summary>📖 查看答案</summary>\n\n"
    content += f"**答案：{ans}**\n\n"
    content += "> ⚠️ **AI 解题参考答案（非官方评分标准）**；原卷整页图已随题嵌入，可对照核对。\n"
    if not q["answer"]:
        content += "> ⚠️ **存疑题**：官方原答案缺失，此为 AI 判定，见主卷答案文件 [待核] 清单。\n"
    content += "\n</details>\n"
    # knowledge_points 行修正（上面拼接易碎，重写一次）
    kp_line = "knowledge_points: [" + ", ".join(f'"[[{k}]]"' for k in kps) + "]"
    content = re.sub(r"^knowledge_points: .*$", kp_line, content, count=1, flags=re.M)
    os.makedirs(OUTDIR, exist_ok=True)
    p = os.path.join(OUTDIR, fn)
    assert not os.path.exists(p), f"文件已存在: {fn}"
    io.open(p, "w", encoding="utf-8", newline="\n").write(content)
    created.append(fn)

print(f"创建 {len(created)}, 跳过 {len(skipped)}")
for s in skipped:
    print("SKIP", s)
