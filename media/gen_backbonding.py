"""
Textbook-quality 2D schematic: CO sigma-donation + pi-backbonding
(synergic bonding) to a metal centre.

v4 – clean, no arrow crossing, well-spaced.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# ── Canvas ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(-0.5, 14.5)
ax.set_ylim(-0.5, 8.5)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("white")

# ── Palette ───────────────────────────────────────────────────────────
BLUE      = "#1E88E5"
BLUE_DARK = "#1565C0"
BLUE_LT   = "#BBDEFB"
RED       = "#E53935"
RED_DARK  = "#C62828"
GREY      = "#757575"
LABEL     = "#212121"
ATOM_BG   = "#90A4AE"

# ── Helpers ───────────────────────────────────────────────────────────
def filled(cx, cy, r, c=BLUE, ec=BLUE_DARK, lw=2.0):
    ax.add_patch(mpatches.Circle((cx, cy), r, fc=c, ec=ec, lw=lw, zorder=2))

def empty(cx, cy, r, ec=RED, lw=2.0):
    ax.add_patch(mpatches.Circle((cx, cy), r, fc="white", ec=ec,
                                 lw=lw, ls="--", zorder=2))

def atom(cx, cy, r, lbl):
    ax.add_patch(mpatches.Circle((cx, cy), r, fc=ATOM_BG, ec="#455A64",
                                 lw=2.0, zorder=3))
    ax.text(cx, cy, lbl, ha="center", va="center", fontsize=14,
            fontweight="bold", color="white", zorder=4)

def straight_arrow(x0, y0, x1, y1, color=RED, lw=3.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.30",
                                color=color, lw=lw, shrinkA=0, shrinkB=0),
                zorder=5)

def curved_arrow(x0, y0, x1, y1, rad, color=RED, lw=3.0):
    ax.add_patch(FancyArrowPatch(
        (x0, y0), (x1, y1),
        arrowstyle="->,head_width=0.25,head_length=0.30",
        connectionstyle=f"arc3,rad={rad}",
        color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=5))

def tag(text, x, y, **kw):
    d = dict(ha="center", va="center", fontsize=11, color=RED,
             fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=RED,
                       lw=1.2, alpha=0.95), zorder=6)
    d.update(kw); ax.text(x, y, text, **d)


# =====================================================================
#  Geometry
# =====================================================================
AX = 4.5   # bond-axis y

# ── CO molecule (left) ────────────────────────────────────────────────
C_x, O_x = 2.2, 3.5
ar = 0.34

atom(C_x, AX, ar, "C")
atom(O_x, AX, ar, "O")

for dy in [-0.13, 0, 0.13]:
    ax.plot([C_x + ar + 0.04, O_x - ar - 0.04], [AX + dy] * 2,
            color=GREY, lw=1.8, zorder=1)

# ── CO HOMO 3σ  (filled, on C, pointing left) ────────────────────────
homo_x, homo_y = C_x - 1.1, AX
homo_r = 0.55
filled(homo_x, homo_y, homo_r)
ax.text(homo_x, homo_y, "+", ha="center", va="center", fontsize=14,
        fontweight="bold", color="white", zorder=5)
# small minus back-lobe
filled(C_x - 0.15, AX - 0.9, 0.28, BLUE_LT, BLUE_DARK, lw=1.2)
ax.text(C_x - 0.15, AX - 0.9, "−", ha="center", va="center",
        fontsize=10, color=BLUE_DARK, zorder=5)

ax.text(homo_x, homo_y + homo_r + 0.3, "HOMO 3σ", ha="center",
        va="bottom", fontsize=11, color=BLUE_DARK, fontstyle="italic", zorder=5)
ax.text(homo_x, homo_y - homo_r - 0.3, "(filled)", ha="center",
        va="top", fontsize=9, color=BLUE_DARK, zorder=5)

# ── CO LUMO π*  (empty, above & below, between C-O) ──────────────────
pi_cx = (C_x + O_x) / 2
pi_up, pi_dn = AX + 1.3, AX - 1.3
pi_r = 0.48

empty(pi_cx, pi_up, pi_r)
ax.text(pi_cx, pi_up, "+", ha="center", va="center", fontsize=13,
        color=RED, zorder=5)
empty(pi_cx, pi_dn, pi_r)
ax.text(pi_cx, pi_dn, "−", ha="center", va="center", fontsize=13,
        color=RED, zorder=5)

ax.text(pi_cx, pi_up + pi_r + 0.25, "LUMO π*", ha="center",
        va="bottom", fontsize=11, color=RED_DARK, fontstyle="italic", zorder=5)
ax.text(pi_cx, pi_dn - pi_r - 0.25, "(empty)", ha="center",
        va="top", fontsize=9, color=RED_DARK, zorder=5)

ax.text((C_x + O_x) / 2, AX + 3.0, "CO", ha="center", fontsize=14,
        fontweight="bold", color=LABEL, zorder=5)


# ── Metal centre (right) ─────────────────────────────────────────────
M_x = 11.5
met_r = 0.60

ax.add_patch(mpatches.Circle((M_x, AX), met_r, fc="#FF8F00", ec="#E65100",
                             lw=2.4, zorder=3))
ax.text(M_x, AX, "M", ha="center", va="center", fontsize=17,
        fontweight="bold", color="white", zorder=4)

# Metal dσ* (empty, left of M)
dsig_x, dsig_y = M_x - 1.55, AX
dsig_r = 0.52
empty(dsig_x, dsig_y, dsig_r)
ax.text(dsig_x, dsig_y, "dσ*", ha="center", va="center", fontsize=10.5,
        color=RED, fontweight="bold", zorder=5)
ax.text(dsig_x, dsig_y - dsig_r - 0.28, "empty", ha="center",
        va="top", fontsize=9, color=RED_DARK, zorder=5)

# Metal dπ (filled, above M)
dpi_x, dpi_y = M_x, AX + 1.55
dpi_r = 0.52
filled(dpi_x, dpi_y, dpi_r)
ax.text(dpi_x, dpi_y, "dπ", ha="center", va="center", fontsize=10.5,
        color="white", fontweight="bold", zorder=5)
ax.text(dpi_x, dpi_y + dpi_r + 0.25, "filled", ha="center",
        va="bottom", fontsize=9, color=BLUE_DARK, zorder=5)

ax.text(M_x, AX + 3.0, "Metal", ha="center", fontsize=14,
        fontweight="bold", color=LABEL, zorder=5)


# ── Dashed M-CO axis ─────────────────────────────────────────────────
ax.plot([O_x + ar + 0.06, M_x - met_r - 0.06], [AX, AX],
        color=GREY, lw=1.5, ls="--", zorder=1)


# =====================================================================
#  Arrow 1 — SIGMA DONATION:  CO 3σ  →  Metal dσ*
#  Straight, slightly below axis so it sits clearly below the bond line
# =====================================================================
a1_y = AX - 0.55        # below the axis
a1_x0 = homo_x + homo_r + 0.15
a1_x1 = dsig_x - dsig_r - 0.15
straight_arrow(a1_x0, a1_y, a1_x1, a1_y, lw=3.2)

tag("σ donation", (a1_x0 + a1_x1) / 2, a1_y - 0.65)


# =====================================================================
#  Arrow 2 — PI BACKDONATION:  Metal dπ  →  CO π*
#  Arcs above, right -> left, rad > 0 curves upward (concave down)
# =====================================================================
a2_x0 = dpi_x - 0.15
a2_y0 = dpi_y + dpi_r + 0.10
a2_x1 = pi_cx + 0.15
a2_y1 = pi_up + pi_r + 0.10

curved_arrow(a2_x0, a2_y0, a2_x1, a2_y1, rad=0.32, lw=3.2)

tag("π backdonation", (a2_x0 + a2_x1) / 2, max(a2_y0, a2_y1) + 0.7)


# =====================================================================
#  Title
# =====================================================================
ax.text(7.0, 7.8, "Synergic Bonding:  M – CO",
        ha="center", va="center", fontsize=17, fontweight="bold",
        color=LABEL,
        bbox=dict(boxstyle="round,pad=0.5", fc="#FFF9C4", ec="#F9A825",
                  lw=1.5, alpha=0.95), zorder=7)


# ── Legend ─────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(fc=BLUE, ec=BLUE_DARK, label="Filled orbital (e⁻ donor)"),
    mpatches.Patch(fc="white", ec=RED, ls="--",
                   label="Empty orbital (e⁻ acceptor)"),
    plt.Line2D([0], [0], color=RED, lw=2.5, marker=">",
               markersize=8, label="Electron flow"),
]
ax.legend(handles=legend_items, loc="lower center", fontsize=10,
          frameon=True, fancybox=True, edgecolor="#BDBDBD",
          ncol=3, bbox_to_anchor=(0.5, -0.04))


# ── Save ──────────────────────────────────────────────────────────────
out = r"C:\Obsidion\妙妙屋\media\sigma-pi-backbonding-synergy.png"
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white",
            pad_inches=0.3)
plt.close(fig)
print(f"Saved -> {out}")
