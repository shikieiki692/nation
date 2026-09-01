# -*- coding: utf-8 -*-
"""终极对账：当前红链全集 vs HEAD，新增条目归类"""
import sys, re, subprocess
sys.path.insert(0, r"C:\Obsidion\妙妙屋\11-模板\scripts")
from pathlib import Path
import validate_kb as vk

ROOT = vk.VAULT_ROOT

def fm_reds(text):
    fm, _ = vk.parse_frontmatter(text)
    out = set()
    if not isinstance(fm, dict):
        return out
    for field in vk.QB_LINK_FIELDS:
        vals = fm.get(field)
        if isinstance(vals, str):
            vals = [vals]
        if not isinstance(vals, list):
            continue
        for v in vals:
            if not isinstance(v, str):
                continue
            for tgt in re.findall(r"(?<!\!)\[\[([^\]|#]+)", v):
                tgt = tgt.strip()
                if not tgt or vk.is_placeholder_target(tgt):
                    continue
                if Path(tgt).suffix.lower() in {".png",".jpg",".jpeg",".gif",".webp",".svg"}:
                    continue
                if vk.find_wikilink_target(tgt, ROOT) is None:
                    out.add((field, tgt))
    return out

# 当前全集
cur = {}
for p in vk.collect_md_files(ROOT, vk.INCLUDE_DIRS):
    rel = p.relative_to(ROOT).as_posix()
    cur[rel] = fm_reds(p.read_text(encoding="utf-8"))
total_now = sum(len(s) for s in cur.values())
print("NOW TOTAL:", total_now)

# HEAD 全集：未改动文件与当前相同，仅对 git 改动文件重算
changed = [e for e in subprocess.run(["git", "status", "--porcelain", "-z"], cwd=str(ROOT),
                                     capture_output=True).stdout.decode("utf-8", "replace").split("\0") if e]
changed_paths = set()
for e in changed:
    st, path = e[:2], e[3:].strip()
    if st.strip() in ("M", "A") and path.endswith(".md"):
        changed_paths.add(path.strip('"'))
head = {}
for rel, s in cur.items():
    if rel in changed_paths:
        r = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=str(ROOT), capture_output=True)
        text = r.stdout.decode("utf-8", "replace") if r.returncode == 0 else ""
        head[rel] = fm_reds(text) if text else set()
    else:
        head[rel] = s
total_head = sum(len(s) for s in head.values())
print("HEAD TOTAL:", total_head, "(changed md:", len(changed_paths), ")")

added, removed = [], []
for rel in cur:
    for item in cur[rel] - head.get(rel, set()):
        added.append((rel,)+item)
    for item in head.get(rel, set()) - cur[rel]:
        removed.append((rel,)+item)
print(f"\n新增 {len(added)} 条:")
for rel, f, t in added:
    print(f"  + {rel} [{f}] {t}")
print(f"\n消失 {len(removed)} 条:")
for rel, f, t in removed:
    print(f"  - {rel} [{f}] {t}")
