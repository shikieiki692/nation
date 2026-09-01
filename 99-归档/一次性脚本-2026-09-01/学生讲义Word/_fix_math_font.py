"""Post-process docx to set math font to Times New Roman."""
import xml.etree.ElementTree as ET
from zipfile import ZipFile
import shutil, sys

def fix_math_font(docx_path):
    tmp_path = docx_path + '.tmp'
    with ZipFile(docx_path, 'r') as zin, ZipFile(tmp_path, 'w') as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/settings.xml':
                root = ET.fromstring(data)
                ns_m = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
                ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
                # Find or create mathPr
                math_pr = root.find('{%s}mathPr' % ns_m)
                if math_pr is None:
                    math_pr = ET.SubElement(root, '{%s}mathPr' % ns_m)
                # Set math font
                math_font = math_pr.find('{%s}mathFont' % ns_m)
                if math_font is None:
                    math_font = ET.SubElement(math_pr, '{%s}mathFont' % ns_m)
                math_font.set('{%s}val' % ns_m, 'Times New Roman')
                # Also set mathFontName
                math_font_name = math_pr.find('{%s}mathFontName' % ns_m)
                if math_font_name is None:
                    math_font_name = ET.SubElement(math_pr, '{%s}mathFontName' % ns_m)
                math_font_name.set('{%s}val' % ns_m, 'Times New Roman')
                data = ET.tostring(root, xml_declaration=True, encoding='UTF-8')
            zout.writestr(item, data)
    shutil.move(tmp_path, docx_path)
    print(f'Math font set to Times New Roman: {docx_path}')

if __name__ == '__main__':
    for p in sys.argv[1:]:
        fix_math_font(p)
