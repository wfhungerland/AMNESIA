"""Shared look for all figures of the manuscript and the appendix.

Sans-serif type (Inter), recessive axes, a light horizontal grid, direct labels and one
validated categorical palette (blue, orange, aqua, yellow, assigned in this order).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = Path(__file__).resolve().parents[2]
D, F = R / "data", R / "manuscript" / "figures"

INK, MUTED, GRID, SOFT = "#1d2733", "#6b7785", "#e3e7ec", "#f2f4f7"
BLUE, ORANGE, AQUA, YELLOW = "#257de0", "#f47230", "#00b894", "#f2a600"
GRAY = "#b4bcc6"
# sequential blue ramp (light to dark) for ordered scores
RAMP = ["#c6dcf5", "#8fbcec", "#5a9be3", "#2f74c8", "#174b8c"]

plt.rcParams.update({
    "font.family": "Inter", "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5,
    "axes.edgecolor": GRAY, "axes.linewidth": 0.7, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "xtick.major.size": 3, "xtick.major.width": 0.7, "ytick.major.size": 0,
    "lines.linewidth": 2, "lines.solid_capstyle": "round", "lines.solid_joinstyle": "round",
    "legend.frameon": False, "legend.fontsize": 8, "pdf.fonttype": 42, "svg.fonttype": "none",
    "figure.dpi": 100, "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.04,
})


def tidy(ax, grid="y"):
    """Bottom axis only, light grid behind the data."""
    ax.spines[["top", "right", "left"]].set_visible(False)
    if grid:
        ax.grid(axis=grid, color=GRID, lw=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", pad=2)


def title(ax, text):
    ax.set_title(text, loc="left", fontsize=9, fontweight="semibold", color=INK, pad=8)


def note(ax, x, y, text, **kw):
    """Small muted annotation in data coordinates."""
    kw = {"fontsize": 7.5, "color": MUTED, **kw}
    return ax.text(x, y, text, **kw)


def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(F / f"{name}.{ext}")
    plt.close(fig)
