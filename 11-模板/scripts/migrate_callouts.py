import os
import re
from pathlib import Path

# Mapping dictionaries
# Note: keys are the possible legacy label strings found in the Markdown
MAPPING = {
    # Tip
    '理解要点': 'tip', '记忆': 'tip', '关键认识': 'tip', '掌握性要求': 'tip',
    # Warning
    '易错点': 'warning', '易错提醒': 'warning', '注意': 'warning', '高频错误': 'warning',
    # Info
    '教学洞察': 'info', '核心思想': 'info', '物理直觉': 'info', '竞赛启示': 'info', '数值冲击': 'info', '应用': 'info',
    # Example
    '练一练': 'example', '算一算': 'example',
    # Teacher
    '教师原话': 'teacher', '课堂原话': 'teacher', '备课思路': 'teacher', '纯私密备注': 'teacher'
}

STANDARD_TITLE = {
    'tip': '理解要点',
    'warning': '易错提醒',
    'info': '深入思考',
    'example': '练一练',
    'teacher': '备课备注'
}

# Regex to match a callout line:
# Optional emoji from the known list
# Optional bold markers
# The label text
CALLOUT_EMOJIS = r'[🧠🗣️⚠️💡⚡🔥📝🌟✅🔗]'
# Pattern: > (optional emoji) (optional **) (label) (optional **) (: or ：) (optional text)
# E.g. > 🧠 **教学洞察**：内容
pattern = re.compile(
    r'^>\s*'                                   # > and spaces
    r'(?:' + CALLOUT_EMOJIS + r'\s*)?'         # Optional emoji
    r'(?:\*\*)?'                               # Optional bold
    r'(' + '|'.join(MAPPING.keys()) + r')'     # Label text
    r'(?:\*\*)?'                               # Optional bold
    r'[:：]?\s*'                                # Optional colon
    r'(.*)$',                                  # The rest of the line
    flags=re.MULTILINE
)

def process_file(filepath: Path) -> int:
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0

    if not pattern.search(content):
        return 0

    def repl(m: re.Match) -> str:
        label = m.group(1)
        rest = m.group(2).strip()
        
        callout_type = MAPPING.get(label)
        if not callout_type:
            return m.group(0) # fallback
            
        std_title = STANDARD_TITLE[callout_type]
        
        if rest:
            return f"> [!{callout_type}] {std_title}\n> {rest}"
        else:
            return f"> [!{callout_type}] {std_title}"

    new_content = pattern.sub(repl, content)

    if new_content != content:
        filepath.write_text(new_content, encoding='utf-8')
        print(f"Updated {filepath.name}")
        return 1
    return 0

def main():
    base_dir = Path(r"C:\Obsidion\妙妙屋\04-课件\学生讲义")
    if not base_dir.exists():
        print(f"Error: {base_dir} not found")
        return

    count = 0
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.md'):
                count += process_file(Path(root) / f)
                
    print(f"\nMigration complete! Updated {count} files.")

if __name__ == '__main__':
    main()
