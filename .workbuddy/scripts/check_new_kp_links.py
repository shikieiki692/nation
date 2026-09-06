"""校验即将写入 4 个新知识点文件的 wikilink 目标：
   1. 文件名是否已被占用（basename 冲突会让 Level-2 解析歧义）
   2. 每个候选链接目标解析到哪、被解析成什么 type
   OK  = 解析到知识点/专题/题型类文件
   BAD = 解析到题目/真题文件（静默吸题，不能用）
   NEW = 解析不到（会成为新断链，不能用）
"""
import os, sys, re

VAULT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(VAULT, "11-模板", "scripts"))
import validate_kb as V

QB_TYPES = V.QB_TYPES
GOOD_TYPES = {"知识点", "专题", "题型", "教学洞察", "概念", "术语", "卡片", ""}

# 1. 文件名冲突检查
import subprocess
NEW_FILES = ["水合物", "水解反应", "Appel反应", "Kolbe电解"]
print("=== 1. 新建文件名冲突检查 ===")
for n in NEW_FILES:
    r = subprocess.run(["git", "-c", "core.quotepath=false", "ls-files",
                        f"*{n}.md"], cwd=VAULT, capture_output=True, text=True)
    hits = [x for x in r.stdout.splitlines() if x.endswith(f"{n}.md")]
    # 精确 basename
    exact = [x for x in hits if os.path.basename(x) == f"{n}.md"]
    print(f"  {n}.md → {'⚠ 已存在 ' + str(exact) if exact else '✅ 无冲突'}")

# 2. 链接目标校验
CAND = {
    "水合物": ["羰基亲核加成", "醛酮", "半缩醛", "缩醛", "亲核加成", "硼氢化钠还原",
               "亲核体与亲电体", "空间位阻", "配位化合物", "氢键", "结晶水",
               "硫酸", "氧化还原反应", "化学平衡", "酸碱催化", "茚三酮"],
    "水解反应": ["酸碱理论", "离子极化", "氧化还原反应", "配位化合物",
                 "高价金属氟化物水解", "三价铬水解", "化学平衡", "溶度积",
                 "亲核取代", "羧酸衍生物", "盐类水解", "卤化氢前体"],
    "Appel反应": ["亲核取代", "SN2反应", "Mitsunobu反应", "离去基与pKa",
                  "Walden翻转", "卤代烷", "醇的氧化", "三苯基膦", "膦化合物",
                  "亲核体与亲电体", "构型翻转", "Swern氧化"],
    "Kolbe电解": ["自由基", "Wurtz偶联", "电化学", "电解", "羧酸", "偶联反应",
                  "单电子反应", "Grignard试剂", "电极电势", "氧化还原反应",
                  "脱羧", "自由基偶联"],
}


def ftype(p):
    try:
        raw = p.read_text(encoding="utf-8", errors="ignore")[:2000]
    except Exception:
        return "?"
    m = None
    # 取 frontmatter 里的 type
    fm = re.search(r"^---\s*\n(.*?)\n---", raw, re.S)
    if fm:
        m = re.search(r"^type:\s*(.+?)\s*$", fm.group(1), re.M)
    return m.group(1).strip() if m else ""


print("\n=== 2. 链接目标校验 ===")
verdict = {}
for owner, cands in CAND.items():
    print(f"\n--- {owner} ---")
    ok, bad, new = [], [], []
    for t in cands:
        tgt = V.find_wikilink_target(t, V.VAULT_ROOT)
        if tgt is None:
            new.append(t)
            print(f"  NEW  [[{t}]]  （无此文件 → 会成新断链）")
            continue
        rel = tgt.relative_to(V.VAULT_ROOT).as_posix()
        ty = ftype(tgt)
        if ty in QB_TYPES:
            bad.append(t)
            print(f"  BAD  [[{t}]] → {rel}  (type={ty})  ← 静默吸题！")
        else:
            ok.append(t)
            print(f"  OK   [[{t}]] → {rel}  (type={ty or '—'})")
    verdict[owner] = {"ok": ok, "bad": bad, "new": new}

print("\n=== 汇总（只能写 OK 的） ===")
for k, v in verdict.items():
    print(f"{k}: OK {len(v['ok'])} / BAD {len(v['bad'])} / NEW {len(v['new'])}")
    if v["bad"]:
        print("   BAD:", "、".join(v["bad"]))
    if v["new"]:
        print("   NEW:", "、".join(v["new"]))
