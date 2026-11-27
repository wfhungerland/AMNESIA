"""Referee round 2, points 3 and 4: functional form of the gradient and import pressure (Japan and Korea).

Panel as in robust_broad.py (groups at risk until the first start: a discrete-time hazard). Standard errors clustered
by SITC two-digit division (see robust_measure.py).
(a) bins of the export ratio x_ch / x_us instead of the log ratio;
(b) the log ratio with other offsets (0.01, 1 and 10 million USD) and without the cap;
(c) import pressure: US imports from the challenger against the export ratio.
Output: data/robust_form.txt
"""
from pathlib import Path
import warnings

import numpy as np
import pandas as pd

# Main panel without textile groups (SITC 65, 84): textiles were restrained before displacement under a standing
# regime (Section 7.2). The full register is reported in data/register_sweep_textiles_check.py and Appendix C.
TEXTILE = ["65", "84"]
import statsmodels.api as sm
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")
D = Path(__file__).resolve().parent
P = pd.read_csv(D / "population_panel.csv", dtype={"code": str})
P = P[P.challenger.isin(["JP", "KR"]) & (P.data == "s1") & (P.at_risk == 1) & ~P.code.str[:2].isin(TEXTILE)].copy()
P["fe"] = (P.year.astype(str) + P.challenger).astype(object)
P = P[P.groupby("fe").broad.transform("sum") > 0].copy()
P["div"] = ("s1_" + P.code.str[:2]).astype(object)
P["lx_ch"], P["lm_us"] = np.log1p(P.x_ch / 1e6), np.log1p(P.m_us / 1e6)
ratio = P.x_ch / P.x_us.replace(0, np.nan)
P["rbin"] = pd.cut(ratio, [-np.inf, 0.25, 0.5, 1, 2, np.inf], labels=["<0.25", "0.25-0.5", "0.5-1", "1-2", ">=2"]).astype(object)
P = P.dropna(subset=["rbin"])
out = [f"Japan and Korea: {len(P)} group-years at risk, {int(P.broad.sum())} starts"]


def fit(f, df=P):
    return smf.glm(f"broad ~ {f}", data=df, family=sm.families.Poisson()).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(df["div"])[0]}, maxiter=200)


m = fit("C(rbin, Treatment('<0.25')) + lx_ch + lm_us + C(fe)")
out.append("(a) Export ratio in bins (reference below 0.25), at given exports and imports:")
for b in ["0.25-0.5", "0.5-1", "1-2", ">=2"]:
    k = f"C(rbin, Treatment('<0.25'))[T.{b}]"
    g = P[P.rbin == b]
    out.append(f"    {b:9s}: {len(g)} group-years, {int(g.broad.sum())} starts; rate ratio {np.exp(m.params[k]):.2f} "
               f"({np.exp(m.params[k] - 1.96 * m.bse[k]):.2f}-{np.exp(m.params[k] + 1.96 * m.bse[k]):.2f})")
g = P[P.rbin == "<0.25"]
out.append(f"    <0.25    : {len(g)} group-years, {int(g.broad.sum())} starts (reference)")
out.append("(b) Log export ratio per doubling, other offsets and caps:")
for off in (1e4, 1e5, 1e6, 1e7):
    for cap in (5, None):
        lr = np.log((P.x_ch + off) / (P.x_us + off))
        P["lr"] = lr.clip(-cap, cap) if cap else lr
        m = fit("lr + lx_ch + lm_us + C(fe)")
        b, se = m.params["lr"], m.bse["lr"]
        out.append(f"    offset {off / 1e6:g}m, cap {cap or 'none'}: x{2 ** b:.2f} ({2 ** (b - 1.96 * se):.2f}-{2 ** (b + 1.96 * se):.2f}), p={m.pvalues['lr']:.3f}")
P["lr"] = np.clip(np.log((P.x_ch + 1e5) / (P.x_us + 1e5)), -5, 5)
out.append("(c) Import pressure against relative position:")
for f in ["lm_us + lx_ch + C(fe)", "lr + lx_ch + C(fe)", "lr + lm_us + lx_ch + C(fe)"]:
    m = fit(f)
    out.append("    " + f.replace(" + C(fe)", "") + ": " + "; ".join(
        f"{t} {m.params[t]:+.2f} (p={m.pvalues[t]:.3f})" for t in ("lr", "lm_us", "lx_ch") if t in m.params))
(D / "robust_form.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
