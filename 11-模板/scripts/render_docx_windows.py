import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

import pypdfium2 as pdfium

TWIPS_PER_INCH = 1440


def calc_dpi_via_ooxml_docx(input_path: str, max_w_px: int, max_h_px: int) -> int:
    with ZipFile(input_path, "r") as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    sect_pr = root.find(".//w:sectPr", ns)
    if sect_pr is None:
        raise RuntimeError("Section properties not found in document.xml")
    pg_sz = sect_pr.find("w:pgSz", ns)
    if pg_sz is None:
        raise RuntimeError("Page size not found in section properties")

    w_twips_str = pg_sz.get(f"{{{ns['w']}}}w") or pg_sz.get("w")
    h_twips_str = pg_sz.get(f"{{{ns['w']}}}h") or pg_sz.get("h")
    if not w_twips_str or not h_twips_str:
        raise RuntimeError("Page size attributes missing in pgSz")

    width_in = int(w_twips_str) / TWIPS_PER_INCH
    height_in = int(h_twips_str) / TWIPS_PER_INCH
    if width_in <= 0 or height_in <= 0:
        raise RuntimeError("Invalid page size values in document.xml")

    return round(min(max_w_px / width_in, max_h_px / height_in))


def find_soffice() -> str:
    candidates = [
        shutil.which("soffice"),
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate))
    raise RuntimeError(
        "LibreOffice soffice.exe not found. Install LibreOffice or add soffice to PATH."
    )


def build_lo_env(user_profile: str) -> dict:
    env = os.environ.copy()
    env["HOME"] = user_profile
    env["XDG_CONFIG_HOME"] = os.path.join(user_profile, "xdg_config")
    env["XDG_CACHE_HOME"] = os.path.join(user_profile, "xdg_cache")
    os.makedirs(env["XDG_CONFIG_HOME"], exist_ok=True)
    os.makedirs(env["XDG_CACHE_HOME"], exist_ok=True)
    return env


def run_cmd(cmd: list[str], env: dict, verbose: bool) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        cmd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    if verbose:
        print("[render_docx_windows] $ " + " ".join(cmd))
        if proc.stdout:
            print(proc.stdout)
        if proc.stderr:
            print(proc.stderr)
    return proc


def convert_to_pdf(
    input_path: str,
    user_profile: str,
    convert_tmp_dir: str,
    stem: str,
    verbose: bool,
) -> str:
    soffice = find_soffice()
    profile_uri = Path(user_profile).resolve().as_uri()
    env = build_lo_env(user_profile)

    cmd = [
        soffice,
        "-env:UserInstallation=" + profile_uri,
        "--invisible",
        "--headless",
        "--norestore",
        "--convert-to",
        "pdf",
        "--outdir",
        convert_tmp_dir,
        input_path,
    ]
    proc = run_cmd(cmd, env=env, verbose=verbose)
    pdf_path = os.path.join(convert_tmp_dir, f"{stem}.pdf")
    if proc.returncode != 0 or not os.path.exists(pdf_path):
        raise RuntimeError(
            "LibreOffice PDF conversion failed.\n"
            f"Command: {' '.join(cmd)}\n"
            f"Exit: {proc.returncode}\n"
            f"STDOUT:\n{proc.stdout}\n"
            f"STDERR:\n{proc.stderr}"
        )
    return pdf_path


def rasterize_pdf(pdf_path: str, out_dir: str, scale: float) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    pdf = pdfium.PdfDocument(pdf_path)
    try:
        page_paths: list[str] = []
        for index in range(len(pdf)):
            image = pdf[index].render(scale=scale).to_pil()
            path = os.path.join(out_dir, f"page-{index + 1}.png")
            image.save(path)
            page_paths.append(path)
        return page_paths
    finally:
        pdf.close()


def main() -> None:
    if os.name != "nt":
        raise RuntimeError("render_docx_windows.py is intended for Windows only.")

    parser = argparse.ArgumentParser(
        description="Windows-safe DOCX renderer using LibreOffice + pypdfium2."
    )
    parser.add_argument("input_path", type=str)
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=2000)
    parser.add_argument("--dpi", type=int, default=None)
    parser.add_argument("--emit_pdf", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    input_path = os.path.abspath(os.path.expanduser(args.input_path))
    out_dir = (
        os.path.abspath(os.path.expanduser(args.output_dir))
        if args.output_dir
        else os.path.splitext(input_path)[0]
    )
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(input_path))[0]

    if args.dpi is not None:
        dpi = int(args.dpi)
    else:
        try:
            dpi = calc_dpi_via_ooxml_docx(input_path, args.width, args.height)
        except Exception:
            dpi = 150

    scale = dpi / 72.0

    with tempfile.TemporaryDirectory(prefix="soffice_profile_") as user_profile:
        with tempfile.TemporaryDirectory(prefix="soffice_convert_") as convert_tmp_dir:
            if input_path.lower().endswith(".pdf"):
                pdf_path = input_path
            else:
                pdf_path = convert_to_pdf(
                    input_path, user_profile, convert_tmp_dir, stem, verbose=args.verbose
                )

            if args.emit_pdf and pdf_path != input_path:
                shutil.copy2(pdf_path, os.path.join(out_dir, f"{stem}.pdf"))

            paths = rasterize_pdf(pdf_path, out_dir, scale=scale)

    print("Pages rendered to " + out_dir)
    print("Page count: " + str(len(paths)))


if __name__ == "__main__":
    main()
