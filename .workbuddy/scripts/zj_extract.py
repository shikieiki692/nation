# -*- coding: utf-8 -*-
"""浙江三卷选择题拆题：解析题块 + 答案映射 → JSON（供分类代理使用）"""
import io, json, re, os

ROOT = r"C:\Obsidion\妙妙屋"
SRC = os.path.join(ROOT, "04-题库", "真题", "省预赛")
OUT = os.path.join(ROOT, ".workbuddy", "scripts")

def parse_paper(year):
    p = os.path.join(SRC, f"{year}-浙江预赛.md")
    lines = io.open(p, encoding="utf-8").read().splitlines()
    qpat = re.compile(r"^\*\*(\d+)\.\*\*\s*(.*)$")
    blocks = {}
    order = []
    cur = None
    for ln in lines:
        m = qpat.match(ln)
        if m:
            cur = int(m.group(1))
            blocks[cur] = [m.group(2)]
            order.append(cur)
            continue
        if cur is not None:
            if ln.strip() == "---" and len(blocks) > 70:
                break
            blocks[cur].append(ln)
    # 答案映射（只解析 ``` 围栏内的答案块，避免年份污染）
    ap = os.path.join(SRC, f"{year}-浙江预赛-答案.md")
    atext = io.open(ap, encoding="utf-8").read()
    ans = {}
    for fence in re.findall(r"```(.*?)```", atext, re.S):
        for tok in re.split(r"[\s　]+", fence.strip()):
            m = re.fullmatch(r"(\d{1,2})[．.、]?\s*([A-D]{1,4})(?:\(图\)|（图）)?[．.、]?", tok)
            if m:
                n = int(m.group(1))
                if 1 <= n <= 80:
                    ans[n] = m.group(2)
    # 清理题块（去掉尾部多余空行；分离图片行）
    out = []
    for n in order:
        body = "\n".join(blocks[n]).strip()
        figs = re.findall(r"!\[\[([^\]]+)\]\]", body)
        out.append({
            "num": n,
            "type": "单选" if n <= 60 else "多选",
            "body": body,
            "figs": figs,
            "answer": ans.get(n, ""),
        })
    return out

result = {}
for y in (2021, 2022, 2023):
    qs = parse_paper(y)
    result[str(y)] = qs
    print(y, len(qs), "题; 空答案:", [q["num"] for q in qs if not q["answer"]])

json.dump(result, io.open(os.path.join(OUT, "zj_split_source.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("saved zj_split_source.json")
