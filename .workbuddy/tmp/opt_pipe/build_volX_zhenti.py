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
CAP_ORG = {"land": (8.4, 5.2), "port": (4.8, 6.8), "sq": (6.0, 6.0), "page": (16.5, 21.0)}
# ↑ 2026-10-11 版式优化（第二轮：「再仔细斟酌」）：
#   首轮放宽到 land 9.5／sq 7.0／port 6.0×8.0 后**部分图占版面过大**（实测 17 张 >8cm 宽、5 张 7.0cm 高，
#   单图面积最大 55cm² ＝ 近 1/5 页）⇒ 回调为**适度档**（相对首轮 −12%~−15%，相对原档仍 +10~20%），
#   并加**单图面积上限**（`AREA_MAX`）作硬闸，确保任何一张图都不霸版。
AREA_MAX_CM2 = 42.0          # 单图面积上限（≈6.5×6.5cm），超出按等比再缩

MAXPX, TARGETPX = 2600, 2400  # 降采样后长边仍 ≥1800 ⇒ 整页档判定不受影响
NAME_MAP = {}                # 原图名 → 暂存实际文件名
PAGE_NAMES = set()           # ★ 判定为「整页级」的**暂存实际文件名**

# ── ★ 构建期「图有效分辨率」封顶（治本，2026-10-09）─────────────────────
# 病根：物理档封顶（land 7.0cm 等）与**源像素**无关 ⇒ 低清小图被拉到 7.0cm 打印，
#       有效分辨率掉到 72~100 dpi（渲染层机检 40 处 BLUR/SMALL 全是这一类）。
# 治法：在全部物理档封顶**之后**再加一道按源像素的封顶 —— 渲染宽 ≤ px/MIN_DPI。
#       等价于「印刷有效分辨率 ≥ MIN_DPI」，只缩不放（≥MIN_DPI 的图不受影响）。
# 位置：作为 process_document_xml 的**最终 pass**（monkey-patch 包装），
#       在 <w:drawing> 粒度上处理 ⇒ **段落图与表格内图一并覆盖**（表格图走的是
#       cap_table_images，不走 cap_image_width，故不能只在 cap_image_width 里加）。
MIN_DPI = 150.0              # 印刷线稿的最低有效分辨率（≈印刷厂对线稿的合格线）
EMU_PER_CM = 360000
IMG_PX = {}                  # ★ 暂存实际文件名 → (w,h) **最终**像素（降采样后）
DRAW_RE = re.compile(r"<w:drawing>.*?</w:drawing>", re.S)
DESCR_RE = re.compile(r'<pic:cNvPr[^>]*?\bdescr="([^"]*)"')
_CX_RE = re.compile(r'<wp:extent cx="(\d+)" cy="(\d+)"')
_AX_RE = re.compile(r'<a:ext cx="(\d+)" cy="(\d+)"')


def apply_dpi_cap(xml: str):
    """按源像素封顶每张图的渲染尺寸，保证有效分辨率 ≥ MIN_DPI（只缩不放）。

    返回 (xml, 被缩图数, 缩放清单)。
    """
    log = []

    def _one(m):
        frag = m.group(0)
        d = DESCR_RE.search(frag)
        nm = (d.group(1) if d else "").strip()
        wh = IMG_PX.get(nm)
        w_px, h_px = (wh if wh else (0, 0))
        max_w = w_px / MIN_DPI * 2.54 * EMU_PER_CM
        max_h = h_px / MIN_DPI * 2.54 * EMU_PER_CM
        before = _CX_RE.search(frag)

        def _size(cx, cy):
            if cx <= 0 or cy <= 0:
                return cx, cy
            s = 1.0
            if w_px > 0 and h_px > 0:                 # ① 有效分辨率 ≥ MIN_DPI（只缩不放）
                s = min(1.0, max_w / cx, max_h / cy)
            area = (cx * s / EMU_PER_CM) * (cy * s / EMU_PER_CM)
            if nm not in PAGE_NAMES and area > AREA_MAX_CM2:   # ② 单图面积硬闸（整页档豁免）
                s *= (AREA_MAX_CM2 / area) ** 0.5
            if s >= 0.99999:      # 容差收紧（原 0.9995 会跳过 0.05% 级别的微缩 ⇒ 有效 dpi 掉到 149.98）
                return cx, cy
            return max(1, int(cx * s)), max(1, int(cy * s))   # 向下取整 ⇒ 有效 dpi 严格 ≥ MIN_DPI

        frag = _CX_RE.sub(
            lambda mm: '<wp:extent cx="%d" cy="%d"' % _size(int(mm.group(1)), int(mm.group(2))), frag)
        frag = _AX_RE.sub(
            lambda mm: '<a:ext cx="%d" cy="%d"' % _size(int(mm.group(1)), int(mm.group(2))), frag)
        after = _CX_RE.search(frag)
        if before and after and int(after.group(1)) < int(before.group(1)):
            log.append((nm, w_px, h_px, int(before.group(1)) / EMU_PER_CM,
                        int(after.group(1)) / EMU_PER_CM))
        return frag

    xml = DRAW_RE.sub(_one, xml)
    return xml, len(log), log

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


# ── ★ 2026-10-11 图像净化（构建期，源图**不动**，只净化卷内副本）──────────────
# 病根：源为扫描件，裁图时带入**灰色底纹 / 浅灰水印（清北营教育·CHICAMY）/邻页渗色**。
# 处置：① 灰底 ⇒ 白场化（把背景灰压到纯白）；② 浅灰低饱和像素 ⇒ 压白（含水印）。
# 覆盖范围＝**目检白名单**（80 张里 ~22 张；自动判据区分度不足，勿改为自动）。
CLEAN_GRAY = {  # 灰底：白场化 + 浅中性残压白
    "d240dbfd83b5e53e8e7ba12459776562ce4f312afb96feed09b5e0aeb2339b95.jpg",
    "4d09f4727126dea2b0952ad5793eee5610e0bd114f997e72738445bb59044ab5.jpg",
    "ff0f77a73636e174d037b4cb8ea6a320550c4ee2aabf41f8a60053b041b107f7.jpg",
    "e5506a959df8daa2605586c8861f93b8a0c121409fb1fd73817cf40bcc9dacee.jpg",
    "07b102e8611dac7b8c84f0d140579e8dbbc5c882fee8db0b952e568ffdddcbf1.jpg",
    "7c7fa2cda2d458bd0f3b42a0c7fdb2f7d126cef96447c7867eafa18fab438caa.jpg",
    "a7bbb5441b19f87dbaacd3a1ea4f3605f0bc6390080134738072f34c6d785fde.jpg",
    "8caa43de17a625be7a7726bb4fa2876f4e53ead06140174fcc1da1625609390f.jpg",
    "295eef699ce20365887e2e3eb0c822a698478c2ffe1a7f7934e09a27c12ca911.jpg",
    "881ef87685739508a298bc6077eb8eb3d8524738d1b3fd9ff904742857136292.jpg",
    "b591c46e9b9a3daa2837abb8af2047055b9a85b85d4fa349028666910732bc1b.jpg",
    "3005d9a2baf04c3437b00c251a36f2044cf79fdec7e200b2a395a3fc3d85a2ef.jpg",
    "c1408cb1ca0a90afd6888a8d959f2c1b7d0760c4d63767966c4f5d2edcf946d6.jpg",
    "ba5ef0a9381a4e29cba25e4764eb49dbc7f774fb8c590d01b0e2b99da636ec47.jpg",
    "08e3478dc6b008f42ed754d8f0e89dea7f2410c4f9629753a397a5c62a8ed971.jpg",
    "87e86bb30c8a9d2eeb69cdeaa4f06768b3542b55ea97dcd16f363d2903da7c08.jpg",
    "5128a54af65ce9323d8d75d3e3711af61226fb77832e12be2d267fabe6ebdd34.jpg",
}
CLEAN_WM = {  # 仅浅灰水印（底已白）：浅中性像素压白
    "a8ce9ccff7b1a53f039c7aaa3a8b8facb6b676dff863261bab4c479768fdbbcd.jpg",   # 清北营 吸附曲线
    "2486ce26aa01bd92f21d240383e0219c52b449c23e201a07436122019f33ff30.jpg",   # 清北营 [Cr(O2)2] 结构
    "792684dab0c2f995f1ca4a09b9f731f1ae24aced341aad08ea92123f7f2b26d4.jpg",   # XeChem 曲线
}
# 🔴 未纳入白名单（保持原图）：`a8ec894e…`/`a9b30bc6…`（XeChem 晶体图）——
#   其**灰色填充原子与灰底同灰阶**（实测二者 lum 均 ≈200-230，不可分离），
#   任何去背景的阈值都会同时把原子填充削白 ⇒ 一并不动。
TH_MAIN = 168
# ── ★ 2026-10-11 回源重裁（构建期；源图不动）────────────────────────────
# 病根：源卡的图从原 PDF 裁切时**切掉了图下的标签行**（实测：壹尖培优 Fe₄L₄ 笼 2 张，
#       卡内标签只剩半行「T  R  M…」）。⇒ 按「图 ＋ 图下标签」从源 PDF 重新裁切。
# 说明：源 PDF 为**数字版**（有文字层），`get_image_info()` 取各联图像 bbox，
#       标签为图下的文本行（同一页 y 724–735）⇒ 裁到 737 即「图＋标签」完整。
_YJ12 = ("06-外部资料导入/OCR/01-题目/2026年壹尖培优夏令营（国初高端冲刺营）/"
         "第40届中国化学奥林匹克（初赛）模拟试题和答题卡/"
         "第 40 届中国化学奥林匹克（初赛）模拟试题12.pdf")
RECROP = {
    # 卡图名 → 源（PDF 相对路径 / 页序 / 裁切框 pt / dpi）
    "6f6ea31f7b45c003ce00373828c3e58e6cfa8cc3e2c94608124772f698e30a16.jpg":
        {"pdf": _YJ12, "page": 4, "bbox": (87, 617, 192, 737), "dpi": 300},   # T_L R = Me
    "f9c25d8cf66afa052557dc1db8cde1a47309ce437479934e5eea042528911c26.jpg":
        {"pdf": _YJ12, "page": 4, "bbox": (194, 617, 298, 737), "dpi": 300},  # T_L R = Et
}
CLEAN_LOG = []


def _clean_array(a, th):
    """a: HxWx3 int16 → 净化后 uint8 数组（白场化 + 浅中性压白）。"""
    import numpy as np
    bg = int(np.argmax(np.bincount(a.mean(axis=2).astype(np.int16).ravel(), minlength=256)[128:])) + 128
    if bg < 246:
        sc = 255.0 / max(bg, 190)
        a = np.clip(a.astype(np.float32) * sc, 0, 255).astype(np.int16)
    lum = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)
    m = (lum >= th) & (sat <= 32)          # 浅且中性 ⇒ 背景/水印（168 离线对比实测最佳）
    a = a.copy()
    a[m] = 255
    return a.astype(np.uint8)


def clean_scan(im, name):
    """按白名单净化（源图不动）。返回 (新图, 是否净化)。"""
    if name not in CLEAN_GRAY and name not in CLEAN_WM:
        return im, False
    try:
        from PIL import Image
        import numpy as np
        a = np.asarray(im.convert("RGB")).astype(np.int16)
        return Image.fromarray(_clean_array(a, TH_MAIN)), True
    except Exception as e:  # 净化失败不阻断构建
        print("     [净化跳过] %s：%s" % (name[:20], e))
        return im, False


def stage_image(src: str, name: str) -> str:
    """把源图铺到暂存：长边 >MAXPX 者降采样存 JPEG；长边 ≥PAGE_MIN_LONG 者登记为「整页档」。

    返回暂存实际文件名。
    """
    from PIL import Image
    rc = RECROP.get(name)
    if rc:                                   # ★ 回源重裁（补回被切掉的图下标签）
        try:
            import fitz
            doc = fitz.open(os.path.join(str(VAULT), rc["pdf"]))
            pix = doc[rc["page"]].get_pixmap(dpi=rc.get("dpi", 300), clip=fitz.Rect(*rc["bbox"]))
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            print("     [回源重裁] %s → %dx%d（含图下标签）" % (name[:18], pix.width, pix.height))
            im, _c = clean_scan(im, name)
            real = os.path.splitext(name)[0] + ".jpg"
            im.save(str(STAGE / real), "JPEG", quality=92, optimize=True)
            IMG_PX[real] = (im.width, im.height)
            if max(im.size) >= PAGE_MIN_LONG:
                PAGE_NAMES.add(real)
            return real
        except Exception as e:
            print("     [重裁失败⇒回退原图] %s：%s" % (name[:18], e))
    try:
        im = Image.open(src).convert("RGB")
        w, h = im.size
    except Exception:
        shutil.copyfile(src, str(STAGE / name))
        return name
    im, cleaned = clean_scan(im, name)
    real = name
    fw, fh = w, h
    if max(w, h) > MAXPX or cleaned:
        im2 = im
        if max(w, h) > MAXPX:
            sc = TARGETPX / max(w, h)
            im2 = im.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.LANCZOS)
            print("     [缩图] %s %dx%d → %dx%d" % (name[:28], w, h, im2.width, im2.height))
        if cleaned:
            print("     [净化] %s（去灰底/浅水印）" % name[:24])
        real = os.path.splitext(name)[0] + ".jpg"
        im2.save(str(STAGE / real), "JPEG", quality=92, optimize=True)
        fw, fh = im2.width, im2.height
    else:
        shutil.copyfile(src, str(STAGE / name))
    IMG_PX[real] = (fw, fh)          # ★ 记录**最终**像素（供 DPI 封顶）
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


META = VAULT / ".workbuddy" / "tmp" / "opt_pipe" / ("vol_meta_%s.json" % VOL)


def run_post_patches() -> int:
    """★ P0-2（2026-10-11）：按 vol_meta_<卷>.json 的 post_patches 串行执行**卷级后处理补丁**。

    病根：卷级补丁（如卷 XVI 的「21 列颜色表 pandoc 网格修复」）必须在本脚本**重建 docx 之后**
          再跑，但没有任何环节强制它 —— 漏跑时**所有闸门都不报**（折行审计不感知显式 tblCellMar），
          交付件会静默带缺陷。
    对策：把补丁登记进计划 sidecar（`post_patches`），由本脚本自动串行执行并**校验退出码**；
          补丁脚本缺失或失败 ⇒ 明确报错并返回非 0，绝不「静默交付未打补丁的 docx」。
    """
    import json
    import subprocess
    try:
        meta = json.loads(META.read_text(encoding="utf-8"))
    except Exception:
        return 0
    patches = meta.get("post_patches") or []
    if not patches:
        return 0
    print("\n卷级后处理补丁 %d 个（登记于 %s）：" % (len(patches), META.name))
    for it in patches:
        script = (it.get("script") or "").strip()
        # ★ 2026-10-15 修：`script` 可含参数（如 `vol_img_upscale.py --vol XVI`）。
        #   原实现把整串当文件名 ⇒ `path.exists()` 恒 False ⇒ **带参数的补丁全部被静默跳过**
        #   （X/XI/XIp/XIV/XV/XVI 的图片放大补丁因此从未自动生效，只靠人工补跑）。
        parts = script.split()
        if not parts:
            continue
        path = VAULT / ".workbuddy" / "tmp" / "opt_pipe" / parts[0]
        if not path.exists():
            print("  ⛔ 补丁脚本缺失：%s ⇒ 交付件可能带缺陷，请先补齐脚本" % script)
            return 2
        r = subprocess.run([sys.executable, "-X", "utf8", str(path)] + parts[1:],
                           cwd=str(VAULT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        ok = r.returncode == 0
        print("  %s %s ｜ %s" % ("[OK]  " if ok else "[FAIL]", script, it.get("why", "")))
        for line in (r.stdout or "").strip().splitlines()[-4:]:
            print("        " + line)
        if not ok:
            print("        " + (r.stderr or "").strip()[-400:])
            print("  ⛔ 补丁失败 ⇒ 请修复后重跑本脚本（勿带未打补丁的 docx 交付）")
            return 3
    return 0


# ── ★ 2026-10-11 版式优化 pass（作用于 document.xml 最终态，dpi 封顶之后）──────
_PARA_RE = re.compile(r"<w:p\b[\s\S]*?</w:p>")
_TBL_RE2 = re.compile(r"<w:tbl>[\s\S]*?</w:tbl>")
_JC_RE2 = re.compile(r"<w:jc\b[^>]*/>")
_SP_RE2 = re.compile(r"<w:spacing\b[^>]*/>")
_TXT2 = re.compile(r"<w:t(?:\s[^>]*)?>([\s\S]*?)</w:t>")
OPT_RE = re.compile(r"^\s*[A-D][.、．)）]")
SCORE_RE = re.compile(r"^\s*[（(]\s*\d+\s*分\s*[）)]")
NONE_BORDERS = ('<w:tblBorders>'
                '<w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/>'
                '<w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
                '</w:tblBorders>')
_SP_IMG = '<w:spacing w:before="120" w:after="40" w:line="240" w:lineRule="auto"/>'
_SP_CAP = '<w:spacing w:before="0" w:after="120" w:line="240" w:lineRule="auto"/>'


def _ptxt(p):
    return "".join(_TXT2.findall(p))


def _ensure(p, tag, xml):
    if "<w:pPr>" not in p:
        m = re.match(r"<w:p\b[^>]*>", p)
        p = p[:m.end()] + "<w:pPr></w:pPr>" + p[m.end():]
    if tag == "jc" and _JC_RE2.search(p):
        return _JC_RE2.sub(xml, p, count=1)
    if tag == "spacing" and _SP_RE2.search(p):
        return _SP_RE2.sub(xml, p, count=1)
    if tag == "keepNext":
        return p if "<w:keepNext" in p else Z._insert_into_pPr(p, "keepNext", "<w:keepNext/>")
    return Z._insert_into_pPr(p, tag, xml)


def _is_caption(t):
    """紧随图片的「短图注」判据（治：图居中、注左对齐）。"""
    if not t:
        return False
    if Z.SUBQ_RE.match(t) or OPT_RE.match(t) or SCORE_RE.match(t):
        return False
    if Z.CAPTION_RE.match(t):          # 「图 N …」「第 N 题图…」：无论长短一律图注
        return True
    if len(t) > 26 or t.endswith("分"):
        return False
    if any(ch in t for ch in "。：；？！，"):   # 句读 ⇒ 非图注（半角逗号不算，如 2,2'-bptz）
        return False
    return True


def polish_images(xml: str, stat: dict) -> str:
    # ① 含图表格：去框 + 居中（并排图不再被黑框住）
    def _tbl(m):
        t = m.group(0)
        if "<w:drawing" not in t:
            return t
        t = re.sub(r"<w:tblBorders\b[\s\S]*?</w:tblBorders>", NONE_BORDERS, t)
        if "<w:tblBorders" not in t:
            t = re.sub(r"(<w:tblPr>)", r"\1" + NONE_BORDERS, t, count=1)
        if "<w:tblPr>" in t and "<w:jc " not in t[:t.find("</w:tblPr>") + 10]:
            t = re.sub(r"(<w:tblW\b[^>]*/>)", r'\1<w:jc w:val="center"/>', t, count=1)
        stat["img_tbl"] = stat.get("img_tbl", 0) + 1
        return t
    xml = _TBL_RE2.sub(_tbl, xml)

    spans = [(m.start(), m.end()) for m in _TBL_RE2.finditer(xml)]

    def in_tbl(pos):
        return any(a <= pos < b for a, b in spans)

    out, last, prev_img = [], 0, False
    for m in _PARA_RE.finditer(xml):
        p, pos = m.group(0), m.start()
        out.append(xml[last:pos])
        last = m.end()
        if in_tbl(pos):
            out.append(p)
            prev_img = False
            continue
        if "<w:drawing" in p:                       # 图片段：居中 + 紧下距 + 跨页不分离
            p = _ensure(p, "spacing", _SP_IMG)
            p = _ensure(p, "jc", '<w:jc w:val="center"/>')
            p = _ensure(p, "keepNext", "")
            prev_img = True
            out.append(p)
            continue
        t = _ptxt(p).strip()
        if not t:                                   # 空段不打断「图 → 图注」邻接
            out.append(p)
            continue
        if prev_img and _is_caption(t):             # 图注：居中贴图
            p = _ensure(p, "spacing", _SP_CAP)
            p = _ensure(p, "jc", '<w:jc w:val="center"/>')
            stat["caption_c"] = stat.get("caption_c", 0) + 1
            out.append(p)
            prev_img = False
            continue
        prev_img = False
        out.append(p)
    out.append(xml[last:])
    return "".join(out)


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

    # ★ monkey-patch：在段落/表格全部封顶**之后**加一道「按源像素」的有效分辨率封顶
    if "--no-dpi-cap" not in sys.argv:
        _orig_pdx = Z.process_document_xml

        def process_document_xml2(xml, stat):
            xml = _orig_pdx(xml, stat)
            xml, _n, _log = apply_dpi_cap(xml)
            if _log:
                _log.sort(key=lambda r: r[4])
                worst = _log[:5]
                print("  图分辨率封顶：缩 %d 张（目标 ≥%.0fdpi）｜最紧 %s"
                      % (_n, MIN_DPI, "、".join("%s %.2f→%.2fcm" % (r[0][:12], r[3], r[4]) for r in worst)))
            xml = polish_images(xml, stat)
            if stat.get("caption_c") or stat.get("img_tbl"):
                print("  版式优化：图注居中 %d 处 ｜ 并排图表去框 %d 张"
                      % (stat.get("caption_c", 0), stat.get("img_tbl", 0)))
            return xml

        Z.process_document_xml = process_document_xml2
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
    rc = run_post_patches()
    if rc:
        return rc
    return 0


if __name__ == "__main__":
    sys.exit(main())
