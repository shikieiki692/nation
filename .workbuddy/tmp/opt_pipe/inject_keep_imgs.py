# -*- coding: utf-8 -*-
"""把「被误删的真图」按最小改动补回卷 md（学生版 + 答案版）。

- 只补 `noise_keep.json` 里的图（＝已逐张目检确认为**真内容**）。
- 题面图：按卡内「图前一段」原文定位插入点（插在该段之后）。
- 答案图：优先插在含「详见随卷解图」的解析行之后；否则插在答案段末尾。

用法：python inject_keep_imgs.py            # dry（只打印计划）
      python inject_keep_imgs.py --apply
"""
import io, json, os, re, sys

R = r"C:\Obsidion\妙妙屋"
QB = os.path.join(R, "04-题库")
PLAN = os.path.join(R, ".workbuddy", "tmp", "opt_pipe")
sys.stdout.reconfigure(encoding="utf-8")

TITLE = re.compile(r"^### 第 (\d+) 题（", re.M)
IMG_MD = re.compile(r"!\[\]\(images/([^)\s]+)\)")
IMG_EMBED = re.compile(r"!\[\[([^\]\|\\]+)")

KEEP = set(json.load(open(os.path.join(PLAN, "noise_keep.json"), encoding="utf-8")))


def segs(md):
    idx = [m.start() for m in TITLE.finditer(md)] + [len(md)]
    out = {}
    for a, b in zip(idx, idx[1:]):
        out[int(TITLE.match(md[a:b]).group(1))] = (a, b)
    return out


def card_parts(path):
    t = io.open(os.path.join(R, path), encoding="utf-8-sig").read()
    front = t.split("\n## 参考答案")[0]
    rest = t.split("\n## 参考答案", 1)[1] if "\n## 参考答案" in t else ""
    ans = rest.split("\n## 知识点映射")[0]
    return front, ans


def img_ctx_front(front, h):
    """返回卡内该图**紧邻的前一段**（去掉行首空行）。"""
    lines = front.split("\n")
    for i, l in enumerate(lines):
        if l.strip() == "![](images/%s)" % h or ("images/" + h) in l:
            j = i - 1
            while j >= 0 and not lines[j].strip():
                j -= 1
            return lines[j].strip() if j >= 0 else None
    return None


def plan_vol(v):
    p = json.load(open(os.path.join(PLAN, "vol_plan_%s.json" % v), encoding="utf-8"))
    return [c["path"] for _m, l in p for c in l]


def run(apply_):
    total = 0
    for v in ("X", "XIp", "XI"):
        stu_p = os.path.join(QB, "初赛模拟卷%s（非有机·学生版）.md" % v)
        ans_p = os.path.join(QB, "初赛模拟卷%s（非有机·答案版）.md" % v)
        stu = io.open(stu_p, encoding="utf-8-sig").read().replace("\r\n", "\n")
        ans = io.open(ans_p, encoding="utf-8-sig").read().replace("\r\n", "\n")
        sg_s, sg_a = segs(stu), segs(ans)
        cards = plan_vol(v)
        jobs = []   # (target, 题, hash, kind, prev_text)
        for i, path in enumerate(cards, 1):
            front, cardans = card_parts(path)
            fwant = list(dict.fromkeys(IMG_MD.findall(front)))      # 保卡内顺序
            awant = list(dict.fromkeys(IMG_MD.findall(cardans)))
            a, b = sg_s.get(i, (None, None))
            if a is None:
                continue
            got_s = set(IMG_EMBED.findall(stu[a:b]))
            got_a = set(IMG_EMBED.findall(ans[sg_a[i][0]:sg_a[i][1]]))
            for h in fwant:
                if h not in got_s and h in KEEP:
                    jobs.append(("stu", i, h, "front", img_ctx_front(front, h)))
            for h in awant:
                if h not in got_a and h in KEEP:
                    jobs.append(("ans", i, h, "answer", None))
        print("=" * 78)
        print("卷 %s：待补 %d 张" % (v, len(jobs)))
        for tgt, i, h, kind, prev in jobs:
            tag = "题面" if kind == "front" else "答案"
            hint = ""
            if kind == "answer":
                a, b = sg_a[i]
                hint = "｜随卷解图锚" if "详见随卷解图" in ans[a:b] else "｜答案段末尾"
            print("   %-4s 题%-3d %s  %s%s" % (tag, i, h[:20], (("｜锚: " + prev[-30:]) if prev else ""), hint))
            if not apply_:
                continue
            img = "![[%s]]" % h
            if kind == "front":
                if prev:
                    key = prev[-36:]
                    a, b = sg_s[i]
                    k = stu.find(key, a, b)
                    if k < 0:
                        print("      !! 锚未命中（学生版），跳过"); continue
                    eol = stu.find("\n", k)
                    stu = stu[:eol] + "\n\n" + img + "\n" + stu[eol:]
                    sg_s = segs(stu)
                    a2, b2 = sg_a[i]
                    k2 = ans.find(key, a2, b2)
                    if k2 >= 0:
                        e2 = ans.find("\n", k2)
                        ans = ans[:e2] + "\n\n" + img + "\n" + ans[e2:]
                        sg_a = segs(ans)
                else:
                    a, b = sg_s[i]
                    stu = stu[:a] + img + "\n\n" + stu[a:]
                    sg_s = segs(stu)
            else:
                a, b = sg_a[i]
                k = ans.find("详见随卷解图", a, b)
                if k >= 0:
                    eol = ans.find("\n", k)
                    ans = ans[:eol] + "\n\n" + img + "\n" + ans[eol:]
                else:
                    cut = ans.rfind("\n---", a, b)
                    cut = b if cut < 0 else cut
                    ans = ans[:cut] + "\n" + img + "\n" + ans[cut:]
                sg_a = segs(ans)
            total += 1
        if apply_:
            io.open(stu_p, "w", encoding="utf-8", newline="\n").write(stu)
            io.open(ans_p, "w", encoding="utf-8", newline="\n").write(ans)
    print("=" * 78)
    print("已补 %d 张（apply=%s）" % (total, apply_))


run("--apply" in sys.argv)
