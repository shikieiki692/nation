"""
Post-process docx to replace 等线 (DengXian) with 黑体 (SimHei) for Chinese text,
and set math font to Times New Roman.
"""
import xml.etree.ElementTree as ET
from zipfile import ZipFile
import shutil, sys, os, re

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
}

def fix_fonts(docx_path):
    tmp_path = docx_path + '.tmp'
    with ZipFile(docx_path, 'r') as zin, ZipFile(tmp_path, 'w') as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)

            if item.filename == 'word/styles.xml':
                # Use regex replacement for styles.xml to avoid XML parsing issues
                text = data.decode('utf-8')
                original = text
                text = text.replace('等线', '黑体')
                text = text.replace('DengXian', 'SimHei')
                if text != original:
                    count = original.count('等线') + original.count('DengXian')
                    print(f'  Replaced {count} font references in styles.xml')
                data = text.encode('utf-8')

            if item.filename == 'word/settings.xml':
                text = data.decode('utf-8')
                # Set math font to Times New Roman via regex
                if 'm:mathFont' not in text:
                    # Insert mathPr if not present
                    text = text.replace('</w:settings>', '<m:mathPr xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:mathFont m:val="Times New Roman"/><m:mathFontName m:val="Times New Roman"/></m:mathPr></w:settings>')
                else:
                    text = text.replace('m:mathFont m:val="', 'm:mathFont m:val="Times New Roman" m:val="')
                    # Simpler: just replace the value
                    import re
                    text = re.sub(r'(<m:mathFont[^>]*m:val=")[^"]*"', r'\1Times New Roman"', text)
                    text = re.sub(r'(<m:mathFontName[^>]*m:val=")[^"]*"', r'\1Times New Roman"', text)
                data = text.encode('utf-8')

            zout.writestr(item, data)
    # Try multiple methods to replace the file
    try:
        os.replace(tmp_path, docx_path)
    except PermissionError:
        # If file is locked, try copying and deleting
        import time
        time.sleep(1)
        try:
            os.remove(docx_path)
            time.sleep(0.5)
            os.replace(tmp_path, docx_path)
        except:
            # Last resort: write to a new filename
            new_path = docx_path.replace('.docx', '_fixed.docx')
            shutil.move(tmp_path, new_path)
            docx_path = new_path
    print(f'Fixed: {docx_path}')

if __name__ == '__main__':
    for p in sys.argv[1:]:
        fix_fonts(p)
