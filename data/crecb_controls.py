"""Sektorvolumen im Kongress gegen Beschaeftigung und US-Einfuhren kontrolliert (Japan, Korea).

Kontrollen fuer alle Kreuzungsgruppen in data/population_crossovers.csv (Japan SITC Rev. 1, Korea SITC Rev. 1
und Rev. 3), auch jene mit Kreuzung im ersten Datenjahr, nach den Regeln von data/population_employment.py und
data/population_panel.py: l_emp = log US-Beschaeftigung (Tsd., NBER-CES nberces5818v1, NAICS-Industrien nach dem
Anteil ihrer HS10-Positionen auf die Gruppen verteilt, Census-Konkordanz 2002, HS6 -> SITC Rev. 1 ueber WITS) im
Kreuzungsjahr (frueher als 1958: 1958); l_m_us = log(1 + US-Einfuhren aus dem Aufsteiger in Mio. USD) im
Kreuzungsjahr (UN Comtrade, data/raw/comtrade_us_imports_groups.csv). Rohdaten: data/fetch.sh.
Sektorvolumen vor der Kreuzung aus data/ds1_share_test.csv (Nennungen je 1 Mio. Woerter).

(1) Sektorebene: Sektoren mit Kontrollen; Beschaeftigung und Einfuhren je Sektor summiert.
    Lineares Wahrscheinlichkeitsmodell measure ~ l_vol + l_emp + l_m_us + Land; p-Wert fuer l_vol aus
    10.000 Permutationen von measure innerhalb des Landes.
(2) Gruppenebene: broad (Sektor der Gruppe mit breiter Massnahme) ~ l_vol + l_emp + l_m_us + C(src), Logit,
    Standardfehler nach Sektor geclustert; l_vol ist das Volumen des Sektors der Gruppe.
Ergebnis: data/ds1_share_controls.txt. Aufruf: python3 data/crecb_controls.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import crecb_korea as K  # noqa: E402
from crec_filter import jp_fine_of  # noqa: E402

n = pd.read_csv(D / "raw/nberces/n1997.csv", dtype={"naics": str})[["naics", "year", "emp"]]
c = pd.read_excel(D / "raw/census/impconcord02.xls", dtype=str)
c = c[c.NAICS.str[:1] == "3"].assign(hs6=lambda z: z.COMMODITY.str[:6])
w1 = pd.read_csv(D / "raw/wits/H0_S1/JobID-9_Concordance_H0_to_S1.CSV", dtype=str, encoding="latin1").iloc[:, [0, 2]]
w1.columns = ["hs6", "s1"]
c["g_s1"] = c.hs6.map(w1.assign(g=w1.s1.str[:3]).groupby("hs6").g.first())
c["g_s3"] = c.SITC.str[:3]
shares = {}
for data in ("s1", "s3"):
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
imp = imp.groupby(["partner", "data", "code", "year"]).value.sum()
REP = {"JP": 392, "KR": 410}
W = pd.read_csv(D / "population_crossovers.csv", dtype={"code": str})
W = W[W.challenger.isin(["JP", "KR"]) & W.data.isin(["s1", "s3"])].copy()
W["emp_k"] = [emp(d, cd, int(y)) for d, cd, y in zip(W.data, W.code, W.crossover_year)]
W["m_us"] = [imp.get((REP[ch], d, cd, int(y)), 0.0) for ch, d, cd, y in zip(W.challenger, W.data, W.code, W.crossover_year)]
W["l_emp"], W["l_m_us"] = np.log1p(W.emp_k), np.log1p(W.m_us / 1e6)
W["sector"] = [jp_fine_of(c) if ch == "JP" else K.kr_of(d, c) for ch, d, c in zip(W.challenger, W.data, W.code)]
W["src"] = W.challenger + "_" + W.data
PW = pd.read_csv(D / "population_weight.csv", dtype={"code": str})
chk = W.merge(PW[["challenger", "data", "code", "l_m_us", "emp_k"]], on=["challenger", "data", "code"], suffixes=("", "_pw"))
S = pd.read_csv(D / "ds1_share_test.csv")
S["l_vol"] = np.log1p(S.volume_pre.fillna(S.volume_window))
out = [f"Abgleich mit data/population_weight.csv ({len(chk)} gemeinsame Gruppen): groesste Abweichung l_m_us "
       f"{(chk.l_m_us - chk.l_m_us_pw).abs().max():.3f}, emp_k {(chk.emp_k - chk.emp_k_pw).abs().max():.3f}"]

agg = (W.dropna(subset=["sector"]).assign(emp=lambda z: z.emp_k, imp=lambda z: z.m_us / 1e6)
       .groupby(["challenger", "sector"], as_index=False).agg(emp=("emp", "sum"), imp=("imp", "sum"), groups=("code", "size")))
X = S.merge(agg, on=["challenger", "sector"], how="inner")
X["l_emp"], X["l_m_us"], X["y"] = np.log1p(X.emp), np.log1p(X.imp), X.measure.astype(int)
out.append(f"(1) Sektorebene: {len(X)} Sektoren mit Kontrollen (JP {int((X.challenger=='JP').sum())}, KR {int((X.challenger=='KR').sum())}); "
           f"davon mit Massnahme {int(X.y.sum())}")
out.append(X[["challenger", "sector", "measure", "volume_pre", "volume_window", "emp", "imp", "groups"]].round(1).to_string(index=False))
rng = np.random.default_rng(1995)
for f in ["y ~ l_vol + C(challenger)", "y ~ l_emp + C(challenger)", "y ~ l_m_us + C(challenger)",
          "y ~ l_vol + l_emp + l_m_us + C(challenger)"]:
    m = smf.ols(f, X).fit(cov_type="HC1")
    terms = [t for t in ("l_vol", "l_emp", "l_m_us") if t in f]
    txt = []
    for t in terms:
        obs, cnt = m.params[t], 0
        for _ in range(10000):
            yy = X.groupby("challenger").y.transform(lambda s: rng.permutation(s.values))
            cnt += smf.ols(f, X.assign(y=yy)).fit().params[t] >= obs
        txt.append(f"{t} {obs:+.3f} (HC1 p={m.pvalues[t]:.3f}; Permutation einseitig p={cnt/10000:.3f})")
    out.append(f"   {f}: " + "; ".join(txt))
# Rangkorrelation zwischen den Groessen
out.append("   Spearman: " + "; ".join(f"{a}/{b} {X[a].corr(X[b], method='spearman'):+.2f}"
                                       for a, b in (("l_vol", "l_emp"), ("l_vol", "l_m_us"), ("l_emp", "l_m_us"))))

G = W.merge(S[["challenger", "sector", "l_vol", "measure"]], on=["challenger", "sector"], how="inner").dropna(subset=["l_emp", "l_m_us"])
G["broad"] = G.measure.astype(int)
out.append(f"(2) Gruppenebene: {len(G)} verdraengte Gruppen in {G.sector.nunique()} Sektoren; Sektor mit breiter Massnahme "
           f"in {int(G.broad.sum())} Gruppen (Ergebnis je Sektor, daher Standardfehler nach Sektor geclustert)")
for f in ["broad ~ l_vol + C(src)", "broad ~ l_emp + l_m_us + C(src)", "broad ~ l_vol + l_emp + l_m_us + C(src)"]:
    try:
        m = smf.logit(f, G).fit(disp=0, cov_type="cluster", cov_kwds={"groups": G.sector.astype("category").cat.codes})
        out.append(f"   {f}: " + "; ".join(f"{t} {m.params[t]:+.2f} (p={m.pvalues[t]:.3f})" for t in ("l_vol", "l_emp", "l_m_us") if t in f))
    except Exception as e:  # perfekte Trennung o. Ae.
        out.append(f"   {f}: nicht schaetzbar ({type(e).__name__})")
(D / "ds1_share_controls.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
