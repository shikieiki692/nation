"""Create custom pandoc reference docx with Chinese fonts."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ref_path = r"C:\Users\蕾赛\AppData\Local\Temp\pandoc-reference.docx"
doc = Document(ref_path)

# Set page size to A4
section = doc.sections[0]
section.page_width = Cm(21.0)
section.page_height = Cm(29.7)
section.left_margin = Cm(2.2)
section.right_margin = Cm(2.2)
section.top_margin = Cm(2.0)
section.bottom_margin = Cm(2.0)


def set_style_font(style, cn_font="SimSun", en_font="Times New Roman",
                   size=11.5, bold=False, color=None):
    """Set font for a style element."""
    style.font.name = en_font
    style.font.size = Pt(size)
    style.font.bold = bold
    if color:
        style.font.color.rgb = color

    rpr = style.element.rPr
    if rpr is None:
        rpr = OxmlElement("w:rPr")
        style.element.append(rpr)

    rFonts = rpr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rpr.insert(0, rFonts)

    rFonts.set(qn("w:eastAsia"), cn_font)
    rFonts.set(qn("w:ascii"), en_font)
    rFonts.set(qn("w:hAnsi"), en_font)
    for attr in ["w:eastAsiaTheme", "w:asciiTheme",
                 "w:hAnsiTheme", "w:cstheme"]:
        key = qn(attr)
        if key in rFonts.attrib:
            del rFonts.attrib[key]


style_configs = {
    "Normal": {"cn": "SimSun", "size": 11.5},
    "Heading 1": {"cn": "SimHei", "size": 16, "bold": True,
                  "color": RGBColor(23, 50, 77)},
    "Heading 2": {"cn": "SimHei", "size": 14, "bold": True,
                  "color": RGBColor(23, 50, 77)},
    "Heading 3": {"cn": "SimHei", "size": 12.5, "bold": True,
                  "color": RGBColor(23, 50, 77)},
    "Title": {"cn": "SimHei", "size": 22, "bold": True,
              "color": RGBColor(23, 50, 77)},
    "Subtitle": {"cn": "SimSun", "size": 12,
                 "color": RGBColor(91, 105, 117)},
    "Caption": {"cn": "FangSong", "size": 10.5},
}

for style_name, cfg in style_configs.items():
    try:
        style = doc.styles[style_name]
        set_style_font(style,
                       cn_font=cfg.get("cn", "SimSun"),
                       size=cfg.get("size", 11.5),
                       bold=cfg.get("bold", False),
                       color=cfg.get("color", None))
    except KeyError:
        print(f"Style not found: {style_name}")

output_dir = r"C:\Obsidion\妙妙屋\11-模板\scripts\templates"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "custom-reference.docx")
doc.save(output_path)
print(f"Custom reference docx saved: {output_path}")
print(f"Size: {os.path.getsize(output_path)} bytes")
