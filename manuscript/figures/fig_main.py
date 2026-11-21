"""Abbildungen 1 und 2 des Manuskripts aus DS1 und DS3."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

R = Path(__file__).resolve().parents[2]
INK, MUTED, GRID = "#1f2328", "#59636e", "#d8dee4"
plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.edgecolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": INK})

# Abbildung 1: Lag je Reaktion, nach Fall; Fuellung nach MSS
e = pd.read_csv(R / "data" / "ds1_events.csv")
cases = [("DE", "Germany vs Britain"), ("JP", "Japan vs United States"), ("KR", "Korea vs United States, Japan"), ("CN", "China vs United States, EU")]
shade = {1: "#c9d6e3", 2: "#9fb6cc", 3: "#6f93b4", 4: "#3f6f99", 5: "#1b3f63"}
fig, ax = plt.subplots(figsize=(6.3, 3.1))
for i, (c, lab) in enumerate(cases):
    x = e[e.case == c]
    y = [i + (k % 5 - 2) * 0.08 for k in range(len(x))]
    ax.scatter(x.lag_years, y, s=28, c=[shade[int(v)] for v in x.mss_coder1], edgecolors="white", linewidths=0.8, zorder=3)
ax.axvline(0, color=INK, lw=0.9)
ax.axvspan(-30, 0, color="#eef1f4", lw=0, zorder=0)
ax.set_yticks(range(len(cases)), [l for _, l in cases])
ax.set_xlim(-28, 65)
ax.invert_yaxis()
ax.set_xlabel("Years from the sector's displacement milestone (response year minus milestone year)")
ax.text(-27, -0.45, "absorption phase", color=MUTED, fontsize=8, va="top")
ax.grid(axis="x", color=GRID, lw=0.6)
ax.spines[["top", "right"]].set_visible(False)
for k in range(1, 6):
    ax.scatter([], [], s=28, c=shade[k], edgecolors="white", label=f"MSS {k}")
ax.legend(frameon=False, ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.16), fontsize=8, handletextpad=0.2, columnspacing=0.9)
fig.savefig(R / "manuscript" / "figures" / "fig1_lags.pdf", bbox_inches="tight")
fig.savefig(R / "manuscript" / "figures" / "fig1_lags.png", dpi=200, bbox_inches="tight")

# Abbildung 2: TFP relativ zu den USA (PWT 11.0, ctfp)
t = pd.read_csv(R / "data" / "ds3_tfp.csv")
lines = [("DEU", "Germany", "#1b3f63", "-"), ("JPN", "Japan", "#3f6f99", "--"), ("KOR", "Korea", "#6f93b4", "-."), ("CHN", "China", "#8a5a2b", ":")]
fig, ax = plt.subplots(figsize=(6.3, 3.0))
ax.axhspan(0.70, 0.80, color="#eef1f4", lw=0)
for c, lab, col, ls in lines:
    s = t[t.country == c]
    ax.plot(s.year, s.ctfp, color=col, ls=ls, lw=1.6)
    off = {"KOR": 0.025, "JPN": -0.02}.get(c, 0)
    ax.text(2024, s.ctfp.iloc[-1] + off, f" {lab}", color=INK, va="center", fontsize=8)
ax.axhline(1, color=MUTED, lw=0.8)
ax.text(1955, 1.01, "United States = 1", color=MUTED, fontsize=8, va="bottom")
ax.set_xlim(1954, 2031)
ax.set_ylabel("TFP level relative to the US")
ax.grid(axis="y", color=GRID, lw=0.6)
ax.spines[["top", "right"]].set_visible(False)
fig.text(0.01, -0.03, "Source: Penn World Table 11.0, variable ctfp (current PPPs). Shaded band: 0.70 to 0.80.", fontsize=7, color=MUTED)
fig.savefig(R / "manuscript" / "figures" / "fig2_tfp.pdf", bbox_inches="tight")
fig.savefig(R / "manuscript" / "figures" / "fig2_tfp.png", dpi=200, bbox_inches="tight")
