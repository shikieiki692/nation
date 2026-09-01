import sys, os, re
sys.path.insert(0, r'C:\Obsidion\妙妙屋\11-模板\scripts')
from convert_handout_to_pdf import preprint

files = [
    r'C:\Obsidion\妙妙屋\04-课件\学生讲义\分子结构基础-超级充实版（自学完整）.md',
    r'C:\Obsidion\妙妙屋\04-课件\学生讲义\元素周期表与周期律-超级充实版（自学完整）.md',
    r'C:\Obsidion\妙妙屋\04-课件\学生讲义\晶体学与晶体结构-超级充实版（自学完整）.md',
]
for f in files:
    with open(f, encoding='utf-8') as fh:
        src = fh.read()
    out = preprint(src)
    fname = os.path.basename(f)
    corrupted = [l for l in out.splitlines() if '$_{' in l and ('media/' in l or '.jpg' in l or '.png' in l)]
    img_refs = re.findall(r'!\[.*?\]\((media/[^\)]+)\)', out)
    bad_imgs = [i for i in img_refs if '$' in i]
    print(f'{fname}:')
    print(f'  Images: {len(img_refs)} total, {len(bad_imgs)} corrupted')
    print(f'  Lines: {len(src.splitlines())} -> {len(out.splitlines())}')
    if corrupted:
        for l in corrupted[:3]:
            print(f'  CORRUPTED: {l[:100]}')
    else:
        print(f'  All clean!')
