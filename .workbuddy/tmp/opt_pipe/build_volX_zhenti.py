# -*- coding: utf-8 -*-
"""机构卷 → 真题版式 docx（复用 build_chusai_zhenti_layout.py 的全部排版手术）。

差异点（相对共享脚本，全部以 monkey-patch 方式**只作用于机构组卷线**）：
① 图片取自 `04-题库/2026机构初赛模拟题/*/images/`，先建暂存媒体目录并铺图；
② ★ 新增「整页档」封顶：两维都 ≥1700px 的**整页级答案扫描**放到版心宽（16.5×21.0cm），
   否则沿用 land 7.0×5.2 / port 4.6×6.6 / sq 5.6×5.6 —— 修「整页裁图被压到 4.6cm ⇒ 不可读」；
③ ★ 落盘前**降采样**：长边 >2500px 者缩到 2200px 并存 JPEG（控 docx 体积，260dpi 仍清晰）。

用法：python build_volX_zhenti.py --vol XI [--answer|--student]   默认两种都出。
"""
import glob
import os
import re
import shutil
import sys
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
QB = VAULT / "04-题库"
ORGBASE = QB / "2026机构初赛模拟题"
SCRIPTS = VAULT / ".workbuddy" / "scripts"


def _arg_vol():
    for i, a in enumerate(sys.argv):
        if a == "--vol" and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
        if a.startswith("--vol="):
            return a.split("=", 1)[1]
    return os.environ.get("VOL") or "X"


VOL = _arg_vol()
WORK = VAULT / ".workbuddy" / "tmp" / ("vol%s_zhenti" % VOL)
STAGE = WORK / "media"
for d in (WORK, STAGE):
    d.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SCRIPTS))
# 注意：build_chusai_zhenti_layout 在 import 时会把 sys.stdout 换成一个 utf-8
# 包装器（基于当时的底层 buffer）。不要在这之前/之后自行重设 stdout。
import build_chusai_zhenti_layout as Z   # noqa: E402

MEDIA_FILES = ["初赛模拟卷%s（非有机·答案版）.md" % VOL, "初赛模拟卷%s（非有机·学生版）.md" % VOL]

# ── ★ 机构线专属：整页档封顶 + 落盘降采样 ─────────────────────────────
CM_TO_EMU = 360000
EMU_PER_PX = 9525            # pandoc 按 96dpi 折算像素→EMU
PAGE_MIN_LONG = 1800         # ★ 长边 ≥1800px ⇒ 判为「整页级」（实测：该档 206 张抽样全部为整页扫描；
                             #   而 1000–1799 档抽样为正常结构图）
CAP_ORG = {"land": (7.0, 5.2), "port": (4.6, 6.6), "sq": (5.6, 5.6), "page": (16.5, 21.0)}
MAXPX, TARGETPX = 2600, 2400  # 降采样后长边仍 ≥1800 ⇒ 整页档判定不受影响
NAME_MAP = {}                # 原图名 → 暂存实际文件名
PAGE_NAMES = set()           # ★ 判定为「整页级」的**暂存实际文件名**

# 🔴 关键：pandoc 会先把每张图铺到「版心宽」再写 <wp:extent>，故 XML 里的 cx 与
#    「原图像素」无关 ⇒ 不能用 cx 判整页档。改从 <pic:cNvPr descr="原名"> 取图片名，
#    与 PAGE_NAMES 比对（descr 由 resolve_images 输出的文件名决定）。
CNVP_RE = re.compile(r'<pic:cNvPr[^>]*?(?:descr|name)="([^"]+)"')


def cap_image_width2(p: str) -> str:
    """整页级扫描放开到版心宽（可读）；其余沿用原三档（只缩不放）。"""
    ext = re.compile(r'<wp:extent cx="(\d+)" cy="(\d+)"')
    aext = re.compile(r'<a:ext cx="(\d+)" cy="(\d+)"')
    m = CNVP_RE.search(p)
    nm = (m.group(1) if m else '').strip()
    is_page = nm in PAGE_NAMES

    def _size(cx, cy):
        if cx <= 0 or cy <= 0:
            return cx, cy
        if is_page:
            mw, mh = CAP_ORG["page"]
        else:
            a = cx / cy
            key = "land" if a > 1.3 else ("port" if a < 0.7 else "sq")
            mw, mh = CAP_ORG[key]
        scale = min(1.0, (mw * CM_TO_EMU) / cx, (mh * CM_TO_EMU) / cy)
        if scale >= 0.999:
            return cx, cy
        return int(cx * scale), int(cy * scale)

    p = ext.sub(lambda m: '<wp:extent cx="%d" cy="%d"' % _size(int(m.group(1)), int(m.group(2))), p)
    p = aext.sub(lambda m: '<a:ext cx="%d" cy="%d"' % _size(int(m.group(1)), int(m.group(2))), p)
    return p


def stage_image(src: str, name: str) -> str:
    """把源图铺到暂存：长边 >MAXPX 者降采样存 JPEG；长边 ≥PAGE_MIN_LONG 者登记为「整页档」。

    返回暂存实际文件名。
    """
    from PIL import Image
    try:
        im = Image.open(src)
        w, h = im.size
    except Exception:
        shutil.copyfile(src, str(STAGE / name))
        return name
    real = name
    if max(w, h) > MAXPX:
        sc = TARGETPX / max(w, h)
        im2 = im.convert("RGB").resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.LANCZOS)
        real = os.path.splitext(name)[0] + ".jpg"
        im2.save(str(STAGE / real), "JPEG", quality=86, optimize=True)
        print("     [缩图] %s %dx%d → %s %dx%d" % (name[:28], w, h, real[-24:], im2.width, im2.height))
    else:
        shutil.copyfile(src, str(STAGE / name))
    if max(w, h) >= PAGE_MIN_LONG:
        PAGE_NAMES.add(real)
    return real


def prepare_media():
    """铺图（含降采样），返回 (引用数, 缺图列表)。"""
    idx = {}
    for p in glob.glob(str(ORGBASE / "*" / "images" / "*")):
        idx.setdefault(os.path.basename(p), p)
    need, missing = set(), []
    for md in MEDIA_FILES:
        t = (QB / md).read_text(encoding="utf-8")
        for m in re.finditer(r"!\[\[([^\]\|\\]+?)(?:\\?\|\d+)?\]\]", t):
            need.add(m.group(1).strip())
    for name in sorted(need):
        src = idx.get(name)
        if src and os.path.exists(src):
            NAME_MAP[name] = stage_image(src, name)
        else:
            missing.append(name)
    return len(need), missing


def main():
    only_ans = "--answer" in sys.argv
    only_stu = "--student" in sys.argv
    only_kz = "--kazhu" in sys.argv
    n, missing = prepare_media()
    print("图准备：引用 %d 张，已铺 %d 张，缺 %d" % (n, len(os.listdir(STAGE)), len(missing)))
    for m in missing[:10]:
        print("   [缺图]", m)
    # ★ monkey-patch：媒体目录 / 图片正则（容 `![[hash.jpg\\|250]]` 转义形态）/ 封顶（加整页档）
    Z.MEDIA = STAGE
    Z.cap_image_width = cap_image_width2
    print("  整页档图 %d 张（长边≥%dpx ⇒ 放到版心宽 16.5×21.0cm）" % (len(PAGE_NAMES), PAGE_MIN_LONG))

    def resolve_images2(body, log):
        def rep(m):
            name = m.group(1).strip()
            real = NAME_MAP.get(name, name)
            if not (STAGE / real).exists():
                log.append(f"   [缺图] {name}")
                return ""
            return f"![]({real})"
        return re.sub(r"!\[\[([^\]\|\\]+?)(?:\\?\|\d+)?\]\]", rep, body)

    Z.resolve_images = resolve_images2
    Z.TMP.mkdir(parents=True, exist_ok=True)
    ref = Z.build_reference()
    print("reference:", ref)

    if only_ans:
        eds = ["answer"]
    elif only_stu:
        eds = ["student"]
    elif only_kz:
        eds = []
    else:
        eds = ["student", "answer"]
    done = []
    for ed in eds:
        t = Z.convert_one(VOL, ref, ed)
        if t:
            done.append(t)
    if only_kz or not eds:                 # ★ 答题卡（信息栏＋阅卷得分表＋逐题作答框）
        t = Z.build_answer_sheet(VOL, ref)
        if t:
            done.append(t)
    print("\n完成 %d 个：%s" % (len(done), Z.OUTDIR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
