"""Gutachten, Gewicht verdraengter Sektoren: US-Beschaeftigung je Warengruppe als Mass des politischen Gewichts.

Quelle: NBER-CES Manufacturing Industry Database (nberces5818v1, NAICS 1997, 1958-2018), Beschaeftigte in Tausend.
Zuordnung: Census-Konkordanz der Einfuhrwaren 2002 (HS10 -> NAICS, SITC Rev. 3); HS6 -> SITC Rev. 1 ueber WITS.
Jede NAICS-Industrie wird auf die Warengruppen nach dem Anteil ihrer HS10-Positionen verteilt (Naeherung ohne Werte).
Beschaeftigung im Kreuzungsjahr (fuer Jahre nach 2018: 2018). Ergebnis: data/population_weight.csv (ergaenzt),
data/population_employment.txt
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

D = Path(__file__).resolve().parent
n = pd.read_csv(D / "raw/nberces/n1997.csv", dtype={"naics": str})[["naics", "year", "emp"]]
c = pd.read_excel(D / "raw/census/impconcord02.xls", dtype=str)
c = c[c.NAICS.str[:1] == "3"].assign(hs6=lambda z: z.COMMODITY.str[:6])
w1 = pd.read_csv(D / "raw/wits/H0_S1/JobID-9_Concordance_H0_to_S1.CSV", dtype=str, encoding="latin1").iloc[:, [0, 2]]
w1.columns = ["hs6", "s1"]
s1map = w1.assign(g=w1.s1.str[:3]).groupby("hs6").g.first()
c["g_s1"] = c.hs6.map(s1map)
c["g_s3"] = c.SITC.str[:3]
c["g_hs4"] = c.COMMODITY.str[:4]
shares = {}
for data in ("s1", "s3", "hs4"):
    z = c.dropna(subset=[f"g_{data}"])
    k = z.groupby(["NAICS", f"g_{data}"]).size().rename("k").reset_index()
    k["share"] = k.k / k.groupby("NAICS").k.transform("sum")
    shares[data] = k.rename(columns={f"g_{data}": "code", "NAICS": "naics"})[["naics", "code", "share"]]


def emp(data, code, year):
    s = shares[data][shares[data].code == code]
    e = n[(n.year == min(max(year, 1958), 2018)) & n.naics.isin(s.naics)].merge(s, on="naics")
    return (e.emp * e.share).sum() if len(e) else np.nan


W = pd.read_csv(D / "population_weight.csv", dtype={"code": str})
W["emp_k"] = [emp(d, cd, y) for d, cd, y in zip(W.data, W.code, W.crossover_year)]
W["l_emp"] = np.log1p(W.emp_k)
W.to_csv(D / "population_weight.csv", index=False)
out = [f"Gruppen mit Beschaeftigung: {W.emp_k.notna().sum()} von {len(W)}; Median {W.emp_k.median():.1f} Tsd."]
for y, sub, lab in (("broad10", W[(W.data == "s1") & ~W.code.astype(str).str[:2].isin(["65", "84"])], "breite Massnahme binnen 10 J., JP und KR (s1), ohne Textil (SITC 65, 84)"),
                    ("ad5", W.dropna(subset=["ad5"]), "AD/CVD binnen 5 J., alle Quellen")):
    sub = sub.dropna(subset=["l_emp"])
    fe = " + C(src)" if sub.src.nunique() > 1 else ""
    for f in (f"{y} ~ l_emp{fe}", f"{y} ~ l_emp + l_m_us{fe}"):
        m = smf.glm(f, data=sub, family=sm.families.Binomial()).fit(cov_type="HC1")
        out.append(f"{lab} | {f}: N={len(sub)}; " + "; ".join(f"{k} {m.params[k]:+.2f} (p={m.pvalues[k]:.3f})" for k in m.params.index if k.startswith("l_")))
    t = sub.assign(t=pd.qcut(sub.l_emp.rank(method="first"), 3, labels=["niedrig", "mittel", "hoch"])).groupby("t", observed=True)
    out.append("   nach Terzil der Beschaeftigung: " + ", ".join(f"{k} {v:.2f} (Median {e:.0f} Tsd.)" for (k, v), e in zip(t[y].mean().items(), t.emp_k.median())))
(D / "population_employment.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
