# -*- coding: utf-8 -*-
"""
真断链 vs 幻影断链 分类

背景：fix_body_redlinks_v4.py 算出 10 条"可机械折叠"的目标，但应用 0 处替换。
怀疑这些 target 根本没在正文里以 [[target 的形式出现过 —— 即"幻影断链"
（校验器自己推算出来的，或者来自 frontmatter / 报告文本）。

做法：
  1. 收集全库 md 文件名（basename，去 .md）集合 ALL_MD
  2. 收集所有正文里出现过的 [[xxx 链接目标 LINKED
  3. 断链集合 = LINKED - ALL_MD
  4. 对断链集合，再精确统计每个 target 在【哪些文件】里以 [[target 出现过
     - 出现文件里只要有一个不是 09-审计报告/auto-validation/* → 真断链
     - 全部都只在审计报告里 → 幻影断链
输出 JSON + 控制台摘要。
"""
import os, re, json, sys

VAULT = r"C:\Obsidion\妙妙屋"
EXCLUDE_DIRS = {".git", "node_modules", ".obsidian", ".trash", "__pycache__",
                ".workbuddy", ".kb", ".claudian", "11-模板/node_modules"}
REPORT_PREFIX = "09-审计报告/auto-validation/"

sys.stdout.reconfigure(encoding="utf-8")


def iter_md():
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f.endswith(".md"):
                yield os.path.join(root, f)


ALL_MD = set()
PATHS = []
for p in iter_md():
    PATHS.append(p)
    ALL_MD.add(os.path.splitext(os.path.basename(p))[0])

print(f"全库 md：{len(PATHS)}  basename unique：{len(ALL_MD)}")

LINK_RE = re.compile(r"\[\[([^\]\|#\^]+)")
occ = {}  # target -> list of (relpath, line_no)

for p in PATHS:
    rel = os.path.relpath(p, VAULT).replace("\\", "/")
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as fh:
            txt = fh.read()
    except Exception:
        continue
    for i, line in enumerate(txt.splitlines(), 1):
        for m in LINK_RE.finditer(line):
            t = m.group(1).strip().rstrip(".")
            if not t:
                continue
            occ.setdefault(t, []).append((rel, i))

print(f"正文链接目标 unique：{len(occ)}")

broken = {t: v for t, v in occ.items() if t not in ALL_MD}
print(f"正文断链 unique：{len(broken)}")

real, phantom = {}, {}
for t, hits in broken.items():
    src = [h for h in hits if not h[0].startswith(REPORT_PREFIX)]
    if src:
        real[t] = {"total": len(hits), "src": src[:5], "src_n": len(src)}
    else:
        phantom[t] = {"total": len(hits), "hits": hits[:3]}

print(f"\n真断链（正文确实有引用）：{len(real)}")
print(f"幻影断链（只在审计报告里出现）：{len(phantom)}")

print("\n--- 幻影断链前 30 条 ---")
for t, d in list(phantom.items())[:30]:
    print(f"  {t}  (出现 {d['total']} 次)  例：{d['hits'][0][0]}:{d['hits'][0][1]}")

out = {
    "all_md": len(ALL_MD),
    "linked": len(occ),
    "broken": len(broken),
    "real": {t: d for t, d in real.items()},
    "phantom": {t: d for t, d in phantom.items()},
}
with open(os.path.join(VAULT, ".workbuddy", "scripts", "real_vs_phantom.json"),
          "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)

print("\n已写出 real_vs_phantom.json")

# 另：断链按出现次数排序，便于抓"高频断链"
top = sorted(broken.items(), key=lambda kv: -len(kv[1]))[:25]
print("\n--- 出现次数最多的 25 条断链 ---")
for t, hits in top:
    srcn = len([h for h in hits if not h[0].startswith(REPORT_PREFIX)])
    print(f"  {len(hits):4d} 次 (正文 {srcn:3d})  {t}")
