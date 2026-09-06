import os

# Only the specific emojis actually used in these files
# Using str.replace() which is completely safe - no regex risk
EMOJIS = [
    '⭐', '✅', '❌', '⚠️', '⚠', '✔️', '✔',
    '📝', '💡', '🧠', '📌', '🔗', '📋', '🗣️', '🗣',
    '🧪', '🔑', '🎯', '🔬', '💪', '🎓',
    '⭐️', '‼️', '‼', '❗', '💯', '🔥',
    '✨', '🌟', '💫', '💬', '🔔', '📢',
    '🚫', '⛔', '🔄', '📊', '📐', '📖',
    '💎', '💥', '💣', '🚩', '🏷️', '🏷',
    '⚛️', '⚛', '🌊', '🌈', '🚀',
    '🤔', '🙂', '😊', '👋', '👍',
    '🎨', '🎬', '🎭', '🥁',
]

vault = r'C:\Obsidion\妙妙屋'
files = [
    r'04-课件\学生讲义\原子结构-超级充实版（自学完整）.md',
    r'04-课件\学生讲义\元素周期表与周期律-超级充实版（自学完整）.md',
    r'04-课件\学生讲义\分子结构基础-超级充实版（自学完整）.md',
    r'04-课件\学生讲义\晶体学与晶体结构-超级充实版（自学完整）.md',
    r'04-课件\学生讲义\配位化合物基础-超级充实版（自学完整）.md',
]

for f in files:
    full = os.path.join(vault, f)
    with open(full, 'r', encoding='utf-8') as fh:
        content = fh.read()

    # Count emojis before
    count = 0
    for emoji in EMOJIS:
        count += content.count(emoji)

    # Remove emojis using simple str.replace
    new_content = content
    for emoji in EMOJIS:
        new_content = new_content.replace(emoji, '')

    # Clean double spaces (emoji + space pattern)
    import re
    new_content = re.sub(r'  +', ' ', new_content)
    # Clean trailing spaces on lines
    new_content = re.sub(r' +\n', '\n', new_content)

    with open(full, 'w', encoding='utf-8') as fh:
        fh.write(new_content)

    name = os.path.basename(f)
    print(f'{name}: {count} emoji removed')
