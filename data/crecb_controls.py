"""Sektorvolumen im Kongress gegen Beschaeftigung und US-Einfuhren kontrolliert (Japan, Korea).

Kontrollen aus data/population_weight.csv: l_emp = log US-Beschaeftigung (Tsd., NBER-CES) im Kreuzungsjahr,
l_m_us = log US-Einfuhren aus dem Aufsteiger (Mio. USD) im Kreuzungsjahr; nur Gruppen mit Kreuzung nach dem
ersten Datenjahr. Sektorvolumen vor der Kreuzung aus data/ds1_share_test.csv (Nennungen je 1 Mio. Woerter).

(1) Sektorebene: Sektoren mit Kontrollen; Beschaeftigung und Einfuhren je Sektor summiert.
    Lineares Wahrscheinlichkeitsmodell measure ~ l_vol + l_emp + l_m_us + Land; p-Wert fuer l_vol aus
    10.000 Permutationen von measure innerhalb des Landes.
(2) Gruppenebene wie data/population_employment.py: broad10 ~ l_vol + l_emp + l_m_us + C(src), Logit,
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

W = pd.read_csv(D / "population_weight.csv", dtype={"code": str})
W = W[W.challenger.isin(["JP", "KR"])].copy()
W["sector"] = [jp_fine_of(c) if ch == "JP" else K.kr_of(d, c) for ch, d, c in zip(W.challenger, W.data, W.code)]
S = pd.read_csv(D / "ds1_share_test.csv")
S["l_vol"] = np.log1p(S.volume_pre.fillna(S.volume_window))
out = []

agg = (W.dropna(subset=["sector"]).assign(emp=lambda z: z.emp_k, imp=lambda z: np.expm1(z.l_m_us))
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

G = W.merge(S[["challenger", "sector", "l_vol"]], on=["challenger", "sector"], how="inner").dropna(subset=["l_emp", "l_m_us"])
out.append(f"(2) Gruppenebene: {len(G)} verdraengte Gruppen in {G.sector.nunique()} Sektoren; broad10 = 1 in {int(G.broad10.sum())}")
for f in ["broad10 ~ l_vol + C(src)", "broad10 ~ l_emp + l_m_us + C(src)", "broad10 ~ l_vol + l_emp + l_m_us + C(src)"]:
    try:
        m = smf.logit(f, G).fit(disp=0, cov_type="cluster", cov_kwds={"groups": G.sector.astype("category").cat.codes})
        out.append(f"   {f}: " + "; ".join(f"{t} {m.params[t]:+.2f} (p={m.pvalues[t]:.3f})" for t in ("l_vol", "l_emp", "l_m_us") if t in f))
    except Exception as e:  # perfekte Trennung o. Ae.
        out.append(f"   {f}: nicht schaetzbar ({type(e).__name__})")
(D / "ds1_share_controls.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
