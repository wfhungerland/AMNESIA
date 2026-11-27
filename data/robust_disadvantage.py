"""Referee round 3, point 1: displacement or American comparative disadvantage?

At given challenger exports, the log export ratio varies only through US exports. This script separates the two:
(a) challenger exports and US exports as separate regressors, with five-year changes;
(b) a measure of US comparative disadvantage that does not depend on the challenger: the US trade balance of the
    group against the rest of the world, (X_us - M_row) / (X_us + M_row), where M_row is US imports from the world
    minus US imports from the challenger (data/raw/comtrade_us_imports_world_s1.csv, population_fetch_usworld.py);
(c) within-group estimates: group fixed effects (only groups with a start identify them) and challenger trends.
Japan and Korea, SITC Rev. 1, groups at risk until the first start; Poisson; errors clustered by SITC division.
Output: data/robust_disadvantage.txt
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
P = P[P.challenger.isin(["JP", "KR"]) & (P.data == "s1") & ~P.code.str[:2].isin(TEXTILE)].sort_values(["challenger", "code", "year"]).copy()
W = pd.read_csv(D / "raw" / "comtrade_us_imports_world_s1.csv", dtype={"code": str}).rename(columns={"value": "m_world"})
P = P.merge(W[["code", "year", "m_world"]], on=["code", "year"], how="left")
P["m_row"] = (P.m_world - P.m_us).clip(lower=0)
P["bal"] = (P.x_us - P.m_row) / (P.x_us + P.m_row)
P["lx_ch"], P["lx_us"], P["lm_us"] = np.log1p(P.x_ch / 1e6), np.log1p(P.x_us / 1e6), np.log1p(P.m_us / 1e6)
P["lr"] = np.clip(np.log((P.x_ch + 1e5) / (P.x_us + 1e5)), -5, 5)
g = P.groupby(["challenger", "code"])
for c in ("lx_ch", "lx_us", "bal"):
    P[f"d5_{c}"] = g[c].diff(5)
P = P[P.at_risk == 1].copy()
P["fe"] = (P.year.astype(str) + P.challenger).astype(object)
P["div"] = ("s1_" + P.code.str[:2]).astype(object)
P["grp"] = (P.challenger + "_" + P.code).astype(object)
P["t"] = P.year - 1962
out = [f"US imports from the world matched for {P.m_world.notna().mean():.3f} of group-years at risk; "
       f"US balance against the rest of the world: median {P.bal.median():.2f}"]


def fit(f, df, label, terms):
    df = df.dropna(subset=[t for t in terms if t in df])
    if "C(fe)" in f:
        df = df[df.groupby("fe").broad.transform("sum") > 0]
    m = smf.glm(f"broad ~ {f}", data=df, family=sm.families.Poisson()).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(df["div"])[0]}, maxiter=300)
    out.append(f"{label} (N={int(m.nobs)}, starts={int(df.broad.sum())}): " + "; ".join(
        f"{t} {m.params[t]:+.2f} (p={m.pvalues[t]:.3f})" for t in terms if t in m.params))


T = ["lr", "lx_ch", "lx_us", "lm_us", "bal", "d5_lx_ch", "d5_lx_us", "d5_bal"]
fit("lx_ch + lx_us + lm_us + C(fe)", P, "(1) levels", T)
fit("lx_ch + lx_us + lm_us + d5_lx_ch + d5_lx_us + C(fe)", P, "(2) levels and five-year changes", T)
fit("bal + lx_ch + lm_us + C(fe)", P, "(3) US balance against the rest of the world, at given challenger exports and imports", T)
fit("lr + bal + lx_ch + lm_us + C(fe)", P, "(4) export ratio and US balance", T)
fit("lx_ch + lx_us + bal + lm_us + C(fe)", P, "(5) levels and US balance", T)
fit("lr + bal + d5_bal + lx_ch + lm_us + C(fe)", P, "(6) as (4) + five-year change of the US balance", T)
E = P[P.grp.isin(P[P.broad == 1].grp)]
fit("lr + lx_ch + C(grp) + C(challenger):t", E, "(7) within groups: export ratio, group effects, challenger trends", T)
fit("lx_ch + lx_us + C(grp) + C(challenger):t", E, "(8) within groups: levels", T)
fit("lr + bal + lx_ch + C(grp) + C(challenger):t", E, "(9) within groups: export ratio and US balance", T)
(D / "robust_disadvantage.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
