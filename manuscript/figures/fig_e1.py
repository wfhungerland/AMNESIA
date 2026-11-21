"""Abbildung E1: Deutschland in britischen Wirtschaftsdebatten 1850-1914 (Historic Hansard)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

R = Path(__file__).resolve().parents[2]
y = pd.read_csv(R / "data" / "ds1_hansard_salience.csv")
INK, MUTED, GRID, LINE = "#1f2328", "#59636e", "#d8dee4", "#2f5d8a"
plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.edgecolor": MUTED,
                     "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED})
fig, a0 = plt.subplots(1, 1, figsize=(6.3, 2.9))
ax = [a0]
panels = [("germany_hits_per_100k_words", "Mentions of Germany per 100,000 words of economic debate")]
for a, (col, title) in zip(ax, panels):
    v = y[col] * (100 if col == "competition_share" else 1)
    a.axvspan(1850, 1870, color="#eef1f4", lw=0)
    a.plot(y.year, v, color=LINE, lw=1.6)
    a.plot(y.year, v.rolling(5, center=True).mean(), color=INK, lw=1.0, ls="--")
    for x, lab in [(1870, "dyes"), (1893, "steel")]:
        a.axvline(x, color=MUTED, lw=0.8, ls=":")
    a.set_title(title, loc="left", fontsize=9, color=INK)
    a.grid(axis="y", color=GRID, lw=0.6)
    a.spines[["top", "right"]].set_visible(False)
    a.set_xlim(1850, 1914)
top = ax[0].get_ylim()[1]
ax[0].text(1860, top * 0.92, "absorption\nphase", ha="center", va="top", color=MUTED, fontsize=8)
for x, lab in [(1870, "dye milestone"), (1893, "steel milestone")]:
    ax[0].text(x + 0.6, top * 0.92, lab, va="top", color=MUTED, fontsize=8)
ax[0].plot([], [], color=LINE, lw=1.6, label="annual")
ax[0].plot([], [], color=INK, lw=1.0, ls="--", label="5-year centred mean")
ax[0].legend(frameon=False, loc="upper left", bbox_to_anchor=(0.0, 0.72), fontsize=8)
ax[0].set_xlabel("Year")
fig.text(0.01, -0.06, "Source: Historic Hansard (UK Parliament), Commons and Lords; 15,126 economic debates selected by title filter econ_v2.",
         fontsize=7, color=MUTED)
for ext in ("pdf", "png"):
    fig.savefig(R / "manuscript" / "figures" / f"fig_e1_hansard.{ext}", dpi=200, bbox_inches="tight")
