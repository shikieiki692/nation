import os, glob

files = glob.glob(r'c:\Obsidion\妙妙屋\04-课件\学生讲义\*.md')
count = 0
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    new_text = text.replace('<span class="claudian-embedded-image-fallback">', '')
    new_text = new_text.replace('</span>\n*图', '\n*图')
    
    if new_text != text:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_text)
        count += 1
        print(f'Fixed {os.path.basename(file)}')

print(f'Total files fixed: {count}')
