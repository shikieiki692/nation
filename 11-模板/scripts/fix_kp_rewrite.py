# -*- coding: utf-8 -*-
"""
断链名 → 已有 KP 映射执行（2026-08-31 批次2前置）
原则：不新建 KP，断链名改写到 03-知识点 已有 KP（人工审核 + 手补，来源标注）
执行范围：04-题库/05-真题库 题目类文件的 knowledge_points（及其他链接字段）内匹配名改写
安全：--dry 预览；写盘前备份到 09-审计报告/备份/质量修正-2026-08-31 同目录新子目录
"""
import argparse, json, re, sys, datetime
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, '11-模板/scripts')
import audit_question_bank as A
import validate_kb as VKB

VAULT = A.VAULT
BACKUP = VAULT / "09-审计报告" / "备份" / "质量修正-2026-08-31" / "KP断链改指"
TODAY = datetime.date.today().isoformat()

# ── 审核后映射表（断链名 → 已有 KP；来源：script=脚本词面匹配+人工审核，manual=手补）──
MAPPING = {
    # 手补（用户点名/词面不匹配但语义明确）
    "Ksp计算": "溶度积",
    "分子质量": "气体分子量测定",
    "混合气体": "理想气体",
    "阿伏伽德罗常数": "物质的量与气体计算",
    # 脚本匹配 + 人工审核采纳
    "第一电离能": "电离能",
    "弱酸Ka": "弱酸",
    "混合弱酸": "弱酸",
    "量子数规则": "量子数",
    "晶系判断": "七大晶系",
    "碘量法滴定": "碘量法",
    "双核配合物": "配合物",
    "三元环中间体": "中间体",
    "2+2": "2+2环加成",
    "热力学稳定性": "热力学",
    "四氧化三铅": "铅",
    "三氯化铋水解": "铋",
    "氧化银": "银",
    "卤素歧化反应": "卤素",
    "卤素化合物推断": "卤素",
    "硫化亚铁": "铁",
    "硅酸盐结构": "硅",
    "硅的反应": "硅",
    "羟汞化反应": "汞",
    "价态分析": "价态-氧化态-形式电荷",
    "pH影响": "pH",
}
# 排除的误报/弱候选（不执行）：氢卤酸酸性→氢、硫化氢沉淀→氢、定性分析→稳定性系列、
# 亚硫酸钠→钠、气体鉴别、化合物性质、稳定性比较、选择性、晶体性质、几何计算（语义过泛）

# 校验目标 KP 存在（全库解析：basename/路径/别名）
MISSING = [v for v in MAPPING.values() if VKB.find_wikilink_target(v, VKB.VAULT_ROOT) is None]
if MISSING:
    print("❌ 映射目标不存在，中止：", MISSING)
    sys.exit(1)

FIELDS = ["knowledge_points", "depends_on", "cross_references", "related"]
QT = {"题目", "真题", "例题", "题目集", "题组"}

def rewrite(text: str, stats: dict, log: list) -> str:
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end < 0:
        return text
    block = text[3:end]
    body = text[end:]
    lines = block.split("\n")
    out = []
    changed = False
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\w[\w_-]*):\s*(.*)$", line)
        if not m or m.group(1) not in FIELDS:
            out.append(line)
            i += 1
            continue
        key, inline = m.group(1), m.group(2).strip()
        # 收集该字段全部文本（inline 或块列表），做纯文本链接替换（保留原格式）
        if inline:
            field_text = inline
            consumed = 1
        else:
            j = i + 1
            lines2 = []
            while j < len(lines) and re.match(r"^\s*-\s+", lines[j]):
                lines2.append(lines[j].strip()[2:])
                j += 1
            field_text = ", ".join(lines2)
            consumed = j - i
        new_field = field_text
        field_changed = False
        for k, v in MAPPING.items():
            old_ref = f"[[{k}]]"
            if old_ref in new_field:
                new_field = new_field.replace(old_ref, f"[[{v}]]")
                field_changed = True
                changed = True
                stats["改写"] += 1
                log.append(f"{k}→{v}")
        if field_changed:
            if inline:
                out.append(f"{key}: {new_field}")
            else:
                # 块列表：每个条目一行
                items = [x.strip() for x in new_field.split(",") if x.strip()]
                out.append(f"{key}:")
                for it in items:
                    out.append(f"  - {it}")
        else:
            out.extend(lines[i:i + consumed])
        i += consumed
    if changed:
        # updated 置今天（若存在）
        for k, l in enumerate(out):
            mm = re.match(r"^(updated):\s*(.*)$", l)
            if mm:
                out[k] = f"updated: {TODAY}"
    return "---" + "\n".join(out) + body

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    stats = defaultdict(int)
    touched = []
    for root in ("04-题库", "05-真题库"):
        for f in sorted((VAULT / root).rglob("*.md")):
            rel = f.relative_to(VAULT).as_posix()
            raw = f.read_text(encoding="utf-8")
            fm, _ = A.strip_fm(raw)
            if str(fm.get("type", "")).strip() not in QT:
                continue
            log = []
            new = rewrite(raw, stats, log)
            if new != raw:
                touched.append((f, rel, new, raw))
                print(f"  {f.name[:40]}: {'; '.join(log[:3])}{' …' if len(log) > 3 else ''}")
    print(f"\n📊 {'预览' if args.dry else '执行'}：{len(touched)} 文件 | 改写 {stats['改写']} 处")
    if not args.dry:
        BACKUP.mkdir(parents=True, exist_ok=True)
        import time
        for f, rel, new, raw in touched:
            dst = BACKUP / rel
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(raw.encode("utf-8"))
            for attempt in range(4):
                try:
                    f.write_text(new, encoding="utf-8")
                    break
                except OSError:
                    if attempt == 3:
                        raise
                    time.sleep(0.6)
        print(f"💾 备份: {BACKUP}")

if __name__ == "__main__":
    main()
