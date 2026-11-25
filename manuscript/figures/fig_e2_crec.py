"""Figure G.1: the US Congress and the challengers.
(a) China, Japan and Mexico in economic debates 1995-2025 (daily Congressional Record, title filter).
(b) Sampled sitting days 1955-2025: Japan or China within 30 words of a competition term, per million words
    (bound Record to 1994, daily Record from 1995)."""
import matplotlib.pyplot as plt
import pandas as pd

from style import BLUE, D, GRAY, MUTED, ORANGE, note, save, tidy, title

y = pd.read_csv(D / "ds1_crec_salience.csv")
b = pd.read_csv(D / "ds1_crecb_years.csv").sort_values("year")
fig, (a, c) = plt.subplots(2, 1, figsize=(6.6, 5.6))


def events(ax, items, top):
    for x, lab in items:
        ax.axvline(x, color=MUTED, lw=0.7, ls=(0, (2, 2)), zorder=1)
        note(ax, x + 0.3, top, lab, va="top", fontsize=7)


a.plot(y.year, y.china_hits_per_100k_words, color=ORANGE, lw=2, zorder=3)
a.plot(y.year, y.japan_hits_per_100k_words, color=BLUE, lw=1.4, zorder=3)
a.plot(y.year, y.mexico_hits_per_100k_words, color=GRAY, lw=1.4, zorder=3)
a.set_xlim(1995, 2027.5)
top = a.get_ylim()[1] * 1.12
a.set_ylim(0, top)
for col, lab, s in [("china_hits_per_100k_words", "China", ORANGE), ("japan_hits_per_100k_words", "Japan", BLUE),
                    ("mexico_hits_per_100k_words", "Mexico", GRAY)]:
    a.text(y.year.iloc[-1] + 0.4, y[col].iloc[-1] + {"Mexico": 12, "Japan": -8}.get(lab, 0), lab, color=s if s != GRAY else MUTED, fontsize=8.5,
           fontweight="semibold", va="center")
events(a, [(2001, "WTO accession"), (2010, "manufacturing\nmilestone"), (2018, "Section 301\ntariffs")], top * 0.99)
title(a, "(a) Mentions per 100,000 words of economic debate, 1995-2025")
tidy(a)

j = b[b.source == "CRECB"]
k = b[b.source == "CREC"]
c.plot(j.year, j.japan_comp_per_1m, color=BLUE, lw=1.6, zorder=3)
c.plot(k.year, k.japan_comp_per_1m, color=BLUE, lw=1.2, ls=(0, (3, 2)), zorder=3)
c.plot(k.year, k.china_comp_per_1m, color=ORANGE, lw=1.6, zorder=3)
c.set_xlim(1955, 2030)
top = c.get_ylim()[1] * 1.12
c.set_ylim(0, top)
c.text(k.year.iloc[-1] + 0.5, k.china_comp_per_1m.iloc[-1], "China", color=ORANGE, fontsize=8.5, fontweight="semibold", va="center")
c.text(k.year.iloc[-1] + 0.5, k.japan_comp_per_1m.iloc[-1], "Japan", color=BLUE, fontsize=8.5, fontweight="semibold", va="center")
c.axvline(1994.5, color=GRAY, lw=0.7, zorder=1)
note(c, 1994, top * 0.58, "bound Record ", ha="right", fontsize=7)
note(c, 2001.5, top * 0.58, "daily Record", ha="left", fontsize=7)
events(c, [(1969, "steel"), (1980, "cars"), (1986, "semiconductor\nagreement")], top * 0.99)
title(c, "(b) Sampled sitting days: mentions near a competition term per million words, 1955-2025")
tidy(c)
n = int(y.econ_granules.sum())
fig.text(0.0, -0.02, f"Source: Congressional Record (govinfo). (a) {n:,} economic granules selected by title filter. "
         "(b) 20 random sitting days per year in the bound Record\n(1955-1994) and 10 in the daily Record (1995-2025), "
         "full text of all chambers.", fontsize=7, color=MUTED)
fig.tight_layout(h_pad=2.5)
save(fig, "fig_e2_crec")
