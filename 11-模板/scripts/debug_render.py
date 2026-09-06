#!/usr/bin/env python3
"""Debug Excalidraw rendering by checking JSON and node output."""
import json, re, subprocess, os, sys

media_dir = r"C:\Obsidion\妙妙屋\media"
script_dir = r"C:\Obsidion\妙妙屋\11-模板\scripts"

fname = sys.argv[1] if len(sys.argv) > 1 else "第二周期MO能级对比.关系图.md"
fpath = os.path.join(media_dir, fname)

with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

# Validate JSON first
m = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
if not m:
    print("NO JSON BLOCK FOUND")
    sys.exit(1)

raw = m.group(1)
try:
    parsed = json.loads(raw)
    print(f"✅ JSON valid: {len(raw)} chars, {len(parsed.get('elements',[]))} elements")
except json.JSONDecodeError as e:
    print(f"❌ JSON INVALID: {e}")
    sys.exit(1)

# Run node render
png_path = os.path.join(media_dir, fname.replace('.md', '.png'))
result = subprocess.run(
    ["node", "excalidraw-to-png.mjs", fpath, png_path],
    cwd=script_dir, capture_output=True, text=True, timeout=30
)
print(f"STDOUT: {result.stdout.strip()}")
if result.stderr:
    print(f"STDERR: {result.stderr.strip()}")
print(f"EXIT: {result.returncode}")

if os.path.exists(png_path):
    size = os.path.getsize(png_path)
    print(f"✅ PNG created: {size} bytes")
else:
    print("❌ PNG NOT CREATED")
