#!/usr/bin/env python3
"""Fix remaining bare Greek letters that were missed."""
import re

FILE = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（完整版）.md"

with open(FILE, "r", encoding="utf-8") as f:
    c = f.read()

# Fix bare σ before \* (escaped asterisk) - σ* patterns
c = re.sub(r'(?<!\$)σ(\\[*])', r'$σ$\1', c)

# Fix bare σ in 'σ能级'
c = re.sub(r'(?<!\$)σ(能级)', r'$σ$\1', c)

# Fix bare σ in 'σ在前' inside bold
c = re.sub(r'(?<!\$)σ(在前)', r'$σ$\1', c)

# Fix bare σ in 'σ先填'
c = re.sub(r'(?<!\$)σ(先填)', r'$σ$\1', c)

# Fix bare σ in 'σ键' 'σ配体' 'σ给体' 'σ受体' 'σ轨道' 'σ电子'
c = re.sub(r'(?<!\$)σ(键|配体|给体|受体|轨道|电子|离域)', r'$σ$\1', c)

# Fix bare π in 'π先于σ' etc
c = re.sub(r'(?<!\$)(?<!\\)π(先于|先填|受体|给体|键|电子|体系)', r'$π$\1', c)

# Fix σ/π in header text
c = c.replace('——σ/π理解框架', '——$σ$/$π$理解框架')
c = c.replace('**σ/π理解框架**', '**$σ$/$π$理解框架**')

# Fix bare σ in table cell: σ\*(C-F) patterns
c = re.sub(r'(?<!\$)σ(\\[*]\(C-F\))', r'$σ$\1', c)

# Fix bare σ in 'σ电子离域'
c = re.sub(r'(?<!\$)σ(电子离域)', r'$σ$\1', c)

# Clean up any double $$$$ → $$
c = re.sub(r'\${3,}', r'$', c)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(c)

# Count remaining bare Greek
lines = c.split('\n')
bare = 0
for line in lines:
    parts = re.split(r'\$[^$]+\$', line)
    for p in parts:
        bare += len(re.findall(r'[σπΔδλμχθρψω]', p))
print(f"Remaining bare Greek outside math: {bare}")

# Also check specific problem lines
for i, line in enumerate(lines, 1):
    parts = re.split(r'\$[^$]+\$', line)
    for p in parts:
        greeks = re.findall(r'[σπΔδλμχθρψω]', p)
        if greeks:
            print(f"  Line {i}: {greeks} in: {p[:80]}...")
