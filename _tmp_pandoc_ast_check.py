# Temporary diagnostic: does a stray `<->` make pandoc swallow following images?
import pathlib
import pypandoc

root = pathlib.Path(r"C:\Obsidion\妙妙屋")
md = root / "_tmp_ast_check.md"

a = "83e57661d60a63ef63f4adc374933b9b0eae8008c0ba4d5bb90d535d60f041dc.jpg"
b = "0e3e06d7b30d7fdc30b0da9836fd9e8dfe42f27e97ba24f9e478a60e3a374cd1.jpg"

cases = {
    "with_arrow": (
        "**8.2.4** 判断依据：**酰胺中羰基的极性明显强于酯中的羰基**。"
        "酰胺存在电荷分离共振式 $\\ce{R-C(=O)-NHR <-> R-C(-O^-)=N^+HR}$，"
        "使 C=O 极性更大 → anti 与 syn 的能量差更大。amide 中还有 F···H–N 氢键"
        "（本质是静电相互作用）进一步稳定 anti-1。**实验数据：**"
        "| 物种 | anti 与 syn 能量差 / (kJ mol⁻¹) |\n"
        "|:---|:---:|\n"
        "| α-氟代醛 | 7.1 |\n"
        "| α-氟代酮 | 9.2 |\n"
        "| α-氟代酯 | 18.9 |\n"
        f"| α-氟代酰胺 | 33.6 |![]({a})![]({b})\n"
    ),
    "no_arrow": (
        "**8.2.4** 判断依据：**酰胺中羰基的极性明显强于酯中的羰基**。"
        "酰胺存在电荷分离共振式 $\\ce{R-C(=O)-NHR R-C(-O^-)=N^+HR}$，"
        "使 C=O 极性更大 → anti 与 syn 的能量差更大。amide 中还有 F···H–N 氢键"
        "（本质是静电相互作用）进一步稳定 anti-1。**实验数据：**"
        "| 物种 | anti 与 syn 能量差 / (kJ mol⁻¹) |\n"
        "|:---|:---:|\n"
        "| α-氟代醛 | 7.1 |\n"
        "| α-氟代酮 | 9.2 |\n"
        "| α-氟代酯 | 18.9 |\n"
        f"| α-氟代酰胺 | 33.6 |![]({a})![]({b})\n"
    ),
    "escaped_arrow": (
        "**8.2.4** 判断依据：**酰胺中羰基的极性明显强于酯中的羰基**。"
        "酰胺存在电荷分离共振式 $\\ce{R-C(=O)-NHR \\textless-\\textgreater R-C(-O^-)=N^+HR}$，"
        "使 C=O 极性更大 → anti 与 syn 的能量差更大。amide 中还有 F···H–N 氢键"
        "（本质是静电相互作用）进一步稳定 anti-1。**实验数据：**"
        "| 物种 | anti 与 syn 能量差 / (kJ mol⁻¹) |\n"
        "|:---|:---:|\n"
        "| α-氟代醛 | 7.1 |\n"
        "| α-氟代酮 | 9.2 |\n"
        "| α-氟代酯 | 18.9 |\n"
        f"| α-氟代酰胺 | 33.6 |![]({a})![]({b})\n"
    ),
}

for name, text in cases.items():
    md.write_text(text, encoding="utf-8")
    try:
        ast = pypandoc.convert_file(str(md), "json", extra_args=["--from=markdown+pipe_tables"])
        img_count = ast.count('"Image"')
        print(name, "image_nodes=", img_count)
        low = ast.lower()
        for token in ["<->", "\\\\textless", "83e57661", "0e3e06d7"]:
            print("   has", token, ":", token.lower() in low)
    except Exception as exc:
        print(name, "ERROR", repr(exc))
