"""Washington Consensus als dritter Kanal: IWF-Auflagen, US-Hilfe, Sitz im Sicherheitsrat und Naehe zu den USA,
im Vergleich mit der Verdraengung der USA durch die Aufsteiger dieses Papers.

Quellen (Harvard Dataverse, siehe fetch.sh):
- Stubbs, Reinsberg, Kentikelenis und King (2020), Replikationsdaten (doi:10.7910/DVN/YSZ79K): Land-Jahr 1989-2014,
  IWF-Programm (IMF55), Zahl der bindenden Auflagen BA2TOT = QPCsTOT + SPCsTOT + PAsTOT (quantitative und strukturelle
  Leistungskriterien, Vorabmassnahmen; im Datensatz nachgerechnet) nach Politikfeld (EXT Aussenwirtschaft, FIN Finanzsektor,
  PRI Privatisierung, SOE Staatsunternehmen u. a.), Sitz im Sicherheitsrat (unsc), Abstimmungsnaehe zu den USA (unga).
  Programmjahre ohne erfasste Auflagen (z. B. Thailand 1997-2000) gelten als fehlend.
- Replikationsdaten zu IWF und Gebern (doi:10.7910/DVN/TE8TXZ): Land-Jahr 1960-2012, US-Hilfezusagen (ac_USA, OECD DAC,
  Mio. USD von 2011), Sitz im Sicherheitsrat (s_unsc; Dreher, Sturm und Vreeland), Abstimmungsnaehe (s_unga3USA),
  Verteidigungsbuendnis (s_milUSA). Nur Empfaenger von Hilfe (ohne Korea).
- Reichweite der Verdraengung: data/cases_breadth.csv (Anteil der US-Industrieausfuhren in ueberholten Gruppen).
Ergebnis: data/conditionality.txt, data/conditionality_challengers.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

D = Path(__file__).resolve().parent
R = D / "raw" / "imf"
out = []
m = pd.read_stata(R / "IMFMETH_Data.dta", convert_categoricals=False)
m["lgdppc"] = np.log(m.gdppc_WDI)
m["state_role"] = m.BA2PRI + m.BA2SOE
NAMES = {"Korea, Rep.": "KR", "Mexico": "MX", "Brazil": "BR", "Vietnam": "VN", "Thailand": "TH", "Malaysia": "MY", "China": "CN"}
m["challenger"] = m.cname.map(NAMES)

# Reichweite der Verdraengung je Aufsteiger und Jahr (SITC 1 bis 1991, SITC 3 1992-2009, HS ab 2010)
b = pd.read_csv(D / "cases_breadth.csv")
b = b[((b.data == "s1") & (b.year <= 1991)) | ((b.data == "s3") & b.year.between(1992, 2009)) | ((b.data == "hs4") & (b.year >= 2010))]
reach = b.set_index(["challenger", "year"]).us_exports_share_overtaken
m["reach"] = [reach.get((c, y), np.nan) if isinstance(c, str) else np.nan for c, y in zip(m.challenger, m.year)]

P = m[(m.IMF55 == 1) & (m.BA1TOT > 0)].dropna(subset=["unsc", "unga", "lgdppc", "growth", "trade"]).copy()
P["year_c"] = P.year.astype(str)
out.append(f"(A) IWF-Auflagen 1989-2014: {len(P)} Programmjahre mit erfassten Auflagen, {P.cname.nunique()} Laender")
for y in ("BA2TOT", "BA2EXT", "BA2FIN", "state_role"):
    f = f"{y} ~ unsc + unga + lgdppc + growth + trade + C(year_c)"
    r = smf.glm(f, data=P, family=sm.families.Poisson()).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(P.cname)[0]})
    out.append(f"{y}: Mittel {P[y].mean():.2f}; Sicherheitsrat IRR {np.exp(r.params['unsc']):.2f} (p={r.pvalues['unsc']:.3f}); "
               f"Naehe zu den USA (0-1) IRR {np.exp(r.params['unga']):.2f} (p={r.pvalues['unga']:.3f})")
# Gegenprobe mit Laendereffekten (Variation innerhalb eines Landes)
for y in ("BA2TOT", "BA2EXT", "BA2FIN"):
    r = smf.glm(f"{y} ~ unsc + unga + lgdppc + growth + trade + C(year_c) + C(cname)", data=P, family=sm.families.Poisson()).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(P.cname)[0]})
    out.append(f"{y} mit Laendereffekten: Sicherheitsrat IRR {np.exp(r.params['unsc']):.2f} (p={r.pvalues['unsc']:.3f}); "
               f"Naehe zu den USA IRR {np.exp(r.params['unga']):.2f} (p={r.pvalues['unga']:.3f})")
# Programmteilnahme (Logit, alle Land-Jahre)
A = m.dropna(subset=["IMF55", "unsc", "unga", "lgdppc", "growth", "trade"]).copy()
A["year_c"] = A.year.astype(str)
r = smf.glm("IMF55 ~ unsc + unga + lgdppc + growth + trade + C(year_c)", data=A, family=sm.families.Binomial()).fit(
    cov_type="cluster", cov_kwds={"groups": pd.factorize(A.cname)[0]})
out.append(f"Programmteilnahme (Logit, {len(A)} Land-Jahre): Sicherheitsrat {r.params['unsc']:+.2f} (p={r.pvalues['unsc']:.3f}); "
           f"Naehe zu den USA {r.params['unga']:+.2f} (p={r.pvalues['unga']:.3f})")
# Aufsteiger: Programmjahre im Vergleich zu allen anderen Programmjahren
P["is_ch"] = P.challenger.notna().astype(int)
for y in ("BA2TOT", "BA2EXT", "state_role"):
    r = smf.glm(f"{y} ~ is_ch + unsc + unga + lgdppc + growth + trade + C(year_c)", data=P, family=sm.families.Poisson()).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(P.cname)[0]})
    out.append(f"{y}: Aufsteiger dieses Papers gegen andere Programmlaender IRR {np.exp(r.params['is_ch']):.2f} (p={r.pvalues['is_ch']:.3f})")

CH = m[m.challenger.notna()][["challenger", "year", "IMF55", "BA2TOT", "BA2EXT", "BA2FIN", "state_role", "unsc", "unga", "reach"]]
CH = CH[(CH.IMF55 == 1) | (CH.unsc == 1)]
CH.to_csv(D / "conditionality_challengers.csv", index=False)
out += ["", "Aufsteiger: Programm- und Ratsjahre (Auflagen 0 bei Thailand = nicht erfasst)", CH.to_string(index=False)]

# (B) US-Hilfe 1960-2012
a = pd.read_stata(R / "IMFAIDData.dta", convert_categoricals=False)
a["year"] = pd.to_datetime(a.year).dt.year if not np.issubdtype(a.year.dtype, np.number) else a.year
a = a.dropna(subset=["ac_USA", "s_unsc", "s_unga3USA", "s_milUSA", "n_lngdppcppp"]).copy()
a["lus"] = np.log1p(a.ac_USA.clip(lower=0))
r = smf.ols("lus ~ s_unsc + s_unga3USA + s_milUSA + n_lngdppcppp + C(cname) + C(year)", data=a).fit(
    cov_type="cluster", cov_kwds={"groups": pd.factorize(a.cname)[0]})
out += ["", f"(B) US-Hilfezusagen, log(1+Mio. USD), Land- und Jahreseffekte, {len(a)} Land-Jahre {a.year.min()}-{a.year.max()}:",
        f"Sicherheitsrat {r.params['s_unsc']:+.3f} (p={r.pvalues['s_unsc']:.3f}); Abstimmungsnaehe {r.params['s_unga3USA']:+.3f} "
        f"(p={r.pvalues['s_unga3USA']:.3f}); Buendnis {r.params['s_milUSA']:+.3f} (p={r.pvalues['s_milUSA']:.3f})"]
(D / "conditionality.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
