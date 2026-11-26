"""Weitere Faelle gegen die USA: Gegenfaelle (Thailand, Vietnam, Malaysia, Mexiko) und neue Verdraengungsfaelle
(Taiwan, Brasilien, Hongkong), mit derselben Regel wie population_test.py und population_panel.py.

Verdraengung: erstes Jahr, in dem die Weltausfuhren des Aufsteigers in einer Warengruppe die der USA erreichen und in
mindestens 3 der 4 Folgejahre darueber bleiben; Mindestgroesse 50 Mio. USD (Funktion wie in population_test.py).
Daten (data/cases_fetch.py): SITC Rev. 1 1962-1999, SITC Rev. 3 1992-2009, HS4 2008-2023.
- Taiwan SITC: Spiegeldaten (Einfuhren aller Meldelaender aus 490 gegen Einfuhren aus den USA); Taiwan HS: eigene Meldung.
- Hongkong: Ausfuhren ohne Wiederausfuhren (X minus RX); HS nur bis 2016, weil RX danach fehlt.
Breite der Verdraengung: Anteil der Industriewaren-Ausfuhren des Aufsteigers in Gruppen, in denen er die USA
erreicht (je Jahr); zum Vergleich Japan, Korea, China aus den Rohdaten von population_fetch*.py, falls vorhanden.
Gefahrenrate und Kontrollgruppe: breite Massnahmen aus data/broad_register.csv (gezielt, ohne globale Massnahmen);
AD/CVD-Verfahren der USA aus TTBD (Bown), 1988-2015, ueber HS-Codes und WITS-Konkordanz.
Ergebnis: data/cases_crossovers.csv, data/cases_breadth.csv, data/cases_hazard.csv, data/cases_panel.txt
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

D = Path(__file__).resolve().parent
R = D / "raw"
NEW = {"TH": 764, "VN": 704, "MY": 458, "MX": 484, "BR": 76, "HK": 344, "TW": 490}
OLD = {"JP": 392, "KR": 410, "CN": 156}
TTBD = {"THA": "TH", "VNM": "VN", "MYS": "MY", "MEX": "MX", "BRA": "BR", "HKG": "HK", "TWN": "TW",
        "JPN": "JP", "KOR": "KR", "CHN": "CN"}
DATA = {"S1": "s1", "S3": "s3", "HS": "hs4"}
GLOBAL = {"B-02", "B-17", "B-19", "B-34"}  # multilateral oder gegen alle Lieferlaender (siehe population_test.py); B-34 Zoelle gegen alle Partner
GLOBAL |= {"B-31"}  # Fortsetzung 1994-2004; Erstabkommen als B-37 bis B-42 erfasst, nicht doppelt in der Gefahrenrate
POLITICAL = {"B-32", "B-33", "B-35", "B-36"}  # nicht handelspolitisch begruendet (Autonomie HK, Migration/Fentanyl, Bolsonaro)


def manuf(data, c):
    return c[:1] in "5678" if data != "hs4" else "28" <= c[:2] <= "96"


def crossover(ch, us, min_val=5e7):
    yrs = sorted(set(ch.index) & set(us.index))
    for i, y in enumerate(yrs):
        if ch[y] >= us[y] and ch[y] >= min_val:
            nxt = [yy for yy in yrs[i + 1:i + 5]]
            if len(nxt) < 2 or sum(ch[yy] >= us[yy] for yy in nxt) >= min(3, len(nxt)):
                return y, (y == yrs[0])
    return None, False


# ---- Reihen je Aufsteiger und Datensatz: Tabelle code, year, x_ch, x_us
ex = pd.read_csv(R / "cases_exports.csv", dtype={"code": str})
ex["data"] = ex.cl.map(DATA)
ex["reporter"] = ex.reporter.replace({841: 842})
us_direct = ex[ex.reporter == 842].groupby(["data", "code", "year"]).value.sum()
mir = pd.read_csv(R / "cases_mirror_tw.csv", dtype={"code": str})
mir["data"] = mir.cl.map(DATA)
rx = pd.read_csv(R / "cases_hk_reexports.csv", dtype={"code": str})
rx["data"] = rx.cl.map(DATA)
SER = {}
for tgt, rep in NEW.items():
    for data in ("s1", "s3", "hs4"):
        if tgt == "TW" and data != "hs4":
            m = mir[mir.data == data]
            ch = m[m.partner == 490].groupby(["code", "year"]).value.sum()
            us = m[m.partner.isin([841, 842])].groupby(["code", "year"]).value.sum()
        else:
            ch = ex[(ex.reporter == rep) & (ex.data == data)].groupby(["code", "year"]).value.sum()
            if tgt == "HK":
                r = rx[rx.data == data].groupby(["code", "year"]).value.sum()
                yrs_rx = set(rx[rx.data == data].year)
                ch = ch[ch.index.get_level_values("year").isin(yrs_rx)]
                ch = (ch - r.reindex(ch.index).fillna(0)).clip(lower=0)
            us = us_direct.loc[data] if data in us_direct.index.get_level_values(0) else pd.Series(dtype=float)
        if len(ch) == 0:
            continue
        g = pd.concat([ch.rename("x_ch"), us.rename("x_us")], axis=1)
        g = g[g.index.get_level_values("year").isin(set(ch.index.get_level_values("year")))].fillna(0).reset_index()
        g = g[g.code.apply(lambda c: manuf(data, c))]
        SER[(tgt, data)] = g
# alte Faelle zum Vergleich der Breite (Rohdaten aus population_fetch*.py)
try:
    old = {"s1": pd.read_csv(R / "comtrade_s1_ag3.csv", dtype={"sitc3": str}).rename(columns={"sitc3": "code"}),
           "s3": pd.read_csv(R / "comtrade_s3_ag3.csv", dtype={"sitc3": str}).rename(columns={"sitc3": "code"}),
           "hs4": pd.read_csv(R / "comtrade_hs_ag4.csv", dtype={"hs4": str}).rename(columns={"hs4": "code"})}
    old["s1"]["reporter"] = old["s1"].reporter.replace({841: 842})
    for tgt, data in [("JP", "s1"), ("KR", "s1"), ("KR", "s3"), ("CN", "s3"), ("CN", "hs4")]:
        df = old[data]
        x = df[df.reporter == OLD[tgt]].groupby(["code", "year"]).value.sum().rename("x_ch")
        u = df[df.reporter == 842].groupby(["code", "year"]).value.sum().rename("x_us")
        g = pd.concat([x, u], axis=1).fillna(0).reset_index()
        SER[(tgt, data)] = g[g.code.apply(lambda c: manuf(data, c))]
except FileNotFoundError:
    print("Rohdaten Japan/Korea/China fehlen; Breitenvergleich nur fuer neue Faelle")

# ---- Kreuzungen und Breite
cross, breadth = [], []
for (tgt, data), g in SER.items():
    for c, s in g.groupby("code"):
        y, left = crossover(s.set_index("year").x_ch, s.set_index("year").x_us)
        if y is not None:
            cross.append({"challenger": tgt, "data": data, "code": c, "crossover_year": y, "left_censored": left})
    for y, s in g.groupby("year"):
        tot = s.x_ch.sum()
        breadth.append({"challenger": tgt, "data": data, "year": y, "manuf_exports_musd": round(tot / 1e6),
                        "us_manuf_exports_musd": round(s.x_us.sum() / 1e6),
                        "share_in_groups_above_us": round(s[s.x_ch >= s.x_us].x_ch.sum() / tot, 3) if tot else np.nan,
                        "groups_above_us_50m": int(((s.x_ch >= s.x_us) & (s.x_ch >= 5e7)).sum()),
                        # Reichweite aus Sicht des Etablierten: Anteil der US-Industrieausfuhren in Gruppen, die der Aufsteiger erreicht
                        "us_exports_share_overtaken": round(s[(s.x_ch >= s.x_us) & (s.x_ch >= 5e7)].x_us.sum() / s.x_us.sum(), 3) if s.x_us.sum() else np.nan})
CR = pd.DataFrame(cross)
CR.to_csv(D / "cases_crossovers.csv", index=False)
B = pd.DataFrame(breadth)
B.to_csv(D / "cases_breadth.csv", index=False)

out = ["Breite der Verdraengung: Anteil der Industriewaren-Ausfuhren in Gruppen mit Ausfuhren >= USA",
       "(Spitzenwert, Jahr; letzte Beobachtung; Anzahl Gruppen >= 50 Mio. USD ueber den USA im Spitzenjahr)"]
for (tgt, data), b in B.groupby(["challenger", "data"]):
    b = b[b.manuf_exports_musd >= 500]
    if not len(b):
        continue
    pk = b.loc[b.share_in_groups_above_us.idxmax()]
    last = b.iloc[-1]
    pu = b.loc[b.us_exports_share_overtaken.idxmax()]
    out.append(f"{tgt} {data}: Anteil der US-Industrieausfuhren in ueberholten Gruppen: Spitze {pu.us_exports_share_overtaken:.3f} ({int(pu.year)}), zuletzt {last.us_exports_share_overtaken:.3f}")
    out.append(f"{tgt} {data}: Spitze {pk.share_in_groups_above_us:.2f} ({int(pk.year)}, {int(pk.groups_above_us_50m)} Gruppen); "
               f"zuletzt {last.share_in_groups_above_us:.2f} ({int(last.year)}); Ausfuhren/US-Ausfuhren zuletzt "
               f"{last.manuf_exports_musd / last.us_manuf_exports_musd:.2f}")

# ---- Register und Gefahrenrate
reg = pd.read_csv(D / "broad_register.csv", dtype=str)
reg = reg[reg.reach.astype(int) >= 4]  # only broad entries (IR 4-5) count; see register_recode.py


def covers(r, data, code):
    cs = r[{"s1": "codes_s1", "s3": "codes_s3", "hs4": "codes_hs4"}[data]]
    cs = cs if isinstance(cs, str) else ""
    return cs == "ALL" or any(code.startswith(k) for k in cs.split(";") if k)


def hits(tgt, data, code, excl=frozenset()):
    return sorted(int(r.year) for _, r in reg.iterrows()
                  if tgt in r.target.split(";") and r.instrument_id not in GLOBAL | excl and covers(r, data, code))


# Befund 2 fuer die neuen Ziele: Kreuzungsjahr der von jeder Massnahme erfassten Gruppen (wie population_test.py)
SERX = {k: v.groupby("year")[["x_ch", "x_us"]] for k, v in SER.items()}
rows = []
for _, r in reg.iterrows():
    for tgt in r.target.split(";"):
        if tgt not in NEW:
            continue
        best = None
        for data in ("s1", "s3", "hs4"):
            cs = r[{"s1": "codes_s1", "s3": "codes_s3", "hs4": "codes_hs4"}[data]]
            if not isinstance(cs, str) or (tgt, data) not in SER:
                continue
            g = SER[(tgt, data)]
            g = g if cs == "ALL" else g[g.code.apply(lambda c: any(c.startswith(k) for k in cs.split(";")))]
            t = g.groupby("year")[["x_ch", "x_us"]].sum()
            y, left = crossover(t.x_ch, t.x_us)
            first = int(t.index.min()) if len(t) else None
            if y is not None or best is None or (best[1] is None and first <= int(r.year)):
                best = (data, y, left, first)
            if y is not None:
                break
        data, y, left, first = best if best else (None, None, False, None)
        iy = int(r.year)
        if y is None:
            ph = "keine Kreuzung in den Daten" if (first is not None and first <= iy) else "vor Datenbeginn"
        elif left:
            ph = "post (Kreuzung spaetestens im ersten Datenjahr)" if iy >= y else "unbestimmt"
        else:
            ph = "post" if iy >= y else "absorption"
        rows.append({"instrument_id": r.instrument_id, "year": iy, "target": tgt, "reach": r.reach, "data": data,
                     "crossover_year": y, "first_data_year": first, "phase": ph})
T = pd.DataFrame(rows)
T.to_csv(D / "cases_register_tested.csv", index=False)
out += ["", "Breite Massnahmen gegen die neuen Ziele: Phase gegen die Kreuzung der erfassten Gruppen"]
out += [T.to_string(index=False)]

q = CR[~CR.left_censored & CR.challenger.isin(NEW)].copy() if len(CR) else CR
H = []
for _, g in q.iterrows():
    ys = hits(g.challenger, g.data, g.code)
    ys_t = hits(g.challenger, g.data, g.code, frozenset(POLITICAL))
    ys_s = hits(g.challenger, g.data, g.code, frozenset(POLITICAL | {"B-29"}))
    H.append({**g.to_dict(), "broad_within10": any(g.crossover_year <= y <= g.crossover_year + 10 for y in ys),
              "broad_within10_sector": any(g.crossover_year <= y <= g.crossover_year + 10 for y in ys_s),
              "broad_within10_trade": any(g.crossover_year <= y <= g.crossover_year + 10 for y in ys_t),
              "broad_before": any(y < g.crossover_year for y in ys)})
H = pd.DataFrame(H)
H.to_csv(D / "cases_hazard.csv", index=False)
out += ["", "Verdraengte Industriewaren-Gruppen (Kreuzung nicht im ersten Datenjahr) und Gefahrenrate gezielter breiter Massnahmen (10 Jahre)"]
for tgt in NEW:
    for data in ("s1", "s3", "hs4"):
        g = H[(H.challenger == tgt) & (H.data == data)] if len(H) else H
        n_all = len(SER[(tgt, data)].code.unique()) if (tgt, data) in SER else 0
        if (tgt, data) not in SER:
            continue
        if len(g):
            yrs = f"Jahre {int(g.crossover_year.min())}-{int(g.crossover_year.max())}; "
            out.append(f"{tgt} {data}: {len(g)} von {n_all} Gruppen verdraengt; {yrs}breit binnen 10 J. {g.broad_within10.mean():.2f}, ohne politisch begruendete {g.broad_within10_trade.mean():.2f}, ohne GSP-Graduierung {g.broad_within10_sector.mean():.2f}; breit schon vorher {int(g.broad_before.sum())}")
        else:
            out.append(f"{tgt} {data}: 0 von {n_all} Gruppen verdraengt")

# ---- AD/CVD aus TTBD: Gruppen x Jahr
conc = {}
for cl, f in (("s1", "H0_S1"), ("s3", "H0_S3")):
    p = next(x for x in (R / "wits" / f).iterdir() if x.suffix.upper() == ".CSV")
    c = pd.read_csv(p, dtype=str, encoding="latin1").iloc[:, [0, 2]]
    c.columns = ["hs6", "sitc"]
    conc[cl] = c.assign(g=c.sitc.str[:3]).groupby("hs6").g.first().to_dict()
    conc[cl + "_4"] = c.assign(h4=c.hs6.str[:4], g=c.sitc.str[:3]).groupby("h4").g.agg(lambda s: s.mode().iloc[0]).to_dict()
cases, allcases = [], []
for f in ("ttbd/gad/GAD/GAD-USA.xls", "ttbd/gcvd/GCVD/GCVD-USA.xls"):
    x = pd.read_excel(R / f, sheet_name=None)
    m = next(v for k, v in x.items() if k.endswith("Master"))
    pr = next(v for k, v in x.items() if k.endswith("Products"))
    m = m[m.INV_CTY_CODE.isin(list(TTBD))]
    yr = pd.to_datetime(m.INIT_DATE, errors="coerce").dt.year
    info = pd.DataFrame({"CASE_ID": m.CASE_ID, "year": yr, "challenger": m.INV_CTY_CODE.map(TTBD), "file": f.split("/")[1]})
    allcases.append(info)
    pr = pr[pr.HS_CODE.astype(str).str.len() >= 4].assign(hs=lambda z: z.HS_CODE.astype(str).str.split(".").str[0])
    cases.append(pr[["CASE_ID", "hs"]].merge(info, on="CASE_ID"))
allc = pd.concat(allcases, ignore_index=True).dropna(subset=["year"])
cases = pd.concat(cases).dropna(subset=["year"])
cases["year"] = cases.year.astype(int)
maps = []
for data in ("s1", "s3", "hs4"):
    z = cases.copy()
    z["code"] = z.hs.str[:4] if data == "hs4" else z.hs.str[:6].map(conc[data]).fillna(z.hs.str[:4].map(conc[data + "_4"]))
    maps.append(z.dropna(subset=["code"]).assign(data=data)[["CASE_ID", "challenger", "data", "code", "year"]].drop_duplicates())
adc = pd.concat(maps).groupby(["challenger", "data", "code", "year"]).CASE_ID.nunique().rename("ad_cases").reset_index()
out += ["", "US-AD/CVD-Verfahren gegen die Faelle (TTBD, Einleitungsjahr; alle Verfahren, mit und ohne HS-Codes)",
        pd.crosstab(allc.challenger, pd.cut(allc.year, [1977, 1989, 1999, 2009, 2015])).to_string()]

# ---- Kontrollgruppe: Panel Gruppe x Jahr, Gruppen mit Ausfuhren des Aufsteigers >= 50 Mio. USD
P = []
for (tgt, data), g in SER.items():
    if tgt not in NEW:
        continue
    g = g.copy()
    rel = g.groupby("code").x_ch.max()
    g = g[g.code.isin(rel[rel >= 5e7].index)]
    cr = CR[(CR.challenger == tgt) & (CR.data == data)].set_index("code").crossover_year if len(CR) else pd.Series(dtype=float)
    g["crossover_year"] = g.code.map(cr)
    g["post"] = (g.year >= g.crossover_year).astype(int)
    hh = {c: hits(tgt, data, c) for c in g.code.unique()}
    g["broad"] = [int(y in hh[c]) for c, y in zip(g.code, g.year)]
    g["at_risk"] = [int(not any(h < y for h in hh[c])) for c, y in zip(g.code, g.year)]
    g = g.merge(adc[(adc.challenger == tgt) & (adc.data == data)][["code", "year", "ad_cases"]], on=["code", "year"], how="left").fillna({"ad_cases": 0})
    g["challenger"], g["data"] = tgt, data
    P.append(g)
P = pd.concat(P, ignore_index=True)
P["src"] = P.challenger + "_" + P.data
P["lx_ch"] = np.log1p(P.x_ch / 1e6)
P.to_csv(D / "cases_panel.csv", index=False)
out += ["", "Kontrollgruppe: Panel Warengruppe x Jahr"]
for s, g in P.groupby("src"):
    out.append(f"{s}: {g.code.nunique()} Gruppen, davon verdraengt {g[g.crossover_year.notna()].code.nunique()}; Jahre {g.year.min()}-{g.year.max()}; breite Massnahmen {int(g.broad.sum())}; AD/CVD {int(g.ad_cases.sum())}")


def poisson(df, y, label, extra=""):
    df = df.copy()
    for c in ("year", "src", "code"):
        df[c] = df[c].astype(object)  # patsy kennt den neuen pandas-Stringtyp nicht
    if df[y].sum() < 3 or df.post.nunique() < 2:
        out.append(f"{label}: zu wenige Ereignisse ({int(df[y].sum())}) oder keine Variation in post"); return
    pre, post = df[df.post == 0], df[df.post == 1]
    r0, r1 = pre[y].sum() / len(pre) * 100, post[y].sum() / len(post) * 100
    try:
        m = smf.glm(f"{y} ~ post + C(year){extra}", data=df, family=sm.families.Poisson()).fit(
            cov_type="cluster", cov_kwds={"groups": pd.factorize(df.src + df.code)[0]})
        b, se = m.params["post"], m.bse["post"]
        res = f"IRR {np.exp(b):.2f} (95 % KI {np.exp(b-1.96*se):.2f}-{np.exp(b+1.96*se):.2f}), p={m.pvalues['post']:.3f}"
    except Exception as e:
        res = f"Schaetzung nicht moeglich ({type(e).__name__}: {str(e)[:200]})"
    out.append(f"{label}: je 100 Gruppenjahre vor {r0:.2f} ({int(pre[y].sum())} Ereignisse, {len(pre)} Gj.), nach {r1:.2f} ({int(post[y].sum())}, {len(post)}); {res}")


out += ["", "(a) Beginn gezielter breiter Massnahmen (Gruppen bis zum ersten Treffer), Jahr x Quelle"]
A = P[P.at_risk == 1].copy()
A["year"] = A.year.astype(str) + A.src
poisson(A, "broad", "alle neuen Faelle")
poisson(A[A.challenger.isin(["TW", "HK", "BR"])], "broad", "TW, HK, BR")
hs = {(t, d, c): hits(t, d, c, frozenset({"B-29"})) for t, d, c in P[["challenger", "data", "code"]].drop_duplicates().itertuples(index=False)}
P["broad_s"] = [int(y in hs[(t, d, c)]) for t, d, c, y in zip(P.challenger, P.data, P.code, P.year)]
P["at_risk_s"] = [int(not any(h < y for h in hs[(t, d, c)])) for t, d, c, y in zip(P.challenger, P.data, P.code, P.year)]
A = P[P.at_risk_s == 1].copy()
A["year"] = A.year.astype(str) + A.src
poisson(A, "broad_s", "alle neuen Faelle, ohne GSP-Graduierung (sektorale Massnahmen)")
out += ["", "(b) Neue US-AD/CVD-Verfahren, 1988-2015, Jahr x Quelle"]
Q = P[(P.year >= 1988) & (P.year <= 2015)].copy()
Q["year"] = Q.year.astype(str) + Q.src
for s, g in Q.groupby("challenger"):
    poisson(g, "ad_cases", s, " + lx_ch")
poisson(Q, "ad_cases", "alle neuen Faelle, mit Groesse der Ausfuhren", " + lx_ch")
poisson(Q, "ad_cases", "alle neuen Faelle, ohne Groessenkontrolle")
(D / "cases_panel.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
