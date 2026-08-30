# Temporary audit: find lines where inline text is immediately followed by `|`,
# which can break pipe-table parsing in pandoc (text and table header on one line).
import pathlib
import re

root = pathlib.Path(r"C:\Obsidion\妙妙屋")
roots = [
    root / "04-题库",
    root / "04-课件" / "习题集" / "习题书-教师版",
]

# Any non-space char glued to `|` that does not start a table row.
pattern = re.compile(r"[^\s|\\\[\]<>\-_:]{1}[\|]")

for base in roots:
    print(f"=== {base.relative_to(root)} ===")
    total = 0
    hits = []
    for p in base.rglob("*.md"):
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                # Exclude obvious link rows / metadata / separators
                if line.lstrip().startswith("|"):
                    continue
                # Exclude wiki-link aliases `[[path|alias]]` and quote metadata.
                if "[[" in line:
                    continue
                if line.lstrip().startswith(">") and not line.lstrip().startswith("> **"):
                    continue
                hits.append((p, i, line))
    total = len(hits)
    print(f"--- total {total} ---")
    out = root / "_tmp_malformed_table_hits.txt"
    with out.open("w", encoding="utf-8") as fh:
        for p, i, line in hits:
            rel = p.relative_to(root)
            fh.write(f"{rel}:{i}: {line}\n")
