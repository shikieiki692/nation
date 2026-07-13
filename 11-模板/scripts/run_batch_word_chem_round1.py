from pathlib import Path
import subprocess
import sys


def main() -> int:
    vault = Path(__file__).resolve().parents[2]
    build_script = vault / "11-模板" / "scripts" / "build-all-handout-docx.py"
    files = [
        vault / "04-课件" / "学生讲义" / "2026-06-23-化学计量与计算规范.md",
        vault / "04-课件" / "学生讲义" / "2026-06-23-方程式书写专项.md",
        vault / "04-课件" / "学生讲义" / "2026-06-23-气体基础.md",
        vault / "04-课件" / "学生讲义" / "溶液与相图-超级充实版（自学完整）.md",
        vault / "04-课件" / "学生讲义" / "热力学初步-超级充实版（自学完整）.md",
        vault / "04-课件" / "学生讲义" / "化学动力学-超级充实版（自学完整）.md",
        vault / "04-课件" / "学生讲义" / "化学平衡-超级充实版（自学完整）.md",
        vault / "04-课件" / "学生讲义" / "酸碱理论-超级充实版（自学完整）.md",
        vault / "04-课件" / "学生讲义" / "2026-06-23-沉淀溶解平衡.md",
        vault / "04-课件" / "学生讲义" / "2026-06-23-水中的几种平衡.md",
        vault / "04-课件" / "学生讲义" / "2026-06-23-电化学基础.md",
    ]

    for file_path in files:
        print(f"[START] {file_path.name}")
        subprocess.run(
            [sys.executable, str(build_script), "--path", str(file_path), "--word-clean"],
            check=True,
        )

    print("[DONE] chemistry principle round 1 word clean batch complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
