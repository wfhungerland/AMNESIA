"""Referee point 1: does the rate ratio of broad measures after the export crossover survive controls for scale?

Panel: data/population_panel.csv (built by population_panel.py). Japan and Korea, SITC Rev. 1, 1962-1999,
groups at risk until their first targeted broad measure. Poisson, standard errors clustered by group.
Output: data/robust_broad.txt, data/robust_broad_es.csv
"""
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")
D = Path(__file__).resolve().parent
P = pd.read_csv(D / "population_panel.csv", dtype={"code": str})
jk = P[P.challenger.isin(["JP", "KR"]) & (P.data == "s1") & (P.at_risk == 1)].copy()
jk["yc"] = jk.year.astype(str) + jk.challenger
jk["grp"] = jk.challenger + "_" + jk.code
jk["lx_ch"] = np.log1p(jk.x_ch / 1e6)
jk["lm_us"] = np.log1p(jk.m_us / 1e6)
jk["lx_us"] = np.log1p(jk.x_us / 1e6)
jk["sitc2"] = jk.code.str[:2]
jk["sitc1"] = jk.code.str[:1]
out = [f"Japan and Korea, SITC Rev. 1: {jk.grp.nunique()} groups, {len(jk)} group-years at risk, "
       f"{int(jk.broad.sum())} starts ({int(jk[jk.post == 0].broad.sum())} before, {int(jk[jk.post == 1].broad.sum())} after the crossover)", ""]


def fit(df, rhs, label, term="post"):
    m = smf.glm(f"broad ~ {rhs}", data=df, family=sm.families.Poisson()).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(df.grp)[0]}, maxiter=200)
    b, se = m.params[term], m.bse[term]
    out.append(f"{label}: IRR {np.exp(b):.2f} (95% CI {np.exp(b - 1.96 * se):.2f}-{np.exp(b + 1.96 * se):.2f}), p={m.pvalues[term]:.3f}; "
               f"N={int(m.nobs)}, events={int(df.broad.sum())}")
    return m


fit(jk, "post + C(yc)", "(1) baseline, year x challenger effects")
m2 = fit(jk, "post + lx_ch + C(yc)", "(2) + log challenger exports")
out.append(f"    coefficient on log challenger exports: {m2.params['lx_ch']:.2f} (p={m2.pvalues['lx_ch']:.3f})")
fit(jk, "post + lx_ch + lm_us + C(yc)", "(3) + log US imports from the challenger")
fit(jk, "post + lx_ch + lm_us + lx_us + C(yc)", "(4) + log US exports of the group")
fit(jk, "post + lx_ch + lm_us + lx_us + C(sitc1) + C(yc)", "(5) as (4) + SITC one-digit sector effects")
w = jk[jk.rel.between(-10, 10)]
fit(w, "post + C(year)", "(6) displaced groups, +-10 years around the crossover, year effects")
fit(w, "post + lx_ch + lm_us + C(year)", "(7) as (6) + log challenger exports and US imports")
ev = jk[jk.grp.isin(jk[jk.broad == 1].grp)]
fit(ev, "post + C(grp) + C(year)", "(8) group fixed effects (groups with a start only), year effects")
fit(ev, "post + lx_ch + C(grp)", "(9) group fixed effects + log challenger exports, linear trend", ) if False else None
ev2 = ev.assign(t=ev.year - 1962)
fit(ev2, "post + lx_ch + t + C(grp)", "(9) group fixed effects + log challenger exports + linear time trend")
# continuous relative position: log ratio of challenger to incumbent exports (0.1 million USD added, capped at +-5)
jk["lr"] = np.clip(np.log((jk.x_ch + 1e5) / (jk.x_us + 1e5)), -5, 5)
m = fit(jk, "post + lr + lx_ch + lm_us + C(yc)", "(10) as (3) + log export ratio")
out.append(f"    log export ratio: coefficient {m.params['lr']:.2f} (p={m.pvalues['lr']:.3f})")
m = fit(jk, "lr + lx_ch + lm_us + C(yc)", "(11) log export ratio instead of the crossover indicator (IRR per log point)", term="lr")
b, se = m.params["lr"], m.bse["lr"]
out.append(f"    per doubling of the export ratio: x{2 ** b:.2f} (95% CI {2 ** (b - 1.96 * se):.2f}-{2 ** (b + 1.96 * se):.2f})")

# further cases (TH, VN, MY, MX, BR, HK, TW): sectoral broad measures without GSP graduation (B-29), as in cases_test.py
reg = pd.read_csv(D / "broad_register.csv", dtype=str)
GLOBAL = {"B-02", "B-17", "B-19", "B-34", "B-31", "B-29"}
COL = {"s1": "codes_s1", "s3": "codes_s3", "hs4": "codes_hs4"}


def covers(r, data, code):
    cs = r[COL[data]] if isinstance(r[COL[data]], str) else ""
    return cs == "ALL" or any(code.startswith(k) for k in cs.split(";") if k)


Q = pd.read_csv(D / "cases_panel.csv", dtype={"code": str})
H = {}
for t, d, c in Q[["challenger", "data", "code"]].drop_duplicates().itertuples(index=False):
    H[(t, d, c)] = sorted(int(r.year) for _, r in reg.iterrows()
                          if t in r.target.split(";") and r.instrument_id not in GLOBAL and covers(r, d, c))
Q["broad"] = [int(y in H[(t, d, c)]) for t, d, c, y in zip(Q.challenger, Q.data, Q.code, Q.year)]
Q = Q[[not any(h < y for h in H[(t, d, c)]) for t, d, c, y in zip(Q.challenger, Q.data, Q.code, Q.year)]].copy()
Q["yc"] = Q.year.astype(str) + Q.src
Q["grp"] = Q.src + "_" + Q.code
# cells of year x source without any start are perfectly predicted by their fixed effect and drop out of a
# Poisson fixed-effects likelihood; removing them leaves the estimates unchanged and saves memory
Q = Q[Q.groupby("yc").broad.transform("sum") > 0].copy()
Q["lr"] = np.clip(np.log((Q.x_ch + 1e5) / (Q.x_us + 1e5)), -5, 5)
out += ["", f"Further cases, sectoral broad measures (year x source cells with a start): {Q.grp.nunique()} group series, {int(Q.broad.sum())} starts "
        f"({int(Q[Q.post == 0].broad.sum())} before, {int(Q[Q.post == 1].broad.sum())} after the crossover)"]
fit(Q, "post + C(yc)", "(12) further cases, baseline, year x source effects")
fit(Q, "post + lx_ch + C(yc)", "(13) further cases + log challenger exports")
m = fit(Q, "post + lr + lx_ch + C(yc)", "(14) further cases + log export ratio")
out.append(f"    log export ratio: coefficient {m.params['lr']:.2f} (p={m.pvalues['lr']:.3f})")
m = fit(Q, "lr + lx_ch + C(yc)", "(15) further cases, log export ratio instead of the crossover indicator (IRR per log point)", term="lr")
b, se = m.params["lr"], m.bse["lr"]
out.append(f"    per doubling of the export ratio: x{2 ** b:.2f} (95% CI {2 ** (b - 1.96 * se):.2f}-{2 ** (b + 1.96 * se):.2f})")

# event study: bins relative to the crossover, never-displaced groups as reference
bins = [(-99, -11, "<=-11"), (-10, -6, "-10..-6"), (-5, -1, "-5..-1"), (0, 4, "0..4"), (5, 9, "5..9"), (10, 99, ">=10")]
jk["bin"] = "never"
for lo, hi, lab in bins:
    jk.loc[jk.rel.between(lo, hi), "bin"] = lab
jk["bin"] = pd.Categorical(jk.bin, ["never"] + [b[2] for b in bins])
m = smf.glm("broad ~ C(bin) + lx_ch + lm_us + C(yc)", data=jk, family=sm.families.Poisson()).fit(
    cov_type="cluster", cov_kwds={"groups": pd.factorize(jk.grp)[0]}, maxiter=200)
rows = []
for lab in [b[2] for b in bins]:
    k = f"C(bin)[T.{lab}]"
    g = jk[jk.bin == lab]
    rows.append({"bin": lab, "group_years": len(g), "starts": int(g.broad.sum()), "rate_per_100": round(100 * g.broad.mean(), 2),
                 "irr": round(np.exp(m.params[k]), 2), "lo": round(np.exp(m.params[k] - 1.96 * m.bse[k]), 2),
                 "hi": round(np.exp(m.params[k] + 1.96 * m.bse[k]), 2)})
g = jk[jk.bin == "never"]
rows.insert(0, {"bin": "never", "group_years": len(g), "starts": int(g.broad.sum()), "rate_per_100": round(100 * g.broad.mean(), 2),
                "irr": 1.0, "lo": np.nan, "hi": np.nan})
es = pd.DataFrame(rows)
es.to_csv(D / "robust_broad_es.csv", index=False)
out += ["", "Event study (reference: groups never displaced; controls: log challenger exports, log US imports, year x challenger):",
        es.to_string(index=False)]
(D / "robust_broad.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
