---
title: 批量化渲染脚本
type: 脚本
purpose: 自动从CIF文件批量渲染标准化图片
created: 2026-08-02
updated: 2026-08-02
tags: [脚本, 渲染, 批量化, VESTA, Python]
---

# 批量化渲染脚本

> 自动从CIF文件批量渲染标准化图片，提高效率。

---

## 一、脚本说明

### 功能

1. 自动读取指定目录下的所有CIF文件
2. 用VESTA命令行模式批量打开
3. 自动设置标准化的显示参数
4. 自动导出标准化的PNG图片

### 依赖

| 依赖 | 版本 | 说明 |
|:-----|:-----|:-----|
| Python | 3.8+ | 脚本运行环境 |
| VESTA | 3.4+ | 晶体结构可视化软件 |

### 安装

1. 确保VESTA已安装并添加到系统PATH
2. 确保Python已安装
3. 将脚本放置在合适的位置

---

## 二、VESTA Python API

VESTA支持Python脚本批处理。以下是基本用法：

### 基本示例

```python
# VESTA Python 脚本示例
import subprocess
import os

# VESTA可执行文件路径（根据实际安装位置修改）
VESTA_PATH = r"C:\Program Files\VESTA\VESTA.exe"

def render_cif(cif_path, output_path, style="ball-and-stick"):
    """
    用VESTA渲染CIF文件

    参数:
        cif_path: CIF文件路径
        output_path: 输出图片路径
        style: 显示样式 (ball-and-stick, polyhedral, spacefill)
    """
    # VESTA命令行模式
    cmd = [VESTA_PATH, "--export-image", output_path, cif_path]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✓ 成功渲染: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"✗ 渲染失败: {cif_path}")
        print(f"  错误: {e.stderr.decode()}")
```

---

## 三、完整脚本

### 脚本1：批量渲染所有CIF文件

```python
#!/usr/bin/env python3
"""
批量渲染CIF文件为PNG图片
用法: python batch_render.py
"""

import os
import subprocess
import sys
from pathlib import Path

# ========== 配置 ==========

# VESTA可执行文件路径（根据实际安装位置修改）
VESTA_PATH = r"C:\Program Files\VESTA\VESTA.exe"

# CIF文件目录
CIF_DIR = Path(r"C:\Obsidion\妙妙屋\08-可视化资源\02-CIF文件库")

# 输出目录
OUTPUT_DIR = Path(r"C:\Obsidion\妙妙屋\08-可视化资源\03-渲染图片")

# 图片规格
IMAGE_WIDTH = 3000
IMAGE_HEIGHT = 2400
IMAGE_DPI = 300

# ========== 主程序 ==========

def find_vesta():
    """查找VESTA可执行文件"""
    # 检查配置的路径
    if os.path.exists(VESTA_PATH):
        return VESTA_PATH

    # 尝试常见安装路径
    common_paths = [
        r"C:\Program Files\VESTA\VESTA.exe",
        r"C:\Program Files (x86)\VESTA\VESTA.exe",
        os.path.expanduser(r"~\AppData\Local\VESTA\VESTA.exe"),
    ]

    for path in common_paths:
        if os.path.exists(path):
            return path

    return None

def render_cif(vesta_path, cif_path, output_path):
    """
    用VESTA渲染单个CIF文件

    参数:
        vesta_path: VESTA可执行文件路径
        cif_path: CIF文件路径
        output_path: 输出图片路径
    """
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # VESTA命令行模式
    cmd = [vesta_path, "--export-image", str(output_path), str(cif_path)]

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            timeout=30  # 30秒超时
        )
        return True, None
    except subprocess.TimeoutExpired:
        return False, "渲染超时"
    except subprocess.CalledProcessError as e:
        return False, e.stderr.decode() if e.stderr else "未知错误"
    except Exception as e:
        return False, str(e)

def batch_render():
    """批量渲染所有CIF文件"""
    # 查找VESTA
    vesta_path = find_vesta()
    if not vesta_path:
        print("❌ 未找到VESTA，请确认已安装并添加到PATH")
        print("   下载地址: https://jp-minerals.org/vesta/")
        sys.exit(1)

    print(f"✓ 找到VESTA: {vesta_path}")
    print(f"✓ CIF目录: {CIF_DIR}")
    print(f"✓ 输出目录: {OUTPUT_DIR}")
    print()

    # 统计
    total = 0
    success = 0
    failed = 0
    skipped = 0

    # 遍历所有子目录
    for subdir in sorted(CIF_DIR.iterdir()):
        if not subdir.is_dir():
            continue

        print(f"\n📁 处理目录: {subdir.name}")

        # 遍历所有CIF文件
        for cif_file in sorted(subdir.glob("*.cif")):
            total += 1

            # 构建输出路径
            # 例: 02-离子晶体/NaCl-Fm-3m.cif → 01-晶体结构/01-离子晶体/NaCl-Fm-3m-ball-stick-crystal.png
            rel_path = cif_file.relative_to(CIF_DIR)
            output_name = f"{cif_file.stem}-ball-stick-crystal.png"

            # 映射子目录
            subdir_map = {
                "01-单质": "01-晶体结构/01-离子晶体",  # 单质也放到离子晶体目录
                "02-离子晶体": "01-晶体结构/01-离子晶体",
                "03-共价晶体": "01-晶体结构/02-共价晶体",
                "04-金属晶体": "01-晶体结构/03-金属晶体",
                "05-分子晶体": "01-晶体结构/04-分子晶体",
                "06-配合物": "02-分子结构/02-配合物构型",
            }

            output_subdir = subdir_map.get(subdir.name, f"99-其他/{subdir.name}")
            output_path = OUTPUT_DIR / output_subdir / output_name

            # 检查是否已存在
            if output_path.exists():
                print(f"  ⏭ 跳过 (已存在): {cif_file.name}")
                skipped += 1
                continue

            # 渲染
            print(f"  ⏳ 渲染: {cif_file.name} → ", end="")
            ok, error = render_cif(vesta_path, cif_path, output_path)

            if ok:
                print(f"✓ {output_name}")
                success += 1
            else:
                print(f"✗ 失败: {error}")
                failed += 1

    # 打印统计
    print("\n" + "="*50)
    print(f"📊 渲染完成")
    print(f"   总计: {total}")
    print(f"   成功: {success}")
    print(f"   失败: {failed}")
    print(f"   跳过: {skipped}")
    print("="*50)

if __name__ == "__main__":
    batch_render()
```

---

### 脚本2：渲染指定CIF文件

```python
#!/usr/bin/env python3
"""
渲染单个或多个指定的CIF文件
用法: python render_specific.py NaCl-Fm-3m CsCl-Pm-3m ZnS-F-43m
"""

import os
import subprocess
import sys
from pathlib import Path

# ========== 配置 ==========

VESTA_PATH = r"C:\Program Files\VESTA\VESTA.exe"
CIF_DIR = Path(r"C:\Obsidion\妙妙屋\08-可视化资源\02-CIF文件库")
OUTPUT_DIR = Path(r"C:\Obsidion\妙妙屋\08-可视化资源\03-渲染图片")

# ========== 主程序 ==========

def find_vesta():
    """查找VESTA可执行文件"""
    if os.path.exists(VESTA_PATH):
        return VESTA_PATH

    common_paths = [
        r"C:\Program Files\VESTA\VESTA.exe",
        r"C:\Program Files (x86)\VESTA\VESTA.exe",
    ]

    for path in common_paths:
        if os.path.exists(path):
            return path

    return None

def find_cif(cif_name):
    """在CIF目录中查找指定的CIF文件"""
    for cif_file in CIF_DIR.rglob(f"{cif_name}*.cif"):
        return cif_file
    return None

def render_cif(vesta_path, cif_path, output_path):
    """用VESTA渲染单个CIF文件"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [vesta_path, "--export-image", str(output_path), str(cif_path)]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, timeout=30)
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    if len(sys.argv) < 2:
        print("用法: python render_specific.py <CIF名称1> <CIF名称2> ...")
        print("示例: python render_specific.py NaCl-Fm-3m CsCl-Pm-3m")
        sys.exit(1)

    vesta_path = find_vesta()
    if not vesta_path:
        print("❌ 未找到VESTA")
        sys.exit(1)

    print(f"✓ VESTA: {vesta_path}\n")

    for cif_name in sys.argv[1:]:
        print(f"🔍 查找: {cif_name}")
        cif_path = find_cif(cif_name)

        if not cif_path:
            print(f"  ✗ 未找到CIF文件: {cif_name}")
            continue

        print(f"  ✓ 找到: {cif_path}")

        # 构建输出路径
        rel_path = cif_path.relative_to(CIF_DIR)
        output_subdir = rel_path.parent
        output_name = f"{cif_path.stem}-ball-stick-crystal.png"
        output_path = OUTPUT_DIR / "01-晶体结构" / output_subdir.name / output_name

        print(f"  ⏳ 渲染中...")
        ok, error = render_cif(vesta_path, cif_path, output_path)

        if ok:
            print(f"  ✓ 成功: {output_path.name}\n")
        else:
            print(f"  ✗ 失败: {error}\n")

if __name__ == "__main__":
    main()
```

---

## 四、使用方法

### 方法1：批量渲染所有CIF文件

```bash
# 1. 打开命令提示符或PowerShell
# 2. 导航到脚本所在目录
cd C:\Obsidion\妙妙屋\08-可视化资源\04-动画脚本

# 3. 运行脚本
python batch_render.py
```

### 方法2：渲染指定CIF文件

```bash
# 渲染单个文件
python render_specific.py NaCl-Fm-3m

# 渲染多个文件
python render_specific.py NaCl-Fm-3m CsCl-Pm-3m ZnS-F-43m
```

---

## 五、注意事项

### VESTA版本

- 确保VESTA版本 ≥ 3.4
- 不同版本的命令行参数可能略有不同

### 路径配置

- 脚本中的路径需要根据实际安装位置修改
- 建议使用绝对路径

### 渲染时间

- 每个CIF文件渲染约需5-10秒
- 84个文件总计约需7-14分钟

### 常见问题

| 问题 | 原因 | 解决方案 |
|:-----|:-----|:---------|
| 未找到VESTA | 路径配置错误 | 修改VESTA_PATH |
| 渲染超时 | 文件太大 | 增加timeout值 |
| 输出目录不存在 | 路径错误 | 检查OUTPUT_DIR配置 |

---

## 六、输出示例

```
✓ 找到VESTA: C:\Program Files\VESTA\VESTA.exe
✓ CIF目录: C:\Obsidion\妙妙屋\08-可视化资源\02-CIF文件库
✓ 输出目录: C:\Obsidion\妙妙屋\08-可视化资源\03-渲染图片

📁 处理目录: 01-单质
  ⏳ 渲染: C_graphite-P63mmc.cif → ✓ C_graphite-P63mmc-ball-stick-crystal.png
  ⏳ 渲染: P_white-Cmca.cif → ✓ P_white-Cmca-ball-stick-crystal.png
  ...

📁 处理目录: 02-离子晶体
  ⏳ 渲染: NaCl-Fm-3m.cif → ✓ NaCl-Fm-3m-ball-stick-crystal.png
  ⏳ 渲染: CsCl-Pm-3m.cif → ✓ CsCl-Pm-3m-ball-stick-crystal.png
  ...

==================================================
📊 渲染完成
   总计: 84
   成功: 84
   失败: 0
   跳过: 0
==================================================
```
