# -*- coding: utf-8 -*-
"""
阶段七 v4：题号-断链【机械折叠】（v2 的正确版）

v2 的错：一直折叠直到找到"某个"存在的文件 → 嫦娥石 被错位到 晶胞。

v4 的规则（严格）：
  链接目标形如  `题-NNN-...-数字-描述`
  去掉【最后一层 `-数字-`】，得到  `题-NNN-...-描述`
  —— 当且仅当 该结果【确实存在】时，才替换。
  只做一层，不递归。找不到就跳过（留红链）。

  例：
    题-036b-1-1-铝铁合金制备方程式  → 题-036b-1-铝铁合金制备方程式   ✓ 存在 → 替换
    题-036b-7-1-1-晶胞中化学式数目n  → 题-036b-7-1-晶胞中化学式数目n   ✓ 存在 → 替换
    题-036b-7-2-1-嫦娥石化学式      → 题-036b-7-2-嫦娥石化学式       ✗ 不存在 → 跳过
    题-037-1-2-Ga低价碘化物结构     → 题-037-1-Ga低价碘化物结构      ✗ 不存在 → 跳过

铁律：
  1. 只折叠一层，不递归（不落到错误父题）。
  2. 折叠结果必须在全库 md basename 集合中。
  3. 排除 09-审计报告/auto-validation/（v2 教训：报告自身不能成为修复对象）。
  4. 保守：找不到就跳过。
  5. 不动 frontmatter（用户原话：frontmatter 断链先不用管）。
"""
import os, re, json

VAULT = r"C:\Obsidion\妙妙屋"
LOG = os.path.join(VAULT, ".workbuddy", "scripts", "fix_body_redlinks_v4.log")
JSON_OUT = os.path.join(VAULT, ".workbuddy", "scripts", "fix_body_redlinks_v4.json")

# ---------- 1. 收集全库 md basename ----------
def collect_all_md():
    s = set()
    for r, ds, fs in os.walk(VAULT):
        if any(p in {".git", "node_modules", ".obsidian", ".trash", "__pycache__"}
               for p in r.split(os.sep)):
            continue
        if r.startswith(os.path.join(VAULT, "09-审计报告", "auto-validation")):
            continue
        for f in fs:
            if f.endswith(".md"):
                s.add(f[:-3])
    return s

ALL_MD = collect_all_md()
print(f"全库 md basename：{len(ALL_MD)}")

# ---------- 2. 解析校验报告取断链 target ----------
REP = os.path.join(VAULT, "09-审计报告", "auto-validation", "2026-09-01-validation.md")
text = open(REP, encoding="utf-8").read()
hits = re.findall(r"→ \[\[([^\]]+)\]\]", text)

targets = []
seen = set()
for h in hits:
    t = h.split("|")[0].rsplit("/", 1)[-1]
    if t in seen:
        continue
    seen.add(t)
    targets.append(t)
print(f"断链 unique target：{len(targets)}")

# ---------- 3. 严格一层折叠 ----------
# 形如 题-...-数字-描述 ，去掉最后一个 -数字-
STRICT = re.compile(r"^(题-\d+\w*(?:-\d+)*)-(\d+)-(.+)$")

plan = []
for t in targets:
    if not t.startswith("题-"):
        continue
    m = STRICT.match(t)
    if not m:
        continue
    collapsed = f"{m.group(1)}-{m.group(3)}"
    # 只接受一层折叠且结果存在
    if collapsed in ALL_MD:
        plan.append((t, collapsed))

print(f"\n可机械折叠（去掉一层子号后确实存在）：{len(plan)} 条")
for o, n in plan:
    print(f"  {o}")
    print(f"    → {n}")
# 记录被跳过的（信息用）
skipped = [t for t in targets if t.startswith("题-") and STRICT.match(t)
           and f"{STRICT.match(t).group(1)}-{STRICT.match(t).group(3)}" not in ALL_MD]
print(f"\n跳过（折叠后不存在）：{len(skipped)} 条 —— 留红链")

# ---------- 4. 应用 ----------
def is_excluded(p):
    rel = os.path.relpath(p, VAULT).replace("\\", "/")
    return (rel.startswith("09-审计报告/auto-validation")
            or rel.startswith(".workbuddy/")
            or rel.startswith(".git/"))

log_lines = []
changes = []
for r, ds, fs in os.walk(VAULT):
    if any(p in {".git", "node_modules", ".obsidian", ".trash", "__pycache__"}
           for p in r.split(os.sep)):
        continue
    for f in fs:
        if not f.endswith(".md"):
            continue
        p = os.path.join(r, f)
        if is_excluded(p):
            continue
        try:
            t = open(p, "r", encoding="utf-8", newline="").read()
        except Exception as e:
            log_lines.append(f"FAIL read {p}: {e}")
            continue
        new_t = t
        file_changes = []
        for old, new in plan:
            pat = re.compile(rf"\[\[{re.escape(old)}(\|[^\]]*)?\]\]")
            found = pat.findall(new_t)
            if found:
                new_t = pat.sub(f"[[{new}\\1]]", new_t)
                file_changes.append((old, new, len(found)))
        if new_t != t:
            with open(p, "w", encoding="utf-8", newline="") as fp:
                fp.write(new_t)
            for old, new, n in file_changes:
                rel = os.path.relpath(p, VAULT)
                log_lines.append(f"{rel}\t{n}×\t[[{old}]] → [[{new}]]")
                changes.append({"file": rel, "old": old, "new": new, "count": n})

open(LOG, "w", encoding="utf-8").write("\n".join(log_lines))
json.dump({"plan": plan, "skipped": skipped, "changes": changes},
          open(JSON_OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n应用 {len(changes)} 处替换，改 {len(set(c['file'] for c in changes))} 个文件")
