# Temporary diagnostic for adjacent image embeds in a table cell.
import pathlib
import pypandoc
import zipfile

root = pathlib.Path(r"C:\Obsidion\妙妙屋")
md = root / "_tmp_adjacent_test.md"
out = root / "_tmp_adjacent_test.docx"
media = root / "媒体仓库"

a = "83e57661d60a63ef63f4adc374933b9b0eae8008c0ba4d5bb90d535d60f041dc.jpg"
b = "0e3e06d7b30d7fdc30b0da9836fd9e8dfe42f27e97ba24f9e478a60e3a374cd1.jpg"
assert (media / a).exists(), a
assert (media / b).exists(), b

cases = {
    "table_space": f"| 名称 | 数值 | 图 |\n|---|---|---|\n| α-氟代酰胺 | 33.6 | ![]({a}) ![]({b}) |\n",
    "table_nospace": f"| 名称 | 数值 | 图 |\n|---|---|---|\n| α-氟代酰胺 | 33.6 | ![]({a})![]({b}) |\n",
    "plain_space": f"图：![]({a}) ![]({b})\n",
    "plain_nospace": f"图：![]({a})![]({b})\n",
}

for name, text in cases.items():
    md.write_text(text, encoding="utf-8")
    try:
        pypandoc.convert_file(
            str(md),
            "docx",
            outputfile=str(out),
            extra_args=[
                "--from=markdown+pipe_tables",
                "--to=docx",
                f"--resource-path={root};{media}",
                f"--reference-doc={root / '11-模板' / 'scripts' / 'templates' / 'custom-reference.docx'}",
            ],
        )
        with zipfile.ZipFile(out) as z:
            names = [n for n in z.namelist() if n.startswith("word/media/") and not n.endswith("/")]
        print(name, "media_count=", len(names))
    except Exception as exc:
        print(name, "ERROR", repr(exc))
