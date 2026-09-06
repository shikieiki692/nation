"""把 kp_links_to_questions.json 里的 316 个目标分流：
   A 类「显式指题」——target 本身就是该 md 的文件名（Level-2 basename 命中），是设计意图，不动。
   B 类「静默吸题」——target 是概念词，靠 Level-3 title/aliases 兜底才连到题目文件上，
                      校验器看不见（不算断链），但读者点进去是道题而不是知识点——隐性错误。
"""
import json, os, sys

VAULT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(VAULT, "11-模板", "scripts"))
import validate_kb as V

data = json.load(open(os.path.join(VAULT, ".workbuddy", "scripts",
                                   "kp_links_to_questions.json"), encoding="utf-8"))

# 惰性构建 basename 索引
if V._FILENAME_INDEX is None:
    V._FILENAME_INDEX = V.build_filename_index(V.VAULT_ROOT)
IDX = V._FILENAME_INDEX

explicit, silent = {}, {}
for t, hits in data.items():
    pure = t.split("|")[0].strip()
    base = pure.split("/")[-1].lower()
    if base.endswith(".md"):
        base = base[:-3]
    if base in IDX:
        # 还要确认命中的就是那个题目文件本身
        cands = {p.relative_to(V.VAULT_ROOT).as_posix() for p in IDX[base]}
        if hits[0]["target"] in cands:
            explicit[t] = hits
            continue
    silent[t] = hits

print(f"A 类 显式指题（文件名命中，正常）：{len(explicit)} 目标 / "
      f"{sum(len(v) for v in explicit.values())} 引用")
print(f"B 类 静默吸题（title/aliases 兜底，隐性错误）：{len(silent)} 目标 / "
      f"{sum(len(v) for v in silent.values())} 引用")

print("\n=== B 类 静默吸题（按引用次数） ===")
for t, hits in sorted(silent.items(), key=lambda kv: -len(kv[1])):
    tg = hits[0]["target"]
    print(f"\n[{len(hits):2d}] [[{t}]] → {tg}  (type={hits[0]['type']})")
    for h in hits[:6]:
        print(f"        ← {h['src']}:{h['line']}")
    if len(hits) > 6:
        print(f"        … 另 {len(hits)-6} 处")

out = {"explicit": explicit, "silent": silent}
json.dump(out, open(os.path.join(VAULT, ".workbuddy", "scripts",
                                 "kp_mislink_split.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\n已写出 kp_mislink_split.json")
