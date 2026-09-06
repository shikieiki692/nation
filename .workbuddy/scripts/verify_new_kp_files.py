"""逐个校验新建的 4 个知识点文件里的所有 wikilink：
   OK  → 解析到非题目类文件
   BAD → 解析到题目/真题类文件（静默吸题）
   NEW → 解析不到（新断链）
"""
import os, sys, re

VAULT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(VAULT, "11-模板", "scripts"))
import validate_kb as V

FILES = [
    r"03-知识点\综合\水合物.md",
    r"03-知识点\无机和结构化学\水解反应.md",
    r"03-知识点\有机化学\Appel反应.md",
    r"03-知识点\有机化学\Kolbe电解.md",
]
LINK = re.compile(r"\[\[([^\]]+)\]\]")
FM = re.compile(r"^---\s*\n(.*?)\n---", re.S)


def ftype(p):
    raw = p.read_text(encoding="utf-8", errors="ignore")[:2000]
    m2 = FM.search(raw)
    if not m2:
        return "?"
    m3 = re.search(r"^type:\s*(.+?)\s*$", m2.group(1), re.M)
    return m3.group(1).strip() if m3 else ""


total = {"ok": 0, "bad": 0, "new": 0}
for rel in FILES:
    p = os.path.join(VAULT, rel)
    if not os.path.exists(p):
        print(f"!!! 文件不存在: {rel}")
        continue
    raw = open(p, encoding="utf-8").read()
    m = FM.match(raw)
    split = m.end() if m else 0
    body = raw[split:]
    targets = []
    for mo in LINK.finditer(body):
        t = mo.group(1).split("|")[0].strip()
        if t:
            targets.append(t)
    uniq = sorted(set(targets))
    print(f"\n=== {rel}  （正文链接 {len(targets)} 处 / unique {len(uniq)}） ===")
    for t in uniq:
        if V.is_placeholder_target(t):
            continue
        tgt = V.find_wikilink_target(t, V.VAULT_ROOT)
        if tgt is None:
            total["new"] += 1
            print(f"  NEW  [[{t}]]")
            continue
        rel2 = tgt.relative_to(V.VAULT_ROOT).as_posix()
        ty = ftype(tgt)
        if ty in V.QB_TYPES:
            total["bad"] += 1
            print(f"  BAD  [[{t}]] → {rel2}  (type={ty})")
        else:
            total["ok"] += 1
            print(f"  OK   [[{t}]] → {rel2}  (type={ty or '—'})")

print("\n" + "=" * 50)
print(f"汇总: OK {total['ok']} / BAD {total['bad']} / NEW {total['new']}")
