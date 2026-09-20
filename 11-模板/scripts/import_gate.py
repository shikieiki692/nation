#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""import_gate.py —— 导入边界闸门（一批新内容进库后跑一次）。

## 为什么需要它
本库**没有导入脚本** —— OCR 产物（`mineru/`）到各域是人工/Agent 手工完成的，
所以没有「函数入口」可以插闸门。实测：`03-知识点/` + `07-资料提炼/` 两域
**从未被任何检查覆盖**（既有预检绑在 docx 管线上），一跑就出 **53 份**公式渲染缺陷。

因此本脚本的定位是「**一批导入之后跑一次**」：
  ① 用 `md_sanitize.sanitize()` 把**机械类**缺陷直接修掉（div / `\\AA` / TAB /
     `\\text{\\text{}}` 嵌套 / 数学域内 HTML 实体）
  ② 再用 `render_gate` 判定**剩下的**（那些需要按原书校正语法、无法机械修的）

## 用法
    # 只看会改什么（默认，不落盘）
    python -X utf8 11-模板/scripts/import_gate.py --manifest <清单>      # 或 --domain <域>
    # 真的修
    python -X utf8 11-模板/scripts/import_gate.py --manifest <清单> --fix
    # 修完再看渲染（render_gate 阶段可跳过）
    python -X utf8 11-模板/scripts/import_gate.py --manifest <清单> --fix --no-render

退出码：0 = 无事可做或已修且渲染全过；1 = 仍有需人工处理的项。
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import md_sanitize as san          # noqa: E402

BAK = VAULT / ".workbuddy" / "tmp" / "import_gate_bak"


def collect(args):
    if args.manifest:
        p = Path(args.manifest)
        if not p.is_absolute():
            p = VAULT / p
        return [x.strip() for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    if args.domain:
        root = VAULT / args.domain
        return [str(f.relative_to(VAULT).as_posix()) for f in sorted(root.rglob("*.md"))]
    raise SystemExit("!! 需指定 --manifest 或 --domain")


def main() -> int:
    ap = argparse.ArgumentParser(description="导入边界闸门（机械类代修 + 渲染判定）")
    ap.add_argument("--manifest", default=None, help="文件清单（一行一个相对路径）")
    ap.add_argument("--domain", default=None, help="按域递归")
    ap.add_argument("--fix", action="store_true", help="真的把机械类缺陷落盘")
    ap.add_argument("--no-render", action="store_true", help="跳过 render_gate 阶段")
    ap.add_argument("--report", default=None, help="把报告写到指定路径")
    args = ap.parse_args()

    rels = collect(args)
    if not rels:
        print("受检 0 文件")
        return 0

    BAK.mkdir(parents=True, exist_ok=True)
    changed, untouched, missing = [], [], []
    for rel in rels:
        p = VAULT / rel
        if not p.is_file():
            missing.append(rel)
            continue
        text = p.read_text(encoding="utf-8")
        new = san.sanitize(text)
        if new == text:
            untouched.append(rel)
            continue
        changed.append(rel)
        if args.fix:
            shutil.copyfile(p, BAK / rel.replace("/", "__"))
            p.write_text(new, encoding="utf-8", newline="")

    print("=" * 70)
    print(f"① 机械类净化（md_sanitize）  {'已落盘' if args.fix else '预检（未落盘）'}")
    print("=" * 70)
    print(f"  可修/已修 : {len(changed)}")
    print(f"  无需改动  : {len(untouched)}")
    if missing:
        print(f"  文件不存在: {len(missing)}")
    for rel in changed[:30]:
        print(f"    · {rel}")
    if len(changed) > 30:
        print(f"    …（另 {len(changed) - 30} 份）")

    rc = 0
    if not args.no_render:
        print()
        print("=" * 70)
        print("② 渲染判定（render_gate）—— 剩下的是需按原书校正语法的")
        print("=" * 70)
        mf = VAULT / ".workbuddy" / "tmp" / "_import_gate_list.txt"
        mf.write_text("\n".join(rels) + "\n", encoding="utf-8", newline="\n")
        r = subprocess.run([sys.executable, "-X", "utf8",
                            str(SCRIPT_DIR / "render_gate.py"),
                            "--manifest", str(mf), "--quiet"],
                           cwd=VAULT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        out = (r.stdout or "") + (r.stderr or "")
        print(out.strip())
        rc = r.returncode
        try:
            mf.unlink()
        except OSError:
            pass

    summary = (f"import_gate: 机械类 {len(changed)} 份 / 渲染残留见上；"
               f"备份在 {BAK.relative_to(VAULT).as_posix() if BAK.exists() else '（无）'}")
    print("\n" + summary)
    if args.report:
        rp = Path(args.report)
        if not rp.is_absolute():
            rp = VAULT / rp
        rp.write_text(summary + "\n\n可修清单：\n" + "\n".join(changed), encoding="utf-8")
        print(f"报告已写 {rp.relative_to(VAULT)}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
