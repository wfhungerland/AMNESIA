"""Abbildung E2: Der US-Kongress und die Aufsteiger.
(a) China in Wirtschaftsdebatten 1995-2025 (Congressional Record, govinfo CREC, Titelfilter crec_econ_v1).
(b) Stichprobentage 1955-2025: Japan bzw. China hoechstens 30 Woerter von einem Wettbewerbswort, je 1 Mio. Woerter
    (gebundener Record CRECB bis 1994, taeglicher Record CREC ab 1995)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

R = Path(__file__).resolve().parents[2]
y = pd.read_csv(R / "data" / "ds1_crec_salience.csv")
b = pd.read_csv(R / "data" / "ds1_crecb_years.csv").sort_values("year")
INK, MUTED, GRID, LINE, LINE2 = "#1f2328", "#59636e", "#d8dee4", "#2f5d8a", "#b0b7bf"
plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.edgecolor": MUTED,
                     "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED})
fig, (a, c) = plt.subplots(2, 1, figsize=(6.3, 5.6))

a.plot(y.year, y.china_hits_per_100k_words, color=LINE, lw=1.6, label="China")
a.plot(y.year, y.japan_hits_per_100k_words, color=LINE2, lw=1.2, label="Japan")
a.plot(y.year, y.mexico_hits_per_100k_words, color=LINE2, lw=1.2, ls="--", label="Mexico")
top = a.get_ylim()[1]
for x, lab in [(2001, "WTO\naccession"), (2010, "manufacturing\nmilestone"), (2018, "Section 301\ntariffs")]:
    a.axvline(x, color=MUTED, lw=0.8, ls=":")
    a.text(x + 0.3, top * 0.97, lab, va="top", color=MUTED, fontsize=7.5)
a.set_title("(a) Mentions per 100,000 words of economic debate, 1995-2025", loc="left", fontsize=9, color=INK)
a.set_xlim(1995, 2025)
a.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.0, 0.8), fontsize=8)

j = b[b.source == "CRECB"]
k = b[b.source == "CREC"]
c.plot(j.year, j.japan_comp_per_1m, color=LINE, lw=1.4, label="Japan near a competition term (bound Record)")
c.plot(k.year, k.china_comp_per_1m, color=INK, lw=1.4, label="China near a competition term (daily Record)")
c.plot(k.year, k.japan_comp_per_1m, color=LINE, lw=1.0, ls="--")
top = c.get_ylim()[1]
for x, lab in [(1969, "steel"), (1970, ""), (1980, "cars"), (1986, "semi-\nconductor\nagreement")]:
    if lab:
        c.axvline(x, color=MUTED, lw=0.8, ls=":")
        c.text(x + 0.3, top * 0.97, lab, va="top", color=MUTED, fontsize=7.5)
c.set_title("(b) Sampled sitting days: mentions near a competition term per million words, 1955-2025", loc="left", fontsize=9, color=INK)
c.set_xlim(1955, 2025)
c.set_xlabel("Year")
c.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.0, 0.75), fontsize=8)
for ax in (a, c):
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.spines[["top", "right"]].set_visible(False)
n = int(y.econ_granules.sum())
fig.text(0.01, -0.03, f"Source: Congressional Record (govinfo, CREC and CRECB). (a) {n:,} economic granules, title filter crec_econ_v1. "
         "(b) 20 random sitting days per year\n(bound Record, 1955-1994) and 10 (daily Record, 1995-2025), full text of all chambers; "
         "dashed line: Japan after 1994.", fontsize=7, color=MUTED)
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(R / "manuscript" / "figures" / f"fig_e2_crec.{ext}", dpi=200, bbox_inches="tight")
