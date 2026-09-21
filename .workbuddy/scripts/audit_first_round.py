# -*- coding: utf-8 -*-
"""第一轮化学原理习题集机检 v2：兼容 题N/第N题 双模式 + emoji/星号难度"""
import re, os, glob, json

D = r"C:\Obsidion\妙妙屋\04-课件\习题集"
files = sorted(glob.glob(os.path.join(D, "第一轮化学原理*.md")))
MEDIA = r"C:\Obsidion\妙妙屋\媒体仓库"
media_set = set()
for root, dirs, fs in os.walk(MEDIA):
    for f in fs:
        media_set.add(os.path.splitext(f)[0])

QPAT = re.compile(r"^###\s*(题\s*\d+|第\d+题)\s*(.*?)(\[[^\]]*\])?\s*$", re.M)

report = {}
for fp in files:
    name = os.path.basename(fp)
    t = open(fp, encoding="utf-8", newline="").read()
    r = {"lines": t.count("\n") + 1}

    qs = list(QPAT.finditer(t))
    r["n_questions"] = len(qs)
    nums = [int(re.sub(r"\D", "", q.group(1))) for q in qs]
    r["first_num"] = nums[0] if nums else None
    r["num_gaps"] = [f"{nums[i]}->{nums[i+1]}" for i in range(len(nums)-1) if nums[i+1] != nums[i]+1]

    # 题头后缀（难度emoji/星号/位置码）
    deco = {}
    for q in qs:
        tail = (q.group(2) or "").strip()
        deco[tail] = deco.get(tail, 0) + 1
    r["deco_top"] = dict(sorted(deco.items(), key=lambda x: -x[1])[:10])
    # 位置码覆盖率（\d\d-\d\d 模式）
    r["with_loc_code"] = sum(1 for q in qs if re.search(r"\d{1,2}-\d{1,3}", q.group(2) or ""))

    # 来源标签
    tags = {}
    for q in qs:
        key = q.group(3) or "(无标签)"
        tags[key] = tags.get(key, 0) + 1
    r["tags"] = dict(sorted(tags.items(), key=lambda x: -x[1]))

    # 三段配对
    blocks = re.split(r"^### ", t, flags=re.M)[1:]
    miss_ti = miss_ans = miss_da = 0
    for b in blocks:
        if "**题目**" not in b and "**题干**" not in b:
            miss_ti += 1
        if "**参考答案**" not in b:
            miss_ans += 1
        if "**答" not in b:
            miss_da += 1
    r["no_timu"] = miss_ti
    r["no_cankao"] = miss_ans
    r["no_da"] = miss_da

    t2 = re.sub(r"\$\$.*?\$\$", "", t, flags=re.S)
    r["dollar_odd_lines"] = sum(1 for ln in t2.split("\n") if ln.count("$") % 2 == 1)
    r["half_math"] = len(re.findall(r"\$\^\{(?![^$]*\\)[^$]*\}\$|\$_\{(?![^$]*\\)[^$]*\}\$", t))
    r["xlongequal"] = t.count("xlongequal")
    r["bare_rightlef"] = len(re.findall(r"(?<!\\)\\rightleftharpoons", t))

    imgs = re.findall(r"!\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]", t)
    r["n_images"] = len(imgs)
    r["img_missing"] = [i.strip()[:60] for i in imgs if os.path.splitext(i.strip())[0] not in media_set]

    report[name] = r

print(json.dumps(report, ensure_ascii=False, indent=1))
