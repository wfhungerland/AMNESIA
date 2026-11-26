"""Politisch-militaerische Lage der Dyaden: erklaert sie die Art der Massnahme (ausgehandelt oder einseitig)
und Massnahmen vor der Verdraengung?

Quellen (data/raw/geo, siehe fetch.sh):
- Correlates of War, National Material Capabilities v7 (CINC, 1816-2022): militaerisch-industrielles Gewicht des
  Aufsteigers im Verhaeltnis zum Etablierten.
- ATOP 5.1 (Leeds et al.), Dyade-Jahr 1815-2018: Verteidigungsbuendnis zwischen Aufsteiger und Etabliertem.
- UNGA-Idealpunkte (Bailey, Strezhnev und Voeten 2017; Fassung Juli 2025), 1946-2025: Abstand der Positionen.
Nach 2018 (ATOP) bzw. 2022 (CINC) wird der letzte Wert fortgeschrieben und markiert.
Einheiten: (a) bindende Reaktionen mit IR >= 4 aus data/ds1_events.csv (mit Japan gegen Grossbritannien);
(b) Instrument-Ziel-Paare aus data/broad_register.csv. Art der Massnahme: data/geo_instrument_mode.csv.
Ergebnis: data/geopolitics_dyads.csv, data/geopolitics_instruments.csv, data/geopolitics.txt
"""
from pathlib import Path
import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
G = D / "raw" / "geo"
CC = {"US": 2, "GB": 200, "DE": 255, "JP": 740, "KR": 732, "CN": 710, "TW": 713, "BR": 140, "MX": 70,
      "TH": 800, "MY": 820, "VN": 816, "EU": 255, "GB+FR": 200}
nmc = pd.read_csv(next(G.glob("nmc/**/NMC-70-abridged.csv")))
atop = pd.read_csv(next(G.glob("atop/**/atop5_1dy.csv")))
unga = pd.read_csv(G / "unga" / "IdealpointsJuly2025.tab", sep="\t")


def geo(ch, inc, year):
    a, b = CC.get(ch), CC.get(inc)
    if a is None or b is None:
        return {}
    yc = min(year, 2022)
    c = nmc[nmc.year == yc].set_index("ccode").cinc
    ya = min(year, 2018)
    x = atop[(atop.mem1 == min(a, b)) & (atop.mem2 == max(a, b)) & (atop.year == ya)]
    u = unga[unga.year == year].set_index("ccode").idealpointall
    return {"cinc_ratio": round(c.get(a, np.nan) / c.get(b, np.nan), 3) if b in c and a in c else np.nan,
            "cinc_carried": year > 2022, "defense_pact": int(len(x) > 0 and x.defense.iloc[0] == 1),
            "any_alliance": int(len(x) > 0 and x.atopally.iloc[0] == 1), "atop_carried": year > 2018,
            "unga_distance": round(abs(u.get(a, np.nan) - u.get(b, np.nan)), 3) if year >= 1946 else np.nan}


mode = pd.read_csv(D / "geo_instrument_mode.csv").set_index("id")
rows = []
e = pd.read_csv(D / "ds1_events.csv")
for _, r in e[(e.reach_coder1 >= 4)].iterrows():
    ch = "JP" if r.case == "JPGB" else r.case
    rows.append({"unit": "response", "id": r.response_id, "challenger": ch, "incumbent": r.incumbent, "year": r.year,
                 "reach": r.reach_coder1, "type": r.type, "phase": r.phase, "mode": mode["mode"].get(r.response_id, "uncoded"),
                 **geo(ch, r.incumbent, r.year)})
reg = pd.read_csv(D / "broad_register.csv", dtype=str)
reg = reg[reg.reach.astype(int) >= 4]  # only broad entries (IR 4-5)
ph = pd.concat([pd.read_csv(D / "broad_register_tested.csv")[["instrument_id", "target", "phase"]],
                pd.read_csv(D / "cases_register_tested.csv")[["instrument_id", "target", "phase"]]])
ph = ph.drop_duplicates(["instrument_id", "target"]).set_index(["instrument_id", "target"]).phase
for _, r in reg.iterrows():
    for t in r.target.split(";"):
        rows.append({"unit": "register", "id": r.instrument_id, "challenger": t, "incumbent": "US", "year": int(r.year),
                     "reach": int(r.reach), "type": r.legal_basis, "phase": ph.get((r.instrument_id, t), "n.a."),
                     "mode": mode["mode"].get(r.instrument_id, "uncoded"), **geo(t, "US", int(r.year))})
I = pd.DataFrame(rows)
GLOBAL = {"B-02", "B-17", "B-18", "B-19", "B-34", "B-31"}  # multilateral, gegen alle Lieferlaender oder undatiert
POLITICAL = {"B-32", "B-33", "B-35", "B-36"}
I["scope"] = np.where(I.id.isin(GLOBAL), "global", np.where(I.id.isin(POLITICAL), "politisch", "gezielt"))
I["era"] = np.where(I.year < 1995, "vor 1995", "ab 1995 (WTO)")
I.to_csv(D / "geopolitics_instruments.csv", index=False)

# Dyaden im Meilensteinjahr
m = pd.read_csv(D / "ds1_milestones.csv")
inc_of = {"DE": "GB", "JP": "US", "KR": "US", "CN": "US", "JPGB": "GB"}
dy = []
for _, r in m.iterrows():
    inc = "EU" if r.milestone_id.endswith("-EU") else inc_of[r.case]
    ch = "JP" if r.case == "JPGB" else r.case
    dy.append({"milestone_id": r.milestone_id, "challenger": ch, "incumbent": inc, "year": r.year, **geo(ch, inc, int(r.year))})
DY = pd.DataFrame(dy)
DY.to_csv(D / "geopolitics_dyads.csv", index=False)

out = ["Art der Massnahme nach Buendnis und Epoche (ohne 'mixed')"]
J = I[I["mode"].isin(["negotiated", "unilateral"])]
for unit, g in J.groupby("unit"):
    out.append(f"\n{unit}: {len(g)} Instrument-Ziel-Paare")
    out.append(pd.crosstab([g.era, g.defense_pact.map({1: "Verteidigungsbuendnis", 0: "kein Buendnis"})], g["mode"]).to_string())
G2 = J[(J.unit == "register") & (J.scope == "gezielt")]
out += ["", "register, nur gezielte und handelspolitisch begruendete Instrumente (ohne global, politisch, undatiert)",
        pd.crosstab([G2.era, G2.defense_pact.map({1: "Verteidigungsbuendnis", 0: "kein Buendnis"})], G2["mode"]).to_string(),
        "Ziele ab 1995: " + ", ".join(f"{r.id} {r.challenger}" for r in G2[G2.era != "vor 1995"].itertuples())]
out += ["", "Technologieverweigerung (denial) und Massnahmen vor der Verdraengung, mit Lage der Dyade"]
sel = I[(I.type == "denial") | I.phase.isin(["absorption"]) | ((I.unit == "response") & (I.phase == "absorption"))]
out.append(sel[["unit", "id", "challenger", "incumbent", "year", "reach", "mode", "phase", "defense_pact", "unga_distance", "cinc_ratio"]].to_string(index=False))
out += ["", "UNGA-Abstand und CINC-Verhaeltnis im Meilensteinjahr (Median je Fall)"]
out.append(DY.groupby(["challenger", "incumbent"])[["cinc_ratio", "unga_distance", "defense_pact"]].median().to_string())
out += ["", "UNGA-Abstand der neuen Faelle zu den USA, Mittel 2009-2023 (Taiwan nicht UN-Mitglied ab 1971)"]
for t in ["JP", "KR", "MX", "BR", "TH", "MY", "VN", "CN"]:
    v = [geo(t, "US", y)["unga_distance"] for y in range(2009, 2024)]
    p = [geo(t, "US", y)["defense_pact"] for y in range(2009, 2019)]
    out.append(f"{t}: UNGA-Abstand {np.nanmean(v):.2f}; Verteidigungsbuendnis 2009-2018 {int(np.mean(p) == 1)}")
(D / "geopolitics.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
