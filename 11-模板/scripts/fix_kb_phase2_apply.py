#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_kb_phase2_apply.py — 执行知识点断链修复（只做人工核定过的映射）

动作（仅对题目类文件）：
  1. knowledge_points 中 CURATED 映射：[[幽灵名]] → [[人工核定 KP]]
  2. knowledge_points 中 DELETE_SET（技能型标签）：删除条目（删除后必须仍有 ≥1 个 KP）
  3. Ch12 复制粘贴簇：按题名重派
  4. cross_references / depends_on / related 中 STALE_XREF：删除或改指
  5. 改动的文件 updated 置为今天

安全机制：写入前全量备份；行级手术不重排其他 frontmatter 字段；--dry 预览。
注意：词面自动匹配已弃用（抽查错误率过高），D 类断链保持原样。
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8")
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_kb as VKB
from fix_kb_phase2_map import CURATED, DELETE_SET, CH12_REASSIGN, STALE_XREF, strip_fm

V = VKB.VAULT_ROOT
BACKUP = V / "09-审计报告" / "备份" / "题库修复-2026-08-31"
MANIFEST = BACKUP / "manifest.jsonl"
TARGETS = ["04-题库", "05-真题库"]
SKIP = {".obsidian", "node_modules", "09-AI工作区"}
QT = {"题目", "真题", "例题", "题目集", "题组"}
TODAY = datetime.date.today().isoformat()

# Ch12 簇的 9 个幽灵标签名
CH12_NAMES = ["BeCl2导电性", "BeCl2成键", "锂镁相似性", "铍铝相似性", "钾的制备",
              "炼镁冷却剂", "黑火药", "卤化物生成热", "镁溶解性"]

# 校验映射目标都真实存在
def verify_targets() -> list[str]:
    stems = {f.stem for f in (V / "03-知识点").rglob("*.md")}
    bad = [f"{k}→{v}" for k, v in CURATED.items() if v not in stems]
    return bad


def kp_names(item: str) -> list[str]:
    return [x.strip() for x in re.findall(r"\[\[([^\]|#]+)", item)]


def transform_kp_list(items: list, stem: str, stats: dict, log: list) -> tuple[list, bool]:
    """返回 (新列表, 是否有变化)。items 为 yaml 解析后的列表。"""
    flat: list[str] = []
    for it in items:
        if isinstance(it, str):
            flat.append(it)
        elif isinstance(it, list):
            flat.extend(str(x) for x in it)

    ch12_key = next((k for k in CH12_REASSIGN if stem.startswith(k)), None)

    out: list[str] = []
    changed = False
    for it in flat:
        names = kp_names(it)
        if not names:
            out.append(it)
            continue
        name = names[0]

        # Ch12 簇：9 个幽灵标签一律移除（随后按题名重派）
        if ch12_key and name in CH12_NAMES:
            changed = True
            stats["ch12移除"] += 1
            log.append(f"Ch12移除 {name}")
            continue

        if name in CURATED:
            tgt = CURATED[name]
            changed = True
            stats["映射"] += 1
            log.append(f"映射 {name}→{tgt}")
            out.append(f"[[{tgt}]]")
            continue

        if name in DELETE_SET:
            changed = True
            stats["待删"] += 1
            log.append(f"待删 {name}")
            continue  # 先移除，末尾检查剩余数量

        out.append(it)

    # Ch12 重派：追加题名对应的 KP
    if ch12_key:
        for kp in CH12_REASSIGN[ch12_key]:
            tgt = CURATED.get(kp, kp)
            if f"[[{tgt}]]" not in out:
                out.append(f"[[{tgt}]]")
                changed = True
                stats["ch12重派"] += 1
                log.append(f"Ch12重派 +{tgt}")

    # 技能标签删除后必须仍有 KP
    if "待删" in stats and len(out) == 0:
        # 全部被删光 → 回滚删除项
        log.append("回滚：删除后将无 KP，保留原条目")
        stats["待删"] = 0
        return flat, False

    # 去重（保序）
    seen = set()
    dedup = []
    for x in out:
        if x not in seen:
            seen.add(x)
            dedup.append(x)
    if len(dedup) != len(out):
        changed = True
        stats["去重"] += 1
    return dedup, changed


def transform_xref_items(items: list, stats: dict, log: list) -> tuple[list, bool]:
    out = []
    changed = False
    for it in items:
        if not isinstance(it, str):
            out.append(it)
            continue
        names = kp_names(it)
        hit = next((n for n in names if n in STALE_XREF), None)
        if hit is None:
            # 兼容不带 .md 的匹配
            hit = next((n for n in names if n.rstrip(".md") in STALE_XREF
                        or any(n.startswith(k) for k in STALE_XREF)), None)
        if hit is None:
            out.append(it)
            continue
        key = next((k for k in STALE_XREF if hit == k or hit.startswith(k)), None)
        if key is None:
            out.append(it)
            continue
        tgt = STALE_XREF[key]
        changed = True
        if tgt is None:
            stats["xref删除"] += 1
            log.append(f"xref删除 {key}")
            continue
        rest = it.split("|", 1)
        new = f"[[{tgt}]]" + (f"|{rest[1]}" if len(rest) > 1 else "")
        stats["xref改指"] += 1
        log.append(f"xref改指 {key}→{tgt}")
        out.append(new)
    return out, changed


def edit_frontmatter(text: str, stem: str, stats: dict, log: list) -> str:
    """行级手术：只改 knowledge_points / cross_references / depends_on / related / updated。"""
    local = defaultdict(int)   # 每文件独立计数，只有真实改动才 bump updated
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end < 0:
        return text
    block = text[3:end]
    body = text[end:]

    lines = block.split("\n")
    out_lines: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\w[\w_-]*):\s*(.*)$", line)
        if not m:
            out_lines.append(line)
            i += 1
            continue
        key, inline = m.group(1), m.group(2).strip()

        if key in ("knowledge_points", "cross_references", "depends_on", "related"):
            items: list = []
            consumed = 1
            if inline:
                try:
                    parsed = yaml.safe_load(inline)
                    items = parsed if isinstance(parsed, list) else ([parsed] if parsed else [])
                except Exception:
                    out_lines.append(line)
                    i += 1
                    continue
            else:
                j = i + 1
                while j < len(lines) and re.match(r"^\s*-\s+", lines[j]):
                    items.append(yaml.safe_load(lines[j].strip()[2:]))
                    j += 1
                consumed = j - i

            if key == "knowledge_points":
                new_items, changed = transform_kp_list(items, stem, local, log)
            else:
                new_items, changed = transform_xref_items(items, local, log)

            if changed and new_items:
                out_lines.append(f"{key}: [" + ", ".join(
                    '"' + str(x).replace('"', "'") + '"' for x in new_items) + "]")
            elif changed and not new_items:
                # 列表被清空：knowledge_points 不允许为空 → 保留原样
                for k in range(consumed):
                    out_lines.append(lines[i + k] if k == 0 else lines[i + k])
                log.append(f"{key} 清空被拒绝，保留原样")
            else:
                for k in range(consumed):
                    out_lines.append(lines[i + k])
            i += consumed
            continue

        if key == "updated" and local:
            out_lines.append(f"updated: {TODAY}")
            i += 1
            continue

        out_lines.append(line)
        i += 1

    return "---" + "\n".join(out_lines) + body


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    bad = verify_targets()
    if bad:
        print("❌ 以下映射目标不存在，中止：", bad)
        sys.exit(1)

    stats = defaultdict(int)
    touched: list[tuple[Path, str, str, bytes]] = []

    for d in TARGETS:
        for f in sorted((V / d).rglob("*.md")):
            if set(f.relative_to(V).parts) & SKIP:
                continue
            raw = f.read_bytes()
            text = raw.decode("utf-8", errors="replace")
            fm, _ = strip_fm(text)
            if str(fm.get("type", "")).strip() not in QT:
                continue

            log: list = []
            new_text = edit_frontmatter(text, f.stem, stats, log)
            if new_text != text:
                touched.append((f, f.relative_to(V).as_posix(), new_text, raw))
                print(f"  {f.name}: {'; '.join(log[:4])}{' …' if len(log) > 4 else ''}")

    print(f"\n📊 {'预览' if args.dry else '执行'}：{len(touched)} 文件")
    for k in sorted(stats):
        print(f"  {stats[k]:5d}  {k}")

    if not args.dry:
        for f, rel, new_text, raw in touched:
            dst = BACKUP / rel
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(raw)
            f.write_bytes(new_text.encode("utf-8"))
            with open(MANIFEST, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"file": rel, "actions": [{"action": "KP断链修复", "detail": 1}]},
                                    ensure_ascii=False) + "\n")
        print(f"💾 备份: {BACKUP}")


if __name__ == "__main__":
    main()
