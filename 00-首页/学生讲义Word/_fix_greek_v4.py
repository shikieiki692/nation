#!/usr/bin/env python3
"""Fix remaining bare Δ and μ letters."""
import re

FILE = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（完整版）.md"

with open(FILE, "r", encoding="utf-8") as f:
    c = f.read()

# Fix bare ΔE patterns
c = re.sub(r'(?<!\$)Δ(E[₀₉]?)', r'$Δ$\1', c)
c = re.sub(r'(?<!\$)Δ(x|y|z)', r'$Δ$\1', c)
c = re.sub(r'(?<!\$)Δ(χ)', r'$Δ$\1', c)

# Fix bare μB patterns (Bohr magneton)
c = re.sub(r'(?<!\$)μ(B)', r'$μ$\1', c)

# Fix bare Δ in other contexts
c = re.sub(r'(?<!\$)Δ(?=[^E₀₉xyznμB\s])', r'$Δ$', c)

# Clean up $Δ$E → $ΔE$ (should be one math block)
c = re.sub(r'\$Δ\$E', r'$ΔE$', c)
c = re.sub(r'\$Δ\$x', r'$Δx$', c)
c = re.sub(r'\$Δ\$y', r'$Δy$', c)
c = re.sub(r'\$Δ\$z', r'$Δz$', c)
c = re.sub(r'\$Δ\$χ', r'$Δχ$', c)
c = re.sub(r'\$μ\$B', r'$μ_B$', c)

# Fix ΔE₀ and ΔE₉
c = re.sub(r'\$Δ\$E₀', r'$ΔE_0$', c)
c = re.sub(r'\$Δ\$E₉', r'$ΔE_9$', c)

# Clean up any triple $
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

# Show any remaining
for i, line in enumerate(lines, 1):
    parts = re.split(r'\$[^$]+\$', line)
    for p in parts:
        greeks = re.findall(r'[σπΔδλμχθρψω]', p)
        if greeks:
            print(f"  Line {i}: {greeks} in: ...{p.strip()[:60]}...")
