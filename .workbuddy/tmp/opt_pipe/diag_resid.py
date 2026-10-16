# -*- coding: utf-8 -*-
"""通用残余 ④-e 诊断：对指定卷，打印**每个缺图题**的 源卡图(名+内容sha) vs 卷内图。"""
import io, os, re, hashlib, json, sys, glob

R = r"C:\Obsidion\妙妙屋"
IMG = re.compile(r"!\[\[([^\]]+)\]\]")
IMG_MD = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
IMG_HTML = re.compile(r'<img[^>]*\bsrc\s*=\s*["\']([^"\']+)["\']', re.I)
IMG_DIRS = glob.glob(os.path.join(R, "04-题库", "**", "images"), recursive=True)
KEEP = {}
try:
    KEEP = {k: v for k, v in json.load(io.open(os.path.join(R, ".workbuddy", "scripts", "figcov_keep.json"),
                                                encoding="utf-8")).items() if not k.startswith("_")}
except Exception:
    pass


def clean(n):
    return re.split(r"\\?\|", n, maxsplit=1)[0].strip()


def find(name):
    b = os.path.basename(clean(name))
    for d in IMG_DIRS:
        p = os.path.join(d, b)
        if os.path.isfile(p):
            return p
    return None


def ck(name):
    p = find(name)
    if not p:
        return None
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]


def in_keep(name):
    b = os.path.basename(clean(name))
    if any(b.startswith(k) and len(k) >= 8 for k in KEEP):
        return True
    c = ck(name) or ""
    return any(c and (k.startswith(c) or c.startswith(k[:12])) for k in KEEP if len(k) >= 8)


def imgs(t):
    return [clean(x) for x in IMG.findall(t) + IMG_MD.findall(t) + IMG_HTML.findall(t)]


def run(vol):
    O = os.path.join(R, ".workbuddy", "tmp", "opt_pipe")
    pl = json.load(io.open(os.path.join(O, "vol_plan_%s.json" % vol), encoding="utf-8"))
    cards = []
    for g, items in pl:
        for it in items:
            cards.append(it.get("path"))
    # 卷内并集
    volmap = {}
    for tag in ("学生版", "答案版"):
        p = os.path.join(R, "04-题库", "初赛模拟卷%s（非有机·%s）.md" % (vol, tag))
        if not os.path.isfile(p):
            p = os.path.join(R, "04-题库", "初赛模拟卷%s（有机·%s）.md" % (vol, tag))
        if not os.path.isfile(p):
            continue
        d = io.open(p, encoding="utf-8-sig").read()
        parts = re.split(r"(?m)^### 第 (\d+) 题", d)
        for i in range(1, len(parts), 2):
            volmap.setdefault(int(parts[i]), [])
            volmap[int(parts[i])].extend(imgs(parts[i + 1]))
    for n, cpath in enumerate(cards, 1):
        card = io.open(os.path.join(R, cpath), encoding="utf-8-sig").read()
        ci = [x for x in imgs(card) if not in_keep(x)]
        vs = volmap.get(n, [])
        vol_h = {ck(x) for x in vs}
        missing = [x for x in ci if ck(x) not in vol_h]
        if missing:
            print("=" * 88)
            print("卷 %s 第 %d 题 ｜ 卡 %s ｜ 卷内 %d 图" % (vol, n, os.path.basename(cpath)[:44], len(vs)))
            for x in dict.fromkeys(missing):
                print("   缺: %-26s sha=%s" % (os.path.basename(x)[:26], ck(x)))
            for x in vs:
                print("   卷: %-26s sha=%s" % (os.path.basename(x)[:26], ck(x)))


for v in sys.argv[1:]:
    run(v)
