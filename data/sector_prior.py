"""Referee point 6: does congressional voice before displacement proxy for earlier protection of the sector?

Sector table (28 sectors of Japan and Korea): data/ds1_share_test.csv (measure, volume before the crossover) and the
sector controls (US employment, US imports from the challenger) printed by crecb_controls.py in
data/ds1_share_controls.txt (raw inputs of that script are not redistributed; the table is read from its output).
Prior protection: the sector already drew a broad measure aimed at an earlier challenger (Japan) before this
challenger's crossover year (data/broad_register.csv). For Japan the register holds no earlier challenger, so the
indicator is zero; the textile and steel sectors are also dropped in turn.
Linear probability model, country indicator; one-sided permutation p for log volume (10,000 draws within country).
Output: data/sector_prior.txt
"""
import io
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

D = Path(__file__).resolve().parent
S = pd.read_csv(D / "ds1_share_test.csv")
txt = (D / "ds1_share_controls.txt").read_text().splitlines()
i = next(k for k, l in enumerate(txt) if l.strip().startswith("challenger") and "emp" in l)
tab = pd.read_fwf(io.StringIO("\n".join(txt[i:i + 29])))
X = S.merge(tab[["challenger", "sector", "emp", "imp"]], on=["challenger", "sector"])
X["y"] = X.measure.astype(int)
X["l_vol"] = np.log1p(X.volume_pre.fillna(X.volume_window))
X["l_emp"], X["l_m_us"] = np.log1p(X.emp), np.log1p(X.imp)
reg = pd.read_csv(D / "broad_register.csv", dtype=str)
year = reg.set_index("instrument_id").year.astype(int)
jp_first = {r.sector: min(year[k] for k in r.measure_ids.split(";")) for r in S[(S.challenger == "JP") & S.measure].itertuples()}
X["prior"] = [int(c == "KR" and s in jp_first and jp_first[s] < cy) for c, s, cy in zip(X.challenger, X.sector, X.crossover_year)]
out = [f"{len(X)} sectors, {int(X.y.sum())} with a broad measure; prior protection (Korean sectors already protected against Japan "
       f"before Korea's crossover): {', '.join(X[X.prior == 1].sector)}"]
rng = np.random.default_rng(1995)


def run(df, f, label):
    m = smf.ols(f, df).fit(cov_type="HC1")
    obs, cnt = m.params["l_vol"], 0
    for _ in range(10000):
        yy = df.groupby("challenger").y.transform(lambda s: rng.permutation(s.values))
        cnt += smf.ols(f, df.assign(y=yy)).fit().params["l_vol"] >= obs
    extra = f"; prior {m.params['prior']:+.3f} (HC1 p={m.pvalues['prior']:.3f})" if "prior" in f else ""
    out.append(f"{label}: N={len(df)}, with measure {int(df.y.sum())}; l_vol {obs:+.3f} (permutation p={cnt / 10000:.3f}){extra}")


base = "y ~ l_vol + l_emp + l_m_us + C(challenger)"
run(X, base, "(1) baseline, as in crecb_controls.py")
run(X, base + " + prior", "(2) + prior protection")
run(X[X.sector != "textiles"], base, "(3) without textiles")
run(X[~X.sector.isin(["textiles", "steel"])], base, "(4) without textiles and steel")
run(X[X.prior == 0], base, "(5) without sectors with prior protection")
(D / "sector_prior.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
