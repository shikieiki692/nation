# -*- coding: utf-8 -*-
"""H 类命中（卡答案图未进答案版）逐张归类：人工噪点清单 / 规则判噪 / 无理由。"""
import glob, io, json, os, re, sys
sys.path.insert(0, r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe")
import build_org as BO
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(ROOT, "04-题库")
IMG_MD = re.compile(r"!\[\]\(images/([^)\s]+)\)")
IMG_EMBED = re.compile(r"!\[\[([^\]\|\\]+)")
TITLE = re.compile(r"^### 第 (\d+) 题（", re.M)

manual = BO.load_noise()
keep = BO.load_keep()

vols = ["X", "XIp", "XI", "XII", "XIII"]
for v in vols:
    plan = json.load(open(os.path.join(ROOT, ".workbuddy/tmp/opt_pipe", "vol_plan_%s.json" % v), encoding="utf-8"))
    cards = [c["path"] for _m, l in plan for c in l]
    ans = io.open(os.path.join(QB, "初赛模拟卷%s（非有机·答案版）.md" % v), encoding="utf-8-sig").read()
    idx = [m.start() for m in TITLE.finditer(ans)] + [len(ans)]
    segs = [ans[a:b] for a, b in zip(idx, idx[1:])]
    for i, path in enumerate(cards):
        t = io.open(os.path.join(ROOT, path), encoding="utf-8-sig").read()
        if "\n## 参考答案" not in t:
            continue
        seg = t.split("\n## 参考答案", 1)[1].split("\n## 知识点映射")[0]
        got = set(IMG_EMBED.findall(segs[i])) if i < len(segs) else set()
        for h in sorted(set(IMG_MD.findall(seg)) - got):
            g = glob.glob(os.path.join(ROOT, "04-题库/**/" + h), recursive=True)
            p = g[0] if g else None
            tag = ("MANUAL" if h in manual else "") + (" KEEP" if h in keep else "")
            reason = BO.noise_of(p) if p else "文件不存在"
            print("卷%-4s 题%-3d %-22s %s" % (v, i + 1, h[:20], (reason or "⚠ 无判噪理由") + tag))
