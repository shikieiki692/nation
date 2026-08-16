import json, os

with open('missing_placeholders.json', 'r', encoding='utf-8') as f:
    missing = json.load(f)

remaining = []
for m in missing:
    md_path = m['file']
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '📌 **图片待补' in content and m['full_match'] in content:
                remaining.append(m)
    except: pass

out_md = []
out_md.append("# 剩余待绘图 / 纯排版清单")
out_md.append("以下为经全域 OCR 检索后，确实无教材来源扫描原图的剩余待补占位符。多数为总结性逻辑导图或纯版式说明。")
out_md.append("")

for r in remaining:
    out_md.append(f"- **文件**: [[{r['basename']}]]")
    out_md.append(f"  - **内容**: {r['desc']}")
    out_md.append(f"  - **原文**: `{r['full_match']}`\n")

out_path = r'c:\Obsidion\妙妙屋\00-首页\活跃任务\图片剩余待手绘清单.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(out_md))

print(f"Recorded {len(remaining)} remaining images to {out_path}")
