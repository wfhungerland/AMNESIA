"""Drittmaerkte 1871-1913: Ausfuhren der USA und Deutschlands im Verhaeltnis zu Grossbritannien.

Quelle: CEPII TRADHIST v4 (Fouquin und Hugot 2016), bilaterale Handelsstroeme in laufenden Pfund.
Fester Kreis von 17 Maerkten, die 1880, 1885, ..., 1913 fuer alle drei Lieferlaender Werte haben.
Aufruf: python3 data/third_markets.py (vorher data/raw/TRADHIST_v4.dta laden, siehe fetch.sh)
"""
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent
d = pd.read_stata(D / "raw" / "TRADHIST_v4.dta", columns=["iso_o", "iso_d", "year", "FLOW", "REGIO_d", "CONTI_d"])
d = d[(d.year.between(1860, 1913)) & d.iso_o.isin(["GBR", "USA", "DEU"]) & ~d.iso_d.isin(["GBR", "USA", "DEU"]) & d.FLOW.notna()]
w = d.pivot_table(index=["iso_d", "year"], columns="iso_o", values="FLOW", aggfunc="sum").reset_index()
w = w.join(d.drop_duplicates("iso_d").set_index("iso_d")[["REGIO_d", "CONTI_d"]], on="iso_d")
w.to_csv(D / "third_markets_tradhist.csv", index=False)
b = w.dropna(subset=["GBR", "USA", "DEU"])
yrs = [1880, 1885, 1890, 1895, 1900, 1905, 1910, 1913]
keep = set.intersection(*[set(b[b.year == y].iso_d) for y in yrs])
p = b[b.iso_d.isin(keep)]
rows = []
for label, x in [("all_17", p), ("without_canada", p[p.iso_d != "CAN"])]:
    g = x.groupby("year")[["GBR", "USA", "DEU"]].sum()
    for y in yrs:
        s = x[x.year == y]
        rows.append({"panel": label, "year": y, "usa_vs_gbr": round(g.at[y, "USA"] / g.at[y, "GBR"], 3),
                     "deu_vs_gbr": round(g.at[y, "DEU"] / g.at[y, "GBR"], 3),
                     "markets_usa_above_gbr": " ".join(sorted(s[s.USA > s.GBR].iso_d)),
                     "markets_deu_above_gbr": " ".join(sorted(s[s.DEU > s.GBR].iso_d))})
out = pd.DataFrame(rows)
out.to_csv(D / "third_markets_summary.csv", index=False)
print("Maerkte:", sorted(keep))
print(out.to_string(index=False))
