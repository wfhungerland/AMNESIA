"""Referee round 2, point 1: inference at the level of measures and sectors.

The 26 starts of broad measures against Japan and Korea in the panel come from nine register entries; three of them
(B-03, B-13, B-04) supply 20. Checks:
(a) standard errors clustered by SITC two-digit division instead of group, and a cluster bootstrap over divisions;
(b) leave-one-measure-out: drop all groups covered by a measure (its whole product scope);
(c) measure-level placebo: for each measure, the mean log export ratio of the covered groups in the year it began,
    against the same mean with the start year shifted by -10..+10 years (0 excluded), 10,000 draws.
Same checks for the seven further economies. Inputs: data/population_panel.csv, data/cases_panel.csv,
data/broad_register.csv. Output: data/robust_measure.txt
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

from register_recode import covers

warnings.filterwarnings("ignore")
D = Path(__file__).resolve().parent
reg = pd.read_csv(D / "broad_register.csv", dtype=str)
reg = reg[reg.reach.astype(int) >= 4]
rng = np.random.default_rng(20261126)
out = []


def prep(P, fe):
    P = P.copy()
    P["fe"] = (P.year.astype(str) + P[fe]).astype(object)
    P["grp"] = (P.src + "_" + P.code).astype(object)
    P["div"] = (P.data + "_" + P.code.str[:2]).astype(object)
    P["lr"] = np.clip(np.log((P.x_ch + 1e5) / (P.x_us + 1e5)), -5, 5)
    P["lx_ch"] = np.log1p(P.x_ch / 1e6)
    if "m_us" in P:
        P["lm_us"] = np.log1p(P.m_us / 1e6)
    return P[P.groupby("fe").broad.transform("sum") > 0].copy()


def fit(df, rhs, term, cl):
    m = smf.glm(f"broad ~ {rhs}", data=df, family=sm.families.Poisson()).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(df[cl])[0]}, maxiter=200)
    return m.params[term], m.bse[term], m.pvalues[term]


def fmt(b, se, p, per_doubling):
    f = (lambda x: 2 ** x) if per_doubling else np.exp
    return f"{f(b):.2f} ({f(b - 1.96 * se):.2f}-{f(b + 1.96 * se):.2f}), p={p:.3f}"


def boot(df, rhs, term, reps=499):
    divs = df["div"].unique()
    g = {d: x for d, x in df.groupby("div")}
    est = []
    for _ in range(reps):
        pick = rng.choice(divs, len(divs), replace=True)
        b = pd.concat([g[d].assign(div=f"{d}_{k}") for k, d in enumerate(pick)])
        if b.broad.sum() < 3:
            continue
        try:
            m = smf.glm(f"broad ~ {rhs}", data=b, family=sm.families.Poisson()).fit(maxiter=100)
            est.append(m.params[term])
        except Exception:
            pass
    est = np.array(est)
    return np.percentile(est, [2.5, 97.5]), np.mean(est <= 0), len(est)


def scope(P, mid):
    r = reg[reg.instrument_id == mid].iloc[0]
    return {(t, d, c) for t, d, c in P[["challenger", "data", "code"]].drop_duplicates().itertuples(index=False)
            if t in r.target.split(";") and covers(r, d, c)}


def block(P, label, specs, drop_ids):
    out.append(f"== {label}: {P.grp.nunique()} groups, {P['div'].nunique()} SITC/HS divisions, {int(P.broad.sum())} starts")
    for rhs, term, dbl, name in specs:
        b, se, p = fit(P, rhs, term, "grp")
        out.append(f"  {name}")
        out.append(f"    clustered by group:    {fmt(b, se, p, dbl)}")
        b, se, p = fit(P, rhs, term, "div")
        out.append(f"    clustered by division: {fmt(b, se, p, dbl)}")
        (lo, hi), share, n = boot(P, rhs, term)
        f = (lambda x: 2 ** x) if dbl else np.exp
        out.append(f"    cluster bootstrap over divisions ({n} draws): 95% {f(lo):.2f}-{f(hi):.2f}; share of draws <= 0: {share:.3f}")
    for ids in drop_ids:
        sc = set().union(*[scope(P, i) for i in ids])
        keep = [(t, d, c) not in sc for t, d, c in zip(P.challenger, P.data, P.code)]
        Q = P[keep]
        Q = Q[Q.groupby("fe").broad.transform("sum") > 0]
        for rhs, term, dbl, name in specs:
            try:
                b, se, p = fit(Q, rhs, term, "div")
                res = fmt(b, se, p, dbl)
            except Exception as e:
                res = f"not estimable ({type(e).__name__})"
            out.append(f"  without {'+'.join(ids)} ({Q.grp.nunique()} groups, {int(Q.broad.sum())} starts): {name}: {res}")


JK = pd.read_csv(D / "population_panel.csv", dtype={"code": str})
JK = prep(JK[JK.challenger.isin(["JP", "KR"]) & (JK.data == "s1") & (JK.at_risk == 1) & ~JK.code.str[:2].isin(TEXTILE)], "challenger")
spec_jk = [("post + lx_ch + lm_us + C(fe)", "post", False, "crossover indicator, at given exports and imports (rate ratio)"),
           ("lr + lx_ch + lm_us + C(fe)", "lr", True, "log export ratio, at given exports and imports (per doubling)")]
block(JK, "Japan and Korea, SITC Rev. 1", spec_jk, [["B-03"], ["B-13"], ["B-04"], ["B-03", "B-13"], ["B-03", "B-13", "B-04"]])

# further cases: sectoral broad measures without GSP graduation, as in robust_broad.py
GL = {"B-02", "B-17", "B-19", "B-34", "B-31", "B-29"}
Q = pd.read_csv(D / "cases_panel.csv", dtype={"code": str})
H = {}
for t, d, c in Q[["challenger", "data", "code"]].drop_duplicates().itertuples(index=False):
    H[(t, d, c)] = sorted(int(r.year) for _, r in reg.iterrows()
                          if t in r.target.split(";") and r.instrument_id not in GL and covers(r, d, c))
Q["broad"] = [int(y in H[(t, d, c)]) for t, d, c, y in zip(Q.challenger, Q.data, Q.code, Q.year)]
Q = Q[[not any(h < y for h in H[(t, d, c)]) for t, d, c, y in zip(Q.challenger, Q.data, Q.code, Q.year)]]
Q = prep(Q, "src")
ev = Q[Q.broad == 1]
src = {}
for r in ev.itertuples():
    ids = [x.instrument_id for _, x in reg.iterrows() if r.challenger in x.target.split(";") and x.instrument_id not in GL
           and int(x.year) == r.year and covers(x, r.data, r.code)]
    for i in ids:
        src[i] = src.get(i, 0) + 1
out.append("")
out.append("Further cases: starts by measure: " + ", ".join(f"{k} {v}" for k, v in sorted(src.items(), key=lambda z: -z[1])))
big = [k for k, _ in sorted(src.items(), key=lambda z: -z[1])[:2]]
block(Q, "Further cases (seven economies)", [("lr + lx_ch + C(fe)", "lr", True, "log export ratio, at given exports (per doubling)")],
      [[big[0]], [big[1]], big])

# (c) measure-level placebo
out += ["", "Measure-level placebo: mean log export ratio of the covered groups in the start year against shifted years"]
for lab, P0, G in [("Japan and Korea", pd.read_csv(D / "population_panel.csv", dtype={"code": str}), {"B-02", "B-17", "B-19"}),
                   ("further cases", pd.read_csv(D / "cases_panel.csv", dtype={"code": str}), GL)]:
    P0 = P0 if lab != "Japan and Korea" else P0[P0.challenger.isin(["JP", "KR"]) & (P0.data == "s1") & ~P0.code.str[:2].isin(TEXTILE)]
    P0 = P0.assign(lr=np.clip(np.log((P0.x_ch + 1e5) / (P0.x_us + 1e5)), -5, 5))
    LR = P0.set_index(["challenger", "data", "code", "year"]).lr
    rows = []
    for _, r in reg.iterrows():
        if r.instrument_id in G:
            continue
        for t in r.target.split(";"):
            sc = [k for k in P0[P0.challenger == t][["data", "code"]].drop_duplicates().itertuples(index=False)
                  if covers(r, k.data, k.code)]
            if not sc:
                continue
            def mean_at(y):
                v = [LR.get((t, d, c, y)) for d, c in sc]
                v = [x for x in v if x is not None and not pd.isna(x)]
                return np.mean(v) if v else np.nan
            y0 = int(r.year)
            obs = mean_at(y0)
            if pd.isna(obs):
                continue
            alt = {s: mean_at(y0 + s) for s in range(-10, 11) if s != 0}
            alt = {s: v for s, v in alt.items() if not pd.isna(v)}
            if alt:
                rows.append((r.instrument_id, t, obs, alt))
    obs_mean = np.mean([o for _, _, o, _ in rows])
    draws = []
    for _ in range(10000):
        draws.append(np.mean([a[rng.choice(list(a))] for _, _, _, a in rows]))
    draws = np.array(draws)
    out.append(f"  {lab}: {len(rows)} measure-target pairs; observed mean log ratio {obs_mean:.2f}, placebo mean {draws.mean():.2f}; "
               f"one-sided p={np.mean(draws >= obs_mean):.4f}")
    out.append("    " + "; ".join(f"{i} {t} {o:.2f}" for i, t, o, _ in rows))
(D / "robust_measure.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
