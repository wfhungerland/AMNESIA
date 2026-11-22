"""China: Sektorvolumen im Kongress gegen Beschaeftigung und US-Einfuhren kontrolliert (17 Feinsektoren).

Volumen: Wirtschaftsdebatten des Sektors (mindestens 3 Sektorwoerter, data/ds1_crec_sector_years.csv) je
1.000 Wirtschaftsdebatten, im festen Fenster 2001-2017 (nach dem WTO-Beitritt, vor den Massnahmen von
2018-2024) und in den 5 Jahren vor der Kreuzung, wo der Record (ab 1995) sie abdeckt.
Kontrollen wie crecb_controls.py fuer jede Kreuzungsgruppe Chinas in data/population_crossovers.csv (SITC Rev. 3
und HS4) im Kreuzungsjahr: US-Beschaeftigung (NBER-CES, bis 2018; spaeter 2018) und US-Einfuhren aus China
(UN Comtrade). Je Sektor werden die Gruppen der Klassifikation summiert, aus der das Kreuzungsjahr des Sektors
stammt (bei Gleichstand SITC Rev. 3), damit dieselben Waren nicht doppelt zaehlen.
Massnahme: sektorspezifisches breites Instrument ohne die 301-Zoelle von 2018 (data/ds1_crec_voice_test.csv).
(1) Sektorebene: measure ~ l_vol + l_emp + l_m_us, lineares Wahrscheinlichkeitsmodell, p aus 10.000 Permutationen.
(2) Gruppenebene: Logit mit dem Instrument des Sektors als Ergebnis, Standardfehler nach Sektor geclustert.
Ergebnis: data/ds1_crec_controls.txt. Aufruf: python3 data/crec_controls.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
from crec_filter import fine_of  # noqa: E402

n = pd.read_csv(D / "raw/nberces/n1997.csv", dtype={"naics": str})[["naics", "year", "emp"]]
c = pd.read_excel(D / "raw/census/impconcord02.xls", dtype=str)
c = c[c.NAICS.str[:1] == "3"]
c["g_s3"], c["g_hs4"] = c.SITC.str[:3], c.COMMODITY.str[:4]
shares = {}
for data in ("s3", "hs4"):
    z = c.dropna(subset=[f"g_{data}"])
    k = z.groupby(["NAICS", f"g_{data}"]).size().rename("k").reset_index()
    k["share"] = k.k / k.groupby("NAICS").k.transform("sum")
    shares[data] = k.rename(columns={f"g_{data}": "code", "NAICS": "naics"})[["naics", "code", "share"]]


def emp(data, code, year):
    s = shares[data][shares[data].code == code]
    e = n[(n.year == min(max(year, 1958), 2018)) & n.naics.isin(s.naics)].merge(s, on="naics")
    return (e.emp * e.share).sum() if len(e) else np.nan


imp = pd.read_csv(D / "raw/comtrade_us_imports_groups.csv", dtype={"code": str})
imp["data"] = imp.cl.map({"S1": "s1", "S3": "s3", "HS": "hs4"})
imp = imp[imp.partner == 156].groupby(["data", "code", "year"]).value.sum()
W = pd.read_csv(D / "population_crossovers.csv", dtype={"code": str})
W = W[W.challenger == "CN"].copy()
W["sector"] = [fine_of(d, cd) for d, cd in zip(W.data, W.code)]
W = W.dropna(subset=["sector"])
W["emp_k"] = [emp(d, cd, int(y)) for d, cd, y in zip(W.data, W.code, W.crossover_year)]
W["m_us"] = [imp.get((d, cd, int(y)), 0.0) for d, cd, y in zip(W.data, W.code, W.crossover_year)]
W["l_emp"], W["l_m_us"] = np.log1p(W.emp_k), np.log1p(W.m_us / 1e6)
PW = pd.read_csv(D / "population_weight.csv", dtype={"code": str})
chk = W.merge(PW[PW.challenger == "CN"][["data", "code", "l_m_us", "emp_k"]], on=["data", "code"], suffixes=("", "_pw"))

T = pd.read_csv(D / "ds1_crec_voice_test.csv")
SY = pd.read_csv(D / "ds1_crec_sector_years.csv")


def vol(sec, a, b):
    z = SY[(SY.sector == sec) & SY.year.between(a, b)]
    return 1000 * z.debates.sum() / z.econ_granules.sum() if len(z) and z.econ_granules.sum() else np.nan


T["volume_2001_2017"] = [vol(s, 2001, 2017) for s in T.sector]
T["volume_pre"] = [vol(s, cy - 5, cy - 1) if cy - 5 >= 1995 else np.nan for s, cy in zip(T.sector, T.crossover_year)]
rows = []
for s, cy in zip(T.sector, T.crossover_year):
    z = W[W.sector == s]
    first = z[z.crossover_year == z.crossover_year.min()]
    cl = "s3" if (first.data == "s3").any() else "hs4"
    q = z[z.data == cl]
    rows.append({"sector": s, "class": cl, "groups": len(q), "emp": q.emp_k.sum(), "imp": q.m_us.sum() / 1e6})
X = T.merge(pd.DataFrame(rows), on="sector")
X["l_vol"], X["l_emp"], X["l_m_us"], X["y"] = (np.log1p(X.volume_2001_2017), np.log1p(X.emp), np.log1p(X.imp),
                                               X.measure.astype(int))
out = [f"Abgleich mit data/population_weight.csv ({len(chk)} gemeinsame Gruppen): groesste Abweichung l_m_us "
       f"{(chk.l_m_us - chk.l_m_us_pw).abs().max():.3f}, emp_k {(chk.emp_k - chk.emp_k_pw).abs().max():.3f}",
       f"(1) Sektorebene: {len(X)} Sektoren, davon mit Massnahme {int(X.y.sum())}",
       X[["sector", "measure", "crossover_year", "volume_pre", "volume_2001_2017", "class", "groups", "emp", "imp"]].round(2).to_string(index=False)]
rng = np.random.default_rng(2001)
for f in ["y ~ l_vol", "y ~ l_emp", "y ~ l_m_us", "y ~ l_vol + l_emp + l_m_us"]:
    m = smf.ols(f, X).fit(cov_type="HC1")
    txt = []
    for t in [t for t in ("l_vol", "l_emp", "l_m_us") if t in f]:
        obs = m.params[t]
        cnt = sum(smf.ols(f, X.assign(y=rng.permutation(X.y.values))).fit().params[t] >= obs for _ in range(10000))
        txt.append(f"{t} {obs:+.3f} (HC1 p={m.pvalues[t]:.3f}; Permutation einseitig p={cnt/10000:.3f})")
    out.append(f"   {f}: " + "; ".join(txt))
out.append("   Spearman: " + "; ".join(f"{a}/{b} {X[a].corr(X[b], method='spearman'):+.2f}"
                                       for a, b in (("l_vol", "l_emp"), ("l_vol", "l_m_us"), ("l_emp", "l_m_us"))))
G = W.merge(X[["sector", "l_vol", "y"]], on="sector").dropna(subset=["l_emp"])
G["src"] = G.data
out.append(f"(2) Gruppenebene: {len(G)} Gruppen in {G.sector.nunique()} Sektoren; Sektor mit Massnahme in {int(G.y.sum())} Gruppen")
for f in ["y ~ l_vol + C(src)", "y ~ l_emp + l_m_us + C(src)", "y ~ l_vol + l_emp + l_m_us + C(src)"]:
    try:
        m = smf.logit(f, G).fit(disp=0, cov_type="cluster", cov_kwds={"groups": G.sector.astype("category").cat.codes})
        out.append(f"   {f}: " + "; ".join(f"{t} {m.params[t]:+.2f} (p={m.pvalues[t]:.3f})" for t in ("l_vol", "l_emp", "l_m_us") if t in f))
    except Exception as e:
        out.append(f"   {f}: nicht schaetzbar ({type(e).__name__})")
(D / "ds1_crec_controls.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
