#!/usr/bin/env python3
"""Fix Excalidraw JSON files: trailing commas → valid JSON, then re-render to PNG."""
import json, re, os, subprocess, sys

media_dir = r"C:\Obsidion\妙妙屋\media"
script_dir = r"C:\Obsidion\妙妙屋\11-模板\scripts"

files = [
    "第二周期MO能级对比.关系图.md",
    "分子间力三层递进.关系图.md",
    "高低自旋判断决策树.决策图.md",
    "光谱化学序列配体排序图.关系图.md",
    "配合物异构现象分类体系.关系图.md",
    "CFSE计算流程.流程图.md",
]

def fix_trailing_commas(json_str):
    """Remove trailing commas before ] or } that cause JSON parsing issues."""
    # Remove trailing comma before }
    json_str = re.sub(r',\s*}', ' }', json_str)
    # Remove trailing comma before ]
    json_str = re.sub(r',\s*]', ' ]', json_str)
    # Also catch "value",} → "value" }
    json_str = re.sub(r'"\s*,\s*}', '" }', json_str)
    json_str = re.sub(r'(\d+)\s*,\s*}', r'\1 }', json_str)
    json_str = re.sub(r'(true|false|null)\s*,\s*}', r'\1 }', json_str)
    return json_str

for fname in files:
    fpath = os.path.join(media_dir, fname)
    if not os.path.exists(fpath):
        print(f"NOT FOUND: {fname}")
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find JSON block
    m = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
    if not m:
        print(f"NO JSON: {fname}")
        continue

    raw_json = m.group(1)

    # Step 1: Try to parse as-is
    try:
        parsed = json.loads(raw_json)
        print(f"OK (clean): {fname}")
    except json.JSONDecodeError:
        # Step 2: Fix trailing commas
        fixed_json_str = fix_trailing_commas(raw_json)
        try:
            parsed = json.loads(fixed_json_str)
            print(f"OK (fixed): {fname}")
            # Write back fixed JSON
            pretty = json.dumps(parsed, indent=2, ensure_ascii=False)
            new_content = content[:m.start(1)] + pretty + content[m.end(1):]
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except json.JSONDecodeError as e:
            print(f"STILL BROKEN: {fname} - {e}")
            continue

    # Step 3: Render to PNG via node
    png_path = os.path.join(media_dir, fname.replace('.md', '.png'))
    result = subprocess.run(
        ["node", "excalidraw-to-png.mjs", fpath, png_path],
        cwd=script_dir, capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        size = os.path.getsize(png_path) if os.path.exists(png_path) else 0
        print(f"  PNG OK: {os.path.basename(png_path)} ({size//1024}KB)")
    else:
        print(f"  PNG FAIL: {result.stderr.strip()}")
