"""同步 media 目录图片到 chem_media ASCII 临时目录"""
import os, shutil

media = r'C:\Obsidion\妙妙屋\media'
temp = r'C:\Users\蕾赛\AppData\Local\Temp\chem_media'

# 原子结构讲义引用的所有图片
needed = {
    'atomic_radius_trend.jpg': True,
    'first_ionization_energy_trend.jpg': True,
    'electronegativity_table.jpg': True,
    '轨道杂化类型对比.关系图.png': True,
    'effective_nuclear_charge.png': True,
    'hydrogen_spectrum.svg': True,
    'hydrogen_transitions.svg': True,
}

copied = 0
missing = 0
for name in needed:
    src = os.path.join(media, name)
    dst = os.path.join(temp, name)
    if os.path.exists(src):
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f'  COPY: {name}')
            copied += 1
        else:
            print(f'  OK:   {name}')
    else:
        print(f'  MISS: {name}')
        missing += 1

print(f'\n复制了 {copied} 张, 缺失 {missing} 张')
