"""Abbildung E2: China in Wirtschaftsdebatten des US-Kongresses 1995-2025 (Congressional Record, govinfo CREC)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

R = Path(__file__).resolve().parents[2]
y = pd.read_csv(R / "data" / "ds1_crec_salience.csv")
INK, MUTED, GRID, LINE, LINE2 = "#1f2328", "#59636e", "#d8dee4", "#2f5d8a", "#b0b7bf"
plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.edgecolor": MUTED,
                     "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED})
fig, a = plt.subplots(1, 1, figsize=(6.3, 2.9))
a.plot(y.year, y.china_hits_per_100k_words, color=LINE, lw=1.6, label="China")
a.plot(y.year, y.japan_hits_per_100k_words, color=LINE2, lw=1.2, label="Japan")
a.plot(y.year, y.mexico_hits_per_100k_words, color=LINE2, lw=1.2, ls="--", label="Mexico")
top = a.get_ylim()[1]
for x, lab in [(2001, "WTO\naccession"), (2010, "manufacturing\nmilestone"), (2018, "Section 301\ntariffs")]:
    a.axvline(x, color=MUTED, lw=0.8, ls=":")
    a.text(x + 0.3, top * 0.97, lab, va="top", color=MUTED, fontsize=7.5)
a.set_title("Mentions per 100,000 words of economic debate, US Congress", loc="left", fontsize=9, color=INK)
a.grid(axis="y", color=GRID, lw=0.6)
a.spines[["top", "right"]].set_visible(False)
a.set_xlim(1995, 2025)
a.set_xlabel("Year")
a.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.0, 0.85), fontsize=8)
n = int(y.econ_granules.sum())
fig.text(0.01, -0.06, f"Source: Congressional Record (govinfo, CREC), House, Senate and Extensions; {n:,} economic granules selected by title filter crec_econ_v1.",
         fontsize=7, color=MUTED)
for ext in ("pdf", "png"):
    fig.savefig(R / "manuscript" / "figures" / f"fig_e2_crec.{ext}", dpi=200, bbox_inches="tight")
