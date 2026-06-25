import csv
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas


ROOT = Path(r"C:\Obsidion\妙妙屋")
CSV_PATH = ROOT / r"06-学生侧材料\闪卡\anki-export\anki-kp-cards-sample.csv"
OUT_DIR = ROOT / r"06-学生侧材料\闪卡\试印版"
PDF_PATH = OUT_DIR / "2026-06-19-闪卡试印样板-8张每页.pdf"
FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\msyh.ttc"),
    Path(r"C:\Windows\Fonts\msyh.ttf"),
    Path(r"C:\Windows\Fonts\simhei.ttf"),
]


def setup_fonts():
    for path in FONT_CANDIDATES:
        if path.exists():
            pdfmetrics.registerFont(TTFont("CardCJK", str(path)))
            return "CardCJK"
    return "Helvetica"


BODY_FONT = setup_fonts()
BODY_FONT_BOLD = BODY_FONT

PAGE_W, PAGE_H = A4
MARGIN_X = 8 * mm
MARGIN_Y = 10 * mm
GAP_X = 6 * mm
GAP_Y = 5 * mm
COLS = 2
ROWS = 4
CARD_W = (PAGE_W - 2 * MARGIN_X - GAP_X) / COLS
CARD_H = (PAGE_H - 2 * MARGIN_Y - 3 * GAP_Y) / ROWS


def normalize(text: str) -> str:
    return " ".join((text or "").replace("\r", " ").replace("\n", " ").split())


def clip_text(c: canvas.Canvas, text: str, font_name: str, font_size: int, max_width: float) -> str:
    text = normalize(text)
    if not text:
        return ""
    if stringWidth(text, font_name, font_size) <= max_width:
        return text
    ellipsis = "..."
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        candidate = text[:mid].rstrip() + ellipsis
        if stringWidth(candidate, font_name, font_size) <= max_width:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo].rstrip() + ellipsis


def wrap_lines(c: canvas.Canvas, text: str, font_name: str, font_size: int, max_width: float, max_lines: int):
    words = normalize(text).split(" ")
    if not words:
        return []
    lines = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if stringWidth(candidate, font_name, font_size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
            if len(lines) >= max_lines:
                break
    if len(lines) < max_lines:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    if len(lines) == max_lines and " ".join(words) != " ".join(lines):
        lines[-1] = clip_text(c, lines[-1], font_name, font_size, max_width)
    return lines


def card_xy(index: int):
    row = index // COLS
    col = index % COLS
    x = MARGIN_X + col * (CARD_W + GAP_X)
    y = PAGE_H - MARGIN_Y - (row + 1) * CARD_H - row * GAP_Y
    return x, y


def draw_card_box(c: canvas.Canvas, x: float, y: float):
    c.setStrokeColor(HexColor("#203040"))
    c.setLineWidth(0.8)
    c.roundRect(x, y, CARD_W, CARD_H, 4 * mm, stroke=1, fill=0)


def draw_front(c: canvas.Canvas, x: float, y: float, row: dict):
    draw_card_box(c, x, y)
    pad = 5 * mm
    content_w = CARD_W - 2 * pad
    c.setFont(BODY_FONT_BOLD, 10)
    c.setFillColor(HexColor("#1f3b5b"))
    note_type = normalize(row["NoteType"]) or "闪卡"
    c.drawString(x + pad, y + CARD_H - 8 * mm, f"[{note_type}]")

    c.setFont(BODY_FONT_BOLD, 13)
    c.setFillColor(HexColor("#111111"))
    question_lines = wrap_lines(c, row["Front"], BODY_FONT_BOLD, 13, content_w, 4)
    top_y = y + CARD_H - 18 * mm
    for i, line in enumerate(question_lines):
        c.drawString(x + pad, top_y - i * 7 * mm, line)

    c.setFont(BODY_FONT, 8)
    c.setFillColor(HexColor("#5b6470"))
    meta = clip_text(c, f"{normalize(row['Source'])} | {normalize(row['ReviewCycle'])}", BODY_FONT, 8, content_w)
    c.drawString(x + pad, y + 8 * mm, meta)


def draw_back(c: canvas.Canvas, x: float, y: float, row: dict):
    draw_card_box(c, x, y)
    pad = 5 * mm
    content_w = CARD_W - 2 * pad
    c.setFont(BODY_FONT_BOLD, 10)
    c.setFillColor(HexColor("#1f3b5b"))
    c.drawString(x + pad, y + CARD_H - 8 * mm, "答案面")

    c.setFont(BODY_FONT, 9)
    c.setFillColor(HexColor("#111111"))
    answer_lines = wrap_lines(c, row["Back"], BODY_FONT, 9, content_w, 7)
    top_y = y + CARD_H - 17 * mm
    for i, line in enumerate(answer_lines):
        c.drawString(x + pad, top_y - i * 5.8 * mm, line)

    c.setFont(BODY_FONT, 7)
    c.setFillColor(HexColor("#5b6470"))
    extra = clip_text(c, normalize(row["Extra"]), BODY_FONT, 7, content_w)
    c.drawString(x + pad, y + 8 * mm, extra)


def load_rows():
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return rows[:8]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    c = canvas.Canvas(str(PDF_PATH), pagesize=A4)
    c.setTitle("闪卡试印样板 8张每页")

    for i, row in enumerate(rows):
        x, y = card_xy(i)
        draw_front(c, x, y, row)
    c.showPage()

    for i, row in enumerate(rows):
        x, y = card_xy(i)
        mirrored_col = COLS - 1 - (i % COLS)
        mirrored_x = MARGIN_X + mirrored_col * (CARD_W + GAP_X)
        draw_back(c, mirrored_x, y, row)
    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    main()
