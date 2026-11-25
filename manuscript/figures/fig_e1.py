"""Figure E.1: Germany in British economic debates, 1850-1914 (Historic Hansard)."""
import matplotlib.pyplot as plt
import pandas as pd

from style import BLUE, D, INK, MUTED, SOFT, note, save, tidy, title

y = pd.read_csv(D / "ds1_hansard_salience.csv")
ms = pd.read_csv(D / "ds1_milestones.csv").set_index("milestone_id")
fig, ax = plt.subplots(figsize=(6.6, 3.0))
v = y.germany_hits_per_100k_words
ax.axvspan(1850, int(ms.loc["M-DE-DYE", "year"]), color=SOFT, lw=0, zorder=0)
ax.fill_between(y.year, v, color=BLUE, alpha=0.12, lw=0, zorder=2)
ax.plot(y.year, v, color=BLUE, lw=1.3, zorder=3, label="annual")
ax.plot(y.year, v.rolling(5, center=True).mean(), color=INK, lw=1.6, zorder=4, label="five-year centred mean")
ax.set_ylim(0, 150)
for m, lab in [("M-DE-DYE", "dye milestone"), ("M-DE-STEEL", "steel milestone")]:
    x = int(ms.loc[m, "year"])
    ax.axvline(x, color=MUTED, lw=0.7, ls=(0, (2, 2)), zorder=1)
    note(ax, x + 0.6, 147, lab, va="top")
note(ax, 1851, 147, "absorption phase", va="top")
ax.set_xlim(1850, 1914)
ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.88), handlelength=1.6)
title(ax, "Mentions of Germany per 100,000 words of economic debate")
tidy(ax)
n = int(y.econ_sections.sum())
fig.text(0.0, -0.04, f"Source: Historic Hansard (UK Parliament), Commons and Lords; {n:,} economic debates selected by title filter.",
         fontsize=7, color=MUTED)
save(fig, "fig_e1_hansard")
