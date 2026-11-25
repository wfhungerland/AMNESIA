"""Figures 2 to 6 of the manuscript, from data/ (no smoothing, no interpolation).

Fig. 2  Export ratio challenger/incumbent in four sectors, with binding responses marked.
Fig. 3  Breadth of displacement: share of US manufactured exports in groups the challenger has overtaken.
Fig. 4  Start rates of instruments by years from a group's export crossover (broad instruments; antidumping cases).
Fig. 5  Parliamentary attention: Germany in British economic debates; Japan in the Congressional Record.
Fig. 6  TFP relative to the United States.
Call from the repository root: python3 manuscript/figures/fig_story.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

R = Path(__file__).resolve().parents[2]
D, F = R / "data", R / "manuscript" / "figures"
INK, MUTED, GRID = "#191919", "#666666", "#dddddd"
BLUE, ORANGE, AQUA, YELLOW = "#257de0", "#f47230", "#00b894", "#f2a600"
plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.edgecolor": MUTED, "axes.linewidth": 0.6,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": INK, "lines.linewidth": 2})


def tidy(ax, grid="y"):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis=grid, color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(F / f"{name}.{ext}", dpi=200, bbox_inches="tight")
    plt.close(fig)


ev = pd.read_csv(D / "ds1_events.csv")
ms = pd.read_csv(D / "ds1_milestones.csv").set_index("milestone_id")

# ---- Fig. 2: export ratios in four sectors
ex = pd.read_csv(D / "ds1_export_series.csv")
order = {"S1": 0, "S2": 1, "S3": 2, "HS": 3}
ex["o"] = ex.classification.map(order)
panels = [("JP-STEEL", "M-JP-STEEL", "Japan, steel (US = 1)"), ("JP-TV", "M-JP-TV", "Japan, television sets (US = 1)"),
          ("JP-AUTO", "M-JP-AUTO", "Japan, passenger cars (US = 1)"), ("CN-SOLAR", "M-CN-SOLAR", "China, solar cells (Germany = 1)")]
fig, axs = plt.subplots(2, 2, figsize=(6.5, 4.4), sharey=False)
for ax, (sec, mid, title) in zip(axs.flat, panels):
    s = ex[ex.sector == sec].sort_values("o").drop_duplicates(["role", "year"], keep="first")
    w = s.pivot(index="year", columns="role", values="value_usd").dropna()
    ratio = w.challenger / w.incumbent
    ax.plot(ratio.index, ratio.values, color=BLUE)
    ax.axhline(1, color=INK, lw=0.8)
    ax.set_yscale("log")
    ax.set_title(title, fontsize=9, loc="left", color=INK)
    tidy(ax)
    my = int(ms.loc[mid, "year"])
    ax.axvline(my, color=MUTED, lw=0.8, ls="--")
    b = ev[(ev.sector_milestone == mid) & ev.type.str.startswith("binding")]
    for y in sorted(b.year.unique()):
        if ratio.index.min() <= y <= ratio.index.max():
            ax.plot([y], [ratio.loc[ratio.index[np.abs(ratio.index - y).argmin()]]], marker="v", ms=8, color=ORANGE,
                    markeredgecolor="white", markeredgewidth=1.2, ls="none", zorder=4)
    ax.yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10, subs=(1, 2, 3, 5)))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True, nbins=5))
axs[0, 0].plot([], [], marker="v", ms=8, color=ORANGE, ls="none", label="binding response")
axs[0, 0].plot([], [], color=MUTED, lw=0.8, ls="--", label="milestone year")
axs[0, 0].legend(frameon=False, fontsize=8, loc="lower right")
fig.supylabel("Challenger's exports relative to the incumbent's (log scale)", fontsize=8.5, color=INK)
fig.tight_layout()
save(fig, "fig2_exports")

# ---- Fig. 3: breadth of displacement
b = pd.read_csv(D / "cases_breadth.csv")
pick = lambda d: d[((d.data == "s1") & (d.year <= 1991)) | ((d.data == "s3") & (d.year.between(1992, 2007))) | ((d.data == "hs4") & (d.year >= 2008))]
b = pick(b)
fig, ax = plt.subplots(figsize=(6.5, 3.0))
for c, lab, col, ls in [("JP", "Japan", BLUE, "-"), ("KR", "Korea", AQUA, "--"), ("TW", "Taiwan", YELLOW, "-."), ("CN", "China", ORANGE, "-")]:
    s = b[b.challenger == c].sort_values("year")
    v = 100 * s.us_exports_share_overtaken
    ax.plot(s.year, v, color=col, ls=ls)
    ax.text(s.year.iloc[-1] + 0.6, v.iloc[-1], lab, color=INK, fontsize=8, va="center")
ax.axvline(2018, color=MUTED, lw=0.8, ls=":")
ax.text(2017.5, 56, "Section 301 tariffs, 2018", color=MUTED, fontsize=7.5, ha="right", va="top")
ax.set_xlim(1962, 2028)
ax.set_ylabel("% of US manufactured exports")
tidy(ax)
save(fig, "fig3_breadth")

# ---- Fig. 4: start rates by years from the crossover
p = pd.read_csv(D / "population_panel.csv")
p = p[p.rel.notna()]
p["bin"] = (np.floor(p.rel / 2) * 2).astype(int)
p = p[p.bin.between(-10, 10)]
jk = p[p.challenger.isin(["JP", "KR"])]
r1 = jk.groupby("bin").apply(lambda g: 100 * g.broad.sum() / g.at_risk.sum(), include_groups=False)
ad = p[(p.year >= 1988) & (p.year <= 2015)]
r2 = ad.groupby("bin").apply(lambda g: 100 * g.ad_cases.sum() / len(g), include_groups=False)
fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.8))
for ax, r, col, title in [(axs[0], r1, BLUE, "Broad instruments, Japan and Korea"),
                          (axs[1], r2, ORANGE, "Antidumping cases, Japan, Korea, China (1988-2015)")]:
    ax.bar(r.index + 1, r.values, width=1.7, color=col, edgecolor="white", linewidth=1)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_title(title, fontsize=8.5, loc="left", color=INK)
    ax.set_xlabel("Years from the export crossover (two-year bins)")
    tidy(ax)
axs[0].set_ylabel("Starts per 100 group-years")
fig.tight_layout()
save(fig, "fig4_rates")

# ---- Fig. 5: attention in parliament
h = pd.read_csv(D / "ds1_hansard_salience.csv")
c = pd.read_csv(D / "ds1_crecb_years.csv").sort_values("year")
c = c[c.source == "CRECB"]
fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.8))
axs[0].plot(h.year, h.germany_hits_per_100k_words, color=BLUE, lw=1.4)
for mid in ["M-DE-DYE", "M-DE-SUGAR", "M-DE-STEEL", "M-DE-ELEC"]:
    axs[0].axvline(int(ms.loc[mid, "year"]), color=MUTED, lw=0.8, ls="--")
axs[0].set_title("Germany in British economic debates", fontsize=8.5, loc="left", color=INK)
axs[0].set_ylabel("Mentions per 100,000 words")
axs[1].plot(c.year, c.japan_comp_per_1m, color=ORANGE, lw=1.4)
for mid in ["M-JP-STEEL", "M-JP-TV", "M-JP-AUTO", "M-JP-DRAM", "M-JP-SEMI"]:
    axs[1].axvline(int(ms.loc[mid, "year"]), color=MUTED, lw=0.8, ls="--")
axs[1].set_title("Japan near a competition term, Congress", fontsize=8.5, loc="left", color=INK)
axs[1].set_ylabel("Mentions per million words")
axs[1].set_xlim(1955, 1994)
for ax in axs:
    tidy(ax)
fig.tight_layout()
save(fig, "fig5_attention")

# ---- Fig. 6: TFP relative to the US
t = pd.read_csv(D / "ds3_tfp.csv")
fig, ax = plt.subplots(figsize=(6.5, 3.0))
for cc, lab, col, ls in [("DEU", "Germany", BLUE, "-"), ("JPN", "Japan", ORANGE, "--"), ("KOR", "Korea", AQUA, "-."), ("CHN", "China", YELLOW, ":")]:
    s = t[t.country == cc]
    ax.plot(s.year, s.ctfp, color=col, ls=ls)
    off = {"KOR": 0.025, "JPN": -0.025}.get(cc, 0)
    ax.text(2024, s.ctfp.iloc[-1] + off, f" {lab}", color=INK, va="center", fontsize=8)
ax.axhline(1, color=INK, lw=0.8)
ax.set_xlim(1954, 2031)
ax.set_ylabel("TFP level, United States = 1")
tidy(ax)
save(fig, "fig6_tfp")
print("ok")
