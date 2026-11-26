"""Figures 1 to 6 of the manuscript and Figure L.1 of the appendix, from data/ (no smoothing, no interpolation).

Fig. 1  Export ratio challenger/incumbent in four sectors, with binding responses marked   (fig2_exports)
Fig. 2  Timing of the 41 core responses relative to the sector milestone                   (fig1_lags)
Fig. 3  Start rates of measures by years from a group's export crossover                   (fig4_rates)
Fig. 4  Breadth of displacement: share of US manufactured exports in overtaken groups      (fig3_breadth)
Fig. 5  Attention to the challenger in the incumbent's legislature                        (fig5_attention)
Fig. 6  TFP relative to the United States                                                  (fig6_tfp)
Fig. L.1 Same as Fig. 6, with the band 0.70-0.80                                           (fig2_tfp)
Call from the repository root: python3 manuscript/figures/fig_story.py
"""
import matplotlib.ticker as mt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from style import AQUA, BLUE, D, GRAY, GRID, INK, MUTED, ORANGE, RAMP, SOFT, YELLOW, note, save, tidy, title

ev = pd.read_csv(D / "ds1_events.csv")
ms = pd.read_csv(D / "ds1_milestones.csv").set_index("milestone_id")

# ---- Fig. 1: export ratios in four sectors
ex = pd.read_csv(D / "ds1_export_series.csv")
ex["o"] = ex.classification.map({"S1": 0, "S2": 1, "S3": 2, "HS": 3})
panels = [("JP-STEEL", "M-JP-STEEL", "Japan, steel", "US"), ("JP-TV", "M-JP-TV", "Japan, television sets", "US"),
          ("JP-AUTO", "M-JP-AUTO", "Japan, passenger cars", "US"), ("CN-SOLAR", "M-CN-SOLAR", "China, solar cells", "Germany")]
fig, axs = plt.subplots(2, 2, figsize=(6.6, 4.8))
for ax, (sec, mid, ttl, inc) in zip(axs.flat, panels):
    s = ex[ex.sector == sec].sort_values("o").drop_duplicates(["role", "year"], keep="first")
    w = s.pivot(index="year", columns="role", values="value_usd").dropna()
    ratio = w.challenger / w.incumbent
    ax.set_yscale("log")
    lo, hi = min(ratio.min(), 1) / 1.35, max(ratio.max(), 1) * 1.35
    ax.set_ylim(lo, hi)
    ax.axhspan(1, hi, color=SOFT, lw=0, zorder=0)
    ax.axhline(1, color=INK, lw=0.8, zorder=1)
    ax.plot(ratio.index, ratio.values, color=BLUE, zorder=3)
    my = int(ms.loc[mid, "year"])
    ax.axvline(my, color=MUTED, lw=0.8, ls=(0, (2, 2)), zorder=2)
    note(ax, my, lo * 1.12, f" milestone {my}", va="bottom", ha="left")
    b = ev[(ev.sector_milestone == mid) & ev.type.str.startswith("binding")]
    for y in sorted(b.year.unique()):
        if ratio.index.min() <= y <= ratio.index.max():
            yy = ratio.loc[ratio.index[np.abs(ratio.index - y).argmin()]]
            ax.plot([y], [yy], marker="v", ms=7.5, color=ORANGE, mec="white", mew=1.2, ls="none", zorder=4)
    title(ax, f"{ttl} ({inc} = 1)")
    tidy(ax)
    ax.yaxis.set_major_locator(mt.LogLocator(base=10, subs=(1, 2, 5)))
    ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.yaxis.set_minor_locator(mt.NullLocator())
    ax.xaxis.set_major_locator(mt.MaxNLocator(integer=True, nbins=5))
    ax.set_xlim(ratio.index.min() - 0.5, ratio.index.max() + 0.5)
note(axs[0, 0], axs[0, 0].get_xlim()[1] - 0.3, 1.06, "challenger ahead", va="bottom", ha="right", fontsize=7)
h = [plt.Line2D([], [], color=BLUE, lw=2), plt.Line2D([], [], marker="v", ms=7.5, color=ORANGE, mec="white", ls="none"),
     plt.Line2D([], [], color=MUTED, lw=0.8, ls=(0, (2, 2)))]
fig.legend(h, ["challenger's exports relative to the incumbent's (log scale)", "binding response", "displacement milestone"],
           loc="upper left", bbox_to_anchor=(0.0, 1.05), ncol=3, handlelength=1.6, columnspacing=1.4)
fig.tight_layout(h_pad=1.6, w_pad=2.0)
save(fig, "fig2_exports")

# ---- Fig. 2: timing of the core responses
cases = [("DE", "Germany vs Britain"), ("JP", "Japan vs United States"), ("KR", "Korea vs United States, Japan"),
         ("CN", "China vs United States, EU")]
fig, ax = plt.subplots(figsize=(6.6, 3.0))
ax.axvspan(-30, 0, color=SOFT, lw=0, zorder=0)
ax.axvline(0, color=INK, lw=0.8, zorder=1)
for i, (c, lab) in enumerate(cases):
    x = ev[ev.case == c].sort_values(["lag_years", "reach_coder1"])
    seen = {}
    for lag, ir in zip(x.lag_years, x.reach_coder1):
        k = seen.get(lag, 0); seen[lag] = k + 1
        off = ((k + 1) // 2) * 0.19 * (1 if k % 2 else -1)
        ax.scatter(lag, i + off, s=42, color=RAMP[int(ir) - 1], edgecolor="white", linewidth=0.9, zorder=3)
    nb, na = int((x.lag_years < 0).sum()), int((x.lag_years >= 0).sum())
    ax.text(66, i, f"{nb} before, {na} after", va="center", ha="left", fontsize=7.5, color=MUTED)
ax.set_yticks(range(len(cases)), [l for _, l in cases])
ax.tick_params(axis="y", colors=INK)
ax.set_ylim(len(cases) - 0.45, -0.75)
ax.set_xlim(-28, 65)
note(ax, -1, -0.62, "absorption phase", va="center", ha="right")
note(ax, 1, -0.62, "after the milestone", va="center")
ax.set_xlabel("Years from the displacement milestone of the response's sector")
tidy(ax, grid="x")
ax.spines["bottom"].set_visible(False)
for k in range(5):
    ax.scatter([], [], s=42, color=RAMP[k], edgecolor="white", label=f"{k + 1}")
ax.legend(title="Instrument reach (IR)", title_fontsize=7.5, ncol=5, loc="lower left", bbox_to_anchor=(0.0, 1.0),
          handletextpad=0.1, columnspacing=0.8, alignment="left")
save(fig, "fig1_lags")

# ---- Fig. 3: start rates by relative position (broad measures) and by years from the crossover (antidumping)
p = pd.read_csv(D / "population_panel.csv", dtype={"code": str})
jk = p[p.challenger.isin(["JP", "KR"]) & (p.data == "s1") & (p.at_risk == 1) & (p.x_us > 0)].copy()
labels = ["<0.25", "0.25-0.5", "0.5-1", "1-2", "\u22652"]
jk["rb"] = pd.cut(jk.x_ch / jk.x_us, [-np.inf, 0.25, 0.5, 1, 2, np.inf], labels=labels)
r1 = jk.groupby("rb", observed=False).broad.agg(["mean", "sum", "size"])
q = p[p.rel.notna()].copy()
q["bin"] = (np.floor(q.rel / 2) * 2).astype(int)
q = q[q.bin.between(-10, 10)]
ad = q[(q.year >= 1988) & (q.year <= 2015)]
r2 = ad.groupby("bin").apply(lambda g: 100 * g.ad_cases.sum() / len(g), include_groups=False)
fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.9))
ax = axs[0]
x = np.arange(len(labels))
ax.bar(x, 100 * r1["mean"].values, width=0.72, color=BLUE, edgecolor="white", linewidth=1.2, zorder=2)
for k, (m, n) in enumerate(zip(r1["mean"].values, r1["sum"].values)):
    note(ax, k, 100 * m + 0.05, f"{int(n)}", ha="center", va="bottom")
ax.set_xticks(x, labels)
ax.set_xlabel("Challenger's exports relative to US exports")
ax.set_ylabel("Starts per 100 group-years")
ax.set_ylim(0, 100 * r1["mean"].max() * 1.2)
title(ax, "Broad measures, Japan and Korea")
tidy(ax)
ax = axs[1]
colors = [GRAY if b < 0 else ORANGE for b in r2.index]
ax.bar(r2.index + 1, r2.values, width=1.75, color=colors, edgecolor="white", linewidth=1.2, zorder=2)
ax.axvline(0, color=INK, lw=0.8, zorder=3)
top = ax.get_ylim()[1] * 1.15
ax.set_ylim(0, top)
note(ax, -0.4, top * 0.98, "before", ha="right", va="top")
note(ax, 0.4, top * 0.98, "after the crossover", ha="left", va="top")
ax.set_xticks(range(-10, 11, 4))
ax.set_xlabel("Years from the export crossover")
title(ax, "US antidumping cases, 1988-2015")
tidy(ax)
fig.tight_layout(w_pad=2.5)
save(fig, "fig4_rates")
print("Fig. 3 left:", r1.assign(rate=lambda z: (100 * z["mean"]).round(2)).to_dict("index"))

# ---- Fig. 4: breadth of displacement
b = pd.read_csv(D / "cases_breadth.csv")
b = b[((b.data == "s1") & (b.year <= 1991)) | ((b.data == "s3") & b.year.between(1992, 2007)) | ((b.data == "hs4") & (b.year >= 2008))]
fig, ax = plt.subplots(figsize=(6.6, 3.1))
ends = {}
for c, lab, col in [("JP", "Japan", BLUE), ("CN", "China", ORANGE), ("KR", "Korea", AQUA), ("TW", "Taiwan", YELLOW)]:
    s = b[b.challenger == c].sort_values("year")
    v = 100 * s.us_exports_share_overtaken
    ax.plot(s.year, v, color=col, lw=2 if c in ("JP", "CN") else 1.6, zorder=3)
    ends[c] = (s.year.iloc[-1], v.iloc[-1], lab, col)
for c, (x, y, lab, col) in ends.items():
    if c == "KR":
        ax.annotate(lab, (x, y), xytext=(1996, 15), color=col, fontsize=8.5, fontweight="semibold", va="center", ha="center",
                    arrowprops=dict(arrowstyle="-", color=col, lw=0.8, shrinkA=2, shrinkB=2))
        continue
    ax.text(x + 0.8, y + {"TW": 1.5}.get(c, 0), lab, color=col, fontsize=8.5, fontweight="semibold", va="center")
note(ax, ends["JP"][0] + 0.8, ends["JP"][1] - 4.5, "series ends 1991", va="center")
cn18 = 100 * b[(b.challenger == "CN") & (b.year == 2018)].us_exports_share_overtaken.iloc[0]
ax.axvline(2018, color=MUTED, lw=0.8, ls=(0, (2, 2)), zorder=1)
ax.plot([2018], [cn18], marker="o", ms=5.5, color=ORANGE, mec="white", mew=1.2, zorder=4)
note(ax, 2017.4, cn18 + 1.5, f"Section 301 tariffs, 2018:\n{cn18:.0f}% displaced", ha="right", va="bottom")
ax.set_xlim(1962, 2029)
ax.set_ylim(0, 60)
ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
title(ax, "Share of US manufactured exports in groups where the challenger's exports lead")
tidy(ax)
save(fig, "fig3_breadth")

# ---- Fig. 5: attention in parliament
h = pd.read_csv(D / "ds1_hansard_salience.csv")
c = pd.read_csv(D / "ds1_crecb_years.csv").sort_values("year")
c = c[c.source == "CRECB"]
fig, axs = plt.subplots(1, 2, figsize=(6.6, 3.0))


def milestones(ax, items, top, lines=None):
    for x in lines or [x for x, _ in items]:
        ax.axvline(x, color=MUTED, lw=0.7, ls=(0, (2, 2)), zorder=1)
    for k, (x, lab) in enumerate(items):
        note(ax, x, top * (1.0 if k % 2 == 0 else 0.92), lab, va="top", ha="center", fontsize=7,
             bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))


axs[0].fill_between(h.year, h.germany_hits_per_100k_words, color=BLUE, alpha=0.12, lw=0, zorder=2)
axs[0].plot(h.year, h.germany_hits_per_100k_words, color=BLUE, lw=1.4, zorder=3)
axs[0].set_xlim(1850, 1914)
axs[0].set_ylim(0, 150)
milestones(axs[0], [(int(ms.loc[m, "year"]), l) for m, l in
                    [("M-DE-DYE", "dyes"), ("M-DE-SUGAR", "sugar"), ("M-DE-STEEL", "steel"), ("M-DE-ELEC", "electrical")]], 149)
title(axs[0], "Germany in British economic debates")
axs[0].set_ylabel("Mentions per 100,000 words")
axs[1].fill_between(c.year, c.japan_comp_per_1m, color=ORANGE, alpha=0.12, lw=0, zorder=2)
axs[1].plot(c.year, c.japan_comp_per_1m, color=ORANGE, lw=1.4, zorder=3)
axs[1].set_xlim(1955, 1994)
axs[1].set_ylim(0, 80)
milestones(axs[1], [(1969.5, "steel, TV"), (1980.5, "cars, DRAM"), (1986, "semiconductors")], 79,
           lines=[int(ms.loc[m, "year"]) for m in ["M-JP-STEEL", "M-JP-TV", "M-JP-AUTO", "M-JP-DRAM", "M-JP-SEMI"]])
title(axs[1], "Japan near a competition term, US Congress")
axs[1].set_ylabel("Mentions per million words")
for ax in axs:
    tidy(ax)
fig.tight_layout(w_pad=2.5)
save(fig, "fig5_attention")

# ---- Fig. 6 and Fig. L.1: TFP relative to the US
t = pd.read_csv(D / "ds3_tfp.csv")
for name, band in [("fig6_tfp", False), ("fig2_tfp", True)]:
    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    if band:
        ax.axhspan(0.70, 0.80, color=SOFT, lw=0, zorder=0)
        note(ax, 1956, 0.79, "0.70-0.80", va="top")
    ax.axhline(1, color=INK, lw=0.8, zorder=1)
    note(ax, 1955, 1.015, "United States = 1", va="bottom")
    for cc, lab, col, dy in [("DEU", "Germany", BLUE, 0.04), ("JPN", "Japan", ORANGE, -0.03), ("KOR", "Korea", AQUA, 0.03),
                             ("CHN", "China", YELLOW, 0)]:
        s = t[t.country == cc]
        ax.plot(s.year, s.ctfp, color=col, zorder=3)
        ax.text(s.year.iloc[-1] + 0.8, s.ctfp.iloc[-1] + dy, lab, color=col, fontsize=8.5, fontweight="semibold", va="center")
    lab_of = {"JPN": "Japan", "KOR": "Korea"}
    for cc, col in [("JPN", ORANGE), ("KOR", AQUA)]:
        s = t[t.country == cc].set_index("year").ctfp
        yr, v = s.idxmax(), s.max()
        ax.plot([yr], [v], marker="o", ms=5.5, color=col, mec="white", mew=1.2, zorder=4)
        xy = {"JPN": (1976, 0.93), "KOR": (2005, 0.52)}[cc]
        ax.annotate(f"{lab_of[cc]} peak {v:.2f}, {yr}", (yr, v), xytext=xy, fontsize=7.5, color=MUTED, ha="center", va="center",
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7, shrinkA=3, shrinkB=4))
    ax.set_xlim(1954, 2031)
    ax.set_ylim(0.15, 1.12)
    title(ax, "TFP level relative to the United States")
    tidy(ax)
    save(fig, name)
print("ok")
