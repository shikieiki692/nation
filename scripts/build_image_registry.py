# -*- coding: utf-8 -*-
"""全库核心图谱总索引生成器 v3 (2026-08-04)

功能升级 (相对 v1):
1. 截断哈希修复: 源头 _index.md 中形如 `fff140...9b9f.jpg` 的截断名,
   通过全库"前缀 + 后缀"唯一匹配, 解析为完整哈希 (如 fff140a862...de9b9f.jpg)。
2. 失效条目剔除: 无法恢复的截断项 / 全库消失的哈希 / 垃圾值(未识别,HIGH 等) 不再入表,
   数量写入审计段。
3. 状态列: 每条目标注 `✅在媒体仓库` / `📁源目录`, 供三步搜图法判断 (Word 管线要求 in 媒体仓库)。
4. source_file 使用真实相对路径 (含 mineru/ 等前缀), 并新增 source_folder 供"所在图库"列展示。

用法: python scripts/build_image_registry.py
"""
import os
import re
import json
import datetime

vault_root = r'C:\Obsidion\妙妙屋'
ignore_dirs = {'.git', '.obsidian', '.trash', '.agents', '.kb', 'node_modules', '.claude'}
media_dir = os.path.join(vault_root, '媒体仓库')
index_dir = os.path.join(vault_root, '10-索引与统计')
output_md = os.path.join(index_dir, '全库核心图谱总索引.md')
output_json = os.path.join(index_dir, '全库核心图谱总索引.json')

IMAGE_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tif', '.tiff')


def is_image_name(name: str) -> bool:
    return name.lower().endswith(IMAGE_EXT)


def clean_phys(raw: str) -> str:
    """从单元格提取文件名: 处理 `![[hash.jpg]]`、`(hash.jpg)`、`media/hash.jpg`、纯名。"""
    name = raw.replace('![[', '').replace(']]', '').strip()
    m = re.search(r'([^/\\()]+\.(?:jpg|jpeg|png|gif|webp|bmp|tif|tiff))', name, re.IGNORECASE)
    return m.group(1) if m else name


def build_vault_image_index():
    """全库图片名集合 + 名称->首个源路径 映射 (跳过 .obsidian/ 之外的 ignore 目录)。"""
    all_names = set()
    name_to_source = {}
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for fn in files:
            if not is_image_name(fn):
                continue
            all_names.add(fn)
            if fn not in name_to_source:
                name_to_source[fn] = os.path.join(root, fn)
    return all_names, name_to_source


def media_names_set():
    """媒体仓库 中已有的图片名 (递归)。"""
    s = set()
    if os.path.isdir(media_dir):
        for root, _, files in os.walk(media_dir):
            for fn in files:
                s.add(fn)
    return s


def resolve_truncated(name, all_names_lower):
    """给定 `prefix...suffix.ext`, 返回唯一完整文件名; 无法唯一或不存在返回 None。"""
    m = re.match(r'^([0-9a-fA-F]+)\.\.\.([0-9a-fA-F]+)\.([a-zA-Z0-9]+)$', name)
    if not m:
        return None
    prefix, suffix, ext = m.group(1).lower(), m.group(2).lower(), m.group(3).lower()
    if not prefix or not suffix:
        return None
    matches = []
    for n in all_names_lower:
        if n.startswith(prefix) and n.endswith(suffix + '.' + ext):
            matches.append(n)
            if len(matches) > 1:
                return None
    return matches[0] if matches else None


def main():
    print("Building vault-wide image index...", flush=True)
    all_names, name_to_source = build_vault_image_index()
    all_names_lower = {n.lower() for n in all_names}
    media_names = media_names_set()
    media_names_lower = {n.lower() for n in media_names}
    print(f"  vault images: {len(all_names)}, media images: {len(media_names)}", flush=True)

    registry = []
    excluded = []  # {physical_filename, source_file, reason}
    seen = set()

    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        if '_index.md' not in files:
            continue
        filepath = os.path.join(root, '_index.md')
        rel_src = os.path.relpath(filepath, vault_root).replace('\\', '/')
        src_folder = os.path.basename(root).replace('_images', '').replace('images', '') or os.path.basename(root)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"  [WARN] read {rel_src}: {e}", flush=True)
            continue

        in_table = False
        headers = []
        for line in lines:
            line = line.strip()
            if not (line.startswith('|') and line.endswith('|')):
                continue
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if not in_table:
                if any(('文件名' in c or 'Quality' in c or '质量' in c) for c in cols):
                    in_table = True
                    headers = cols
                    continue
                continue
            # 分隔行
            if set(line.replace('|', '').replace('-', '').replace(' ', '')) == set():
                continue
            if len(cols) < 2:
                continue

            qual_idx = desc_idx = kp_idx = rename_idx = -1
            for i, h in enumerate(headers):
                if qual_idx < 0 and ('质量' in h or 'Quality' in h):
                    qual_idx = i
                if desc_idx < 0 and '内容描述' in h:
                    desc_idx = i
                if kp_idx < 0 and '关联KP' in h:
                    kp_idx = i
                if rename_idx < 0 and '建议重命名' in h:
                    rename_idx = i
            if qual_idx == -1 or qual_idx >= len(cols):
                continue
            if 'HIGH' not in cols[qual_idx].upper():
                continue

            raw = cols[0]
            phys = clean_phys(raw)
            if not is_image_name(phys):
                excluded.append({'physical_filename': phys, 'source_file': rel_src, 'reason': '非图片名/垃圾值'})
                continue

            resolved = phys
            if '...' in phys:
                full = resolve_truncated(phys, all_names_lower)
                if full:
                    resolved = full
                else:
                    excluded.append({'physical_filename': phys, 'source_file': rel_src, 'reason': '截断无法唯一恢复'})
                    continue

            if resolved.lower() not in all_names_lower:
                excluded.append({'physical_filename': phys, 'source_file': rel_src, 'reason': '全库无此文件'})
                continue

            desc = cols[desc_idx] if desc_idx != -1 and desc_idx < len(cols) else ''
            kp = cols[kp_idx] if kp_idx != -1 and kp_idx < len(cols) else ''
            rename = cols[rename_idx] if rename_idx != -1 and rename_idx < len(cols) else ''

            key = (resolved.lower(), desc, kp)
            if key in seen:
                continue
            seen.add(key)

            registry.append({
                'physical_filename': resolved,
                'description': desc,
                'semantic_alias': rename,
                'knowledge_points': kp,
                'source_file': rel_src,
                'source_folder': src_folder,
                'in_media': resolved.lower() in media_names_lower,
            })

    # 排序: 按所在图库, 再按哈希
    registry.sort(key=lambda x: (x['source_folder'], x['physical_filename'].lower()))

    # 审计统计
    n_in_media = sum(1 for r in registry if r['in_media'])
    n_src_only = len(registry) - n_in_media
    reasons = {}
    for e in excluded:
        reasons[e['reason']] = reasons.get(e['reason'], 0) + 1
    reason_str = '；'.join(f"{k} {v}" for k, v in sorted(reasons.items(), key=lambda x: -x[1]))

    with open(os.path.join(index_dir, 'excluded_dump.json'), 'w', encoding='utf-8') as f:
        json.dump(excluded, f, ensure_ascii=False, indent=2)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump({
            'meta': {
                'built_at': datetime.datetime.now().strftime('%Y-%m-%d'),
                'total': len(registry),
                'in_media': n_in_media,
                'source_only': n_src_only,
                'excluded_count': len(excluded),
                'excluded_reasons': reasons,
            },
            'registry': registry,
        }, f, ensure_ascii=False, indent=2)

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    md_content = f"""---
title: 全库核心图谱总索引
type: 索引
updated: {today}
---
# 全库核心图谱总索引 (Agent 搜图中心)

> [!IMPORTANT] Agent 搜图专用规范
> 1. 请使用 `grep_search` 搜索本文件（可搜索中文描述或英文特征码）。
> 2. 找到对应行后，**必须提取第一列的"物理哈希文件名"**（如 `fff140a862....jpg`），**禁止使用截断名或英文别名**。
> 3. 在讲义中严格按照 `![[物理哈希文件名]]` 的格式写入。
> 4. **状态列**：`✅在媒体仓库` 可直接用于 Word 管线；`📁源目录` 需先复制到 `媒体仓库/` 再引用。

> 📊 **审计 (v3, {today})**：共 **{len(registry)}** 条 HIGH 图 —— ✅在媒体仓库 {n_in_media} · 📁源目录 {n_src_only} · 剔除失效 {len(excluded)}（{reason_str}）。

| 物理哈希文件名 | 语义搜索特征码 (Agent专用) | 内容描述 | 关联KP | 所在图库 | 状态 |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for item in registry:
        status = '✅在媒体仓库' if item['in_media'] else '📁源目录'
        md_content += f"| {item['physical_filename']} | {item['semantic_alias']} | {item['description']} | {item['knowledge_points']} | {item['source_folder']} | {status} |\n"

    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"\nRegistry built: total={len(registry)} (media={n_in_media}, source_only={n_src_only}), excluded={len(excluded)}", flush=True)
    print(f"Excluded reasons: {reason_str}", flush=True)


if __name__ == '__main__':
    main()
