"""Gutachten, Folgeschritte 1 und 2: Kontrollgruppe und Gewicht verdraengter Sektoren.

Kontrollgruppe (Schritt 2): Panel aus Warengruppe und Jahr fuer alle Industriewaren-Gruppen, in denen der Aufsteiger
mindestens einmal 50 Mio. USD ausfuehrt, verdraengt oder nicht. Zustand "post" ab dem Kreuzungsjahr
(data/population_crossovers.csv). Ergebnisse: (a) Beginn einer gezielten breiten Massnahme (data/broad_register.csv;
ohne die globalen B-02, B-17, B-19), Gruppe scheidet nach dem ersten Treffer aus; (b) neue US-Antidumping- und
Ausgleichszollverfahren gegen den Aufsteiger (TTBD, Bown), ueber HS-Codes der Verfahren zugeordnet
(HS6 -> SITC ueber die WITS-Konkordanzen H0-S1 und H0-S3), nur 1988-2015, weil fruehere Verfahren keine HS-Codes tragen.
Schaetzung: Poisson mit Jahres-Effekten, Standardfehler nach Gruppe geclustert.

Gewicht (Schritt 1): Unter den verdraengten Gruppen, sagen US-Einfuhren aus dem Aufsteiger (Heimatmarkt) oder
US-Ausfuhren (Exportmaerkte) im Kreuzungsjahr eine Reaktion voraus? Logit; Beschaeftigung (NBER-CES) steht aus.
Ergebnis: data/population_panel.csv, data/population_weight.csv, data/population_panel.txt
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

D = Path(__file__).resolve().parent
s1 = pd.read_csv(D / "raw/comtrade_s1_ag3.csv", dtype={"sitc3": str}).rename(columns={"sitc3": "code"})
s3 = pd.read_csv(D / "raw/comtrade_s3_ag3.csv", dtype={"sitc3": str}).rename(columns={"sitc3": "code"})
hs = pd.read_csv(D / "raw/comtrade_hs_ag4.csv", dtype={"hs4": str}).rename(columns={"hs4": "code"})
s1["reporter"] = s1.reporter.replace({841: 842})
EXP = {"s1": s1, "s3": s3, "hs4": hs}
imp = pd.read_csv(D / "raw/comtrade_us_imports_groups.csv", dtype={"code": str})
imp["data"] = imp.cl.map({"S1": "s1", "S3": "s3", "HS": "hs4"})
REP = {"JP": 392, "KR": 410, "CN": 156}
SOURCES = [("JP", "s1"), ("KR", "s1"), ("KR", "s3"), ("CN", "s3"), ("CN", "hs4")]
GLOBAL = {"B-02", "B-17", "B-19"}
cross = pd.read_csv(D / "population_crossovers.csv", dtype={"code": str})
reg = pd.read_csv(D / "broad_register.csv", dtype=str)
reg = reg[reg.reach.astype(int) >= 4]  # only broad entries (IR 4-5) count; see register_recode.py


def manuf(data, c):
    return c[:1] in "5678" if data != "hs4" else "28" <= c[:2] <= "96"


def covers(r, data, code):
    cs = r[{"s1": "codes_s1", "s3": "codes_s3", "hs4": "codes_hs4"}[data]]
    cs = cs if isinstance(cs, str) else ""
    return cs == "ALL" or any(code.startswith(k) for k in cs.split(";") if k)


# AD/CVD-Verfahren der USA gegen JP, KR, CN mit HS-Codes -> Gruppen
conc = {}
for cl, f in (("s1", "H0_S1/JobID-9_Concordance_H0_to_S1.CSV"), ("s3", "H0_S3")):
    p = D / "raw/wits" / f
    p = p if p.is_file() else next(x for x in p.iterdir() if x.suffix.upper() == ".CSV")
    c = pd.read_csv(p, dtype=str, encoding="latin1").iloc[:, [0, 2]]
    c.columns = ["hs6", "sitc"]
    conc[cl] = c.assign(g=c.sitc.str[:3]).groupby("hs6").g.first().to_dict()
    conc[cl + "_4"] = c.assign(h4=c.hs6.str[:4], g=c.sitc.str[:3]).groupby("h4").g.agg(lambda s: s.mode().iloc[0]).to_dict()
cases = []
for f in ("raw/ttbd/gad/GAD/GAD-USA.xls", "raw/ttbd/gcvd/GCVD/GCVD-USA.xls"):
    x = pd.read_excel(D / f, sheet_name=None)
    m = next(v for k, v in x.items() if k.endswith("Master"))
    pr = next(v for k, v in x.items() if k.endswith("Products"))
    m = m[m.INV_CTY_CODE.isin(["JPN", "KOR", "CHN"])]
    yr = pd.to_datetime(m.INIT_DATE, errors="coerce").dt.year
    ch = m.INV_CTY_CODE.map({"JPN": "JP", "KOR": "KR", "CHN": "CN"})
    info = pd.DataFrame({"CASE_ID": m.CASE_ID, "year": yr, "challenger": ch})
    pr = pr[pr.HS_CODE.astype(str).str.len() >= 4].assign(hs=lambda z: z.HS_CODE.astype(str).str.split(".").str[0])
    cases.append(pr[["CASE_ID", "hs"]].merge(info, on="CASE_ID"))
cases = pd.concat(cases).dropna(subset=["year"])
cases["year"] = cases.year.astype(int)
maps = []
for data in ("s1", "s3", "hs4"):
    z = cases.copy()
    if data == "hs4":
        z["code"] = z.hs.str[:4]
    else:
        z["code"] = z.hs.str[:6].map(conc[data]).fillna(z.hs.str[:4].map(conc[data + "_4"]))
    maps.append(z.dropna(subset=["code"]).assign(data=data)[["CASE_ID", "challenger", "data", "code", "year"]].drop_duplicates())
adc = pd.concat(maps).groupby(["challenger", "data", "code", "year"]).CASE_ID.nunique().rename("ad_cases").reset_index()

panel = []
for tgt, data in SOURCES:
    df = EXP[data]
    x = df[df.reporter == REP[tgt]].groupby(["code", "year"]).value.sum().rename("x_ch")
    u = df[df.reporter == 842].groupby(["code", "year"]).value.sum().rename("x_us")
    g = pd.concat([x, u], axis=1).fillna(0).reset_index()
    g = g[g.code.apply(lambda c: manuf(data, c))]
    rel = g.groupby("code").x_ch.max()
    g = g[g.code.isin(rel[rel >= 5e7].index)]
    cr = cross[(cross.challenger == tgt) & (cross.data == data)].set_index("code").crossover_year
    g["crossover_year"] = g.code.map(cr)
    g["post"] = (g.year >= g.crossover_year).astype(int)
    g["rel"] = g.year - g.crossover_year
    hits = {c: sorted(int(r.year) for _, r in reg.iterrows() if tgt in r.target.split(";") and r.instrument_id not in GLOBAL and covers(r, data, c)) for c in g.code.unique()}
    hits_x = {c: sorted(int(r.year) for _, r in reg.iterrows() if tgt in r.target.split(";") and r.instrument_id not in GLOBAL | {"B-20"} and covers(r, data, c)) for c in g.code.unique()}
    g["broad"] = [int(y in hits[c]) for c, y in zip(g.code, g.year)]
    g["broad_x301"] = [int(y in hits_x[c]) for c, y in zip(g.code, g.year)]
    g["at_risk"] = [int(not any(h < y for h in hits[c])) for c, y in zip(g.code, g.year)]
    g["at_risk_x301"] = [int(not any(h < y for h in hits_x[c])) for c, y in zip(g.code, g.year)]
    g = g.merge(adc[(adc.challenger == tgt) & (adc.data == data)][["code", "year", "ad_cases"]], on=["code", "year"], how="left").fillna({"ad_cases": 0})
    im = imp[(imp.partner == REP[tgt]) & (imp.data == data)].groupby(["code", "year"]).value.sum().rename("m_us").reset_index()
    g = g.merge(im, on=["code", "year"], how="left").fillna({"m_us": 0})
    g["challenger"], g["data"] = tgt, data
    panel.append(g)
P = pd.concat(panel, ignore_index=True)
P["src"] = P.challenger + "_" + P.data
P["lx_ch"] = np.log1p(P.x_ch / 1e6)
P.to_csv(D / "population_panel.csv", index=False)

out = ["Kontrollgruppe: Panel Warengruppe x Jahr (Gruppen mit Ausfuhren des Aufsteigers >= 50 Mio. USD)"]
for s, g in P.groupby("src"):
    out.append(f"{s}: {g.code.nunique()} Gruppen, davon verdraengt {g[g.crossover_year.notna()].code.nunique()}; Jahre {g.year.min()}-{g.year.max()}")


def poisson(df, y, label, extra=""):
    if df[y].sum() < 3 or df.post.nunique() < 2:
        out.append(f"{label}: zu wenige Ereignisse ({int(df[y].sum())})"); return None
    pre, post = df[df.post == 0], df[df.post == 1]
    r0, r1 = pre[y].sum() / len(pre) * 100, post[y].sum() / len(post) * 100
    try:
        m = smf.glm(f"{y} ~ post + C(year){extra}", data=df, family=sm.families.Poisson()).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(df.src + df.code)[0]})
        b, se = m.params["post"], m.bse["post"]
        res = f"IRR {np.exp(b):.2f} (95 % KI {np.exp(b-1.96*se):.2f}-{np.exp(b+1.96*se):.2f}), p={m.pvalues['post']:.3f}"
    except Exception as e:
        res = f"Schaetzung nicht moeglich ({type(e).__name__})"
    out.append(f"{label}: je 100 Gruppenjahre vor {r0:.2f} ({int(pre[y].sum())} Ereignisse, {len(pre)} Gj.), nach {r1:.2f} ({int(post[y].sum())}, {len(post)}); {res}")
    return res


out += ["", "(a) Beginn gezielter breiter Massnahmen, Gruppen bis zum ersten Treffer"]
jk = P[P.challenger.isin(["JP", "KR"]) & (P.data == "s1") & (P.at_risk == 1)].copy()
jk["year"] = jk.year.astype(str) + jk.challenger
poisson(jk, "broad", "JP und KR, SITC Rev. 1, 1962-1999")
cn = P[(P.challenger == "CN") & (P.at_risk_x301 == 1)].copy()
cn["year"] = cn.year.astype(str) + cn.data
poisson(cn, "broad_x301", "CN ohne 301-Zoelle (s3 und hs4)")
c18 = P[(P.challenger == "CN") & (P.data == "hs4") & (P.year == 2018)]
out.append(f"CN hs4, 301-Zoelle 2018: erfasst {c18.broad.sum()} von {len(c18)} Gruppen; davon verdraengt {int(c18[c18.post==1].broad.sum())} von {int(c18.post.sum())}, nicht verdraengt {int(c18[c18.post==0].broad.sum())} von {int((c18.post==0).sum())}")

out += ["", "(b) Neue US-AD/CVD-Verfahren gegen den Aufsteiger, 1988-2015"]
A = P[(P.year >= 1988) & (P.year <= 2015)].copy()
A["year"] = A.year.astype(str) + A.src
for s, g in A.groupby("src"):
    poisson(g, "ad_cases", s, " + lx_ch")
poisson(A, "ad_cases", "alle zusammen (Jahr x Quelle, mit Groesse der Ausfuhren)", " + lx_ch")
poisson(A, "ad_cases", "alle zusammen, ohne Groessenkontrolle")
# Ereignisstudie: Raten nach Abstand zur Kreuzung
A["bin"] = pd.cut(A.rel, [-99, -6, -1, 4, 9, 99], labels=["<=-6", "-5..-1", "0..4", "5..9", ">=10"]).astype(str)
A.loc[A.crossover_year.isna(), "bin"] = "nie"
es = A.groupby("bin").agg(gj=("ad_cases", "size"), faelle=("ad_cases", "sum"))
es["je100"] = (es.faelle / es.gj * 100).round(2)
out += ["Ereignisstudie (Jahre relativ zur Kreuzung):", es.reindex(["nie", "<=-6", "-5..-1", "0..4", "5..9", ">=10"]).to_string()]

# Gewicht: unter den verdraengten Gruppen (ohne Linkszensierung)
W = []
for (tgt, data, code), g in P[P.crossover_year.notna()].groupby(["challenger", "data", "code"]):
    cy = int(g.crossover_year.iloc[0])
    if cy == g.year.min():
        continue
    row = g[g.year == cy].iloc[0]
    w = {"challenger": tgt, "data": data, "code": code, "crossover_year": cy, "src": tgt + "_" + data,
         "l_m_us": np.log1p(row.m_us / 1e6), "l_x_us": np.log1p(row.x_us / 1e6), "l_x_ch": np.log1p(row.x_ch / 1e6),
         "broad10": int(g[(g.year >= cy) & (g.year <= cy + 10)].broad.sum() > 0),
         "broad10_x301": int(g[(g.year >= cy) & (g.year <= cy + 10)].broad_x301.sum() > 0)}
    ad = g[(g.year >= max(cy, 1988)) & (g.year <= min(cy + 5, 2015))]
    w["ad5"] = int(ad.ad_cases.sum() > 0) if (cy + 5 >= 1988 and cy <= 2015) else np.nan
    W.append(w)
W = pd.DataFrame(W)
W.to_csv(D / "population_weight.csv", index=False)
out += ["", "Gewicht: Logit unter verdraengten Gruppen; Regressoren in log Mio. USD im Kreuzungsjahr"]
for y, sub, lab in (("broad10", W[W.data == "s1"], "breite Massnahme binnen 10 J., JP und KR (s1)"),
                    ("ad5", W.dropna(subset=["ad5"]), "AD/CVD-Verfahren binnen 5 J., alle Quellen")):
    try:
        fe = " + C(src)" if sub.src.nunique() > 1 else ""
        m = smf.glm(f"{y} ~ l_m_us + l_x_us + l_x_ch{fe}", data=sub, family=sm.families.Binomial()).fit(cov_type="HC1")
        coef = "; ".join(f"{k} {m.params[k]:+.2f} (p={m.pvalues[k]:.3f})" for k in ("l_m_us", "l_x_us", "l_x_ch"))
        out.append(f"{lab}: N={len(sub)}, Anteil {sub[y].mean():.2f}; {coef}")
        sub = sub.assign(t=pd.qcut(sub.l_m_us.rank(method="first"), 3, labels=["niedrig", "mittel", "hoch"]))
        out.append("   nach Terzil der US-Einfuhren aus dem Aufsteiger: " + ", ".join(f"{k} {v:.2f}" for k, v in sub.groupby("t", observed=True)[y].mean().items()))
    except Exception as e:
        out.append(f"{lab}: Schaetzung nicht moeglich ({type(e).__name__}: {e})")
(D / "population_panel.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
