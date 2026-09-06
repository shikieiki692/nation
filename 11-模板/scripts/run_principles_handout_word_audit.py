#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent
BUILD_SCRIPT = SCRIPT_DIR / "build-all-handout-docx.py"
HANDOUTS = [
    VAULT_ROOT / "04-课件" / "学生讲义" / "2026-06-23-热力学基础.md",
    VAULT_ROOT / "04-课件" / "学生讲义" / "2026-06-23-化学动力学基础.md",
    VAULT_ROOT / "04-课件" / "学生讲义" / "2026-06-23-酸碱理论.md",
    VAULT_ROOT / "04-课件" / "学生讲义" / "2026-06-23-气体基础.md",
    VAULT_ROOT / "04-课件" / "学生讲义" / "2026-06-23-溶液和胶体.md",
]


def load_build_module():
    spec = importlib.util.spec_from_file_location("handout_docx_builder", BUILD_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load build script: {BUILD_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_precheck(module, verbose: bool) -> int:
    print("== Word Source Precheck ==")
    failed = 0
    for md_path in HANDOUTS:
        report = module.precheck_file(md_path, verbose=verbose)
        if report.has_errors:
            failed += 1
    print()
    print(f"Precheck summary: {len(HANDOUTS) - failed} passed, {failed} failed")
    return 1 if failed else 0


def run_convert(module, verbose: bool, render_preview: bool, emit_render_pdf: bool) -> int:
    print("== DOCX Convert ==")
    out_dir = VAULT_ROOT / "00-首页" / "学生讲义Word"
    render_dir = out_dir / "_render_preview" if render_preview else None
    failed = 0
    for md_path in HANDOUTS:
        print(f"-- {md_path.name}")
        try:
            out_path = module.convert_file(
                md_path,
                verbose=verbose,
                output_dir=out_dir,
                render_preview=render_preview,
                render_output_dir=render_dir,
                emit_render_pdf=emit_render_pdf,
            )
            if out_path is None:
                print("   skipped")
                failed += 1
            else:
                print(f"   ok -> {out_path}")
        except Exception as exc:
            failed += 1
            print(f"   ERROR: {exc}")
    print()
    print(f"Convert summary: {len(HANDOUTS) - failed} succeeded, {failed} failed")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Word precheck / docx export for the five first-round chemistry principle handouts."
    )
    parser.add_argument(
        "--mode",
        choices=["precheck", "convert"],
        default="precheck",
    )
    parser.add_argument("--render-preview", action="store_true")
    parser.add_argument("--emit-render-pdf", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    module = load_build_module()

    if args.mode == "precheck":
        return run_precheck(module, verbose=args.verbose)
    return run_convert(
        module,
        verbose=args.verbose,
        render_preview=args.render_preview,
        emit_render_pdf=args.emit_render_pdf,
    )


if __name__ == "__main__":
    raise SystemExit(main())
