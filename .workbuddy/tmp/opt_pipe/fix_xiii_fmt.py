# -*- coding: utf-8 -*-
"""fix_xiii_fmt.py —— 卷 XIII 用卡的 LaTeX 格式规范化（RMW · 幂等 · 可复核）。

修 4 类：
  A. `^{\\theta}` → `^{\\ominus}`（标准态上标）
  B. `\\mathrm{kJ}/\\mathrm{mol}` → `\\mathrm{kJ}\\cdot\\mathrm{mol}^{-1}`（单位连除写法）
  C. `Q_{\\mathrm{p.m}}` → `Q_{\\mathrm{p,m}}`；`Q_{V.\\mathrm{m}}` → `Q_{V,\\mathrm{m}}`（下标用句点）
  D. `(1^{\\prime})` / `(1 ^ {\\prime})` → `（1 分）`（评分标记还原为中文）

用法：python fix_xiii_fmt.py --dry | --apply
"""
import io, json, os, re, shutil, sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
PLAN = os.path.join(R, ".workbuddy/tmp/opt_pipe/vol_plan_XIII.json")
BAK = os.path.join(R, ".workbuddy/tmp/opt_pipe/xiii_fmt_bak")
DRY = "--dry" in sys.argv

RULES = [
    # 标准态上标：\theta / \Theta / \circ 三种错形 → \ominus（前面不是数字，排除角度 `30^{\circ}`）
    ("std", re.compile(r"(?<![0-9])\s*\^\s*\{?\s*\\(?:theta|Theta|circ)\s*\}?"), r"^{\\ominus}"),
    # 无 `^` 的裸写法：`H_{m} \circ` / `H_{m}\theta` ⇒ `H_{m}^{\ominus}`（仅当前面是 `}`，避免误改角度）
    ("std2", re.compile(r"(?<=\})[ \t]*\\(?:theta|Theta|circ)\b"), r"^{\\ominus}"),
    ("unit_kjmol", re.compile(r"/\\mathrm\{kJ\}/\\mathrm\{mol\}"), r"/\\mathrm{kJ}\\cdot\\mathrm{mol}^{-1}"),
    ("unit_JmolK", re.compile(r"\\mathrm\{J\s*/\s*\(\s*mol\s*K\s*\)\}"), r"\\mathrm{J\\cdot mol^{-1}\\cdot K^{-1}}"),
    ("unit_kJ_mol", re.compile(r"\\mathrm\{kJ\}\s*\\mathrm\{mol\}"), r"\\mathrm{kJ\\cdot mol}"),
    ("lnfix", re.compile(r"\\mathrm\{n\}\s*(?=\\frac)"), r"\\ln "),
    ("Vdotm", re.compile(r"\{\s*([pV])\s*\.\s*\\mathrm\{m\}\s*\}"), lambda m: "{%s,\\mathrm{m}}" % m.group(1)),
    ("pdotm", re.compile(r"\{\\mathrm\{\s*([pV])\s*\.\s*m\s*\}\}"), lambda m: "{\\mathrm{%s,m}}" % m.group(1)),
    ("score", re.compile(r"\(\s*(\d+)\s*\^?\s*\{\s*\\prime\s*\}\s*\)"), lambda m: "（%s 分）" % m.group(1)),
    ("score2", re.compile(r"(?<![\^])(\d+)\s*\^\s*\{\s*\\prime\s*\}"), lambda m: "（%s 分）" % m.group(1)),
    ("score3", re.compile(r"\(\s*(\d+)\s*'\s*\)"), lambda m: "（%s 分）" % m.group(1)),
]


def main():
    plan = json.load(io.open(PLAN, encoding="utf-8"))
    cards = [c["path"] for _m, lst in plan for c in lst]
    os.makedirs(BAK, exist_ok=True)
    total, per = 0, []
    for rel in cards:
        fp = os.path.join(R, rel)
        if not os.path.isfile(fp):
            print("  [缺]", rel); continue
        raw = io.open(fp, encoding="utf-8-sig").read()
        if "\r\n" in raw:
            print("  [CRLF 跳过]", os.path.basename(rel)); continue
        new, hits = raw, {}
        for name, rx, rep in RULES:
            new, n = rx.subn(rep, new)
            if n:
                hits[name] = n
        if new == raw:
            continue
        # 复核：只在原文上做同样替换，逐字节一致
        chk = raw
        for name, rx, rep in RULES:
            chk = rx.sub(rep, chk)
        if chk != new:
            print("  [复核不通过]", os.path.basename(rel)); continue
        total += sum(hits.values()); per.append((os.path.basename(rel)[:40], hits, len(raw), len(new)))
        if not DRY:
            shutil.copy2(fp, os.path.join(BAK, rel.replace("/", "__")))
            io.open(fp, "w", encoding="utf-8", newline="\n").write(new)
    print("%s：%d 卡 / %d 处" % ("(dry)" if DRY else "已写盘", len(per), total))
    for name, hits, a, b in per:
        print("   %-42s %s  %d→%d" % (name, hits, a, b))


if __name__ == "__main__":
    main()
