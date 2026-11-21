"""Gutachten Befunde 1 und 2: Population verdraengter Sektoren und vollstaendige Liste breiter US-Massnahmen.

Verdraengung (Exportregel): erstes Jahr, in dem die Weltausfuhren des Aufsteigers in einer Warengruppe die
der USA erreichen und in mindestens 3 der folgenden 4 Jahre darueber bleiben; Mindestgroesse 50 Mio. USD.
Daten: Comtrade SITC Rev.1 (Japan, Korea 1962-1999), SITC Rev.3 (China, Korea 1992-2009), HS4 (China 2008-2023).
Befund 2: Fuer jede breite Massnahme (data/broad_register.csv) und jedes Zielland: Kreuzungsjahr der
betroffenen Warengruppen. Befund 1: Anteil der verdraengten Industriewaren-Gruppen, denen binnen 10 Jahren
eine breite Massnahme folgte.
Ergebnis: data/population_crossovers.csv, data/broad_register_tested.csv, data/population_test.txt
"""
from pathlib import Path
import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
s1 = pd.read_csv(D / "raw/comtrade_s1_ag3.csv", dtype={"sitc3": str})
s3 = pd.read_csv(D / "raw/comtrade_s3_ag3.csv", dtype={"sitc3": str})
hs = pd.read_csv(D / "raw/comtrade_hs_ag4.csv", dtype={"hs4": str})
s1["reporter"] = s1.reporter.replace({841: 842})
REP = {"JP": 392, "KR": 410, "CN": 156}
SRC = {"JP": [("s1", s1, "sitc3")], "KR": [("s1", s1, "sitc3"), ("s3", s3, "sitc3")], "CN": [("s3", s3, "sitc3"), ("hs4", hs, "hs4")]}


def series(df, col, rep, codes):
    if codes == ["ALL"]:
        x = df[(df.reporter == rep) & df[col].str[:1].isin(list("5678") if col == "sitc3" else list("23456789"))]
    else:
        x = df[(df.reporter == rep) & df[col].apply(lambda c: any(c.startswith(k) for k in codes))]
    return x.groupby("year").value.sum()


def crossover(ch, us, min_val=5e7):
    yrs = sorted(set(ch.index) & set(us.index))
    for i, y in enumerate(yrs):
        if ch[y] >= us[y] and ch[y] >= min_val:
            nxt = [yy for yy in yrs[i + 1:i + 5]]
            if len(nxt) < 2 or sum(ch[yy] >= us[yy] for yy in nxt) >= min(3, len(nxt)):
                return y, (y == yrs[0])
    return None, False


# Befund 2: breite Massnahmen
reg = pd.read_csv(D / "broad_register.csv", dtype=str)
rows = []
for _, r in reg.iterrows():
    for tgt in r.target.split(";"):
        best = None
        for name, df, col in SRC[tgt]:
            key = {"s1": "codes_s1", "s3": "codes_s3", "hs4": "codes_hs4"}[name]
            codes = r[key] if isinstance(r[key], str) else ""
            if not codes:
                continue
            ch = series(df, col, REP[tgt], codes.split(";"))
            us = series(df, col, 842, codes.split(";"))
            y, left = crossover(ch, us)
            first = int(min(ch.index)) if len(ch) else None
            if y is not None or best is None:
                best = (name, y, left, first)
            if y is not None:
                break
        name, y, left, first = best if best else (None, None, False, None)
        iy = int(r.year)
        if y is None:
            status = "keine Kreuzung in den Daten" if (first is not None and first <= iy) else "vor Datenbeginn"
        elif left:
            status = "post (Kreuzung spaetestens im ersten Datenjahr)" if iy >= y else "unbestimmt (Daten beginnen nach Massnahme)"
        else:
            status = "post" if iy >= y else "absorption"
        rows.append({"instrument_id": r.instrument_id, "year": iy, "target": tgt, "instrument": r.instrument, "mss": r.mss,
                     "data": name, "crossover_year": y, "left_censored": left, "first_data_year": first, "phase": status})
t = pd.DataFrame(rows)
t.to_csv(D / "broad_register_tested.csv", index=False)

# Befund 1: Population verdraengter Gruppen (3-Steller Industriewaren; HS4 Kapitel 28-96)
pop = []
for tgt in REP:
    for name, df, col in SRC[tgt]:
        codes = sorted(df[col].unique())
        codes = [c for c in codes if (c[:1] in "5678" if col == "sitc3" else "28" <= c[:2] <= "96")]
        for c in codes:
            ch, us = series(df, col, REP[tgt], [c]), series(df, col, 842, [c])
            y, left = crossover(ch, us)
            if y is not None:
                pop.append({"challenger": tgt, "data": name, "code": c, "crossover_year": y, "left_censored": left})
p = pd.DataFrame(pop)
p.to_csv(D / "population_crossovers.csv", index=False)

out = ["Befund 2: breite Massnahmen gegen den verdraengenden Aufsteiger"]
out += [t.phase.value_counts().to_string()]
out += [t[["instrument_id", "year", "target", "crossover_year", "phase"]].to_string(index=False)]
out += ["", "Befund 1: verdraengte Warengruppen (Kreuzung nicht im ersten Datenjahr)"]
q = p[~p.left_censored]
for (tgt, name), g in q.groupby(["challenger", "data"]):
    out.append(f"{tgt} {name}: {len(g)} Gruppen mit Kreuzung, Jahre {g.crossover_year.min()}-{g.crossover_year.max()}")
(D / "population_test.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))


# Gefahrenrate: Folgte der Verdraengung einer Gruppe binnen 10 Jahren eine gezielte breite Massnahme?
GLOBAL = {"B-02", "B-17", "B-19"}  # multilateral oder gegen alle Lieferlaender, nicht gezielt
def covers(r, data, code):
    key = {"s1": "codes_s1", "s3": "codes_s3", "hs4": "codes_hs4"}[data]
    cs = r[key] if isinstance(r[key], str) else ""
    return cs == "ALL" or any(code.startswith(k) for k in cs.split(";") if k)
haz = []
for _, g in q.iterrows():
    hits = [r for _, r in reg.iterrows() if g.challenger in r.target.split(";") and r.instrument_id not in GLOBAL and covers(r, g.data, g.code)]
    yrs = [int(r.year) for r in hits]
    haz.append({**g.to_dict(),
                "broad_within10": any(g.crossover_year <= y <= g.crossover_year + 10 for y in yrs),
                "broad_within10_excl_301": any(g.crossover_year <= y <= g.crossover_year + 10 for y, r in zip(yrs, hits) if r.instrument_id != "B-20"),
                "broad_before": any(y < g.crossover_year for y in yrs)})
h = pd.DataFrame(haz)
h.to_csv(D / "population_hazard.csv", index=False)
out2 = ["", "Gefahrenrate gezielter breiter Massnahmen nach Verdraengung (10 Jahre)"]
for (tgt, name), g in h.groupby(["challenger", "data"]):
    out2.append(f"{tgt} {name}: {len(g)} Gruppen; breit binnen 10 J. {g.broad_within10.mean():.2f}; ohne 301-Zoelle {g.broad_within10_excl_301.mean():.2f}; breit schon vorher {int(g.broad_before.sum())}")
with open(D / "population_test.txt", "a", encoding="utf-8") as f:
    f.write("\n".join(out2) + "\n")
print("\n".join(out2))
