"""Drittmaerkte 1920-1938: Ausfuhren Japans im Verhaeltnis zu Grossbritannien (Fall Japan gegen Britannien).

Quelle: CEPII TRADHIST v4 (Fouquin und Hugot 2016), bilaterale Gesamtausfuhren, laufende Pfund. Keine Warengliederung:
Gemessen wird die Verdraengung im Gesamthandel; Baumwollwaren sind der groesste Posten der japanischen Ausfuhren
in diese Maerkte, aber nicht der einzige (Milestone auf Warenebene aus der Literatur, siehe ds1_milestones.csv).
Ohne Japans Kolonien und Pachtgebiete (KOR, TWN, KWANTU) und ohne Grossbritannien und Japan selbst.
Fester Kreis: Maerkte mit Werten fuer beide Lieferlaender in jedem Jahr 1924-1938.
Ergebnis: data/third_markets_1930s.csv (Markt x Jahr), data/third_markets_1930s_summary.csv
Aufruf: python3 data/third_markets_1930s.py (vorher data/raw/TRADHIST_v4.dta laden, siehe fetch.sh)
"""
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent
EXCL = {"GBR", "JPN", "KOR", "TWN", "KWANTU"}
EMPIRE = {"GBRIND", "LKA", "MMR", "STRAITS", "FEDMYS", "MYS", "HKG", "EGY", "KEN", "NGA", "GHA", "ADEN", "AUS", "NZL",
          "ZAF", "CAN", "JAM", "TTO", "FJI", "MUS", "SDN", "ZANZ", "MLT", "IRL"}
d = pd.read_stata(D / "raw" / "TRADHIST_v4.dta", columns=["iso_o", "iso_d", "year", "FLOW"])
d = d[d.year.between(1920, 1938) & d.iso_o.isin(["GBR", "JPN"]) & ~d.iso_d.isin(EXCL) & d.FLOW.notna()]
w = d.pivot_table(index=["iso_d", "year"], columns="iso_o", values="FLOW", aggfunc="sum").reset_index()
w["empire"] = w.iso_d.isin(EMPIRE)
w.to_csv(D / "third_markets_1930s.csv", index=False)
b = w.dropna(subset=["GBR", "JPN"])
yrs = list(range(1924, 1939))
keep = set.intersection(*[set(b[b.year == y].iso_d) for y in yrs])
p = b[b.iso_d.isin(keep)]
rows = []
for label, x in [("all", p), ("british_empire", p[p.empire]), ("outside_empire", p[~p.empire]),
                 ("asia_key", p[p.iso_d.isin(["GBRIND", "CHN", "IDN", "STRAITS", "HKG", "PHL", "LKA", "MMR", "THA"])])]:
    g = x.groupby("year")[["GBR", "JPN"]].sum()
    for y in yrs:
        s = x[x.year == y]
        rows.append({"panel": label, "year": y, "markets": len(s), "jpn_vs_gbr": round(g.at[y, "JPN"] / g.at[y, "GBR"], 3),
                     "markets_jpn_above_gbr": int((s.JPN > s.GBR).sum()),
                     "list_jpn_above_gbr": " ".join(sorted(s[s.JPN > s.GBR].iso_d))})
out = pd.DataFrame(rows)
out.to_csv(D / "third_markets_1930s_summary.csv", index=False)
print("Maerkte:", len(keep), sorted(keep))
print(out.drop(columns="list_jpn_above_gbr").to_string(index=False))
for m in ["GBRIND", "IDN", "CHN", "EGY", "STRAITS", "LKA", "MMR"]:
    s = p[p.iso_d == m].set_index("year")
    if len(s):
        print(m, " ".join(f"{y}:{r:.2f}" for y, r in (s.JPN / s.GBR).items()))
